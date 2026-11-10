from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from bitfab.provider_calls import (
    ProviderCall,
    _field,
    _number,
    is_anthropic_url,
    is_openrouter_url,
    provider_call_for_usage,
)

MODEL_CALL_SPAN_TYPES = frozenset({"generation", "response"})
_TOKEN_CONTEXT_KEYS = (
    "inputTokens",
    "outputTokens",
    "cachedInputTokens",
    "cacheReadTokens",
    "costUsd",
)


def _model_responses(span_data: Mapping[str, Any]) -> tuple[Any, ...]:
    output = span_data.get("output")
    first_output = output[0] if isinstance(output, list) and output else None
    return (span_data, span_data.get("response"), first_output)


def _model_response(span_data: Mapping[str, Any]) -> Any:
    return next(
        (
            candidate
            for candidate in _model_responses(span_data)
            if _field(candidate, "usage") is not None
        ),
        None,
    )


def _model(span_data: Mapping[str, Any]) -> str | None:
    return next(
        (
            model
            for model in (
                _field(candidate, "model") for candidate in _model_responses(span_data)
            )
            if isinstance(model, str) and model
        ),
        None,
    )


def _provider(span_data: Mapping[str, Any], call: ProviderCall) -> str:
    base_url = _field(span_data.get("model_config"), "base_url")
    if is_openrouter_url(base_url):
        return "openrouter"
    if is_anthropic_url(base_url):
        return "anthropic"
    return call.provider


def _has_token_usage(context: Any) -> bool:
    return isinstance(context, Mapping) and any(
        _number(context.get(key)) is not None for key in _TOKEN_CONTEXT_KEYS
    )


def agents_sdk_usage_context(span_data: Any) -> dict[str, Any] | None:
    if not isinstance(span_data, Mapping):
        return None
    if span_data.get("type") not in MODEL_CALL_SPAN_TYPES:
        return None
    response = _model_response(span_data)
    if response is None:
        return None
    call = provider_call_for_usage(_field(response, "usage"))
    usage = call.usage({"model": _model(span_data)}, response)
    if "inputTokens" not in usage and "outputTokens" not in usage:
        return None
    return {"provider": _provider(span_data, call), **usage}


def add_agents_sdk_usage_context(span_data: dict[str, Any]) -> None:
    contexts = span_data.get("contexts")
    existing = contexts if isinstance(contexts, list) else []
    if any(_has_token_usage(context) for context in existing):
        return
    context = agents_sdk_usage_context(span_data)
    if context is None:
        return
    span_data["contexts"] = [*existing, context]
