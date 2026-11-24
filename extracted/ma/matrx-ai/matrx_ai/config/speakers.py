"""THE SPEAKERS — in a chat more than one person writes in, the model reads who said each thing.

A group chat is a conversation shared with people (CGU-10). Every person's message is a ``user`` turn,
so without a name the model reads one voice. The database stamps each person row's writer
(``chat.message.author_id``, from the signed-in caller at insert, never client-written); this step
puts the writer's name in front of each person turn on the WIRE copy only:

    Rhonda Taylor:
    is Friday still on?

- Only when the history holds turns by two or more people. A one-person chat sends exactly what it
  sent before (same bytes, same cache prefix).
- Who wrote a turn: a stored row's ``author_id`` (``from_store`` only: a client-sent message cannot
  name its author), else, for this turn's own new message, the person running the turn
  (``AppContext.user_id``). A row written before the column existed has no ``author_id`` and is read
  as the chat's owner (``created_by``, carried by ``UnifiedMessage.from_cx_message``).
- Names come from the host (``set_speaker_name_source``: ``async (ids) -> {id: name}``). A person
  with no name is "Person 1", "Person 2", … in order of first appearance — never an email.
- Host-written user turns (a notice, a cadence row: no words the person typed) carry no name.
- The name block is marked ``authored_by: host`` and is never stored: the canonical config and the
  ledger are untouched, so nothing is ever saved as the person's words.

Called once per send by ``send_boundary.prepare_for_send`` (loop stage, after the wire clone).
Guard: ``packages/matrx-ai/tests/test_speakers_are_named.py``.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from copy import copy
from typing import Any

#: ``async (author_ids) -> {author_id: display name}``; a missing id or empty name = no name.
SpeakerNameSource = Callable[[list[str]], Awaitable[dict[str, str]]]

SPEAKER_NAME_REASON = "speaker_name"

_SOURCE: SpeakerNameSource | None = None


def set_speaker_name_source(source: SpeakerNameSource | None) -> None:
    """Install the host's name reader (``None`` = no names: people are numbered)."""
    global _SOURCE
    _SOURCE = source


def get_speaker_name_source() -> SpeakerNameSource | None:
    return _SOURCE


def _current_person() -> str | None:
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 — no context = no current person
        return None
    user_id = getattr(ctx, "user_id", None) if ctx is not None else None
    return str(user_id) if user_id else None


def author_of(message: Any, current_person: str | None) -> str | None:
    """Who wrote this person turn, or None (not a person turn, or no words a person typed)."""
    from matrx_ai.config.message_config import human_authored_text

    if getattr(message, "role", None) != "user":
        return None
    text = human_authored_text("user", getattr(message, "content", None), getattr(message, "user_content", None))
    if not str(text or "").strip():
        return None
    if getattr(message, "from_store", False):
        author = getattr(message, "author_id", None)
        return str(author) if author else None
    return current_person


async def name_speakers(messages: list[Any], *, current_person: str | None = None) -> list[Any] | None:
    """The list with each person turn led by its writer's name, or None when nothing changes.

    Pure apart from the host's name read; the messages passed in are never mutated.
    """
    from matrx_ai.config.message_config import HOST_AUTHORED_BY
    from matrx_ai.config.unified_content import TextContent

    person = current_person if current_person is not None else _current_person()
    authors = [author_of(m, person) for m in messages]
    order: list[str] = []
    for author in authors:
        if author and author not in order:
            order.append(author)
    if len(order) < 2:
        return None

    names: dict[str, str] = {}
    source = _SOURCE
    if source is not None:
        names = {str(k): str(v).strip() for k, v in (await source(list(order)) or {}).items() if str(v or "").strip()}
    label: dict[str, str] = {}
    unnamed = 0
    for author in order:
        if names.get(author):
            label[author] = names[author]
        else:
            unnamed += 1
            label[author] = f"Person {unnamed}"

    named: list[Any] = []
    for message, author in zip(messages, authors, strict=True):
        if not author:
            named.append(message)
            continue
        twin = copy(message)
        twin.content = [
            TextContent(
                text=f"{label[author]}:",
                metadata={"authored_by": HOST_AUTHORED_BY, "authored_reason": SPEAKER_NAME_REASON},
            ),
            *list(getattr(message, "content", None) or []),
        ]
        named.append(twin)
    return named


__all__ = [
    "SPEAKER_NAME_REASON",
    "SpeakerNameSource",
    "author_of",
    "get_speaker_name_source",
    "name_speakers",
    "set_speaker_name_source",
]
