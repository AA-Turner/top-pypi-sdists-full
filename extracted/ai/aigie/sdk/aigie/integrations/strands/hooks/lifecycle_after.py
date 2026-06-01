"""on_after_invocation body."""

from __future__ import annotations

import contextlib
import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ....buffer import EventType
from ....context_manager import merge_metadata
from ..cost_tracking import calculate_strands_cost
from ._shared import utc_now
from .llm_finalize import finalize_pending_llm_span
from .trace_update import build_trace_summary, build_trace_update, finalize_trace_emission
from .usage import coerce_usage, extract_model_id, get_current_accumulated_usage

if TYPE_CHECKING:
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import AfterInvocationEvent
    with contextlib.suppress(ImportError):
        from strands.agent.agent_result import AgentResult

logger = logging.getLogger(__name__)


def _extract_total_usage(
    handler: StrandsHandler, event: AfterInvocationEvent, result: AgentResult | None
) -> None:
    """Probe result/agent for total token usage in priority order; warn if none hit."""
    candidates: list[Any] = []
    if result is not None:
        candidates.append(getattr(getattr(result, "metrics", None), "accumulated_usage", None))
        candidates.append(getattr(result, "usage", None))
    candidates.append(get_current_accumulated_usage(event.agent))
    for raw in candidates:
        normalized = coerce_usage(raw)
        if normalized:
            handler._total_input_tokens = normalized["inputTokens"]
            handler._total_output_tokens = normalized["outputTokens"]
            return
    logger.warning("[AIGIE] Could not extract token usage from result or agent metrics")


def _calculate_total_cost(handler: StrandsHandler, event: AfterInvocationEvent) -> None:
    """Compute handler._total_cost from the (input, output) tokens."""
    if not (handler._total_input_tokens > 0 or handler._total_output_tokens > 0):
        return
    model_id = extract_model_id(event.agent.model) if hasattr(event.agent, "model") else None
    try:
        handler._total_cost = calculate_strands_cost(
            model_id=model_id,
            input_tokens=handler._total_input_tokens,
            output_tokens=handler._total_output_tokens,
        )
    except Exception as cost_err:
        logger.warning(f"[AIGIE] Cost calculation failed for model {model_id}: {cost_err}")
        handler._total_cost = 0.0


def _resolve_invocation_status(
    handler: StrandsHandler, result: AgentResult | None
) -> tuple[str, str | None, bool]:
    """Return (status, error_message, has_error)."""
    has_error = result is None or handler._has_errors or len(handler._error_messages) > 0
    status = "error" if has_error else "success"
    error_message: str | None = None
    if handler._error_messages:
        error_message = "; ".join(handler._error_messages[:3])
    elif result is None:
        error_message = "Agent invocation returned no result"
    return status, error_message, has_error


def _build_complete_agent_span(
    handler: StrandsHandler,
    agent_span_data: dict[str, Any],
    status: str,
    error_message: str | None,
    duration_ms: float,
    agent_end_time: datetime,
) -> dict[str, Any]:
    """Build the SPAN_CREATE payload that closes the agent span."""
    total_tokens = handler._total_input_tokens + handler._total_output_tokens
    span: dict[str, Any] = {
        "id": handler.agent_span_id,
        "trace_id": handler.trace_id,
        "parent_id": handler._current_parent_span_id or None,
        "name": f"Agent: {agent_span_data.get('agent_name', 'Strands Agent')}",
        "type": "agent",
        "start_time": handler._invocation_start_time.isoformat()
        if handler._invocation_start_time
        else agent_end_time.isoformat(),
        "end_time": agent_end_time.isoformat(),
        "duration_ns": int(duration_ms * 1_000_000),
        "status": status,
        "depth": agent_span_data.get("depth", 0),
        "tags": handler.tags,
        "prompt_tokens": handler._total_input_tokens,
        "completion_tokens": handler._total_output_tokens,
        "total_tokens": total_tokens,
        "total_cost": handler._total_cost,
        "token_usage": {
            "prompt_tokens": handler._total_input_tokens,
            "completion_tokens": handler._total_output_tokens,
            "total_tokens": total_tokens,
            "unit": "TOKENS",
        },
        "usage": {
            "prompt_tokens": handler._total_input_tokens,
            "completion_tokens": handler._total_output_tokens,
            "total_tokens": total_tokens,
            "input_tokens": handler._total_input_tokens,
            "output_tokens": handler._total_output_tokens,
        },
        "metadata": merge_metadata(
            {
                "framework": "strands",
                "agent_id": agent_span_data.get("agent_id"),
                "agent_name": agent_span_data.get("agent_name", "Strands Agent"),
                "depth": agent_span_data.get("depth", 0),
                "total_tool_calls": handler._total_tool_calls,
                "total_input_tokens": handler._total_input_tokens,
                "total_output_tokens": handler._total_output_tokens,
                "total_tokens": total_tokens,
                "total_cost": handler._total_cost,
                "duration_ms": duration_ms,
                "status": status,
            }
        ),
    }
    _attach_identity_and_error(handler, span, agent_span_data, error_message)
    return span


def _attach_identity_and_error(
    handler: StrandsHandler,
    span: dict[str, Any],
    agent_span_data: dict[str, Any],
    error_message: str | None,
) -> None:
    if handler.user_id:
        span["user_id"] = handler.user_id
    if handler.session_id:
        span["session_id"] = handler.session_id
    if agent_span_data.get("input"):
        span["input"] = agent_span_data["input"]
    if not error_message:
        return
    span["error"] = error_message
    span["error_message"] = error_message
    span["error_type"] = "AgentError"
    span["metadata"]["error"] = error_message
    span["metadata"]["error_type"] = "AgentError"


