from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from .pollution_data import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column(nullable=True)
    feels_like: Mapped[float] = mapped_column(nullable=True)
    humidity: Mapped[int] = mapped_column(nullable=True)
    weather_description: Mapped[str] = mapped_column(nullable=True)
    wind_speed: Mapped[float] = mapped_column(nullable=True)
    rain_mm: Mapped[float] = mapped_column(nullable=True)
    sunrise: Mapped[int] = mapped_column(nullable=True)
    sunset: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(default=func.now(), nullable=True)

    def __repr__(self):
        return (
            f"<WeatherData(id={self.id}, description='{self.weather_description}', date={self.date})>"
        )
