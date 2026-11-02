# File: matrx_files/blocks/record.py
"""This package's own write path into `platform.acquisition_block` (board row H8).

Board row H7 moved the ledger's decision logic (vocabulary, dedupe, the
refusal of an org-less block) out of aidream into `matrx_scraper.blocks`,
host-neutral, because the hosted scraper service cannot import aidream.
The IDENTICAL problem exists one layer earlier for matrx-files: the
standalone `matrx_files.standalone.app` service cannot import matrx-scraper
either (independence boundary — matrx-files depends on matrx-utils/connect/orm
only), so a DRM wall, an unsupported container, an empty file, or a missing
OCR binary hit while THAT process is running became a silent no-op — there
was no `matrx_files.blocks` module at all before this one.

This module is the minimal version of `matrx_scraper.blocks.record`: same
two rules (never raise into the read path it observes; a repeat is a count,
not a duplicate), no `rung`/`rung_trail` concept (there is no capture ladder
for a file read — a file either opens or it does not), and a small,
package-local vocabulary (`vocabulary.py`) instead of the platform's full one.
"""

from __future__ import annotations

from matrx_orm import db_sqlstate

import logging
from datetime import UTC, datetime
from typing import Any

from matrx_utils.person_sentence import person_sentence

from matrx_files.blocks.store import BlockStore
from matrx_files.blocks.unblock import unblock_for
from matrx_files.blocks.vocabulary import ENGINE, ERROR_CLASSES, SOURCE_TYPE

__all__ = ["record_block"]

_log = logging.getLogger("matrx_files.blocks")

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
    error_class: str,
    error_sentence: str,
    # `announce_block`'s general surface (`matrx_utils.block_sink.REQUIRED_FIELDS`
    # + its documented optionals) includes `engine` and `source_type` on EVERY
    # call — a reader that calls `announce_block` directly names them, exactly
    # as `matrx_scraper.blocks.record.record_block` requires. This package only
    # ever writes ONE of each (`vocabulary.ENGINE` / `vocabulary.SOURCE_TYPE`),
    # so they are accepted and VALIDATED rather than silently ignored: a caller
    # that named a different engine or source type has the wrong module, and
    # that is a defect worth a loud refusal, not a quietly mislabeled row.
    engine: str = ENGINE,
    source_type: str = SOURCE_TYPE,
    input_label: str = "",
    unblock_note: str = "",
    detail: dict[str, Any] | None = None,
    library_id: str | None = None,
    user_id: str | None = None,
    # Accepted and ignored: this package has no capture ladder, so a rung is
    # never meaningful here, but a caller sharing the platform-wide
    # `announce_block(...)` call shape (rung=None, rung_trail=[]) must not
    # crash on it.
    rung: str | None = None,
    rung_trail: list[dict[str, Any]] | None = None,
    handoff_id: str | None = None,
    store: BlockStore,
) -> str | None:
    """Record one file-reader block. Returns the row id, or `None`.

    `None` is never an error the caller handles — it means the ledger could
    not take this one, and the reason is in the log. THE ONE RULE (matching
    `matrx_scraper.blocks.record`): this never raises into the read path
    that hit the wall.
    """
    try:
        if engine != ENGINE:
            _log.error("a file-reader block named an engine this store does not write: %r", engine)
            return None
        if source_type != SOURCE_TYPE:
            _log.error(
                "a file-reader block named a source type this store does not write: %r",
                source_type,
            )
            return None
        return await _record(
            organization_id=organization_id,
            input_ref=input_ref,
            error_class=error_class,
            error_sentence=error_sentence,
            input_label=input_label,
            unblock_note=unblock_note,
            detail=detail,
            library_id=library_id,
            user_id=user_id,
            store=store,
        )
    except Exception:  # noqa: BLE001 — THE ONE RULE
        _log.error(
            "recording a file-reader block failed (%s on %s) — the read path is unaffected",
            error_class,
            input_ref,
            exc_info=True,
        )
        return None


