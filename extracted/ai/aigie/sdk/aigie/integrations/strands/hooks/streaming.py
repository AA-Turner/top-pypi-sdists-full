"""BidiAgent streaming hook bodies. No-ops on Strands versions without Bidi events."""

from __future__ import annotations

import importlib
import logging
import uuid
from typing import TYPE_CHECKING, Any

from ._shared import utc_now

if TYPE_CHECKING:
    from ..handler import StrandsHandler

# Bidi* events only ship in newer Strands releases. We probe for them at
# runtime via getattr so older Strands installs don't break import. The
# function signatures below use ``Any`` for the event parameter — these
# handlers only access fields via getattr/hasattr, so a precise type would
# add no real safety.
_HOOKS_MOD: Any = None
try:
    _HOOKS_MOD = importlib.import_module("strands.hooks")
except ImportError:
    _HOOKS_MOD = None

BidiBeforeInvocationEvent = getattr(_HOOKS_MOD, "BidiBeforeInvocationEvent", None)
BidiAfterInvocationEvent = getattr(_HOOKS_MOD, "BidiAfterInvocationEvent", None)
BidiBeforeToolCallEvent = getattr(_HOOKS_MOD, "BidiBeforeToolCallEvent", None)
BidiAfterToolCallEvent = getattr(_HOOKS_MOD, "BidiAfterToolCallEvent", None)
BidiInterruptionEvent = getattr(_HOOKS_MOD, "BidiInterruptionEvent", None)

logger = logging.getLogger(__name__)


def register_streaming_hooks(handler: StrandsHandler, registry: Any) -> None:
    """Register BidiAgent streaming callbacks if the events are available."""
    bidi_events = (
        BidiBeforeInvocationEvent,
        BidiAfterInvocationEvent,
        BidiBeforeToolCallEvent,
        BidiAfterToolCallEvent,
        BidiInterruptionEvent,
    )
    if any(ev is None for ev in bidi_events):
        logger.debug("[AIGIE] BidiAgent events not available - streaming hooks disabled")
        return

    try:
        from functools import partial

        registry.add_callback(
            BidiBeforeInvocationEvent, partial(on_bidi_before_invocation, handler)
        )
        registry.add_callback(BidiAfterInvocationEvent, partial(on_bidi_after_invocation, handler))
        registry.add_callback(BidiBeforeToolCallEvent, partial(on_bidi_before_tool_call, handler))
        registry.add_callback(BidiAfterToolCallEvent, partial(on_bidi_after_tool_call, handler))
        registry.add_callback(BidiInterruptionEvent, partial(on_bidi_interruption, handler))
        logger.debug("[AIGIE] BidiAgent streaming hooks registered")
    except Exception as e:
        logger.warning(f"[AIGIE] Failed to register BidiAgent hooks: {e}")


async def on_bidi_before_invocation(handler: StrandsHandler, event: Any) -> None:
    """Start a streaming invocation span."""
    if not handler.config.enabled or not handler.config.trace_streaming:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        from ....buffer import EventType

        span_id = str(uuid.uuid4())
        start_time = utc_now()
        parent_id = handler.agent_span_id or handler._current_parent_span_id
        span_data = {
            "id": span_id,
            "trace_id": handler.trace_id,
            "parent_id": parent_id,
            "name": "BidiAgent Streaming",
            "type": "llm",
            "start_time": start_time.isoformat(),
            "metadata": {"streaming": True, "bidi_agent": True},
            "status": "running",
        }
        await aigie._buffer.add(EventType.SPAN_CREATE, span_data)
        handler._bidi_span_id = span_id
        handler._bidi_start_time = start_time
        logger.debug(f"[AIGIE] BidiAgent streaming started (span_id={span_id[:8]})")
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_bidi_before_invocation: {e}")


