#!/bin/sh

# Чекај додека базата не е подготвена
echo "Waiting for database to be ready..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

# Изврши ги миграциите
echo "Applying database migrations..."
python manage.py migrate

# Стартувај го главниот процес
echo "Starting server..."
exec "$@"
