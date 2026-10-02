"""DRIVER-mode navigate verb: app switch / BACK / deeplink dispatch."""
import logging

import pytest

from testmu_appium import _config, _vars
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers.navigate import navigate


class _FakeDriver:
    def __init__(self):
        self.activated = []
        self.pressed = []
        self.scripts = []

    def activate_app(self, app_id):
        self.activated.append(app_id)

    def press_keycode(self, code):
        self.pressed.append(code)

    def execute_script(self, script, payload):
        self.scripts.append((script, payload))


@pytest.fixture(autouse=True)
def _clear_vars():
    yield
    _vars.clear_state()


def test_app_scheme_activates_the_named_app(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    navigate(driver, "app://com.google.android.gm")
    assert driver.activated == ["com.google.android.gm"]


def test_app_scheme_with_no_id_falls_back_to_configured_app_id(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "app_id", "com.example.fallback")
    driver = _FakeDriver()
    navigate(driver, "app://")
    assert driver.activated == ["com.example.fallback"]


def test_app_scheme_with_no_id_and_no_fallback_raises(monkeypatch):
    monkeypatch.setitem(_config._config, "app_id", "")
    driver = _FakeDriver()
    with pytest.raises(ValueError):
        navigate(driver, "app://")
    assert driver.activated == []


@pytest.mark.parametrize("value", ["back", "BACK", "Back"])
def test_back_is_case_insensitive_and_routes_through_keyevent(monkeypatch, value):
    monkeypatch.setitem(_config._config, "platform", "android")
    driver = _FakeDriver()
    navigate(driver, value)
    assert driver.pressed == [4]
    assert driver.activated == []
    assert driver.scripts == []


def test_anything_else_is_a_deeplink_on_android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "app_id", "com.google.android.gm")
    driver = _FakeDriver()
    navigate(driver, "myapp://checkout/123")
    assert driver.scripts == [
        ("mobile: deepLink", {"url": "myapp://checkout/123", "package": "com.google.android.gm"})
    ]


def test_deeplink_names_the_app_the_way_ios_does(monkeypatch):
    """The whole platform difference for this route is one key name."""
    monkeypatch.setitem(_config._config, "platform", "ios")
    monkeypatch.setitem(_config._config, "app_id", "com.example.app")
    driver = _FakeDriver()
    navigate(driver, "myapp://checkout/123")
    assert driver.scripts == [
        ("mobile: deepLink",
         {"url": "myapp://checkout/123", "bundleId": "com.example.app"}),
    ]


@pytest.mark.parametrize("platform", ["android", "ios"])
def test_deeplink_with_no_app_omits_the_key_rather_than_sending_it_empty(
    monkeypatch, platform,
):
    """Absent means "the OS resolves the scheme"; empty means "an app called ''".

    Only Android reads the two as the same thing. iOS forwards the value to
    WebDriverAgent, which looks up an app by that name and fails the whole
    deeplink when it is empty.
    """
    monkeypatch.setitem(_config._config, "platform", platform)
    monkeypatch.setitem(_config._config, "app_id", "")
    driver = _FakeDriver()
    navigate(driver, "myapp://checkout/123")
    assert driver.scripts == [
        ("mobile: deepLink", {"url": "myapp://checkout/123"}),
    ]


def test_deeplink_raises_on_an_unshipped_platform(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "tizen")
    driver = _FakeDriver()
    with pytest.raises(UnsupportedOnPlatform) as exc:
        navigate(driver, "myapp://checkout/123")
    assert "tizen" in str(exc.value)
    assert driver.scripts == []


def test_url_resolves_var_templates_before_dispatch(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "app_id", "com.example")
    _vars.set_var("target_app", "app://com.other.app")
    driver = _FakeDriver()
    navigate(driver, "{{target_app}}")
    assert driver.activated == ["com.other.app"]


def test_navigate_logs_at_info(monkeypatch, caplog):
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "app_id", "com.example")
    caplog.set_level(logging.INFO, logger="testmu_appium")
    navigate(_FakeDriver(), "app://com.example", description="open the app")
    assert "com.example" in caplog.text
    assert "open the app" in caplog.text
