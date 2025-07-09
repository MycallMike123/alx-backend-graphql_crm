#!/bin/bash

# Run Django shell command to delete inactive customers and log results
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DELETED_COUNT=$(python3 /path/to/your/manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=one_year_ago).delete()
print(deleted)
")

echo \"[$TIMESTAMP] Deleted \$DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
