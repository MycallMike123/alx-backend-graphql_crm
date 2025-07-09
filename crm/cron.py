import logging
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = '/tmp/crm_heartbeat_log.txt'

def log_crm_heartbeat():
    """Logs a heartbeat message and optionally checks GraphQL hello field."""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"

    # Log the heartbeat message
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\n')

    # Optional: Check GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=2
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""query { hello }""")
        result = client.execute(query)
        hello_response = result.get('hello', 'No response')

        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} GraphQL hello: {hello_response}\n")

    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} GraphQL check failed: {str(e)}\n")

