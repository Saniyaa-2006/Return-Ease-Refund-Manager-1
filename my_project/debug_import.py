import os
import sys
import traceback

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
    import django
    django.setup()
    from my_app import views
    print("Import successful")
except Exception:
    with open('traceback.txt', 'w') as f:
        traceback.print_exc(file=f)
    print("Import failed")
