from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional

class CoreSettings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """

    # Database Settings
    DB_ENGINE: str = Field("postgresql", env="DB_ENGINE")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="DB_HOST")  # Default: localhost
    DB_PORT: str = Field("5432", env="DB_PORT")  # Default: 5432

    # API Settings
    API_VERSION: str = "v1"  # Default API version
    WEATHER_API_KEY: Optional[str] = Field(None, env="WEATHER_API_KEY")  # Optional API Key

    # Derived settings (not directly in .env file)
    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the database URL dynamically from individual settings.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        # Specify the .env file location and encoding for environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate settings as a singleton
CORE_SETTINGS = CoreSettings()
