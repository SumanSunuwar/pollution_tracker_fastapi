# Pollution Tracker

This project tracks pollution levels by collecting live sensor data, historical pollution data, and weather information. The system provides insights into air and water quality trends, weather conditions, and pollution alerts.

## Project Overview

The Pollution Tracker integrates data from multiple sources to allow users to monitor the pollution levels of the lake. It includes:

- Live Sensor Data: Simulated API for real-time pollution levels (air and water quality).
- Historical Pollution Data: Data stored in a database to track trends over time.
- Weather Data: Fetches weather conditions for Pokhara from an API.

Here is the `README.md` formatted for your FastAPI project setup:

```markdown
# FastAPI Project Setup and Commands

## Prerequisites

- Python 3.12.0 or higher
- Poetry (for dependency management)

## Setup Instructions

### 1. Verify Python Version

Make sure you're using Python 3.12.0 or higher:

```bash
python --version
```

### 2. Create and Activate a Python Virtual Environment

To isolate your project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
# On Windows, use: venv\Scripts\activate
```

### 3. Update Basic Python Packages

Upgrade `pip`, `setuptools`, and install `wheel` for smoother package management:

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python3 -m pip install wheel
```

### 4. Install Poetry for Dependency Management

Install Poetry to manage the project's dependencies:

```bash
pip install poetry
```

### 5. Run the Project and Create Database (If Not Already Created)

Start the project and automatically create the database if it doesn't already exist:

```bash
./run.sh
```

### 6. Delete the Database and User

If you need to completely drop the database and its user:

```bash
./deletedb.sh
```

---

## Database Migrations

### 1. Generate Alembic Migrations

To create a new migration script based on changes to your models:

```bash
alembic revision --autogenerate -m "Creating migration"
```

### 2. Apply Migrations (Upgrade)

To apply all pending migrations to your database:

```bash
alembic upgrade head
```

### 3. Remove All Migration Files

If you need to remove all migration files:

```bash
rm -rf alembic/versions/*
rm -rf alembic/versions/__pycache__
rm -rf migrations/versions/*.py
```

### 4. Using Alembic with Database Changes Already Applied

If the database schema has already been manually applied, Alembic might not detect changes. In this case, you can reset and apply the migrations as follows:

```bash
alembic downgrade base
alembic upgrade head
```

---

## Utility Scripts

### 1. Check Database Connection

Run the following command to check if your database connection is working properly:

```bash
poetry run python -m app.scripts.check_db
```

### 2. Populate Historic Data Using Faker

To populate the database with historical data using Faker:

```bash
poetry run python -m app.scripts.populate_data
```

---

This README provides a streamlined way to set up, manage, and work with the FastAPI project, including all necessary commands to handle database migrations, checks, and populating the database with sample data. 
```

You can copy and paste this into your `README.md` file. This format covers the essential setup steps, migration commands, and utility scripts for your FastAPI project.