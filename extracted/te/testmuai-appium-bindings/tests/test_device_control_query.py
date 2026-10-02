"""Public query API for DRIVER-mode device-control settings."""

import pytest

from testmu_appium import _config, device_control_query
from testmu_appium._errors import UnsupportedOnPlatform


class _QueryDriver:
    orientation = "LANDSCAPE"

    def __init__(self, failure=False):
        self.failure = failure
        self.scripts = []

    def execute_script(self, script, arguments):
        self.scripts.append((script, arguments))
        if self.failure:
            raise RuntimeError("adb_shell is not allowed")
        return "true"


def test_device_control_query_returns_the_registry_canonical_value(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")

    assert device_control_query(_QueryDriver(), "orientation") == "landscape"


def test_device_control_query_refuses_a_kind_without_a_getter(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")

    with pytest.raises(UnsupportedOnPlatform, match="hide_keyboard"):
        device_control_query(_QueryDriver(), "hide_keyboard")


def test_device_control_query_names_the_shell_capability_when_the_server_denies_it(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")

    with pytest.raises(RuntimeError, match=r"location requires .*--allow-insecure=adb_shell"):
        device_control_query(_QueryDriver(failure=True), "location")
