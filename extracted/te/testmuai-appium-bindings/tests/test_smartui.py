"""DRIVER-mode smartui_screenshot verb — SDK-backed capture.

One SmartUIAppSnapshot per binding session: start() on the first capture
(token via options, buildName carried when configured), later captures reuse
the build, finalize_smartui() stops it. The verb returns a status dict —
captured / skipped (no token) / failed (SDK error) — and never raises except
for a missing SDK package.
"""
import logging
import sys
import types

import pytest

from testmu_appium import _config
from testmu_appium._helpers import smartui as smartui_mod
from testmu_appium._helpers.smartui import (
    finalize_smartui,
    smartui_build_name,
    smartui_screenshot,
)


class _FakeSnapshot:
    instances: list = []

    def __init__(self):
        self.start_calls = []
        self.snapshot_calls = []
        self.stop_count = 0
        self.build_data = types.SimpleNamespace(name="build-7", build_id="b7")
        _FakeSnapshot.instances.append(self)

    def start(self, options=None):
        self.start_calls.append(dict(options or {}))

    def smartui_app_snapshot(self, driver, name, options=None):
        self.snapshot_calls.append((driver, name, dict(options or {})))

    def stop(self):
        self.stop_count += 1


@pytest.fixture(autouse=True)
def _clean_state(monkeypatch):
    """Fresh helper state, no ambient token, fake SDK installed."""
    _FakeSnapshot.instances = []
    monkeypatch.delenv("PROJECT_TOKEN", raising=False)
    monkeypatch.setattr(_config, "_config", dict(_config._config), raising=False)
    _config._config.pop("smartui_project_token", None)
    _config._config.pop("smartui_build_name", None)
    sdk_pkg = types.ModuleType("lambdatest_selenium_driver")
    sdk_mod = types.ModuleType("lambdatest_selenium_driver.smartui_app_snapshot")
    sdk_mod.SmartUIAppSnapshot = _FakeSnapshot
    sdk_pkg.smartui_app_snapshot = sdk_mod
    monkeypatch.setitem(sys.modules, "lambdatest_selenium_driver", sdk_pkg)
    monkeypatch.setitem(
        sys.modules, "lambdatest_selenium_driver.smartui_app_snapshot", sdk_mod
    )
    yield
    smartui_mod._active = None


def test_no_token_returns_skipped_without_raising(caplog):
    caplog.set_level(logging.WARNING, logger="testmu_appium")
    result = smartui_screenshot(object(), "checkout-screen")
    assert result["status"] == "skipped"
    assert "token" in result["reason"].lower()
    assert "checkout-screen" in caplog.text
    assert _FakeSnapshot.instances == []


def test_env_token_starts_sdk_and_captures(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    driver = object()
    result = smartui_screenshot(driver, "checkout-screen")
    assert result == {"status": "captured", "name": "checkout-screen"}
    (inst,) = _FakeSnapshot.instances
    assert inst.start_calls == [{"projectToken": "tok-123"}]
    assert inst.snapshot_calls == [(driver, "checkout-screen", {})]


def test_second_capture_reuses_the_started_session(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    smartui_screenshot(object(), "one")
    smartui_screenshot(object(), "two")
    (inst,) = _FakeSnapshot.instances
    assert len(inst.start_calls) == 1
    assert [c[1] for c in inst.snapshot_calls] == ["one", "two"]


def test_configured_token_wins_over_env(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "env-tok")
    _config.set_value("smartui_project_token", "cfg-tok")
    smartui_screenshot(object(), "shot")
    (inst,) = _FakeSnapshot.instances
    assert inst.start_calls[0]["projectToken"] == "cfg-tok"


def test_configured_build_name_is_carried_into_start(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    _config.set_value("smartui_build_name", "regression-lane")
    smartui_screenshot(object(), "shot")
    (inst,) = _FakeSnapshot.instances
    assert inst.start_calls[0]["buildName"] == "regression-lane"


def test_start_failure_returns_failed_without_raising(monkeypatch, caplog):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    caplog.set_level(logging.WARNING, logger="testmu_appium")

    def boom(options=None):
        raise RuntimeError("build create rejected")

    monkeypatch.setattr(_FakeSnapshot, "start", staticmethod(boom))
    result = smartui_screenshot(object(), "shot")
    assert result["status"] == "failed"
    assert "build create rejected" in result["reason"]


def test_capture_failure_returns_failed_without_raising(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")

    def boom(self, driver, name, options=None):
        raise RuntimeError("upload refused")

    monkeypatch.setattr(_FakeSnapshot, "smartui_app_snapshot", boom)
    result = smartui_screenshot(object(), "shot")
    assert result["status"] == "failed"
    assert "upload refused" in result["reason"]


def test_failure_reason_redacts_the_project_token(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-secret-9")

    def boom(self, driver, name, options=None):
        raise RuntimeError("denied for token tok-secret-9")

    monkeypatch.setattr(_FakeSnapshot, "smartui_app_snapshot", boom)
    result = smartui_screenshot(object(), "shot")
    assert "tok-secret-9" not in result["reason"]
    assert "***" in result["reason"]


def test_failure_reason_redacts_lt_credentials(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    monkeypatch.setenv("LT_ACCESS_KEY", "ak-secret-7")

    def boom(self, driver, name, options=None):
        raise RuntimeError("auth ak-secret-7 rejected")

    monkeypatch.setattr(_FakeSnapshot, "smartui_app_snapshot", boom)
    result = smartui_screenshot(object(), "shot")
    assert "ak-secret-7" not in result["reason"]


def test_missing_sdk_raises_import_error(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    monkeypatch.setitem(
        sys.modules, "lambdatest_selenium_driver.smartui_app_snapshot", None
    )
    with pytest.raises(ImportError):
        smartui_screenshot(object(), "shot")


def test_finalize_stops_the_build_once_and_is_idempotent(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    smartui_screenshot(object(), "shot")
    (inst,) = _FakeSnapshot.instances
    finalize_smartui()
    finalize_smartui()
    assert inst.stop_count == 1


def test_finalize_without_a_session_is_a_no_op():
    finalize_smartui()
    assert _FakeSnapshot.instances == []


def test_finalize_swallows_stop_failure(monkeypatch, caplog):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    caplog.set_level(logging.WARNING, logger="testmu_appium")
    smartui_screenshot(object(), "shot")

    def boom(self):
        raise RuntimeError("stop rejected")

    monkeypatch.setattr(_FakeSnapshot, "stop", boom)
    finalize_smartui()
    assert "stop rejected" in caplog.text
    assert smartui_mod._active is None


def test_build_name_accessor_reports_the_sdk_build(monkeypatch):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    assert smartui_build_name() is None
    smartui_screenshot(object(), "shot")
    assert smartui_build_name() == "build-7"


def test_capture_logs_the_attempt(monkeypatch, caplog):
    monkeypatch.setenv("PROJECT_TOKEN", "tok-123")
    caplog.set_level(logging.INFO, logger="testmu_appium")
    smartui_screenshot(object(), "checkout-screen", description="capture checkout")
    assert "checkout-screen" in caplog.text
