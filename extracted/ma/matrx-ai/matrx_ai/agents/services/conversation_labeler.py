"""Conversation Labeling Service.

Automatically generates title, description, and keywords for conversations
through the conversation.label_chat / conversation.label_agent_run mandates. Handles:

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
    AGENT_DESCRIPTION_MAX_CHARS,
    AGENT_NAME_MAX_CHARS,
    LABEL_PROCESS_KEY,
    USER_PROMPT_MAX_CHARS,
    ConversationLabelResult,
    _bounded_user_variables,
    _format_messages_for_labeling,
    _trim_content,
    label_agent_conversation,
    label_chat_conversation,
)
from matrx_ai.agents.response_parser import extract_model
from matrx_ai.context.app_context import try_get_app_context
from matrx_ai.persistence import standalone_coordinator


class _CxmProxy:
    """Transparent proxy over the real ``cxm`` singleton (``matrx_ai.db.cx_managers``).

    That facade resolves its DB bases lazily, at attribute-access time,
    specifically so importing it never requires ``matrx_ai.configure()``
    (see its own module docstring). A module-level
    ``from matrx_ai.db.cx_managers import cxm`` here defeated that — the
    import machinery's ``getattr(cx_managers, "cxm")`` fires immediately,
    which forced DB configuration at THIS module's import time and crashed
    any boot path that never configures matrx_ai's DB (e.g. a hosted
    sandbox). This proxy is a genuine, harmless object at import time; every
    attribute access is forwarded to the real singleton on first real use.
    Kept as a real module-level name (rather than a local import per call
    site) so ``monkeypatch.setattr(conversation_labeler, "cxm", fake)``
    keeps working exactly as it did before this fix.
    """

    def __getattr__(self, name: str) -> Any:
        from matrx_ai.db.cx_managers import cxm as _real_cxm

        return getattr(_real_cxm, name)


cxm = _CxmProxy()

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


async def _is_staff_channel_conversation(conversation_id: str) -> bool:
    """Is this the person's permanent Personal Staff thread?

    That thread accumulates every conversation the person ever has with their
    staff across text, call, and the signed-in app — it is named for WHO the
    person is talking to, not for whatever the first topic happened to be
    (the iMessage model). It must never be auto-titled or auto-keyworded by
    this labeler, no matter which door the current turn came in through.

    Checked against the PERSISTED conversation row, not the calling turn's
    own ``metadata["channel"]`` — the staff thread is reached through three
    different doors (SMS, voice, the in-app ``/staff`` door) and only ONE of
    them stamps its own per-turn channel as ``"staff"``. What is constant
    across every door is the row's own ``metadata.channel``, written once at
    creation (``aidream/services/communications/staff_channel.py`` and
    ``aidream/services/communications/voice_agent_preparation.py``).
    """
    try:
        rows = await cxm.conversation.model.filter(id=conversation_id).limit(1).all()
    except Exception as exc:
        vcprint(
            f"[ConversationLabeler] Staff-channel check failed for {conversation_id}: {exc}",
            color="yellow",
        )
        return False
    if not rows:
        return False
    metadata = getattr(rows[0], "metadata", None)
    return isinstance(metadata, dict) and metadata.get("channel") == "staff"


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


#: How long after the inline attempt the durable retry may run. The inline call lands in
#: seconds; the retry exists for the process that died, not for a slow model.
LABEL_RETRY_DELAY_FEATURE = "agents.conversations"
LABEL_RETRY_DELAY_KEY = "label_retry_delay_seconds"
#: KNOB MIRROR of platform.feature_knob "agents.conversations" "label_retry_delay_seconds"
LABEL_RETRY_DELAY_MIRROR = 180.0


def label_retry_delay_seconds() -> float:
    """The durable retry's delay, live from the host (``agents.conversations.label_retry_delay_seconds``)."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(LABEL_RETRY_DELAY_FEATURE, LABEL_RETRY_DELAY_KEY, LABEL_RETRY_DELAY_MIRROR,
                               low=30.0, high=3600.0)


