"""DRIVER-mode device_control verb: orientation / hide_keyboard / notification.
"""
import logging

import pytest

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers.device_control import device_control


class _FakeDriver:
    orientation = None

    def __init__(self):
        self.hid_keyboard_calls = 0
        self.opened_notifications = 0
        self.pressed = []

    def hide_keyboard(self):
        self.hid_keyboard_calls += 1

    def open_notifications(self):
        self.opened_notifications += 1

    def press_keycode(self, code):
        self.pressed.append(code)


@pytest.mark.parametrize("value,expected", [("portrait", "PORTRAIT"), ("LANDSCAPE", "LANDSCAPE"),
                                             ("Landscape", "LANDSCAPE")])
def test_orientation_sets_the_uppercase_form(value, expected):
    driver = _FakeDriver()
    device_control(driver, "orientation", value=value)
    assert driver.orientation == expected


def test_orientation_rejects_an_invalid_value():
    driver = _FakeDriver()
    with pytest.raises(ValueError) as exc:
        device_control(driver, "orientation", value="sideways")
    assert "sideways" in str(exc.value)


def test_hide_keyboard_on_android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    device_control(driver, "hide_keyboard")
    assert driver.hid_keyboard_calls == 1


def test_hide_keyboard_refuses_on_ios(monkeypatch):
    """The shared driver row taps a key named "done" and returns true
    unconditionally — on any field that keeps focus through its action key
    that is a verb that does nothing and claims success. Refusing loudly is
    strictly more useful: the agent can see the keyboard and tap outside it.
    A verified implementation lives at b73806a..c818598 pending device
    validation."""
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()
    with pytest.raises(UnsupportedOnPlatform):
        device_control(driver, "hide_keyboard")
    assert driver.hid_keyboard_calls == 0


def test_notification_is_refused_on_ios(monkeypatch):
    """XCUITest exposes no open_notifications, and dismissing the panel relies on
    BACK, which iOS does not have. Notification Centre is reachable there only as
    an edge swipe — a gesture the agent can already perform — so this refuses
    rather than half-implementing one direction of it.
    """
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()
    with pytest.raises(UnsupportedOnPlatform) as exc:
        device_control(driver, "notification", value="show")
    assert "ios" in str(exc.value)


def test_notification_show_opens_notifications_on_android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    device_control(driver, "notification", value="show")
    assert driver.opened_notifications == 1


def test_notification_hide_presses_back_on_android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    device_control(driver, "notification", value="hide")
    assert driver.pressed == [4]


def test_notification_raises_unsupported_on_ios(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()
    with pytest.raises(UnsupportedOnPlatform) as exc:
        device_control(driver, "notification", value="show")
    assert "ios" in str(exc.value)


def test_notification_rejects_an_unknown_value(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    with pytest.raises(ValueError) as exc:
        device_control(driver, "notification", value="toggle")
    assert "toggle" in str(exc.value)


def test_unknown_kind_raises_value_error_naming_the_known_set():
    driver = _FakeDriver()
    with pytest.raises(ValueError) as exc:
        device_control(driver, "not_a_setting", value="50")
    assert "not_a_setting" in str(exc.value)
    for kind in (
        "orientation",
        "wifi",
        "flight_mode",
        "mobile_data",
        "bluetooth",
        "location",
        "dark_mode",
        "brightness",
        "dnd",
        "volume",
        "hide_keyboard",
        "notification",
    ):
        assert kind in str(exc.value)


def test_device_control_logs_at_info(caplog):
    caplog.set_level(logging.INFO, logger="testmu_appium")
    device_control(_FakeDriver(), "orientation", value="landscape", description="rotate device")
    assert "LANDSCAPE" in caplog.text
    assert "rotate device" in caplog.text