def _select_output_data(
    handler: StrandsHandler, event: AfterInvocationEvent, result: AgentResult | None
) -> dict[str, Any] | str | None:
    """Pick the best agent-level output: result.message → result.state → str(result) → last assistant msg."""
    output_data: dict[str, Any] | str | None = None
    if result is not None:
        if hasattr(result, "message") and result.message:
            msg = result.message
            output_data = (
                dict(msg) if isinstance(msg, dict) else {"role": "assistant", "content": str(msg)}
            )
        elif hasattr(result, "state") and result.state:
            output_data = (
                {"state": result.state} if isinstance(result.state, dict) else str(result.state)
            )
        else:
            raw = str(result)
            if raw and raw != "None":
                output_data = raw
    if output_data is not None:
        return output_data
    return _scan_assistant_message_fallback(handler, event)


def _scan_assistant_message_fallback(
    handler: StrandsHandler, event: AfterInvocationEvent
) -> dict[str, Any] | None:
    """Return the most recent assistant message added during this invocation."""
    if not (hasattr(event, "agent") and hasattr(event.agent, "messages")):
        return None
    try:
        msgs = event.agent.messages
    except Exception:
        return None
    if not isinstance(msgs, list):
        return None
    start = handler._messages_start_index
    if start < 0 or start > len(msgs):
        start = 0
    for msg in reversed(msgs[start:]):
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            return dict(msg)
    return None


def _attach_output_to_span(
    handler: StrandsHandler,
    event: AfterInvocationEvent,
    result: AgentResult | None,
    complete_agent_span: dict[str, Any],
) -> None:
    """Pick the best agent output and attach it to the span (rendered as JSON/string)."""
    if not handler.config.capture_outputs:
        return
    output_data = _select_output_data(handler, event, result)
    if output_data is None:
        return
    try:
        output_repr = (
            json.dumps(output_data, default=str)
            if isinstance(output_data, (dict, list))
            else str(output_data)
        )
        if len(output_repr) > handler.config.max_content_length:
            output_repr = output_repr[: handler.config.max_content_length] + "..."
    except Exception:
        output_repr = str(output_data)[: handler.config.max_content_length]
    complete_agent_span["output"] = output_repr
    complete_agent_span["metadata"]["result"] = output_repr


def _run_agent_quality_assessment(
    handler: StrandsHandler, aigie: Any, complete_agent_span: dict[str, Any]
) -> None:
    if not (handler.trace_id and handler.agent_span_id):
        return
    pass  # assess_step removed (step_assessor deleted in P13)


async def _emit_complete_agent_span(
    handler: StrandsHandler, aigie: Any, event: AfterInvocationEvent, result: AgentResult | None
) -> tuple[dict[str, Any], dict[str, Any], str, str | None]:
    """Build & emit the closing agent SPAN_CREATE; return (span, agent_data, status, error)."""
    _extract_total_usage(handler, event, result)
    _calculate_total_cost(handler, event)
    status, error_message, _ = _resolve_invocation_status(handler, result)
    agent_end_time = utc_now()
    duration_ms = (
        (agent_end_time - handler._invocation_start_time).total_seconds() * 1000
        if handler._invocation_start_time
        else 0.0
    )
    agent_span_data = handler._agent_span_data or {}
    complete = _build_complete_agent_span(
        handler, agent_span_data, status, error_message, duration_ms, agent_end_time
    )
    _attach_output_to_span(handler, event, result, complete)
    if aigie._buffer:
        await aigie._buffer.add(EventType.SPAN_CREATE, complete)
    _run_agent_quality_assessment(handler, aigie, complete)
    return complete, agent_span_data, status, error_message


async def _close_invocation_and_emit_trace_update(
    handler: StrandsHandler, aigie: Any, event: AfterInvocationEvent
) -> str:
    """Run all the close-out steps in order; return final ``status`` for the debug log."""
    if handler._pending_llm_span:
        await finalize_pending_llm_span(handler, event.agent)
    result: AgentResult | None = event.result
    complete, agent_span_data, status, error_message = await _emit_complete_agent_span(
        handler, aigie, event, result
    )
    end_time = utc_now()
    trace_output, detected_drifts, plan_data = build_trace_summary(
        handler, complete, end_time, result
    )
    trace_update = build_trace_update(
        handler,
        event,
        end_time,
        status,
        error_message,
        trace_output,
        detected_drifts,
        plan_data,
        agent_span_data,
    )
    await finalize_trace_emission(handler, aigie, trace_update)
    return status


async def on_after_invocation(handler: StrandsHandler, event: AfterInvocationEvent) -> None:
    """Handle AfterInvocationEvent - complete agent span and trace."""
    if not handler.config.enabled or not handler.config.trace_agents:
        return
    if not handler.agent_span_id:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        status = await _close_invocation_and_emit_trace_update(handler, aigie, event)
        logger.debug(f"[AIGIE] Trace completed: {handler.trace_id} (status={status})")
    except Exception as e:
        logger.error(f"[AIGIE] Error in on_after_invocation: {e}", exc_info=True)
        from . import complete_pending as _cp

        await _cp.emit_error_close(handler, aigie, e)
    finally:
        from . import complete_pending as _cp

        _cp.finalize_invocation_cleanup(handler)
