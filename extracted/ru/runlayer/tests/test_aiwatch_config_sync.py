"""Tests for best-effort backend settings reconciliation."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx

from runlayer_cli import aiwatch_config_sync
from runlayer_cli.aiwatch_config_cache import SyncedAIWatchConfig

CONFIG: SyncedAIWatchConfig = {
    "version": 1,
    "daemon_enabled": False,
    "remove_uv_tool": True,
    "mode": "protect",
    "sessions": True,
    "mcp_usage_metadata": True,
    "browser_mode": "enforce",
    "browser_sessions": False,
    "detect_processes": True,
    "detect_containers": False,
    "detect_disguised_skills": True,
    "artifact_lookup_cache": True,
    "project_depth": 12,
    "project_timeout": 90,
}


def test_sync_persists_backend_config(monkeypatch):
    client = MagicMock()
    client.get_aiwatch_config.return_value = CONFIG
    client_class = MagicMock(return_value=client)
    write_config = MagicMock(return_value=True)
    monkeypatch.setattr(aiwatch_config_sync, "RunlayerClient", client_class)
    monkeypatch.setattr(aiwatch_config_sync, "write_backend_config", write_config)

    assert (
        aiwatch_config_sync.sync_backend_config(
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )
        is True
    )
    client_class.assert_called_once_with(
        hostname="https://tenant.runlayer.com",
        secret="rl_org_secret",
    )
    write_config.assert_called_once_with(CONFIG, "rl_org_secret")


def test_sync_keeps_last_good_cache_when_endpoint_is_unsupported(monkeypatch):
    client = MagicMock()
    client.get_aiwatch_config.return_value = None
    monkeypatch.setattr(
        aiwatch_config_sync, "RunlayerClient", MagicMock(return_value=client)
    )
    write_config = MagicMock()
    monkeypatch.setattr(aiwatch_config_sync, "write_backend_config", write_config)

    assert (
        aiwatch_config_sync.sync_backend_config(
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )
        is False
    )
    write_config.assert_not_called()


def test_sync_is_best_effort_on_network_failure(monkeypatch):
    request = httpx.Request("GET", "https://tenant.runlayer.com/api/v1/ai-watch/config")
    client = MagicMock()
    client.get_aiwatch_config.side_effect = httpx.ConnectError(
        "offline", request=request
    )
    monkeypatch.setattr(
        aiwatch_config_sync, "RunlayerClient", MagicMock(return_value=client)
    )

    assert (
        aiwatch_config_sync.sync_backend_config(
            host="https://tenant.runlayer.com",
            org_api_key="rl_org_secret",
        )
        is False
    )