async def _label_row(conversation_id: str) -> Any | None:
    rows = await cxm.conversation.model.filter(id=conversation_id).limit(1).all()
    return rows[0] if rows else None


def _already_labeled(row: Any) -> bool:
    """The labeler writes description and keywords with the title; either one present means
    a label landed (a person renaming the chat changes only the title)."""
    return bool(str(getattr(row, "description", "") or "").strip()) or bool(
        list(getattr(row, "keywords", None) or [])
    )


async def _seed_label_retry(conversation_id: str, payload: dict[str, Any]) -> None:
    """Seed the durable retry BEFORE the inline attempt (host seam; none on a standalone host).

    A process that dies mid-call leaves this row; the host's drain runs it after
    ``label_retry_delay_seconds()`` and skips it when the inline label landed. A failure to seed
    is said, never fatal — the inline attempt still runs.
    """
    from matrx_ai._ext import get_system_process_seed

    seed = get_system_process_seed()
    if seed is None:
        return
    try:
        await seed(
            process_key=LABEL_PROCESS_KEY,
            subject_id=conversation_id,
            payload=payload,
            delay_seconds=label_retry_delay_seconds(),
        )
    except Exception as exc:  # noqa: BLE001 — announced; the inline attempt is unaffected
        vcprint(
            f"[ConversationLabeler] Could not seed the durable retry for {conversation_id}: "
            f"{type(exc).__name__}: {exc}",
            color="red",
        )


async def _label_and_apply(
    *,
    conversation_id: str,
    user_id: str,
    conversation_content: str,
    agent_name: str | None,
    agent_description: str | None,
    user_variables: dict[str, Any] | None,
    user_prompt: str | None,
    keep_title_unless: str | None = None,
) -> tuple[str, ConversationLabelResult | None]:
    """Run the labeler as the platform and write the label. Returns ``(outcome, label)``.

    ``keep_title_unless``: write the title only while the row's title still equals this value
    (the retry passes the title it saw before the inline attempt, so a person's rename made in
    between is never overwritten). None = always write it.
    """
    recent_titles_str = _format_recent_titles(await _fetch_recent_titles(user_id))
    if agent_name:
        result = await label_agent_conversation(
            conversation_content=conversation_content,
            recent_titles=recent_titles_str,
            agent_name=agent_name or "",
            agent_description=agent_description or "",
            # Raw name → value: the Holder's turn frames them, the prompt
            # door renders them; never "- **name**: value" lines in code.
            user_variables=dict(user_variables or {}),
            user_prompt=user_prompt or "",
            conversation_id=conversation_id,
        )
    else:
        result = await label_chat_conversation(
            conversation_content=conversation_content,
            recent_titles=recent_titles_str,
            conversation_id=conversation_id,
        )

    if not result.success:
        return f"failed:{result.error or 'labeler returned failure'}", None

    parsed = extract_model(result.output, ConversationLabelResult)
    if parsed is None:
        return f"failed:unparseable output {result.output[:120]!r}", None

    update_kwargs: dict[str, Any] = {}
    if parsed.label:
        update_kwargs["title"] = parsed.label
    if parsed.description:
        update_kwargs["description"] = parsed.description
    if parsed.keywords:
        update_kwargs["keywords"] = parsed.keywords
    if keep_title_unless is not None and "title" in update_kwargs:
        row = await _label_row(conversation_id)
        if row is None or str(getattr(row, "title", "") or "") != keep_title_unless:
            update_kwargs.pop("title")
    if not update_kwargs:
        return "skipped:empty_label", None

    await _update_conversation_labels(conversation_id, user_id, update_kwargs)
    _title_cache.invalidate(user_id)
    return "succeeded", parsed


