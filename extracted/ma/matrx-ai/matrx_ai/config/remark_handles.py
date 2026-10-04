"""Remark handles — the short, conversation-wide names (``c1``, ``c2`` …) the
model cites to answer a person's remark (THREADS R1, 2026-10-03).

* Every remark item carries a stable ``id`` (the client's resource id; minted
  here when absent). A thread root is keyed on that id, never on the handle.
* A handle is minted ONCE, when the containing message is first sent, and is
  frozen with ``resolved_text`` (it lives on the stored item).
* Allocation (R1's "max over ALL chat.message rows" rule): the next number is
  one above the highest handle stored in ANY user message of the conversation —
  hidden, trimmed and superseded rows included — or in the loaded history,
  whichever is higher. Two sends racing on one conversation could both read the
  same maximum; the reply side refuses a handle that names more than one
  remark (``comment_reply``: "c3 names 2 different remarks"), so a collision is
  loud and never mis-threads. (An UPDATE…RETURNING counter on
  ``chat.conversation.metadata`` was tried first and REJECTED: that column is
  coordinator-owned and rewritten wholesale every request, so the counter was
  clobbered — proven on the clone, 2026-10-03.)
* An item whose ``id`` already holds a handle earlier in the conversation keeps
  that handle (an edit-and-resend does not re-number). A handle the CLIENT put
  on a new item is never trusted: it is re-minted unless that id already owns it.

Also the other half of R3: ``comment_reply`` failures the host recorded on the
conversation are drained here and told to the model inside the next remarks
text. Both writes go through the request's WriteCoordinator (the conversation
row's owner), never a direct write.
"""

from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint

from matrx_ai.config.remarks import (
    REMARKS_PART_TYPE,
    format_handle,
    handle_number,
    remark_item_dicts,
)

#: The item dicts THIS request already minted a handle for. A host step may mint
#: before the structured-input resolver does (the remarks reply note names the
#: handles in the system channel, ``aidream comment_replies.reply_note``); by the
#: time the resolver runs, the person's message — WITH that handle — may already
#: be stored, so a second mint read the stored floor and renumbered c1 → c2: the
#: note said c1 while the marker said c2 (clone, 2026-10-03). A handle this
#: request minted is never re-minted. The list holds the dicts themselves (an
#: ``id()`` alone could be reused after garbage collection).
_MINTED_THIS_REQUEST: ContextVar[list[dict[str, Any]] | None] = ContextVar(
    "remark_handles_minted_this_request", default=None
)


#: ``chat.conversation.metadata`` key holding comment_reply failures the model
#: has not been told about yet (list of ``{"to": "c99", "reason": "…"}``).
REPLY_FAILURES_KEY = "remark_reply_failures"


def _cxm() -> Any | None:
    try:
        from matrx_ai.db import cxm

        return cxm
    except Exception as exc:  # noqa: BLE001 — no DB wired (a bare package / unit test)
        vcprint(f"[remark_handles] no conversation store ({exc})", color="yellow")
        return None


async def stored_handle_floor(conversation_id: str | None) -> int:
    """The highest handle stored in ANY user message of the conversation."""
    if not conversation_id:
        return 0
    managers = _cxm()
    if managers is None:
        return 0
    try:
        rows = (
            await managers.message.model.filter(
                conversation_id=conversation_id,
                role="user",
                content__json_contains=[{"type": REMARKS_PART_TYPE}],
            )
            .only("id", "content")
            .all()
        )
    except Exception as exc:  # noqa: BLE001 — loud; the reply side refuses a duplicate
        vcprint(
            f"[remark_handles] could not read stored handles ({type(exc).__name__}: {exc}) — "
            "numbering from the loaded history only; a duplicate handle is refused at reply time.",
            color="red",
        )
        return 0
    floor = 0
    for row in rows:
        for item in remark_item_dicts(getattr(row, "content", None) or []):  # orm-getattr-ok: model row
            floor = max(floor, handle_number(item.get("handle")) or 0)
    return floor


