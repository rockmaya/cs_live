FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


WORKDIR /app

# System dependencies (PostgreSQL + Excel support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project source
COPY . /app/

# App runs on 9000
EXPOSE 9000

CMD ["gunicorn", "cs_project.wsgi:application", "--chdir", "/app", "--bind", "0.0.0.0:9000"]