async def _record(
    *,
    organization_id: str | None,
    input_ref: str,
    error_class: str,
    error_sentence: str,
    input_label: str,
    unblock_note: str,
    detail: dict[str, Any] | None,
    library_id: str | None,
    user_id: str | None,
    store: BlockStore,
) -> str | None:
    # An org is REQUIRED and is never chosen for the writer (db-rules §2 /
    # no-db-assigned-org). A block with no organization is a defect in the
    # caller.
    if not organization_id:
        _log.error(
            "a file-reader block arrived with no organization and was not recorded: %s on %s "
            "— %s",
            error_class,
            input_ref,
            error_sentence,
        )
        return None

    if error_class not in ERROR_CLASSES:
        _log.error(
            "a file-reader block named an error class this store does not know: %r", error_class
        )
        return None

    input_ref = _clean(input_ref, 4000)
    if not input_ref or not str(error_sentence or "").strip():
        _log.error("a file-reader block arrived without an input or a sentence and was dropped")
        return None

    # 🚨 DRIVER TEXT IS NEVER THE SENTENCE — the same rule, at this package's own
    # seam, for the same reason `matrx_scraper.blocks.record` states at length:
    # `error_sentence` is a person-facing column, a caller is one bad `except`
    # away from assigning `str(exc)` to it, and on 2026-09-20 one did — a raw
    # `INSERT INTO … VALUES ($1, $2 … Args: (…)` reached `/acquisition`. The raw
    # text goes to `detail`, which is diagnostic-only.
    spoken = person_sentence(error_sentence)
    sentence = _clean(spoken.text, _SENTENCE_LIMIT)
    detail = dict(detail or {})
    if spoken.diagnostic:
        _log.warning(
            "a file-reader block arrived with machine text as its sentence (%s on %s) — the "
            "person reads the classified cause and the raw text is in detail.diagnostic",
            error_class,
            input_ref,
        )
        detail["diagnostic"] = {
            **(detail.get("diagnostic") if isinstance(detail.get("diagnostic"), dict) else {}),
            "raw_error": spoken.diagnostic,
        }

    route = unblock_for(error_class)
    note = unblock_note or route.note
    status = "decision" if route.is_decision else "open"

    now = _now()
    existing = await store.find_open(
        organization_id=organization_id,
        input_ref=input_ref,
        source_type=SOURCE_TYPE,
        error_class=error_class,
    )

    if existing is not None:
        block_id = str(getattr(existing, "id", "") or "")
        previous = int(getattr(existing, "occurrence_count", 0) or 0)
        updated = await store.update(
            block_id,
            occurrence_count=previous + 1,
            last_seen_at=now,
            error_sentence=sentence,
            unblock_note=note,
            lawful_route=route.route,
            detail=detail or {},
            library_id=library_id,
            updated_by=user_id,
        )
        return str(getattr(updated, "id", block_id) or block_id)

    try:
        created = await store.create(
            organization_id=organization_id,
            input_ref=input_ref,
            input_label=_clean(input_label, 300),
            source_type=SOURCE_TYPE,
            engine=ENGINE,
            rung=None,
            rung_trail=[],
            error_class=error_class,
            error_sentence=sentence,
            unblock_note=note,
            lawful_route=route.route,
            first_seen_at=now,
            last_seen_at=now,
            occurrence_count=1,
            status=status,
            retry_count=0,
            detail=detail or {},
            library_id=library_id,
            created_by=user_id,
            updated_by=user_id,
        )
        return str(getattr(created, "id", "") or "") or None
    except Exception as exc:  # noqa: BLE001 — two readers can fail on the same input at once
        if not _is_dedupe_conflict(exc):
            raise
        winner = await store.find_open(
            organization_id=organization_id,
            input_ref=input_ref,
            source_type=SOURCE_TYPE,
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
    return db_sqlstate(exc) == "23505"
