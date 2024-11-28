from pydantic import BaseModel
from typing import Optional
from datetime import date

class PollutionDataResponse(BaseModel):
    sensor_id: int
    air_quality_index: int
    water_quality_index: int
    temperature: float
    ph_level: Optional[float] = None
    date: date

    class Config:
        from_attributes = True

class PollutionHistoricalDataResponse(BaseModel):
    air_quality_index: int
    water_quality_index: int
    temperature: float
    ph_level: Optional[float] = None
    date: date

    class Config:
        from_attributes = True