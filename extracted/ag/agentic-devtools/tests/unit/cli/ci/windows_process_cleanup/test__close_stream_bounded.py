from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_cleanup


def test_closes_stream_within_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    stream = Mock()
    thread = Mock()
    thread.is_alive.return_value = False
    thread_factory = Mock(return_value=thread)

    def start_thread() -> None:
        thread_factory.call_args.kwargs["target"]()

    thread.start.side_effect = start_thread
    monkeypatch.setattr(windows_process_cleanup.threading, "Thread", thread_factory)

    windows_process_cleanup._close_stream_bounded(stream, 2)

    stream.close.assert_called_once()
    thread.start.assert_called_once()
    thread.join.assert_called_once_with(2)
    assert thread_factory.call_args.kwargs["daemon"] is True


def test_reports_close_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    thread = Mock()
    thread.is_alive.return_value = True
    monkeypatch.setattr(windows_process_cleanup.threading, "Thread", Mock(return_value=thread))

    with pytest.raises(TimeoutError, match="cleanup deadline"):
        windows_process_cleanup._close_stream_bounded(Mock(), 2)


def test_preserves_stream_close_error(monkeypatch: pytest.MonkeyPatch) -> None:
    stream = Mock()
    stream.close.side_effect = ValueError("injected close failure")
    thread = Mock()
    thread.is_alive.return_value = False
    thread_factory = Mock(return_value=thread)

    def start_thread() -> None:
        thread_factory.call_args.kwargs["target"]()

    thread.start.side_effect = start_thread
    monkeypatch.setattr(windows_process_cleanup.threading, "Thread", thread_factory)

    with pytest.raises(ValueError, match="injected close failure"):
        windows_process_cleanup._close_stream_bounded(stream, 2)
