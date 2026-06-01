from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from mistralai.workflows.core.config.config_discovery import normalize_temporal_url  # noqa: F401
from mistralai.workflows.core.temporal.temporal_client import _get_proxy_basic_auth  # noqa: F401

# Import regression — fail at collection time if any internal path moves.
from mistralai.workflows.core.worker_client import get_worker_client  # noqa: F401
from mistralai.workflows.scripts.diagnose import (
    _check_mistral_api,
    _check_whoami,
    _env_vars_from_models,
    _print_config,
    _print_env_vars,
)


class TestEnvVarsFromModels:
    def test_includes_all_critical_vars(self):
        vars_ = set(_env_vars_from_models())
        assert "MISTRAL_API_KEY" in vars_
        assert "MISTRAL_CLIENT_API_KEY" in vars_
        assert "SERVER_URL" in vars_
        assert "DEPLOYMENT_NAME" in vars_
        assert "CA_BUNDLE" in vars_
        assert "TEMPORAL_SERVER_URL" in vars_
        assert "KUBERNETES_SERVICE_HOST" in vars_


class TestPrintConfig:
    def test_includes_key_config_fields(self, capsys):
        from mistralai.workflows.core.config.config import AppConfig

        _print_config(AppConfig())
        output = capsys.readouterr().out
        assert "server_url" in output
        assert "deployment_name" in output
        assert "task_queue" in output
        assert "_effective_task_queue" in output

    def test_secret_values_are_redacted(self, capsys, monkeypatch):
        monkeypatch.setenv("MISTRAL_API_KEY", "super-secret-value")
        from mistralai.workflows.core.config.config import AppConfig

        _print_config(AppConfig())
        output = capsys.readouterr().out
        assert "super-secret-value" not in output
        assert "***" in output


class TestPrintEnvVars:
    def test_masks_secret_vars(self, capsys, monkeypatch):
        monkeypatch.setenv("MISTRAL_API_KEY", "should-not-appear")
        _print_env_vars()
        output = capsys.readouterr().out
        assert "should-not-appear" not in output
        assert "*** (set)" in output


class TestCheckMistralApi:
    @pytest.mark.asyncio
    async def test_reports_fail_on_network_error(self, capsys):
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("unreachable"))

        with patch("httpx.AsyncClient", return_value=mock_client):
            await _check_mistral_api("https://api.mistral.ai", None)

        assert "[FAIL]" in capsys.readouterr().out


class TestCheckWhoami:
    @pytest.mark.asyncio
    async def test_returns_whoami_on_success(self):
        mock_whoami = MagicMock()
        mock_whoami.model_dump.return_value = {"worker_id": "w1", "tls": False}
        mock_wc = AsyncMock()
        mock_wc.__aenter__ = AsyncMock(return_value=mock_wc)
        mock_wc.__aexit__ = AsyncMock(return_value=None)
        mock_wc.whoami_async = AsyncMock(return_value=mock_whoami)

        with (
            patch("mistralai.workflows.core.worker_client.get_worker_client", return_value=mock_wc),
            patch("mistralai.workflows.client.translate_model", return_value=mock_whoami),
        ):
            result = await _check_whoami("https://api.mistral.ai", "key")

        assert result is mock_whoami

    @pytest.mark.asyncio
    async def test_returns_none_and_prints_fail_on_error(self, capsys):
        with patch(
            "mistralai.workflows.core.worker_client.get_worker_client", side_effect=Exception("connection failed")
        ):
            result = await _check_whoami("https://api.mistral.ai", None)

        assert result is None
        assert "[FAIL]" in capsys.readouterr().out
