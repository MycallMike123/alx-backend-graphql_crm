import logging
import requests
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE_HEARTBEAT = '/tmp/crm_heartbeat_log.txt'
LOG_FILE_STOCK = '/tmp/low_stock_updates_log.txt'

def log_crm_heartbeat():
    """Logs a heartbeat message and optionally checks GraphQL hello field."""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"

    with open(LOG_FILE_HEARTBEAT, 'a') as f:
        f.write(message + '\n')

    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=2)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""query { hello }""")
        result = client.execute(query)
        hello_response = result.get('hello', 'No response')

        with open(LOG_FILE_HEARTBEAT, 'a') as f:
            f.write(f"{timestamp} GraphQL hello: {hello_response}\n")

    except Exception as e:
        with open(LOG_FILE_HEARTBEAT, 'a') as f:
            f.write(f"{timestamp} GraphQL check failed: {str(e)}\n")


def update_low_stock():
    """Calls GraphQL mutation to restock low-stock products and logs the updates."""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=2)
        client = Client(transport=transport, fetch_schema_from_transport=False)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                success
            }
        }
        """)

        result = client.execute(mutation)
        updates = result.get('updateLowStockProducts', {})
        products = updates.get('updatedProducts', [])
        success_message = updates.get('success', '')

        with open(LOG_FILE_STOCK, 'a') as f:
            f.write(f"{timestamp} {success_message}\n")
            for p in products:
                f.write(f"{timestamp} Product: {p['name']}, New Stock: {p['stock']}\n")

    except Exception as e:
        with open(LOG_FILE_STOCK, 'a') as f:
            f.write(f"{timestamp} Error updating stock: {str(e)}\n")
