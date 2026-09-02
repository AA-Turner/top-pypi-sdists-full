"""Conversation Labeling Service.

Automatically generates title, description, and keywords for conversations
using a fast, cheap LLM call (Groq). Handles:

- Regular chat conversations (full message history)
- Agent-initiated conversations (emphasizes user variables over template)
- Recent conversation deduplication (fetches + caches recent titles)
- Non-blocking execution (fire-and-forget via asyncio.create_task)
- Graceful failure (never crashes the parent request)

Usage:
    from matrx_ai.agents.services.conversation_labeler import schedule_conversation_labeling

    # Fire-and-forget after AI execution completes
    schedule_conversation_labeling(
        conversation_id=conversation_id,
        user_id=user_id,
        messages=messages,
        agent_name=agent_name,       # None for regular chats
        agent_description=description, # None for regular chats
        user_variables=variables,      # None for regular chats
        user_prompt=user_prompt,       # None for regular chats
    )
"""

from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any

from matrx_connect.context.data_types import ConversationLabeledData
from matrx_utils import vcprint

from matrx_ai.agent_runners.conversation_labeler import (
    ConversationLabelResult,
    _format_messages_for_labeling,
    label_agent_conversation,
    label_chat_conversation,
)
from matrx_ai.agents.response_parser import extract_model
from matrx_ai.context.app_context import try_get_app_context
from matrx_ai.db.cx_managers import cxm
from matrx_ai.persistence import standalone_coordinator

# ---------------------------------------------------------------------------
# Recent conversation title cache (per-user, in-memory)
# ---------------------------------------------------------------------------

_CACHE_MAX_USERS = 500
_CACHE_TTL_SECONDS = 300  # 5 minutes
_RECENT_CONVERSATION_COUNT = 10


class _UserTitleCache:
    """Per-user cache of recent conversation titles with TTL."""

    def __init__(self) -> None:
        self._store: OrderedDict[str, tuple[float, list[dict[str, str]]]] = OrderedDict()

    def get(self, user_id: str) -> list[dict[str, str]] | None:
        entry = self._store.get(user_id)
        if entry is None:
            return None
        ts, titles = entry
        if time.monotonic() - ts > _CACHE_TTL_SECONDS:
            self._store.pop(user_id, None)
            return None
        self._store.move_to_end(user_id)
        return titles

    def set(self, user_id: str, titles: list[dict[str, str]]) -> None:
        self._store[user_id] = (time.monotonic(), titles)
        self._store.move_to_end(user_id)
        while len(self._store) > _CACHE_MAX_USERS:
            self._store.popitem(last=False)

    def invalidate(self, user_id: str) -> None:
        self._store.pop(user_id, None)


_title_cache = _UserTitleCache()


async def _fetch_recent_titles(user_id: str) -> list[dict[str, str]]:
    """Fetch the most recent conversation titles for a user.

    Returns a list of dicts with 'id' and 'title' keys, ordered by
    most recent first. Uses the in-memory cache when available.

    Server-side pagination: ``ORDER BY updated_at DESC LIMIT N`` runs in
    Postgres and is satisfied by the
    ``cx_conversation_user_status_updated_idx`` index from migration
    0042 — no row transfer beyond the N we actually want, no Python-side
    sort. Previously this fetched every active conversation for the
    user and sliced [:10] in Python, which seq-scanned the table when
    the index was missing and tripped command_timeout=10s in production.
    """
    cached = _title_cache.get(user_id)
    if cached is not None:
        return cached

    try:
        # Drop down to the underlying matrx-orm Model so we can chain
        # order_by / limit. ``filter_items`` is a flat read-all and
        # doesn't expose those knobs.
        conversations = await (
            cxm.conversation.model.filter(created_by=user_id, status="active")
            .order_by("-updated_at")
            .limit(_RECENT_CONVERSATION_COUNT)
            .all()
        )

        recent: list[dict[str, str]] = []
        for conv in conversations:
            title = getattr(conv, "title", None) or ""
            if title:
                recent.append(
                    {
                        "id": str(conv.id),
                        "title": title,
                    }
                )

        _title_cache.set(user_id, recent)
        return recent

    except Exception as exc:
        vcprint(
            f"[ConversationLabeler] Failed to fetch recent titles: {exc}",
            color="yellow",
        )
        return []


def _format_recent_titles(titles: list[dict[str, str]]) -> str:
    if not titles:
        return ""
    lines = [f"- {t['title']}" for t in titles]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core labeling logic
# ---------------------------------------------------------------------------


async def _conversation_committed(kind: str, conversation_id: str) -> bool:
    """Committed-read existence check — the Rendezvous DB fallback.

    Runs only if the commit signal never arrived (cross-process, or a producer
    that forgot to announce). A fresh one-shot Session with no pending
    conversation INSERT reads the REAL committed state — it cannot be fooled by
    the pending-overlay the way the old poll-guard was. ``kind`` is ignored;
    this verifier is conversation-specific.
    """
    from matrx_orm import Session

    async with Session():
        return await cxm.conversation.exists(conversation_id)


async def _update_conversation_labels(
    conversation_id: str,
    user_id: str,
    fields: dict[str, Any],
) -> None:
    """Commit a label mutation through an isolated Coordinator."""
    async with standalone_coordinator(
        reason="conversation_label",
        user_id=user_id,
        conversation_id=conversation_id,
    ) as coordinator:
        coordinator.queue(
            "chat.conversation",
            fields,
            op_type="update",
            primary_key=("id", conversation_id),
        )


