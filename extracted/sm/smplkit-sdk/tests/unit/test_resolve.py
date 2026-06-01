"""Integration tests for SmplClient/AsyncSmplClient constructor resolution."""

from __future__ import annotations

import pytest

from smplkit import AsyncSmplClient, SmplClient, Error


class TestSmplClientResolution:
    """Integration tests: SmplClient constructor uses config resolution chain."""

    def test_explicit_key(self):
        client = SmplClient(api_key="sk_api_test", environment="test")
        assert client._api_key == "sk_api_test"

    def test_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_api_env")
        client = SmplClient(environment="test")
        assert client._api_key == "sk_api_env"

    def test_config_file(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config_file = tmp_path / ".smplkit"
        config_file.write_text("[default]\napi_key = sk_api_file\n")
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        client = SmplClient(environment="test")
        assert client._api_key == "sk_api_file"

    def test_config_file_profile(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config_file = tmp_path / ".smplkit"
        config_file.write_text("[default]\napi_key = sk_api_default\n\n[local]\napi_key = sk_api_local\n")
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        client = SmplClient(profile="local", environment="test")
        assert client._api_key == "sk_api_local"

    def test_error_when_no_key(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="No API key provided"):
            SmplClient(environment="test")

    def test_error_message_lists_all_methods(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="Pass api_key to the constructor"):
            SmplClient(environment="test")
        with pytest.raises(Error, match="SMPLKIT_API_KEY"):
            SmplClient(environment="test")
        with pytest.raises(Error, match=r"~/.smplkit"):
            SmplClient(environment="test")

    def test_error_message_shows_resolved_profile(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match=r"\[default\]"):
            SmplClient(environment="test")

    def test_error_when_no_environment(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="No environment provided"):
            SmplClient(api_key="sk_api_test")

    def test_environment_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = SmplClient(api_key="sk_api_test")
        assert client._environment == "staging"

    def test_environment_explicit_takes_precedence(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = SmplClient(api_key="sk_api_test", environment="production")
        assert client._environment == "production"

    def test_service_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_SERVICE", "user-service")
        client = SmplClient(api_key="sk_api_test", environment="test")
        assert client._service == "user-service"

    def test_service_explicit_takes_precedence(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_SERVICE", "env-service")
        client = SmplClient(api_key="sk_api_test", environment="test", service="explicit-service")
        assert client._service == "explicit-service"

    def test_error_when_no_service(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No service provided"):
            SmplClient(api_key="sk_api_test", environment="test")

    def test_environment_resolved_before_api_key(self, monkeypatch, tmp_path):
        """Environment error takes priority even when API key is also missing."""
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="No environment provided"):
            SmplClient()

    def test_service_resolved_before_api_key(self, monkeypatch):
        """Service error takes priority over API key error."""
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No service provided"):
            SmplClient(environment="test")

    def test_base_domain_and_scheme(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        client = SmplClient(
            api_key="sk_api_test",
            environment="test",
            base_domain="localhost",
            scheme="http",
        )
        assert client._base_domain == "localhost"
        assert client._scheme == "http"


class TestAsyncSmplClientResolution:
    """Integration tests: AsyncSmplClient constructor uses config resolution chain."""

    def test_explicit_key(self):
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        assert client._api_key == "sk_api_test"

    def test_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_api_env")
        client = AsyncSmplClient(environment="test")
        assert client._api_key == "sk_api_env"

    def test_error_when_no_key(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="No API key provided"):
            AsyncSmplClient(environment="test")

    def test_error_when_no_environment(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        with pytest.raises(Error, match="No environment provided"):
            AsyncSmplClient(api_key="sk_api_test")

    def test_environment_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AsyncSmplClient(api_key="sk_api_test")
        assert client._environment == "staging"

    def test_error_when_no_service(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No service provided"):
            AsyncSmplClient(api_key="sk_api_test", environment="test")

    def test_profile_parameter(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config_file = tmp_path / ".smplkit"
        config_file.write_text("[local]\napi_key = sk_api_local\nenvironment = dev\nservice = svc\n")
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        client = AsyncSmplClient(profile="local")
        assert client._api_key == "sk_api_local"
