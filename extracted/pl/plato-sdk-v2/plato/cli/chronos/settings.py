"""Chronos settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class ChronosSettings(BaseSettings):
    """Chronos configuration from environment."""

    chronos_url: str = "https://chronos.plato.so"

    class Config:
        env_prefix = ""


@lru_cache
def get_settings() -> ChronosSettings:
    return ChronosSettings()
