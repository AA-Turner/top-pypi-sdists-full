"""Tests for the privileged backend-settings cache."""

from __future__ import annotations

import json
import os
import stat

import pytest

from runlayer_cli import aiwatch_config_cache

CONFIG: aiwatch_config_cache.SyncedAIWatchConfig = {
    "version": 1,
    "daemon_enabled": True,
    "remove_uv_tool": True,
    "mode": "protect",
    "sessions": True,
    "mcp_usage_metadata": True,
    "detect_processes": True,
    "detect_containers": False,
    "detect_disguised_skills": True,
    "artifact_lookup_cache": True,
    "project_depth": 12,
    "project_timeout": 90,
    "browser_mode": "enforce",
    "browser_sessions": False,
    "browser_extension_enabled": True,
    "browser_extension_update_url": (
        "https://tenant.runlayer.com/api/v1/binary-packages/"
        "browser-extension/chrome/signed/update.xml"
    ),
    "firefox_browser_extension_install_url": (
        "https://downloads.runlayer.com/extension/firefox/"
        "runlayer-aiwatch-browser-extension-firefox-0.27.34.xpi"
    ),
}


class _FakeKey:
    def __init__(self, values):
        self.values = values

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


class _FakeWinreg:
    HKEY_LOCAL_MACHINE = object()
    KEY_READ = 1
    KEY_SET_VALUE = 2
    REG_SZ = 1

    def __init__(self):
        self.values = {}

    def OpenKey(self, *_args):
        return _FakeKey(self.values)

    def CreateKeyEx(self, *_args):
        return _FakeKey(self.values)

    def QueryValueEx(self, key, name):
        try:
            return key.values[name], self.REG_SZ
        except KeyError as exc:
            raise FileNotFoundError(name) from exc

    def SetValueEx(self, key, name, _reserved, _reg_type, value):
        key.values[name] = value


def test_macos_cache_round_trip_is_key_bound_and_world_readable(tmp_path, monkeypatch):
    cache_path = tmp_path / "backend-config.json"
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(aiwatch_config_cache, "MACOS_CACHE_PATH", cache_path)

    assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True

    cached = aiwatch_config_cache.read_backend_config("rl_org_one")
    assert cached is not None
    assert cached == CONFIG
    assert aiwatch_config_cache.read_backend_config("rl_org_two") is None
    assert stat.S_IMODE(cache_path.stat().st_mode) == 0o644
    assert "rl_org_one" not in cache_path.read_text()


def test_macos_cache_rejects_entire_invalid_snapshot(tmp_path, monkeypatch):
    cache_path = tmp_path / "backend-config.json"
    cache_path.write_text(
        json.dumps(
            {
                **CONFIG,
                "project_depth": 21,
                "org_api_key_hash": aiwatch_config_cache.hash_org_api_key("rl_org_one"),
            }
        )
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(aiwatch_config_cache, "MACOS_CACHE_PATH", cache_path)

    assert aiwatch_config_cache.read_backend_config("rl_org_one") is None


@pytest.mark.parametrize(
    "override",
    [
        {"version": 2},
        {"mode": "invalid"},
        {"browser_mode": "invalid"},
        {"sessions": 1},
        {"mcp_usage_metadata": 1},
        {"browser_sessions": 1},
        {"browser_extension_enabled": 1},
        {"browser_extension_update_url": 1},
        {"firefox_browser_extension_install_url": False},
        {"detect_processes": "true"},
        {"detect_containers": None},
        {"project_depth": 0},
        {"project_timeout": 301},
    ],
)
def test_parse_rejects_invalid_or_partial_snapshot(override):
    with pytest.raises(ValueError):
        aiwatch_config_cache.parse_aiwatch_config({**CONFIG, **override})


def test_linux_cache_round_trip_is_key_bound_and_world_readable(tmp_path, monkeypatch):
    cache_path = tmp_path / "backend-config.json"
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path)

    assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True

    cached = aiwatch_config_cache.read_backend_config("rl_org_one")
    assert cached is not None
    assert cached == CONFIG
    assert aiwatch_config_cache.read_backend_config("rl_org_two") is None
    assert stat.S_IMODE(cache_path.stat().st_mode) == 0o644
    assert "rl_org_one" not in cache_path.read_text()


def test_linux_cache_created_under_restrictive_umask_is_world_readable(
    tmp_path, monkeypatch
):
    cache_root = tmp_path / "var"
    cache_path = cache_root / "lib" / "runlayer" / "aiwatch" / "backend-config.json"
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path)

    previous_umask = os.umask(0o077)
    try:
        assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True
    finally:
        os.umask(previous_umask)

    created_directories = (
        cache_root,
        cache_root / "lib",
        cache_root / "lib" / "runlayer",
        cache_root / "lib" / "runlayer" / "aiwatch",
    )
    assert all(
        stat.S_IMODE(directory.stat().st_mode) == 0o755
        for directory in created_directories
    )
    assert aiwatch_config_cache.read_backend_config("rl_org_one") == CONFIG


def test_linux_cache_preserves_preexisting_ancestor_mode(tmp_path, monkeypatch):
    existing_ancestor = tmp_path / "var" / "lib"
    existing_ancestor.mkdir(parents=True)
    existing_ancestor.chmod(0o700)
    cache_path = existing_ancestor / "runlayer" / "aiwatch" / "backend-config.json"
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path)

    previous_umask = os.umask(0o077)
    try:
        assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True
    finally:
        os.umask(previous_umask)

    assert stat.S_IMODE(existing_ancestor.stat().st_mode) == 0o700
    assert stat.S_IMODE((existing_ancestor / "runlayer").stat().st_mode) == 0o755
    assert (
        stat.S_IMODE((existing_ancestor / "runlayer" / "aiwatch").stat().st_mode)
        == 0o755
    )


