"""
Claude Agent SDK callback handler for Aigie SDK.

Provides automatic tracing for Claude Agent SDK query execution,
tool usage, and conversation sessions.

Includes comprehensive error detection and drift monitoring.
"""

import logging
import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

from ...buffer import EventType
from ...context_manager import merge_metadata
from ...tracing.retention import is_retention_suppressed
from .monitoring import (
    DetectedError,
    DriftDetector,
    ErrorDetector,
)


def _utc_now() -> datetime:
    """Get current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


def _utc_isoformat() -> str:
    """Get current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat()


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .session_context import ClaudeSessionContext


def _shorten_model_name(model: str) -> str:
    """Convert full model name to short display name.

    Examples:
        claude-sonnet-4-20250514 -> Sonnet
        claude-haiku-3-5-20241022 -> Haiku
        claude-opus-4-5-20251101 -> Opus
    """
    if not model:
        return "Claude"
    model_lower = model.lower()
    if "sonnet" in model_lower:
        return "Sonnet"
    if "haiku" in model_lower:
        return "Haiku"
    if "opus" in model_lower:
        return "Opus"
    return "Claude"


def _sanitize_error(error_msg: str) -> str:
    """Remove local file paths from error messages."""
    if not error_msg:
        return error_msg
    return re.sub(r"/(?:Users|home)/[^/]+/(?:[^/]+/)*", "", error_msg)


def _pick_error_message(
    error: str | None,
    result_error_message: str | None,
    detected_errors: list,
) -> str | None:
    """Pick the most informative error string, sanitized. Returns None if none apply."""
    if error:
        return _sanitize_error(error)
    if result_error_message:
        return _sanitize_error(result_error_message)
    if detected_errors:
        return _sanitize_error(detected_errors[0].message)
    return None


_USAGE_FIELD_RES = {
    field: re.compile(rf"{field}\s*:\s*(\d+)")
    for field in ("total_tokens", "tool_uses", "duration_ms")
}


def _parse_subagent_usage_payload(result: Any) -> dict[str, Any]:
    """Extract `<usage>total_tokens: N tool_uses: M duration_ms: K</usage>`
    from the SDK Task-tool result. Missing keys come back as None."""
    out: dict[str, Any] = dict.fromkeys(_USAGE_FIELD_RES, None)

    blocks = (
        result
        if isinstance(result, list)
        else (result.get("content") if isinstance(result, dict) else None)
    )
    if not isinstance(blocks, list):
        return out

    for blk in blocks:
        text = blk.get("text") if isinstance(blk, dict) else getattr(blk, "text", None)
        if not text or "<usage>" not in text:
            continue
        for field, pat in _USAGE_FIELD_RES.items():
            m = pat.search(text)
            if m:
                out[field] = int(m.group(1))
        break
    return out


def _serialize_tool_result(result: Any, max_length: int) -> Any:
    """Return a JSON-friendly shape for a tool/subagent result.

    The SDK delivers MCP results as a list of `{"type": "text", "text": ...}`
    blocks (or block objects with `.text` / `.type`). Returning the original
    structure lets downstream consumers `JSON.parse` it instead of the prior
    Python `repr()` string."""
    if result is None:
        return None
    if isinstance(result, str):
        return result[:max_length]
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if isinstance(result, list):
        out: list[Any] = []
        for item in result:
            if isinstance(item, dict):
                out.append(item)
            elif hasattr(item, "model_dump"):
                out.append(item.model_dump())
            else:
                block = {}
                if hasattr(item, "type"):
                    block["type"] = item.type
                if hasattr(item, "text"):
                    block["text"] = item.text
                out.append(block or str(item)[:max_length])
        return out
    return str(result)[:max_length]


def _format_subagent_name(subagent_type: str) -> str:
    """Format subagent type as a proper display name.

    Examples:
        researcher -> Researcher
        data-analyst -> Data Analyst
        report-writer -> Report Writer
    """
    if not subagent_type:
        return "Subagent"
    return subagent_type.replace("-", " ").replace("_", " ").title()


# Late import: ._events.* modules import helpers (_format_subagent_name,
# _serialize_tool_result, ...) from this module, so the imports must run
# after those helpers are defined to avoid a circular import.
from ._events import (  # noqa: E402
    LLMSubagentEvents,
    QueryEvents,
    SessionTurnEvents,
    ToolEvents,
)


