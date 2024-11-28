import os
import requests
from dotenv import load_dotenv
from app.schemas.weather import WeatherResponse

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Phewa Lake coordinates
LATITUDE = 28.2099
LONGITUDE = 83.9805

def get_weather() -> WeatherResponse:
    """Fetch weather data from OpenWeather API for Phewa Lake."""
    response = requests.get(BASE_URL, params={"lat": LATITUDE, "lon": LONGITUDE, "appid": API_KEY, "units": "metric"})
    if response.status_code == 200:
        data = response.json()
        return WeatherResponse(
            city=data["name"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],  # Adding the missing field
            humidity=data["main"]["humidity"],
            weather_description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"],  # Adding the missing field
            sunrise=data["sys"]["sunrise"],  # Adding the missing field
            sunset=data["sys"]["sunset"],  # Adding the missing field
            country=data["sys"]["country"],  # Adding the missing field
        )
    else:
        raise ValueError(f"Failed to fetch weather data: {response.status_code}")
