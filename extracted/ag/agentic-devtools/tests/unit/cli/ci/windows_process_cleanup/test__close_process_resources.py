from collections.abc import Callable
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_cleanup
from agentic_devtools.cli.ci.windows_process_cleanup import _close_process_resources


def test_empty_resource_cleanup() -> None:
    assert _close_process_resources(None, None, 1, Mock()) == ()
    no_handles = Mock(stdout=None, stderr=None, stdin=None)
    no_handles._handle = object()
    assert _close_process_resources(no_handles, None, 1, Mock()) == ()


def test_base_exceptions_do_not_skip_resource_cleanup() -> None:
    first, second, third = Mock(), Mock(), Mock()
    first.close.side_effect = KeyboardInterrupt("worker close interruption")
    process_handle = Mock()
    process = Mock(stdout=first, stderr=second, stdin=third)
    process._handle = process_handle
    close_job = Mock(side_effect=OSError("job close interruption"))

    errors = _close_process_resources(process, 17, 1, close_job)

    assert errors == ("job close interruption", "Stream close failed in worker: worker close interruption")
    close_job.assert_called_once_with(17)
    first.close.assert_called_once()
    second.close.assert_called_once()
    third.close.assert_called_once()
    process_handle.Close.assert_called_once()

    process_handle.Close.side_effect = OSError("process handle close interruption")
    first.close.side_effect = None
    close_job = Mock()
    errors = _close_process_resources(process, 17, 1, close_job)

    assert errors == ("process handle close interruption",)
    close_job.assert_called_once_with(17)


def test_caller_cancellation_is_reraised_after_resource_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    interruption = KeyboardInterrupt("caller cleanup cancellation")
    streams = [Mock(), Mock(), Mock()]
    process_handle = Mock()
    process = Mock(stdout=streams[0], stderr=streams[1], stdin=streams[2])
    process._handle = process_handle
    close_job = Mock()
    threads: list[Mock] = []

    def make_thread(*, target: Callable[[], None], daemon: bool) -> Mock:
        thread = Mock()
        thread.is_alive.return_value = False
        thread.start.side_effect = target
        thread.join.side_effect = (
            interruption
            if not threads
            else (SystemExit("secondary cleanup interruption") if len(threads) == 1 else None)
        )
        threads.append(thread)
        assert daemon
        return thread

    monkeypatch.setattr(windows_process_cleanup.threading, "Thread", make_thread)

    with pytest.raises(KeyboardInterrupt) as raised:
        _close_process_resources(process, 17, 1, close_job)

    assert raised.value is interruption
    close_job.assert_called_once_with(17)
    assert len(threads) == 3
    assert all(stream.close.call_count == 1 for stream in streams)
    process_handle.Close.assert_called_once()
    assert getattr(interruption, "_agdt_cleanup_errors") == ("secondary cleanup interruption",)
