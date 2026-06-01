"""TRACE_UPDATE construction + finalization."""

from __future__ import annotations

import contextlib
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ....buffer import EventType
from .complete_pending import complete_pending_spans

if TYPE_CHECKING:
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import AfterInvocationEvent

logger = logging.getLogger(__name__)


def build_monitoring_data(handler: StrandsHandler, detected_drifts: list[Any]) -> dict[str, Any]:
    return {
        "drift_detection": {
            "plan": handler._drift_detector.plan.to_dict()
            if handler._drift_detector.plan
            else None,
            "execution": handler._drift_detector.execution.to_dict()
            if handler._drift_detector.execution
            else None,
            "detected_drifts": [d.to_dict() for d in detected_drifts],
            "drift_count": len(detected_drifts),
        },
        "error_detection": {
            "stats": handler._error_detector.stats.to_dict(),
            "detected_errors": [e.to_dict() for e in handler._detected_errors],
            "error_count": len(handler._detected_errors),
        },
    }


def build_execution_plan(
    handler: StrandsHandler,
    event: AfterInvocationEvent,
    duration_ms: float,
    status: str,
    detected_drifts_count: int,
    plan_data: dict[str, Any],
) -> dict[str, Any]:
    agent_name = getattr(event.agent, "name", "Strands Agent")
    total_tokens = handler._total_input_tokens + handler._total_output_tokens
    plan = {
        "agent": agent_name,
        "model_calls": handler._llm_call_count,
        "tool_calls": handler._total_tool_calls,
        "turn_count": handler._llm_call_count,
        "total_tokens": total_tokens,
        "total_cost": handler._total_cost,
        "duration_ms": duration_ms,
        "status": status,
        "error_count": len(handler._detected_errors),
        "drift_count": detected_drifts_count,
    }
    if plan_data.get("planned_steps"):
        plan["planned_steps"] = plan_data["planned_steps"]
    if plan_data.get("expected_tools"):
        plan["expected_tools"] = plan_data["expected_tools"]
    return plan


def build_remediation_summary(handler: StrandsHandler) -> dict[str, Any] | None:
    """Return the realtime_remediation summary block, or None if disabled."""
    if not handler.config.enable_realtime_remediation:
        return None
    engine = handler._remediation_engine
    return {
        "enabled": True,
        "mode": handler.config.remediation_mode,
        "applied_count": engine.applied_count if engine else 0,
        "results": [r.to_dict() for r in (engine.results[:10] if engine else [])],
    }


def build_trace_update(
    handler: StrandsHandler,
    event: AfterInvocationEvent,
    end_time: datetime,
    status: str,
    error_message: str | None,
    trace_output: dict[str, Any],
    detected_drifts: list[Any],
    plan_data: dict[str, Any],
    agent_span_data: dict[str, Any],
) -> dict[str, Any]:
    duration_ms = (
        (end_time - handler._invocation_start_time).total_seconds() * 1000
        if handler._invocation_start_time
        else 0.0
    )
    total_tokens = handler._total_input_tokens + handler._total_output_tokens
    agent_name = agent_span_data.get("agent_name", "Strands Agent")
    update: dict[str, Any] = {
        "id": handler.trace_id,
        "name": handler.trace_name or agent_name,
        "status": status,
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration_ms * 1_000_000),
        "output": trace_output,
        "total_tokens": total_tokens,
        "prompt_tokens": handler._total_input_tokens,
        "completion_tokens": handler._total_output_tokens,
        "total_cost": handler._total_cost,
        "metadata": {
            "total_tool_calls": handler._total_tool_calls,
            "total_input_tokens": handler._total_input_tokens,
            "total_output_tokens": handler._total_output_tokens,
            "total_tokens": total_tokens,
            "total_cost": handler._total_cost,
            "last_agent": agent_name,
            "turn_count": handler._llm_call_count,
            "execution_plan": build_execution_plan(
                handler, event, duration_ms, status, len(detected_drifts), plan_data
            ),
            "monitoring": build_monitoring_data(handler, detected_drifts),
            "realtime_remediation": build_remediation_summary(handler),
        },
    }
    if plan_data:
        update["metadata"]["agent_plan"] = plan_data
    if error_message:
        update["error"] = error_message
        update["error_message"] = error_message
    return update


async def finalize_trace_emission(
    handler: StrandsHandler,
    aigie: Any,
    trace_update: dict[str, Any],
) -> None:
    """Emit TRACE_UPDATE, clean up pending spans, then re-send TRACE_CREATE to restore name.

    The backend's auto-create on first SPAN can overwrite the trace name; re-emit
    TRACE_CREATE after spans land so the original name wins.
    """
    if aigie._buffer:
        await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)
    await complete_pending_spans(handler)
    await aigie._buffer.flush()
    await aigie._buffer.add(
        EventType.TRACE_CREATE, {"id": handler.trace_id, "name": trace_update["name"]}
    )
    await aigie._buffer.flush()


def build_trace_summary(
    handler: StrandsHandler,
    complete_agent_span: dict[str, Any],
    end_time: datetime,
    result: Any,
) -> tuple[dict[str, Any], list[Any], dict[str, Any]]:
    """Finalize drift detector and build the (trace_output, detected_drifts, plan_data) triple."""
    trace_output: dict[str, Any] = {}
    if handler.config.capture_outputs and complete_agent_span.get("output"):
        trace_output["response"] = complete_agent_span["output"]
    duration_ms = (
        (end_time - handler._invocation_start_time).total_seconds() * 1000
        if handler._invocation_start_time
        else 0.0
    )
    total_tokens = handler._total_input_tokens + handler._total_output_tokens
    final_output = (
        str(result)[:500] if (handler.config.capture_outputs and result is not None) else None
    )
    detected_drifts = handler._drift_detector.finalize(
        total_duration_ms=duration_ms,
        total_tokens=total_tokens,
        total_cost=handler._total_cost,
        final_output=final_output,
    )
    if detected_drifts:
        logger.info(f"[AIGIE] Drift detection summary: {len(detected_drifts)} drifts detected")
    if handler._detected_errors:
        logger.info(
            f"[AIGIE] Error detection summary: {len(handler._detected_errors)} errors detected"
        )
    trace_output["monitoring"] = {
        "drift_count": len(detected_drifts),
        "error_count": len(handler._detected_errors),
        "plan_captured": handler._drift_detector._plan_captured,
    }
    plan_data = handler._drift_detector.plan.to_dict() if handler._drift_detector.plan else {}
    return trace_output, detected_drifts, plan_data
