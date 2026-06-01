"""Tests for BaseSettings extra='ignore' behavior in shared .env workspaces."""

import pytest
from pydantic import ValidationError

from csrd.models import BaseSettings


class AppSettings(BaseSettings):
    app_name: str = "test"
    debug: bool = False


class TestBaseSettingsIgnoresExtra:
    """Verify BaseSettings silently ignores env vars not declared as fields."""

    def test_unknown_env_vars_ignored(self, monkeypatch: pytest.MonkeyPatch):
        """Env vars belonging to other services must not cause ValidationError."""
        monkeypatch.setenv("APP_NAME", "my-service")
        monkeypatch.setenv("JWT_TTL_SECONDS", "3600")  # belongs to auth-service
        monkeypatch.setenv("REDIS_URL", "redis://localhost")  # belongs to another service

        # Should not raise
        settings = AppSettings(_env_file=None)  # type: ignore[call-arg]
        assert settings.app_name == "my-service"

    def test_missing_required_field_still_raises(self, monkeypatch: pytest.MonkeyPatch):
        """Typos are still caught via 'field required' errors for declared fields."""

        class StrictSettings(BaseSettings):
            required_field: str  # no default → required

        monkeypatch.delenv("REQUIRED_FIELD", raising=False)

        with pytest.raises(ValidationError):
            StrictSettings(_env_file=None)  # type: ignore[call-arg]

    def test_extra_config_value(self):
        """Confirm model_config has extra='ignore'."""
        assert AppSettings.model_config.get("extra") == "ignore"
