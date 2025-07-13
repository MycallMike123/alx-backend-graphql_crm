INSTALLED_APPS = [
    'django_crontab',
]

CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]
