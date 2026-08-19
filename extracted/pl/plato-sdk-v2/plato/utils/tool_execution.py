"""Typed local spool helpers for tool execution attribution."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from opentelemetry.trace import Span, Tracer
from pydantic import BaseModel, Field

from plato.otel import start_step_span

DEFAULT_TOOL_EXECUTION_CONTEXT_PATH = Path("/tmp/plato-tool-execution-context.json")
DEFAULT_TOOL_EXECUTION_SPOOL_PATH = Path("/tmp/plato-tool-executions.jsonl")
DEFAULT_TOOL_START_SPOOL_PATH = Path("/tmp/plato-tool-starts.jsonl")

# Env var carrying the absolute path (inside the agent VM) the post-compaction
# hook writes the summary to. Set by the agent runner from the
# ``compaction_summary_path`` config field; unset means the hook is a no-op.
# Shared by the claude-code PostCompact hook and the opencode compaction plugin.
COMPACTION_SUMMARY_PATH_ENV = "PLATO_COMPACTION_SUMMARY_PATH"

logger = logging.getLogger(__name__)


class ToolExecutionStatus(StrEnum):
    """Lifecycle status for one completed tool execution."""

    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class ToolExecutionScope(BaseModel):
    """One tracked workspace scope available to the running agent."""

    workspace_name: str
    mount_path: str
    audit_run_id: str
    audit_key: str


class ToolExecutionContext(BaseModel):
    """Agent-local context for recording tool execution spans."""

    session_id: str = ""
    agent_id: str = ""
    agent_name: str = ""
    display_name: str = ""
    trace_id: str = ""
    span_id: str = ""
    spool_path: str = str(DEFAULT_TOOL_EXECUTION_SPOOL_PATH)
    hook_spool_path: str = str(DEFAULT_TOOL_START_SPOOL_PATH)
    scopes: list[ToolExecutionScope] = Field(default_factory=list)


class ActiveToolExecution(BaseModel):
    """In-memory state for a tool execution that has started but not finished."""

    trace_id: str
    span_id: str
    tool_name: str
    started_at: datetime
    command: str | None = None
    path_hints: list[str] = Field(default_factory=list)
    working_directory: str | None = None
    agent_id: str | None = None
    agent_name: str | None = None
    display_name: str | None = None


class PendingToolExecution(BaseModel):
    """Pending tool execution paired from start to completion."""

    execution: ActiveToolExecution | None = None
    step_id: int
    tool_name: str
    # Identity of the ATIF tool step span (lowercase hex), captured so callers
    # can parent related spans (e.g. a sub-agent spawned by this Task call)
    # under the tool span itself.
    trace_id: str | None = None
    span_id: str | None = None


class ToolExecutionRecord(BaseModel):
    """Completed tool execution record written to the local JSONL spool."""

    trace_id: str
    span_id: str
    tool_name: str
    started_at: datetime
    ended_at: datetime
    status: ToolExecutionStatus
    command: str | None = None
    path_hints: list[str] = Field(default_factory=list)
    working_directory: str | None = None
    pid: int | None = None
    child_pids: list[int] = Field(default_factory=list)
    agent_id: str | None = None
    agent_name: str | None = None
    display_name: str | None = None


class ToolStartRecord(BaseModel):
    """Pre-tool sidecar record emitted by CLI hook surfaces."""

    source: str
    observed_at: datetime
    tool_name: str
    normalized_tool_input: str
    tool_use_id: str | None = None
    session_id: str = ""
    transcript_path: str = ""
    cwd: str = ""


class ToolExecutionRecorderLike(Protocol):
    """Shared protocol for agent adapters that record tool execution windows."""

    def start(
        self,
        span: Span,
        *,
        tool_name: str,
        started_at: datetime | None = None,
        command: str | None = None,
        path_hints: list[str] | None = None,
        working_directory: str | None = None,
    ) -> ActiveToolExecution: ...

    def finish(
        self,
        active: ActiveToolExecution,
        *,
        status: ToolExecutionStatus,
        pid: int | None = None,
        child_pids: list[int] | None = None,
    ) -> ToolExecutionRecord | None: ...


start_tool_step_span = start_step_span

MCP_TOOL_ORIGIN = "mcp"
"""Value of ``origin`` on ``atif.step.tool_calls[]`` for remote MCP invocations.

