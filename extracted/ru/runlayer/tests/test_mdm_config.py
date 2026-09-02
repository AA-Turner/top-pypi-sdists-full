"""Tests for MDM-managed config lookup."""

from __future__ import annotations

import json
import os
import plistlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from runlayer_cli import mdm_config
from runlayer_cli import runtime
from runlayer_cli.aiwatch import _apply_managed_config

try:
    import winreg
except ImportError:
    winreg = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _isolate_macos_cli_preferences(monkeypatch) -> None:
    """Keep developer-managed CLI preferences out of MDM unit tests."""
    monkeypatch.setattr(mdm_config, "CLI_MACOS_PLIST_PATHS", ())


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
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "GrokHome": ".grok-custom",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "grok_home": ".grok-custom",
    }


def test_read_macos_backend_snapshot_overrides_only_synced_fields(
    tmp_path, monkeypatch
):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "Mode": "monitor",
            "Sessions": False,
            "DetectProcesses": False,
            "DetectContainers": True,
            "GzipHooks": False,
            "DetectDisguisedSkills": True,
            "ProjectDepth": 7,
            "ProjectTimeout": 60,
            "AutoUpdate": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    monkeypatch.setattr(
        mdm_config,
        "read_backend_config",
        lambda org_api_key: (
            {
                "version": 1,
                "daemon_enabled": True,
                "mode": "protect",
                "sessions": True,
                "mcp_usage_metadata": True,
                "browser_mode": "monitor",
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
                "detect_processes": True,
                "detect_containers": False,
                "gzip_hooks": True,
                "detect_disguised_skills": False,
                "artifact_lookup_cache": True,
                "hook_wire_encodings": ("zstd", "gzip"),
                "project_depth": 12,
                "project_timeout": 90,
            }
            if org_api_key == "rl_org_secret"
            else None
        ),
    )

    result = mdm_config.read_managed_config()
    assert result == {
        "daemon_enabled": True,
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "mode": mdm_config.AIWatchMode.PROTECT,
        "sessions": True,
        "mcp_usage_metadata": True,
        "browser_mode": mdm_config.AIWatchMode.MONITOR,
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
        "detect_processes": True,
        "detect_containers": False,
        "gzip_hooks": True,
        "detect_disguised_skills": False,
        "artifact_lookup_cache": True,
        "hook_wire_encodings": ("zstd", "gzip"),
        "project_depth": 12,
        "project_timeout": 90,
        "auto_update": False,
    }
    assert mdm_config.resolve_include_pipeline(False, result) is True
    assert mdm_config.resolve_install_hooks(result) is True


def test_gzip_hooks_plist_survives_snapshot_without_the_key(tmp_path, monkeypatch):
    """Back-compat bootstrap (ENG-5919): a locally-managed GzipHooks key holds
    until the backend snapshot actually carries the field; when it does, the
    backend value wins (covered by the override test above)."""
    managed = tmp_path / "com.runlayer.aiwatch.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "GzipHooks": True,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    monkeypatch.setattr(
        mdm_config,
        "read_backend_config",
        lambda org_api_key: {
            "version": 1,
            "daemon_enabled": True,
            "mode": "monitor",
            "sessions": True,
            "mcp_usage_metadata": False,
            "browser_mode": "monitor",
            "browser_sessions": True,
            "detect_processes": False,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
        },
    )

    result = mdm_config.read_managed_config()

    assert result["gzip_hooks"] is True