class ClaudeAgentSDKEvents(
    QueryEvents,
    ToolEvents,
    SessionTurnEvents,
    LLMSubagentEvents,
):
    # ABC marker attributes — let the lifecycle bridge recognise this class
    # as an Aigie callback regardless of import path.
    _is_aigie_handler = True
    framework_type = "claude_agent_sdk"

    # L1 emission primitives. The dispatch mixin builds the legacy-shaped
    # payload; these methods route it to the buffer iff retention is not
    # suppressed. Wire-shape baselines lock the payload format.

    _emitter: Any = None

    def _resolve_buffer(self) -> Any:
        if self._emitter is not None:
            return self._emitter
        aigie = self._get_aigie()
        buf = getattr(aigie, "_buffer", None) if aigie is not None else None
        if buf is not None:
            self._emitter = buf
        return buf

    def _emit(self, event_type: EventType, payload: dict[str, Any]) -> None:
        if is_retention_suppressed():
            return
        buf = self._resolve_buffer()
        if buf is not None:
            buf.add_sync(event_type, payload)

    def open_trace(self, *, payload: dict[str, Any]) -> None:
        self._emit(EventType.TRACE_CREATE, payload)

    def open_span(self, *, payload: dict[str, Any]) -> None:
        self._emit(EventType.SPAN_CREATE, payload)

    def close_span(self, *, payload: dict[str, Any]) -> None:
        self._emit(EventType.SPAN_UPDATE, payload)

    def fail_span(self, *, payload: dict[str, Any]) -> None:
        self._emit(EventType.SPAN_UPDATE, payload)

    def close_trace(self, *, payload: dict[str, Any]) -> None:
        self._emit(EventType.TRACE_UPDATE, payload)


    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_tool_results: bool = True,
        capture_messages: bool = True,
        session_context: Optional["ClaudeSessionContext"] = None,
    ):
        """Initialize Claude Agent SDK handler."""
        self._init_identity(trace_name, metadata, tags, user_id, session_id)
        self.capture_tool_results = capture_tool_results
        self.capture_messages = capture_messages
        self._session_context = session_context
        self._init_span_state(session_context)
        self._init_parent_tracking()
        self._init_local_stats()
        self._init_monitoring()

    def _init_identity(
        self,
        trace_name: str | None,
        metadata: dict[str, Any] | None,
        tags: list[str] | None,
        user_id: str | None,
        session_id: str | None,
    ) -> None:
        """Trace-level identity fields. Honors ambient tracing_context() so
        harness-supplied metadata/tags propagate into TRACE_CREATE."""
        from ...context_manager import merge_metadata, merge_tags

        self.trace_name = trace_name
        self.metadata = merge_metadata(metadata)
        self.tags = merge_tags(tags)
        self.user_id = user_id
        self.session_id = session_id  # type: ignore[has-type]

    def _init_span_state(self, session_context: Optional["ClaudeSessionContext"]) -> None:
        """In-flight span registries keyed by SDK-native ids."""
        self.trace_id: str | None = session_context.trace_id if session_context else None
        self.query_span_id: str | None = None
        self.session_span_id: str | None = None
        # tool_use_id / turn_id -> {spanId, startTime, startTimeIso, ...}
        self.tool_map: dict[str, dict[str, Any]] = {}
        self.turn_map: dict[str, dict[str, Any]] = {}
        # subagent_map also tracks tokens for aggregation
        self.subagent_map: dict[str, dict[str, Any]] = {}

    def _init_parent_tracking(self) -> None:
        """Nested-subagent parent stack + depth tracking."""
        self._current_query_span_id: str | None = None
        self._current_turn_span_id: str | None = None
        self._current_parent_tool_use_id: str | None = None
        self._aigie: Any = None
        self._trace_context: Any | None = None
        self._current_user_prompt: str | None = None  # type: ignore[assignment]
        self._parent_span_stack: list[str] = []
        self._local_current_parent: str | None = None
        self._span_depth_map: dict[str, int] = {}
        self._current_depth: int = 0

    def _init_local_stats(self) -> None:
        """Per-handler running totals (delegated to session context if present)."""
        self._local_total_turns = 0
        self._local_total_tool_calls = 0
        self._local_total_input_tokens = 0
        self._local_total_output_tokens = 0
        self._local_total_cache_read_tokens = 0
        self._local_total_cache_creation_tokens = 0
        self._local_total_cost = 0.0
        self._tokens_accumulated_from_stream = False

    def _init_monitoring(self) -> None:
        """Error / drift detectors and the remediation engine seam."""
        self._error_detector = ErrorDetector()
        self._drift_detector = DriftDetector()
        self._detected_errors: list[DetectedError] = []
        self._query_start_time: datetime | None = None  # type: ignore[assignment]
        self._remediation_engine: Any = None

    @property  # type: ignore[override]
    def total_turns(self) -> int:
        if self._session_context:
            return self._session_context.total_turns
        return self._local_total_turns

    @total_turns.setter
    def total_turns(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_turns = value
        else:
            self._local_total_turns = value

    @property
    def total_tool_calls(self) -> int:
        if self._session_context:
            return self._session_context.total_tool_calls
        return self._local_total_tool_calls

    @total_tool_calls.setter
    def total_tool_calls(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_tool_calls = value
        else:
            self._local_total_tool_calls = value

    @property
    def total_input_tokens(self) -> int:
        if self._session_context:
            return self._session_context.total_input_tokens
        return self._local_total_input_tokens

    @total_input_tokens.setter
    def total_input_tokens(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_input_tokens = value
        else:
            self._local_total_input_tokens = value

    @property
    def total_output_tokens(self) -> int:
        if self._session_context:
            return self._session_context.total_output_tokens
        return self._local_total_output_tokens

    @total_output_tokens.setter
    def total_output_tokens(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_output_tokens = value
        else:
            self._local_total_output_tokens = value

    @property
    def total_cache_read_tokens(self) -> int:
        if self._session_context:
            return self._session_context.total_cache_read_tokens
        return self._local_total_cache_read_tokens

    @total_cache_read_tokens.setter
    def total_cache_read_tokens(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_cache_read_tokens = value
        else:
            self._local_total_cache_read_tokens = value

    @property
    def total_cache_creation_tokens(self) -> int:
        if self._session_context:
            return self._session_context.total_cache_creation_tokens
        return self._local_total_cache_creation_tokens

    @total_cache_creation_tokens.setter
    def total_cache_creation_tokens(self, value: int) -> None:
        if self._session_context:
            self._session_context.total_cache_creation_tokens = value
        else:
            self._local_total_cache_creation_tokens = value

    @property
    def total_cost(self) -> float:
        if self._session_context:
            return self._session_context.total_cost
        return self._local_total_cost

    @total_cost.setter
    def total_cost(self, value: float) -> None:
        if self._session_context:
            self._session_context.total_cost = value
        else:
            self._local_total_cost = value

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def _get_current_parent(self) -> str | None:
        """Get current parent span ID for nesting."""
        if self._session_context:
            ctx_parent = self._session_context.get_current_parent()
            if ctx_parent:
                return ctx_parent
        # Check local parent first (for subagent nesting), then fall back to turn/query
        if self._local_current_parent:
            return self._local_current_parent
        return self._current_turn_span_id or self._current_query_span_id

    def _set_current_parent(self, span_id: str | None) -> None:
        """Set current parent span ID."""
        self._local_current_parent = span_id
        if self._session_context:
            self._session_context.set_current_parent(span_id)

    def _get_depth_for_parent(self, parent_id: str | None) -> int:
        """Calculate depth based on parent span's depth."""
        if not parent_id:
            return 0  # Root level (trace)
        # Look up parent's depth and add 1
        parent_depth = self._span_depth_map.get(parent_id, 0)
        return parent_depth + 1

    def _register_span_depth(self, span_id: str, parent_id: str | None) -> int:
        """Register a span's depth and return it."""
        depth = self._get_depth_for_parent(parent_id)
        self._span_depth_map[span_id] = depth
        return depth

    def _get_current_subagent(self) -> dict[str, Any] | None:
        """Get the active subagent for the current parent context.

        Looks at three signals in order:
          1. `_current_parent_tool_use_id` — set by `set_parent_context` when
             we observe an AssistantMessage emitted *from* a subagent.
          2. The active parent span id (`_get_current_parent`) — matched
             against `subagent_map` by `spanId`.
          3. Legacy `_parent_span_stack` — kept for backward-compat with
             nested-spawn paths that push to the stack directly.
        """
        if self._current_parent_tool_use_id:
            data = self.subagent_map.get(self._current_parent_tool_use_id)
            if data:
                return data

        current_parent = self._get_current_parent()
        if current_parent:
            for _tool_use_id, subagent_data in self.subagent_map.items():
                if subagent_data.get("spanId") == current_parent:
                    return subagent_data

        if self._parent_span_stack:
            for _tool_use_id, subagent_data in self.subagent_map.items():
                if subagent_data.get("spanId") == self._parent_span_stack[-1]:
                    return subagent_data
        return None

    def set_trace_context(self, trace_context: Any) -> None:
        """Set an existing trace context to use."""
        self._trace_context = trace_context
        if hasattr(trace_context, "id"):
            self.trace_id = str(trace_context.id)

    async def _report_remediation(self, span_id: str, result) -> None:
        """Report a remediation result to the platform via SPAN_UPDATE metadata
        and POST to /remediation/results for closed-loop learning."""
        try:
            aigie = self._get_aigie()
            if not aigie or not aigie._initialized:
                return

            # Path 1: Span metadata (for trace detail view)
            if aigie._buffer:
                self.close_span(
                    payload={
                        "id": span_id,
                        "trace_id": self.trace_id,
                        "metadata": merge_metadata(
                            {
                                "realtime_remediation": result.to_dict(),
                            }
                        ),
                    }
                )

            # Path 2: POST to /remediation/results (shared engine handles this)
            if self._remediation_engine:
                await self._remediation_engine.report_result(result, self.trace_id)
        except Exception as exc:  # noqa: BLE001
            logger.debug('remediation result reporting failed' + ': %s', exc)

    def __repr__(self) -> str:
        return (
            f"ClaudeAgentSDKEvents("
            f"trace_id={self.trace_id}, "
            f"turns={self.total_turns}, "
            f"tool_calls={self.total_tool_calls}, "
            f"tokens={self.total_input_tokens + self.total_output_tokens}, "
            f"cost=${self.total_cost:.4f})"
        )


# ABC-canonical alias.
ClaudeAgentSDKNativeCallback = ClaudeAgentSDKEvents

__all__ = ["ClaudeAgentSDKEvents", "ClaudeAgentSDKNativeCallback"]

