"""Multi-agent orchestrator + node hook bodies for the Strands integration.

Strands' multi-agent and graph features fire ``BeforeMultiAgentInvocationEvent``,
``AfterMultiAgentInvocationEvent``, ``BeforeNodeCallEvent``, and
``AfterNodeCallEvent``. We translate each into a span on the active trace.
"""

from __future__ import annotations

import contextlib
import logging
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ._shared import utc_now

if TYPE_CHECKING:
    from ....client import Aigie
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import (
            AfterMultiAgentInvocationEvent,
            AfterNodeCallEvent,
            BeforeMultiAgentInvocationEvent,
            BeforeNodeCallEvent,
        )

logger = logging.getLogger(__name__)


def _pop_multi_agent_parent(handler: StrandsHandler) -> None:
    """Restore the parent span_id after a multi-agent orchestrator closes."""
    if handler._parent_span_stack:
        handler._current_parent_span_id = handler._parent_span_stack.pop()
    else:
        handler._current_parent_span_id = handler.agent_span_id


def _record_event_exception(handler: StrandsHandler, event: object, source: str) -> None:
    """Classify an event-level exception (orchestrator/node) into _detected_errors.

    Strands emits ``exception`` on after-events for graph/swarm orchestrators when
    the wrapping invocation fails before producing a result. Without this,
    orchestrator-level failures only surface as accumulated text and never go
    through the typed error detector.
    """
    exc = getattr(event, "exception", None)
    if exc is None:
        return
    handler.record_detection(handler._error_detector.detect_from_exception(exc, source=source))


def _maybe_join_error_messages(handler: StrandsHandler) -> tuple[str, bool, str | None]:
    """Read accumulated error state from the handler in a uniform shape."""
    if handler._has_errors:
        msg = "; ".join(handler._error_messages[:2]) if handler._error_messages else None
        return "error", True, msg
    return "success", False, None


async def on_before_multi_agent(
    handler: StrandsHandler, event: BeforeMultiAgentInvocationEvent
) -> None:
    """Create the orchestrator span for a multi-agent invocation."""
    if not handler.config.enabled or not handler.config.trace_multi_agent:
        return
    if not handler.trace_id:
        handler.trace_id = str(uuid.uuid4())
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return

    try:
        await _open_multi_agent_span(handler, aigie, event.source)
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_before_multi_agent: {e}")


async def _open_multi_agent_span(
    handler: StrandsHandler, aigie: Aigie, orchestrator: object
) -> None:
    """Allocate the multi-agent orchestrator span, emit it, push the parent stack."""
    from ....buffer import EventType

    orchestrator_id = id(orchestrator)
    orchestrator_type = type(orchestrator).__name__
    span_id = str(uuid.uuid4())
    start_time = utc_now()
    depth = handler._register_span_depth(span_id, handler._current_parent_span_id)

    handler.multi_agent_map[orchestrator_id] = {
        "spanId": span_id,
        "startTime": start_time,
        "type": orchestrator_type,
        "depth": depth,
    }
    span_data = _build_multi_agent_span(
        handler, span_id, orchestrator_id, orchestrator_type, start_time, depth
    )
    if aigie._buffer:
        await aigie._buffer.add(EventType.SPAN_CREATE, span_data)
    _push_parent(handler, span_id)
    logger.debug(
        f"[AIGIE] Multi-agent orchestrator span created: {orchestrator_type} (id={span_id})"
    )


def _build_multi_agent_span(
    handler: StrandsHandler,
    span_id: str,
    orchestrator_id: int,
    orchestrator_type: str,
    start_time: datetime,
    depth: int,
) -> dict[str, Any]:
    span_data: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id or str(uuid.uuid4()),
        "parent_id": handler._current_parent_span_id,
        "name": f"Multi-Agent: {orchestrator_type}",
        "type": "multi_agent",
        "start_time": start_time.isoformat(),
        "metadata": {
            "orchestrator_type": orchestrator_type,
            "orchestrator_id": str(orchestrator_id),
            "depth": depth,
        },
        "depth": depth,
        "tags": handler.tags,
        "status": "running",
    }
    if handler.user_id:
        span_data["user_id"] = handler.user_id
    if handler.session_id:
        span_data["session_id"] = handler.session_id
    return span_data


def _push_parent(handler: StrandsHandler, span_id: str) -> None:
    if handler._current_parent_span_id:
        handler._parent_span_stack.append(handler._current_parent_span_id)
    handler._current_parent_span_id = span_id


