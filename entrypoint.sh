#!/bin/sh
set -e

# Wait for Postgres
if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for database at $DATABASE_HOST..."
  until pg_isready -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" >/dev/null 2>&1; do
    sleep 1
  done
fi

# Apply migrations
python manage.py migrate --noinput

# Collect static (safe if not configured)
python manage.py collectstatic --noinput || true

exec "$@"


