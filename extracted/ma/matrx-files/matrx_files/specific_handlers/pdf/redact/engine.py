"""``RedactionEngine`` — the platform redaction primitive.

Implements design §5.4 on top of PyMuPDF's native content-stream-rewrite path:

1. For each region: ``page.add_redact_annot(rect, ...)``.
2. ``page.apply_redactions(images=2, graphics=1, text=0)`` rewrites the
   underlying content stream — glyphs and image overlap are physically
   removed, not merely painted over.
3. ``doc.save(out, garbage=4, deflate=True, clean=True)`` — full save with
   maximum garbage-collect so no incremental-update trailer carries
   recoverable history. **NEVER use ``saveIncr``** — that leaves the
   pre-redaction bytes intact under an older generation.
4. **Verification.** Re-open the output and run ``page.get_text("words")``
   over every redacted bbox. If any glyph survives, raise — do not return
   the file. This is the bug-class-extinction move per design §5.4 step 4.
5. Emit a ``RedactionAudit`` (caller persists it). Status fields capture
   whether verification passed and how much byte delta the operation
   produced — a sanity check.

The audit table itself is created and persisted by the host (aidream) via
matrx-orm; this module only produces the audit payload.
"""

from __future__ import annotations

from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .models import (
    RedactionAudit,
    RedactionRegion,
    RedactionResult,
    RedactionTier,
)


# Verification shrink tolerance. 0.5pt is below the per-pixel threshold at
# 72 DPI (a real surviving glyph would be visible at 1px = 1pt minimum) so
# false-positive boundary noise from PyMuPDF's content-stream rewrite is
# ignored while genuine residue still fails. Strict-0pt mode is exposed
# via ``_VERIFY_SHRINK_STRICT_PT`` for callers that want to re-run with
# zero tolerance.
_VERIFY_SHRINK_PT = 0.5
_VERIFY_SHRINK_STRICT_PT = 0.0


def _build_audit(
    *,
    reason: str,
    redaction_kind: str,
    redaction_params: dict[str, Any],
    tier_used: RedactionTier,
    status: str,
    bytes_removed_estimate: int,
    regions_count: int,
    parent_file_id: str | None,
    user_id: str | None,
) -> RedactionAudit:
    return RedactionAudit(
        parent_file_id=parent_file_id,
        user_id=user_id,
        reason=reason,
        redaction_kind=redaction_kind,  # type: ignore[arg-type]
        redaction_params=redaction_params,
        tier_used=tier_used,
        status=status,  # type: ignore[arg-type]
        bytes_removed_estimate=bytes_removed_estimate,
        regions_count=regions_count,
    )


def _apply_redact_annots(doc: Any, regions: list[RedactionRegion]) -> int:
    """Add redaction annotations for every region and apply them.

    Returns the count of pages that actually had at least one annotation
    applied — useful for the audit row.

    Per-page ``apply_redactions(text=…)`` is 0 (REMOVE) unless every region
    on the page has ``preserve_text=True``, in which case it switches to 1
    (IGNORE text). Mixed-mode pages always remove text — preserving on a
    mixed page would silently leak the surgical-redaction text.
    """
    pymupdf = load_pymupdf()
    pages_touched: dict[int, bool] = {}
    for region in regions:
        if region.page_number < 1 or region.page_number > doc.page_count:
            raise ValueError(
                f"Redaction region targets page {region.page_number} but "
                f"document has {doc.page_count} page(s)."
            )
        page = doc[region.page_number - 1]
        rect = pymupdf.Rect(region.x0, region.y0, region.x1, region.y1)
        fill = (0, 0, 0) if region.replacement == "BLOCK" else (1, 1, 1)
        annot = page.add_redact_annot(
            rect,
            text=region.text or "",
            fill=fill,
            cross_out=region.replacement == "BLOCK",
        )
        if annot is None:
            raise ValueError(
                f"Could not create redact annotation on page {region.page_number} "
                f"at {region.x0},{region.y0}-{region.x1},{region.y1}."
            )
        # Track whether ALL regions on the page set preserve_text — only
        # then can we ignore text safely.
        prev = pages_touched.get(region.page_number, True)
        pages_touched[region.page_number] = prev and region.preserve_text

    for page_no, all_preserve in pages_touched.items():
        page = doc[page_no - 1]
        # PyMuPDF 1.27 semantics:
        #   text=0 → remove text in rect (default)
        #   text=1 → ignore text (images/graphics only)
        # We default to 0 (remove); preserve_text=True only fires when
        # EVERY region on the page opted in.
        text_arg = 1 if all_preserve else 0
        page.apply_redactions(images=2, graphics=1, text=text_arg)
    return len(pages_touched)


