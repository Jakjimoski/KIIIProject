#!/bin/sh

echo "Waiting for database to be ready..."
#while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
while ! nc -z "postgres-service" "5432"; do
  sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec "$@"
