"""SHA-256 canonical request hashing for fixture lookup."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from agentic_devtools.orchestration.llm.types import LLMMessage


def compute_fixture_key(
    *,
    node_type: str = "",
    model: str = "",
    messages: list[LLMMessage] | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    response_format: dict[str, Any] | None = None,
    additional_params: dict[str, Any] | None = None,
) -> str:
    """Compute deterministic SHA-256 hash for fixture lookup.

    Creates a canonical JSON representation of the request parameters
    with sorted keys, then hashes it to produce a fixture key.

    Args:
        node_type: Node type identifier.
        model: Model name.
        messages: Input messages.
        temperature: Temperature setting.
        max_tokens: Max tokens setting.
        response_format: Response format specification.
        additional_params: Additional provider kwargs that can affect model output.

    Returns:
        Hex-encoded SHA-256 hash string.
    """
    canonical: dict[str, Any] = {
        "node_type": node_type,
        "model": model,
        "messages": [{"role": m.role, "content": m.content, "name": m.name} for m in (messages or [])],
    }

    if temperature is not None:
        canonical["temperature"] = temperature
    if max_tokens is not None:
        canonical["max_tokens"] = max_tokens
    if response_format is not None:
        canonical["response_format"] = response_format
    if additional_params:
        canonical["additional_params"] = additional_params

    # Sort keys and pin separators for determinism (no extra whitespace)
    payload = json.dumps(canonical, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
