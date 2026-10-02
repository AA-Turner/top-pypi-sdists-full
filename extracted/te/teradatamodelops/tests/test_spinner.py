import io
import sys
import threading
from unittest import mock

import pytest

import tmo.spinner as spinner


def test_sys_print_writes_to_stdout(monkeypatch):
    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    spinner.sys_print("hello")
    assert buf.getvalue() == "hello"


def test_spin_it_invokes_spinner_and_returns(monkeypatch):
    calls = []

    class DummySpinner:
        def __init__(self, msg, speed):
            calls.append(("init", msg, speed))

        def start(self):
            calls.append("start")

        def stop(self):
            calls.append("stop")

        def remove_line(self):
            calls.append("remove_line")

    monkeypatch.setattr(spinner, "Spinner", DummySpinner)

    def sample_fn(x, y=2):
        calls.append(("fn", x, y))
        return "ok"

    result = spinner.spin_it(sample_fn, "testing", 0.123, 1, y=3)
    assert result == "ok"
    assert calls == [
        ("init", "testing", 0.123),
        "start",
        ("fn", 1, 3),
        "stop",
        "remove_line",
    ]


def test_progressbase_back_step_and_remove_line_calls_sys_print(monkeypatch):
    # Create instance without running __init__ to avoid threads
    pb = spinner.ProgressBase.__new__(spinner.ProgressBase)

    # Replace sys_print with a mock
    sp_mock = mock.Mock()
    monkeypatch.setattr(spinner, "sys_print", sp_mock)

    # When inplace is truthy, the sequences should be printed
    pb.inplace = 1
    pb.back_step()
    pb.remove_line()
    sp_mock.assert_any_call(spinner.CODE["CURSOR_NEXT_LINE"])
    sp_mock.assert_any_call(spinner.CODE["RM_LINE"])

    # Reset mock and ensure no calls when inplace is falsy
    sp_mock.reset_mock()
    pb.inplace = 0
    pb.back_step()
    pb.remove_line()
    sp_mock.assert_not_called()


def test_progressbase_start_calls_thread_start(monkeypatch):
    pb = spinner.ProgressBase.__new__(spinner.ProgressBase)
    mock_start = mock.Mock()
    monkeypatch.setattr(threading.Thread, "start", mock_start)
    pb.start()
    assert pb.stopFlag == 0
    mock_start.assert_called_once()


def test_progressbase_call_invokes_start(monkeypatch):
    pb = spinner.ProgressBase.__new__(spinner.ProgressBase)
    start_mock = mock.Mock()
    pb.start = start_mock
    pb()
    start_mock.assert_called_once()


def test_progressbase_stop_notifies_cv_and_acquires_rlock(monkeypatch):
    pb = spinner.ProgressBase.__new__(spinner.ProgressBase)
    pb.rlock = mock.Mock()
    pb.cv = mock.Mock()
    sp_mock = mock.Mock()
    monkeypatch.setattr(spinner, "sys_print", sp_mock)
    pb.stop()
    assert pb.stopFlag == 1
    sp_mock.assert_called_with(spinner.CODE["SHOW_CURSOR"])
    pb.cv.notify.assert_called_once()
    pb.rlock.acquire.assert_called_once()


def test_spinner_run_releases_rlock_and_prints(monkeypatch):
    s = spinner.Spinner("m", speed=0.001)
    s.rlock = mock.Mock()
    s.cv = mock.Mock()
    s.cv.acquire = mock.Mock()

    def wait_side_effect(timeout):
        if not hasattr(wait_side_effect, "calls"):
            wait_side_effect.calls = 1
            return None
        wait_side_effect.calls += 1
        s.stopFlag = 1
        return None

    s.cv.wait = mock.Mock(side_effect=wait_side_effect)
    sp_mock = mock.Mock()
    monkeypatch.setattr(spinner, "sys_print", sp_mock)
    s.inplace = 1
    s.stopFlag = 0
    s.run()
    sp_mock.assert_any_call(spinner.CODE["HIDE_CURSOR"])
    sp_mock.assert_any_call(spinner.CODE["CURSOR_NEXT_LINE"])
    s.rlock.release.assert_called_once()


def test_spinner_run_propagates_exception_and_does_not_release_rlock_on_error(
    monkeypatch,
):
    s = spinner.Spinner("m", speed=0.001)
    s.rlock = mock.Mock()
    s.cv = mock.Mock()
    s.cv.acquire = mock.Mock()
    s.cv.wait = mock.Mock(side_effect=RuntimeError("boom"))
    sp_mock = mock.Mock()
    monkeypatch.setattr(spinner, "sys_print", sp_mock)
    with pytest.raises(RuntimeError):
        s.run()
    assert not s.rlock.release.called


def test_spin_it_does_not_suppress_exceptions_from_function(monkeypatch):
    calls = []

    class DummySpinner:
        def __init__(self, msg, speed):
            calls.append(("init", msg, speed))

        def start(self):
            calls.append("start")

        def stop(self):
            calls.append("stop")

        def remove_line(self):
            calls.append("remove_line")

    monkeypatch.setattr(spinner, "Spinner", DummySpinner)

    def failing_fn():
        raise ValueError("fail")

    with pytest.raises(ValueError):
        spinner.spin_it(failing_fn, "msg", 0.01)
    assert ("start" in calls) and ("stop" not in calls)
