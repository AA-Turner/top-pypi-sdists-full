"""uploads larger than ~100MB must not be base64'd over the wire.

Selenium-Python's WebDriver defaults to ``LocalFileDetector``: it sees a path
that exists on the machine running the test and base64-encodes the whole file
into the send_keys command so the grid node can materialise it. In an exported
run the file is ALREADY on the node (the bundle downloads ``uploaded_files``
into ~/Downloads before the test), so that transfer is both unnecessary and
fatal past ~100MB — chromedriver rejects the oversized command.

Port of the V2 upload branch:

    with driver.file_detector_context(UselessFileDetector):
        element.send_keys(file_path)

Selenium-Java needs no equivalent — its RemoteWebDriver already defaults to
UselessFileDetector and the binding never calls setFileDetector — so this
ticket is Python-only.
"""
from unittest.mock import MagicMock, patch

from selenium.webdriver.remote.file_detector import UselessFileDetector

from testmu_selenium import _action_set_input_files as sif
from testmu_selenium._action_set_input_files import (
    _upload_send_keys,
    _set_input_files_runner,
    _set_input_files_coord_runner,
    set_input_files,
)


def _driver_with_detector_ctx():
    """A driver whose file_detector_context records entry/exit around send_keys."""
    driver = MagicMock(name="driver")
    events = []

    class _Ctx:
        def __init__(self, detector):
            events.append(("enter", detector))

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            events.append(("exit", None))
            return False

    driver.file_detector_context.side_effect = _Ctx
    return driver, events


# ---------------------------------------------------------------------------
# _upload_send_keys — the helper itself
# ---------------------------------------------------------------------------

def test_send_keys_runs_inside_a_useless_file_detector_context():
    driver, events = _driver_with_detector_ctx()
    element = MagicMock(name="element")

    _upload_send_keys(driver, element, "/tmp/big.zip")

    driver.file_detector_context.assert_called_once_with(UselessFileDetector)
    element.send_keys.assert_called_once_with("/tmp/big.zip")
    assert [e[0] for e in events] == ["enter", "exit"]
    assert events[0][1] is UselessFileDetector


def test_the_context_is_scoped_and_exits_after_the_upload():
    """Scoped per call so the session-wide detector is restored and non-upload
    send_keys (type / press_key) keep the default LocalFileDetector."""
    driver, events = _driver_with_detector_ctx()
    element = MagicMock(name="element")

    order = []
    element.send_keys.side_effect = lambda v: order.append("send")
    _upload_send_keys(driver, element, "/tmp/big.zip")

    # send_keys must happen between enter and exit, not after the context closed.
    assert [e[0] for e in events] == ["enter", "exit"]
    assert order == ["send"]


def test_helper_degrades_to_a_plain_send_keys_without_a_driver():
    element = MagicMock(name="element")
    _upload_send_keys(None, element, "/tmp/a.txt")
    element.send_keys.assert_called_once_with("/tmp/a.txt")


def test_helper_degrades_when_the_driver_has_no_detector_context():
    """A stub/mock driver without file_detector_context must still upload."""
    driver = MagicMock(name="driver", spec=[])  # no file_detector_context attr
    element = MagicMock(name="element")

    _upload_send_keys(driver, element, "/tmp/a.txt")

    element.send_keys.assert_called_once_with("/tmp/a.txt")


# ---------------------------------------------------------------------------
# Every upload send-keys site must use it
# ---------------------------------------------------------------------------

def test_runner_uses_the_detector_context():
    driver, _ = _driver_with_detector_ctx()
    element = MagicMock(name="element")

    _set_input_files_runner(element, {"driver": driver, "file_path": "/tmp/a.txt"})

    driver.file_detector_context.assert_called_once_with(UselessFileDetector)
    element.send_keys.assert_called_once_with("/tmp/a.txt")


def test_coord_runner_uses_the_detector_context():
    driver, _ = _driver_with_detector_ctx()
    element = MagicMock(name="element")
    driver.execute_script.return_value = element

    _set_input_files_coord_runner(driver, 10, 20, {"file_path": "/tmp/a.txt"})

    driver.file_detector_context.assert_called_once_with(UselessFileDetector)
    element.send_keys.assert_called_once_with("/tmp/a.txt")


def test_dom_first_fast_path_uses_the_detector_context():
    driver, _ = _driver_with_detector_ctx()
    element = MagicMock(name="element")

    with patch.object(sif, "_resolve_file_input_dom", return_value=element), \
         patch.object(sif, "_run_action") as m_run:
        set_input_files(driver, [], file_path="/tmp/a.txt")

    driver.file_detector_context.assert_called_once_with(UselessFileDetector)
    element.send_keys.assert_called_once_with("/tmp/a.txt")
    m_run.assert_not_called()


def test_multi_file_upload_also_goes_through_the_detector_context():
    driver, _ = _driver_with_detector_ctx()
    element = MagicMock(name="element")

    _set_input_files_runner(
        element, {"driver": driver, "file_paths": ["/tmp/a.txt", "/tmp/b.txt"]})

    driver.file_detector_context.assert_called_once_with(UselessFileDetector)
    element.send_keys.assert_called_once_with("/tmp/a.txt\n/tmp/b.txt")
