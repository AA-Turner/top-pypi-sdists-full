"""DRIVER-mode keyevent verb: semantic key name -> platform keycode -> press_keycode."""
import logging

import pytest

from testmu_appium import _config
from testmu_appium._errors import UnknownKeyEvent
from testmu_appium._helpers.keyevent import keyevent


class _FakeDriver:
    def __init__(self):
        self.pressed = []
        self.scripts = []

    def press_keycode(self, code):
        self.pressed.append(code)

    def execute_script(self, name, args=None):
        self.scripts.append((name, args))


def test_keyevent_presses_the_resolved_keycode(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    keyevent(driver, "BACK")
    assert driver.pressed == [4]


def test_keyevent_is_case_insensitive_and_resolves_aliases(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    keyevent(driver, "go_back")
    assert driver.pressed == [4]


def test_keyevent_uses_the_configured_platform(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    keyevent(driver, "ENTER")
    assert driver.pressed == [66]


def test_unknown_key_propagates_unknown_key_event(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    with pytest.raises(UnknownKeyEvent) as exc:
        keyevent(driver, "SIRI")
    assert "SIRI" in str(exc.value)
    assert driver.pressed == []


def test_ios_presses_a_hardware_button(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()
    keyevent(driver, "HOME")
    assert driver.scripts == [("mobile: pressButton", {"name": "home"})]
    assert driver.pressed == []


def test_ios_propagates_unknown_key_for_a_key_it_has_no_equivalent_for(monkeypatch):
    """BACK reaches the verb unchanged: there is nothing to heal or retry.

    It raises UnknownKeyEvent rather than UnsupportedOnPlatform because iOS key
    events ARE shipped — this one key has no iOS counterpart, and the message
    lists what the platform does have.
    """
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _FakeDriver()
    with pytest.raises(UnknownKeyEvent):
        keyevent(driver, "BACK")
    assert driver.scripts == []
    assert driver.pressed == []


def test_keyevent_logs_at_info(monkeypatch, caplog):
    monkeypatch.setitem(_config._config, "platform", "android")
    caplog.set_level(logging.INFO, logger="testmu_appium")
    keyevent(_FakeDriver(), "BACK", description="go back to inbox")
    assert "BACK" in caplog.text
    assert "go back to inbox" in caplog.text


@pytest.mark.parametrize('key,code', [(4, 4), ('4', 4), (' 66 ', 66), (3, 3), ('24', 24), (29, 29), (0, 0), ('0', 0)])
def test_android_numeric_keycodes_dispatch_directly(monkeypatch, key, code):
    monkeypatch.setitem(_config._config, 'platform', 'android')
    driver = _FakeDriver()
    keyevent(driver, key)
    assert driver.pressed == [code]
    assert type(driver.pressed[0]) is int


@pytest.mark.parametrize('key', [True, False, -1, '-1', 4.5, '4.0', '', '٤'])
def test_android_invalid_numeric_keys_are_rejected(monkeypatch, key):
    monkeypatch.setitem(_config._config, 'platform', 'android')
    driver = _FakeDriver()
    with pytest.raises(UnknownKeyEvent):
        keyevent(driver, key)
    assert driver.pressed == []


@pytest.mark.parametrize('key', [4, '4', 0, '0'])
def test_ios_numeric_keys_remain_unsupported(monkeypatch, key):
    monkeypatch.setitem(_config._config, 'platform', 'ios')
    driver = _FakeDriver()
    with pytest.raises(UnknownKeyEvent):
        keyevent(driver, key)
    assert driver.pressed == []
    assert driver.scripts == []
