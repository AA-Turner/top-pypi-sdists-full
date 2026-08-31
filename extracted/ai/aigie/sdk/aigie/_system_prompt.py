"""Flatten a provider's system prompt to text.

Providers that take it as a request argument rather than a message — Anthropic's
``system=``, the Claude Agent SDK's options, a Strands Agent's attribute, Gemini's
``system_instruction`` — accept either a string or a list of content pieces. Every
consumer reads ``system_prompt`` as a string, and ``str()`` on the list form stores a
Python repr that then shows up as the goal.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

__all__ = ["system_prompt_text"]

# A piece nests at most `value -> parts -> [part] -> text`. The cap is what makes the
# traversal terminate: `parts` can point back at its own container, and a proxy object
# answers every attribute with another proxy, both of which otherwise recurse until the
# stack ends — inside the caller's own call.
_MAX_DEPTH = 4


def system_prompt_text(value: Any) -> str:
    """Best-effort text from a string, a content block, or a list of either.

    Pieces carry their text under ``text`` as dicts or as provider objects; some nest
    them a level deeper under ``parts``.
    """
    return _flatten(value, _MAX_DEPTH)


def _flatten(value: Any, depth: int) -> str:
    if isinstance(value, str):
        return value
    if depth <= 0:
        return ""
    if _is_piece_sequence(value):
        return "\n".join(text for text in (_flatten(part, depth - 1) for part in value) if text)
    text = value.get("text") if isinstance(value, dict) else getattr(value, "text", None)
    if isinstance(text, str):
        return text
    parts = value.get("parts") if isinstance(value, dict) else getattr(value, "parts", None)
    return _flatten(parts, depth - 1) if parts is not None else ""


def _is_piece_sequence(value: Any) -> bool:
    """True for a run of content pieces to join, false for a single piece.

    ``Sequence`` rather than ``list``: the legacy ``google.generativeai`` client
    normalizes ``system_instruction`` into a protobuf ``Content`` whose ``parts`` is a
    ``RepeatedComposite`` — a registered ``Sequence`` that is not a ``list``, so a
    ``list``-only test bottomed out and flattened every legacy system prompt to "".

    Deliberately not ``hasattr(value, "__iter__")``: the current ``google.genai`` types
    are pydantic models, whose ``__iter__`` yields ``(field_name, value)`` pairs. That
    test would tear a ``Part`` into its field names instead of reading its ``text``.
    """
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))
