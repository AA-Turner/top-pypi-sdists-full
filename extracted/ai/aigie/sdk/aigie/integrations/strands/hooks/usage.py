"""Token-usage extraction helpers for the Strands integration.

These are pure functions (no handler state) that probe Strands events,
agents, and stop_responses for input/output token counts.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_current_accumulated_usage(agent: Any) -> dict[str, int]:
    """Read accumulated input/output tokens from the agent's event-loop metrics.

    Used to capture a "before" snapshot so per-call tokens can be derived as a
    delta after the model call completes. Returns zeroes if metrics aren't
    available.
    """
    result = {"inputTokens": 0, "outputTokens": 0}
    try:
        metrics = getattr(agent, "event_loop_metrics", None)
        if metrics is None:
            logger.debug("[AIGIE] Agent has no event_loop_metrics attribute")
            return result
        usage = getattr(metrics, "accumulated_usage", None)
        if not usage:
            logger.debug("[AIGIE] No accumulated_usage in metrics")
            return result
        result["inputTokens"] = usage.get("inputTokens", 0) or 0
        result["outputTokens"] = usage.get("outputTokens", 0) or 0
        logger.debug(f"[AIGIE] Got accumulated usage from metrics: {result}")
    except Exception as e:
        logger.debug(f"[AIGIE] Error getting accumulated usage: {e}")
    return result


def _coerce_usage_dict(usage: Any) -> dict[str, int] | None:
    """Normalize a usage dict (any of the provider-specific key spellings)."""
    if not isinstance(usage, dict):
        return None
    input_tokens = (
        usage.get("inputTokens", 0)
        or usage.get("input_tokens", 0)
        or usage.get("prompt_tokens", 0)
        or usage.get("prompt_token_count", 0)
        or 0
    )
    output_tokens = (
        usage.get("outputTokens", 0)
        or usage.get("output_tokens", 0)
        or usage.get("completion_tokens", 0)
        or usage.get("candidates_token_count", 0)
        or 0
    )
    if input_tokens or output_tokens:
        return {"inputTokens": input_tokens, "outputTokens": output_tokens}
    return None


def _coerce_usage_obj(usage: Any) -> dict[str, int] | None:
    """Normalize a usage object exposing tokens as attributes."""
    input_tokens = (
        getattr(usage, "inputTokens", 0)
        or getattr(usage, "input_tokens", 0)
        or getattr(usage, "prompt_tokens", 0)
        or getattr(usage, "prompt_token_count", 0)
        or 0
    )
    output_tokens = (
        getattr(usage, "outputTokens", 0)
        or getattr(usage, "output_tokens", 0)
        or getattr(usage, "completion_tokens", 0)
        or getattr(usage, "candidates_token_count", 0)
        or 0
    )
    if input_tokens or output_tokens:
        return {"inputTokens": input_tokens, "outputTokens": output_tokens}
    return None


def coerce_usage(usage: Any) -> dict[str, int] | None:
    """Normalize either a usage dict or attribute-bearing object into ``{inputTokens, outputTokens}``."""
    if usage is None:
        return None
    if isinstance(usage, dict):
        return _coerce_usage_dict(usage)
    return _coerce_usage_obj(usage)


_coerce_usage = coerce_usage  # backward-compat alias for internal callers


def _usage_from_message(stop_response: Any) -> Any:
    """Probe stop_response.message for usage data (incl. Gemini layout)."""
    msg = getattr(stop_response, "message", None)
    if msg is None:
        return None
    direct = getattr(msg, "usage", None)
    if direct:
        return direct
    content = getattr(msg, "content", None)
    if isinstance(content, list) and content:
        first = content[0]
        return getattr(first, "usage_metadata", None)
    return None


def _usage_from_response(stop_response: Any) -> Any:
    """Probe stop_response.response for usage / usage_metadata."""
    resp = getattr(stop_response, "response", None)
    if resp is None:
        return None
    return getattr(resp, "usage", None) or getattr(resp, "usage_metadata", None)


def _usage_from_metrics(stop_response: Any) -> Any:
    """Probe stop_response.metrics for usage in Strands' various layouts."""
    metrics = getattr(stop_response, "metrics", None)
    if metrics is None:
        return None
    if hasattr(metrics, "usage") and metrics.usage:
        return metrics.usage
    if isinstance(metrics, dict):
        if "usage" in metrics:
            return metrics["usage"]
        if "inputTokens" in metrics or "input_tokens" in metrics:
            return metrics
    return None


def extract_usage_from_stop_response(stop_response: Any) -> dict[str, int] | None:
    """Pull token usage out of a Strands StopResponse.

    Probes the standard locations (direct ``usage``, ``message.usage``,
    ``response.usage``, ``metrics.usage``) and normalizes the result.
    """
    if not stop_response:
        return None
    try:
        candidates = (
            getattr(stop_response, "usage", None),
            _usage_from_message(stop_response),
            _usage_from_response(stop_response),
            _usage_from_metrics(stop_response),
        )
        for raw in candidates:
            normalized = _coerce_usage(raw)
            if normalized is not None:
                return normalized
    except Exception as e:
        logger.debug(f"[AIGIE] Could not extract usage from stop_response: {e}")
    return None


def _usage_from_event_metrics(event: Any) -> dict[str, int] | None:
    """Probe ``event.metrics['usage']``."""
    metrics = getattr(event, "metrics", None)
    if not isinstance(metrics, dict):
        return None
    return _coerce_usage_dict(metrics.get("usage"))


def _usage_from_event_attrs(event: Any) -> dict[str, int] | None:
    """Probe inputTokens/outputTokens directly attached to the event."""
    if not (hasattr(event, "input_tokens") or hasattr(event, "inputTokens")):
        return None
    input_tokens = getattr(event, "inputTokens", 0) or getattr(event, "input_tokens", 0) or 0
    output_tokens = getattr(event, "outputTokens", 0) or getattr(event, "output_tokens", 0) or 0
    if input_tokens or output_tokens:
        return {"inputTokens": input_tokens, "outputTokens": output_tokens}
    return None


def _usage_from_event_agent(event: Any) -> dict[str, int] | None:
    """Probe ``event.agent.last_response_usage``."""
    agent = getattr(event, "agent", None)
    if agent is None:
        return None
    usage = getattr(agent, "last_response_usage", None)
    return _coerce_usage_dict(usage)


def extract_usage_from_event(event: Any) -> dict[str, int] | None:
    """Pull token usage out of an AfterModelCallEvent."""
    if not event:
        return None
    try:
        direct = _coerce_usage_dict(getattr(event, "usage", None))
        if direct:
            return direct
        for fn in (_usage_from_event_metrics, _usage_from_event_attrs, _usage_from_event_agent):
            normalized = fn(event)
            if normalized:
                return normalized
    except Exception as e:
        logger.debug(f"[AIGIE] Could not extract usage from event: {e}")
    return None


def extract_model_id(model: Any) -> str | None:
    """Best-effort model id extraction across Strands model implementations."""
    if not model:
        return None
    for attr in ("model_id", "_model_id"):
        val = getattr(model, attr, None)
        if isinstance(val, str):
            return val
    config = getattr(model, "config", None)
    if isinstance(config, dict):
        cid = config.get("model_id")
        return cid if isinstance(cid, str) else None
    cid = getattr(config, "model_id", None)
    if isinstance(cid, str):
        return cid
    if isinstance(getattr(model, "client_args", None), dict):
        return type(model).__name__.replace("Model", "").lower()
    return None
