"""Finalize a deferred LLM span — emit SPAN_CREATE once tokens are available."""

from __future__ import annotations

import contextlib
import logging
from typing import TYPE_CHECKING, Any

from ....buffer import EventType
from ..cost_tracking import calculate_strands_cost
from .usage import get_current_accumulated_usage

if TYPE_CHECKING:
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands import Agent

logger = logging.getLogger(__name__)


def _resolve_call_tokens(pending: dict[str, Any], agent: Agent) -> tuple[int, int]:
    """Determine per-call (input, output) tokens for a pending LLM span."""
    response_usage = pending.get("response_usage")
    event_usage = pending.get("event_usage")
    if response_usage and (
        response_usage.get("inputTokens", 0) > 0 or response_usage.get("outputTokens", 0) > 0
    ):
        in_tok = response_usage.get("inputTokens", 0)
        out_tok = response_usage.get("outputTokens", 0)
        logger.debug(f"[AIGIE] LLM tokens from stop_response: in={in_tok}, out={out_tok}")
        return in_tok, out_tok
    if event_usage and (
        event_usage.get("inputTokens", 0) > 0 or event_usage.get("outputTokens", 0) > 0
    ):
        in_tok = event_usage.get("inputTokens", 0)
        out_tok = event_usage.get("outputTokens", 0)
        logger.debug(f"[AIGIE] LLM tokens from event: in={in_tok}, out={out_tok}")
        return in_tok, out_tok
    start_tokens = pending.get("start_tokens", {"inputTokens": 0, "outputTokens": 0})
    current = get_current_accumulated_usage(agent)
    in_tok = max(0, current["inputTokens"] - start_tokens.get("inputTokens", 0))
    out_tok = max(0, current["outputTokens"] - start_tokens.get("outputTokens", 0))
    logger.debug(f"[AIGIE] LLM tokens from delta: in={in_tok}, out={out_tok}")
    return in_tok, out_tok


def _calculate_call_cost(
    model_id: str | None, in_tok: int, out_tok: int
) -> tuple[float, float, float]:
    """Compute (total, input_cost, output_cost) — split 40/60 per the legacy ratio."""
    try:
        total = calculate_strands_cost(
            model_id=model_id, input_tokens=in_tok, output_tokens=out_tok
        )
    except Exception:
        total = 0.0
    return total, total * 0.4 if total else 0, total * 0.6 if total else 0


def _extract_usage_details(pending: dict[str, Any]) -> dict[str, int]:
    """Pull cache + reasoning tokens out of pending response/event usage dicts."""
    details: dict[str, int] = {}
    candidates = (pending.get("response_usage") or {}, pending.get("event_usage") or {})
    if not any(candidates):
        return details
    for src in candidates:
        if not src:
            continue
        for key in ("cacheReadInputTokens", "cache_read_input_tokens"):
            if src.get(key):
                details["cache_read_input_tokens"] = src[key]
        for key in ("cacheCreationInputTokens", "cache_creation_input_tokens"):
            if src.get(key):
                details["cache_creation_input_tokens"] = src[key]
        for key in ("reasoningTokens", "reasoning_tokens"):
            if src.get(key):
                details["reasoning_tokens"] = src[key]
    return details


def _build_llm_span_metadata(
    pending: dict[str, Any],
    in_tok: int,
    out_tok: int,
    cost: float,
    in_cost: float,
    out_cost: float,
    duration_ms: float,
) -> dict[str, Any]:
    model_id = pending["model_id"]
    total_tokens = in_tok + out_tok
    metadata: dict[str, Any] = {
        "service": "llm",
        "framework": "strands",
        "model": model_id,
        "model_id": model_id,
        "depth": pending["depth"],
        "duration_ms": duration_ms,
        "status": pending["status"],
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "prompt_tokens": in_tok,
        "completion_tokens": out_tok,
        "total_tokens": total_tokens,
        "input_cost": in_cost,
        "output_cost": out_cost,
        "total_cost": cost,
        "cost": cost,
        "token_usage": {
            "prompt_tokens": in_tok,
            "completion_tokens": out_tok,
            "total_tokens": total_tokens,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "input_cost": in_cost,
            "output_cost": out_cost,
            "total_cost": cost,
        },
    }
    details = _extract_usage_details(pending)
    if details:
        metadata["usage_details"] = details
    return metadata


