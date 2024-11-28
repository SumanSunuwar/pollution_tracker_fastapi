from sqlalchemy import create_engine, text
from app.core.config import CORE_SETTINGS

# Create a database engine
engine = create_engine(CORE_SETTINGS.DATABASE_URL)

try:
    # Connect to the database
    with engine.connect() as conn:
        # Use a text() object to execute raw SQL
        result = conn.execute(text("SELECT 1")).fetchone()

        if result == (1,):
            print("Database is available and running.")
        else:
            print("Unexpected result from the database. Please check your configuration.")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")
