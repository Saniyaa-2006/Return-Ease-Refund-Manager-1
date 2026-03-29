import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass')
    user.save()

c = Client()
c.login(username='testuser', password='testpass')
response = c.get('/dashboard/')
print("STATUS CODE:", response.status_code)
if response.status_code == 500:
    print("ERROR rendering dashboard page.")
elif response.status_code == 200:
    print("It worked! Dashboard is 200 OK.")
else:
    print("STATUS:", response.status_code)
