from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict

settings_config = SettingsConfigDict(
    env_file=(".default_env", ".env"),
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
)


class BaseSettings(_BaseSettings, frozen=True):  # type: ignore[misc]
    model_config = SettingsConfigDict(
        env_file=(".default_env", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
