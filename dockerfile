FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Environment variables for superuser
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=222222

# Run migrations and create superuser
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput


WORKDIR /app

# System dependencies (PostgreSQL + Excel support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
COPY staticfiles /app/staticfiles
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project source
COPY . /app/

# App runs on 9000
EXPOSE 9000


# CMD ["gunicorn", "cs_project.wsgi:application", "--chdir", "/app", "--bind", "0.0.0.0:9000"]    

CMD ["gunicorn", "cs_project.wsgi:application", "--chdir", "/app", "--bind", "0.0.0.0:$PORT"]


