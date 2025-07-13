#!/bin/bash

# Get current working directory
cwd="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Move to Django project root (assumes crm/cron_jobs structure)
if cd "$cwd/../.."; then
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
else
    echo "Failed to change directory to project root." >&2
    exit 1
fi

