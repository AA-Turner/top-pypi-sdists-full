"""Test _settle_before_teardown — cloud-only settle window before driver.quit()
so the grid's video encoder can flush the final action's frames.

Regression: on the LambdaTest grid (capability video:true), driver.quit()
fired immediately after the verdict (`lambda-status=...`) was reported, so
the session VIDEO recording blacked out before the last action was visible —
the grid-side encoder never got a chance to flush. Fix: a best-effort settle
window — bounded wait for document.readyState == 'complete', then a fixed
flush delay — inserted between status reporting and driver.quit(). No-op on
local runs or when video recording is disabled (_bool_he("VIDEO", True) from
_capability.py, reused rather than re-resolved here).
"""
import pytest
from unittest.mock import MagicMock, patch
from testmu_selenium._session import run
from testmu_selenium._helpers.driver import _drivers


@pytest.fixture(autouse=True)
def reset_drivers():
    _drivers.clear()
    yield
    _drivers.clear()


@pytest.fixture(autouse=True)
def force_cloud_run_target():
    """Default to the cloud (webdriver.Remote) branch; tests override to
    'local' where needed, same pattern as test_session.py."""
    with patch("testmu_selenium._config.run_target", "cloud"):
        yield


@pytest.fixture(autouse=True)
def _clean_teardown_env(monkeypatch):
    """Isolate from host-shell env and cross-test leakage for the new knobs."""
    for k in ("VIDEO", "TESTMU_TEARDOWN_VIDEO_DRAIN_MS", "TESTMU_TEARDOWN_IDLE_TIMEOUT_MS"):
        monkeypatch.delenv(k, raising=False)


def _readystate_calls(fake_driver):
    return [
        c for c in fake_driver.execute_script.call_args_list
        if c.args and c.args[0] == "return document.readyState"
    ]


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_waits_for_idle_and_drains_after_status_before_quit(mock_sleep, mock_remote):
    """cloud + video on (default) -> readyState wait happens, drain sleep(2.0)
    happens, and both fire AFTER lambda-status=passed and BEFORE driver.quit()."""
    fake_driver = MagicMock()
    fake_driver.execute_script.return_value = "complete"
    mock_remote.return_value = fake_driver

    run(lambda driver: None)

    assert _readystate_calls(fake_driver), (
        f"expected a document.readyState poll before teardown; "
        f"execute_script calls: {fake_driver.execute_script.call_args_list}"
    )
    mock_sleep.assert_called_once_with(2.0)

    calls = fake_driver.method_calls
    status_idx = next(
        i for i, c in enumerate(calls)
        if c[0] == "execute_script" and c.args[0] == "lambda-status=passed"
    )
    ready_idx = next(
        i for i, c in enumerate(calls)
        if c[0] == "execute_script" and c.args and c.args[0] == "return document.readyState"
    )
    quit_idx = next(i for i, c in enumerate(calls) if c[0] == "quit")
    assert status_idx < ready_idx < quit_idx, (
        f"expected status < settle < quit ordering; method_calls={calls}"
    )


@patch("testmu_selenium._session.time.sleep")
def test_settle_is_noop_for_local_run_target(mock_sleep):
    """run_target='local' -> no readyState wait, no drain sleep; quit still happens."""
    fake_driver = MagicMock()
    with patch("testmu_selenium._session._create_local_driver", return_value=fake_driver), \
         patch("testmu_selenium._config.run_target", "local"):
        run(lambda driver: None)

    mock_sleep.assert_not_called()
    assert not _readystate_calls(fake_driver)
    fake_driver.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_drain_ms_env_override(mock_sleep, mock_remote, monkeypatch):
    monkeypatch.setenv("TESTMU_TEARDOWN_VIDEO_DRAIN_MS", "500")
    fake_driver = MagicMock()
    fake_driver.execute_script.return_value = "complete"
    mock_remote.return_value = fake_driver

    run(lambda driver: None)

    mock_sleep.assert_called_once_with(0.5)


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_drain_ms_zero_skips_sleep(mock_sleep, mock_remote, monkeypatch):
    monkeypatch.setenv("TESTMU_TEARDOWN_VIDEO_DRAIN_MS", "0")
    fake_driver = MagicMock()
    fake_driver.execute_script.return_value = "complete"
    mock_remote.return_value = fake_driver

    run(lambda driver: None)

    mock_sleep.assert_not_called()


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_swallows_readystate_failure_on_pass_path(mock_sleep, mock_remote):
    """readyState poll raising must not block the drain sleep or driver.quit()."""
    fake_driver = MagicMock()
    fake_driver.execute_script.side_effect = Exception("session already gone")
    mock_remote.return_value = fake_driver

    run(lambda driver: None)  # must not raise

    mock_sleep.assert_called_once_with(2.0)
    fake_driver.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_swallows_readystate_failure_on_fail_path(mock_sleep, mock_remote):
    """readyState poll raising on the fail path must not mask the original
    test exception, and settle + quit must still both run."""
    fake_driver = MagicMock()
    fake_driver.execute_script.side_effect = Exception("session already gone")
    mock_remote.return_value = fake_driver

    def failing(driver):
        raise ValueError("original failure")

    with pytest.raises(ValueError, match="original failure"):
        run(failing)

    mock_sleep.assert_called_once_with(2.0)
    fake_driver.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.time.sleep")
def test_settle_is_noop_when_video_disabled(mock_sleep, mock_remote, monkeypatch):
    monkeypatch.setenv("VIDEO", "false")
    fake_driver = MagicMock()
    fake_driver.execute_script.return_value = "complete"
    mock_remote.return_value = fake_driver

    run(lambda driver: None)

    mock_sleep.assert_not_called()
    assert not _readystate_calls(fake_driver), (
        f"video disabled must skip the readyState poll entirely; "
        f"execute_script calls: {fake_driver.execute_script.call_args_list}"
    )
