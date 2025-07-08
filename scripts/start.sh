#!/bin/sh

echo "Waiting for database to be ready..."
sleep 5

echo "Initializing Aerich..."
aerich init -t database.TORTOISE_ORM || true
aerich init-db || true

echo "Starting FastAPI application..."
exec uvicorn app:app --host 0.0.0.0 --port 8080 --reload
