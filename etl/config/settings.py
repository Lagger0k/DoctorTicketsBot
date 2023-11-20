import os
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic.fields import Field
from pydantic import BaseModel


class EtLSettings(BaseSettings):
    """
    Настройки ETL сервиса.
    """

    # DB
    host: str = Field(...)
    port: int = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_config = SettingsConfigDict(env_prefix='DB_')

    @property
    def db_connection_str(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.host}:{self.port}/{self.db_name}"


class Settings(BaseModel):
    """
    Настройки всех сервисов.
    """

    etl = EtLSettings()


settings = Settings()
