"""LLM/model hook bodies for the Strands integration."""

from __future__ import annotations

import contextlib
import logging
import uuid
from typing import TYPE_CHECKING, Any

from ._shared import format_messages_for_span, utc_now
from .llm_finalize import finalize_pending_llm_span
from .usage import (
    extract_model_id,
    extract_usage_from_event,
    extract_usage_from_stop_response,
    get_current_accumulated_usage,
)

if TYPE_CHECKING:
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import AfterModelCallEvent, BeforeModelCallEvent

logger = logging.getLogger(__name__)


def _try_inject_pending_quality_fix(handler: StrandsHandler, event: BeforeModelCallEvent) -> None:
    """No-op (async judge fix injection removed with autonomous mode)."""
    return


def _extract_model_parameters(model_obj: Any) -> dict[str, Any]:
    """Pull common LLM parameters off a model object's config (or direct attrs)."""
    params: dict[str, Any] = {}
    config = getattr(model_obj, "config", None) or getattr(model_obj, "model_config", None)
    if config:
        for key in ("temperature", "top_p", "top_k", "max_tokens", "stop_sequences"):
            val = getattr(config, key, None)
            if val is None and isinstance(config, dict):
                val = config.get(key)
            if val is not None:
                params[key] = val
    for key in ("temperature", "top_p", "max_tokens"):
        if key not in params:
            val = getattr(model_obj, key, None)
            if val is not None:
                params[key] = val
    return params


def _capture_llm_input(
    handler: StrandsHandler, event: BeforeModelCallEvent, model_id: str | None
) -> dict[str, Any] | None:
    """Best-effort capture of the prompts going into a model call."""
    if not (handler.config.capture_inputs and hasattr(event.agent, "messages")):
        return None
    try:
        agent_msgs = event.agent.messages
        if not isinstance(agent_msgs, list) or not agent_msgs:
            return None
        return {
            "model": model_id,
            "prompts": format_messages_for_span(agent_msgs, handler.config.max_content_length),
        }
    except Exception:
        return None


def _register_new_model_call(
    handler: StrandsHandler, event: BeforeModelCallEvent
) -> tuple[str, str | None]:
    """Allocate a span_id, register depth + state, return (span_id, model_id)."""
    span_id = str(uuid.uuid4())
    start_time = utc_now()
    handler._llm_call_count += 1
    start_tokens = get_current_accumulated_usage(event.agent)
    model_id = extract_model_id(event.agent.model) if hasattr(event.agent, "model") else None
    llm_depth = handler._register_span_depth(span_id, handler._current_parent_span_id)
    model_parameters = (
        _extract_model_parameters(event.agent.model) if hasattr(event.agent, "model") else {}
    )
    handler.model_call_map[span_id] = {
        "startTime": start_time,
        "startTokens": start_tokens,
        "modelId": model_id,
        "depth": llm_depth,
        "parentId": handler._current_parent_span_id,
        "modelParameters": model_parameters or None,
        "llm_input": _capture_llm_input(handler, event, model_id),
    }
    handler.model_span_id = span_id
    handler.model_start_time = start_time
    handler._model_call_start_tokens = start_tokens
    return span_id, model_id


async def on_before_model_call(handler: StrandsHandler, event: BeforeModelCallEvent) -> None:
    """Finalize the prior pending LLM span and prepare state for a new model call.

    Strands updates ``accumulated_usage`` *after* AfterModelCallEvent, so we defer
    creating each LLM span until the next BeforeModelCallEvent (or after_invocation),
    when the previous call's tokens have landed in the metrics.
    """
    if not handler.config.enabled or not handler.config.trace_llm_calls:
        return
    if not handler._current_parent_span_id or not handler.trace_id:
        return
    try:
        with contextlib.suppress(Exception):
            _try_inject_pending_quality_fix(handler, event)
        if handler._pending_llm_span:
            await finalize_pending_llm_span(handler, event.agent)
        span_id, model_id = _register_new_model_call(handler, event)
        logger.debug(
            f"[AIGIE] LLM call #{handler._llm_call_count} started: model={model_id} (id={span_id})"
        )
    except Exception as e:
        logger.error(f"[AIGIE] Error in on_before_model_call: {e}", exc_info=True)


def _resolve_after_call_status(
    handler: StrandsHandler, event: AfterModelCallEvent
) -> tuple[str, bool, str | None]:
    """Return (status, is_error, error_str) for an AfterModelCallEvent."""
    if not event.exception:
        return "success", False, None
    handler._has_errors = True
    error_str = str(event.exception)
    if error_str and error_str not in handler._error_messages:
        handler._error_messages.append(error_str)
    return "error", True, error_str


def _build_after_call_output(
    handler: StrandsHandler,
    event: AfterModelCallEvent,
    model_id: str | None,
    status: str,
    response_usage: dict[str, int] | None,
) -> tuple[dict[str, Any] | None, str | None]:
    """Return (structured_output_or_None, stop_reason_or_None)."""
    if not event.stop_response:
        return None, None
    stop_reason = str(event.stop_response.stop_reason)
    if not handler.config.capture_outputs:
        return None, stop_reason
    response_text = str(event.stop_response.message)
    if len(response_text) > handler.config.max_content_length:
        response_text = response_text[: handler.config.max_content_length] + "..."
    structured: dict[str, Any] = {
        "model": model_id,
        "status": status,
        "response": response_text,
        "finish_reason": stop_reason,
    }
    if response_usage:
        in_tok = response_usage.get("inputTokens", 0)
        out_tok = response_usage.get("outputTokens", 0)
        structured["token_usage"] = {
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
        }
    return structured, stop_reason


