"""DRIVER-mode app_lifecycle verb: terminate / background."""
import logging

import pytest

from testmu_appium import _config
from testmu_appium._helpers.app_lifecycle import app_lifecycle


class _FakeDriver:
    def __init__(self):
        self.terminated = []
        self.backgrounded = []

    def terminate_app(self, app_id):
        self.terminated.append(app_id)

    def background_app(self, seconds):
        self.backgrounded.append(seconds)


def test_terminate_uses_the_given_app_id():
    driver = _FakeDriver()
    app_lifecycle(driver, "terminate", app_id="com.google.android.gm")
    assert driver.terminated == ["com.google.android.gm"]


def test_terminate_falls_back_to_the_configured_app_id(monkeypatch):
    monkeypatch.setitem(_config._config, "app_id", "com.example.configured")
    driver = _FakeDriver()
    app_lifecycle(driver, "terminate")
    assert driver.terminated == ["com.example.configured"]


@pytest.mark.parametrize(
    "duration_ms,expected_seconds",
    [
        (500, 1),      # rounds up, minimum 1
        (1000, 1),
        (1001, 2),
        (2500, 3),
        (0, 1),
    ],
)
def test_background_converts_duration_ms_to_seconds(duration_ms, expected_seconds):
    driver = _FakeDriver()
    app_lifecycle(driver, "background", duration_ms=duration_ms)
    assert driver.backgrounded == [expected_seconds]


def test_background_with_no_duration_is_indefinite():
    driver = _FakeDriver()
    app_lifecycle(driver, "background")
    assert driver.backgrounded == [-1]


def test_unknown_kind_raises_value_error_naming_the_known_set():
    driver = _FakeDriver()
    with pytest.raises(ValueError) as exc:
        app_lifecycle(driver, "restart")
    assert "restart" in str(exc.value)
    assert "terminate" in str(exc.value)
    assert "background" in str(exc.value)


def test_app_lifecycle_logs_at_info(caplog):
    caplog.set_level(logging.INFO, logger="testmu_appium")
    app_lifecycle(_FakeDriver(), "terminate", app_id="com.example", description="close the app")
    assert "com.example" in caplog.text
    assert "close the app" in caplog.text


class TestTerminateNeedsAnAppId:
    """terminate_app("") is not a no-op — it is a driver call with an empty bundle,
    whose behaviour is the server's to decide, so the verb refuses instead."""

    def test_no_app_id_anywhere_raises(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "")
        driver = _FakeDriver()
        with pytest.raises(ValueError) as exc:
            app_lifecycle(driver, "terminate")
        assert "app id" in str(exc.value)
        assert driver.terminated == []

    def test_an_explicit_app_id_is_enough(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "")
        driver = _FakeDriver()
        app_lifecycle(driver, "terminate", app_id="com.example.app")
        assert driver.terminated == ["com.example.app"]

    def test_the_configured_app_id_is_enough(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "com.configured.app")
        driver = _FakeDriver()
        app_lifecycle(driver, "terminate")
        assert driver.terminated == ["com.configured.app"]

    def test_an_explicit_app_id_wins_over_the_configured_one(self, monkeypatch):
        monkeypatch.setitem(_config._config, "app_id", "com.configured.app")
        driver = _FakeDriver()
        app_lifecycle(driver, "terminate", app_id="com.explicit.app")
        assert driver.terminated == ["com.explicit.app"]

    def test_background_is_unaffected(self, monkeypatch):
        """background_app takes no app id, so it has no such gap."""
        monkeypatch.setitem(_config._config, "app_id", "")
        driver = _FakeDriver()
        app_lifecycle(driver, "background", duration_ms=1000)
        assert driver.backgrounded == [1]
