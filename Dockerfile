FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

# System dependencies (curl for healthchecks, postgres client for pg_isready)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Install Python dependencies first (better layer caching)
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# Copy project files
COPY . .

# Ensure proper permissions for non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Collect static files (does nothing if not configured)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Use entrypoint to run migrations then start the server
ENTRYPOINT ["/bin/sh", "-c", "./entrypoint.sh"]

# Default command (can be overridden by docker-compose)
CMD gunicorn conf.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
