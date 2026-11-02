import subprocess

from agentic_devtools.ai_providers.copilot_discovery import _terminate_process


class _Stdin:
    def __init__(self, *, error: Exception | None = None) -> None:
        self._error = error
        self.closed = False

    def close(self) -> None:
        if self._error is not None:
            raise self._error
        self.closed = True


class _Process:
    def __init__(
        self,
        *,
        alive: bool = True,
        wait_error: Exception | None = None,
        stdin: _Stdin | None = None,
        terminate_exits: bool = False,
    ) -> None:
        self.stdin = stdin if stdin is not None else _Stdin()
        self._alive = alive
        self._wait_error = wait_error
        self._terminate_exits = terminate_exits
        self.terminated = False
        self.killed = False
        self.wait_call_count = 0

    def poll(self) -> int | None:
        return None if self._alive else 0

    def terminate(self) -> None:
        self.terminated = True
        if self._terminate_exits:
            self._alive = False

    def wait(self, timeout: float | None = None) -> int:
        self.wait_call_count += 1
        if self._wait_error is not None:
            raise self._wait_error
        return 0

    def kill(self) -> None:
        self.killed = True


def test_closes_stdin_and_terminates_a_running_process() -> None:
    process = _Process()

    _terminate_process(process)

    assert process.stdin.closed is True
    assert process.terminated is True
    assert process.killed is False


def test_leaves_an_already_exited_process_alone() -> None:
    process = _Process(alive=False)

    _terminate_process(process)

    assert process.terminated is False


def test_kills_the_process_when_termination_times_out() -> None:
    process = _Process(wait_error=subprocess.TimeoutExpired(cmd="copilot", timeout=5))

    _terminate_process(process)

    assert process.killed is True


def test_reaps_after_kill_when_termination_times_out() -> None:
    # The post-kill wait(timeout=0.0) must be attempted so the process can be
    # reaped without leaving a zombie.
    process = _Process(wait_error=subprocess.TimeoutExpired(cmd="copilot", timeout=5))

    _terminate_process(process)

    # wait() is called twice: once for the initial terminate (raises TimeoutExpired,
    # triggering the except branch that calls kill()), and once for the post-kill reap.
    assert process.wait_call_count == 2


def test_kills_immediately_when_the_deadline_is_already_exhausted() -> None:
    process = _Process()

    _terminate_process(process, deadline=0.0)

    assert process.killed is True


def test_reaps_after_kill_when_deadline_is_exhausted() -> None:
    # Even when the deadline is exhausted and kill() is used directly, a
    # non-blocking wait(timeout=0.0) must be attempted to reap the process.
    process = _Process()

    _terminate_process(process, deadline=0.0)

    # wait() is called once for the post-kill reap (deadline=0.0 skips the
    # post-terminate wait and goes straight to kill).
    assert process.wait_call_count == 1


def test_swallows_post_kill_reap_failure_in_deadline_exhausted_branch() -> None:
    # If the post-kill wait(timeout=0.0) itself raises (e.g. SIGKILL not yet
    # processed), _terminate_process must not propagate the error.
    process = _Process(wait_error=subprocess.TimeoutExpired(cmd="copilot", timeout=5))

    _terminate_process(process, deadline=0.0)  # must not raise

    assert process.killed is True


def test_skips_kill_when_the_deadline_is_exhausted_but_terminate_already_exited_the_process() -> None:
    process = _Process(terminate_exits=True)

    _terminate_process(process, deadline=0.0)

    assert process.terminated is True
    assert process.killed is False


def test_swallows_teardown_failures() -> None:
    process = _Process(
        stdin=_Stdin(error=ValueError("already closed")),
        wait_error=OSError("gone"),
    )
    process.kill = _raise  # type: ignore[method-assign]

    _terminate_process(process)

    assert process.terminated is True


def test_swallows_post_kill_wait_failure() -> None:
    # If the post-kill wait() itself fails (e.g. the process entry is already
    # gone), _terminate_process must not propagate the error.
    class _FailWaitAfterKill(_Process):
        def wait(self, timeout: float | None = None) -> int:
            self.wait_call_count += 1
            if self.killed:
                raise OSError("no child processes")
            if self._wait_error is not None:
                raise self._wait_error
            return 0

    process = _FailWaitAfterKill(wait_error=subprocess.TimeoutExpired(cmd="copilot", timeout=5))

    _terminate_process(process)  # must not raise

    assert process.killed is True


def _raise() -> None:
    raise OSError("no such process")
