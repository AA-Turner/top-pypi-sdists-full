"""The ONE write seam of the Block Ledger — host-neutral, so every host shares it.

Every failed acquisition anywhere on the platform arrives here and leaves as one row in
`platform.acquisition_block`. The engines that fail do not know about this module: the ones
inside packages announce through `matrx_utils.block_sink`, and the ones inside aidream call
`record_block()` directly. Either way there is one function that decides what a row is.

🚨 **Why this lives in matrx-scraper and not in aidream.** It used to live in aidream, and the
consequence was board row H7: the hosted scraper service (`scraper.app.matrxserver.com`) runs
an image that installs `packages/` and NOT aidream, so it could never wire the sink and every
failure it caused was a silent no-op for the ledger. The rules of the ledger — the closed
vocabularies, the lawful routes, the dedupe — are not aidream's; they belong beside
`matrx_scraper.ladder`, which already owns the rung contract this module's `RUNGS` come from.
What stays host-specific is only the TABLE ACCESS, injected as `store`, and the organization,
which a package never knows and a host always does.

🚨 **THE ONE RULE: recording a block never raises into the acquisition path it observes.**
Everything below is inside a `try`, and a failure to record is logged loudly and swallowed.
A ledger that can break an acquisition is worse than no ledger (board row H2's own note:
"the one shared write seam must never raise into the acquisition path it observes").

🚨 **The second rule: a repeat is a count, not a duplicate.** The same (organization, input,
source type, error class) is ONE row whose `occurrence_count` grows and whose `last_seen_at`
moves. The partial unique index `acquisition_block_dedupe_uniq` is what holds when two engines
fail on the same page in the same second; the read-then-write below is what keeps the normal
case to one round trip more than a blind insert.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from matrx_utils.person_sentence import person_sentence

from matrx_scraper.blocks.store import BlockStore
from matrx_scraper.blocks.unblock import unblock_for
from matrx_scraper.blocks.vocabulary import ENGINES, RUNGS, SOURCE_TYPES

__all__ = ["record_block"]

_log = logging.getLogger("matrx_scraper.blocks")

#: How much of a provider's sentence we keep verbatim. Long enough for every real message we
#: have measured, short enough that a runaway stack trace never becomes the row.
_SENTENCE_LIMIT = 2000


def _now() -> datetime:
    return datetime.now(UTC)


def _clean(value: Any, limit: int = 500) -> str:
    text = str(value or "").strip()
    return text[:limit]


async def record_block(
    *,
    organization_id: str | None,
    input_ref: str,
    source_type: str,
    engine: str,
    error_class: str,
    error_sentence: str,
    rung: str | None = None,
    rung_trail: list[dict[str, Any]] | None = None,
    input_label: str = "",
    unblock_note: str = "",
    lawful_route: str | None = None,
    detail: dict[str, Any] | None = None,
    handoff_id: str | None = None,
    library_id: str | None = None,
    user_id: str | None = None,
    store: BlockStore,
) -> str | None:
    """Record one block. Returns the row id, or `None` when nothing was recorded.

    `None` is never an error the caller handles — it means the ledger could not take this one,
    and the reason is in the log. The caller is already dealing with a failure of its own.
    """
    try:
        return await _record(
            organization_id=organization_id,
            input_ref=input_ref,
            source_type=source_type,
            engine=engine,
            error_class=error_class,
            error_sentence=error_sentence,
            rung=rung,
            rung_trail=rung_trail,
            input_label=input_label,
            unblock_note=unblock_note,
            lawful_route=lawful_route,
            detail=detail,
            handoff_id=handoff_id,
            library_id=library_id,
            user_id=user_id,
            store=store,
        )
    except Exception:  # noqa: BLE001 — THE ONE RULE
        _log.error(
            "recording a block failed (%s on %s) — the acquisition path is unaffected",
            error_class,
            input_ref,
            exc_info=True,
        )
        return None


async def _record(
    *,
    organization_id: str | None,
    input_ref: str,
    source_type: str,
    engine: str,
    error_class: str,
    error_sentence: str,
    rung: str | None,
    rung_trail: list[dict[str, Any]] | None,
    input_label: str,
    unblock_note: str,
    lawful_route: str | None,
    detail: dict[str, Any] | None,
    handoff_id: str | None,
    library_id: str | None,
    user_id: str | None,
    store: BlockStore,
) -> str | None:
    # ── An org is REQUIRED and is never chosen for the writer ────────────────
    # (db-rules §2 / no-db-assigned-org: no personal, system or parent fallback.) A block with
    # no organization is a defect in the caller, and saying so is more useful than a row
    # somebody else's screen would show.
    if not organization_id:
        _log.error(
            "a block arrived with no organization and was not recorded: %s on %s — %s",
            error_class,
            input_ref,
            error_sentence,
        )
        return None

    if engine not in ENGINES:
        _log.error("a block named an engine the ledger does not know: %r", engine)
        return None
    if source_type not in SOURCE_TYPES:
        _log.error("a block named a source type the ledger does not know: %r", source_type)
        return None
    if rung is not None and rung not in RUNGS:
        _log.error("a block named a rung the ladder does not have: %r", rung)
        return None

    input_ref = _clean(input_ref, 4000)
    if not input_ref or not str(error_sentence or "").strip():
        _log.error("a block arrived without an input or without a sentence and was dropped")
        return None

    # ── 🚨 DRIVER TEXT IS NEVER THE SENTENCE (fourteenth cold walk, 2026-09-20) ──
    # `/acquisition` printed a raw `INSERT INTO docproc.processed_documents … VALUES
    # ($1, $2, … Args: ('03e3dab7-…', …)` inside a block row, because the caller that
    # caught a `QueryTimeoutError` assigned `str(exc)` straight to `error_sentence`
    # and every reader downstream faithfully rendered what it was handed. A schema,
    # a statement and its bound argument values, on a screen otherwise written in
    # careful English.
    #
    # Fixing the caller alone would be fixing the instance: `error_sentence` is a
    # PERSON-FACING column and there are ~14 callers, any of which is one bad
    # `except` away from doing it again. So the rule is structural and lives HERE,
    # at the one seam every block passes through — raw exception text becomes a
    # sentence from its classified cause, and the raw text rides in `detail`, which
    # is diagnostic-only and never rendered as prose.
    spoken = person_sentence(error_sentence)
    sentence = _clean(spoken.text, _SENTENCE_LIMIT)
    detail = dict(detail or {})
    if spoken.diagnostic:
        _log.warning(
            "a block arrived with machine text as its sentence (%s on %s) — the person reads "
            "the classified cause and the raw text is in detail.diagnostic",
            error_class,
            input_ref,
        )
        detail["diagnostic"] = {
            **(detail.get("diagnostic") if isinstance(detail.get("diagnostic"), dict) else {}),
            "raw_error": spoken.diagnostic,
        }

    # The lawful route is looked up, never invented. An explicit note from the caller wins,
    # because the engine that failed knows more about this one than the table does.
    route = unblock_for(error_class)
    note = unblock_note or route.note
    machine_route = lawful_route or route.route
    status = "decision" if route.is_decision else "open"

    now = _now()
    existing = await store.find_open(
        organization_id=organization_id,
        input_ref=input_ref,
        source_type=source_type,
        error_class=error_class,
    )

    if existing is not None:
        block_id = str(getattr(existing, "id", "") or "")
        previous = int(getattr(existing, "occurrence_count", 0) or 0)
        updated = await store.update(
            block_id,
            occurrence_count=previous + 1,
            last_seen_at=now,
            # The newest sentence wins: a site whose refusal changed from 403 to a paywall
            # notice is telling us something, and the old words would hide it.
            error_sentence=sentence,
            engine=engine,
            rung=rung,
            rung_trail=rung_trail or [],
            unblock_note=note,
            lawful_route=machine_route,
            detail=detail or {},
            handoff_id=handoff_id,
            library_id=library_id,
            updated_by=user_id,
        )
        return str(getattr(updated, "id", block_id) or block_id)

    try:
        created = await store.create(
            organization_id=organization_id,
            input_ref=input_ref,
            input_label=_clean(input_label, 300),
            source_type=source_type,
            engine=engine,
            rung=rung,
            rung_trail=rung_trail or [],
            error_class=error_class,
            error_sentence=sentence,
            unblock_note=note,
            lawful_route=machine_route,
            first_seen_at=now,
            last_seen_at=now,
            occurrence_count=1,
            status=status,
            retry_count=0,
            detail=detail or {},
            handoff_id=handoff_id,
            library_id=library_id,
            created_by=user_id,
            updated_by=user_id,
        )
        return str(getattr(created, "id", "") or "") or None
    except Exception as exc:  # noqa: BLE001 — one failure is normal here
        # Two engines failed on the same page in the same moment and the unique index caught
        # the second. That is the index doing its job: read the winner and count this one.
        if not _is_dedupe_conflict(exc):
            raise
        winner = await store.find_open(
            organization_id=organization_id,
            input_ref=input_ref,
            source_type=source_type,
            error_class=error_class,
        )
        if winner is None:
            raise
        block_id = str(getattr(winner, "id", "") or "")
        previous = int(getattr(winner, "occurrence_count", 0) or 0)
        await store.update(
            block_id,
            occurrence_count=previous + 1,
            last_seen_at=now,
            updated_by=user_id,
        )
        return block_id


def _is_dedupe_conflict(exc: Exception) -> bool:
    text = str(exc)
    return "acquisition_block_dedupe_uniq" in text or "23505" in text