async def assign_remark_handles(
    history: Sequence[Any],
    fresh_items: Sequence[dict[str, Any]],
    conversation_id: str | None,
) -> None:
    """Give every fresh remark item its ``id`` and ``handle`` (mutates the dicts,
    which are what the message persists)."""
    fresh_ids = {id(item) for item in fresh_items}
    known: dict[str, str] = {}
    floor = 0
    for message in history:
        for item in remark_item_dicts(getattr(message, "content", None) or ()):
            if id(item) in fresh_ids:
                continue
            number = handle_number(item.get("handle"))
            if number is None:
                continue
            floor = max(floor, number)
            if item.get("id"):
                known.setdefault(str(item["id"]), str(item["handle"]))

    minted = _MINTED_THIS_REQUEST.get()
    if minted is None:
        minted = []
        _MINTED_THIS_REQUEST.set(minted)

    pending: list[dict[str, Any]] = []
    for item in fresh_items:
        if item.get("handle") and any(m is item for m in minted):
            continue  # this request minted it already — never renumber
        if not item.get("id"):
            item["id"] = str(uuid4())
        prior = known.get(str(item["id"]))
        if prior:
            item["handle"] = prior
            continue
        item.pop("handle", None)  # never trust a client-supplied handle
        pending.append(item)
    if not pending:
        return

    floor = max(floor, await stored_handle_floor(conversation_id))
    for offset, item in enumerate(pending, start=1):
        item["handle"] = format_handle(floor + offset)
        minted.append(item)


async def _conversation_metadata(managers: Any, conversation_id: str) -> dict[str, Any]:
    row = await managers.conversation.model.filter(id=conversation_id).only("id", "metadata").first()
    metadata = getattr(row, "metadata", None) if row is not None else None  # orm-getattr-ok: model row
    return dict(metadata) if isinstance(metadata, dict) else {}


def _queue_metadata(conversation_id: str, metadata: dict[str, Any]) -> bool:
    from matrx_ai.persistence.queue_helpers import get_coordinator, queue_conversation_update

    if get_coordinator() is None:
        vcprint(
            f"[remark_handles] no WriteCoordinator — the reply-failure note for "
            f"{conversation_id} was not saved (chat.conversation is coordinator-owned)",
            color="red",
        )
        return False
    queue_conversation_update(conversation_id, metadata=metadata)
    return True


async def drain_reply_failures(conversation_id: str | None) -> list[dict[str, Any]]:
    """Take (and clear) the comment_reply failures recorded on the conversation."""
    if not conversation_id:
        return []
    managers = _cxm()
    if managers is None:
        return []
    try:
        metadata = await _conversation_metadata(managers, conversation_id)
    except Exception as exc:  # noqa: BLE001 — wording, never a failed turn; loud
        vcprint(f"[remark_handles] could not read reply failures: {exc}", color="red")
        return []
    failures = metadata.get(REPLY_FAILURES_KEY)
    if not failures:
        return []
    metadata.pop(REPLY_FAILURES_KEY, None)
    _queue_metadata(conversation_id, metadata)
    return [f for f in failures if isinstance(f, dict)]


async def record_reply_failures(conversation_id: str | None, failures: Sequence[dict[str, Any]]) -> None:
    """Remember comment_reply failures so the NEXT remarks text tells the model
    (``drain_reply_failures``). Loud on failure — it is the model's only way to
    learn its reply did not land."""
    if not conversation_id or not failures:
        return
    managers = _cxm()
    if managers is None:
        return
    metadata = await _conversation_metadata(managers, conversation_id)
    prior = metadata.get(REPLY_FAILURES_KEY)
    merged = [*(prior if isinstance(prior, list) else []), *(dict(f) for f in failures)]
    metadata[REPLY_FAILURES_KEY] = merged[-20:]
    _queue_metadata(conversation_id, metadata)


__all__ = [
    "REPLY_FAILURES_KEY",
    "assign_remark_handles",
    "drain_reply_failures",
    "record_reply_failures",
    "stored_handle_floor",
]
