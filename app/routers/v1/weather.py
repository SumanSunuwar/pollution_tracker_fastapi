from fastapi import APIRouter, HTTPException
from app.services.weather import get_weather
from app.schemas.weather import WeatherResponse

router = APIRouter()

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
