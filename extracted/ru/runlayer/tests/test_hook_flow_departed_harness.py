"""A harness that closed stdout before the hook finished is marked, not skipped.

Cursor fires sessionStart/sessionEnd/afterAgentResponse/... without waiting
for the hook, so a slow hook may find its reader gone before it starts. The
flow records a ``harness_departed`` marker for that cohort and then runs in
full: the event POST is the audit record whoever reads the response, and a
deny must still be attempted. ``harness_closed`` (the write itself failing)
stays a separate marker.
"""

import io
import json
import os
import sys
from collections.abc import Iterator
from typing import TextIO

import pytest

from runlayer_cli import flow_spool, flow_trace
from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io
from runlayer_cli.hook.clients import Client
from runlayer_cli.mdm_config import AIWatchMode


@pytest.fixture(autouse=True)
def _clean_flow_state(monkeypatch, tmp_path):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield tmp_path
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


# pytest's capture reinstalls its own sys.stdout when a test body starts, so
# a fixture cannot install the pipe as the process stdout; each test does the
# ``monkeypatch.setattr(sys, "stdout", ...)`` in-body. Fixtures own descriptors.
@pytest.fixture
def departed_pipe() -> Iterator[io.TextIOWrapper]:
    """Write end of a real pipe whose reader is already gone."""
    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    stdout = io.TextIOWrapper(
        io.FileIO(write_fd, "w", closefd=True), write_through=True
    )
    yield stdout
    try:
        stdout.close()
    except BrokenPipeError:
        pass


@pytest.fixture
def live_pipe() -> Iterator[io.TextIOWrapper]:
    """Write end of a real pipe with the reader still attached."""
    read_fd, write_fd = os.pipe()
    stdout = io.TextIOWrapper(
        io.FileIO(write_fd, "w", closefd=True), write_through=True
    )
    yield stdout
    stdout.close()
    os.close(read_fd)


def _run_hook(
    monkeypatch,
    payload: dict,
    *,
    process_stdout: TextIO,
    client: Client = Client.CURSOR,
    mode: AIWatchMode = AIWatchMode.MONITOR,
    io_overrides: hook_io.HookIO | None = None,
) -> dict[str, list[str]]:
    """Run the hook; return the events each relay stub saw, keyed by stub name."""
    calls: dict[str, list[str]] = {
        "forward_event": [],
        "forward_stop_event": [],
        "check_tool_lifecycle": [],
    }
    monkeypatch.setattr(sys, "stdout", process_stdout)
    monkeypatch.setattr(hook_dispatch, "detect_client", lambda: client)
    monkeypatch.setattr(hook_dispatch, "should_noop_for_cursor", lambda client: False)
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: mode)
    monkeypatch.setattr(
        hook_dispatch,
        "forward_event",
        lambda client, event, *a, **k: calls["forward_event"].append(event),
    )
    monkeypatch.setattr(
        hook_dispatch,
        "forward_stop_event",
        lambda client, event, *a, **k: calls["forward_stop_event"].append(event),
    )

    def _allow(target, client, event, *a, **k):
        calls["check_tool_lifecycle"].append(event)
        return '{"permission":"allow"}'

    monkeypatch.setattr(hook_dispatch, "check_tool_lifecycle", _allow)
    monkeypatch.setattr(hook_dispatch, "start_transcript_stream", lambda *a, **k: True)
    monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with hook_io.scoped(io_overrides or hook_io.HookIO()):
        hook_dispatch.run_hook()
    return calls


def _only_flow() -> dict:
    envelope = flow_spool.spool_drain()
    flows = envelope["flows"] if envelope else []
    assert len(flows) == 1, flows
    return flows[0]


def _steps(flow: dict) -> list[str]:
    return [s["name"] for s in flow["steps"]]


_AFTER_AGENT_RESPONSE = {"hook_event_name": "afterAgentResponse", "session_id": "s1"}
_PRE_TOOL_USE = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Edit",
    "tool_input": {"file_path": "/tmp/x"},
    "session_id": "s2",
}


