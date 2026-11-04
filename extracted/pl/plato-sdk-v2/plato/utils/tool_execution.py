"""Shared helpers for ATIF tool spans and the agent-local tool execution context."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from opentelemetry.trace import Span, Tracer
from pydantic import BaseModel

from plato.otel import start_step_span

DEFAULT_TOOL_EXECUTION_CONTEXT_PATH = Path("/tmp/plato-tool-execution-context.json")

# Env var carrying the absolute path (inside the agent VM) the post-compaction
# hook writes the summary to. Set by the agent runner from the
# ``compaction_summary_path`` config field; unset means the hook is a no-op.
# Shared by the claude-code PostCompact hook and the opencode compaction plugin.
COMPACTION_SUMMARY_PATH_ENV = "PLATO_COMPACTION_SUMMARY_PATH"

logger = logging.getLogger(__name__)


class ToolExecutionContext(BaseModel):
    """Agent-local context out-of-band hooks use to parent their spans.

    Written to :data:`DEFAULT_TOOL_EXECUTION_CONTEXT_PATH` on the agent VM
    before the run; ``trace_id`` / ``span_id`` identify the span hooks (browser
    screenshot capture, the file watcher sidecar) nest under. Unknown fields
    written by an older SDK are ignored (pydantic's default ``extra="ignore"``).
    """

    session_id: str = ""
    agent_id: str = ""
    agent_name: str = ""
    display_name: str = ""
    trace_id: str = ""
    span_id: str = ""


class PendingToolExecution(BaseModel):
    """Pending tool execution paired from start to completion."""

    step_id: int
    tool_name: str
    # Identity of the ATIF tool step span (lowercase hex), captured so callers
    # can parent related spans (e.g. a sub-agent spawned by this Task call)
    # under the tool span itself.
    trace_id: str | None = None
    span_id: str | None = None
    # Legacy: always ``None``. Published agents built against the removed
    # recorder API still read it in their abort loops; drop with the compat
    # section at the bottom of this module.
    execution: None = None


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
    logger.debug("Loaded tool execution context from %s: agent_id=%s", path, context.agent_id)
    return context


def build_tool_execution_hook_command(mode: str) -> str:
    """Return the shell command agent CLIs run for a ``plato.utils.tool_execution_hook`` mode."""
    return f"python3 -m plato.utils.tool_execution_hook {mode}"


def build_compaction_summary_hook_command() -> str:
    """Return the shell command for the Claude Code ``PostCompact`` hook.

    Reads the hook payload (with ``compact_summary``) on stdin and persists it
    to ``$PLATO_COMPACTION_SUMMARY_PATH``. See
    :func:`plato.utils.tool_execution_hook._handle_claude_postcompact`.
    """
    return build_tool_execution_hook_command("claude-postcompact")


def open_tool_execution(
    *,
    tracer: Tracer,
    step_id: int,
    tool_id: str,
    tool_name: str,
    tool_arguments: object,
    model_name: str,
    pending_tool_executions: dict[str, PendingToolExecution] | None = None,
    span_kwargs: dict[str, object] | None = None,
    tool_span: Span | None = None,
    origin: str | None = None,
    mcp_server: str | None = None,
    # Legacy kwargs, accepted and ignored: published agents built against the
    # removed recorder API still pass them. Drop with the compat section below.
    recorder: object | None = None,
    started_at: datetime | None = None,
    command: str | None = None,
    path_hints: list[str] | None = None,
    working_directory: str | None = None,
) -> PendingToolExecution:
    """Open a shared ATIF tool span and register the pending execution.

    When ``tool_span`` is provided, the caller created the span and owns its
    lifecycle (deferred-export path: the span is finished later, once
    late-resolving usage lands); only the registration runs here. Otherwise a
    span is created and ended immediately.

    ``origin`` / ``mcp_server`` are copied onto the ATIF ``tool_calls[]``
    entry so MCP invocations are distinguishable from harness builtins.
    """
    del recorder, started_at, command, path_hints, working_directory

    def _register(span: Span) -> PendingToolExecution:
        pending_execution = PendingToolExecution(
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
    pending_tool_executions: dict[str, PendingToolExecution],
    # Legacy kwargs, accepted and ignored: published agents built against the
    # removed recorder API still pass them. Drop with the compat section below.
    status: object | None = None,
    recorder: object | None = None,
) -> int | None:
    """Pop a pending execution and return its originating ATIF step ID."""
    del status, recorder
    pending_execution = pending_tool_executions.pop(tool_id, None)
    if pending_execution is None:
        return None
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


# ---------------------------------------------------------------------------
# Compat for published agents built against the removed recorder API; drop once
# all agents are republished. Agent VMs always install the latest SDK
# (``plato/agents/install.py``), so already-published agent versions import
# these names and call the no-ops below. Nothing in this repo uses them.
# ---------------------------------------------------------------------------


class ToolExecutionStatus(StrEnum):
    """Legacy lifecycle status; only ever passed to the no-op recorder below."""

    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class ToolExecutionRecorder:
    """No-op stand-in for the removed JSONL tool execution recorder."""

    def __init__(self, context: ToolExecutionContext | None = None):
        self._context = context

    @classmethod
    def from_default_context(cls) -> ToolExecutionRecorder:
        return cls(None)

    @property
    def enabled(self) -> bool:
        return False

    def start(self, span: Span, **kwargs: object) -> None:
        del span, kwargs
        return None

    def consume_start_record(self, **kwargs: object) -> None:
        del kwargs
        return None

    def finish(self, active: object, **kwargs: object) -> None:
        del active, kwargs
        return None
