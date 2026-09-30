"""clear the file <input> before send_keys so a re-used input does
not carry the previous row's file.

``send_keys`` on a file input APPENDS to its FileList rather than replacing it,
so a form that reuses one hidden <input> across rows uploads "File A + File B"
on the second row instead of "File B". Playwright's set_input_files replaces
natively, which is why only the Selenium bindings need this.

Port of V2 (upload branch):

    try:
        driver.execute_script("arguments[0].value = '';", element)
    except Exception as e:
        print('Could not clear file input before upload: ', e)
    element.send_keys(file_path)

The binding has THREE send_keys sites (the spec runner, the DESKTOP_LOCATE
coord runner, and the selectorless DOM-first fast path); all three must clear.
"""
from unittest.mock import MagicMock, call, patch

import pytest

from testmu_selenium import _action_set_input_files as sif
from testmu_selenium._action_set_input_files import (
    _clear_file_input,
    _set_input_files_runner,
    _set_input_files_coord_runner,
    set_input_files,
)

CLEAR_JS = "arguments[0].value = '';"


# ---------------------------------------------------------------------------
# _clear_file_input — the helper itself
# ---------------------------------------------------------------------------

def test_clear_runs_the_value_reset_script_against_the_element():
    driver, element = MagicMock(name="driver"), MagicMock(name="element")
    _clear_file_input(driver, element)
    driver.execute_script.assert_called_once_with(CLEAR_JS, element)


def test_clear_is_best_effort_and_never_raises():
    """A JS failure must not abort an otherwise valid upload (V2 parity)."""
    driver, element = MagicMock(name="driver"), MagicMock(name="element")
    driver.execute_script.side_effect = RuntimeError("javascript error")
    _clear_file_input(driver, element)  # must not raise


def test_clear_is_a_no_op_without_a_driver():
    _clear_file_input(None, MagicMock())  # must not raise


# ---------------------------------------------------------------------------
# Site 1 — the spec runner
# ---------------------------------------------------------------------------

def test_runner_clears_before_send_keys():
    driver, element = MagicMock(name="driver"), MagicMock(name="element")
    manager = MagicMock()
    manager.attach_mock(driver.execute_script, "clear")
    manager.attach_mock(element.send_keys, "send")

    _set_input_files_runner(element, {"driver": driver, "file_path": "/tmp/a.txt"})

    driver.execute_script.assert_called_once_with(CLEAR_JS, element)
    element.send_keys.assert_called_once_with("/tmp/a.txt")
    # Order is the whole point: clearing AFTER send_keys would wipe the upload.
    assert [c[0] for c in manager.mock_calls] == ["clear", "send"]


def test_runner_still_uploads_when_the_clear_fails():
    driver, element = MagicMock(name="driver"), MagicMock(name="element")
    driver.execute_script.side_effect = RuntimeError("javascript error")

    _set_input_files_runner(element, {"driver": driver, "file_path": "/tmp/a.txt"})

    element.send_keys.assert_called_once_with("/tmp/a.txt")


# ---------------------------------------------------------------------------
# Site 2 — the DESKTOP_LOCATE coord runner
# ---------------------------------------------------------------------------

def test_coord_runner_clears_before_send_keys():
    driver, element = MagicMock(name="driver"), MagicMock(name="element")
    # First execute_script resolves the input from the healed pixel; the second
    # is the clear.
    driver.execute_script.side_effect = [element, None]

    _set_input_files_coord_runner(driver, 10, 20, {"file_path": "/tmp/a.txt"})

    assert driver.execute_script.call_args_list[-1] == call(CLEAR_JS, element)
    element.send_keys.assert_called_once_with("/tmp/a.txt")


# ---------------------------------------------------------------------------
# Site 3 — the selectorless DOM-first fast path
# ---------------------------------------------------------------------------

def test_dom_first_fast_path_clears_before_send_keys():
    driver, element = MagicMock(name="driver"), MagicMock(name="element")

    with patch.object(sif, "_resolve_file_input_dom", return_value=element), \
         patch.object(sif, "_run_action") as m_run:
        set_input_files(driver, [], file_path="/tmp/a.txt")

    driver.execute_script.assert_called_once_with(CLEAR_JS, element)
    element.send_keys.assert_called_once_with("/tmp/a.txt")
    # DOM-first succeeded, so the heal engine is never reached.
    m_run.assert_not_called()


# ---------------------------------------------------------------------------
# The carry-over scenario this ticket exists for
# ---------------------------------------------------------------------------

def test_second_upload_to_a_shared_input_clears_the_first_file():
    """Two rows, one shared <input>: row 2 must reset before sending File B."""
    driver, element = MagicMock(name="driver"), MagicMock(name="element")

    _set_input_files_runner(element, {"driver": driver, "file_path": "/tmp/A.txt"})
    _set_input_files_runner(element, {"driver": driver, "file_path": "/tmp/B.txt"})

    assert driver.execute_script.call_args_list == [
        call(CLEAR_JS, element), call(CLEAR_JS, element),
    ]
    assert element.send_keys.call_args_list == [call("/tmp/A.txt"), call("/tmp/B.txt")]
