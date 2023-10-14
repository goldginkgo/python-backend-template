from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn

    # PGAdmin
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    # Utils
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Logging
    log_level: str = "INFO"
    log_mode_json: bool = False

    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/var/run/secrets/app")


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()
