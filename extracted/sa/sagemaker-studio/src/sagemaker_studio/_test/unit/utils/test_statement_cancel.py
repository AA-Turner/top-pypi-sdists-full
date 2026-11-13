"""
Tests for sagemaker_studio.utils._statement_cancel (cancel-statement-on-stop).

``run_bounded`` runs a cancellation call on a daemon thread under a time bound and never
reports a failure to its caller: a broken or slow cancel must not replace the user's interrupt
and must not hold it. The one exception that may leave it is a fresh ``KeyboardInterrupt``
delivered while it waits, i.e. a second Stop click.

No thread in these tests outlives its test: the slow-call case releases its worker before
returning, and every patched ``threading`` stand-in only replaces the name inside the module
under test.
"""

import io
import logging
import sys
import threading

import pytest

from sagemaker_studio.utils import _statement_cancel
from sagemaker_studio.utils._statement_cancel import report_cancelled, run_bounded

LOGGER_NAME = "sagemaker_studio.utils._statement_cancel"


class _InterruptingEvent:
    """An event whose wait is interrupted, as a second Stop click would interrupt it."""

    def set(self):
        pass

    def wait(self, timeout=None):
        raise KeyboardInterrupt


class _ThreadingShim:
    """``threading`` as the module under test sees it, with one name replaced."""

    def __init__(self, thread=threading.Thread, event=threading.Event):
        self.Thread = thread
        self.Event = event


class TestRunBounded:
    def test_success_runs_the_call_and_logs_it(self, caplog):
        calls = []

        with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
            returned = run_bounded(lambda: calls.append("cancel"), "thing cancel")

        assert returned is True
        assert calls == ["cancel"]
        assert "thing cancel: cancellation request succeeded" in caplog.text

    def test_a_failing_call_is_swallowed_and_logged_at_warning(self, caplog):
        def boom():
            raise RuntimeError("endpoint said no")

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            assert run_bounded(boom, "thing cancel") is False

        assert "thing cancel: cancellation request failed" in caplog.text
        assert "endpoint said no" in caplog.text
        assert [r.levelno for r in caplog.records] == [logging.WARNING]

    def test_a_slow_call_hits_the_bound_and_is_abandoned(self, caplog, monkeypatch):
        monkeypatch.setattr(_statement_cancel, "CANCEL_TIMEOUT_SECONDS", 0.05)
        release = threading.Event()
        started = threading.Event()

        def slow():
            started.set()
            release.wait(10)

        try:
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                assert run_bounded(slow, "slow cancel") is False
            assert started.is_set()
            assert "slow cancel: cancellation abandoned after 0.1s" in caplog.text
        finally:
            release.set()

    def test_a_thread_that_cannot_start_is_swallowed_and_logged(self, caplog):
        class _UnstartableThread:
            def __init__(self, *args, **kwargs):
                pass

            def start(self):
                raise RuntimeError("can't start new thread")

        shim = _ThreadingShim(thread=_UnstartableThread)
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(_statement_cancel, "threading", shim)
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                assert run_bounded(lambda: None, "thing cancel") is False

        assert "thing cancel: could not start cancellation thread" in caplog.text

    def test_an_interrupt_during_start_is_not_swallowed(self):
        """The start guard catches Exception, not BaseException, so Stop still gets through."""

        class _InterruptedThread:
            def __init__(self, *args, **kwargs):
                pass

            def start(self):
                raise KeyboardInterrupt

        shim = _ThreadingShim(thread=_InterruptedThread)
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(_statement_cancel, "threading", shim)
            with pytest.raises(KeyboardInterrupt):
                run_bounded(lambda: None, "thing cancel")

    def test_an_interrupt_while_waiting_propagates(self):
        shim = _ThreadingShim(event=_InterruptingEvent)
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(_statement_cancel, "threading", shim)
            with pytest.raises(KeyboardInterrupt):
                run_bounded(lambda: None, "thing cancel")


class TestReportCancelled:
    """
    The user-facing notice. ipykernel replaces ``sys.stderr`` with a stream that forwards to the
    notebook, so writing there puts the line in the cell output above the traceback. These cases
    replace ``sys.stderr`` the same way to observe what the cell would receive.
    """

    def test_an_accepted_cancel_says_so(self, capsys):
        report_cancelled("Redshift", True)

        err = capsys.readouterr().err
        assert err == "Query cancelled; cancel request accepted by Redshift.\n"

    def test_a_failed_cancel_warns_the_query_may_still_be_running(self, capsys):
        report_cancelled("Athena", False)

        err = capsys.readouterr().err
        assert "cancel request to Athena did not complete" in err
        assert "may still be running" in err

    def test_stderr_is_read_at_call_time_not_captured_at_import(self):
        """ipykernel swaps sys.stderr after import, so a captured reference would miss it."""
        replacement = io.StringIO()
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(sys, "stderr", replacement)
            report_cancelled("Redshift", True)

        assert "accepted by Redshift" in replacement.getvalue()

    def test_a_broken_stderr_is_swallowed_and_logged(self, caplog):
        """The interrupt is already unwinding; a dead stderr must not add a second failure."""

        class _BrokenStream:
            def write(self, _):
                raise ValueError("I/O operation on closed file")

            def flush(self):
                pass

        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(sys, "stderr", _BrokenStream())
            with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
                assert report_cancelled("Redshift", True) is None

        assert "could not write the cancellation notice to stderr" in caplog.text
