"""Cursor fire-and-forget hooks close stdout before the hook writes its response.

A hook whose harness has already gone away is not a hook failure: the flow
must not spool ``status="error"`` for it, and the abandoned process must not
print a traceback on its way out. Linear: PLA-1605.
"""

import errno
import io
import json
import os
import sys
from typing import TextIO, cast

import pytest

from runlayer_cli import aiwatch, flow_spool, flow_trace
from runlayer_cli.hook import daemon_client
from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io
from runlayer_cli.hook.clients import Client, HookResponse
from runlayer_cli.mdm_config import AIWatchMode


@pytest.fixture(autouse=True)
def _clean_flow_state(monkeypatch, tmp_path):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield tmp_path
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def _closed_reader_pipe_fd() -> int:
    """Write end of a real pipe whose read end is already closed: writes raise EPIPE."""
    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    return write_fd


def _closed_reader_stdout() -> io.TextIOWrapper:
    return io.TextIOWrapper(
        io.FileIO(_closed_reader_pipe_fd(), "w", closefd=True), write_through=True
    )


def _closed_reader_process_stdout() -> tuple[io.TextIOWrapper, int]:
    """Block-buffered like a real piped ``sys.stdout``; returns (stream, fd)."""
    write_fd = _closed_reader_pipe_fd()
    raw = io.FileIO(write_fd, "w", closefd=True)
    return io.TextIOWrapper(io.BufferedWriter(raw)), write_fd


def _assert_fd_is_devnull(fd: int) -> None:
    devnull_stat = os.stat(os.devnull)
    fd_stat = os.fstat(fd)
    assert (fd_stat.st_dev, fd_stat.st_ino) == (
        devnull_stat.st_dev,
        devnull_stat.st_ino,
    )


class _FailingWriter(io.StringIO):
    """stdout stand-in whose write fails with a non-pipe OS error."""

    def write(self, value: str) -> int:
        raise OSError(errno.EIO, "disk on fire")


def _run_cursor_hook(
    monkeypatch,
    stdout: TextIO,
    payload: dict,
    *,
    stderr: TextIO | None = None,
) -> None:
    monkeypatch.setattr(hook_dispatch, "detect_client", lambda: Client.CURSOR)
    monkeypatch.setattr(hook_dispatch, "should_noop_for_cursor", lambda client: False)
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: AIWatchMode.ENFORCE)
    monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **k: None)
    monkeypatch.setattr(hook_dispatch, "start_transcript_stream", lambda *a, **k: True)
    monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
    request_io = hook_io.HookIO(
        stdin_text=json.dumps(payload), stdout=stdout, stderr=stderr
    )
    with hook_io.scoped(request_io):
        hook_dispatch.run_hook()


def _run_observational_hook(monkeypatch, stdout: TextIO) -> None:
    # Cursor observational event: reaches _handle_unknown_event, which writes
    # resp.observational() == "{}" to stdout after the event POST.
    payload = {"hook_event_name": "afterAgentResponse", "session_id": "sess-epipe"}
    _run_cursor_hook(monkeypatch, stdout, payload)


def _spooled_flows() -> list[dict]:
    envelope = flow_spool.spool_drain()
    return envelope["flows"] if envelope else []


def test_harness_closed_stdout_is_not_a_hook_failure(monkeypatch):
    stdout = _closed_reader_stdout()
    _run_observational_hook(monkeypatch, stdout)
    stdout.close()

    flows = _spooled_flows()
    assert len(flows) == 1
    flow = flows[0]
    assert flow["operation"] == "cli.hook_event"
    assert flow["status"] == "ok", flow
    assert all(step["status"] == "ok" for step in flow["steps"])
    assert "harness_closed" in [step["name"] for step in flow["steps"]]


def test_deny_to_closed_stdout_is_quiet_and_keeps_client_exit_code(monkeypatch):
    # A deny nobody reads still exits with the client's deny code (a harness
    # that stopped reading may still honour it), writes nothing to stderr, and
    # the flow keeps the policy step as an ok outcome plus the harness marker.
    stdout = _closed_reader_stdout()
    stderr = io.StringIO()
    payload = {"hook_event_name": "beforeShellExecution", "command": "cat .env"}
    with pytest.raises(SystemExit) as exc_info:
        _run_cursor_hook(monkeypatch, stdout, payload, stderr=stderr)
    stdout.close()

    expected_code = HookResponse(Client.CURSOR, "beforeShellExecution").deny_exit_code()
    assert exc_info.value.code == expected_code
    assert stderr.getvalue() == ""
    flows = _spooled_flows()
    assert len(flows) == 1
    flow = flows[0]
    assert flow["status"] == "ok", flow
    assert [s["name"] for s in flow["steps"]] == ["policy_check", "harness_closed"]
    assert all(step["status"] == "ok" for step in flow["steps"])


