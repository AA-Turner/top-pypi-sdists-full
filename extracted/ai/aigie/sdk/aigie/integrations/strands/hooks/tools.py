"""Tool hook bodies for the Strands integration."""

from __future__ import annotations

import contextlib
import json
import logging
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from . import remediation as _rem
from ._shared import utc_now

if TYPE_CHECKING:
    from strands.types.tools import ToolResult

    from ....client import Aigie
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent
    with contextlib.suppress(ImportError):
        from strands.types.tools import ToolUse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Before-tool-call: register span placeholder + interception
# ---------------------------------------------------------------------------


async def on_before_tool_call(handler: StrandsHandler, event: BeforeToolCallEvent) -> None:
    """Stage a tool span entry; the actual SPAN_CREATE happens in on_after."""
    if not handler.config.enabled or not handler.config.trace_tools:
        return
    if not handler._current_parent_span_id or not handler.trace_id:
        return

    try:
        tool_use = event.tool_use
        tool_name = tool_use.get("name", "unknown_tool")
        tool_use_id, span_id = _stage_tool_entry(handler, tool_use)
        await _run_pre_tool_intercept(handler, tool_name, tool_use, span_id)
        await _maybe_apply_pending_intervention(handler, tool_name, tool_use, tool_use_id)
        logger.debug(f"[AIGIE] Tool call started: {tool_name} (span_id={span_id})")
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_before_tool_call: {e}")


def _stage_tool_entry(handler: StrandsHandler, tool_use: ToolUse | dict) -> tuple[str, str]:
    """Allocate ids, publish ambient parent, populate tool_map. Returns (tool_use_id, span_id)."""
    from ....auto_instrument.trace import push_thread_local_parent_span_id

    tool_use_id = tool_use.get("toolUseId", str(uuid.uuid4()))
    tool_name = tool_use.get("name", "unknown_tool")
    span_id = str(uuid.uuid4())
    start_time = utc_now()
    depth = handler._register_span_depth(span_id, handler._current_parent_span_id)
    prev_ambient_parent = push_thread_local_parent_span_id(span_id)
    handler.tool_map[tool_use_id] = {
        "spanId": span_id,
        "startTime": start_time,
        "toolName": tool_name,
        "depth": depth,
        "tool_input": tool_use.get("input", {}),
        "parentId": handler._current_parent_span_id,
        "_prev_ambient_parent": prev_ambient_parent,
    }
    handler._total_tool_calls += 1
    with contextlib.suppress(Exception):
        from ....auto_instrument.span_enricher import set_active_span_id

        set_active_span_id(span_id)
    return tool_use_id, span_id


async def _run_pre_tool_intercept(
    handler: StrandsHandler, tool_name: str, tool_use: ToolUse | dict, span_id: str
) -> None:
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        intercept = await aigie.intercept_before_tool(
            tool_name=tool_name,
            tool_args=tool_use.get("input", {}),
            trace_id=handler.trace_id,
            span_id=span_id,
        )
        if intercept.get("decision") != "allow":
            logger.info(
                f"[AIGIE] Pre-tool signal for {tool_name}: "
                f"{intercept.get('decision')} — {intercept.get('reason')}"
            )
    except Exception as ie:
        logger.debug(f"[AIGIE] Pre-tool intercept error (non-fatal): {ie}")


async def _maybe_apply_pending_intervention(
    handler: StrandsHandler, tool_name: str, tool_use: ToolUse | dict, tool_use_id: str
) -> None:
    if not (handler._intervention_dispatcher and handler.trace_id):
        return
    signal = handler._intervention_dispatcher.pop_pending(handler.trace_id)
    if not signal:
        return
    logger.info(
        f"[AIGIE] Intervention received for {tool_name}: "
        f"type={signal.intervention_type}, reason={signal.reason}"
    )
    import asyncio as _asyncio

    result = await handler._intervention_dispatcher.process(
        signal, tool_name, tool_use.get("input", {})
    )
    if result.delay_ms:
        await _asyncio.sleep(result.delay_ms / 1000.0)
    handler.tool_map[tool_use_id]["_pending_intervention"] = signal


# ---------------------------------------------------------------------------
# After-tool-call: status, error detection, remediation, span emit
# ---------------------------------------------------------------------------


def _determine_tool_status(event: AfterToolCallEvent) -> tuple[str, bool, str | None]:
    """Inspect a Strands AfterToolCallEvent and yield (status, is_error, error_msg)."""
    if event.exception:
        return "error", True, str(event.exception)
    result = event.result
    if isinstance(result, dict) and result.get("status") == "error":
        msg = None
        content = result.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    msg = item["text"]
                    break
        return "error", True, msg or str(result)
    if event.cancel_message:
        return "cancelled", False, None
    return "success", False, None


def _resolve_tool_use_id(handler: StrandsHandler, tool_use: ToolUse | dict) -> str | None:
    """Look up the tool_use id, falling back to most-recent-by-name."""
    tu_id = tool_use.get("toolUseId")
    if isinstance(tu_id, str):
        return tu_id
    tool_name = tool_use.get("name", "unknown_tool")
    for tid, tdata in reversed(list(handler.tool_map.items())):
        if tdata.get("toolName") == tool_name:
            return tid
    logger.warning(f"[AIGIE] No toolUseId found for tool {tool_name}, skipping duration tracking")
    return None


