import os
import django
from django.conf import settings

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
    django.setup()
    print("SUCCESS: Django is setup correctly")
except Exception as e:
    print(f"FAILURE: Django setup failed with error: {e}")
    import traceback
    traceback.print_exc()
