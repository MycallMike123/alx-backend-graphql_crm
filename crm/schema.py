import re
from time import timezone


import graphene
from graphene_django.filter import DjangoFilterConnectionField
from rest_framework import status

from .models import Customer, Product, Order
from .types import CustomerType, BulkCustomerInput, ProductType, OrderType
from .filters import CustomerFilter, ProductFilter, OrderFilter


#  Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already in use")

        if phone not in re.match(r"^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$", phone):
            raise Exception("Invalid phone number")
        customer = Customer.objects.create(name=name, email=email, phone=phone or "")

        return CreateCustomer(
            customer=customer,
            message="Created successfully",
        )


class CreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(BulkCustomerInput)

    success = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []

        for customer in customers:
            try:
                if Customer.objects.filter(email=customer.email).exists():
                    raise ValueError(f"Email already exists {customer.email}")
                if customer.phone and not re.match(
                    r"^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$", customer.phone
                ):
                    raise ValueError(f"Invalid phone number {customer.phone}")
                created.append(Customer.objects.create(**customer))
            except Exception as e:
                errors.append(str(e))
            return CreateCustomers(success=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock <= 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        product_ids = graphene.List(graphene.Int, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer not found")

        if not product_ids:
            raise Exception("Select atleast a product")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("One or more product IDs are invalid")

        total_amount = sum([p.price for p in products])
        order = Order.objects.create(
            customer=customer,
            order_date=order_date or timezone.now(),
            total_amount=total_amount,
        )
        order.products.set(products)
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = CreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType, filterset_class=CustomerFilter)
    customer = graphene.Field(CustomerType, id=graphene.Int(required=True))

    products = graphene.List(ProductType, filterset_class=ProductFilter)
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

    orders = graphene.List(OrderType, filterset_class=OrderFilter)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_orders(self, info):
        return (
            Order.objects.prefetch_related("products").select_related("customer").all()
        )

    def resolve_order(self, info, id):
        try:
            return (
                Order.objects.select_related("customer")
                .prefetch_related("products")
                .get(pk=id)
            )
        except Order.DoesNotExist:
            return None
