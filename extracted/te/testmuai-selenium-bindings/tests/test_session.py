"""Test run() lifecycle — single-driver entrypoint (cloud branch)."""
import pytest
from unittest.mock import MagicMock, patch
from testmu_selenium._session import run
from testmu_selenium._helpers.driver import get_driver, _drivers


@pytest.fixture(autouse=True)
def reset_drivers():
    _drivers.clear()
    yield
    _drivers.clear()


@pytest.fixture(autouse=True)
def force_cloud_run_target():
    """These tests exercise the cloud (webdriver.Remote) branch — pin run_target."""
    with patch("testmu_selenium._config.run_target", "cloud"):
        yield


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_launches_driver(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    run(lambda driver: None)
    assert mock_remote.called


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_invokes_fn_with_driver(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    received = {}
    def my_test(driver):
        received["driver"] = driver
    run(my_test)
    assert received["driver"] is fake_driver


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_calls_quit_in_finally(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    run(lambda driver: None)
    fake_driver.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_calls_quit_even_on_test_failure(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    def failing(driver):
        raise ValueError("boom")
    with pytest.raises(ValueError):
        run(failing)
    fake_driver.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_swallows_quit_failure(mock_remote, caplog):
    fake_driver = MagicMock()
    fake_driver.quit.side_effect = Exception("quit failed")
    mock_remote.return_value = fake_driver
    # Should not raise — quit failure is logged + swallowed
    run(lambda driver: None)


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_registers_driver_for_get_driver(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    captured = {}
    def my_test(driver):
        captured["d"] = get_driver("default")
    run(my_test)
    assert captured["d"] is fake_driver


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_clears_driver_registry_after(mock_remote):
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    run(lambda driver: None)
    assert _drivers == {}


def test_get_driver_raises_when_no_session():
    """Without an active run(), get_driver raises a clear error."""
    with pytest.raises(RuntimeError, match="no driver registered"):
        get_driver()


# ---------------------------------------------------------------------------
# LambdaTest cloud session status reporting
#
# Pre-0.1.5 the bindings never told the LT cloud session whether the test
# passed or failed, so HyperExecute classified the scenario as "skipped"
# (total_tests:0) regardless of the actual outcome — a regression was observed
# where a heal cascade ran cleanly but no test_status was recorded against the LT
# session. New contract mirrors V2 selenium emit `lambda-status=...` and V4
# playwright's `set_test_status(page, status, remark)` convention.
# ---------------------------------------------------------------------------

@patch("testmu_selenium._session.webdriver.Remote")
def test_run_reports_lambda_status_passed_on_success(mock_remote):
    """Cloud run_target + fn returns cleanly → driver.execute_script called
    with `lambda-status=passed` as the script body BEFORE quit."""
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    run(lambda driver: None)

    # Find the lambda-status=passed execute_script call
    matches = [
        c for c in fake_driver.execute_script.call_args_list
        if c.args[0] == "lambda-status=passed"
    ]
    assert matches, (
        f"No lambda-status=passed call. All execute_script calls: "
        f"{fake_driver.execute_script.call_args_list}"
    )
    # Status reporting must happen BEFORE quit so the LT session is updated
    # while still active. Compare call ordering on the same driver mock.
    quit_call_idx = next(
        (i for i, c in enumerate(fake_driver.method_calls) if c[0] == "quit"),
        -1,
    )
    status_call_idx = next(
        (i for i, c in enumerate(fake_driver.method_calls)
         if c[0] == "execute_script" and c.args[0] == "lambda-status=passed"),
        -1,
    )
    assert status_call_idx >= 0 and quit_call_idx >= 0, "missing call(s)"
    assert status_call_idx < quit_call_idx, (
        "lambda-status=passed must fire before driver.quit() — otherwise the LT "
        "session is gone before status reaches the cloud."
    )


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_reports_lambda_status_failed_on_exception(mock_remote):
    """fn raises → lambda-status=failed emitted as script body, then re-raise.

    The remark (exception message) is no longer sent in the execute_script call;
    it is logged instead. Only the status keyword reaches the LT hub.
    """
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver

    def failing(driver):
        raise ValueError("synthetic test failure")

    with pytest.raises(ValueError, match="synthetic test failure"):
        run(failing)

    matches = [
        c for c in fake_driver.execute_script.call_args_list
        if c.args[0] == "lambda-status=failed"
    ]
    assert matches, "No lambda-status=failed call on exception path"
    # The remark is NOT in the execute_script call — it is logged. Verify
    # the call has exactly one positional arg (the script body, no extra args).
    call = matches[0]
    assert len(call.args) == 1, (
        f"execute_script should have exactly 1 arg (script body); got: {call.args!r}"
    )


@patch("testmu_selenium._session.webdriver.Remote")
def test_lambdatest_action_is_script_body_not_arg(mock_remote):
    """The lambda-status marker must BE the script body, not passed as an argument.

    The LambdaTest Selenium hub intercepts the WebDriver executeScript command by
    matching the SCRIPT BODY — it never reads args[0]. Passing the marker as an
    argument means the hub never sees it (test shows "completed" instead of
    passed/failed). Also, the prior `lambdatest_action: {...JSON...}` body form
    caused Chrome 148 SyntaxError on the inner `:`. The correct form is the simple
    V2/V4-proven `lambda-status=<status>` as the sole script body.
    """
    fake_driver = MagicMock()
    mock_remote.return_value = fake_driver
    run(lambda driver: None)

    status_calls = [
        c for c in fake_driver.execute_script.call_args_list
        if str(c.args[0]).startswith("lambda-status=")
    ]
    assert status_calls, (
        f"No lambda-status= call found. All execute_script calls: "
        f"{fake_driver.execute_script.call_args_list}"
    )
    call = status_calls[0]
    # The marker must be the sole positional argument (the script body) — no extra args.
    assert len(call.args) == 1, (
        f"execute_script must have exactly 1 arg (script body); got: {call.args!r}"
    )
    assert call.args[0] == "lambda-status=passed", (
        f"script body should be 'lambda-status=passed'; got: {call.args[0]!r}"
    )
    assert "lambdatest_action" not in call.args[0], (
        f"lambdatest_action must not appear in script body: {call.args[0]!r}"
    )


def test_run_skips_lambda_status_for_local_target():
    """run_target='local' → no lambda-status= call (no cloud session to update).
    Reporting against a local webdriver would be harmless but pollutes logs;
    we explicitly no-op on the local branch."""
    fake_driver = MagicMock()
    with patch("testmu_selenium._session._create_local_driver",
               return_value=fake_driver), \
         patch("testmu_selenium._config.run_target", "local"):
        run(lambda driver: None)

    matches = [
        c for c in fake_driver.execute_script.call_args_list
        if str(c.args[0]).startswith("lambda-status=")
    ]
    assert not matches, (
        f"Local run_target should NOT report LT status — found: {matches}"
    )


@patch("testmu_selenium._session.webdriver.Remote")
def test_run_swallows_status_reporter_failure(mock_remote, caplog):
    """If execute_script for status reporting fails (e.g. session torn down,
    network hiccup), the test outcome must NOT be masked. Reporter error is
    logged + swallowed; the original test result still propagates."""
    fake_driver = MagicMock()
    fake_driver.execute_script.side_effect = Exception("LT cloud unreachable")
    mock_remote.return_value = fake_driver

    # Successful test — reporter raises but is swallowed; run() returns clean
    run(lambda driver: None)

    # Failed test — exception propagates, reporter still runs
    fake_driver_2 = MagicMock()
    fake_driver_2.execute_script.side_effect = Exception("LT cloud down")
    mock_remote.return_value = fake_driver_2
    with pytest.raises(ValueError, match="real failure"):
        run(lambda driver: (_ for _ in ()).throw(ValueError("real failure")))
