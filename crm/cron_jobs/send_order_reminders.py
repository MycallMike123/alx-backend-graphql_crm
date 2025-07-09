#!/usr/bin/env python3

import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
logging.basicConfig(filename='/tmp/order_reminders_log.txt',
                    level=logging.INFO,
                    format='[%(asctime)s] %(message)s')

def main():
    # Define GraphQL transport and client
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # GraphQL query to get pending orders
    query = gql("""
    query GetRecentOrders($since: Date!) {
      orders(orderDate_Gte: $since) {
        edges {
          node {
            id
            customer {
              email
            }
          }
        }
      }
    }
    """)

    # Execute query
    try:
        params = {"since": seven_days_ago}
        result = client.execute(query, variable_values=params)
        orders = result.get('orders', {}).get('edges', [])

        for order in orders:
            order_id = order['node']['id']
            email = order['node']['customer']['email']
            logging.info(f"Order ID: {order_id}, Customer Email: {email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        print("Failed to process order reminders.", file=sys.stderr)

if __name__ == '__main__':
    main()