async def on_bidi_after_invocation(handler: StrandsHandler, event: Any) -> None:
    """Complete the streaming invocation span."""
    if not handler.config.enabled or not handler.config.trace_streaming:
        return
    bidi_span_id = handler._bidi_span_id
    if not bidi_span_id:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        from ....buffer import EventType

        end_time = utc_now()
        start = handler._bidi_start_time
        duration = (end_time - start).total_seconds() if start else 0.0
        output, status = _bidi_invocation_result(event, handler.config.max_content_length)
        await aigie._buffer.add(
            EventType.SPAN_UPDATE,
            {
                "id": bidi_span_id,
                "trace_id": handler.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": status,
                "output": output,
            },
        )
        logger.debug(f"[AIGIE] BidiAgent streaming completed (span_id={bidi_span_id[:8]})")
        handler._bidi_span_id = None
        handler._bidi_start_time = None
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_bidi_after_invocation: {e}")


def _bidi_invocation_result(event: Any, max_len: int) -> tuple[str | None, str]:
    """Extract (output_text, status) from a BidiAfterInvocationEvent."""
    if not hasattr(event, "result"):
        return None, "success"
    if event.result is None:
        return None, "cancelled"
    if hasattr(event.result, "text"):
        return str(event.result.text)[:max_len], "success"
    return None, "success"


async def on_bidi_before_tool_call(handler: StrandsHandler, event: Any) -> None:
    """Track a streaming tool call."""
    if not handler.config.enabled or not handler.config.trace_streaming:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        from ....buffer import EventType

        tool_name = getattr(event, "tool_name", "unknown_tool")
        tool_use_id = getattr(event, "tool_use_id", str(uuid.uuid4()))
        span_id = str(uuid.uuid4())
        start_time = utc_now()
        parent_id = getattr(handler, "_bidi_span_id", None) or handler.agent_span_id
        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "id": span_id,
                "trace_id": handler.trace_id,
                "parent_id": parent_id,
                "name": f"Tool: {tool_name}",
                "type": "tool",
                "start_time": start_time.isoformat(),
                "metadata": {
                    "tool_name": tool_name,
                    "tool_use_id": tool_use_id,
                    "streaming": True,
                },
                "status": "running",
            },
        )
        handler.tool_map[tool_use_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "toolName": tool_name,
            "streaming": True,
        }
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_bidi_before_tool_call: {e}")


async def on_bidi_after_tool_call(handler: StrandsHandler, event: Any) -> None:
    """Complete a streaming tool call span."""
    if not handler.config.enabled or not handler.config.trace_streaming:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        from ....buffer import EventType

        tool_use_id = getattr(event, "tool_use_id", None)
        if not tool_use_id or tool_use_id not in handler.tool_map:
            return
        tool_data = handler.tool_map[tool_use_id]
        end_time = utc_now()
        duration = (end_time - tool_data["startTime"]).total_seconds()
        output, status = _bidi_tool_result(event, handler.config.max_tool_result_length)
        await aigie._buffer.add(
            EventType.SPAN_UPDATE,
            {
                "id": tool_data["spanId"],
                "trace_id": handler.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": status,
                "output": output,
            },
        )
        del handler.tool_map[tool_use_id]
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_bidi_after_tool_call: {e}")


def _bidi_tool_result(event: Any, max_len: int) -> tuple[str | None, str]:
    """Extract (output_text, status) from a BidiAfterToolCallEvent."""
    output: str | None = None
    status = "success"
    if hasattr(event, "result"):
        output = str(event.result)[:max_len]
    if getattr(event, "error", None):
        status = "error"
        output = str(event.error)
    return output, status


async def on_bidi_interruption(handler: StrandsHandler, event: Any) -> None:
    """Record a streaming interruption as a zero-duration span."""
    if not handler.config.enabled or not handler.config.trace_streaming:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        from ....buffer import EventType

        span_id = str(uuid.uuid4())
        timestamp = utc_now()
        parent_id = getattr(handler, "_bidi_span_id", None) or handler.agent_span_id
        reason = getattr(event, "reason", "unknown")
        source = getattr(event, "source", "user")
        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "id": span_id,
                "trace_id": handler.trace_id,
                "parent_id": parent_id,
                "name": f"Interruption: {reason}",
                "type": "event",
                "start_time": timestamp.isoformat(),
                "end_time": timestamp.isoformat(),
                "duration_ns": 0,
                "metadata": {"interruption": True, "reason": reason, "source": source},
                "status": "cancelled",
            },
        )
        logger.debug(f"[AIGIE] BidiAgent interruption recorded (reason={reason})")
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_bidi_interruption: {e}")
