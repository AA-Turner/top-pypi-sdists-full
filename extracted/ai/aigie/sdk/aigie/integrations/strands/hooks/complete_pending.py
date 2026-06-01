"""End-of-invocation cleanup: complete dangling spans, close-on-error, finalize."""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Callable
from datetime import datetime
from typing import TYPE_CHECKING

from ....buffer import EventType
from ._shared import utc_now

if TYPE_CHECKING:
    from ....client import Aigie
    from ..handler import StrandsHandler

logger = logging.getLogger(__name__)


async def complete_pending_spans(handler: StrandsHandler) -> None:
    """Close any spans still open in the handler's per-kind maps.

    Strands sometimes ends an invocation without firing the matching `After*`
    event (e.g. on cancellation). For each kind of span we track, emit a
    SPAN_UPDATE with a synthesized end_time so the trace doesn't carry
    open-ended children.
    """
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized or not handler.trace_id or not aigie._buffer:
        return

    end_time = utc_now()
    trace_id = handler.trace_id

    await _close_map(
        aigie,
        handler.tool_map,
        end_time,
        lambda _key, data: _tool_update(data, trace_id, end_time),
    )
    await _close_map(
        aigie,
        handler.model_call_map,
        end_time,
        lambda key, data: _model_update(key, data, trace_id, end_time),
    )
    handler.model_span_id = None
    handler.model_start_time = None

    await _close_map(
        aigie,
        handler.multi_agent_map,
        end_time,
        lambda _key, data: _multi_agent_update(data, trace_id, end_time),
    )
    await _close_map(
        aigie,
        handler.node_map,
        end_time,
        lambda key, data: _node_update(key, data, trace_id, end_time),
    )


async def _close_map(
    aigie: Aigie,
    items: dict,
    _end_time: datetime,
    build_update: Callable[[object, dict], dict],
) -> None:
    """Drain ``items`` (a span map), emitting SPAN_UPDATE for each entry."""
    buffer = aigie._buffer
    if buffer is None:
        return
    for key in list(items.keys()):
        data = items.get(key)
        if not data:
            continue
        with contextlib.suppress(Exception):
            await buffer.add(EventType.SPAN_UPDATE, build_update(key, data))
        items.pop(key, None)


def _tool_update(data: dict, trace_id: str, end_time: datetime) -> dict:
    duration = (end_time - data["startTime"]).total_seconds()
    return {
        "id": data["spanId"],
        "trace_id": trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration * 1_000_000_000),
        "status": "success",
        "metadata": {"tool_name": data["toolName"], "pending_cleanup": True},
    }


def _model_update(span_id: object, data: dict, trace_id: str, end_time: datetime) -> dict:
    start = data.get("startTime")
    duration = (end_time - start).total_seconds() if start else 0.0
    return {
        "id": span_id,
        "trace_id": trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration * 1_000_000_000),
        "status": "success",
        "metadata": {"model_id": data.get("modelId"), "pending_cleanup": True},
    }


def _multi_agent_update(data: dict, trace_id: str, end_time: datetime) -> dict:
    duration = (end_time - data["startTime"]).total_seconds()
    return {
        "id": data["spanId"],
        "trace_id": trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration * 1_000_000_000),
        "status": "success",
        "metadata": {"orchestrator_type": data["type"], "pending_cleanup": True},
    }


def _node_update(node_id: object, data: dict, trace_id: str, end_time: datetime) -> dict:
    duration = (end_time - data["startTime"]).total_seconds()
    return {
        "id": data["spanId"],
        "trace_id": trace_id,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration * 1_000_000_000),
        "status": "success",
        "metadata": {"node_id": node_id, "pending_cleanup": True},
    }


async def emit_error_close(handler: StrandsHandler, aigie: Aigie, exc: Exception) -> None:
    """Best-effort: close the agent span and trace as 'error' when on_after blew up."""
    if not (handler.agent_span_id and handler.trace_id):
        return
    now = utc_now()
    agent_span_data = handler._agent_span_data or {}
    name = f"Agent: {agent_span_data.get('agent_name', 'Strands Agent')}"
    start_iso = (
        handler._invocation_start_time.isoformat()
        if handler._invocation_start_time
        else now.isoformat()
    )
    error_span = {
        "id": handler.agent_span_id,
        "trace_id": handler.trace_id,
        "parent_id": None,
        "name": name,
        "type": "agent",
        "start_time": start_iso,
        "end_time": now.isoformat(),
        "status": "error",
        "error": str(exc),
        "error_message": str(exc),
    }
    trace_update = {
        "id": handler.trace_id,
        "status": "error",
        "end_time": now.isoformat(),
        "error": str(exc),
        "error_message": str(exc),
    }
    if not aigie._buffer:
        return
    buffer = aigie._buffer
    with contextlib.suppress(Exception):
        await buffer.add(EventType.SPAN_CREATE, error_span)
        await buffer.add(EventType.TRACE_UPDATE, trace_update)


def finalize_invocation_cleanup(handler: StrandsHandler) -> None:
    """End-of-invocation cleanup: unsubscribe interventions, clear depth, drop trace ownership."""
    if handler._intervention_dispatcher and handler.trace_id:
        handler._intervention_dispatcher.unsubscribe_trace(handler.trace_id)
    handler._span_depth_map.clear()
    if handler._is_trace_owner:
        with contextlib.suppress(Exception):
            from ....auto_instrument.trace import (
                clear_current_trace,
                set_thread_local_trace_id,
            )

            clear_current_trace()
            set_thread_local_trace_id(None)
        handler._is_trace_owner = False
    handler.trace_id = None
