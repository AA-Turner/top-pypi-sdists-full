"""Browser policy files alone do not establish extension installation."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from runlayer_cli.hook_install import browser_extension as chrome
from runlayer_cli.hook_install import console_user
from runlayer_cli.hook_install import chromium_profile_health as health
from runlayer_cli.hook_install import edge_extension as edge
from runlayer_cli.mdm_config import ManagedConfig

EXTENSION_ID = chrome.RUNLAYER_CHROME_EXTENSION_ID
MANAGED: ManagedConfig = {
    "host": "https://tenant.runlayer.com",
    "org_api_key": "rl_org_test",
    "browser_extension_enabled": True,
    "browser_extension_id": EXTENSION_ID,
    "browser_extension_update_url": chrome.RUNLAYER_CHROME_UPDATE_URL,
}
pytestmark = pytest.mark.skipif(os.name != "posix", reason="macOS profile reader")


@pytest.fixture(params=["chrome", "edge"])
def browser(tmp_path, monkeypatch, request):
    monkeypatch.setattr(chrome.platform, "system", lambda: "Darwin")
    home = tmp_path / "user"
    monkeypatch.setattr(console_user, "find_console_user_home", lambda: home)
    managed_dir = tmp_path / "managed"
    if request.param == "chrome":
        dirs = {
            "managed_prefs_dir": managed_dir,
            "external_dir": tmp_path / "external",
        }
        chrome.install_browser_extension(MANAGED, **dirs)

        def check():
            return chrome.check_browser_extension(MANAGED, **dirs)

        root = home / "Library/Application Support/Google/Chrome"
    else:
        edge.install_edge_extension(MANAGED, managed_prefs_dir=managed_dir)
        native_host = tmp_path / "native.json"
        native_host.write_text(json.dumps(edge.expected_native_host()))

        def check():
            return edge.check_edge_extension(
                MANAGED, managed_prefs_dir=managed_dir, native_host_path=native_host
            )

        root = home / "Library/Application Support/Microsoft Edge"
    return root, check


def _profile(root: Path, name: str = "Default") -> Path:
    profile = root / name
    profile.mkdir(parents=True)
    (profile / "Secure Preferences").write_text(
        json.dumps({"extensions": {"settings": {}}})
    )
    return profile


def test_matching_policy_with_missing_extension_is_not_healthy(browser):
    root, check = browser
    _profile(root)

    ok, detail = check()

    assert not ok, "Correct policy files must not hide a missing extension"
    assert "extension missing" in (detail or "")


def _installed(profile: Path, **overrides) -> None:
    relative = f"{EXTENSION_ID}/1.2.3_0"
    manifest = profile / "Extensions" / relative / "manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({"version": "1.2.3", "manifest_version": 3}))
    registration = {"disable_reasons": [], "path": relative, **overrides}
    (profile / "Secure Preferences").write_text(
        json.dumps({"extensions": {"settings": {EXTENSION_ID: registration}}})
    )


@pytest.mark.parametrize("name", ["Default", "Profile 7", "Work account"])
@pytest.mark.parametrize("filename", ["Preferences", "Secure Preferences"])
def test_registration_and_current_files_are_present(browser, name, filename):
    root, check = browser
    profile = _profile(root, name)
    (root / "Local State").write_text(
        json.dumps({"profile": {"info_cache": {name: {}}}})
    )
    _installed(profile)
    (profile / "Secure Preferences").rename(profile / filename)

    assert check() == (True, None)


def test_unused_browser_and_no_console_user_keep_policy_check(browser, monkeypatch):
    root, check = browser
    assert check() == (True, None)
    root.mkdir(parents=True)
    (root / "Local State").write_text("{}")
    assert check() == (True, None)
    _profile(root)
    monkeypatch.setattr(console_user, "find_console_user_home", lambda: None)
    assert check() == (True, None)


@pytest.mark.parametrize(
    "registration",
    [{"disable_reasons": [1]}, {"disable_reasons": 4}, {"state": 0}],
)
def test_disabled_extension_is_not_healthy(browser, registration):
    root, check = browser
    _installed(_profile(root), **registration)

    ok, detail = check()

    assert not ok
    assert "extension disabled" in detail


def test_only_old_version_files_do_not_count_as_current_install(browser):
    root, check = browser
    _installed(_profile(root), path=f"{EXTENSION_ID}/2.0.0_0")

    ok, detail = check()

    assert not ok
    assert "extension files missing" in detail


def test_missing_profile_is_not_hidden_by_healthy_profile(browser):
    root, check = browser
    _installed(_profile(root))
    _profile(root, "Profile 2")

    ok, detail = check()

    assert not ok
    assert "extension missing" in detail
    assert "Profile 2" not in detail


@pytest.mark.parametrize(
    "filename,content",
    [
        ("Secure Preferences", "{"),
        ("Secure Preferences", "[]"),
        ("Secure Preferences", '{"extensions":{"settings":[]}}'),
        ("Local State", "{"),
        ("Local State", '{"profile":{"info_cache":[]}}'),
        ("Local State", '{"profile":{"info_cache":{"../outside":{}}}}'),
    ],
)
def test_invalid_profile_state_is_not_healthy(browser, filename, content):
    root, check = browser
    profile = _profile(root)
    _installed(profile)
    destination = root if filename == "Local State" else profile
    (destination / filename).write_text(content)

    assert check() == (False, health._UNVERIFIED)


def test_unreadable_profile_state_is_not_healthy(browser, monkeypatch):
    root, check = browser
    _installed(_profile(root))
    monkeypatch.setattr(health, "safe_read_file", lambda *_args, **_kwargs: None)

    assert check() == (False, health._UNVERIFIED)


@pytest.mark.parametrize("target", ["Secure Preferences", "Extensions"])
def test_profile_symlink_is_not_followed(browser, tmp_path, target):
    root, check = browser
    profile = _profile(root)
    if target == "Secure Preferences":
        (profile / target).unlink()
    else:
        (profile / "Secure Preferences").write_text(
            json.dumps(
                {
                    "extensions": {
                        "settings": {EXTENSION_ID: {"path": f"{EXTENSION_ID}/1.2.3_0"}}
                    }
                }
            )
        )
    outside = tmp_path / "unrelated-private-data"
    outside.write_text("sensitive value")
    (profile / target).symlink_to(outside)

    ok, detail = check()

    assert not ok
    assert "sensitive" not in detail
    assert outside.name not in detail


def test_oversized_profile_state_is_not_healthy(browser, monkeypatch):
    root, check = browser
    _installed(_profile(root))
    monkeypatch.setattr(health, "_MAX_JSON_BYTES", 8)

    assert check() == (False, health._UNVERIFIED)


def test_guest_and_system_profiles_do_not_trigger_missing_extension(browser):
    root, check = browser
    _profile(root, "Guest Profile")
    _profile(root, "System Profile")

    assert check() == (True, None)


def test_other_browser_channels_are_outside_the_profile_check(browser):
    root, check = browser
    _profile(root.with_name(root.name + " Beta"))

    assert check() == (True, None)


def test_deleted_profile_in_local_state_is_not_existing_profile(browser):
    root, check = browser
    _installed(_profile(root))
    (root / "Local State").write_text(
        json.dumps({"profile": {"info_cache": {"removed account": {}}}})
    )

    assert check() == (True, None)


def test_profile_without_preferences_is_unverified(browser):
    root, check = browser
    (root / "Default").mkdir(parents=True)

    assert check() == (False, health._UNVERIFIED)


@pytest.mark.parametrize(
    "registration",
    [
        {"path": "/private/unrelated"},
        {"path": f"{EXTENSION_ID}/../../unrelated"},
        {"path": f"{'b' * 32}/1.2.3_0"},
        {"path": None},
        {"state": None},
        {"disable_reasons": "invalid"},
    ],
)
def test_invalid_registration_is_unverified(browser, registration):
    root, check = browser
    _installed(_profile(root), **registration)

    assert check() == (False, health._UNVERIFIED)


@pytest.mark.parametrize("limit", ["_MAX_DIRECTORY_ENTRIES", "_MAX_PROFILES"])
def test_profile_discovery_is_bounded(browser, monkeypatch, limit):
    root, check = browser
    _installed(_profile(root))
    _installed(_profile(root, "Profile 2"))
    monkeypatch.setattr(health, limit, 1)

    assert check() == (False, health._UNVERIFIED)
