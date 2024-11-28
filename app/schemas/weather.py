from pydantic import BaseModel
from typing import Optional
from datetime import date


class WeatherResponse(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    weather_description: str
    wind_speed: float
    rain_mm: Optional[float] = None
    sunrise: int
    sunset: int
    city: str
    country: str      

    class Config:
        from_attributes = True

class WeatherHistoricalDataResponse(BaseModel):
    date: date
    temperature: float
    humidity: int
    wind_speed: float
    rain_mm: Optional[float] = None
    weather_description: str

    class Config:
        from_attributes = True