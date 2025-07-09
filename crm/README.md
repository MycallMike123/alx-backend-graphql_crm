# Weekly CRM Report with Celery & GraphQL

## Prerequisites
- **Redis** as broker:
  ```bash
  sudo apt-get update
  sudo apt-get install redis
  redis-server
    ```

## Installation
    ```bash
    - **# Install Python deps:**
    pip install -r requirements.txt
    - **# Apply migrations:**
    python manage.py migrate
    ```


## Running
    ```bash
    **# Django server**
    python manage.py runserver
    **# Celery worker**
    celery -A crm worker -l info
    **# Celery beat(Scheduler)**
    celery -A crm beat -l info
    ```