Harness builtins (Bash, Read, Write, ``command_execution``, …) omit ``origin``.
"""


def claude_mcp_tool_origin(tool_name: str) -> tuple[str | None, str | None]:
    """Return ``(origin, mcp_server)`` for a Claude Code tool name.

    Remote MCP tools are named ``mcp__{server}__{tool}``. Harness meta-tools
    such as ``ListMcpResourcesTool`` are not remote MCP calls.
    """
    if not tool_name.startswith("mcp__"):
        return None, None
    parts = tool_name.split("__")
    if len(parts) < 3 or not parts[1]:
        return None, None
    return MCP_TOOL_ORIGIN, parts[1]


def opencode_mcp_server(
    tool_name: str,
    mcp_servers: Mapping[str, object] | None,
    *,
    part: Mapping[str, object] | None = None,
) -> str | None:
    """Return the MCP server name for an OpenCode tool part, if any.

    Prefers an explicit ``mcp`` / ``server`` field on the part, then matches
    OpenCode's ``{server}_{tool}`` prefix against configured ``mcp_servers``
    (longest name wins).
    """
    if part is not None:
        for key in ("mcp", "server"):
            value = part.get(key)
            if isinstance(value, str) and value:
                return value
            if isinstance(value, dict):
                as_map = {str(k): v for k, v in value.items()}
                nested = as_map.get("name") or as_map.get("server")
                if isinstance(nested, str) and nested:
                    return nested
    if not mcp_servers or not tool_name:
        return None
    best: str | None = None
    for name in mcp_servers:
        if not isinstance(name, str):
            continue
        if tool_name != name and not tool_name.startswith(f"{name}_"):
            continue
        if best is None or len(name) > len(best):
            best = name
    return best


def tool_call_payload(
    *,
    tool_call_id: str,
    function_name: str,
    arguments: object,
    origin: str | None = None,
    mcp_server: str | None = None,
) -> dict[str, object]:
    """Build one ATIF ``tool_calls[]`` entry, adding MCP attrs when present."""
    payload: dict[str, object] = {
        "tool_call_id": tool_call_id,
        "function_name": function_name,
        "arguments": arguments,
    }
    if origin:
        payload["origin"] = origin
    if mcp_server:
        payload["mcp_server"] = mcp_server
    return payload


def update_tool_execution_context_trace(
    trace_id: str,
    span_id: str,
    path: Path = DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
) -> None:
    """Update the on-disk tool execution context with a new parent span.

    Lets the agent process re-anchor the parent context after opening its own
    deeper spans (e.g. a ``session`` span) so out-of-band hooks reading this
    file emit spans nested inside the agent's subtree rather than at the
    agent.task level.
    """
    if not path.exists():
        return
    try:
        context = ToolExecutionContext.model_validate_json(path.read_text())
    except Exception:
        logger.warning("Failed to load context for span update at %s", path)
        return
    context.trace_id = trace_id
    context.span_id = span_id
    path.write_text(context.model_dump_json())


def load_tool_execution_context(
    path: Path = DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
) -> ToolExecutionContext | None:
    """Load tool execution context from disk when available."""
    if not path.exists():
        logger.debug("Tool execution context missing at %s", path)
        return None
    context = ToolExecutionContext.model_validate_json(path.read_text())
    logger.debug(
        "Loaded tool execution context from %s: agent_id=%s spool_path=%s scopes=%s",
        path,
        context.agent_id,
        context.spool_path,
        [
            {
                "workspace_name": scope.workspace_name,
                "mount_path": scope.mount_path,
                "audit_run_id": scope.audit_run_id,
            }
            for scope in context.scopes
        ],
    )
    return context


def iter_tool_execution_records(spool_path: Path) -> list[ToolExecutionRecord]:
    """Read all completed tool execution records from a JSONL spool file."""
    if not spool_path.exists():
        return []
    return parse_tool_execution_records(spool_path.read_text(encoding="utf-8"))


def normalize_tool_input(tool_input: object) -> str:
    """Return a deterministic JSON representation for tool input matching."""
    return json.dumps(tool_input, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def build_tool_execution_hook_command(mode: str) -> str:
    """Return the shell command used by CLI hooks to record pre-tool metadata."""
    return f"python3 -m plato.utils.tool_execution_hook {mode}"


def build_compaction_summary_hook_command() -> str:
    """Return the shell command for the Claude Code ``PostCompact`` hook.

    Reads the hook payload (with ``compact_summary``) on stdin and persists it
    to ``$PLATO_COMPACTION_SUMMARY_PATH``. See
    :func:`plato.utils.tool_execution_hook._handle_claude_postcompact`.
    """
    return build_tool_execution_hook_command("claude-postcompact")


def tool_execution_spool_path(
    plato_dir: Path,
    *,
    workspace_name: str,
    audit_run_id: str,
) -> Path:
    """Return the persisted workspace-local JSONL spool path for one audit scope."""
    normalized_workspace_name = workspace_name or "unknown-workspace"
    return plato_dir / "tool-execution" / normalized_workspace_name / f"{audit_run_id}.jsonl"


def parse_tool_execution_records(raw_text: str) -> list[ToolExecutionRecord]:
    """Parse JSONL text into completed tool execution records."""
    records: list[ToolExecutionRecord] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(ToolExecutionRecord.model_validate_json(line))
    return records


def parse_tool_start_records(raw_text: str) -> list[ToolStartRecord]:
    """Parse JSONL text into pre-tool start records."""
    records: list[ToolStartRecord] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(ToolStartRecord.model_validate_json(line))
    return records


def append_tool_start_record(
    spool_path: Path,
    record: ToolStartRecord,
) -> None:
    """Append one pre-tool sidecar record to the local JSONL spool."""
    spool_path.parent.mkdir(parents=True, exist_ok=True)
    with spool_path.open("a", encoding="utf-8") as handle:
        handle.write(record.model_dump_json())
        handle.write("\n")


def append_tool_execution_record(
    spool_path: Path,
    record: ToolExecutionRecord,
) -> None:
    """Append one completed tool execution record to the JSONL spool."""
    spool_path.parent.mkdir(parents=True, exist_ok=True)
    with spool_path.open("a", encoding="utf-8") as handle:
        handle.write(record.model_dump_json())
        handle.write("\n")
    logger.debug(
        "Appended tool execution record to %s: tool_name=%s span_id=%s pid=%s",
        spool_path,
        record.tool_name,
        record.span_id,
        record.pid,
    )


def write_tool_execution_records(
    spool_path: Path,
    records: list[ToolExecutionRecord],
) -> None:
    """Write a full JSONL spool for completed tool execution records."""
    spool_path.parent.mkdir(parents=True, exist_ok=True)
    with spool_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(record.model_dump_json())
            handle.write("\n")


def open_tool_execution(
    *,
    tracer: Tracer,
    step_id: int,
    tool_id: str,
    tool_name: str,
    tool_arguments: object,
    model_name: str,
    pending_tool_executions: dict[str, PendingToolExecution] | None = None,
    recorder: ToolExecutionRecorderLike | None = None,
    started_at: datetime | None = None,
    command: str | None = None,
    path_hints: list[str] | None = None,
    working_directory: str | None = None,
    span_kwargs: dict[str, object] | None = None,
    tool_span: Span | None = None,
    origin: str | None = None,
    mcp_server: str | None = None,
) -> PendingToolExecution:
    """Open a shared ATIF tool span and register the pending execution.

    When ``tool_span`` is provided, the caller created the span and owns its
    lifecycle (deferred-export path: the span is finished later, once
    late-resolving usage lands); only the recorder/registration wiring runs
    here. Otherwise a span is created and ended immediately.

    ``origin`` / ``mcp_server`` are copied onto the ATIF ``tool_calls[]``
    entry so MCP invocations are distinguishable from harness builtins.
    """

    def _register(span: Span) -> PendingToolExecution:
        pending_execution = PendingToolExecution(
            execution=(
                recorder.start(
                    span,
                    tool_name=tool_name,
                    started_at=started_at,
                    command=command,
                    path_hints=path_hints,
                    working_directory=working_directory,
                )
                if recorder is not None
                else None
            ),
            step_id=step_id,
            tool_name=tool_name,
            trace_id=_maybe_span_trace_id(span),
            span_id=_maybe_span_span_id(span),
        )
        if pending_tool_executions is not None:
            pending_tool_executions[tool_id] = pending_execution
        return pending_execution

    if tool_span is not None:
        return _register(tool_span)

    with start_tool_step_span(
        tracer,
        step_id=step_id,
        source="agent",
        message="",
        model_name=model_name,
        tool_calls=[
            tool_call_payload(
                tool_call_id=tool_id,
                function_name=tool_name,
                arguments=tool_arguments,
                origin=origin,
                mcp_server=mcp_server,
            )
        ],
        **(span_kwargs or {}),  # type: ignore[arg-type]  # dynamic kwargs forwarded to start_step_span
    ) as span:
        return _register(span)


def close_tool_execution(
    tool_id: str,
    *,
    status: ToolExecutionStatus,
    pending_tool_executions: dict[str, PendingToolExecution],
    recorder: ToolExecutionRecorderLike | None = None,
    pid: int | None = None,
    child_pids: list[int] | None = None,
) -> int | None:
    """Finish a pending execution and return its originating ATIF step ID."""
    pending_execution = pending_tool_executions.pop(tool_id, None)
    if pending_execution is None:
        return None
    if recorder is not None and pending_execution.execution is not None:
        recorder.finish(
            pending_execution.execution,
            status=status,
            pid=pid,
            child_pids=child_pids,
        )
    return pending_execution.step_id


def span_trace_id(span: Span) -> str:
    """Return the current span's trace ID as a lowercase hex string."""
    return format(span.get_span_context().trace_id, "032x")