def _restore_ambient_parent(handler: StrandsHandler, event: AfterToolCallEvent) -> None:
    """Restore the ambient parent span_id stashed in on_before_tool_call."""
    with contextlib.suppress(Exception):
        from ....auto_instrument.trace import set_thread_local_parent_span_id

        tu = event.tool_use
        tu_id = tu.get("toolUseId") if isinstance(tu, dict) else None
        tdata = handler.tool_map.get(tu_id) if tu_id else None
        if tdata is not None and "_prev_ambient_parent" in tdata:
            set_thread_local_parent_span_id(tdata["_prev_ambient_parent"])


def _matches_subagent_naming(tool_name: str) -> bool:
    """Conservative agent-as-tool naming heuristic.

    Matches: ``agent``, ``agent_*``, ``*_agent``, anything containing ``subagent``.
    Rejects names like ``manage_agent_settings`` to avoid false positives.
    """
    lowered = tool_name.lower()
    if "subagent" in lowered:
        return True
    if lowered == "agent":
        return True
    return lowered.startswith("agent_") or lowered.endswith("_agent")


def _resolve_subagent_type(handler: StrandsHandler, tool_name: str) -> str | None:
    """Return the subagent type for a tool, or None if the tool is not a subagent.

    Strands subagents flow through the regular tool path. We treat a tool as a
    subagent if (a) it was explicitly registered via
    ``handler.register_subagent_tool(name)`` (explicit type label) or (b) its
    name matches a common agent-as-tool naming convention.
    """
    explicit = handler._subagent_types.get(tool_name)
    if explicit is not None:
        return explicit
    if _matches_subagent_naming(tool_name):
        return tool_name
    return None


def _record_detection(
    handler: StrandsHandler,
    tool_name: str,
    tool_use_id: str,
    tool_data: dict,
    event_result: ToolResult | dict[str, object] | None,
    is_error: bool,
    duration_ms: float,
) -> str:
    """Run error + drift detection; return the result-as-string used elsewhere."""
    result_str = str(event_result) if event_result else ""
    subagent_type = _resolve_subagent_type(handler, tool_name)
    if subagent_type is not None:
        detected = handler._error_detector.detect_from_subagent_result(
            subagent_type=subagent_type,
            tool_use_id=tool_use_id,
            result=result_str,
            is_error_flag=is_error,
            duration_ms=duration_ms,
        )
    else:
        detected = handler._error_detector.detect_from_tool_result(
            tool_name=tool_name,
            tool_use_id=tool_use_id,
            result=result_str,
            is_error_flag=is_error,
            duration_ms=duration_ms,
        )
    handler.record_detection(detected)
    if detected:
        logger.debug(f"[AIGIE] Error detected in tool {tool_name}: {detected.error_type.value}")
    handler._drift_detector.record_tool_use(
        tool_name=tool_name,
        tool_input=tool_data.get("tool_input", {}),
        duration_ms=duration_ms,
        is_error=is_error,
    )
    return result_str


def _build_tool_span_data(
    handler: StrandsHandler,
    span_id: str,
    tool_name: str,
    tool_use_id: str,
    tool_data: dict,
    start_time: datetime,
    end_time: datetime,
    duration: float,
    duration_ms: float,
    status: str,
    is_error: bool,
    error_msg: str | None,
    event: AfterToolCallEvent,
) -> dict[str, Any]:
    """Build the SPAN_CREATE payload for a completed tool span."""
    span_data: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id,
        "parent_id": tool_data.get("parentId", handler._current_parent_span_id),
        "name": f"Tool: {tool_name}",
        "type": "tool",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration * 1_000_000_000),
        "status": status,
        "is_error": is_error,
        "depth": tool_data.get("depth", 1),
        "tags": handler.tags,
        "metadata": {
            "framework": "strands",
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "depth": tool_data.get("depth", 1),
            "duration_ms": duration_ms,
            "status": status,
        },
    }
    try:
        from ....tool_category import infer_tool_category

        category = infer_tool_category(tool_name, None)
        if category:
            span_data["metadata"]["tool_category"] = category
    except ImportError:
        pass
    if handler.user_id:
        span_data["user_id"] = handler.user_id
    if handler.session_id:
        span_data["session_id"] = handler.session_id
    _attach_tool_io(span_data, handler, tool_data, event)
    if is_error and error_msg:
        _attach_tool_error(span_data, error_msg, event)
    return span_data


