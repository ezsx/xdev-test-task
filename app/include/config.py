from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG_MODE: bool = Field(False, validation_alias='DEBUG_MODE')
    SERVICE_NAME: str = Field('test_task', validation_alias='SERVICE_NAME')

    DB_TYPE: str = "postgresql"
    DB_CONNECTOR: str = "asyncpg"
    DB_HOST: Optional[str] = Field(None, validation_alias='POSTGRES_HOST')
    DB_PORT: Optional[int] = Field(None, validation_alias='POSTGRES_PORT')
    DB_USER: Optional[str] = Field(None, validation_alias='POSTGRES_USER')
    DB_PASSWORD: Optional[str] = Field(None, validation_alias='POSTGRES_PASSWORD')
    DB_DB: Optional[str] = Field(None, validation_alias='POSTGRES_DB')
    DB_MIN_CONNECTIONS: int = Field(1, validation_alias='MIN_CONNECTIONS')
    DB_MAX_CONNECTIONS: int = Field(10, validation_alias='MAX_CONNECTIONS')

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_TYPE}+{self.DB_CONNECTOR}://" \
               f"{self.DB_USER}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/" \
               f"{self.DB_DB}"


config = Settings()
