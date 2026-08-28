"""Application settings loaded from environment variables."""

import os


class Settings:
    """Application configuration."""

    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_LOG_LEVEL: str = os.getenv("APP_LOG_LEVEL", "info")
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