def test_linux_cache_heals_preexisting_restrictive_runlayer_directories(
    tmp_path, monkeypatch
):
    system_ancestor = tmp_path / "var" / "lib"
    runlayer_root = system_ancestor / "runlayer"
    cache_dir = runlayer_root / "aiwatch"
    cache_dir.mkdir(parents=True)
    cache_dir.chmod(0o700)
    runlayer_root.chmod(0o700)
    system_ancestor.chmod(0o700)
    cache_path = cache_dir / "backend-config.json"
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path)

    assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True

    assert stat.S_IMODE(runlayer_root.stat().st_mode) == 0o755
    assert stat.S_IMODE(cache_dir.stat().st_mode) == 0o755
    assert stat.S_IMODE(system_ancestor.stat().st_mode) == 0o700


def test_linux_cache_rejects_entire_invalid_snapshot(tmp_path, monkeypatch):
    cache_path = tmp_path / "backend-config.json"
    cache_path.write_text(
        json.dumps(
            {
                **CONFIG,
                "project_timeout": 301,
                "org_api_key_hash": aiwatch_config_cache.hash_org_api_key("rl_org_one"),
            }
        )
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(aiwatch_config_cache, "LINUX_CACHE_PATH", cache_path)

    assert aiwatch_config_cache.read_backend_config("rl_org_one") is None


def test_unsupported_platform_does_not_persist(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "FreeBSD")

    assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is False
    assert aiwatch_config_cache.read_backend_config("rl_org_one") is None


def test_legacy_snapshot_inherits_browser_settings():
    legacy = {
        key: value
        for key, value in CONFIG.items()
        if key
        not in {
            "browser_mode",
            "browser_sessions",
            "browser_extension_enabled",
            "daemon_enabled",
            "mcp_usage_metadata",
            "remove_uv_tool",
            "artifact_lookup_cache",
        }
    }

    parsed = aiwatch_config_cache.parse_aiwatch_config(legacy)

    assert parsed["daemon_enabled"] is False
    assert parsed["remove_uv_tool"] is False
    assert parsed["browser_mode"] == "protect"
    assert parsed["browser_sessions"] is True
    assert parsed["mcp_usage_metadata"] is False
    assert parsed["artifact_lookup_cache"] is False
    assert "browser_extension_enabled" not in parsed


@pytest.mark.parametrize("value", [None, 0, "true"])
def test_invalid_optional_daemon_gate_fails_dark(value):
    parsed = aiwatch_config_cache.parse_aiwatch_config(
        {**CONFIG, "daemon_enabled": value}
    )

    assert parsed["daemon_enabled"] is False


@pytest.mark.parametrize("value", [None, 0, "true"])
def test_invalid_optional_remove_uv_tool_fails_dark(value):
    parsed = aiwatch_config_cache.parse_aiwatch_config(
        {**CONFIG, "remove_uv_tool": value}
    )

    assert parsed["remove_uv_tool"] is False


@pytest.mark.parametrize("value", [None, 0, "true"])
def test_invalid_optional_gzip_hooks_fails_dark(value):
    """Missing/malformed gzip_hooks stays absent without invalidating the
    otherwise-complete snapshot (ENG-5919)."""
    parsed = aiwatch_config_cache.parse_aiwatch_config({**CONFIG, "gzip_hooks": value})

    assert "gzip_hooks" not in parsed


def test_gzip_hooks_bool_round_trips():
    parsed = aiwatch_config_cache.parse_aiwatch_config({**CONFIG, "gzip_hooks": True})

    assert parsed["gzip_hooks"] is True


@pytest.mark.parametrize("value", [None, 0, "true"])
def test_missing_or_invalid_disguised_skill_detection_fails_dark(value):
    payload = {**CONFIG, "detect_disguised_skills": value}
    if value is None:
        payload.pop("detect_disguised_skills")

    parsed = aiwatch_config_cache.parse_aiwatch_config(payload)

    assert parsed["detect_disguised_skills"] is False


@pytest.mark.parametrize("value", [None, 0, "true"])
def test_missing_or_invalid_artifact_lookup_cache_fails_dark(value):
    payload = {**CONFIG, "artifact_lookup_cache": value}
    if value is None:
        payload.pop("artifact_lookup_cache")

    parsed = aiwatch_config_cache.parse_aiwatch_config(payload)

    assert parsed["artifact_lookup_cache"] is False


def test_windows_cache_round_trip_is_one_key_bound_json_value(monkeypatch):
    fake_winreg = _FakeWinreg()
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setattr(aiwatch_config_cache, "winreg", fake_winreg)

    assert aiwatch_config_cache.write_backend_config(CONFIG, "rl_org_one") is True

    cached = aiwatch_config_cache.read_backend_config("rl_org_one")
    assert cached is not None
    assert cached == CONFIG
    assert aiwatch_config_cache.read_backend_config("rl_org_two") is None
    assert set(fake_winreg.values) == {"BackendConfig"}
    assert "rl_org_one" not in next(iter(fake_winreg.values.values()))


@pytest.mark.parametrize("value", [None, 7, "zstd", {"zstd": True}])
def test_invalid_hook_wire_encodings_fails_dark(value):
    parsed = aiwatch_config_cache.parse_aiwatch_config(
        {**CONFIG, "hook_wire_encodings": value}
    )

    assert "hook_wire_encodings" not in parsed


def test_hook_wire_encodings_filters_unknown_codecs():
    """A future backend codec must not make this client claim support."""
    parsed = aiwatch_config_cache.parse_aiwatch_config(
        {**CONFIG, "hook_wire_encodings": ["brotli", "zstd", 3, "gzip"]}
    )

    assert parsed["hook_wire_encodings"] == ("zstd", "gzip")
