"""LangChain token-usage / cost extraction → canonical ``Usage`` metadata.

Shared by every integration that rides langchain_core's callback contract
(LangGraph + LangChain). LangChain hides token usage in many provider-specific
locations on the ``LLMResult``; ``extract_langchain_usage`` walks all known
paths. The result is funneled through the shared ``Usage`` so the wire
placement of the prompt/completion split is owned in exactly one place rather
than re-derived per integration.
"""

from __future__ import annotations

from aigie.cost_tracking import UsageMetadata, calculate_cost
from aigie.tracing.usage import llm_span_payload


def _normalize_usage(raw: object) -> dict[str, int] | None:
    if raw is None:
        return None
    if isinstance(raw, dict):
        d = raw
    elif hasattr(raw, "prompt_tokens") or hasattr(raw, "input_tokens"):
        d = {
            "prompt_tokens": getattr(raw, "prompt_tokens", 0) or getattr(raw, "input_tokens", 0),
            "completion_tokens": (
                getattr(raw, "completion_tokens", 0) or getattr(raw, "output_tokens", 0)
            ),
            "total_tokens": getattr(raw, "total_tokens", 0),
        }
    else:
        return None
    prompt = d.get("prompt_tokens") or d.get("input_tokens") or 0
    completion = d.get("completion_tokens") or d.get("output_tokens") or 0
    total = d.get("total_tokens") or (prompt + completion)
    if prompt == 0 and completion == 0 and total == 0:
        return None
    return {
        "prompt_tokens": int(prompt),
        "completion_tokens": int(completion),
        "total_tokens": int(total),
    }


def _iter_usage_sources(response: object):
    """Yield candidate usage payloads from every known LangChain location."""
    llm_output = getattr(response, "llm_output", None)
    if isinstance(llm_output, dict):
        yield llm_output.get("token_usage")
        yield llm_output.get("usage")
        rmeta = llm_output.get("response_metadata")
        if isinstance(rmeta, dict):
            yield rmeta.get("token_usage")
            yield rmeta.get("usage")
    try:
        gen = getattr(response, "generations", [])[0][0]
    except Exception:  # noqa: BLE001
        return
    gen_info = getattr(gen, "generation_info", None)
    if isinstance(gen_info, dict):
        yield gen_info.get("usage_metadata")
        yield gen_info.get("token_usage")
        yield gen_info.get("usage")
    msg = getattr(gen, "message", None)
    if msg is not None:
        yield getattr(msg, "usage_metadata", None)


def extract_langchain_usage(response: object) -> dict[str, int] | None:
    """Walk LangChain's LLMResult shape to find token usage.

    Token usage lands in many places depending on provider — ``llm_output``
    (OpenAI/Anthropic via langchain_aws), nested ``response_metadata``,
    ``generation_info["usage_metadata"]`` (modern LangChain), or
    ``message.usage_metadata`` (chat models with AIMessage).
    """
    for raw in _iter_usage_sources(response):
        found = _normalize_usage(raw)
        if found:
            return found
    return None


def _calculate_cost(usage: dict[str, int], model_id: str | None) -> dict[str, float] | None:
    """Compute input/output/total cost. Best-effort: None on unknown model/error."""
    if not model_id:
        return None
    try:
        breakdown = calculate_cost(
            UsageMetadata(
                input_tokens=usage["prompt_tokens"],
                output_tokens=usage["completion_tokens"],
                total_tokens=usage["total_tokens"],
            ),
            model_override=model_id,
        )
    except Exception:  # noqa: BLE001
        return None
    if breakdown is None:
        return None
    return {
        "input_cost": float(getattr(breakdown, "input_cost", 0.0) or 0.0),
        "output_cost": float(getattr(breakdown, "output_cost", 0.0) or 0.0),
        "total_cost": float(getattr(breakdown, "total_cost", 0.0) or 0.0),
    }


def usage_payload(
    response: object, model_id: str | None
) -> tuple[dict[str, object], dict[str, object]]:
    """Return ``(extras, metadata_updates)`` for an LLM-end span.

    ``metadata_updates`` is ``Usage.to_metadata()`` (the canonical placement the
    ingest mapper reads). ``extras`` re-states the flat split at the payload top
    level for back-compat; the forgiving mapper accepts either. Returns two
    empty dicts when no usage is found.
    """
    usage = extract_langchain_usage(response)
    if usage is None:
        return {}, {}
    cost = _calculate_cost(usage, model_id)
    # model rides extras via the caller (lc_callback_base), so it's not passed here.
    return llm_span_payload(usage, cost=cost)
