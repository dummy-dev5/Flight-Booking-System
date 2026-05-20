import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbs_backend.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword123'
    
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully with password: {password}")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == '__main__':
    create_admin()
