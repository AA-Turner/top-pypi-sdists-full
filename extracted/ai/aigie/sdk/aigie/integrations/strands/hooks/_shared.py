"""Shared helpers used across the Strands hook modules."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_messages_for_span(messages: Any, max_content_length: int) -> list[dict[str, str]]:
    """Coerce a Strands message list into ``[{"role", "content"}, ...]`` for a span.

    Handles dict messages with list-of-parts content (Bedrock/Anthropic shape) and
    falls back to ``str()`` for anything non-dict.
    """
    prompts: list[dict[str, str]] = []
    if not isinstance(messages, list):
        return prompts
    for msg in messages:
        if not isinstance(msg, dict):
            prompts.append({"role": "user", "content": str(msg)[:max_content_length]})
            continue
        role = str(msg.get("role", "user"))
        content = msg.get("content", "")
        if isinstance(content, list):
            text_parts = [p.get("text", "") for p in content if isinstance(p, dict) and "text" in p]
            content_text = " ".join(text_parts) if text_parts else str(content)
        else:
            content_text = str(content)
        prompts.append({"role": role, "content": content_text[:max_content_length]})
    return prompts