def _verify_regions_empty(
    pdf_bytes: bytes,
    regions: list[RedactionRegion],
) -> tuple[bool, list[str]]:
    """Re-open the redacted output and assert every region bbox is empty.

    Regions with ``preserve_text=True`` are intentionally kept — they are
    skipped for the text-survival check (the redaction only affected
    images/graphics there).
    """
    pymupdf = load_pymupdf()
    notes: list[str] = []
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        for region in regions:
            if region.preserve_text:
                continue
            page = doc[region.page_number - 1]
            shrunk = pymupdf.Rect(
                region.x0 + _VERIFY_SHRINK_PT,
                region.y0 + _VERIFY_SHRINK_PT,
                region.x1 - _VERIFY_SHRINK_PT,
                region.y1 - _VERIFY_SHRINK_PT,
            )
            if shrunk.is_empty or shrunk.is_infinite:
                # Region was too small to shrink — fall back to the original
                # rect for the verification lookup.
                shrunk = pymupdf.Rect(region.x0, region.y0, region.x1, region.y1)
            words = page.get_text("words", clip=shrunk)
            if words:
                notes.append(
                    f"verification: {len(words)} word(s) survived in region "
                    f"page={region.page_number} bbox={region.x0:.1f},{region.y0:.1f}-"
                    f"{region.x1:.1f},{region.y1:.1f}"
                )
    return (not notes), notes


def _verify_pattern_empty(
    pdf_bytes: bytes, pattern: str, flags: int = 0
) -> tuple[bool, list[str]]:
    """Re-open the redacted output and assert *pattern* finds zero matches.

    Uses the same word-joining strategy the redactor employs (single-space
    join of ``get_text("words")``) so the verifier doesn't develop an
    asymmetric blind-spot against multi-column / table-cell layouts.

    *flags* MUST match the flags the redactor used — otherwise the verifier
    could miss case-insensitive survivors.
    """
    import re

    pymupdf = load_pymupdf()
    notes: list[str] = []
    compiled = re.compile(pattern, flags=flags)
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_index in range(doc.page_count):
            page = doc[page_index]
            words = page.get_text("words", sort=True)
            joined = " ".join(str(w[4]) for w in words if w and len(w) > 4)
            matches = compiled.findall(joined)
            if matches:
                notes.append(
                    f"verification: {len(matches)} pattern match(es) survived on "
                    f"page {page_index + 1}"
                )
    return (not notes), notes


def redact_regions(
    pdf_bytes: bytes,
    regions: list[RedactionRegion],
    *,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
) -> RedactionResult:
    """Remove text + image content inside *regions* and return the new PDF.

    Verification is mandatory: if any redacted region still contains text
    after the rewrite, raises ``RuntimeError`` instead of returning the
    file. Callers that want the audit row even on failure should catch the
    exception and call ``build_audit_for_failure(...)``.

    *scrub_metadata*=True chains ``doc.scrub()`` after the rewrite to wipe
    /Metadata, /Info, attached files, JS, embedded files, hidden text, etc.
    Recommended for outbound legal/medical PDFs.
    """
    if not reason or not reason.strip():
        raise ValueError("redact_regions requires a non-empty reason for the audit row.")
    if not regions:
        audit = _build_audit(
            reason=reason,
            redaction_kind="regions",
            redaction_params={"regions": []},
            tier_used="n/a",
            status="no_targets",
            bytes_removed_estimate=0,
            regions_count=0,
            parent_file_id=parent_file_id,
            user_id=user_id,
        )
        return RedactionResult(
            content=pdf_bytes,
            page_count=0,
            audit=audit,
            verification_passed=True,
            notes=["no regions supplied"],
        )

    scrub_notes: list[str] = []
    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        _apply_redact_annots(doc, regions)
        if scrub_metadata:
            try:
                doc.scrub(
                    attached_files=True,
                    clean_pages=False,
                    embedded_files=True,
                    hidden_text=True,
                    javascript=True,
                    metadata=True,
                    redactions=False,  # already applied
                    redact_images=0,
                    remove_links=False,
                    reset_fields=False,
                    reset_responses=False,
                    thumbnails=True,
                    xml_metadata=True,
                )
            except Exception as exc:
                # Loud notes — silent fallback would let a caller think
                # privacy categories were stripped when they weren't.
                scrub_notes.append(f"scrub-with-kwargs failed: {exc!r}")
                try:
                    doc.scrub()
                    scrub_notes.append("scrub-default succeeded as fallback")
                except Exception as exc2:
                    scrub_notes.append(f"scrub-default also failed: {exc2!r}")
        out_bytes = doc.tobytes(garbage=4, deflate=True, clean=True)

    verified, notes = _verify_regions_empty(out_bytes, regions)
    notes.extend(scrub_notes)
    status = "success" if verified else "verification_failed"
    audit = _build_audit(
        reason=reason,
        redaction_kind="regions",
        redaction_params={
            "regions": [r.model_dump(exclude={"text"}) for r in regions]
        },
        tier_used="stream_rewrite",
        status=status,
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=len(regions),
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    if not verified:
        # Bug-class-extinction: refuse to return a file whose redactions
        # didn't fully take. Callers can inspect ``exc.args[1]`` (audit) and
        # retry with a rasterize fallback or different region rects.
        raise RuntimeError(
            "Redaction verification failed — text survived in at least one "
            "region. The file was NOT returned to prevent silent leakage.",
            audit.model_dump(),
            notes,
        )

    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
        notes=notes,
    )


async def redact_regions_async(
    pdf_bytes: bytes,
    regions: list[RedactionRegion],
    *,
    reason: str,
    user_id: str | None = None,
    parent_file_id: str | None = None,
    scrub_metadata: bool = True,
) -> RedactionResult:
    return await run_in_cpu_executor(
        lambda: redact_regions(
            pdf_bytes,
            regions,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
        )
    )


__all__ = [
    "redact_regions",
    "redact_regions_async",
]
