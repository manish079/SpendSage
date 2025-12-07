# config/celery_app.py

import os
from celery import Celery

# Set the default Django settings module 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SpendSage.settings')

# Create a Celery instance, named after the project configuration
app = Celery('config')

# Load task configurations from Django settings. 
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps' 'tasks.py' files.
app.autodiscover_tasks()