async def _run_labeling(
    conversation_id: str,
    user_id: str,
    messages: list[dict[str, Any]],
    agent_name: str | None = None,
    agent_description: str | None = None,
    user_variables: dict[str, Any] | None = None,
    user_prompt: str | None = None,
) -> None:
    """Execute the labeling pipeline and update the database.

    Invoked by the Rendezvous once the conversation row is CONFIRMED committed
    (via the ORM commit signal, or the DB-fallback verify) — so it never races
    the INSERT. It NEVER raises — all errors are caught and logged.
    """
    try:
        recent_titles = await _fetch_recent_titles(user_id)
        recent_titles_str = _format_recent_titles(recent_titles)

        conversation_content = _format_messages_for_labeling(messages)

        is_agent = bool(agent_name)

        if is_agent:
            variables_str = ""
            if user_variables:
                variables_str = "\n".join(f"- **{k}**: {v}" for k, v in user_variables.items())
            result = await label_agent_conversation(
                conversation_content=conversation_content,
                recent_titles=recent_titles_str,
                agent_name=agent_name or "",
                agent_description=agent_description or "",
                user_variables=variables_str,
                user_prompt=user_prompt or "",
            )
        else:
            result = await label_chat_conversation(
                conversation_content=conversation_content,
                recent_titles=recent_titles_str,
            )

        if not result.success:
            vcprint(
                f"[ConversationLabeler] Labeling agent returned failure for {conversation_id}: {result.error}",
                color="yellow",
            )
            return

        parsed = extract_model(result.output, ConversationLabelResult)
        if parsed is None:
            vcprint(
                f"[ConversationLabeler] Failed to parse labeling response for {conversation_id}. "
                f"Raw output: {result.output[:200]}",
                color="yellow",
            )
            return

        update_kwargs: dict[str, Any] = {}

        if parsed.label:
            update_kwargs["title"] = parsed.label
        if parsed.description:
            update_kwargs["description"] = parsed.description
        if parsed.keywords:
            update_kwargs["keywords"] = parsed.keywords

        if not update_kwargs:
            vcprint(
                f"[ConversationLabeler] No label data to update for {conversation_id}",
                color="yellow",
            )
            return

        await _update_conversation_labels(conversation_id, user_id, update_kwargs)

        _title_cache.invalidate(user_id)

        ctx = try_get_app_context()
        if ctx is not None and ctx.emitter is not None:
            await ctx.emitter.send_data(
                ConversationLabeledData(
                    conversation_id=conversation_id,
                    title=parsed.label,
                    description=parsed.description,
                    keywords=parsed.keywords,
                )
            )

        vcprint(
            f"[ConversationLabeler] Labeled conversation {conversation_id}: title={parsed.label!r}",
            color="green",
        )

    except Exception as exc:
        vcprint(
            f"[ConversationLabeler] Labeling failed for {conversation_id}: {exc}",
            color="yellow",
        )
        import traceback

        traceback.print_exc()


# ---------------------------------------------------------------------------
# Public API — fire-and-forget scheduling
# ---------------------------------------------------------------------------


def schedule_conversation_labeling(
    conversation_id: str,
    user_id: str,
    messages: list[dict[str, Any]],
    agent_name: str | None = None,
    agent_description: str | None = None,
    user_variables: dict[str, Any] | None = None,
    user_prompt: str | None = None,
) -> None:
    """Register conversation labeling to run the instant the conversation row is
    COMMITTED — regardless of arrival order.

    This used to poll the DB for the row and then UPDATE it, which raced the
    end-of-request flush: a fast turn made the poll see the still-QUEUED row
    (pending-aware read) and the UPDATE then hit zero committed rows. That whole
    class is gone. We hand the work to the process Rendezvous:

      * If the conversation already committed → the labeler runs immediately.
      * If not → the note is held until the ORM's commit signal fires it (see
        ``matrx_orm.session.session._announce_committed``).
      * If the commit never announces within the window → the note's dying act
        is a COMMITTED-read verify; it either runs anyway with a loud LEAK
        warning (the row slipped by) or is dropped with a critical BROKEN-PROMISE
        alarm. Nothing silent, nothing racy.

    Fire-and-forget: never raises, returns None.
    """
    if not conversation_id or not user_id:
        vcprint(
            "[ConversationLabeler] Cannot schedule: missing conversation_id or user_id",
            color="yellow",
        )
        return None

    if not messages:
        vcprint(
            f"[ConversationLabeler] Cannot schedule: no messages for {conversation_id}",
            color="yellow",
        )
        return None

    from matrx_utils import rendezvous

    async def _labeling_after_commit() -> None:
        await _run_labeling(
            conversation_id=conversation_id,
            user_id=user_id,
            messages=messages,
            agent_name=agent_name,
            agent_description=agent_description,
            user_variables=user_variables,
            user_prompt=user_prompt,
        )

    # coalesce on the conversation id: two messages from the same user used to
    # spawn two racing labelers — the Rendezvous collapses same-label notes.
    rendezvous.on_present(
        "Conversation",
        conversation_id,
        do=_labeling_after_commit,
        verify=_conversation_committed,
        ttl=300.0,
        label=f"label:{conversation_id}",
    )
    return None
