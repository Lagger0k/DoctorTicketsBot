import os
from pydantic import BaseSettings
from pydantic.fields import Field

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """
    Настройки ETL сервиса.
    """

    # DB
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_USER: str = Field(..., env='DB_USER')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')
    # Extractor
    REQUEST_LIMIT: int = Field(..., env='REQUEST_LIMIT')

    class Config:
        env_file = '.env'


etl_settings = Settings()