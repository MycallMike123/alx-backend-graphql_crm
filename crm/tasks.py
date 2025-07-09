import logging
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = '/tmp/crm_report_log.txt'

@shared_task
def generate_crm_report():
    """Generates weekly CRM report via GraphQL and logs it."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=2
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        # Fetch all customers and orders
        query = gql("""
        query {
          customers { id }
          orders { totalAmount }
        }
        """)
        result = client.execute(query)

        total_customers = len(result.get('customers', []))
        orders = result.get('orders', [])
        total_orders = len(orders)
        total_revenue = sum(o.get('totalAmount', 0) for o in orders)

        report = (
            f"{timestamp} - Report: "
            f"{total_customers} customers, "
            f"{total_orders} orders, "
            f"{total_revenue} revenue"
        )
        with open(LOG_FILE, 'a') as f:
            f.write(report + '\n')

    except Exception as e:
        error_line = f"{timestamp} - Report generation failed: {e}"
        with open(LOG_FILE, 'a') as f:
            f.write(error_line + '\n')
