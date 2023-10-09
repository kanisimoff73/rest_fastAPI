#!/bin/bash

alembic upgrade head

DB_USER="postgres"
DB_HOST="postgres-db"
DB_PORT="5432"
DB_NAME="postgres"
SEQUENCE_NAME="task_sid_seq"

# Connect to the PostgreSQL database
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" <<EOF
SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = '$SEQUENCE_NAME';
CREATE SEQUENCE IF NOT EXISTS $SEQUENCE_NAME;
SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = '$SEQUENCE_NAME';
EOF

## Prompt to remove the sequence
#read -p "Do you want to remove the sequence (y/n)? " choice
#if [[ $choice =~ ^[Yy]$ ]]; then
#    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "DROP SEQUENCE IF EXISTS $SEQUENCE_NAME;"
#    echo "PostgreSQL sequence '$SEQUENCE_NAME' removed."
#else
#    echo "Sequence removal canceled."
#fi

#psql -U postgres -h localhost -p 5433 -d db_tasks

#postgresql

#CREATE SEQUENCE IF NOT EXISTS task_sid_seq

#\q

cd src

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000