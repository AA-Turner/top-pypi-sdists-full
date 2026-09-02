"""Static contracts for shipped AI Watch tenant configuration artifacts."""

from __future__ import annotations

import json
import plistlib
from pathlib import Path

import pytest

_MACOS_PACKAGING = Path(__file__).parent.parent / "packaging" / "macos"
_JAMF_SCHEMA = _MACOS_PACKAGING / "com.runlayer.aiwatch.jamf.schema.json"
_LINUX_CONFIG = (
    Path(__file__).parent.parent / "packaging" / "linux" / "aiwatch-config.json"
)
_CONFIG_PROFILES = (
    _MACOS_PACKAGING / "com.runlayer.aiwatch.mobileconfig",
    _MACOS_PACKAGING / "com.runlayer.aiwatch.ws1.mobileconfig",
)

# The deployed profile is bootstrap-only: Host + OrgApiKey. Everything else
# (mode, sessions, detection, scan tuning) is backend-managed and delivered by
# the settings sync, so it must never re-enter the shipped MDM artifacts.
_BOOTSTRAP_KEYS = {"Host", "OrgApiKey"}


@pytest.mark.parametrize("profile_path", _CONFIG_PROFILES, ids=lambda path: path.name)
def test_payload_versions_use_apple_required_value(profile_path: Path) -> None:
    with profile_path.open("rb") as profile_file:
        profile = plistlib.load(profile_file)

    assert profile["PayloadVersion"] == 1
    assert all(payload["PayloadVersion"] == 1 for payload in profile["PayloadContent"])


@pytest.mark.parametrize("profile_path", _CONFIG_PROFILES, ids=lambda path: path.name)
def test_profiles_ship_bootstrap_settings_only(profile_path: Path) -> None:
    with profile_path.open("rb") as profile_file:
        profile = plistlib.load(profile_file)

    settings = profile["PayloadContent"][0]["PayloadContent"]["com.runlayer.aiwatch"][
        "Forced"
    ][0]["mcx_preference_settings"]
    assert set(settings) == _BOOTSTRAP_KEYS


def test_jamf_schema_collects_bootstrap_settings_only() -> None:
    properties = json.loads(_JAMF_SCHEMA.read_text())["properties"]

    assert set(properties) == _BOOTSTRAP_KEYS


def test_linux_config_ships_bootstrap_host_only() -> None:
    config = json.loads(_LINUX_CONFIG.read_text())

    assert set(config) == {"Host"}