async def _run_labeling(
    conversation_id: str,
    user_id: str,
    messages: list[dict[str, Any]],
    agent_name: str | None = None,
    agent_description: str | None = None,
    user_variables: dict[str, Any] | None = None,
    user_prompt: str | None = None,
) -> None:
    """Seed the durable retry, label inline as the platform, and stream the title.

    Invoked by the Rendezvous once the conversation row is CONFIRMED committed
    (via the ORM commit signal, or the DB-fallback verify) — so it never races
    the INSERT. It NEVER raises — all errors are caught and logged.
    """
    try:
        if await _is_staff_channel_conversation(conversation_id):
            vcprint(
                f"[ConversationLabeler] Skipping Personal Staff thread {conversation_id} "
                "(metadata.channel == 'staff') — never auto-titled",
                color="cyan",
            )
            return

        conversation_content = _format_messages_for_labeling(messages)
        row = await _label_row(conversation_id)
        # The retry's inputs, bounded exactly as the labeler bounds them (an agent definition can
        # be hundreds of thousands of characters) and JSON-safe for the queue row. The queue keeps
        # them only until the item settles.
        import asyncio
        import json

        retry_payload = json.loads(
            json.dumps(
                {
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    # The subject's own organization (tenancy for the retry's reads and writes).
                    "organization_id": str(getattr(row, "organization_id", "") or "") if row else "",
                    "conversation_content": conversation_content,
                    "agent_name": _trim_content(agent_name or "", AGENT_NAME_MAX_CHARS),
                    "agent_description": _trim_content(agent_description or "", AGENT_DESCRIPTION_MAX_CHARS),
                    "user_variables": _bounded_user_variables(dict(user_variables or {})),
                    "user_prompt": _trim_content(user_prompt or "", USER_PROMPT_MAX_CHARS),
                    "title_before": str(getattr(row, "title", "") or "") if row else "",
                },
                default=str,
            )
        )
        # The retry is seeded beside the inline attempt, never in front of it: the title must not
        # wait on the queue's round trips (it is due label_retry_delay_seconds() later anyway).
        _seeded, (outcome, parsed) = await asyncio.gather(
            _seed_label_retry(conversation_id, retry_payload),
            _label_and_apply(
                conversation_id=conversation_id,
                user_id=user_id,
                conversation_content=conversation_content,
                agent_name=agent_name,
                agent_description=agent_description,
                user_variables=user_variables,
                user_prompt=user_prompt,
            ),
        )
        if parsed is None:
            vcprint(
                f"[ConversationLabeler] {conversation_id}: {outcome} (the durable retry will try again)",
                color="yellow",
            )
            return

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


async def run_label_retry(payload: dict[str, Any]) -> str:
    """The durable retry (``conversation.name`` system process): label the conversation now
    unless the inline attempt already did. Returns the settlement; raises only when the label
    call itself failed, so the host retries with backoff."""
    conversation_id = str(payload.get("conversation_id") or "")
    user_id = str(payload.get("user_id") or "")
    if not conversation_id or not user_id:
        return "skipped:incomplete_payload"
    row = await _label_row(conversation_id)
    if row is None or getattr(row, "deleted_at", None) is not None:
        return "skipped:conversation_gone"
    title_before = str(payload.get("title_before") or "")
    if _already_labeled(row) or str(getattr(row, "title", "") or "") != title_before:
        # Labeled, or retitled since the inline attempt began (by it or by the person).
        return "skipped:already_labeled"
    if isinstance(getattr(row, "metadata", None), dict) and row.metadata.get("channel") == "staff":
        return "skipped:staff_thread"
    outcome, _parsed = await _label_and_apply(
        conversation_id=conversation_id,
        user_id=user_id,
        conversation_content=str(payload.get("conversation_content") or ""),
        agent_name=payload.get("agent_name") or None,
        agent_description=payload.get("agent_description") or None,
        user_variables=payload.get("user_variables") or None,
        user_prompt=payload.get("user_prompt") or None,
        keep_title_unless=title_before,
    )
    if outcome.startswith("failed:"):
        raise RuntimeError(f"conversation labeler retry {outcome}")
    return outcome


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
