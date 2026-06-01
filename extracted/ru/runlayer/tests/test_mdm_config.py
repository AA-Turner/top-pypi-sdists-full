"""Tests for MDM-managed config lookup."""

from __future__ import annotations

import os
import plistlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli import mdm_config
from runlayer_cli.aiwatch import _apply_managed_config

try:
    import winreg
except ImportError:
    winreg = None  # type: ignore[assignment]


def _write_plist(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        plistlib.dump(payload, f)


def test_read_returns_empty_when_no_config(tmp_path, monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (tmp_path / "missing.plist",))
    assert mdm_config.read_managed_config() == {}


def test_read_macos_managed_plist(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed, {"Host": "https://tenant.runlayer.com", "OrgApiKey": "rl_org_secret"}
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }


def test_macos_managed_preferred_over_local(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Host": "https://managed.example.com"})
    _write_plist(local, {"Host": "https://local.example.com"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {"host": "https://managed.example.com"}


def test_macos_falls_through_to_local_when_managed_missing(tmp_path, monkeypatch):
    managed = tmp_path / "missing.plist"
    local = tmp_path / "local.plist"
    _write_plist(local, {"OrgApiKey": "rl_org_secret"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {"org_api_key": "rl_org_secret"}


def test_macos_merges_partial_configs_across_plists(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Host": "https://managed.example.com"})
    _write_plist(local, {"OrgApiKey": "rl_org_local"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {
        "host": "https://managed.example.com",
        "org_api_key": "rl_org_local",
    }


def test_macos_first_plist_wins_per_key(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Host": "https://managed.example.com"})
    _write_plist(
        local,
        {"Host": "https://local.example.com", "OrgApiKey": "rl_org_local"},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {
        "host": "https://managed.example.com",
        "org_api_key": "rl_org_local",
    }


def test_macos_rejects_malformed_plist(tmp_path, monkeypatch):
    managed = tmp_path / "bad.plist"
    managed.write_text("not a plist")
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_non_string_values(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Host": 42, "OrgApiKey": ""})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_linux_returns_empty(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert mdm_config.read_managed_config() == {}


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_registry(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "Host", 0, winreg.REG_SZ, "https://tenant.runlayer.com")
        winreg.SetValueEx(key, "OrgApiKey", 0, winreg.REG_SZ, "rl_org_secret")

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {
            "host": "https://tenant.runlayer.com",
            "org_api_key": "rl_org_secret",
        }
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


def test_apply_managed_config_injects_env(monkeypatch):
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={
            "host": "https://t.runlayer.com",
            "org_api_key": "rl_org_secret",
        },
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_HOST"] == "https://t.runlayer.com"
    assert os.environ["RUNLAYER_API_KEY"] == "rl_org_secret"


def test_apply_managed_config_does_not_override_existing_env(monkeypatch):
    monkeypatch.setenv("RUNLAYER_HOST", "https://explicit.example.com")
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_explicit")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={
            "host": "https://managed.example.com",
            "org_api_key": "rl_org_managed",
        },
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_HOST"] == "https://explicit.example.com"
    assert os.environ["RUNLAYER_API_KEY"] == "rl_org_explicit"


def test_apply_managed_config_noop_when_nothing_managed(monkeypatch):
    monkeypatch.delenv("RUNLAYER_HOST", raising=False)
    monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)
    with patch("runlayer_cli.aiwatch.read_managed_config", return_value={}):
        _apply_managed_config()
    assert "RUNLAYER_HOST" not in os.environ
    assert "RUNLAYER_API_KEY" not in os.environ
