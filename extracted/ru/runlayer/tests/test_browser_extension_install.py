"""Tests for the Chrome-side browser-extension install (hook_install.browser_extension)."""

from __future__ import annotations

import json
import plistlib

import pytest

from runlayer_cli.hook_install import browser_extension as bx
from runlayer_cli.hook_install import browser_policy as browser_policy
from runlayer_cli.mdm_config import AIWatchMode, ManagedConfig

EXT_ID = "a" * 32
UPDATE_URL = "https://downloads.runlayer.com/extension/update_manifest.xml"
TARGETED_UPDATE_URL = (
    "https://tenant.runlayer.com/api/v1/binary-packages/"
    "browser-extension/chrome/signed-token/update.xml"
)
CUSTOM_HOST_TARGETED_UPDATE_URL = (
    "https://ai.example.customer/api/v1/binary-packages/"
    "browser-extension/chrome/signed-token/update.xml"
)
LEGACY_UPDATE_URL = "https://extensions.runlayer.example/aiwatch/update.xml"

BASE_MANAGED: ManagedConfig = {
    "host": "https://tenant.runlayer.com",
    "org_api_key": "rl_org_secret",
    "browser_extension_id": EXT_ID,
    "browser_extension_update_url": UPDATE_URL,
}


@pytest.fixture(autouse=True)
def _darwin(monkeypatch):
    monkeypatch.setattr(bx.platform, "system", lambda: "Darwin")


def _install(managed: ManagedConfig, tmp_path):
    return bx.install_browser_extension(
        managed,
        managed_prefs_dir=tmp_path / "managed",
        external_dir=tmp_path / "external",
    )


def _capture_policy_refresh(monkeypatch, tmp_path, *, username="alice"):
    commands: list[list[str]] = []
    console_home = tmp_path / "Users" / username if username else None
    monkeypatch.setattr(bx, "CHROME_MANAGED_PREFS_DIR", tmp_path / "managed")
    monkeypatch.setattr(browser_policy, "find_console_user_home", lambda: console_home)
    monkeypatch.setattr(
        browser_policy.subprocess,
        "run",
        lambda command, **_kwargs: commands.append(command),
    )
    return commands


def _seed_stale_runlayer_artifacts(tmp_path, update_url=UPDATE_URL):
    managed_dir = tmp_path / "managed"
    external_dir = tmp_path / "external"
    managed_dir.mkdir()
    external_dir.mkdir()

    other_id = "b" * 32
    other_url = "https://extensions.example.com/other/update.xml"
    chrome_policy_path = bx.chrome_policy_plist_path(managed_dir)
    with chrome_policy_path.open("wb") as f:
        plistlib.dump(
            {
                "HomepageLocation": "https://example.com",
                bx.EXTENSION_INSTALL_FORCELIST_KEY: [
                    f"{EXT_ID};{update_url}",
                    f"{other_id};{other_url}",
                ],
            },
            f,
        )

    extension_policy_path = bx.policy_plist_path(EXT_ID, managed_dir)
    with extension_policy_path.open("wb") as f:
        plistlib.dump(
            {
                "Host": "https://tenant.runlayer.com",
                "OrgApiKey": "rl_org_secret",
                "Enforcement": True,
            },
            f,
        )

    install_path = bx.external_install_path(EXT_ID, external_dir)
    install_path.write_text(json.dumps({"external_update_url": update_url}) + "\n")
    other_install_path = bx.external_install_path(other_id, external_dir)
    other_install_path.write_text(json.dumps({"external_update_url": other_url}) + "\n")
    return chrome_policy_path, extension_policy_path, install_path, other_install_path


def test_skips_without_extension_id(tmp_path):
    managed: ManagedConfig = {"host": "https://h", "org_api_key": "k"}
    result = _install(managed, tmp_path)
    assert not result.written
    assert "BrowserExtensionId" in (result.skipped_reason or "")
    assert not (tmp_path / "managed").exists()


def test_recognizes_current_and_legacy_runlayer_update_urls():
    assert bx._is_runlayer_update_url(UPDATE_URL)
    assert bx._is_runlayer_update_url(TARGETED_UPDATE_URL)
    assert bx._is_runlayer_update_url(
        CUSTOM_HOST_TARGETED_UPDATE_URL,
        managed_host="https://ai.example.customer",
    )
    assert not bx._is_runlayer_update_url(CUSTOM_HOST_TARGETED_UPDATE_URL)
    assert bx._is_runlayer_update_url(LEGACY_UPDATE_URL)
    assert not bx._is_runlayer_update_url(
        "http://downloads.runlayer.com/extension/update_manifest.xml"
    )
    assert not bx._is_runlayer_update_url(
        "https://tenant.runlayer.com/api/v1/binary-packages/"
        "browser-extension/chrome/signed-token/not-update.xml"
    )
    assert not bx._is_runlayer_update_url(
        "https://downloads.runlayer.com/cli/manifest.json"
    )
    assert not bx._is_runlayer_update_url(
        "https://extensions.example.com/extension/update_manifest.xml"
    )