def _attach_tool_io(
    span_data: dict[str, Any], handler: StrandsHandler, tool_data: dict, event: AfterToolCallEvent
) -> None:
    if handler.config.capture_inputs:
        tool_input = tool_data.get("tool_input", {})
        try:
            input_repr = (
                json.dumps(tool_input, default=str)
                if isinstance(tool_input, (dict, list))
                else str(tool_input)
            )
        except Exception:
            input_repr = str(tool_input)
        if len(input_repr) > handler.config.max_content_length:
            input_repr = input_repr[: handler.config.max_content_length] + "..."
        span_data["input"] = input_repr
        span_data["metadata"]["tool_input"] = input_repr
    if handler.config.capture_outputs and event.result:
        try:
            result_repr = (
                json.dumps(event.result, default=str)
                if isinstance(event.result, (dict, list))
                else str(event.result)
            )
        except Exception:
            result_repr = str(event.result)
        if len(result_repr) > handler.config.max_tool_result_length:
            result_repr = result_repr[: handler.config.max_tool_result_length] + "..."
        span_data["output"] = result_repr
        span_data["metadata"]["tool_result"] = result_repr


def _attach_tool_error(
    span_data: dict[str, Any], error_msg: str, event: AfterToolCallEvent
) -> None:
    span_data["error"] = error_msg
    span_data["error_message"] = error_msg
    span_data["metadata"]["error"] = error_msg
    if event.exception:
        span_data["error_type"] = type(event.exception).__name__
        span_data["metadata"]["error_type"] = type(event.exception).__name__
    else:
        span_data["error_type"] = "ToolError"


async def _assess_tool_step(
    handler: StrandsHandler,
    span_id: str,
    tool_name: str,
    result_str: str,
    error_msg: str | None,
    event: AfterToolCallEvent,
) -> None:
    if not (handler.trace_id and span_id):
        return


async def on_after_tool_call(handler: StrandsHandler, event: AfterToolCallEvent) -> None:
    """Emit the tool span and run remediation/intercept logic."""
    with contextlib.suppress(Exception):
        from ....auto_instrument.span_enricher import set_active_span_id

        set_active_span_id(handler._current_parent_span_id)
    _restore_ambient_parent(handler, event)

    if not handler.config.enabled or not handler.config.trace_tools:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return

    tool_use = event.tool_use
    tool_use_id = _resolve_tool_use_id(handler, tool_use)
    if not tool_use_id:
        return

    try:
        await _run_after_tool_call(handler, event, tool_use_id, aigie)
    except Exception as e:
        logger.warning(f"[AIGIE] Error in on_after_tool_call: {e}")
    finally:
        handler.tool_map.pop(tool_use_id, None)


async def _run_after_tool_call(
    handler: StrandsHandler,
    event: AfterToolCallEvent,
    tool_use_id: str,
    aigie: Aigie,
) -> None:
    """Body of on_after_tool_call once tool_use_id is resolved."""
    from ....buffer import EventType

    tool_data = handler.tool_map.get(tool_use_id)
    if not tool_data:
        return
    span_id = tool_data["spanId"]
    tool_name = tool_data["toolName"]
    status, is_error, error_msg = _determine_tool_status(event)
    _accumulate_error(handler, is_error, error_msg)

    start_time = tool_data["startTime"]
    end_time = utc_now()
    duration = (end_time - start_time).total_seconds()
    duration_ms = duration * 1000

    result_str = _record_detection(
        handler, tool_name, tool_use_id, tool_data, event.result, is_error, duration_ms
    )
    await _run_post_processing(
        handler,
        is_error,
        error_msg,
        tool_name,
        span_id,
        tool_data,
        result_str,
        duration_ms,
        event,
    )
    span_data = _build_tool_span_data(
        handler,
        span_id,
        tool_name,
        tool_use_id,
        tool_data,
        start_time,
        end_time,
        duration,
        duration_ms,
        status,
        is_error,
        error_msg,
        event,
    )
    logger.debug(f"[AIGIE] Creating complete Tool span: id={span_id}")
    if aigie._buffer:
        await aigie._buffer.add(EventType.SPAN_CREATE, span_data)
    await _assess_tool_step(handler, span_id, tool_name, result_str, error_msg, event)
    logger.debug(
        f"[AIGIE] Tool span created: {tool_name} (id={span_id}, status={status}, "
        f"duration_ms={duration_ms:.2f})"
    )


def _accumulate_error(handler: StrandsHandler, is_error: bool, error_msg: str | None) -> None:
    if not is_error:
        return
    handler._has_errors = True
    if error_msg and error_msg not in handler._error_messages:
        handler._error_messages.append(error_msg)


async def _run_post_processing(
    handler: StrandsHandler,
    is_error: bool,
    error_msg: str | None,
    tool_name: str,
    span_id: str,
    tool_data: dict,
    result_str: str,
    duration_ms: float,
    event: AfterToolCallEvent,
) -> None:
    """Real-time remediation, post-tool intercept, and push-intervention application."""
    await _rem._maybe_remediate(
        handler, is_error, error_msg, tool_name, span_id, tool_data, result_str, event
    )
    await _rem._maybe_post_tool_intercept(
        handler, is_error, error_msg, tool_name, span_id, duration_ms, event
    )
    _rem._apply_push_intervention(handler, tool_data, event)


# ---------------------------------------------------------------------------
# Remediation helpers
# ---------------------------------------------------------------------------
