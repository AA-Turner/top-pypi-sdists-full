"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline`."""

from __future__ import annotations

from queue import Empty
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import _run_jira_probe_with_deadline


class _FakeQueue:
    def __init__(self, *, result: tuple[object, ...] | None = None, empty: bool = False) -> None:
        self.result = result
        self.empty = empty
        self.closed = False
        self.joined = False

    def get_nowait(self) -> tuple[object, ...]:
        if self.empty:
            raise Empty
        assert self.result is not None
        return self.result

    def close(self) -> None:
        self.closed = True

    def join_thread(self) -> None:
        self.joined = True


class _FakeProcess:
    def __init__(
        self,
        *,
        alive: bool = False,
        exitcode: int | None = 0,
        start_error: OSError | None = None,
        survives_terminate: bool = False,
    ) -> None:
        self.alive = alive
        self.exitcode = exitcode
        self.start_error = start_error
        self.survives_terminate = survives_terminate
        self.started = False
        self.join_calls: list[float] = []
        self.terminated = False
        self.killed = False

    def start(self) -> None:
        if self.start_error is not None:
            raise self.start_error
        self.started = True

    def join(self, timeout: float | None = None) -> None:
        if timeout is not None:
            self.join_calls.append(timeout)

    def is_alive(self) -> bool:
        return self.alive

    def terminate(self) -> None:
        self.terminated = True
        if not self.survives_terminate:
            self.alive = False

    def kill(self) -> None:
        self.killed = True
        self.alive = False


class _FakeContext:
    def __init__(self, queue: _FakeQueue, process: _FakeProcess) -> None:
        self.queue = queue
        self.process = process

    def Queue(self) -> _FakeQueue:
        return self.queue

    def Process(self, *, target, args) -> _FakeProcess:
        assert callable(target)
        assert args[0] is self.queue
        return self.process


class TestRunJiraProbeWithDeadline:
    """Cover result decoding and hard-deadline failure handling."""

    def test_returns_response_result(self) -> None:
        """A successful child result is passed through unchanged."""
        queue = _FakeQueue(result=("response", 200, "ok"))
        process = _FakeProcess()
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (200, "ok", None)
        assert process.join_calls == [5.0]
        assert queue.closed is True
        assert queue.joined is True

    def test_returns_timeout_result_payload(self) -> None:
        """Timeout payloads from the child process are normalized to an error message."""
        queue = _FakeQueue(result=("timeout", "timed out"))
        process = _FakeProcess()
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check timed out after 5.0s: timed out")

    def test_returns_error_result_payload(self) -> None:
        """Generic child-process request failures are surfaced as connectivity errors."""
        queue = _FakeQueue(result=("error", "offline"))
        process = _FakeProcess()
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: offline")

    def test_returns_invalid_result_message(self) -> None:
        """Unexpected child payload shapes are rejected explicitly."""
        queue = _FakeQueue(result=("unexpected",))
        process = _FakeProcess()
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: probe returned an invalid result")

    def test_returns_invalid_result_for_non_tuple_payload(self) -> None:
        """Non-tuple child payloads are rejected before result decoding."""
        queue = _FakeQueue()
        queue.result = "bad-payload"  # type: ignore[assignment]
        process = _FakeProcess()
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: probe returned an invalid result")

    def test_terminates_alive_process_on_parent_deadline(self) -> None:
        """A still-running child process is terminated when the hard deadline expires."""
        queue = _FakeQueue(result=("response", 200, "ok"))
        process = _FakeProcess(alive=True)
        context = _FakeContext(queue, process)

        with (
            patch("agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context),
            patch("agentic_devtools.cli.setup.provider_connectivity.time.monotonic", side_effect=[10.0, 15.0]),
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check timed out after 5.0s")
        assert process.terminated is True
        assert process.join_calls == [5.0, 0.0]
        assert process.killed is False

    def test_kills_alive_process_when_terminate_does_not_stop_it(self) -> None:
        """A child still alive after terminate() is killed with bounded reap joins."""
        queue = _FakeQueue(result=("response", 200, "ok"))
        process = _FakeProcess(alive=True, survives_terminate=True)
        context = _FakeContext(queue, process)

        with (
            patch("agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context),
            patch("agentic_devtools.cli.setup.provider_connectivity.time.monotonic", side_effect=[10.0, 15.0]),
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check timed out after 5.0s")
        assert process.terminated is True
        assert process.killed is True
        assert process.join_calls == [5.0, 0.0, 0.1]

    def test_reports_missing_result_for_nonzero_exitcode(self) -> None:
        """Empty queues with a failing child exit code mention the process exit status."""
        queue = _FakeQueue(empty=True)
        process = _FakeProcess(exitcode=2)
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: probe exited with code 2")

    def test_reports_missing_result_for_clean_exit(self) -> None:
        """Empty queues with a clean exit mention that no result was returned."""
        queue = _FakeQueue(empty=True)
        process = _FakeProcess(exitcode=0)
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: probe returned no result")

    def test_reports_oserror_from_process_setup(self) -> None:
        """Process setup failures are surfaced as non-fatal connectivity errors."""
        queue = _FakeQueue(result=("response", 200, "ok"))
        process = _FakeProcess(start_error=OSError("spawn failed"))
        context = _FakeContext(queue, process)

        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context", return_value=context
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: spawn failed")

    def test_reports_oserror_before_queue_creation(self) -> None:
        """Queue-creation failures still surface as non-fatal connectivity errors."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity.multiprocessing.get_context",
            side_effect=OSError("context failed"),
        ):
            result = _run_jira_probe_with_deadline(
                "https://jira.example.com/rest/api/2/myself",
                {"Authorization": "******"},
                timeout=5.0,
                verify=True,
            )

        assert result == (None, None, "Jira connectivity check failed: context failed")
