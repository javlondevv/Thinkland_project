#!/bin/sh
set -e

if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for database at $DATABASE_HOST..."
  until pg_isready -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" >/dev/null 2>&1; do
    sleep 1
  done
fi

python manage.py migrate --noinput

python manage.py collectstatic --noinput || true

exec "$@"


