import os
os.system("python3 manage.py runserver 0.0.0.0:8000")
os.system("celery -A backend worker --loglevel=info")


