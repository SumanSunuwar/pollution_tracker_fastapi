#!/bin/bash

export $(grep -v '^#' .env | xargs)

if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_HOST" || -z "$DB_PORT" ]]; then
  echo "Error: One or more required environment variables are not set. Exiting."
  exit 1
fi

read -p "Are you sure you want to delete the database '$DB_NAME' and user '$DB_USER'? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "Operation cancelled."
    exit 0
fi

DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ "$DB_EXISTS" == "1" ]; then
    echo "Terminating database '$DB_NAME' connections..."

    psql -U postgres -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();"

    if [ $? -eq 0 ]; then
        echo "Active connections terminated."
    else
        echo "Failed to terminate active connections."
        exit 1
    fi

    echo "Dropping database '$DB_NAME'..."
    psql -U postgres -c "DROP DATABASE $DB_NAME;"

    if [ $? -eq 0 ]; then
        echo "Database '$DB_NAME' has been deleted."
    else
        echo "Failed to delete the database."
        exit 1
    fi

    echo "Dropping user '$DB_USER'..."
    psql -U postgres -c "DROP USER $DB_USER;"

    if [ $? -eq 0 ]; then
        echo "User '$DB_USER' has been deleted."
    else
        echo "Failed to delete the user."
        exit 1
    fi
else
    echo "Database '$DB_NAME' does not exist."
fi
