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
    """Absent Sessions key means callers default to True themselves."""
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


# ── resolve_install_hooks (Enforcement/Sessions install gate) ──────────


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({}, True),  # enforcement absent ⇒ false, sessions absent ⇒ true
        ({"enforcement": True, "sessions": True}, True),
        ({"enforcement": True, "sessions": False}, True),  # enforcement-only
        ({"enforcement": False, "sessions": True}, True),  # event/session only
        ({"enforcement": False, "sessions": False}, False),  # scan-only no-op
        ({"enforcement": True}, True),  # sessions absent ⇒ true (full set)
        ({"enforcement": False}, True),  # sessions absent ⇒ true (full set)
        ({"sessions": False}, False),  # enforcement absent ⇒ false ⇒ scan-only
        ({"sessions": True}, True),  # enforcement absent ⇒ false, sessions on
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