def test_read_macos_ignores_legacy_browser_surface_policy_fields(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "OrgApiKey": "rl_org_secret",
            "Mode": "enforce",
            "BrowserSurfaceExplorationEnabled": True,
            "BrowserSurfaceCandidateTelemetryEnabled": True,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {
        "org_api_key": "rl_org_secret",
        "mode": mdm_config.AIWatchMode.ENFORCE,
    }


def test_read_macos_includes_skill_sync_org_api_key(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "SkillSyncOrgApiKey": "rl_org_sync_secret",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "skill_sync_org_api_key": "rl_org_sync_secret",
    }


def test_read_macos_rejects_placeholder_skill_sync_org_api_key(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {"SkillSyncOrgApiKey": "REPLACE_WITH_SKILL_SYNC_ORG_API_KEY_OR_LEAVE_BLANK"},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert "skill_sync_org_api_key" not in mdm_config.read_managed_config()


def test_read_linux_includes_skill_sync_org_api_key(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"SkillSyncOrgApiKey": "rl_org_sync_secret"}), encoding="utf-8"
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (config,))
    assert mdm_config.read_managed_config() == {
        "skill_sync_org_api_key": "rl_org_sync_secret"
    }


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_skill_sync_org_api_key(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(
            key, "SkillSyncOrgApiKey", 0, winreg.REG_SZ, "rl_org_sync_secret"
        )

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {"skill_sync_org_api_key": "rl_org_sync_secret"}
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


def test_read_macos_includes_enrollment_fields(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "EnrollmentKey": "rl_enroll_secret",
            "Username": "user@example.com",
            "DeviceName": "Mac-1",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "enrollment_key": "rl_enroll_secret",
        "username": "user@example.com",
        "device_name": "Mac-1",
    }


def test_read_macos_ignores_legacy_browser_surface_policy_fields(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "BrowserExtensionId": "a" * 32,
            "BrowserExtensionUpdateUrl": "https://extensions.example/update.xml",
            "FirefoxBrowserExtensionId": "aiwatch@runlayer.com",
            "FirefoxBrowserExtensionInstallUrl": "https://extensions.example/aiwatch.xpi",
            "BrowserSurfaceExplorationEnabled": True,
            "BrowserSurfaceCandidateTelemetryEnabled": True,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "browser_extension_id": "a" * 32,
        "browser_extension_update_url": "https://extensions.example/update.xml",
        "firefox_browser_extension_id": "aiwatch@runlayer.com",
        "firefox_browser_extension_install_url": "https://extensions.example/aiwatch.xpi",
    }


def test_read_macos_rejects_non_bool_browser_surface_exploration(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"BrowserSurfaceExplorationEnabled": "true"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "browser_surface_exploration_enabled" not in result


def test_read_macos_rejects_non_bool_browser_surface_candidate_telemetry(
    tmp_path, monkeypatch
):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"BrowserSurfaceCandidateTelemetryEnabled": "true"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "browser_surface_candidate_telemetry_enabled" not in result


def test_read_macos_includes_detect_processes(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectProcesses": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"detect_processes": True}


def test_read_macos_rejects_non_bool_detect_processes(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectProcesses": "yes"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "detect_processes" not in result


def test_read_macos_includes_detect_containers(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectContainers": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"detect_containers": True}


def test_read_macos_rejects_non_bool_detect_containers(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectContainers": "yes"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "detect_containers" not in result


def test_read_macos_includes_detect_disguised_skills(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectDisguisedSkills": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"detect_disguised_skills": True}


def test_read_macos_rejects_non_bool_detect_disguised_skills(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"DetectDisguisedSkills": "yes"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "detect_disguised_skills" not in result


def test_read_macos_ignores_native_artifact_lookup_cache(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ArtifactLookupCache": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))

    assert mdm_config.read_managed_config() == {}


def test_read_macos_enrollment_only_for_hook_only_install(tmp_path, monkeypatch):
    """Hook-only deploy: EnrollmentKey present, OrgApiKey absent (scan disabled)."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "EnrollmentKey": "rl_enroll_secret",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "enrollment_key": "rl_enroll_secret",
    }


def test_macos_managed_preferred_over_local(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(
        managed,
        {
            "Host": "https://managed.example.com",
            "OrgApiKey": "rl_org_managed",
        },
    )
    _write_plist(
        local,
        {
            "Host": "https://local.example.com",
            "OrgApiKey": "rl_org_local",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {
        "host": "https://managed.example.com",
        "org_api_key": "rl_org_managed",
    }


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


def test_full_cli_prefers_cli_domain_then_falls_back_to_aiwatch_per_key(
    tmp_path, monkeypatch
):
    cli_managed = tmp_path / "cli-managed.plist"
    aiwatch_managed = tmp_path / "aiwatch-managed.plist"
    _write_plist(
        cli_managed,
        {
            "Host": "https://cli.example.com",
            "OrgApiKey": "rl_org_cli",
        },
    )
    _write_plist(
        aiwatch_managed,
        {
            "Host": "https://aiwatch.example.com",
            "OrgApiKey": "rl_org_aiwatch",
            "Sessions": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(
        mdm_config,
        "CLI_MACOS_PLIST_PATHS",
        (cli_managed,),
        raising=False,
    )
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (aiwatch_managed,))
    monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: False)
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {
        "host": "https://cli.example.com",
        "org_api_key": "rl_org_cli",
        "sessions": False,
    }


def test_full_cli_macos_orders_cli_managed_local_before_aiwatch_managed_local(
    tmp_path, monkeypatch
):
    cli_managed = tmp_path / "cli-managed.plist"
    cli_local = tmp_path / "cli-local.plist"
    aiwatch_managed = tmp_path / "aiwatch-managed.plist"
    aiwatch_local = tmp_path / "aiwatch-local.plist"
    _write_plist(cli_managed, {"Host": "https://cli-managed.example.com"})
    _write_plist(
        cli_local,
        {
            "Host": "https://cli-local.example.com",
            "OrgApiKey": "rl_org_cli_local",
        },
    )
    _write_plist(
        aiwatch_managed,
        {
            "OrgApiKey": "rl_org_aiwatch_managed",
            "Sessions": False,
        },
    )
    _write_plist(
        aiwatch_local,
        {
            "Sessions": True,
            "AutoUpdate": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(
        mdm_config,
        "CLI_MACOS_PLIST_PATHS",
        (cli_managed, cli_local),
    )
    monkeypatch.setattr(
        mdm_config,
        "MACOS_PLIST_PATHS",
        (aiwatch_managed, aiwatch_local),
    )
    monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: False)
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {
        "host": "https://cli-managed.example.com",
        "org_api_key": "rl_org_cli_local",
        "sessions": False,
        "auto_update": False,
    }


def test_aiwatch_runtime_ignores_cli_macos_domain(tmp_path, monkeypatch):
    cli_managed = tmp_path / "cli-managed.plist"
    aiwatch_managed = tmp_path / "aiwatch-managed.plist"
    _write_plist(
        cli_managed,
        {
            "Host": "https://cli.example.com",
            "SyncSkills": False,
        },
    )
    _write_plist(aiwatch_managed, {"OrgApiKey": "rl_org_aiwatch"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "CLI_MACOS_PLIST_PATHS", (cli_managed,))
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (aiwatch_managed,))
    monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: True)
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {"org_api_key": "rl_org_aiwatch"}


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


def test_macos_rejects_template_placeholders(tmp_path, monkeypatch):
    """Unedited shipped mobileconfig (REPLACE_WITH_* placeholders) must read as empty.

    Operators who upload the .mobileconfig template without find-and-replace
    would otherwise push the literal placeholder strings as live host /
    org_api_key / enrollment_key — invalid material that scan would send as
    `RUNLAYER_API_KEY` and the hook would feed into /api/v1/mdm/enroll on
    every fire (only rate-limited by the 60 s cooldown file).
    """
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "REPLACE_WITH_TENANT_HOST",
            "OrgApiKey": "REPLACE_WITH_ORG_API_KEY",
            "EnrollmentKey": "REPLACE_WITH_ENROLLMENT_KEY_OR_LEAVE_BLANK",
            "Username": "REPLACE_WITH_USERNAME_OR_LEAVE_BLANK",
            "DeviceName": "REPLACE_WITH_DEVICE_NAME_OR_LEAVE_BLANK",
            "Mode": "REPLACE_WITH_MODE_OR_LEAVE_BLANK",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_or_leave_blank_suffix(tmp_path, monkeypatch):
    """Defense-in-depth: any placeholder ending in _OR_LEAVE_BLANK is ignored."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_real",
            "EnrollmentKey": "SOMETHING_OR_LEAVE_BLANK",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_real",
    }


def test_macos_keeps_real_values_alongside_placeholder(tmp_path, monkeypatch):
    """Real values survive; only the placeholder fields drop out."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_real",
            "EnrollmentKey": "REPLACE_WITH_ENROLLMENT_KEY_OR_LEAVE_BLANK",
            "Username": "REPLACE_WITH_USERNAME_OR_LEAVE_BLANK",
            "DeviceName": "REPLACE_WITH_DEVICE_NAME_OR_LEAVE_BLANK",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_real",
    }


def test_ws1_unsubstituted_custom_attribute_filtered(tmp_path, monkeypatch):
    """Workspace ONE pushes `{CustomAttribute3}` literal when the admin uploaded
    the WS1 mobileconfig template but never assigned that Custom Attribute.

    Without filtering, the literal `{CustomAttribute3}` would be POSTed to
    `/api/v1/mdm/enroll` as the enrollment key and trigger fail-loud spam.
    """
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_real",
            "EnrollmentKey": "{CustomAttribute3}",
            "Username": "{EnrollmentUser}",
            "DeviceName": "{DeviceUid}",
            "Mode": "{CustomAttribute5}",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_real",
    }


def test_ws1_lookup_token_filter_does_not_match_real_values(tmp_path, monkeypatch):
    """Real values that contain braces in the middle (e.g. templated URLs)
    must survive — the WS1 regex only matches `{LookupName}` whole-string."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://foo.com/{path}/api",
            "OrgApiKey": "rl_org_{notatoken}_real",
            "EnrollmentKey": "rl_enroll_real",
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://foo.com/{path}/api",
        "org_api_key": "rl_org_{notatoken}_real",
        "enrollment_key": "rl_enroll_real",
    }


# ── Linux managed config (/etc/runlayer/aiwatch/config.json) ────────────


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def test_linux_returns_empty_when_no_config(tmp_path, monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (tmp_path / "missing.json",))
    assert mdm_config.read_managed_config() == {}


def test_linux_reads_config_json(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(
        cfg, {"Host": "https://tenant.runlayer.com", "OrgApiKey": "rl_org_secret"}
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
    }


_LINUX_SNAPSHOT = {
    "version": 1,
    "daemon_enabled": False,
    "mode": "monitor",
    "sessions": False,
    "mcp_usage_metadata": False,
    "browser_mode": "monitor",
    "browser_sessions": False,
    "detect_processes": True,
    "detect_containers": True,
    "detect_disguised_skills": True,
    "artifact_lookup_cache": True,
    "project_depth": 9,
    "project_timeout": 120,
}


def test_linux_backend_snapshot_binds_to_env_org_key(tmp_path, monkeypatch):
    """Linux keeps the org key out of the world-readable config; the snapshot
    binds to the RUNLAYER_API_KEY the root cron wrapper hands scan children."""
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_env_secret")
    monkeypatch.setattr(
        mdm_config,
        "read_backend_config",
        lambda org_api_key: (
            dict(_LINUX_SNAPSHOT) if org_api_key == "rl_org_env_secret" else None
        ),
    )

    result = mdm_config.read_managed_config()

    assert result["detect_processes"] is True
    assert result["detect_containers"] is True
    assert result["detect_disguised_skills"] is True
    assert result["artifact_lookup_cache"] is True
    assert result["project_depth"] == 9
    assert result["project_timeout"] == 120


def test_linux_managed_org_key_wins_over_env_for_snapshot_binding(
    tmp_path, monkeypatch
):
    cfg = tmp_path / "config.json"
    _write_json(
        cfg, {"Host": "https://tenant.runlayer.com", "OrgApiKey": "rl_org_managed"}
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    monkeypatch.setenv("RUNLAYER_API_KEY", "rl_org_env_secret")
    seen: list[str] = []

    def fake_read(org_api_key: str):
        seen.append(org_api_key)
        return None

    monkeypatch.setattr(mdm_config, "read_backend_config", fake_read)

    mdm_config.read_managed_config()

    assert seen == ["rl_org_managed"]


def test_linux_without_any_org_key_skips_snapshot(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    monkeypatch.delenv("RUNLAYER_API_KEY", raising=False)

    def fail_read(org_api_key: str):
        raise AssertionError("snapshot must not be read without a binding key")

    monkeypatch.setattr(mdm_config, "read_backend_config", fail_read)

    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
    }


@pytest.mark.parametrize("value", [True, False])
def test_linux_reads_auto_update_bool(tmp_path, monkeypatch, value):
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"AutoUpdate": value})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {"auto_update": value}


def test_linux_rejects_non_bool_auto_update(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"AutoUpdate": "false"})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


def test_linux_detect_only_fleet_config(tmp_path, monkeypatch):
    """The shipped Linux template contract: Sessions/Enforcement false ⇒
    scan-only fleet — enforce + sessions check-ins report `disabled` and the
    hook-install gate is off. Guards the Detect-only Linux distribution."""
    cfg = tmp_path / "config.json"
    _write_json(
        cfg,
        {
            "Host": "https://tenant.runlayer.com",
            "Sessions": False,
            "Enforcement": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    result = mdm_config.read_managed_config()
    assert result == {
        "host": "https://tenant.runlayer.com",
        "sessions": False,
        "enforcement": False,
    }
    assert mdm_config.resolve_include_pipeline(False, result) is False
    assert mdm_config.resolve_enforcement(result) is False
    assert mdm_config.resolve_install_hooks(result) is False


def test_linux_rejects_malformed_json(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    cfg.write_text("not json{")
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


def test_linux_rejects_non_dict_json(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(cfg, ["not", "a", "dict"])
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


def test_linux_rejects_template_placeholders(tmp_path, monkeypatch):
    """Unedited shipped config.json: the placeholder Host drops out while the
    real bool values survive, so an unconfigured install still reads as a
    scan-only fleet (and scan exits quietly with no host/key)."""
    cfg = tmp_path / "config.json"
    _write_json(
        cfg,
        {
            "Host": "REPLACE_WITH_RUNLAYER_HOST_URL_OR_LEAVE_BLANK",
            "Sessions": False,
            "Enforcement": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {
        "sessions": False,
        "enforcement": False,
    }


def test_linux_rejects_bad_types(tmp_path, monkeypatch):
    """Hand-edited JSON with wrong types is dropped field-by-field."""
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"Host": 42, "Sessions": "false", "ProjectDepth": "12"})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


def test_linux_reads_project_fields(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"ProjectDepth": 12, "ProjectTimeout": 120})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {
        "project_depth": 12,
        "project_timeout": 120,
    }


def test_linux_rejects_bool_project_fields(tmp_path, monkeypatch):
    """JSON true parses as Python bool; isinstance(True, int) is True, so the
    explicit bool exclusion in _parse_mapping must hold for JSON too."""
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"ProjectDepth": True, "ProjectTimeout": False})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


def test_linux_first_config_wins_per_key(tmp_path, monkeypatch):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    _write_json(first, {"Host": "https://first.example.com"})
    _write_json(
        second,
        {"Host": "https://second.example.com", "OrgApiKey": "rl_org_second"},
    )
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (first, second))
    assert mdm_config.read_managed_config() == {
        "host": "https://first.example.com",
        "org_api_key": "rl_org_second",
    }


class _FakeRegistryKey:
    def __init__(self, values):
        self.values = values

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None


class _FakeWinreg:
    HKEY_LOCAL_MACHINE = "HKLM"
    HKEY_CURRENT_USER = "HKCU"
    KEY_READ = 1
    REG_SZ = 1
    REG_DWORD = 4

    def __init__(self, values):
        self.values = values
        self.opened = []

    def OpenKey(self, hive, path, _reserved, _access):
        self.opened.append((hive, path))
        try:
            values = self.values[(hive, path)]
        except KeyError as exc:
            raise FileNotFoundError(path) from exc
        return _FakeRegistryKey(values)

    def QueryValueEx(self, key, name):
        try:
            return key.values[name]
        except KeyError as exc:
            raise FileNotFoundError(name) from exc


def test_full_cli_windows_orders_cli_domain_before_aiwatch_across_hives(
    monkeypatch,
):
    """Domain-major precedence, mirroring macOS: any CLI value (even HKCU)
    beats any AI Watch value (even HKLM). Within a domain, HKLM beats HKCU."""
    cli_path = r"Software\RunlayerTest\CLI"
    aiwatch_path = r"Software\RunlayerTest\AIWatch"
    fake_winreg = _FakeWinreg(
        {
            ("HKLM", cli_path): {
                "Host": ("https://machine-cli.example.com", _FakeWinreg.REG_SZ),
            },
            ("HKLM", aiwatch_path): {
                "OrgApiKey": ("rl_org_machine_aiwatch", _FakeWinreg.REG_SZ),
            },
            ("HKCU", cli_path): {
                "Host": ("https://user-cli.example.com", _FakeWinreg.REG_SZ),
                "OrgApiKey": ("rl_org_user_cli", _FakeWinreg.REG_SZ),
                "Sessions": (0, _FakeWinreg.REG_DWORD),
            },
            ("HKCU", aiwatch_path): {
                "Sessions": (1, _FakeWinreg.REG_DWORD),
                "AutoUpdate": (0, _FakeWinreg.REG_DWORD),
            },
        }
    )
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setattr(mdm_config, "winreg", fake_winreg)
    monkeypatch.setattr(mdm_config, "CLI_REG_KEY_PATH", cli_path, raising=False)
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", aiwatch_path)
    monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: False)
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {
        "host": "https://machine-cli.example.com",
        "org_api_key": "rl_org_user_cli",
        "sessions": False,
        "auto_update": False,
    }
    assert fake_winreg.opened == [
        ("HKLM", cli_path),
        ("HKCU", cli_path),
        ("HKLM", aiwatch_path),
        ("HKCU", aiwatch_path),
    ]


def test_aiwatch_runtime_ignores_cli_windows_path(monkeypatch):
    cli_path = r"Software\RunlayerTest\CLI"
    aiwatch_path = r"Software\RunlayerTest\AIWatch"
    fake_winreg = _FakeWinreg(
        {
            ("HKLM", cli_path): {
                "Host": ("https://cli.example.com", _FakeWinreg.REG_SZ),
            },
            ("HKLM", aiwatch_path): {
                "OrgApiKey": ("rl_org_aiwatch", _FakeWinreg.REG_SZ),
            },
            ("HKCU", cli_path): {
                "SyncSkills": (0, _FakeWinreg.REG_DWORD),
            },
            ("HKCU", aiwatch_path): {
                "Sessions": (0, _FakeWinreg.REG_DWORD),
            },
        }
    )
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setattr(mdm_config, "winreg", fake_winreg)
    monkeypatch.setattr(mdm_config, "CLI_REG_KEY_PATH", cli_path)
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", aiwatch_path)
    monkeypatch.setattr(runtime, "is_aiwatch_runtime", lambda: True)
    monkeypatch.setattr(mdm_config, "read_backend_config", lambda _org_api_key: None)

    assert mdm_config.read_managed_config() == {
        "org_api_key": "rl_org_aiwatch",
        "sessions": False,
    }
    assert fake_winreg.opened == [
        ("HKLM", aiwatch_path),
        ("HKCU", aiwatch_path),
    ]


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


# ── Enforcement bool field (MDM-driven hook enforcement) ────────────────


def test_macos_reads_enforcement_true(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Enforcement": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"enforcement": True}


def test_macos_reads_enforcement_false(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Enforcement": False})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"enforcement": False}


def test_macos_enforcement_absent_omits_key(tmp_path, monkeypatch):
    """Absent Enforcement key means callers default to True themselves."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "enforcement" not in result


def test_macos_rejects_non_bool_enforcement(tmp_path, monkeypatch):
    """Garbage type (e.g. string from a hand-edited plist) is dropped."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Enforcement": "false"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "enforcement" not in result


def test_macos_reads_enforcement_alongside_strings(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "Enforcement": False,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "enforcement": False,
    }


def test_macos_enforcement_first_plist_wins(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Enforcement": False})
    _write_plist(local, {"Enforcement": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {"enforcement": False}


def test_macos_lower_trust_mode_cannot_override_higher_trust_enforcement(
    tmp_path, monkeypatch
):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Enforcement": True})
    _write_plist(local, {"Mode": "monitor"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))

    result = mdm_config.read_managed_config()

    assert result == {"enforcement": True}
    assert mdm_config.resolve_mode(result) is mdm_config.AIWatchMode.ENFORCE


def test_macos_lower_trust_enforcement_cannot_override_higher_trust_mode(
    tmp_path, monkeypatch
):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Mode": "monitor"})
    _write_plist(local, {"Enforcement": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))

    result = mdm_config.read_managed_config()

    assert result == {"mode": mdm_config.AIWatchMode.MONITOR}
    assert mdm_config.resolve_mode(result) is mdm_config.AIWatchMode.MONITOR


def test_macos_same_source_preserves_mode_and_legacy_enforcement(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Mode": "protect", "Enforcement": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))

    result = mdm_config.read_managed_config()

    assert result == {
        "mode": mdm_config.AIWatchMode.PROTECT,
        "enforcement": True,
    }
    assert mdm_config.resolve_mode(result) is mdm_config.AIWatchMode.PROTECT


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_enforcement_dword(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "Enforcement", 0, winreg.REG_DWORD, 0)

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {"enforcement": False}
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


# ── Mode enum field (overrides legacy Enforcement) ───────────────────────


@pytest.mark.parametrize(
    ("raw_mode", "expected"),
    [
        ("monitor", "monitor"),
        ("Protect", "protect"),
        ("  ENFORCE  ", "enforce"),
    ],
)
def test_macos_reads_normalized_mode(tmp_path, monkeypatch, raw_mode, expected):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Mode": raw_mode})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))

    assert mdm_config.read_managed_config() == {
        "mode": mdm_config.AIWatchMode(expected)
    }


@pytest.mark.parametrize("raw_mode", ["", "observe", 1, True])
def test_macos_rejects_invalid_mode(tmp_path, monkeypatch, raw_mode):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Mode": raw_mode, "Enforcement": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))

    assert mdm_config.read_managed_config() == {"enforcement": True}


def test_linux_reads_normalized_mode(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"Mode": " Protect "}))
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (config,))

    assert mdm_config.read_managed_config() == {"mode": mdm_config.AIWatchMode.PROTECT}


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_normalized_mode(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "Mode", 0, winreg.REG_SZ, "Protect")

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {"mode": mdm_config.AIWatchMode.PROTECT}
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


# ── Sessions bool field (MDM-driven event/session hook install) ─────────


def test_macos_reads_sessions_true(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Sessions": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"sessions": True}


def test_macos_reads_sessions_false(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Sessions": False})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"sessions": False}


def test_macos_sessions_absent_omits_key(tmp_path, monkeypatch):
    """Absent Sessions key lets callers use the fail-closed default."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "sessions" not in result


def test_macos_rejects_non_bool_sessions(tmp_path, monkeypatch):
    """Garbage type (e.g. string from a hand-edited plist) is dropped."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Sessions": "false"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "sessions" not in result


def test_macos_sessions_first_plist_wins(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"Sessions": False})
    _write_plist(local, {"Sessions": True})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {"sessions": False}


def test_macos_reads_sessions_alongside_enforcement(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Enforcement": False, "Sessions": False})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "enforcement": False,
        "sessions": False,
    }


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_sessions_dword(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "Sessions", 0, winreg.REG_DWORD, 0)

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {"sessions": False}
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


# ── AutoUpdate bool field (MDM-driven self-update gate) ──────────────


@pytest.mark.parametrize("value", [True, False])
def test_macos_reads_auto_update_bool(tmp_path, monkeypatch, value):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"AutoUpdate": value})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"auto_update": value}


def test_macos_rejects_non_bool_auto_update(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"AutoUpdate": "false"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert "auto_update" not in mdm_config.read_managed_config()


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, True),
        ({"auto_update": True}, True),
        ({"auto_update": False}, False),
    ],
)
def test_resolve_auto_update(managed, expected):
    assert mdm_config.resolve_auto_update(managed) is expected


def test_resolve_auto_update_reads_managed_when_none():
    with patch(
        "runlayer_cli.mdm_config.read_managed_config",
        return_value={"auto_update": False},
    ):
        assert mdm_config.resolve_auto_update() is False


# ── ProjectDepth / ProjectTimeout int fields (MDM-driven scan tuning) ──


def test_macos_reads_project_depth(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ProjectDepth": 12})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"project_depth": 12}


def test_macos_reads_project_timeout(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ProjectTimeout": 120})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {"project_timeout": 120}


def test_macos_reads_project_fields_alongside_strings(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "ProjectDepth": 20,
            "ProjectTimeout": 300,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "project_depth": 20,
        "project_timeout": 300,
    }


def test_macos_project_fields_absent_omits_keys(tmp_path, monkeypatch):
    """Absent keys mean scan keeps its typer defaults (7 / 60)."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "project_depth" not in result
    assert "project_timeout" not in result


def test_macos_rejects_non_int_project_fields(tmp_path, monkeypatch):
    """Garbage type (e.g. string from a hand-edited plist) is dropped."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ProjectDepth": "12", "ProjectTimeout": "120"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_bool_project_fields(tmp_path, monkeypatch):
    """isinstance(True, int) is True, so bool nodes must be excluded explicitly."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ProjectDepth": True, "ProjectTimeout": False})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_non_positive_project_fields(tmp_path, monkeypatch):
    """Zero / negative depth or timeout is nonsensical; drop it (=> default)."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"ProjectDepth": 0, "ProjectTimeout": -5})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_project_depth_first_plist_wins(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    local = tmp_path / "local.plist"
    _write_plist(managed, {"ProjectDepth": 9})
    _write_plist(local, {"ProjectDepth": 15})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed, local))
    assert mdm_config.read_managed_config() == {"project_depth": 9}


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_project_fields_dword(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "ProjectDepth", 0, winreg.REG_DWORD, 12)
        winreg.SetValueEx(key, "ProjectTimeout", 0, winreg.REG_DWORD, 120)

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {"project_depth": 12, "project_timeout": 120}
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_rejects_non_positive_project_dword(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "ProjectDepth", 0, winreg.REG_DWORD, 0)

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert "project_depth" not in result
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


# ── CpuCores / MaxCpuPercent / MemoryLimitMb int fields (resource caps) ─


def test_macos_reads_resource_cap_fields(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {"CpuCores": 2, "MaxCpuPercent": 40, "MemoryLimitMb": 512},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "cpu_cores": 2,
        "max_cpu_percent": 40,
        "memory_limit_mb": 512,
    }


def test_macos_reads_resource_caps_alongside_strings(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {
            "Host": "https://tenant.runlayer.com",
            "OrgApiKey": "rl_org_secret",
            "CpuCores": 4,
            "MaxCpuPercent": 75,
            "MemoryLimitMb": 2048,
        },
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "cpu_cores": 4,
        "max_cpu_percent": 75,
        "memory_limit_mb": 2048,
    }


def test_macos_resource_caps_absent_omits_keys(tmp_path, monkeypatch):
    """Absent keys mean scan keeps its typer defaults (half cores / 50% / 1024)."""
    managed = tmp_path / "managed.plist"
    _write_plist(managed, {"Host": "https://tenant.runlayer.com"})
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    result = mdm_config.read_managed_config()
    assert "cpu_cores" not in result
    assert "max_cpu_percent" not in result
    assert "memory_limit_mb" not in result


def test_macos_rejects_non_int_resource_caps(tmp_path, monkeypatch):
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {"CpuCores": "2", "MaxCpuPercent": "40", "MemoryLimitMb": "512"},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_bool_resource_caps(tmp_path, monkeypatch):
    """isinstance(True, int) is True, so bool nodes must be excluded explicitly."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {"CpuCores": True, "MaxCpuPercent": False, "MemoryLimitMb": True},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_macos_rejects_non_positive_resource_caps(tmp_path, monkeypatch):
    """Type-only guard drops <= 0; range clamping to the min is downstream."""
    managed = tmp_path / "managed.plist"
    _write_plist(
        managed,
        {"CpuCores": 0, "MaxCpuPercent": -5, "MemoryLimitMb": 0},
    )
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(mdm_config, "MACOS_PLIST_PATHS", (managed,))
    assert mdm_config.read_managed_config() == {}


def test_linux_reads_resource_cap_fields(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"CpuCores": 2, "MaxCpuPercent": 40, "MemoryLimitMb": 512})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {
        "cpu_cores": 2,
        "max_cpu_percent": 40,
        "memory_limit_mb": 512,
    }


def test_linux_rejects_bool_resource_caps(tmp_path, monkeypatch):
    """JSON true parses as Python bool; the explicit bool exclusion must hold."""
    cfg = tmp_path / "config.json"
    _write_json(cfg, {"CpuCores": True, "MaxCpuPercent": False, "MemoryLimitMb": True})
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(mdm_config, "LINUX_CONFIG_PATHS", (cfg,))
    assert mdm_config.read_managed_config() == {}


@pytest.mark.skipif(sys.platform != "win32", reason="Windows registry only")
def test_windows_reads_resource_cap_dwords(monkeypatch):
    assert winreg is not None
    test_key_path = r"Software\RunlayerTest\AIWatchTest"
    monkeypatch.setattr(mdm_config, "REG_KEY_PATH", test_key_path)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key_path) as key:
        winreg.SetValueEx(key, "CpuCores", 0, winreg.REG_DWORD, 2)
        winreg.SetValueEx(key, "MaxCpuPercent", 0, winreg.REG_DWORD, 40)
        winreg.SetValueEx(key, "MemoryLimitMb", 0, winreg.REG_DWORD, 512)

    try:
        with patch("platform.system", return_value="Windows"):
            result = mdm_config.read_managed_config()
        assert result == {
            "cpu_cores": 2,
            "max_cpu_percent": 40,
            "memory_limit_mb": 512,
        }
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key_path)


def test_apply_managed_config_injects_env(monkeypatch):
    # Pre-claim the env vars so monkeypatch tears them down even though
    # _apply_managed_config writes via os.environ[...] = directly.
    monkeypatch.setenv("RUNLAYER_HOST", "__placeholder__")
    monkeypatch.setenv("RUNLAYER_API_KEY", "__placeholder__")
    monkeypatch.delenv("RUNLAYER_HOST")
    monkeypatch.delenv("RUNLAYER_API_KEY")
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


def test_apply_managed_config_injects_project_env(monkeypatch):
    # Pre-claim so monkeypatch tears them down even though _apply_managed_config
    # writes via os.environ[...] = directly.
    for var in ("RUNLAYER_PROJECT_DEPTH", "RUNLAYER_PROJECT_TIMEOUT"):
        monkeypatch.setenv(var, "__placeholder__")
        monkeypatch.delenv(var)
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"project_depth": 12, "project_timeout": 120},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_PROJECT_DEPTH"] == "12"
    assert os.environ["RUNLAYER_PROJECT_TIMEOUT"] == "120"


def test_apply_managed_config_does_not_override_existing_project_env(monkeypatch):
    monkeypatch.setenv("RUNLAYER_PROJECT_DEPTH", "3")
    monkeypatch.setenv("RUNLAYER_PROJECT_TIMEOUT", "30")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"project_depth": 12, "project_timeout": 120},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_PROJECT_DEPTH"] == "3"
    assert os.environ["RUNLAYER_PROJECT_TIMEOUT"] == "30"


def test_apply_managed_config_injects_resource_cap_env(monkeypatch):
    # Pre-claim so monkeypatch tears them down even though _apply_managed_config
    # writes via os.environ[...] = directly.
    for var in (
        "RUNLAYER_CPU_CORES",
        "RUNLAYER_MAX_CPU_PERCENT",
        "RUNLAYER_MEMORY_LIMIT_MB",
    ):
        monkeypatch.setenv(var, "__placeholder__")
        monkeypatch.delenv(var)
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"cpu_cores": 2, "max_cpu_percent": 40, "memory_limit_mb": 512},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_CPU_CORES"] == "2"
    assert os.environ["RUNLAYER_MAX_CPU_PERCENT"] == "40"
    assert os.environ["RUNLAYER_MEMORY_LIMIT_MB"] == "512"


def test_apply_managed_config_does_not_override_existing_resource_cap_env(monkeypatch):
    monkeypatch.setenv("RUNLAYER_CPU_CORES", "1")
    monkeypatch.setenv("RUNLAYER_MAX_CPU_PERCENT", "10")
    monkeypatch.setenv("RUNLAYER_MEMORY_LIMIT_MB", "256")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"cpu_cores": 8, "max_cpu_percent": 90, "memory_limit_mb": 4096},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_CPU_CORES"] == "1"
    assert os.environ["RUNLAYER_MAX_CPU_PERCENT"] == "10"
    assert os.environ["RUNLAYER_MEMORY_LIMIT_MB"] == "256"


@pytest.mark.parametrize(
    ("managed_value", "expected_env"),
    [(True, "true"), (False, "false")],
)
def test_apply_managed_config_injects_detect_processes_env(
    monkeypatch, managed_value, expected_env
):
    # Pre-claim so monkeypatch tears it down even though _apply_managed_config
    # writes via os.environ[...] = directly.
    monkeypatch.setenv("RUNLAYER_DETECT_PROCESSES", "__placeholder__")
    monkeypatch.delenv("RUNLAYER_DETECT_PROCESSES")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_processes": managed_value},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_PROCESSES"] == expected_env


def test_apply_managed_config_does_not_override_existing_detect_processes_env(
    monkeypatch,
):
    monkeypatch.setenv("RUNLAYER_DETECT_PROCESSES", "false")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_processes": True},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_PROCESSES"] == "false"


@pytest.mark.parametrize(
    ("managed_value", "expected_env"),
    [(True, "true"), (False, "false")],
)
def test_apply_managed_config_injects_detect_containers_env(
    monkeypatch, managed_value, expected_env
):
    monkeypatch.setenv("RUNLAYER_DETECT_CONTAINERS", "__placeholder__")
    monkeypatch.delenv("RUNLAYER_DETECT_CONTAINERS")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_containers": managed_value},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_CONTAINERS"] == expected_env


def test_apply_managed_config_does_not_override_existing_detect_containers_env(
    monkeypatch,
):
    monkeypatch.setenv("RUNLAYER_DETECT_CONTAINERS", "false")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_containers": True},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_CONTAINERS"] == "false"


@pytest.mark.parametrize(
    ("managed_value", "expected_env"),
    [(True, "true"), (False, "false")],
)
def test_apply_managed_config_injects_detect_disguised_skills_env(
    monkeypatch, managed_value, expected_env
):
    monkeypatch.setenv("RUNLAYER_DETECT_DISGUISED_SKILLS", "__placeholder__")
    monkeypatch.delenv("RUNLAYER_DETECT_DISGUISED_SKILLS")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_disguised_skills": managed_value},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_DISGUISED_SKILLS"] == expected_env


def test_apply_managed_config_does_not_override_existing_disguised_skills_env(
    monkeypatch,
):
    monkeypatch.setenv("RUNLAYER_DETECT_DISGUISED_SKILLS", "false")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"detect_disguised_skills": True},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_DETECT_DISGUISED_SKILLS"] == "false"


@pytest.mark.parametrize(
    ("managed_value", "expected_env"),
    [(True, "true"), (False, "false")],
)
def test_apply_managed_config_injects_artifact_lookup_cache_env(
    monkeypatch, managed_value, expected_env
):
    monkeypatch.setenv("RUNLAYER_ARTIFACT_LOOKUP_CACHE", "__placeholder__")
    monkeypatch.delenv("RUNLAYER_ARTIFACT_LOOKUP_CACHE")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"artifact_lookup_cache": managed_value},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_ARTIFACT_LOOKUP_CACHE"] == expected_env


def test_apply_managed_config_does_not_override_existing_artifact_cache_env(
    monkeypatch,
):
    monkeypatch.setenv("RUNLAYER_ARTIFACT_LOOKUP_CACHE", "false")
    with patch(
        "runlayer_cli.aiwatch.read_managed_config",
        return_value={"artifact_lookup_cache": True},
    ):
        _apply_managed_config()
    assert os.environ["RUNLAYER_ARTIFACT_LOOKUP_CACHE"] == "false"


# ── resolve_mode (Mode overrides legacy Enforcement) ─────────────────────


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, "monitor"),
        ({"enforcement": False}, "monitor"),
        ({"enforcement": True}, "enforce"),
        ({"mode": "monitor", "enforcement": True}, "monitor"),
        ({"mode": "protect", "enforcement": False}, "protect"),
        ({"mode": "protect", "enforcement": True}, "protect"),
        ({"mode": "enforce", "enforcement": False}, "enforce"),
        ({"mode": "invalid", "enforcement": True}, "enforce"),
        ({"mode": 1, "enforcement": False}, "monitor"),
    ],
)
def test_resolve_mode_prefers_valid_mode_and_falls_back_to_enforcement(
    managed, expected
):
    assert mdm_config.resolve_mode(managed) is mdm_config.AIWatchMode(expected)


def test_resolve_mode_reads_managed_when_none():
    with patch(
        "runlayer_cli.mdm_config.read_managed_config",
        return_value={"mode": "protect", "enforcement": True},
    ):
        assert mdm_config.resolve_mode() is mdm_config.AIWatchMode.PROTECT


# ── resolve_install_hooks (Mode/Enforcement/Sessions install gate) ───────


def test_missing_sessions_is_fail_closed():
    managed: mdm_config.ManagedConfig = {}

    assert mdm_config.resolve_include_pipeline(False, managed) is False
    assert mdm_config.resolve_install_hooks(managed) is False


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, False),  # enforcement absent ⇒ false, sessions absent ⇒ false
        ({"enforcement": True, "sessions": True}, True),
        ({"enforcement": True, "sessions": False}, True),  # enforcement-only
        ({"enforcement": False, "sessions": True}, True),  # event/session only
        ({"enforcement": False, "sessions": False}, False),  # scan-only no-op
        ({"enforcement": True}, True),  # legacy enforcement enables hooks
        ({"enforcement": False}, False),  # sessions absent ⇒ fail closed
        ({"sessions": False}, False),  # enforcement absent ⇒ false ⇒ scan-only
        ({"sessions": True}, True),  # enforcement absent ⇒ false, sessions on
        ({"mode": "monitor", "enforcement": True, "sessions": False}, False),
        (
            {
                "mode": "monitor",
                "enforcement": False,
                "sessions": False,
                "mcp_usage_metadata": True,
            },
            True,
        ),
        # Sessions key ABSENT + metadata true must fail closed: metadata-only
        # requires an explicit Sessions=false, so no hooks install at all.
        ({"mode": "monitor", "enforcement": False, "mcp_usage_metadata": True}, False),
        ({"mode": "monitor", "enforcement": False, "sessions": True}, True),
        ({"mode": "protect", "enforcement": False, "sessions": False}, True),
        ({"mode": "enforce", "enforcement": False, "sessions": False}, True),
        ({"mode": "invalid", "enforcement": True, "sessions": False}, True),
        ({"mode": "invalid", "enforcement": False, "sessions": False}, False),
    ],
)
def test_resolve_install_hooks(managed, expected):
    assert mdm_config.resolve_install_hooks(managed) is expected


def test_resolve_install_hooks_reads_managed_when_none(monkeypatch):
    with patch(
        "runlayer_cli.mdm_config.read_managed_config",
        return_value={"enforcement": False, "sessions": False},
    ):
        assert mdm_config.resolve_install_hooks() is False


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, False),
        ({"mode": "monitor", "sessions": False}, False),
        # Sessions key absent is NOT sessions-off: the privacy profile needs
        # the explicit opt-out.
        ({"mode": "monitor", "mcp_usage_metadata": True}, False),
        (
            {
                "mode": "monitor",
                "sessions": False,
                "mcp_usage_metadata": True,
            },
            True,
        ),
        (
            {
                "mode": "monitor",
                "sessions": True,
                "mcp_usage_metadata": True,
            },
            False,
        ),
        (
            {
                "mode": "protect",
                "sessions": False,
                "mcp_usage_metadata": True,
            },
            False,
        ),
    ],
)
def test_resolve_mcp_usage_metadata_only(managed, expected):
    assert mdm_config.resolve_mcp_usage_metadata_only(managed) is expected


# ── resolve_enforcement (Enforce feature check-in gate) ────────────────


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, False),  # enforcement absent ⇒ monitor (false)
        ({"enforcement": True}, True),
        ({"enforcement": False}, False),
        ({"enforcement": True, "sessions": True}, True),
        # Monitoring-only fleet: sessions on, enforcement off ⇒ Enforce off.
        ({"enforcement": False, "sessions": True}, False),
        ({"sessions": True}, False),  # enforcement absent ⇒ false
    ],
)
def test_resolve_enforcement(managed, expected):
    assert mdm_config.resolve_enforcement(managed) is expected


def test_resolve_enforcement_reads_managed_when_none():
    with patch(
        "runlayer_cli.mdm_config.read_managed_config",
        return_value={"enforcement": True},
    ):
        assert mdm_config.resolve_enforcement() is True
