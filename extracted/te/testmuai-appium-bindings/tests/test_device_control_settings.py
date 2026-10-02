"""Fake-driver coverage for the v1 device-control settings catalogue."""
from __future__ import annotations

import pytest

from testmu_appium import _config
from testmu_appium._helpers.device_control import KINDS, device_control


class _FakeDriver:
    def __init__(self, responses=None, failures=None):
        self.responses = responses or {}
        self.failures = failures or set()
        self.scripts = []
        self.keycodes = []

    def execute_script(self, script, arguments):
        call = (script, arguments)
        self.scripts.append(call)
        command = arguments.get("command", script)
        args = tuple(arguments.get("args", ()))
        if (command, args) in self.failures:
            raise RuntimeError("adb_shell is not allowed")
        return self.responses.get((command, args))

    def press_keycode(self, keycode):
        self.keycodes.append(keycode)


@pytest.mark.parametrize(
    ("kind", "value", "expected"),
    [
        ("wifi", "on", ("mobile: setConnectivity", {"wifi": True})),
        ("flight_mode", "off", ("mobile: setConnectivity", {"airplaneMode": False})),
        ("mobile_data", "on", ("mobile: setConnectivity", {"data": True})),
        (
            "bluetooth",
            "on",
            ("mobile: shell", {"command": "svc", "args": ["bluetooth", "enable"]}),
        ),
        (
            "location",
            "off",
            ("mobile: shell", {"command": "cmd", "args": ["location", "set-location-enabled", "false"]}),
        ),
        (
            "dark_mode",
            "on",
            ("mobile: shell", {"command": "cmd", "args": ["uimode", "night", "yes"]}),
        ),
        (
            "dnd",
            "on",
            ("mobile: shell", {"command": "cmd", "args": ["notification", "set_dnd", "on"]}),
        ),
    ],
)
def test_android_setting_setters_map_canonical_values_to_driver_calls(
    monkeypatch, kind, value, expected
):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()

    device_control(driver, kind, value=value)

    assert driver.scripts == [expected]


