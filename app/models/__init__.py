from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .pollution_data import PollutionData
from .weather_data import WeatherData
