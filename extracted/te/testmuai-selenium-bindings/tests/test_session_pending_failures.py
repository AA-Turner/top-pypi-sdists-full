"""Tests: testmu_selenium._session.run() surfaces pending failures
recorded by route_failure('Fail but continue executing', ...).

Without this surfacing, every step in a 'Fail but continue' test could
fail and run() would still report the LT session as 'passed' — see
test_route_failure.py's accumulator section for the regression repro.

The contract:
- On end-of-fn with a non-empty accumulator, run() reports `failed` to LT
  AND re-raises so HE exit code reflects the failure.
- The accumulator is reset at the START of every run() so stale state from
  a prior test in the same process cannot bleed in.
- If fn(driver) itself raises, the original exception still propagates
  (immediate-fail and explicit raises take precedence over pending-list
  surfacing — the user already has the most-specific failure).
- 'Warn but continue' alone leaves the accumulator empty so run() reports
  `passed` as before.
"""
import pytest
from unittest.mock import MagicMock, patch
from testmu_selenium._session import run
from testmu_selenium._helpers.driver import _drivers
from testmu_selenium._route_failure import (
    route_failure,
    _has_pending_failures,
    _reset_pending_failures,
)


@pytest.fixture(autouse=True)
def _reset_state():
    _drivers.clear()
    _reset_pending_failures()
    yield
    _drivers.clear()
    _reset_pending_failures()


@pytest.fixture(autouse=True)
def _force_cloud_run_target():
    """Drive the cloud (webdriver.Remote) branch so lambda-status reporting is exercised."""
    with patch("testmu_selenium._config.run_target", "cloud"):
        yield


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_raises_when_fail_continue_step_recorded(mock_remote):
    """End-of-fn with pending failures must raise so HE sees non-zero exit."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    def test_body(driver):
        route_failure("Fail but continue executing", ValueError("boom"), "click login")

    with pytest.raises(RuntimeError) as exc_info:
        run(test_body)
    msg = str(exc_info.value)
    assert "click login" in msg, f"label missing from RuntimeError: {msg!r}"
    assert "boom" in msg, f"exc text missing from RuntimeError: {msg!r}"


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_reports_failed_status_when_pending_failures(mock_remote):
    """Pending failures must also report `lambda-status=failed` to LT cloud."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    def test_body(driver):
        route_failure("Fail but continue executing", ValueError("boom"), "click login")

    with pytest.raises(RuntimeError):
        run(test_body)

    failed_calls = [
        c for c in fake_driver.execute_script.call_args_list
        if c.args[0] == "lambda-status=failed"
    ]
    assert failed_calls, (
        "expected lambda-status=failed call when pending failures present; "
        f"all execute_script calls: {fake_driver.execute_script.call_args_list}"
    )


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_does_not_raise_for_warn_continue_only(mock_remote):
    """'Warn but continue' alone must NOT mark the test failed — passed stays passed."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    def test_body(driver):
        route_failure("Warn but continue executing", ValueError("warn"), "noisy step")

    run(test_body)  # must not raise

    passed_calls = [
        c for c in fake_driver.execute_script.call_args_list
        if c.args[0] == "lambda-status=passed"
    ]
    assert passed_calls, "expected lambda-status=passed for warn-only test"


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_resets_pending_failures_at_start(mock_remote):
    """Stale pending failures from a previous run must not contaminate this one."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    route_failure("Fail but continue executing", ValueError("stale"), "previous test")
    assert _has_pending_failures()

    run(lambda d: None)  # clean body — must not raise


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_preserves_fn_exception_when_pending_also_present(mock_remote):
    """If fn(driver) itself raises, the original exception propagates.
    Pending failures are surfaced only when fn returned cleanly — they must
    NOT shadow a real, specific exception class from the test body."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    def test_body(driver):
        route_failure("Fail but continue executing", ValueError("earlier"), "step A")
        raise KeyError("immediate fail at end")

    with pytest.raises(KeyError, match="immediate fail at end"):
        run(test_body)