def test_other_stdout_os_errors_still_fail_the_flow(monkeypatch):
    # Only the "reader is gone" errors are absorbed; anything else is a real
    # failure and must keep surfacing as one.
    with pytest.raises(OSError) as exc_info:
        _run_observational_hook(monkeypatch, cast(TextIO, _FailingWriter()))

    assert exc_info.value.errno == errno.EIO
    flows = _spooled_flows()
    assert len(flows) == 1
    assert flows[0]["status"] == "error"
    assert flows[0]["error_type"] == "OSError"
    assert "harness_closed" not in [s["name"] for s in flows[0]["steps"]]


def test_process_stdout_fd_is_parked_on_devnull_after_closed_pipe(monkeypatch):
    # Without a request-local writer the process stdout descriptor itself is
    # redirected, so the interpreter's exit-time flush of the still-buffered
    # response succeeds instead of printing "Exception ignored" to stderr.
    stdout, write_fd = _closed_reader_process_stdout()
    monkeypatch.setattr(sys, "stdout", stdout)
    flow_trace.enable_flow_tracing(flow_spool.spool_append)

    with flow_trace.flow("cli.hook_event"):
        hook_dispatch._write("{}")

    _assert_fd_is_devnull(write_fd)
    stdout.close()  # the block-buffered "{}" drains into devnull without raising
    flows = _spooled_flows()
    assert [s["name"] for s in flows[0]["steps"]] == ["harness_closed"]
    assert flows[0]["status"] == "ok"


def test_custom_writer_leaves_process_stdout_alone(monkeypatch):
    stdout = _closed_reader_stdout()
    calls: list[int] = []
    monkeypatch.setattr(os, "dup2", lambda *a: calls.append(1))
    with hook_io.scoped(hook_io.HookIO(stdout=stdout)):
        hook_dispatch._write("{}")
    stdout.close()
    assert calls == []


@pytest.mark.parametrize("exit_code", [0, 2])
def test_daemon_response_relay_to_closed_stdout_is_quiet(monkeypatch, exit_code):
    # The thin client replays the daemon's response through the real process
    # stdout; a harness that already left must not turn that into a traceback,
    # and the daemon's exit code is replayed unchanged.
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.setattr(
        daemon_client,
        "try_daemon_hook",
        lambda *_a, **_k: {"stdout": "{}", "stderr": "", "exit_code": exit_code},
    )
    monkeypatch.setattr(aiwatch.sys, "stdin", io.StringIO("request"))
    stdout, write_fd = _closed_reader_process_stdout()
    stderr = io.StringIO()
    monkeypatch.setattr(aiwatch.sys, "stdout", stdout)
    monkeypatch.setattr(aiwatch.sys, "stderr", stderr)

    with pytest.raises(SystemExit) as exc_info:
        aiwatch._run_hook_daemon_first()

    assert exc_info.value.code == exit_code
    assert stderr.getvalue() == ""
    _assert_fd_is_devnull(write_fd)
    stdout.close()


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        (BrokenPipeError(errno.EPIPE, "pipe"), True),
        (ConnectionResetError(errno.ECONNRESET, "reset"), True),
        (OSError(errno.EIO, "io"), False),
    ],
)
@pytest.mark.parametrize("platform", ["darwin", "linux", "win32"])
def test_harness_gone_classification(monkeypatch, platform, exc, expected):
    monkeypatch.setattr(sys, "platform", platform)
    assert hook_io.harness_gone(exc) is expected


@pytest.mark.parametrize(
    ("platform", "expected"), [("win32", True), ("darwin", False), ("linux", False)]
)
def test_harness_gone_einval_only_counts_on_windows(monkeypatch, platform, expected):
    # Windows has no SIGPIPE; a pipe whose reader exited surfaces as EINVAL
    # there, while on POSIX EINVAL is a programming error that must raise.
    monkeypatch.setattr(sys, "platform", platform)
    assert hook_io.harness_gone(OSError(errno.EINVAL, "invalid")) is expected
