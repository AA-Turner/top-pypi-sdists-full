"""Tests for local tool execution spooling."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from plato.utils.tool_execution import (
    ActiveToolExecution,
    PendingToolExecution,
    ToolExecutionContext,
    ToolExecutionRecorder,
    ToolExecutionScope,
    ToolExecutionStatus,
    ToolStartRecord,
    append_tool_start_record,
    close_tool_execution,
    load_tool_execution_context,
    open_tool_execution,
    parse_tool_execution_records,
    tool_execution_spool_path,
)


def test_load_tool_execution_context_round_trip(tmp_path: Path) -> None:
    context = ToolExecutionContext(
        session_id="sess-123",
        agent_id="agent-123",
        agent_name="gemini-cli",
        display_name="Gemini CLI",
        spool_path=str(tmp_path / "tool-executions.jsonl"),
        scopes=[
            ToolExecutionScope(
                workspace_name="code",
                mount_path="/workspace/code",
                audit_run_id="run-123",
                audit_key="audit-key-123",
            )
        ],
    )
    context_path = tmp_path / "tool-context.json"
    context_path.write_text(context.model_dump_json(), encoding="utf-8")

    loaded = load_tool_execution_context(context_path)

    assert loaded == context


def test_append_and_parse_tool_execution_records(tmp_path: Path) -> None:
    record_time = datetime.now(UTC)
    spool_path = tmp_path / "tool-executions.jsonl"
    ToolExecutionRecorder(ToolExecutionContext(spool_path=str(spool_path))).finish(
        ActiveToolExecution(
            trace_id="t" * 32,
            span_id="s" * 16,
            tool_name="run_shell_command",
            started_at=record_time,
            command="cat /workspace/code/a.txt",
            path_hints=["/workspace/code/a.txt"],
            working_directory="/workspace/code",
            agent_id="agent-1",
        ),
        status=ToolExecutionStatus.COMPLETED,
    )

    parsed = parse_tool_execution_records(spool_path.read_text(encoding="utf-8"))

    assert len(parsed) == 1
    assert parsed[0].tool_name == "run_shell_command"
    assert parsed[0].command == "cat /workspace/code/a.txt"
    assert parsed[0].path_hints == ["/workspace/code/a.txt"]


def test_tool_execution_spool_path_layout(tmp_path: Path) -> None:
    path = tool_execution_spool_path(
        tmp_path / ".plato",
        workspace_name="code",
        audit_run_id="run-123",
    )

    assert path == tmp_path / ".plato" / "tool-execution" / "code" / "run-123.jsonl"


def test_recorder_start_captures_span_identity() -> None:
    fake_span = MagicMock()
    fake_context = MagicMock()
    fake_context.trace_id = int("1" * 32, 16)
    fake_context.span_id = int("2" * 16, 16)
    fake_span.get_span_context.return_value = fake_context

    recorder = ToolExecutionRecorder(ToolExecutionContext(agent_id="agent-1"))
    active = recorder.start(
        fake_span,
        tool_name="Read",
        path_hints=["/workspace/code/a.txt"],
        working_directory="/workspace/code",
    )

    assert active.trace_id == "1" * 32
    assert active.span_id == "2" * 16
    assert active.tool_name == "Read"


def test_open_tool_execution_registers_pending_execution() -> None:
    recorder = MagicMock(spec=ToolExecutionRecorder)
    fake_span = MagicMock()
    active = ActiveToolExecution(
        trace_id="t" * 32,
        span_id="s" * 16,
        tool_name="Read",
        started_at=datetime.now(UTC),
    )
    recorder.start.return_value = active
    pending_tool_executions: dict[str, PendingToolExecution] = {}

    @contextmanager
    def fake_start_tool_step_span(*args, **kwargs):
        del args, kwargs
        yield fake_span

    with patch(
        "plato.utils.tool_execution.start_tool_step_span",
        fake_start_tool_step_span,
    ):
        pending_execution = open_tool_execution(
            tracer=MagicMock(),
            step_id=7,
            tool_id="tool-1",
            tool_name="Read",
            tool_arguments={"file_path": "/workspace/a.txt"},
            model_name="anthropic/test-model",
            pending_tool_executions=pending_tool_executions,
            recorder=recorder,
            path_hints=["/workspace/a.txt"],
            working_directory="/workspace",
        )

    assert pending_tool_executions["tool-1"] == pending_execution
    recorder.start.assert_called_once_with(
        fake_span,
        tool_name="Read",
        started_at=None,
        command=None,
        path_hints=["/workspace/a.txt"],
        working_directory="/workspace",
    )


def test_close_tool_execution_returns_original_step_id() -> None:
    recorder = MagicMock(spec=ToolExecutionRecorder)
    active = ActiveToolExecution(
        trace_id="t" * 32,
        span_id="s" * 16,
        tool_name="Read",
        started_at=datetime.now(UTC),
    )
    pending_tool_executions = {
        "tool-1": PendingToolExecution(
            execution=active,
            step_id=9,
            tool_name="Read",
        )
    }

    step_id = close_tool_execution(
        "tool-1",
        status=ToolExecutionStatus.COMPLETED,
        pending_tool_executions=pending_tool_executions,
        recorder=recorder,
    )

    assert step_id == 9
    assert pending_tool_executions == {}
    recorder.finish.assert_called_once_with(
        active,
        status=ToolExecutionStatus.COMPLETED,
        pid=None,
        child_pids=None,
    )


def test_close_tool_execution_with_none_recorder() -> None:
    """close_tool_execution must not crash when recorder is None."""
    active = ActiveToolExecution(
        trace_id="t" * 32,
        span_id="s" * 16,
        tool_name="Bash",
        started_at=datetime.now(UTC),
    )
    pending_tool_executions = {
        "tool-1": PendingToolExecution(
            execution=active,
            step_id=3,
            tool_name="Bash",
        )
    }

    step_id = close_tool_execution(
        "tool-1",
        status=ToolExecutionStatus.ABORTED,
        pending_tool_executions=pending_tool_executions,
        recorder=None,
    )

    assert step_id == 3
    assert pending_tool_executions == {}


def test_recorder_consumes_matching_hook_record(tmp_path: Path) -> None:
    hook_spool_path = tmp_path / "tool-starts.jsonl"
    append_tool_start_record(
        hook_spool_path,
        ToolStartRecord(
            source="claude-pretooluse",
            observed_at=datetime.now(UTC),
            tool_name="Read",
            normalized_tool_input='{"file_path":"/workspace/a.txt"}',
            tool_use_id="tool-1",
        ),
    )
    recorder = ToolExecutionRecorder(ToolExecutionContext(hook_spool_path=str(hook_spool_path)))

    record = recorder.consume_start_record(tool_use_id="tool-1")

    assert record is not None
    assert record.tool_name == "Read"
    assert hook_spool_path.read_text(encoding="utf-8") == ""
