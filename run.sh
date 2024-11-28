#!/bin/bash

export $(grep -v '^#' .env | xargs)

if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_HOST" || -z "$DB_PORT" ]]; then
  echo "Error: One or more required environment variables are not set. Exiting."
  exit 1
fi

check_database_exists() {
  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'"
}

check_user_exists() {
  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'"
}

if [[ "$(check_database_exists)" != "1" ]]; then
  echo "Creating database '$DB_NAME' and user..."

  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -c "CREATE DATABASE $DB_NAME;"
  echo "-- Database '$DB_NAME' created successfully."

  if [[ "$(check_user_exists)" != "1" ]]; then
    psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    echo "-- User '$DB_USER' created successfully."
  else
    echo "-------------------------------------"
  fi

  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
  echo "-- Database Permissions granted to user '$DB_USER' on database '$DB_NAME'."
  # After granting database privileges

  # Grant privileges on the schema
  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
  echo "-- Schema 'public' privileges granted to user '$DB_USER'."

  # Grant privileges on all existing tables in the schema
  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
  echo "-- Table privileges granted to user '$DB_USER'."

  # Grant privileges on all sequences (e.g., for serial types)
  psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"
  echo "-- Sequence privileges granted to user '$DB_USER'."


fi

DB_CONNECTION=$(psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1")

if [ "$DB_CONNECTION" != "1" ]; then
  echo "Error: Could not connect to the database '$DB_NAME' using user '$DB_USER'. Exiting."
  exit 1
fi

echo "Database '$DB_NAME' is available for connection."

echo "Starting FastAPI application..."
uvicorn app.main:app --reload
