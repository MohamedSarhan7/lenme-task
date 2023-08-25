
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py crontab add

# RUN celery -A backend worker --loglevel=info

EXPOSE 8000

# CMD python3 manage.py runserver 0.0.0.0:8000
CMD python3 run.py