def span_span_id(span: Span) -> str:
    """Return the current span's span ID as a lowercase hex string."""
    return format(span.get_span_context().span_id, "016x")


def _maybe_span_trace_id(span: Span) -> str | None:
    """``span_trace_id`` that tolerates non-recording/test-double spans."""
    try:
        return span_trace_id(span)
    except (TypeError, ValueError, AttributeError):
        return None


def _maybe_span_span_id(span: Span) -> str | None:
    """``span_span_id`` that tolerates non-recording/test-double spans."""
    try:
        return span_span_id(span)
    except (TypeError, ValueError, AttributeError):
        return None


class ToolExecutionRecorder:
    """Recorder that writes completed tool execution windows to JSONL."""

    def __init__(self, context: ToolExecutionContext | None):
        self._context = context
        self._spool_path = Path(context.spool_path) if context is not None else None
        self._hook_spool_path = Path(context.hook_spool_path) if context is not None else None

    @classmethod
    def from_default_context(cls) -> ToolExecutionRecorder:
        """Build a recorder from the default agent-local context file."""
        return cls(load_tool_execution_context())

    @property
    def enabled(self) -> bool:
        """Whether recording is enabled for the current agent process."""
        return self._context is not None and self._spool_path is not None

    def start(
        self,
        span: Span,
        *,
        tool_name: str,
        started_at: datetime | None = None,
        command: str | None = None,
        path_hints: list[str] | None = None,
        working_directory: str | None = None,
    ) -> ActiveToolExecution:
        """Capture live span identity and open a pending tool execution."""
        active = ActiveToolExecution(
            trace_id=span_trace_id(span),
            span_id=span_span_id(span),
            tool_name=tool_name,
            started_at=started_at or datetime.now(UTC),
            command=command,
            path_hints=path_hints or [],
            working_directory=working_directory,
            agent_id=self._context.agent_id if self._context is not None else None,
            agent_name=self._context.agent_name if self._context is not None else None,
            display_name=self._context.display_name if self._context is not None else None,
        )
        logger.debug(
            "Starting tool execution: tool_name=%s span_id=%s",
            tool_name,
            active.span_id,
        )
        return active

    def consume_start_record(
        self,
        *,
        tool_use_id: str | None = None,
        tool_name: str | None = None,
        tool_input: object | None = None,
    ) -> ToolStartRecord | None:
        """Consume the earliest matching pre-tool hook record when available."""
        if self._hook_spool_path is None or not self._hook_spool_path.exists():
            return None

        records = parse_tool_start_records(self._hook_spool_path.read_text(encoding="utf-8"))
        if not records:
            return None

        normalized_tool_input = normalize_tool_input(tool_input) if tool_input is not None else None
        matched_index: int | None = None

        if tool_use_id:
            for index, record in enumerate(records):
                if record.tool_use_id == tool_use_id:
                    matched_index = index
                    break
        elif tool_name is not None and normalized_tool_input is not None:
            for index, record in enumerate(records):
                if record.tool_name == tool_name and record.normalized_tool_input == normalized_tool_input:
                    matched_index = index
                    break

        if matched_index is None:
            return None

        matched = records.pop(matched_index)
        self._hook_spool_path.write_text(
            "".join(record.model_dump_json() + "\n" for record in records),
            encoding="utf-8",
        )
        return matched

    def finish(
        self,
        active: ActiveToolExecution,
        *,
        status: ToolExecutionStatus,
        pid: int | None = None,
        child_pids: list[int] | None = None,
    ) -> ToolExecutionRecord | None:
        """Persist one completed tool execution record when recording is enabled."""
        record = ToolExecutionRecord(
            trace_id=active.trace_id,
            span_id=active.span_id,
            tool_name=active.tool_name,
            started_at=active.started_at,
            ended_at=datetime.now(UTC),
            status=status,
            command=active.command,
            path_hints=active.path_hints,
            working_directory=active.working_directory,
            pid=pid,
            child_pids=child_pids or [],
            agent_id=active.agent_id,
            agent_name=active.agent_name,
            display_name=active.display_name,
        )
        if self._spool_path is not None:
            append_tool_execution_record(self._spool_path, record)
        else:
            logger.warning(
                "Tool execution record not written because spool path is unavailable: tool_name=%s span_id=%s",
                record.tool_name,
                record.span_id,
            )
        return record
