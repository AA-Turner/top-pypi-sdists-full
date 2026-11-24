"""Interim text — the words a model writes before it calls a tool, marked on the saved text part.

"Add a services section to the Home draft." written right before a tool call is a note between
steps, not the answer. The save funnel marks such a text part ``interim: true``; the ``message_blocks``
event carries the same flag, and a client draws it as a progress note instead of answer text.

THE RULE (one place; the chat's live reading mirrors it in ``@ai-matrx/tool-cards`` ``interimProse``):

* a text part a tool call follows IN THE SAME MESSAGE is interim;
* text a reply ends on before it parks on the person (``is_person_ask_call``) is what the person reads to
  answer: never interim, even with another call between it and the ask. A notice to the person (the
  extension's ``user`` tool with type notify) waits on nobody: it is a call like any other;
* everything else carries no flag — an ordinary answer and every row saved before this are unchanged.

The flag is derived from the row's own parts, so it is recomputed on every save (a stale one is
dropped) and never mutates the caller's content. It is display data: no provider translator reads it.
"""

from __future__ import annotations

import re
from typing import Any

INTERIM_FIELD = "interim"


# A reasoning region at the very start of a text (closed, or still open at its end): the model's
# thinking written inline, not words to the person. The chat's `hasReplyText` reads it the same way.
_LEADING_REASONING = re.compile(r"^\s*<(thinking|think|reasoning)(?:\s[^>]*)?>.*?(?:</\1\s*>|$)", re.IGNORECASE | re.DOTALL)


def _has_reply_text(text: str) -> bool:
    rest = text
    while True:
        cut = _LEADING_REASONING.sub("", rest, count=1)
        if cut == rest:
            return bool(rest.strip())
        rest = cut


def _is_prose(part: Any) -> bool:
    return isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str) and _has_reply_text(part["text"])


def interim_flags(content: Any) -> list[bool]:
    """Per part of ``content``: is it a text part a tool call follows (and no ask to the person ends its leg)?"""
    if not isinstance(content, list):
        return []
    from matrx_ai.config.tool_result_guard import is_person_ask_call

    flags = [False] * len(content)
    tool_follows = False
    ask_ends_leg = False
    for i in range(len(content) - 1, -1, -1):
        part = content[i]
        if not isinstance(part, dict):
            continue
        if part.get("type") == "tool_call":
            name = part.get("name")
            if isinstance(name, str) and is_person_ask_call(name, part.get("arguments")):
                ask_ends_leg = True
                tool_follows = False
            else:
                tool_follows = True
        elif _is_prose(part):
            flags[i] = tool_follows and not ask_ends_leg
            # Text ends the leg an ask closed: earlier text answers to the calls before THIS text.
            if ask_ends_leg:
                ask_ends_leg = False
                tool_follows = False
    return flags


def mark_interim_text(content: Any) -> Any:
    """``content`` with every text part's ``interim`` flag set to the rule's answer (present only when true).

    Returns the same object when nothing changed.
    """
    if not isinstance(content, list):
        return content
    flags = interim_flags(content)
    out: list[Any] | None = None
    for i, part in enumerate(content):
        if not isinstance(part, dict) or part.get("type") != "text":
            continue
        if flags[i] == (part.get(INTERIM_FIELD) is True) and (flags[i] or INTERIM_FIELD not in part):
            continue
        if out is None:
            out = list(content)
        updated = {k: v for k, v in part.items() if k != INTERIM_FIELD}
        if flags[i]:
            updated[INTERIM_FIELD] = True
        out[i] = updated
    return content if out is None else out


__all__ = ["INTERIM_FIELD", "interim_flags", "mark_interim_text"]