def test_default_policy_enables_browser_surface_compatibility_wires() -> None:
    policy = browser_policy.expected_policy(BASE_MANAGED)

    assert policy["BrowserSurfaceExplorationEnabled"] is True
    assert policy["BrowserSurfaceCandidateTelemetryEnabled"] is True


def test_removes_stale_runlayer_artifacts_without_extension_id(tmp_path):
    chrome_policy_path, extension_policy_path, install_path, other_install_path = (
        _seed_stale_runlayer_artifacts(tmp_path)
    )

    result = _install({"host": "https://h", "org_api_key": "k"}, tmp_path)

    assert result.written
    assert result.force_policy_path == chrome_policy_path
    with chrome_policy_path.open("rb") as f:
        chrome_policy = plistlib.load(f)
    assert chrome_policy == {
        "HomepageLocation": "https://example.com",
        bx.EXTENSION_INSTALL_FORCELIST_KEY: [
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;https://extensions.example.com/other/update.xml",
        ],
    }
    assert not extension_policy_path.exists()
    assert not install_path.exists()
    assert other_install_path.exists()


def test_removes_targeted_artifacts_on_custom_host_without_extension_id(tmp_path):
    chrome_policy_path, extension_policy_path, install_path, _ = (
        _seed_stale_runlayer_artifacts(tmp_path, CUSTOM_HOST_TARGETED_UPDATE_URL)
    )

    result = _install(
        {"host": "https://ai.example.customer", "org_api_key": "k"}, tmp_path
    )

    assert result.written
    with chrome_policy_path.open("rb") as f:
        chrome_policy = plistlib.load(f)
    assert chrome_policy[bx.EXTENSION_INSTALL_FORCELIST_KEY] == [
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;"
        "https://extensions.example.com/other/update.xml"
    ]
    assert not extension_policy_path.exists()
    assert not install_path.exists()


@pytest.mark.parametrize(
    ("managed", "message"),
    [
        ({**BASE_MANAGED, "browser_extension_id": "not-an-id"}, "invalid"),
        (
            {
                "host": "https://tenant.runlayer.com",
                "org_api_key": "rl_org_secret",
                "browser_extension_id": EXT_ID,
            },
            "BrowserExtensionUpdateUrl",
        ),
        (
            {
                **BASE_MANAGED,
                "browser_extension_update_url": "http://insecure.example/update.xml",
            },
            "invalid BrowserExtensionUpdateUrl",
        ),
        (
            {
                "browser_extension_id": EXT_ID,
                "browser_extension_update_url": UPDATE_URL,
                "host": "https://h",
            },
            "OrgApiKey",
        ),
    ],
)
def test_fails_invalid_managed_config(tmp_path, managed, message):
    with pytest.raises(bx.BrowserExtensionMisconfiguration, match=message):
        _install(managed, tmp_path)


def test_skips_on_non_darwin(tmp_path, monkeypatch):
    monkeypatch.setattr(bx.platform, "system", lambda: "Windows")
    result = _install(BASE_MANAGED, tmp_path)
    assert not result.written
    assert "macOS" in (result.skipped_reason or "")


def test_writes_policy_plist_and_install_entry(tmp_path):
    managed: ManagedConfig = {
        **BASE_MANAGED,
        "username": "alice@company.com",
        "device_name": "Alice Mac",
        "mode": AIWatchMode.MONITOR,
        "sessions": True,
        "browser_mode": AIWatchMode.PROTECT,
        "browser_sessions": False,
        "enforcement": False,
    }
    result = _install(managed, tmp_path)
    assert result.written

    assert result.policy_path is not None
    assert result.policy_path.name == f"com.google.Chrome.extensions.{EXT_ID}.plist"
    with result.policy_path.open("rb") as f:
        policy = plistlib.load(f)
    assert policy == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "Enforcement": True,
        "Mode": "protect",
        "Sessions": False,
        "BrowserSurfaceExplorationEnabled": True,
        "BrowserSurfaceCandidateTelemetryEnabled": True,
    }

    assert result.install_path is not None
    entry = json.loads(result.install_path.read_text())
    assert entry == {"external_update_url": UPDATE_URL}

    assert result.force_policy_path is not None
    with result.force_policy_path.open("rb") as f:
        chrome_policy = plistlib.load(f)
    assert chrome_policy["ExtensionInstallForcelist"] == [f"{EXT_ID};{UPDATE_URL}"]


def test_install_survives_managed_preferences_rebuild(tmp_path, monkeypatch):
    managed_dir = tmp_path / "managed"
    _capture_policy_refresh(monkeypatch, tmp_path)

    def rebuild_managed_preferences(*_args, **_kwargs):
        for policy_path in managed_dir.glob("com.google.Chrome*.plist"):
            policy_path.unlink()

    monkeypatch.setattr(
        browser_policy.subprocess,
        "run",
        rebuild_managed_preferences,
    )

    _install(BASE_MANAGED, tmp_path)

    ok, detail = _check(BASE_MANAGED, tmp_path)
    assert ok, detail


