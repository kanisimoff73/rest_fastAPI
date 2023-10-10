#!/bin/bash

alembic upgrade head

DB_USER="postgres"
DB_HOST="postgres-db"
DB_PORT="5432"
DB_NAME="postgres"
SEQUENCE_NAME="task_sid_seq"

# Connect to the PostgreSQL database
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" <<EOF
postgres
SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = '$SEQUENCE_NAME';
CREATE SEQUENCE IF NOT EXISTS $SEQUENCE_NAME;
SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = '$SEQUENCE_NAME';
EOF

cd src

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000