from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API keys
    etherscan_api_key: str = "demo"
    coingecko_api_key: str = ""

    # Database
    database_url: str = "sqlite+aiosqlite:///./crypto_risk.db"

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    cache_ttl_seconds: int = 300

    # Risk scoring weights
    weight_sanctions: int = 30
    weight_mixer: int = 25
    weight_velocity: int = 20
    weight_structuring: int = 15
    weight_counterparty: int = 10

    # External API base URLs
    etherscan_base_url: str = "https://api.etherscan.io/api"
    coingecko_base_url: str = "https://api.coingecko.com/api/v3"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()