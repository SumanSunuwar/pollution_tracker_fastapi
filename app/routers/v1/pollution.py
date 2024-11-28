import pandas as pd

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.dependencies import get_db
from app.services.pollution import fetch_historical_pollution_data, fetch_historical_pollution_data, fetch_historical_weather_data, map_live_sensor_data_to_pollution_data
from app.services.pollution import get_live_sensor_data
from app.services.weather import get_weather
from app.schemas.pollution_overview import CorrelationSummaryResponse, HistoricalPollutionResponse,  HistoricalWeatherResponse, LivePollutionData, PollutionOverviewResponse
from app.schemas.weather import WeatherResponse

router = APIRouter()

# ------------------------------------------------------
# 1. Live Pollution Data API
# ------------------------------------------------------
@router.get("/live_pollution_data", response_model=LivePollutionData)
def get_live_pollution_data():
    """
    Endpoint to fetch live pollution data from sensors.
    """
    live_data = get_live_sensor_data()
    live_pollution_data = map_live_sensor_data_to_pollution_data(live_data)
    return live_pollution_data

# ------------------------------------------------------
# 2. Historical Pollution Data API
# ------------------------------------------------------
@router.get("/historical_pollution_data", response_model=HistoricalPollutionResponse)
def get_historical_pollution_data(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date for filtering historical data (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering historical data (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Offset for fetching historical records")
):
    """
    Endpoint to fetch historical pollution data from the database.
    """
    historical_data, total_count = fetch_historical_pollution_data(
        db, start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )
    return HistoricalPollutionResponse(historical_data=historical_data, total_count=total_count)

# ------------------------------------------------------
# 2.1 Historical Weather Data API
# ------------------------------------------------------
@router.get("/historical_weather_data", response_model=HistoricalWeatherResponse)
def get_historical_weather_data(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date for filtering historical data (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering historical data (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Offset for fetching historical records")
):
    """
    Endpoint to fetch historical weather data from the database.
    """
    print("checking this please")
    historical_weather_data, total_count = fetch_historical_weather_data(
        db, start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )
    print(total_count)
    pass
    return HistoricalWeatherResponse(historical_data=historical_weather_data, total_count=total_count)

# ------------------------------------------------------
# 3. Pollution Overview API
# ------------------------------------------------------
@router.get("/pollution_overview", response_model=PollutionOverviewResponse)
def get_pollution_overview(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date for filtering historical data (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering historical data (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Offset for fetching historical records")
):
    """
    Endpoint to get a combined overview of pollution and weather data.
    """
    # Live pollution data
    live_data = get_live_sensor_data()
    live_pollution_data = map_live_sensor_data_to_pollution_data(live_data)

    # Historical pollution data
    historical_pollution_data, total_pollution_count = fetch_historical_pollution_data(
        db, start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )
        # Historical weather data
    historical_weather_data, total_weather_count = fetch_historical_weather_data(
        db, start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )


    # Weather data
    weather_data = get_weather()

    return PollutionOverviewResponse(
        live_pollution_data=live_pollution_data,
        historical_pollution_data=HistoricalPollutionResponse(historical_data=historical_pollution_data, total_count=total_pollution_count),
        historical_weather_data=HistoricalWeatherResponse(historical_data=historical_weather_data, total_count=total_weather_count),
        weather=weather_data
    )

# ------------------------------------------------------
# 4. Weather Data API
# ------------------------------------------------------
@router.get("/weather", response_model=WeatherResponse)
def get_weather_data():
    """
    Endpoint to fetch current weather data.
    """
    weather_data = get_weather()
    return weather_data

# ------------------------------------------------------
# 5. Correlation Data API
# ------------------------------------------------------
@router.get("/pollution-weather-correlation", response_model=CorrelationSummaryResponse)
def get_pollution_weather_correlation(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date for filtering data (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering data (YYYY-MM-DD)"),
):
    """
    Endpoint to get correlation insights between weather and pollution data, 
    averaging or grouping by date if there are multiple data points.
    """
    # Fetch historical pollution data
    historical_pollution_data, _ = fetch_historical_pollution_data(
        db, start_date=start_date, end_date=end_date, limit=100, offset=0
    )
    
    # Fetch historical weather data
    historical_weather_data, _ = fetch_historical_weather_data(
        db, start_date=start_date, end_date=end_date, limit=100, offset=0
    )

    # Check if there's enough data to calculate correlation
    if not historical_pollution_data or not historical_weather_data:
        raise HTTPException(status_code=400, detail="Insufficient data to calculate correlation")

    # Convert the pollution and weather data into dictionaries for easier processing
    pollution_data = {
        "date": [item.date for item in historical_pollution_data],
        "air_quality_index": [item.air_quality_index for item in historical_pollution_data],
        "water_quality_index": [item.water_quality_index for item in historical_pollution_data],
        "temperature": [item.temperature for item in historical_pollution_data],
    }

    weather_data = {
        "date": [item.date for item in historical_weather_data],
        "humidity": [item.humidity for item in historical_weather_data],
        "rain_mm": [item.rain_mm for item in historical_weather_data],
    }

    # Create pandas DataFrames from the pollution and weather data
    pollution_df = pd.DataFrame(pollution_data)
    weather_df = pd.DataFrame(weather_data)

    # Group by date and average the data (if there are multiple entries per date)
    pollution_df = pollution_df.groupby("date").mean()
    weather_df = weather_df.groupby("date").mean()

    # Merge the dataframes on the 'date' column
    merged_df = pd.merge(pollution_df, weather_df, on="date", how="inner")

    # Calculate correlations between pollution and weather variables
    correlation_summary = {
        "air_quality_index_temperature": merged_df["air_quality_index"].corr(merged_df["temperature"]),
        "air_quality_index_humidity": merged_df["air_quality_index"].corr(merged_df["humidity"]),
        "air_quality_index_rainfall": merged_df["air_quality_index"].corr(merged_df["rain_mm"]),
        "water_quality_index_temperature": merged_df["water_quality_index"].corr(merged_df["temperature"]),
        "water_quality_index_humidity": merged_df["water_quality_index"].corr(merged_df["humidity"]),
        "water_quality_index_rainfall": merged_df["water_quality_index"].corr(merged_df["rain_mm"]),
    }

    # Generate insights based on correlations
    insights = []
    if correlation_summary["air_quality_index_temperature"] > 0.5:
        insights.append("Higher temperatures tend to correlate with poorer air quality.")
    if correlation_summary["air_quality_index_humidity"] < 0:
        insights.append("Higher humidity tends to correlate with better air quality.")
    if correlation_summary["air_quality_index_rainfall"] < 0:
        insights.append("Rainfall tends to reduce air pollution.")
    if correlation_summary["water_quality_index_temperature"] < 0:
        insights.append("Higher temperatures tend to correlate with poorer water quality.")
    if correlation_summary["water_quality_index_humidity"] > 0.5:
        insights.append("Higher humidity tends to correlate with poorer water quality.")
    if correlation_summary["water_quality_index_rainfall"] < 0:
        insights.append("Rainfall tends to improve water quality.")

    return CorrelationSummaryResponse(
        correlation_summary=correlation_summary,
        insights=insights
    )
