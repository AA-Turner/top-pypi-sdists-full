"""Token estimation via tiktoken for usage fallback.

When the API does not return streaming usage data, this module provides
cl100k_base-based estimation from the message list and response content.
"""

from __future__ import annotations

from typing import Any

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
