"""Server-authoritative history for a persisted conversation.

THE INVARIANT: for a conversation that exists in the database, the DATABASE is
the history. A client-supplied ``messages`` array can only ever ADD new turns to
it — it is never the history itself.

Why this exists
---------------
The message-shaped endpoint (``POST /ai/chat``, aka ``/ai/manual``) lets the
caller pass a whole ``messages`` list. When that list is the ENTIRE conversation
the persistence layer's index-based bookkeeping lines up and everything works.
When a client instead sends only the NEW turn against an existing
``conversation_id`` — the natural thing to do, and what a delta-shaped client
does — the model sees no history at all and the turn is stored as if it were the
first one. Both failures are silent. Found live 2026-07-11 alongside 115
conversations carrying duplicate ``position`` slots.

So resolution is centralized here rather than patched into a router: load the
persisted history through the SAME seam ``ConversationResolver`` uses, and append
only what the client genuinely added.

What counts as "new"
--------------------
Deliberately NOT a fuzzy diff of the past. Two exact signals, then a default:

1. **By id.** A submitted message carrying an ``id`` that is already a persisted
   ``cx_message`` is a replay of a stored row — dropped.
2. **By full-history prefix.** A client that re-sends the whole conversation and
   appends to it (``len(submitted) > len(persisted)`` and the two lists start on
   the same message) has its replayed prefix dropped, LOUDLY.
3. **Otherwise every submitted message is a new turn** — appended to the
   persisted history.

This NEVER rejects a turn. An earlier draft inferred the client's shape by
prefix-matching message text and raised a 422 on divergence; that fails a real
user whose new message merely repeats the conversation's opening words, and it
misreads any conversation containing tool calls or model-hidden rows (the loader
returns the model-visible subset, which is not what a client's own view looks
like). A user's turn must never die over a heuristic about the past.

The consequence is intentional and stated: a client that submits a MODIFIED past
has its edits ignored — the DB wins, and we say so in the log. Editing history is
a real capability with real endpoints (message edit + ``cx_truncate_conversation_after``,
or fork-and-run); it is not something an append-only door should half-honor.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.config.message_config import UnifiedMessage

logger = logging.getLogger("matrx_ai.agents.history_hydration")


class HistoryLoader(Protocol):
    """Seam: the persisted messages for a conversation, already rebuilt through
    the ``rebuild_conversation_messages`` funnel (so model-hidden and
    soft-deleted rows are already excluded)."""

    async def __call__(self, conversation_id: str) -> list[UnifiedMessage]: ...


def _identity(message: UnifiedMessage) -> str:
    """Role + text, for the full-history-prefix check only. Text alone, because
    ids/timestamps/tool blocks are rewritten by the rebuild funnel and would make
    every faithful client look like a stranger."""
    role = getattr(message, "role", "") or ""
    try:
        text = message.get_output()
    except Exception:
        text = ""
    return f"{role}:{(text or '').strip()}"


async def hydrate_persisted_history(
    config: UnifiedConfig,
    conversation_id: str,
    *,
    load: HistoryLoader | None = None,
) -> int:
    """Make ``config.messages`` = persisted history + the client's NEW turns.

    Mutates ``config`` in place; returns the number of turns treated as new.
    Never raises on client shape — see the module docstring.

    A no-op when the conversation has no persisted messages (brand-new, or an
    ephemeral run): there the client's list IS the history.
    """
    loader = load or _default_loader
    persisted = await loader(conversation_id)
    if not persisted:
        return len(config.messages)

    submitted: list[UnifiedMessage] = list(config.messages)

    # (1) Exact: anything the client echoed back by cx_message id is a replay.
    persisted_ids = {str(m.id) for m in persisted if getattr(m, "id", None)}
    if persisted_ids:
        kept = [m for m in submitted if str(getattr(m, "id", "") or "") not in persisted_ids]
        if len(kept) != len(submitted):
            logger.warning(
                "[history] Conversation %s: dropped %d submitted message(s) that are already "
                "stored (matched by cx_message id). Send ONLY new turns — a saved "
                "conversation's history comes from the server.",
                conversation_id,
                len(submitted) - len(kept),
            )
            submitted = kept

    # (2) Exact enough: a client that replayed the WHOLE history and appended to
    # it. Requires strictly more messages than the entire stored conversation AND
    # the same opening message — a delta can satisfy neither by accident.
    if len(submitted) > len(persisted) and _identity(submitted[0]) == _identity(persisted[0]):
        dropped = len(persisted)
        logger.warning(
            "[history] Conversation %s: client re-sent the full %d-message history on an "
            "append-only endpoint. Dropping the replayed prefix, appending the %d new turn(s). "
            "Any edit the client made to an EARLIER message is IGNORED — the database is the "
            "history. To change the past, edit + truncate, or fork-and-run.",
            conversation_id,
            dropped,
            len(submitted) - dropped,
        )
        submitted = submitted[dropped:]

    # (3) Everything left is a new turn.
    config.messages.clear()
    config.messages.extend(persisted)
    config.messages.extend(submitted)
    return len(submitted)


async def _default_loader(conversation_id: str) -> list[UnifiedMessage]:
    """Server path: the stored conversation's rebuilt message list.

    Reuses ``ConversationResolver``'s own load seam, so the history a
    continuation sees on ``/chat`` is byte-for-byte the history it sees on
    ``/conversations/{id}`` — one funnel, never a second reader.
    """
    from matrx_ai.agents.resolver import _load_unified_config

    stored: Any = await _load_unified_config(conversation_id)
    return list(stored.messages)


__all__ = [
    "HistoryLoader",
    "hydrate_persisted_history",
]
