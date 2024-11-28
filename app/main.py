from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.sessions import engine
from app.routers.v1.pollution import router as pollution_router
from app.routers.v1.weather import router as weather_router
# from sqlalchemy.ext.declarative import declarative_base
from app.models.pollution_data import Base

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,                  # If cookies or credentials are required
    allow_methods=["*"],                     # HTTP methods to allow (e.g., GET, POST)
    allow_headers=["*"],                     # HTTP headers to allow
)
# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(pollution_router, prefix="/api/v1", tags=["Pollution Data"])
app.include_router(weather_router, prefix="/api/v1", tags=["Weather Data"])