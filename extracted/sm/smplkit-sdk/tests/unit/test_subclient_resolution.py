"""Uniform sub-client config resolution.

Every standalone-constructible sub-client with an environment concept
(audit, config, flags, logging, jobs) resolves ``environment`` — and, where
it exists, ``service`` — exactly like the top-level client: defaults →
``~/.smplkit`` file → ``SMPLKIT_*`` environment variables → constructor
kwargs (kwarg wins). Parent-wired values win over resolution.

The autouse ``_scrub_smplkit_env`` fixture removes ambient SMPLKIT_* vars and
points ``~/.smplkit`` at an empty directory; ``_set_smplkit_service`` then
sets ``SMPLKIT_SERVICE=test-service``, so that value is the ambient service
in these tests.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from smplkit import (
    AsyncAuditClient,
    AsyncConfigClient,
    AsyncFlagsClient,
    AsyncJobsClient,
    AsyncLoggingClient,
    AuditClient,
    ConfigClient,
    FlagsClient,
    JobsClient,
    LoggingClient,
)
from smplkit._config import resolve_client_config

BASE = "https://audit.example.test"


# ---------------------------------------------------------------------------
# resolve_client_config: environment / service resolution chain
# ---------------------------------------------------------------------------


class TestResolveClientConfigEnvironmentService:
    def test_defaults_to_none(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        cfg = resolve_client_config(api_key="sk_test")
        assert cfg.environment is None
        assert cfg.service is None

    def test_from_config_file(self, tmp_path, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        (tmp_path / ".smplkit").write_text("[default]\napi_key = sk_file\nenvironment = file-env\nservice = file-svc\n")
        cfg = resolve_client_config(_home_dir=tmp_path)
        assert cfg.environment == "file-env"
        assert cfg.service == "file-svc"

    def test_env_var_overrides_file(self, tmp_path, monkeypatch):
        (tmp_path / ".smplkit").write_text("[default]\napi_key = sk_file\nenvironment = file-env\nservice = file-svc\n")
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "env-env")
        monkeypatch.setenv("SMPLKIT_SERVICE", "env-svc")
        cfg = resolve_client_config(_home_dir=tmp_path)
        assert cfg.environment == "env-env"
        assert cfg.service == "env-svc"

    def test_kwarg_overrides_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "env-env")
        monkeypatch.setenv("SMPLKIT_SERVICE", "env-svc")
        cfg = resolve_client_config(api_key="sk_test", environment="kwarg-env", service="kwarg-svc")
        assert cfg.environment == "kwarg-env"
        assert cfg.service == "kwarg-svc"

    def test_common_section_applies(self, tmp_path):
        (tmp_path / ".smplkit").write_text("[common]\nenvironment = common-env\n\n[default]\napi_key = sk_file\n")
        cfg = resolve_client_config(_home_dir=tmp_path)
        assert cfg.environment == "common-env"


# ---------------------------------------------------------------------------
# Audit: fast path + resolution fallback
# ---------------------------------------------------------------------------


class TestAuditResolution:
    def test_fast_path_skips_resolution_when_all_supplied(self):
        # api_key AND base_url AND environment supplied → no resolution at all.
        with patch("smplkit.audit.clients.resolve_client_config") as mock_resolve:
            client = AuditClient(api_key="sk_test", base_url=BASE, environment="prod")
        mock_resolve.assert_not_called()
        assert client._environment == "prod"
        client._close()

    def test_environment_resolved_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AuditClient(api_key="sk_test", base_url=BASE)
        assert client._environment == "staging"
        assert client.events._environment == "staging"
        client._close()

    def test_environment_resolved_from_file(self, tmp_path, monkeypatch):
        (tmp_path / ".smplkit").write_text("[default]\napi_key = sk_file\nenvironment = file-env\n")
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        client = AuditClient(base_url=BASE)
        assert client._environment == "file-env"
        client._close()

    def test_kwarg_wins_over_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AuditClient(api_key="sk_test", base_url=BASE, environment="prod")
        assert client._environment == "prod"
        client._close()

    def test_wired_auth_client_keeps_supplied_environment(self, monkeypatch):
        # Parent-wired construction never resolves — the wired value wins.
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        auth = MagicMock()
        client = AuditClient(environment=None, auth_client=auth)
        assert client._environment is None

    def test_async_fast_path_skips_resolution(self):
        with patch("smplkit.audit.clients.resolve_client_config") as mock_resolve:
            client = AsyncAuditClient(api_key="sk_test", base_url=BASE, environment="prod")
        mock_resolve.assert_not_called()
        assert client._environment == "prod"

    def test_async_environment_resolved_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AsyncAuditClient(api_key="sk_test", base_url=BASE)
        assert client._environment == "staging"
        assert client.events._environment == "staging"


# ---------------------------------------------------------------------------
# Config / Flags / Logging: environment + service resolution
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cls",
    [ConfigClient, AsyncConfigClient, FlagsClient, AsyncFlagsClient, LoggingClient, AsyncLoggingClient],
)
class TestRuntimeSubclientResolution:
    def test_environment_and_service_resolved_from_env_vars(self, cls, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        # SMPLKIT_SERVICE=test-service comes from the autouse fixture.
        client = cls(api_key="sk_test", base_domain="example.test")
        assert client._environment == "staging"
        assert client._service == "test-service"

    def test_kwargs_win_over_env_vars(self, cls, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = cls(api_key="sk_test", base_domain="example.test", environment="prod", service="my-svc")
        assert client._environment == "prod"
        assert client._service == "my-svc"

    def test_environment_and_service_resolved_from_file(self, cls, tmp_path, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        (tmp_path / ".smplkit").write_text("[default]\napi_key = sk_file\nenvironment = file-env\nservice = file-svc\n")
        monkeypatch.setattr("smplkit._config.Path.home", lambda: tmp_path)
        client = cls()
        assert client._environment == "file-env"
        assert client._service == "file-svc"

    def test_none_when_unset_anywhere(self, cls, monkeypatch):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        client = cls(api_key="sk_test", base_domain="example.test")
        assert client._environment is None
        assert client._service is None


class TestRuntimeSubclientWiredPrecedence:
    def test_wired_config_uses_parent_values(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "ambient-env")
        parent = MagicMock()
        parent._environment = "parent-env"
        parent._service = "parent-svc"
        client = ConfigClient(parent=parent, transport=MagicMock())
        assert client._environment == "parent-env"
        assert client._service == "parent-svc"

    def test_wired_flags_uses_parent_values(self):
        parent = MagicMock()
        parent._environment = "parent-env"
        parent._service = "parent-svc"
        client = FlagsClient(parent=parent, transport=MagicMock(), contexts=MagicMock())
        assert client._environment == "parent-env"
        assert client._service == "parent-svc"

    def test_wired_logging_uses_parent_values(self):
        parent = MagicMock()
        parent._environment = "parent-env"
        parent._service = "parent-svc"
        transport = MagicMock()
        transport._base_url = "https://logging.example.test"
        client = LoggingClient(parent=parent, transport=transport)
        assert client._environment == "parent-env"
        assert client._service == "parent-svc"

    def test_transport_without_parent_keeps_raw_kwargs(self, monkeypatch):
        # Internal shape: pre-built transport, no parent — no resolution runs.
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "ambient-env")
        client = ConfigClient(transport=MagicMock(), environment=None, service=None)
        assert client._environment is None
        assert client._service is None


# ---------------------------------------------------------------------------
# Jobs: environment resolution (no service concept)
# ---------------------------------------------------------------------------


class TestJobsResolution:
    def test_environment_resolved_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = JobsClient(api_key="sk_test", base_domain="example.test")
        assert client._environment == "staging"
        assert client.runs._environment == "staging"

    def test_kwarg_wins_over_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = JobsClient(api_key="sk_test", base_domain="example.test", environment="prod")
        assert client._environment == "prod"
        assert client.runs._environment == "prod"

    def test_wired_auth_client_keeps_supplied_environment(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = JobsClient(auth_client=MagicMock())
        assert client._environment is None

    def test_async_environment_resolved_from_env_var(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AsyncJobsClient(api_key="sk_test", base_domain="example.test")
        assert client._environment == "staging"
        assert client.runs._environment == "staging"

    def test_async_wired_auth_client_keeps_supplied_environment(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        client = AsyncJobsClient(auth_client=MagicMock())
        assert client._environment is None