def _build_llm_span_data(
    handler: StrandsHandler,
    pending: dict[str, Any],
    in_tok: int,
    out_tok: int,
    cost: float,
    in_cost: float,
    out_cost: float,
    duration_ms: float,
) -> dict[str, Any]:
    span_id = pending["span_id"]
    start_time = pending["start_time"]
    end_time = pending["end_time"]
    model_id = pending["model_id"]
    total_tokens = in_tok + out_tok
    metadata = _build_llm_span_metadata(
        pending, in_tok, out_tok, cost, in_cost, out_cost, duration_ms
    )
    span: dict[str, Any] = {
        "id": span_id,
        "trace_id": handler.trace_id,
        "parent_id": pending["parent_id"],
        "name": f"LLM: {model_id}" if model_id else "LLM",
        "type": "llm",
        "start_time": start_time.isoformat() if start_time else end_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_ns": int(duration_ms * 1_000_000),
        "status": pending["status"],
        "metadata": metadata,
        "token_usage": {
            "prompt_tokens": in_tok,
            "completion_tokens": out_tok,
            "total_tokens": total_tokens,
            "unit": "TOKENS",
            "input_cost": in_cost,
            "output_cost": out_cost,
            "total_cost": cost,
        },
        "usage": {
            "prompt_tokens": in_tok,
            "completion_tokens": out_tok,
            "total_tokens": total_tokens,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "input_cost": in_cost,
            "output_cost": out_cost,
            "total_cost": cost,
        },
        "prompt_tokens": in_tok,
        "completion_tokens": out_tok,
        "total_tokens": total_tokens,
        "input_cost": in_cost,
        "output_cost": out_cost,
        "total_cost": cost,
    }
    _attach_optional_fields(span, handler, pending, model_id)
    return span


def _attach_optional_fields(
    span: dict[str, Any],
    handler: StrandsHandler,
    pending: dict[str, Any],
    model_id: str | None,
) -> None:
    """Attach model/user/session/input/output/stop_reason/error to ``span`` in place."""
    if model_id:
        span["model"] = model_id
    if handler.user_id:
        span["user_id"] = handler.user_id
    if handler.session_id:
        span["session_id"] = handler.session_id
    if pending.get("input"):
        span["input"] = pending["input"]
    if pending.get("output"):
        span["output"] = pending["output"]
    if pending.get("model_parameters"):
        span["metadata"]["model_parameters"] = pending["model_parameters"]
    if pending.get("stop_reason"):
        span["metadata"]["stop_reason"] = pending["stop_reason"]
        span["metadata"]["finish_reason"] = pending["stop_reason"]
    _attach_error_fields(span, pending)


def _attach_error_fields(span: dict[str, Any], pending: dict[str, Any]) -> None:
    err = pending.get("error_str")
    if not err:
        return
    err_type = pending.get("error_type", "LLMError")
    span["error"] = span["error_message"] = err
    span["error_type"] = err_type
    span["metadata"]["error"] = err
    span["metadata"]["error_type"] = err_type


async def finalize_pending_llm_span(handler: StrandsHandler, agent: Agent) -> None:
    """Finalize a pending LLM span by calculating tokens and creating it.

    Called from on_before_model_call (for intermediate calls) or
    on_after_invocation (for the last call). At these points,
    accumulated_usage has been updated with the call's tokens.
    """
    pending = handler._pending_llm_span
    if not pending:
        return
    handler._pending_llm_span = None  # Clear immediately to prevent double-finalization
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        in_tok, out_tok = _resolve_call_tokens(pending, agent)
        cost, in_cost, out_cost = _calculate_call_cost(pending["model_id"], in_tok, out_tok)
        start_time = pending["start_time"]
        end_time = pending["end_time"]
        duration_ms = (end_time - start_time).total_seconds() * 1000 if start_time else 0.0
        span_data = _build_llm_span_data(
            handler, pending, in_tok, out_tok, cost, in_cost, out_cost, duration_ms
        )
        await aigie._buffer.add(EventType.SPAN_CREATE, span_data)
        logger.debug(
            f"[AIGIE] LLM span created (deferred): {pending['span_id']} "
            f"(in={in_tok}, out={out_tok}, status={pending['status']})"
        )
    except Exception as e:
        logger.error(f"[AIGIE] Error finalizing pending LLM span: {e}", exc_info=True)
