from collections.abc import Mapping

from opentelemetry.attributes import BoundedAttributes
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.util.types import AttributeValue


RESPONSE_MODEL = "gen_ai.response.model"

_STRING_ALIASES = {
    "gen_ai.provider.name": ("gen_ai.system", "ai.model.provider"),
    "gen_ai.request.model": ("ai.model.id", "ai.model"),
}

_NUMBER_ALIASES = {
    "gen_ai.usage.input_tokens": (
        "gen_ai.usage.prompt_tokens",
        "ai.usage.prompt_tokens",
        "ai.usage.promptTokens",
        "ai.usage.input_tokens",
        "ai.usage.inputTokens",
    ),
    "gen_ai.usage.output_tokens": (
        "gen_ai.usage.completion_tokens",
        "ai.usage.completion_tokens",
        "ai.usage.completionTokens",
        "ai.usage.output_tokens",
        "ai.usage.outputTokens",
    ),
    "gen_ai.usage.reasoning_tokens": (
        "gen_ai.usage.reasoning.output_tokens",
        "ai.usage.reasoningTokens",
        "ai.usage.thoughts_tokens",
    ),
    "gen_ai.usage.cache_read_input_tokens": (
        "gen_ai.usage.cache_read_tokens",
        "gen_ai.usage.cache_read.input_tokens",
        "ai.usage.cachedInputTokens",
        "ai.usage.cached_tokens",
        "ai.usage.cache_read_tokens",
        "ai.usage.cache_read_input_tokens",
        "ai.usage.cacheReadInputTokens",
    ),
    "gen_ai.usage.cache_write_input_tokens": (
        "gen_ai.usage.cache_creation_input_tokens",
        "gen_ai.usage.cache_creation.input_tokens",
        "ai.usage.cacheWriteInputTokens",
        "ai.usage.cache_creation_input_tokens",
        "ai.usage.cacheCreationInputTokens",
    ),
}


def _first_string(
    attributes: Mapping[str, AttributeValue], keys: tuple[str, ...]
) -> str | None:
    for key in keys:
        value = attributes.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _first_token_count(
    attributes: Mapping[str, AttributeValue], keys: tuple[str, ...]
) -> int | None:
    for key in keys:
        value = attributes.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int) and value >= 0:
            return value
        if isinstance(value, float) and value.is_integer() and value >= 0:
            return int(value)
    return None


def normalize_model_usage_attributes(
    attributes: Mapping[str, AttributeValue] | None,
) -> dict[str, AttributeValue] | None:
    if not attributes:
        return None

    response_model = _first_string(attributes, (RESPONSE_MODEL, "ai.response.model"))
    if response_model is None:
        return None

    original = dict(attributes)
    normalized = original.copy()
    normalized.setdefault(RESPONSE_MODEL, response_model)

    for target, aliases in _STRING_ALIASES.items():
        if target in normalized:
            continue
        value = _first_string(normalized, aliases)
        if value is not None:
            normalized[target] = value

    for target, aliases in _NUMBER_ALIASES.items():
        if target in normalized:
            continue
        value = _first_token_count(normalized, aliases)
        if value is not None:
            normalized[target] = value

    return normalized if normalized != original else None


def _bounded_attributes(
    source: BoundedAttributes,
    normalized: Mapping[str, AttributeValue],
) -> BoundedAttributes:
    original = dict(source)
    if source.maxlen is None or len(normalized) <= source.maxlen:
        attributes = normalized
    else:
        additions = {
            key: value for key, value in normalized.items() if key not in original
        }
        attributes = dict(reversed(tuple(additions.items())))
        attributes.update(original)

    bounded = BoundedAttributes(
        maxlen=source.maxlen,
        attributes=attributes,
        immutable=True,
        max_value_len=source.max_value_len,
    )
    rebuilt = dict(bounded)
    if any(
        key not in rebuilt or rebuilt[key] != value
        for key, value in original.items()
    ):
        raise ValueError("normalization changed existing span attributes")
    bounded.dropped += source.dropped
    return bounded


def normalize_model_usage_span(span: ReadableSpan) -> None:
    try:
        normalized = normalize_model_usage_attributes(span.attributes)
        if normalized is None:
            return

        if isinstance(span._attributes, BoundedAttributes):
            span._attributes = _bounded_attributes(span._attributes, normalized)
        else:
            span._attributes = normalized
    except Exception:
        return
