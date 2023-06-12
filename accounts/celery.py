import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts.settings')

app = Celery('accounts')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()