"""OpenAI-compatible usage parsing helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..runtime import ModelUsage


def openai_compatible_usage_from_payload(payload: Mapping[str, Any]) -> ModelUsage:
    usage_payload = payload.get("usage", {})
    if not isinstance(usage_payload, dict):
        return ModelUsage()
    prompt_tokens = int(usage_payload.get("prompt_tokens", usage_payload.get("input_tokens", 0)))
    completion_tokens = int(usage_payload.get("completion_tokens", usage_payload.get("output_tokens", 0)))
    total_tokens = int(usage_payload.get("total_tokens", prompt_tokens + completion_tokens))
    prompt_details = usage_payload.get("prompt_tokens_details", usage_payload.get("input_tokens_details", {}))
    if not isinstance(prompt_details, Mapping):
        prompt_details = {}
    cached_prompt_tokens = int(
        prompt_details.get("cached_tokens")
        or prompt_details.get("cached_prompt_tokens")
        or usage_payload.get("cached_prompt_tokens")
        or usage_payload.get("cache_read_input_tokens")
        or usage_payload.get("cache_read_tokens")
        or 0
    )
    cache_creation_prompt_tokens = int(
        prompt_details.get("cache_creation_tokens")
        or prompt_details.get("cache_creation_prompt_tokens")
        or prompt_details.get("cache_creation_input_tokens")
        or usage_payload.get("cache_creation_prompt_tokens")
        or usage_payload.get("cache_creation_input_tokens")
        or usage_payload.get("cache_write_input_tokens")
        or 0
    )
    return ModelUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cached_prompt_tokens=cached_prompt_tokens,
        cache_creation_prompt_tokens=cache_creation_prompt_tokens,
        cache_usage_reported=bool(prompt_details) or cached_prompt_tokens > 0 or cache_creation_prompt_tokens > 0,
    )
