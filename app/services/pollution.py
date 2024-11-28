import pandas as pd
import random
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from app.models.pollution_data import PollutionData
from app.schemas.pollution import PollutionDataResponse
from app.schemas.pollution_overview import CorrelationSummaryResponse, HistoricalWeatherResponse
from app.models.weather_data import WeatherData
from app.schemas.weather import WeatherHistoricalDataResponse, WeatherResponse

# Simulated live data fetch (this will simulate the data you receive from the sensor)
def get_live_sensor_data():
    # Simulate fetching live data from an API or mock source
    print(f"Fetching live sensor data")
    return {
        "sensor_id": "phewa-001",
        "timestamp": "2024-10-28T12:00:00Z",
        "air_quality_index": random.randint(0, 300),
        "water_quality_index": random.randint(30, 100),
        "ph_level": round(random.uniform(6.5, 8.5), 1),
        "date": date.today()
    }

# Mapping the live data to the PollutionDataResponse
def map_live_sensor_data_to_pollution_data(live_data):
    # Here, we are assuming the 'sensor_id' can be mapped to 'id', and 'temperature' is default
    return {
        "sensor_id": int(live_data["sensor_id"].split("-")[-1]),  # Extract an ID based on sensor_id
        "air_quality_index": live_data["air_quality_index"],
        "water_quality_index": live_data["water_quality_index"],
        "temperature": 22.0,  # Assuming a default temperature or fetching it from somewhere
        "ph_level": live_data["ph_level"],
        "date": live_data["date"]
    }

def fetch_historical_pollution_data(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 10,
    offset: int = 0
) -> List[PollutionDataResponse]:
    """
    Fetch historical pollution data with pagination and optional default date range.
    """
    # Default date range: last 30 days
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()

    query = db.query(PollutionData).filter(
        PollutionData.date >= start_date,
        PollutionData.date <= end_date
    )

    # Fetch total count for pagination metadata
    total_count = query.count()

    # Apply limit and offset for pagination
    historical_data = query.offset(offset).limit(limit).all()

    return historical_data, total_count

def fetch_historical_weather_data(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 10,
    offset: int = 0
) -> List[WeatherHistoricalDataResponse]:
    """
    Fetch historical pollution data with pagination and optional default date range.
    """
    # Default date range: last 30 days
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()

    query = db.query(WeatherData).filter(
        WeatherData.date >= start_date,
        WeatherData.date <= end_date
    )

    # Fetch total count for pagination metadata
    total_count = query.count()

    # Apply limit and offset for pagination
    historical_data = query.offset(offset).limit(limit).all()

    return historical_data, total_count

def fetch_correlation_summary(db: Session, start_date: Optional[date], end_date: Optional[date]):
    historical_data, _ = fetch_historical_pollution_data(db, start_date, end_date, limit=100, offset=0)

    data = {
        "temperature": [item.temperature for item in historical_data],
        # "humidity": [item.humidity for item in historical_data],
        # "rainfall": [item.rainfall for item in historical_data],
        "aqi": [item.air_quality_index for item in historical_data],
        # "pm2_5": [item.pm2_5 for item in historical_data],
    }

    df = pd.DataFrame(data)

    correlation_summary = {
        "rainfall_aqi": df["rainfall"].corr(df["aqi"]),
        "temperature_aqi": df["temperature"].corr(df["aqi"]),
        "humidity_pm2_5": df["humidity"].corr(df["pm2_5"]),
    }

    insights = []
    if correlation_summary["rainfall_aqi"] < 0:
        insights.append("Pollution tends to decrease on rainy days.")
    if correlation_summary["temperature_aqi"] > 0.5:
        insights.append("Higher temperatures tend to correlate with poorer air quality.")

    return CorrelationSummaryResponse(
        correlation_summary=correlation_summary,
        insights=insights
    )