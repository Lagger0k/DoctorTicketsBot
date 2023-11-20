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
    host: str = Field(default='localhost')
    port: int = Field(default=54321)
    user: str = Field(default='postgres')
    password: str = Field(default='postgres')
    db: str = Field(default='test_ticket')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_config = SettingsConfigDict(env_prefix='DB_')

    @property
    def db_connection_str(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseModel):
    """
    Настройки всех сервисов.
    """

    etl: EtLSettings = EtLSettings()


settings = Settings()