async def _emit_multi_agent_close(
    handler: StrandsHandler,
    span_id: str,
    orchestrator_type: str,
    start_time: datetime,
) -> str:
    """Emit the SPAN_UPDATE for a closed multi-agent span and run assessors."""
    from ....buffer import EventType

    aigie = handler._get_aigie()
    end_time = utc_now()
    duration_s = (end_time - start_time).total_seconds()
    status, is_error, error_message = _maybe_join_error_messages(handler)

    update_data: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration_s * 1_000_000_000),
        "status": status,
        "is_error": is_error,
        "metadata": {
            "orchestrator_type": orchestrator_type,
            "duration_ms": duration_s * 1000,
            "status": status,
        },
    }
    if error_message:
        update_data["error"] = error_message
        update_data["error_message"] = error_message
        update_data["metadata"]["error"] = error_message

    await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

    return status


async def on_after_multi_agent(
    handler: StrandsHandler, event: AfterMultiAgentInvocationEvent
) -> None:
    """Complete the orchestrator span and pop the parent stack."""
    if not handler.config.enabled or not handler.config.trace_multi_agent:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return

    orchestrator = event.source
    orchestrator_id = id(orchestrator)

    try:
        _record_event_exception(handler, event, f"multi_agent:{type(orchestrator).__name__}")
        data = handler.multi_agent_map.get(orchestrator_id)
        if not data:
            return
        status = await _emit_multi_agent_close(
            handler, data["spanId"], data["type"], data["startTime"]
        )

        _pop_multi_agent_parent(handler)

        logger.debug(
            f"[AIGIE] Multi-agent orchestrator span completed: {data['type']} "
            f"(id={data['spanId']}, status={status})"
        )
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_after_multi_agent: {e}")
    finally:
        handler.multi_agent_map.pop(orchestrator_id, None)


async def on_before_node_call(handler: StrandsHandler, event: BeforeNodeCallEvent) -> None:
    """Create a node span (for graph orchestrators)."""
    if not handler.config.enabled or not handler.config.trace_multi_agent:
        return
    if not handler._current_parent_span_id or not handler.trace_id:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return

    try:
        from ....buffer import EventType

        node_id = event.node_id
        orchestrator_type = type(event.source).__name__
        span_id = str(uuid.uuid4())
        start_time = utc_now()
        depth = handler._register_span_depth(span_id, handler._current_parent_span_id)

        handler.node_map[node_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "nodeId": node_id,
            "depth": depth,
        }
        span_data = _build_node_span(
            handler, span_id, node_id, orchestrator_type, start_time, depth
        )
        await aigie._buffer.add(EventType.SPAN_CREATE, span_data)
        logger.debug(f"[AIGIE] Node span created: {node_id} (id={span_id})")
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_before_node_call: {e}")


def _build_node_span(
    handler: StrandsHandler,
    span_id: str,
    node_id: str,
    orchestrator_type: str,
    start_time: datetime,
    depth: int,
) -> dict[str, Any]:
    span_data: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id,
        "parent_id": handler._current_parent_span_id,
        "name": f"Node: {node_id}",
        "type": "node",
        "start_time": start_time.isoformat(),
        "metadata": {
            "node_id": node_id,
            "orchestrator_type": orchestrator_type,
            "depth": depth,
        },
        "tags": handler.tags,
        "status": "running",
        "depth": depth,
    }
    if handler.user_id:
        span_data["user_id"] = handler.user_id
    if handler.session_id:
        span_data["session_id"] = handler.session_id
    return span_data


async def on_after_node_call(handler: StrandsHandler, event: AfterNodeCallEvent) -> None:
    """Complete a node span."""
    if not handler.config.enabled or not handler.config.trace_multi_agent:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return

    node_id = event.node_id

    try:
        _record_event_exception(handler, event, f"node:{node_id}")
        data = handler.node_map.get(node_id)
        if not data:
            return
        await _emit_node_close(handler, data["spanId"], node_id, data["startTime"])
        logger.debug(f"[AIGIE] Node span completed: {node_id} (id={data['spanId']})")
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_after_node_call: {e}")
    finally:
        handler.node_map.pop(node_id, None)


async def _emit_node_close(
    handler: StrandsHandler, span_id: str, node_id: str, start_time: datetime
) -> None:
    """Emit the SPAN_UPDATE that closes a node span."""
    from ....buffer import EventType

    aigie = handler._get_aigie()
    end_time = utc_now()
    duration_s = (end_time - start_time).total_seconds()
    status, is_error, error_message = _maybe_join_error_messages(handler)

    update_data: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration_s * 1_000_000_000),
        "status": status,
        "is_error": is_error,
        "metadata": {
            "node_id": node_id,
            "duration_ms": duration_s * 1000,
            "status": status,
        },
    }
    if error_message:
        update_data["error"] = error_message
        update_data["error_message"] = error_message
        update_data["metadata"]["error"] = error_message

    await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)
