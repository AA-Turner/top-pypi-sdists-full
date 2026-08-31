"""Token counts and pricing for a Bedrock call.

Bedrock reports usage in three different places depending on the model - the
response body, an `amazon-bedrock-invocationMetrics` block, or response headers
- so finding them is its own job, and it lives here rather than in the wrapper.
"""

from __future__ import annotations

import logging
from typing import Any

from aigie.cost_tracking import extract_and_calculate_cost
from aigie.wrappers._base import contained

logger = logging.getLogger(__name__)

PROVIDER = "bedrock"


def record_usage(run_ctx: Any, usage: dict[str, int] | None, model_id: str) -> None:
    """Put token counts on the span and price them. The three callers' shared tail."""
    if usage is None:
        return
    run_ctx.metadata["usage"] = usage
    contained("pricing the Bedrock call", record_cost, run_ctx, usage, model_id)


def record_cost(run_ctx: Any, usage: dict[str, int], model_id: str) -> None:
    """Price the call from its token counts, if the model has a price."""
    cost = extract_and_calculate_cost(
        {
            "amazon-bedrock-invocationMetrics": {
                "inputTokenCount": usage["prompt_tokens"],
                "outputTokenCount": usage["completion_tokens"],
            }
        },
        PROVIDER,
        model_override=model_id,
    )
    if not cost:
        logger.debug("[wrapper] No Bedrock price for model %s", model_id)
        return

    run_ctx.metadata["cost"] = {
        "input_cost": float(cost.input_cost),
        "output_cost": float(cost.output_cost),
        "total_cost": float(cost.total_cost),
        "currency": cost.currency,
    }


def usage_dict(
    prompt_tokens: int, completion_tokens: int, reported_total: int | None = None
) -> dict[str, int]:
    """Token counts for one call.

    `reported_total` wins over the sum when the provider sent one: with prompt
    caching a Bedrock `converse` reports a `totalTokens` far above
    `inputTokens + outputTokens`, and recomputing it silently under-reports the
    call.
    """
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": reported_total
        if reported_total is not None
        else prompt_tokens + completion_tokens,
    }


def usage_from(parsed: dict[str, Any], response: Any) -> dict[str, int] | None:
    """Token counts, from whichever of Bedrock's three places carries them.

    Which one depends on the model, so all three are tried rather than guessed.
    """
    found = _usage_from_body(parsed) or usage_from_metrics(parsed) or _usage_from_headers(response)
    return usage_dict(*found) if found else None


def counts(source: dict[str, Any], prompt_key: str, completion_key: str) -> tuple[int, int] | None:
    """Two token counts from one source, or `None` when it carries neither.

    Absent is not zero: models name these keys differently, so `.get(key, 0)`
    would return a truthy `(0, 0)` and end the search before the headers, which
    carry the real numbers for every model.
    """
    prompt = source.get(prompt_key)
    completion = source.get(completion_key)
    if prompt is None and completion is None:
        return None
    return int(prompt or 0), int(completion or 0)


def _usage_from_body(parsed: dict[str, Any]) -> tuple[int, int] | None:
    """Anthropic-on-Bedrock reports usage in the response body."""
    usage = parsed.get("usage")
    if not isinstance(usage, dict):
        return None
    return counts(usage, "input_tokens", "output_tokens")


def usage_from_metrics(parsed: dict[str, Any]) -> tuple[int, int] | None:
    """Streamed responses carry an invocation-metrics block on the last chunk."""
    metrics = parsed.get("amazon-bedrock-invocationMetrics")
    if not isinstance(metrics, dict):
        return None
    return counts(metrics, "inputTokenCount", "outputTokenCount")


def _usage_from_headers(response: Any) -> tuple[int, int] | None:
    """Every model reports counts in the response headers, whatever its body."""
    if not isinstance(response, dict):
        return None
    headers = (response.get("ResponseMetadata") or {}).get("HTTPHeaders") or {}
    return counts(headers, "x-amzn-bedrock-input-token-count", "x-amzn-bedrock-output-token-count")
