# ALX Backend GraphQL CRM

A simple Django project demonstrating a GraphQL endpoint using `graphene-django`. This project is part of the ALX backend curriculum and serves as an introduction to building and querying a GraphQL API.

---

## 🚀 Features

- Django-based backend
- GraphQL endpoint at `/graphql`
- Simple `hello` query that returns: `"Hello, GraphQL!"`
- GraphiQL enabled for easy query testing
- Clean modular structure for scaling into a full CRM

---

## 📁 Project Structure

alx_backend_graphql_crm/
├── crm/ # Main Django app (currently empty)
├── alx_backend_graphql_crm/ # Django config module
│ ├── init.py
│ ├── asgi.py
│ ├── urls.py
│ ├── wsgi.py
├── manage.py # Django management script
├── requirements.txt # Python dependencies
├── settings.py # Project settings (moved to root)
├── schema.py # GraphQL schema with hello query
├── README.md # Project documentation

## Create a Virtual Environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

##  Install Dependencies & Apply migrations
    ```bash
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    ```

## 🔍 Testing the GraphQL Endpoint
Visit: http://localhost:8000/graphql

Run the following query:
    ```bash
    {
        hello
    }
    ```

Expected response
    ```bash
    {
        "data": {
            "hello": "Hello, GraphQL!"
        }
    }
    ```


## 🧪 Requirements
- Python 3.8+

- Django 3.2+ or 4.x

- graphene-django

- django-filter

✍️ Author
Michael Mwangi
GitHub: @MycallMike123
