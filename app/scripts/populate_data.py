from faker import Faker
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal
from app.models.pollution_data import PollutionData
from app.models.weather_data import WeatherData
from sqlalchemy import func
import random

# Initialize Faker for random data generation
fake = Faker()

def get_oldest_record_date(db: Session, model):
    """
    Retrieve the oldest date from any given model.
    """
    oldest_record = db.query(model).order_by(model.date.asc()).first()
    return oldest_record.date if oldest_record else None

def generate_pollution_data(record_date):
    """
    Generate pollution data for a given date.
    """
    return {
        "date": record_date,
        "air_quality_index": fake.random_int(min=0, max=500),
        "water_quality_index": fake.random_int(min=0, max=100),
        "ph_level": round(fake.random.uniform(6.5, 8.5), 2),
        "temperature": round(fake.random.uniform(-10.0, 40.0), 1),
    }

def generate_weather_data(record_date):
    """
    Generate weather data for a given date.
    """
    return {
        "date": record_date,
        "temperature": round(random.uniform(-10.0, 60.0), 2),
        "feels_like": round(random.uniform(-10.0, 60.0), 2),
        "humidity": random.randint(0, 100),
        "weather_description": fake.word(),
        "wind_speed": round(random.uniform(0.0, 15.0), 2),
        "rain_mm": round(random.uniform(0.0, 100.0), 2) if random.random() < 0.3 else None,
        "sunrise": random.randint(1600000000, 1700000000),
        "sunset": random.randint(1700000000, 1800000000),
        "city": fake.city(),
        "country": fake.country(),
    }

def populate_pollution_data_from_year(start_year: int) -> bool:
    """
    Populate the database with pollution data starting from a given year up to today.
    """
    db = SessionLocal()
    try:
        # Fetch the oldest existing date in the database
        oldest_date = get_oldest_record_date(db, PollutionData)

        if oldest_date and start_year >= oldest_date.year:
            print(f"Cannot add data for {start_year} or later, as data already exists from {oldest_date.year}.")
            return False

        # Calculate start and end dates
        start_date = date(start_year, 1, 1)
        end_date = date.today()

        # Generate dates from start_year to today
        dates_to_generate = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Generate and save data
        data_records = [PollutionData(**generate_pollution_data(record_date)) for record_date in dates_to_generate]
        db.bulk_save_objects(data_records)
        db.commit()

        print(f"Pollution data from {start_year}-01-01 to {end_date} added successfully.")
        return True
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        db.close()

def populate_weather_data_from_year(start_year: int) -> bool:
    """
    Populate the database with weather data starting from a given year up to today.
    """
    db = SessionLocal()
    try:
        # Fetch the oldest existing date in the database
        oldest_date = get_oldest_record_date(db, WeatherData)

        if oldest_date and start_year >= oldest_date.year:
            print(f"Cannot add data for {start_year} or later, as data already exists from {oldest_date.year}.")
            return False

        # Calculate start and end dates
        start_date = date(start_year, 1, 1)
        end_date = date.today()

        # Generate dates from start_year to today
        dates_to_generate = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Generate and save data
        data_records = [WeatherData(**generate_weather_data(record_date)) for record_date in dates_to_generate]
        db.bulk_save_objects(data_records)
        db.commit()

        print(f"Weather data from {start_year}-01-01 to {end_date} added successfully.")
        return True
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        db.close()

def prompt_for_year() -> int:
    """
    Prompt the user to input a year for adding data, ensuring it is valid.
    """
    db = SessionLocal()
    try:
        # Fetch the oldest date from the database for both pollution and weather data
        oldest_pollution_date = get_oldest_record_date(db, PollutionData)
        oldest_weather_date = get_oldest_record_date(db, WeatherData)

        oldest_date = min(oldest_pollution_date, oldest_weather_date) if oldest_pollution_date and oldest_weather_date else None

        if oldest_date:
            print(f"The oldest data in the database is from {oldest_date.year}. Please enter a year earlier than this.")
            while True:
                try:
                    start_year = int(input(f"Enter the year to add data (before {oldest_date.year}): "))
                    if start_year >= oldest_date.year:
                        print(f"Cannot add data for {start_year} as it already exists.")
                    else:
                        return start_year
                except ValueError:
                    print("Invalid input. Please enter a valid integer year.")
        else:
            # If there's no data yet, prompt the user for any year
            print("No data found in the database. Please enter the year you want to add data from.")
            while True:
                try:
                    start_year = int(input("Enter the year to add data: "))
                    return start_year
                except ValueError:
                    print("Invalid input. Please enter a valid integer year.")
    except Exception as e:
        print(f"An error occurred while checking the oldest date: {e}")
    finally:
        db.close()

def populate_data_for_year(start_year: int) -> bool:
    """
    Populate both the pollution and weather data for the specified year.
    """
    print(f"Populating data for year {start_year}...")

    # Run both population functions
    pollution_success = populate_pollution_data_from_year(start_year)
    weather_success = populate_weather_data_from_year(start_year)

    if pollution_success and weather_success:
        print("Both pollution and weather data populated successfully.")
        return True
    else:
        print("There was an error populating the data.")
        return False

if __name__ == "__main__":
    print("Starting database population...")

    # Prompt the user to enter the year for adding data
    start_year = prompt_for_year()

    # Populate both data for the given year
    if populate_data_for_year(start_year):
        print("Database population completed.")
    else:
        print("Database population unsuccessful.")
