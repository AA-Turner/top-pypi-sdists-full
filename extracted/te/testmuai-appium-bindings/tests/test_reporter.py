"""Sync Reporter Protocol, factory, and the LT lambda-hook wire form."""
import json

import pytest

from testmu_appium import _config
from testmu_appium._reporter import (
    LocalReporter, LTReporter, NullReporter, get_reporter, reporter, _reset_reporter,
)


class _RecordingDriver:
    def __init__(self, fail=False):
        self.scripts = []
        self._fail = fail

    def execute_script(self, script, *args):
        if self._fail:
            raise RuntimeError("session gone")
        self.scripts.append(script)


@pytest.fixture(autouse=True)
def _clean_reporter():
    _reset_reporter()
    yield
    _reset_reporter()


def test_factory_picks_lt_reporter_for_cloud(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "cloud")
    assert isinstance(get_reporter(), LTReporter)


def test_factory_picks_local_reporter_otherwise(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "local")
    assert isinstance(get_reporter(), LocalReporter)


def test_reporter_singleton_is_memoised(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "local")
    assert reporter() is reporter()


def test_null_reporter_satisfies_the_protocol():
    r = NullReporter()
    r.begin_test("t")
    r.begin_step("s", instruction_id="i")
    r.end_step("s", ok=True)
    r.warn_step("s", RuntimeError("x"))
    r.attach_screenshot(b"png")
    r.pass_test()
    r.fail_test(RuntimeError("x"))


class TestLTReporter:
    def _reporter(self, driver=None):
        r = LTReporter()
        r.set_driver(driver or _RecordingDriver())
        return r

    def test_begin_step_emits_the_testcase_start_hook(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.begin_step("Tap Compose", instruction_id="op-7")
        assert len(driver.scripts) == 1
        name, _, payload = driver.scripts[0].partition("=")
        assert name == "lambda-testCase-start"
        assert json.loads(payload) == {"name": "Tap Compose", "instructionId": "op-7"}

    def test_end_step_carries_the_heal_telemetry(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.end_step("Tap Compose", ok=True, instruction_id="op-7",
                   is_autohealed=True, autoheal_source="v16-autoheal")
        name, _, payload = driver.scripts[0].partition("=")
        assert name == "lambda-testCase-end"
        assert json.loads(payload) == {
            "name": "Tap Compose",
            "status": "passed",
            "instructionId": "op-7",
            "is_autohealed": True,
            "autoheal_source": "v16-autoheal",
        }

    def test_end_step_omits_heal_fields_when_no_heal_ran(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.end_step("Tap Compose", ok=False, error=RuntimeError("boom"))
        payload = json.loads(driver.scripts[0].partition("=")[2])
        assert payload["status"] == "failed"
        assert "is_autohealed" not in payload
        assert "autoheal_source" not in payload

    def test_end_step_includes_the_interacted_element_payload(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.end_step("Tap Compose", ok=True, interacted_element={
            "original_locator": 'new UiSelector().text("Compose")',
            "bounds": [840, 2050, 1040, 2250],
            "center": [940, 2150],
        })
        payload = json.loads(driver.scripts[0].partition("=")[2])
        assert payload["interacted_element"]["center"] == [940, 2150]

    def test_verdict_uses_the_body_matched_lambda_status_form(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.pass_test()
        assert driver.scripts == ["lambda-status=passed"]

    def test_fail_verdict(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.fail_test(RuntimeError("boom"))
        assert driver.scripts == ["lambda-status=failed"]

    def test_hook_failures_never_propagate(self):
        r = self._reporter(_RecordingDriver(fail=True))
        r.begin_step("s")
        r.end_step("s", ok=True)
        r.pass_test()

    def test_no_driver_is_a_no_op(self):
        r = LTReporter()
        r.begin_step("s")
        r.end_step("s", ok=True)

    def test_step_numbering_restarts_each_test(self):
        driver = _RecordingDriver()
        r = self._reporter(driver)
        r.begin_step("a")
        r.begin_step("b")
        assert r._step_num == 2
        r.begin_test("t")
        assert r._step_num == 0


class TestLocalReporter:
    def test_records_nothing_on_the_driver(self, caplog):
        r = LocalReporter()
        r.set_driver(_RecordingDriver())
        r.begin_test("t")
        r.begin_step("Tap Compose")
        r.end_step("Tap Compose", ok=True, is_autohealed=True)
        r.pass_test()
        assert r._driver.scripts == []

    def test_logs_the_step_lines(self, caplog):
        import logging

        caplog.set_level(logging.INFO, logger="testmu_appium")
        r = LocalReporter()
        r.begin_test("t")
        r.begin_step("Tap Compose")
        r.end_step("Tap Compose", ok=True, is_autohealed=True)
        text = caplog.text
        assert "[TEST START] t" in text
        assert "Tap Compose" in text
        assert "auto_heal=True" in text