def _build_after_call_input(
    handler: StrandsHandler,
    event: AfterModelCallEvent,
    model_id: str | None,
    fallback: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Build the structured input dict, falling back to the BeforeModelCall capture."""
    if not (handler.config.capture_inputs and hasattr(event, "messages") and event.messages):
        return fallback
    try:
        prompts = format_messages_for_span(event.messages, handler.config.max_content_length)
    except Exception:
        prompts = [
            {"role": "user", "content": str(event.messages)[: handler.config.max_content_length]}
        ]
    return {"model": model_id, "prompts": prompts}


def _run_llm_quality_evaluation(
    handler: StrandsHandler,
    event: AfterModelCallEvent,
    span_id: str,
    output_repr: dict[str, Any] | None,
    model_id: str | None,
    error_str: str | None,
) -> None:
    """No-op: step assessor removed in P13."""


def _record_llm_error_detection(
    handler: StrandsHandler, event: AfterModelCallEvent, model_id: str | None
) -> None:
    """Classify model exceptions and assistant-message error content.

    Why both: provider transport errors surface via ``event.exception`` (rate limit,
    network, etc.), while error content embedded inside an otherwise-successful
    response (a model returning ``"I encountered an error: ..."``) only shows up
    in ``stop_response.message``. We feed each into the appropriate detector.
    """
    if event.exception is not None:
        handler.record_detection(
            handler._error_detector.detect_from_exception(
                event.exception,
                source=f"llm:{model_id or 'unknown'}",
                context={"model": model_id},
            )
        )
        return
    stop_response = getattr(event, "stop_response", None)
    message = getattr(stop_response, "message", None) if stop_response is not None else None
    if message is None:
        return
    handler.record_detection(
        handler._error_detector.detect_from_llm_response(message, model=model_id)
    )


def _cleanup_after_model_call(handler: StrandsHandler, span_id: str) -> None:
    handler.model_call_map.pop(span_id, None)
    handler.model_span_id = None
    handler.model_start_time = None
    handler._model_call_start_tokens = None


async def on_after_model_call(handler: StrandsHandler, event: AfterModelCallEvent) -> None:
    """Queue an LLM span for deferred creation (tokens land in the next event)."""
    if not handler.config.enabled or not handler.config.trace_llm_calls:
        return
    if not handler.model_span_id:
        return
    span_id = handler.model_span_id

    try:
        output_repr, model_id, error_str = _queue_pending_llm_span(handler, event, span_id)
        logger.debug(f"[AIGIE] LLM span queued for deferred creation: {span_id} (model={model_id})")
        try:
            _record_llm_error_detection(handler, event, model_id)
        except Exception as e:
            logger.warning(f"[AIGIE] _record_llm_error_detection failed: {e}")
        with contextlib.suppress(Exception):
            _run_llm_quality_evaluation(handler, event, span_id, output_repr, model_id, error_str)
    except Exception as e:
        logger.error(f"[AIGIE] Error in on_after_model_call: {e}", exc_info=True)
    finally:
        _cleanup_after_model_call(handler, span_id)


def _queue_pending_llm_span(
    handler: StrandsHandler, event: AfterModelCallEvent, span_id: str
) -> tuple[dict[str, Any] | None, str | None, str | None]:
    """Build & store the pending LLM span; return (output, model_id, error_str)."""
    model_data = handler.model_call_map.get(span_id, {})
    status, is_error, error_str = _resolve_after_call_status(handler, event)
    model_id = model_data.get("modelId")
    if not model_id and hasattr(event.agent, "model"):
        model_id = extract_model_id(event.agent.model)
    response_usage = extract_usage_from_stop_response(event.stop_response)
    event_usage = extract_usage_from_event(event) if not response_usage else None
    output_repr, stop_reason = _build_after_call_output(
        handler, event, model_id, status, response_usage
    )
    input_repr = _build_after_call_input(handler, event, model_id, model_data.get("llm_input"))
    handler._pending_llm_span = {
        "span_id": span_id,
        "start_time": model_data.get("startTime") or handler.model_start_time,
        "end_time": utc_now(),
        "start_tokens": model_data.get("startTokens") or handler._model_call_start_tokens,
        "model_id": model_id,
        "parent_id": model_data.get("parentId") or handler._current_parent_span_id,
        "depth": model_data.get("depth", 1),
        "status": status,
        "is_error": is_error,
        "error_str": error_str,
        "error_type": "LLMError" if is_error else None,
        "response_usage": response_usage,
        "event_usage": event_usage,
        "output": output_repr,
        "input": input_repr,
        "stop_reason": stop_reason,
        "model_parameters": model_data.get("modelParameters"),
    }
    return output_repr, model_id, error_str
