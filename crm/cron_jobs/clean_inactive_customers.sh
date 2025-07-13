#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the root of the Django project
cd "$SCRIPT_DIR/../.." || exit 1

# Get timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Run Django shell command and capture deleted count
DELETED_COUNT=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=one_year_ago).delete()
print(deleted)
")

# Log result
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt

