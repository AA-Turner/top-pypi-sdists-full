"""Flatten a provider's system prompt to text.

Providers that take it as a request argument rather than a message — Anthropic's
``system=``, the Claude Agent SDK's options, a Strands Agent's attribute — accept either
a string or a list of content pieces. Every consumer reads ``system_prompt`` as a string,
and ``str()`` on the list form stores a Python repr that then shows up as the goal.
"""

from __future__ import annotations

from typing import Any

__all__ = ["system_prompt_text"]


def system_prompt_text(value: Any) -> str:
    """Best-effort text from a string, a content block, or a list of either.

    Pieces carry their text under ``text`` as dicts or as provider objects; some nest
    them a level deeper under ``parts``.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(part for part in map(system_prompt_text, value) if part)
    text = value.get("text") if isinstance(value, dict) else getattr(value, "text", None)
    if isinstance(text, str):
        return text
    parts = value.get("parts") if isinstance(value, dict) else getattr(value, "parts", None)
    return system_prompt_text(parts) if parts is not None else ""
