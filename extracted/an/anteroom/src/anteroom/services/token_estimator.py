"""Token estimation via tiktoken for usage fallback.

When the API does not return streaming usage data, this module provides
cl100k_base-based estimation from the message list and response content.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestTokenBreakdown:
    """Per-component token breakdown for a full LLM request."""

    message_tokens: int
    system_prompt_tokens: int
    tool_schema_tokens: int
    total: int


_encoding: Any = None


def _get_encoding() -> Any:
    """Get the cl100k_base encoding, cached after first call."""
    global _encoding
    if _encoding is None:
        try:
            import tiktoken

            _encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _encoding = False
    return _encoding


def count_message_tokens(messages: list[dict[str, Any]]) -> int:
    """Count tokens in a list of chat messages using cl100k_base.

    Includes ~4 tokens per-message overhead for role/separators (OpenAI chat format).
    Falls back to len(text)//4 if tiktoken is unavailable.
    """
    enc = _get_encoding()
    total = 0
    for msg in messages:
        total += 4  # Per-message overhead
        content = msg.get("content", "")
        if isinstance(content, str):
            if enc:
                total += len(enc.encode(content, allowed_special="all"))
            else:
                total += len(content) // 4
        elif isinstance(content, list):
            for part in content:
                text = str(part) if isinstance(part, dict) else ""
                if enc:
                    total += len(enc.encode(text, allowed_special="all"))
                else:
                    total += len(text) // 4
        for tc in msg.get("tool_calls", []):
            if isinstance(tc, dict):
                func = tc.get("function", {})
                args = func.get("arguments", "")
                name = func.get("name", "")
                if enc:
                    total += len(enc.encode(args, allowed_special="all")) + len(enc.encode(name, allowed_special="all"))
                else:
                    total += (len(args) + len(name)) // 4
    return total


def count_text_tokens(text: str) -> int:
    """Count tokens in a plain text string."""
    if not text:
        return 0
    enc = _get_encoding()
    if enc:
        return len(enc.encode(text, allowed_special="all"))
    return len(text) // 4


def estimate_usage(
    messages: list[dict[str, Any]],
    response_content: str,
    model: str,
) -> dict[str, Any]:
    """Estimate token usage from messages and response content.

    Returns a usage dict compatible with the ``usage`` event protocol,
    with ``estimated: True`` so handlers can flag it in metadata.
    The ``model`` field is the real model name (not prefixed) so cost
    reporting works unchanged.
    """
    prompt_tokens = count_message_tokens(messages)
    completion_tokens = count_text_tokens(response_content)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "model": model,
        "estimated": True,
    }


def estimate_request_tokens(
    messages: list[dict[str, Any]],
    system_prompt: str = "",
    extra_system_prompt: str = "",
    tool_schemas: list[dict[str, Any]] | None = None,
) -> RequestTokenBreakdown:
    """Estimate the total token cost of a full LLM request.

    Accounts for message history, system prompt (default + extra),
    and tool schemas — the three major components that the previous
    message-only estimator missed.
    """
    message_tokens = count_message_tokens(messages)

    combined_system = ""
    if extra_system_prompt and system_prompt:
        combined_system = extra_system_prompt + "\n\n" + system_prompt
    elif extra_system_prompt:
        combined_system = extra_system_prompt
    elif system_prompt:
        combined_system = system_prompt
    system_prompt_tokens = count_text_tokens(combined_system) + 4 if combined_system else 0

    tool_schema_tokens = 0
    if tool_schemas:
        for tool in tool_schemas:
            func = tool.get("function", {})
            serialized = json.dumps(func, separators=(",", ":"))
            tool_schema_tokens += count_text_tokens(serialized)

    total = message_tokens + system_prompt_tokens + tool_schema_tokens
    return RequestTokenBreakdown(
        message_tokens=message_tokens,
        system_prompt_tokens=system_prompt_tokens,
        tool_schema_tokens=tool_schema_tokens,
        total=total,
    )
