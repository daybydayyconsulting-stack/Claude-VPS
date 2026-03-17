from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Meta Ads
    meta_app_id: str
    meta_app_secret: str
    meta_access_token: str
    meta_ad_account_id: str  # format: act_XXXXXXXXXX

    # API Security
    api_secret_key: str

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
