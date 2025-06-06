import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoDjango.settings')
django.setup()

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin1234')

if not User.objects.filter(username=username).exists():
    print(f"Creando superusuario {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"Superusuario {username} ya existe.")
