# bogor_tourism_project/asgi.py
import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bogor_tourism_project.settings')
django.setup()

application = get_asgi_application()
