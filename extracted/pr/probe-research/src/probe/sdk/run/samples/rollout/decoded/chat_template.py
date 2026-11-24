"""The chat-template reader interface: one model family's decoded text (special tokens kept) as OpenAI-shaped messages,
so decoded turns hold roles, tool calls, tool results and reasoning instead of the template's control text."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any


class ChatTemplate(ABC):
    """One chat template. ``control_tokens`` are every marker the template writes around messages: never part of a
    message's text (the conformance test reads them from here). ``role_markers`` tell its text from another's.
    ``message_starts`` open a message: a run's tokens are cut before each that is one token, to count each message's."""

    name: str = ""
    control_tokens: tuple[str, ...] = ()
    role_markers: tuple[str, ...] = ()
    message_starts: tuple[str, ...] = ()

    def is_written_in(self, text: str) -> bool:
        """True when ``text`` holds one of this template's role markers."""
        return any(marker in text for marker in self.role_markers)

    @abstractmethod
    def read_messages(self, text: str, *, role: str) -> list[dict]:
        """``text`` (one run of tokens, specials kept) as messages: OpenAI-shaped dicts (`role`, `content`,
        `reasoning_content`, `tool_calls`). Text before the first role marker belongs to ``role``."""

    def strip_control_tokens(self, text: str) -> str:
        """``text`` with every control token removed: a stray marker never reaches a message."""
        for token in self.control_tokens:
            text = text.replace(token, "")
        return text


def to_hermes_call(body: str) -> dict | None:
    """A Hermes `<tool_call>` body (`{"name": ..., "arguments": {...}}`) as an OpenAI tool call with no id (the template
    names none: results link by order), or None when it is not one."""
    try:
        found: Any = json.loads(body)
    except (TypeError, ValueError):
        return None
    if not isinstance(found, dict) or not isinstance(found.get("name"), str) or not found["name"]:
        return None
    arguments = found.get("arguments", found.get("parameters", {}))
    if not isinstance(arguments, str):
        arguments = json.dumps(arguments, ensure_ascii=False)
    return {"type": "function", "function": {"name": found["name"], "arguments": arguments}}