def test_bluetooth_falls_back_to_bluetooth_manager_when_svc_is_api_gated(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver(failures={("svc", ("bluetooth", "enable"))})

    device_control(driver, "bluetooth", value="on")

    assert driver.scripts == [
        ("mobile: shell", {"command": "svc", "args": ["bluetooth", "enable"]}),
        ("mobile: shell", {"command": "cmd", "args": ["bluetooth_manager", "enable"]}),
    ]


def test_shell_capability_error_names_the_required_appium_capability(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver(failures={("cmd", ("location", "set-location-enabled", "true"))})

    with pytest.raises(RuntimeError, match=r"location requires .*adb_shell.*--allow-insecure=adb_shell"):
        device_control(driver, "location", value="on")


def test_brightness_disables_auto_mode_and_maps_percent_to_system_level(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()

    device_control(driver, "brightness", value="42")

    assert driver.scripts == [
        ("mobile: shell", {"command": "settings", "args": ["put", "system", "screen_brightness_mode", "0"]}),
        ("mobile: shell", {"command": "settings", "args": ["put", "system", "screen_brightness", "107"]}),
    ]


def test_android_volume_uses_keycodes_for_relative_values(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()

    device_control(driver, "volume", value="down")

    assert driver.keycodes == [25]


def test_android_volume_maps_percent_to_media_session_level(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver(
        responses={
            (
                "cmd",
                ("media_session", "volume", "--stream", "3", "--get"),
            ): "[V] will get volume\n[V] Connecting to AudioService\n"
            "[V] volume is 17 in range [0..25]"
        }
    )

    device_control(driver, "volume", value="40")

    assert driver.scripts == [
        (
            "mobile: shell",
            {
                "command": "cmd",
                "args": ["media_session", "volume", "--stream", "3", "--get"],
            },
        ),
        (
            "mobile: shell",
            {
                "command": "cmd",
                "args": [
                    "media_session",
                    "volume",
                    "--stream",
                    "3",
                    "--set",
                    "10",
                ],
            },
        ),
    ]


@pytest.mark.parametrize(
    ("kind", "response", "expected"),
    [
        ("wifi", {"wifi": True}, "on"),
        ("flight_mode", {"airplaneMode": False}, "off"),
        ("mobile_data", {"data": True}, "on"),
        ("bluetooth", "1", "on"),
        ("location", "true", "on"),
        ("dark_mode", "Night mode: yes", "on"),
        ("brightness", "107", "42"),
        ("dnd", "2", "on"),
        (
            "volume",
            (
                "[V] will get volume\n[V] Connecting to AudioService\n"
                "[V] volume is 17 in range [0..25]"
            ),
            "68",
        ),
    ],
)
def test_android_setting_getters_return_canonical_values(kind, response, expected):
    ops = KINDS[kind].platforms["android"]
    assert ops.getter is not None
    assert ops.value_domain is not None
    driver = _FakeDriver(responses=_getter_responses(kind, response))

    actual = ops.getter(driver)
    assert actual == expected
    assert ops.value_domain.contains(actual)


def _getter_responses(kind, response):
    commands = {
        "wifi": ("mobile: getConnectivity", (), response),
        "flight_mode": ("mobile: getConnectivity", (), response),
        "mobile_data": ("mobile: getConnectivity", (), response),
        "bluetooth": ("settings", ("get", "global", "bluetooth_on"), response),
        "location": ("cmd", ("location", "is-location-enabled"), response),
        "dark_mode": ("cmd", ("uimode", "night"), response),
        "brightness": ("settings", ("get", "system", "screen_brightness"), response),
        "dnd": ("settings", ("get", "global", "zen_mode"), response),
        "volume": (
            "cmd",
            ("media_session", "volume", "--stream", "3", "--get"),
            response,
        ),
    }
    command, args, result = commands[kind]
    return {(command, args): result}


def test_ios_only_exposes_the_supported_contract(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()

    device_control(driver, "dark_mode", value="off")
    device_control(driver, "volume", value="up")

    assert driver.scripts == [
        ("mobile: setAppearance", {"style": "light"}),
        ("mobile: pressButton", {"name": "volumeUp"}),
    ]


def test_ios_dark_mode_getter_returns_the_binary_canonical_value():
    ops = KINDS["dark_mode"].platforms["ios"]
    assert ops.getter is not None
    assert ops.value_domain is not None
    driver = _FakeDriver(responses={("mobile: getAppearance", ()): {"style": "dark"}})

    actual = ops.getter(driver)

    assert actual == "on"
    assert ops.value_domain.contains(actual)


def test_ios_dark_mode_getter_reports_off_for_a_light_style_response():
    ops = KINDS["dark_mode"].platforms["ios"]
    driver = _FakeDriver(responses={("mobile: getAppearance", ()): {"style": "light"}})

    assert ops.getter(driver) == "off"


def test_ios_volume_up_down_refused_on_a_simulator(monkeypatch):
    # mobile: pressButton volumeUp/volumeDown is documented real-device-only for
    # XCUITest; a simulator target must fail up front, never reaching the driver.
    monkeypatch.setitem(_config._config, "platform", "ios")
    monkeypatch.setitem(_config._config, "target_kind", "simulator")
    driver = _FakeDriver()

    with pytest.raises(Exception) as excinfo:
        device_control(driver, "volume", value="up")

    message = str(excinfo.value).lower()
    assert "simulator" in message or "real device" in message
    assert driver.scripts == []


def test_ios_volume_up_down_dispatches_on_a_real_device(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")
    monkeypatch.setitem(_config._config, "target_kind", "physical")
    driver = _FakeDriver()

    device_control(driver, "volume", value="down")

    assert driver.scripts == [("mobile: pressButton", {"name": "volumeDown"})]