def test_removed_policy_refreshes_managed_preferences_for_console_user(
    tmp_path, monkeypatch
):
    _seed_stale_runlayer_artifacts(tmp_path)
    commands = _capture_policy_refresh(monkeypatch, tmp_path)

    result = _install({"host": "https://h", "org_api_key": "k"}, tmp_path)

    assert result.written
    assert commands == [["/usr/bin/mcxrefresh", "-n", "alice"]]


def test_preserves_existing_chrome_policy(tmp_path):
    managed_dir = tmp_path / "managed"
    managed_dir.mkdir()
    existing_id = "b" * 32
    chrome_policy_path = managed_dir / "com.google.Chrome.plist"
    with chrome_policy_path.open("wb") as f:
        plistlib.dump(
            {
                "HomepageLocation": "https://example.com",
                "ExtensionInstallForcelist": [
                    f"{existing_id};{UPDATE_URL}",
                ],
            },
            f,
        )

    result = _install(BASE_MANAGED, tmp_path)
    assert result.written

    with chrome_policy_path.open("rb") as f:
        chrome_policy = plistlib.load(f)
    assert chrome_policy["HomepageLocation"] == "https://example.com"
    assert chrome_policy["ExtensionInstallForcelist"] == [
        f"{existing_id};{UPDATE_URL}",
        f"{EXT_ID};{UPDATE_URL}",
    ]


def _check(managed: ManagedConfig, tmp_path):
    return bx.check_browser_extension(
        managed,
        managed_prefs_dir=tmp_path / "managed",
        external_dir=tmp_path / "external",
    )


def test_check_drifts_on_stale_runlayer_artifacts_without_extension_id(tmp_path):
    _seed_stale_runlayer_artifacts(tmp_path)

    ok, detail = _check({"host": "https://h", "org_api_key": "k"}, tmp_path)

    assert not ok
    assert "stale force-install policy" in (detail or "")
    assert "stale auto-install entry" in (detail or "")
    assert "stale extension policy" in (detail or "")


def test_check_drifts_on_invalid_extension_id(tmp_path):
    managed: ManagedConfig = {**BASE_MANAGED, "browser_extension_id": "not-an-id"}
    ok, detail = _check(managed, tmp_path)
    assert not ok
    assert "invalid BrowserExtensionId" in (detail or "")


def test_check_ok_after_install(tmp_path):
    _install(BASE_MANAGED, tmp_path)
    ok, detail = _check(BASE_MANAGED, tmp_path)
    assert ok, detail


def test_check_drifts_when_browser_surface_exploration_policy_stale(tmp_path):
    managed = BASE_MANAGED
    result = _install(managed, tmp_path)
    assert result.policy_path is not None
    with result.policy_path.open("rb") as f:
        policy = plistlib.load(f)
    policy["BrowserSurfaceExplorationEnabled"] = False
    with result.policy_path.open("wb") as f:
        plistlib.dump(policy, f)

    ok, detail = _check(managed, tmp_path)
    assert not ok
    assert "policy" in (detail or "")


def test_check_drifts_when_browser_surface_candidate_telemetry_policy_stale(tmp_path):
    managed = BASE_MANAGED
    result = _install(managed, tmp_path)
    assert result.policy_path is not None
    with result.policy_path.open("rb") as f:
        policy = plistlib.load(f)
    policy["BrowserSurfaceCandidateTelemetryEnabled"] = False
    with result.policy_path.open("wb") as f:
        plistlib.dump(policy, f)

    ok, detail = _check(managed, tmp_path)
    assert not ok
    assert "policy" in (detail or "")


def test_check_drifts_when_force_policy_missing(tmp_path):
    result = _install(BASE_MANAGED, tmp_path)
    assert result.force_policy_path is not None
    with result.force_policy_path.open("wb") as f:
        plistlib.dump({"ExtensionInstallForcelist": []}, f)

    ok, detail = _check(BASE_MANAGED, tmp_path)
    assert not ok
    assert "force-install policy" in (detail or "")


def test_check_drifts_when_auto_install_entry_stale(tmp_path):
    result = _install(BASE_MANAGED, tmp_path)
    assert result.install_path is not None
    result.install_path.write_text(
        json.dumps({"external_update_url": "https://old.example/update.xml"}) + "\n"
    )

    ok, detail = _check(BASE_MANAGED, tmp_path)
    assert not ok
    assert "auto-install entry" in (detail or "")


def test_check_drifts_on_stale_policy_or_missing_entry(tmp_path):
    ok, detail = _check(BASE_MANAGED, tmp_path)
    assert not ok
    assert (
        "policy" in (detail or "")
        and "force-install" in (detail or "")
        and "auto-install" in (detail or "")
    )

    result = _install(BASE_MANAGED, tmp_path)
    stale: ManagedConfig = {**BASE_MANAGED, "org_api_key": "rl_org_rotated"}
    ok, detail = _check(stale, tmp_path)
    assert not ok
    assert "policy" in (detail or "")

    _install(stale, tmp_path)
    result.install_path.unlink()  # type: ignore[union-attr]
    ok, detail = _check(stale, tmp_path)
    assert not ok
    assert "auto-install" in (detail or "")