class TestDepartedHarnessIsMarkedNotSkipped:
    @pytest.mark.parametrize("mode", list(AIWatchMode))
    def test_event_hook_still_posts_in_every_mode(
        self, monkeypatch, departed_pipe, mode
    ):
        # The probe is about the channel, not policy: every mode marks the
        # cohort, and every mode still delivers the event POST.
        calls = _run_hook(
            monkeypatch,
            _AFTER_AGENT_RESPONSE,
            process_stdout=departed_pipe,
            mode=mode,
        )

        assert calls["forward_event"] == ["afterAgentResponse"]
        flow = _only_flow()
        assert flow["operation"] == "cli.hook_event"
        assert flow["status"] == "ok", flow
        # Two distinct cohorts: reader gone before the work (departed) and
        # the "{}" write itself failing afterwards (closed).
        assert _steps(flow)[0] == "harness_departed"
        assert "harness_closed" in _steps(flow)

    def test_stop_hook_still_forwards(self, monkeypatch, departed_pipe):
        calls = _run_hook(
            monkeypatch,
            {"hook_event_name": "Stop", "session_id": "s3"},
            process_stdout=departed_pipe,
        )

        assert calls["forward_stop_event"] == ["Stop"]
        flow = _only_flow()
        assert flow["operation"] == "cli.hook_stop"
        assert "harness_departed" in _steps(flow)

    def test_enforcement_still_consults_the_scanner(self, monkeypatch, departed_pipe):
        calls = _run_hook(
            monkeypatch,
            _PRE_TOOL_USE,
            process_stdout=departed_pipe,
            client=Client.CLAUDE_CODE,
            mode=AIWatchMode.ENFORCE,
        )

        assert calls["check_tool_lifecycle"] == ["PreToolUse"]
        assert calls["forward_event"] == ["PreToolUse"]
        flow = _only_flow()
        assert flow["operation"] == "cli.hook_pre_tool"
        assert flow["status"] == "ok", flow
        assert "harness_departed" in _steps(flow)

    def test_live_harness_has_no_marker(self, monkeypatch, live_pipe):
        calls = _run_hook(monkeypatch, _AFTER_AGENT_RESPONSE, process_stdout=live_pipe)

        assert calls["forward_event"] == ["afterAgentResponse"]
        assert "harness_departed" not in _steps(_only_flow())

    def test_daemon_served_request_ignores_process_stdout(
        self, monkeypatch, departed_pipe
    ):
        # The daemon answers over IPC through its own writer; the process
        # stdout descriptor says nothing about that request's harness.
        request_io = hook_io.HookIO(stdout=io.StringIO(), daemon_served=True)
        calls = _run_hook(
            monkeypatch,
            _AFTER_AGENT_RESPONSE,
            process_stdout=departed_pipe,
            io_overrides=request_io,
        )

        assert calls["forward_event"] == ["afterAgentResponse"]
        assert _steps(_only_flow()) == ["daemon_ipc"]


class TestStdoutReaderGone:
    def test_closed_reader_pipe(self, monkeypatch, departed_pipe):
        monkeypatch.setattr(sys, "stdout", departed_pipe)
        assert hook_io.stdout_reader_gone() is True

    def test_open_pipe(self, monkeypatch, live_pipe):
        monkeypatch.setattr(sys, "stdout", live_pipe)
        assert hook_io.stdout_reader_gone() is False

    def test_tty(self, monkeypatch):
        controller_fd, worker_fd = os.openpty()
        with io.TextIOWrapper(io.FileIO(worker_fd, "w", closefd=True)) as stdout:
            monkeypatch.setattr(sys, "stdout", stdout)
            assert hook_io.stdout_reader_gone() is False
        os.close(controller_fd)

    def test_regular_file(self, monkeypatch, tmp_path):
        with open(tmp_path / "out.txt", "w") as stdout:
            monkeypatch.setattr(sys, "stdout", stdout)
            assert hook_io.stdout_reader_gone() is False

    def test_stream_without_descriptor(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", io.StringIO())
        assert hook_io.stdout_reader_gone() is False

    def test_request_local_writer_wins(self, monkeypatch, departed_pipe):
        monkeypatch.setattr(sys, "stdout", departed_pipe)
        with hook_io.scoped(hook_io.HookIO(stdout=io.StringIO())):
            assert hook_io.stdout_reader_gone() is False

    def test_windows_never_reports_gone(self, monkeypatch, departed_pipe):
        monkeypatch.setattr(sys, "stdout", departed_pipe)
        monkeypatch.setattr(sys, "platform", "win32")
        assert hook_io.stdout_reader_gone() is False

    def test_poll_failure_reports_alive(self, monkeypatch, departed_pipe):
        monkeypatch.setattr(sys, "stdout", departed_pipe)
        monkeypatch.setattr(
            hook_io.select, "poll", lambda: (_ for _ in ()).throw(OSError())
        )
        assert hook_io.stdout_reader_gone() is False
