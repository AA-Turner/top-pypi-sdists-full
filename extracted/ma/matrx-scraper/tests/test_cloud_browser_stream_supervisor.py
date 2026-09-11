"""SelkiesSupervisor — the human-control stream's process lifecycle.

SUT: `SelkiesSupervisor` (`start` / `stop`). It OWNS: launching Selkies in a
private process group, not reporting ready before the listener accepts,
failing closed (and cleaning up) when startup fails, never double-launching,
and tearing down the WHOLE group — SIGTERM, then SIGKILL after a bounded wait.
Doubled where the OS would make a unit test slow or dangerous: Popen, killpg,
the socket, and the clock. One test runs a REAL process with no doubles.
"""

from __future__ import annotations

import shutil
import signal
import socket
import subprocess
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor

MOD = "matrx_scraper.cloud_browser.streaming.supervisor"


def _live_launcher(pid: int) -> Mock:
    process = Mock(spec=subprocess.Popen)
    process.pid = pid
    process.poll.return_value = None
    process.wait.return_value = 0
    return process


@contextmanager
def _os(process: Mock, *, connect: Any = None, monotonic: Any = None) -> Iterator[SimpleNamespace]:
    with ExitStack() as stack:
        connect_kwargs: dict[str, Any] = (
            {"side_effect": connect} if connect is not None else {"return_value": MagicMock()}
        )
        doubles = SimpleNamespace(
            popen=stack.enter_context(patch(f"{MOD}.subprocess.Popen", return_value=process)),
            connect=stack.enter_context(patch(f"{MOD}.socket.create_connection", **connect_kwargs)),
            killpg=stack.enter_context(patch(f"{MOD}.os.killpg")),
            sleep=stack.enter_context(patch(f"{MOD}.time.sleep")),
        )
        if monotonic is not None:
            stack.enter_context(patch(f"{MOD}.time.monotonic", side_effect=monotonic))
        yield doubles


def test_stop_terminates_the_launcher_process_group_not_just_the_wrapper() -> None:
    process = _live_launcher(4242)

    with _os(process) as os_:
        supervisor = SelkiesSupervisor()
        supervisor.start()
        supervisor.stop()

    assert os_.popen.call_args.kwargs["start_new_session"] is True
    os_.killpg.assert_called_once_with(4242, signal.SIGTERM)
    # The graceful wait is bounded — stop() can never hang on a stuck stream.
    assert process.wait.call_args.kwargs["timeout"] > 0
    assert supervisor.running is False


def test_a_group_that_ignores_sigterm_is_killed_after_the_bounded_wait() -> None:
    process = _live_launcher(4343)
    process.wait.side_effect = [subprocess.TimeoutExpired("selkies", 0.75), 0]

    with _os(process) as os_:
        supervisor = SelkiesSupervisor()
        supervisor.start()
        supervisor.stop()

    assert os_.killpg.call_args_list == [call(4343, signal.SIGTERM), call(4343, signal.SIGKILL)]


def test_start_does_not_return_until_the_listener_accepts() -> None:
    process = _live_launcher(4444)

    with _os(process, connect=[ConnectionRefusedError(), MagicMock()]) as os_:
        supervisor = SelkiesSupervisor()
        supervisor.start()

    assert os_.connect.call_count == 2
    assert os_.sleep.call_count == 1  # backed off between probes, never a busy loop
    assert supervisor.running is True


def test_startup_fails_closed_and_tears_down_when_the_listener_never_accepts() -> None:
    process = _live_launcher(4545)

    with _os(process, connect=socket.timeout, monotonic=[0.0, 1.0, 9.0]) as os_:
        supervisor = SelkiesSupervisor()
        with pytest.raises(RuntimeError, match="did not become ready during startup"):
            supervisor.start()

    os_.killpg.assert_called_once_with(4545, signal.SIGTERM)
    assert supervisor.running is False


def test_a_second_start_while_streaming_does_not_launch_another_process() -> None:
    """Break: a second takeover spawns a second Selkies that collides on the port."""
    process = _live_launcher(4646)

    with _os(process) as os_:
        supervisor = SelkiesSupervisor()
        supervisor.start()
        supervisor.start()

    assert os_.popen.call_count == 1


def test_stop_after_the_stream_already_exited_sends_no_signal() -> None:
    """Break: stop() signals a group that no longer exists (or a recycled pgid)."""
    process = _live_launcher(4747)

    with _os(process) as os_:
        supervisor = SelkiesSupervisor()
        supervisor.start()
        process.poll.return_value = 0  # the stream exited on its own
        supervisor.stop()

    os_.killpg.assert_not_called()
    assert supervisor.running is False


def _unused_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def test_a_launcher_that_dies_during_startup_is_reported_as_a_startup_failure() -> None:
    """Real OS, no doubles. Break (found 2026-09-10): the dead launcher's group is
    already reaped by poll(), so the cleanup `killpg` raised ProcessLookupError
    and masked the real startup failure from the caller."""
    executable = shutil.which("false")
    assert executable, "this proof needs a `false` executable on PATH"
    supervisor = SelkiesSupervisor(
        executable=executable,
        port=_unused_local_port(),
        startup_timeout_seconds=2.0,
    )

    outcome: BaseException | None = None
    try:
        supervisor.start()
    except Exception as exc:  # noqa: BLE001 — the TYPE of what escaped is the assertion
        outcome = exc

    assert isinstance(outcome, RuntimeError) and "failed during startup" in str(outcome), (
        f"a launcher that exited during startup surfaced as {type(outcome).__name__}: "
        f"{outcome} — the real startup failure is masked"
    )
    assert supervisor.running is False
