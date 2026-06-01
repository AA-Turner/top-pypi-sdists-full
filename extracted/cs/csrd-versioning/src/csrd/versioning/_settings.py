import logging
from functools import lru_cache

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class VersioningSettings(BaseSettings):
    """Environment-backed settings required for the versioning system to operate.

    This includes identity and auth values (e.g. ``jwt_secret``) that
    versioned endpoints depend on, not just version-routing configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("APP_NAME", "app_name"),
    )
    jwt_secret: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("JWT_SECRET", "JAVELIN_JWT_KEY_CREDENTIALS_JAVELIN_JWT_KEY"),
    )
    service_root_domain: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SERVICE_ROOT_DOMAIN"),
    )
    build_tag: str | None = Field(
        default=None,
        validation_alias=AliasChoices("BUILD_TAG"),
    )


@lru_cache(maxsize=1)
def load_versioning_settings() -> VersioningSettings:
    """Return cached settings read from environment variables.

    The result is cached for the lifetime of the process — only add
    fields here for values that are fixed at startup (e.g. ``APP_NAME``,
    ``JWT_SECRET``). Environment variable changes after the first call
    will not be reflected.
    """
    return VersioningSettings()


def load_app_name(override: str | None = None) -> str:
    """Resolve application name with an explicit override or environment fallback.

    When *override* is a non-empty string it is returned immediately.
    When *override* is ``None``, the function reads ``APP_NAME`` from
    environment-backed Pydantic settings. If ``APP_NAME`` is missing, or any
    error occurs, the function falls back to ``"UNKNOWN_APP"``.

    Raises:
        ValueError: If *override* is an empty string.
    """
    if isinstance(override, str):
        if not override:
            raise ValueError("override must be a non-empty string or None")
        return override

    fallback = "UNKNOWN_APP"

    try:
        settings = load_versioning_settings()
        if settings.app_name:
            logger.debug("App name loaded from settings: %s", settings.app_name)
            return settings.app_name

        logger.warning("No APP_NAME value found in settings, defaulting to %s", fallback)
        return fallback
    except Exception as e:
        logger.warning(
            "error retrieving app_name from settings defaulting to %s: %s",
            fallback,
            e,
        )
        return fallback


__all__ = ("VersioningSettings", "load_app_name", "load_versioning_settings")
