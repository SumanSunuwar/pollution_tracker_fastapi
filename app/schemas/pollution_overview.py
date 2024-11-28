from pydantic import BaseModel
from typing import List, Dict
from .pollution import PollutionDataResponse, PollutionHistoricalDataResponse
from .weather import WeatherHistoricalDataResponse, WeatherResponse


class LivePollutionData(PollutionDataResponse):
    class Config:
        from_attributes = True

class HistoricalPollutionData(PollutionHistoricalDataResponse):
    class Config:
        from_attributes = True

class HistoricalPollutionResponse(BaseModel):
    total_count: int
    historical_data: List[HistoricalPollutionData]

    class Config:
        from_attributes = True

# class HistoricalWeatherData(WeatherHistoricalDataResponse):
#     class Config:
#         from_attributes = True

class HistoricalWeatherResponse(BaseModel):
    total_count: int
    historical_data: List[WeatherHistoricalDataResponse]

class PollutionOverviewResponse(BaseModel):
    live_pollution_data: LivePollutionData
    historical_pollution_data: HistoricalPollutionResponse
    historical_weather_data: HistoricalWeatherResponse
    weather: WeatherResponse

    class Config:
        from_attributes = True

class CorrelationSummaryResponse(BaseModel):
    correlation_summary: Dict[str, float]
    insights: List[str]
