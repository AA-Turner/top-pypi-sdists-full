"""
U8 — Bulk page-verification surface for a processed_document.

Makes a big extraction reviewable: scan every page and flag the ones a curator
should look at — near-empty / image-only pages, low extraction confidence, and
"the cleaner may have eaten content" shrinkage (the known gpt-4o-mini failure
where a content page is returned blank). Cheap: pure read + heuristics over
``processed_document_pages``, no LLM, no embeddings. Returns a structured report
the studio renders (raw-vs-clean review, flag filters).

This is the review counterpart to the derivation utilities: derive_* produce
the premium representations; verify_processed_document tells the curator which
source pages to fix first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from matrx_orm import transaction

from matrx_rag._ext import NotFoundError, get_db_model
from matrx_rag.llm import page_is_cleaned
from matrx_rag.stages import ProgressCb, StageEvent, _noop

# Flag reasons (stable strings — the FE filters on these).
NEAR_EMPTY = "near_empty"  # almost no extracted text — image/chart page or failed extract
LOW_CONFIDENCE = "low_confidence"  # extractor's own confidence below threshold
CLEAN_SHRANK = (
    "clean_shrank"  # cleaned_text is a tiny fraction of raw — cleaner may have dropped content
)
CLEAN_EMPTIED = (
    "clean_emptied"  # page HAD raw text but the cleaner blanked it ENTIRELY — likely lost content
)
NO_TEXT = "no_text"  # neither raw nor cleaned text at all


@dataclass
class PageFlag:
    page_number: int
    reasons: list[str]
    raw_chars: int
    cleaned_chars: int
    confidence: float | None
    has_image: bool


@dataclass
class VerificationReport:
    processed_document_id: str
    total_pages: int
    flagged_pages: int
    counts: dict[str, int] = field(default_factory=dict)  # reason -> count
    flags: list[PageFlag] = field(default_factory=list)  # one per flagged page
    chunks_written: int = 0  # pages verified — the countable output for derive_runs


async def verify_processed_document(
    processed_document_id: str,
    *,
    near_empty_chars: int = 80,
    low_confidence: float = 0.60,
    clean_shrink_ratio: float = 0.30,
    clean_shrink_min_raw: int = 200,
    on_progress: ProgressCb = _noop,
) -> VerificationReport:
    """Scan the doc's pages and flag the ones worth a curator's review.

    Thresholds are tunable. A page may carry several reasons. Pages with no
    issues are omitted from ``flags`` (only flagged pages are returned), but
    ``total_pages`` reflects the whole doc.
    """
    # Validate the doc exists (distinct from "doc with zero pages").
    if not await get_db_model("ProcessedDocuments").exists(id=processed_document_id):
        raise NotFoundError(f"processed_document {processed_document_id} not found")
    pages = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values(
            "page_number",
            "raw_text",
            "cleaned_text",
            "section_kind",
            "extraction_confidence",
            "image_cld_file_id",
        )
    )

    total_pages = len(pages)
    # Did cleaning run on this doc at all? If ANY page has cleaned text, then an
    # empty cleaned_text on a page that HAD raw content means the cleaner blanked
    # it (lost content) — vs. a doc that was simply never cleaned, where empty
    # cleaned_text is expected and must NOT be flagged.
    # page_is_cleaned, not cleaned_text emptiness: an all-illegible doc is
    # cleaned (every page cleaned to "" with section_kind set).
    doc_cleaned = any(page_is_cleaned(p["cleaned_text"], p["section_kind"]) for p in pages)
    await on_progress(
        StageEvent(
            stage="page_verification",
            phase="started",
            message=f"Verifying {total_pages} page(s)",
            current=0,
            total=total_pages,
            extra={"granularity": "page_verification"},
        )
    )
    emit_every = max(1, total_pages // 50)
    last_emit = 0

    counts: dict[str, int] = {}
    flags: list[PageFlag] = []
    for seen, p in enumerate(pages, start=1):
        # Throttled progress; this await is also the cooperative cancel point.
        if seen == total_pages or (seen - last_emit) >= emit_every:
            last_emit = seen
            await on_progress(
                StageEvent(
                    stage="page_verification",
                    phase="progress",
                    message=f"Verified page {seen} / {total_pages}",
                    current=seen,
                    total=total_pages,
                    extra={
                        "granularity": "page_verification",
                        "page_number": int(p["page_number"]),
                        "flagged_so_far": len(flags),
                    },
                )
            )
        raw = p["raw_text"] or ""
        cleaned = p["cleaned_text"] or ""
        raw_len = len(raw)
        cleaned_len = len(cleaned)
        conf = p["extraction_confidence"]
        has_image = p["image_cld_file_id"] is not None
        reasons: list[str] = []

        if raw_len == 0 and cleaned_len == 0:
            reasons.append(NO_TEXT)
        elif max(raw_len, cleaned_len) < near_empty_chars:
            reasons.append(NEAR_EMPTY)

        if conf is not None and conf < low_confidence:
            reasons.append(LOW_CONFIDENCE)

        # Cleaner-dropped-content guards. A page that HAD real raw content but
        # whose cleaned_text shrank far below it means the cleaner likely ate
        # content. Split into two so the curator sees which is which:
        #   clean_emptied — cleaner blanked the page ENTIRELY (worst case; only
        #     flagged when the doc was actually cleaned, so we never false-flag a
        #     doc that was simply never cleaned);
        #   clean_shrank  — cleaner kept some but dropped most.
        if raw_len >= clean_shrink_min_raw and cleaned_len < clean_shrink_ratio * raw_len:
            if cleaned_len == 0:
                if doc_cleaned:
                    reasons.append(CLEAN_EMPTIED)
            else:
                reasons.append(CLEAN_SHRANK)

        if reasons:
            for r in reasons:
                counts[r] = counts.get(r, 0) + 1
            flags.append(
                PageFlag(
                    page_number=int(p["page_number"]),
                    reasons=reasons,
                    raw_chars=raw_len,
                    cleaned_chars=cleaned_len,
                    confidence=float(conf) if conf is not None else None,
                    has_image=has_image,
                )
            )

    # Persist results so the count is REAL and the per-page "why" survives a
    # refresh. This used to write NOTHING — the UI's "verified pages" count
    # stayed 0 forever even on success (a no-fake-verification violation). We
    # mark EVERY page verified now, and stamp the flag reasons on the flagged
    # ones (the same reasons that explain "N of M pages have text"). Anchored to
    # the exact source page via (processed_document_id, page_number).
    Pages = get_db_model("ProcessedDocumentPages")
    now = datetime.now(UTC)
    async with transaction():
        # Mark every page verified, clearing any prior flags…
        await Pages.update_where(
            {"processed_document_id": processed_document_id},
            verified_at=now,
            verification_flags=None,
        )
        # …then stamp the reasons on the flagged pages, anchored to the exact
        # source page via (processed_document_id, page_number). A future
        # connection-scoped per-row bulk-UPDATE primitive would replace this loop.
        for f in flags:
            await Pages.update_where(
                {"processed_document_id": processed_document_id, "page_number": f.page_number},
                verification_flags=f.reasons,
            )

    await on_progress(
        StageEvent(
            stage="page_verification",
            phase="done",
            message=f"Flagged {len(flags)} of {total_pages} page(s)",
            current=total_pages,
            total=total_pages,
            extra={
                "granularity": "page_verification",
                "total_pages": total_pages,
                "flagged_pages": len(flags),
                "counts": counts,
            },
        )
    )

    return VerificationReport(
        processed_document_id=processed_document_id,
        total_pages=len(pages),
        flagged_pages=len(flags),
        counts=counts,
        flags=flags,
        chunks_written=len(pages),  # pages verified — the countable output
    )


__all__ = [
    "verify_processed_document",
    "VerificationReport",
    "PageFlag",
    "NEAR_EMPTY",
    "LOW_CONFIDENCE",
    "CLEAN_SHRANK",
    "CLEAN_EMPTIED",
    "NO_TEXT",
]
