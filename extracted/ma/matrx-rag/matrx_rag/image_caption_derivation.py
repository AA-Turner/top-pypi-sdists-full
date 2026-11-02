"""
U2 — Image Extractor → caption + index (a Knowledge Asset derivation).

Figures, diagrams, and charts inside a PDF are invisible to text search. This
utility captions them: for each FIGURE-BEARING page, run vision over the
rendered page image (alt/caption/description/OCR/keywords) and index it as a
`derivation_kind='page_image_caption'` chunk, page-anchored, so a query like
"anatomical range-of-motion frontal plane diagram" lands on the right page even
though no text on that page says it.

A generator on `matrx_rag.derivation.derive_chunk_set`. Targeted by design: it
only captions pages that actually carry visual content (raster images or heavy
vector drawings), so plain-text pages don't burn vision calls or add noise.
Requires the page images to already be rendered onto
`processed_document_pages.image_cld_file_id` (see
`aidream/services/documents/page_image.render_page_image`).

Closes the gap that `image_pipeline.ingest_image` only handles standalone image
FILES — nothing captioned a PDF page's figure with page provenance until now.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from matrx_rag._ext import NotFoundError, get_db_model, get_page_image_renderer
from matrx_rag.derivation import (
    ChunkSpec,
    DeriveResult,
    derive_chunk_set,
    existing_max_chunk_index,
    existing_page_numbers,
)
from matrx_rag.stages import ProgressCb, StageEvent, _noop

log = logging.getLogger(__name__)

# A page is "figure-bearing" if it has raster images or substantial vector
# graphics (line-art diagrams / charts). Matches the profiler heuristic.
_DRAWINGS_FIGURE_THRESHOLD = 40

# Persist captioned pages after this many — each flush is an APPEND
# (replace=False) that makes the paid vision work durable IMMEDIATELY, so a
# mid-run death keeps every completed batch instead of losing them all to one
# final end-only write. Mirrors knowledge_derivations._FLUSH_EVERY.
_FLUSH_EVERY = 12

# The figure-caption default vision model is HOST-SUPPLIED via
# ``matrx_rag.configure(default_vision_model=...)`` and read through
# ``_ext.get_default_vision_model()``; an explicit ``vision_model=`` argument
# always wins. The package ships no model identifier of its own.


@dataclass
class ImageCaptionResult:
    processed_document_id: str
    figure_pages: int
    captioned: int
    chunks_written: int


def _detect_figure_pages(local_path: str) -> set[int]:
    """1-based page numbers that carry visual content (raster or heavy vector)."""
    import pymupdf

    figs: set[int] = set()
    doc = pymupdf.open(local_path)
    try:
        for i, page in enumerate(doc):
            try:
                n_images = len(page.get_images(full=True))
            except Exception:
                n_images = 0
            try:
                n_draw = len(page.get_drawings())
            except Exception:
                n_draw = 0
            if n_images > 0 or n_draw > _DRAWINGS_FIGURE_THRESHOLD:
                figs.add(i + 1)
    finally:
        doc.close()
    return figs


def _caption_to_text(enr: dict, page_number: int) -> str:
    """Project a vision enrichment into embeddable, retrieval-friendly text."""
    lines = [f"PAGE: {page_number}"]
    if enr.get("title"):
        lines.append(enr["title"])
    if enr.get("caption"):
        lines.append(f"FIGURE: {enr['caption']}")
    if enr.get("description"):
        lines.append(enr["description"])
    alt = enr.get("alt_text")
    if alt and alt != enr.get("caption"):
        lines.append(alt)
    if enr.get("ocr_text"):
        lines.append(f"OCR: {enr['ocr_text']}")
    if enr.get("keywords"):
        lines.append("KEYWORDS: " + ", ".join(enr["keywords"]))
    return "\n".join(lines).strip()


async def derive_page_image_captions(
    processed_document_id: str,
    *,
    page_numbers: set[int] | None = None,
    embedding_model: str | None = None,
    rag_boost: int = 0,
    vision_model: str | None = None,
    auto_render: bool = True,
    max_concurrent: int = 8,
    reset: bool = False,
    on_progress: ProgressCb = _noop,
) -> ImageCaptionResult:
    """Caption every figure-bearing page that has a rendered image, and index
    the captions as a ``page_image_caption`` derivation set.

    ``page_numbers`` (1-based) overrides figure auto-detection. If a requested
    page has no rendered ``image_cld_file_id`` it is skipped.

    Every per-page vision call is dispatched immediately; matrx-ai centrally
    admits calls at the resolved provider endpoint. ``max_concurrent`` is kept
    for compatibility and only bounds the local PDF render pre-pass. Per-page
    failures stay isolated and each completed caption streams a
    ``page_image_caption`` progress event.

    INCREMENTAL + RESUMABLE (same money-loss fix as the section-summary path).
    Captioned pages are persisted in batches of ``_FLUSH_EVERY`` via an APPEND
    write (``replace=False``), so a mid-run death keeps every completed batch —
    paid vision calls are never lost to one final all-or-nothing write. On a
    re-run (``reset=False``, the default) pages whose caption chunks already
    exist are SKIPPED *before* both the vision call and the auto-render pre-pass
    (no re-spend, no wasted render). ``reset=True`` clears the set once, then
    re-captions everything from scratch.
    """
    import asyncio

    ProcessedDocuments = get_db_model("ProcessedDocuments")
    doc_rows = await ProcessedDocuments.filter(id=processed_document_id).values(
        "id", "source_kind", "source_id", "name", "created_by"
    )
    doc = doc_rows[0] if doc_rows else None
    if doc is None:
        raise NotFoundError(f"processed_document {processed_document_id} not found")

    # Which pages to caption: explicit override, else figure pages auto-detected
    # from the source PDF (raster images / heavy vector line-art).
    candidate_pages: set[int] | None = None
    if page_numbers is not None:
        candidate_pages = set(page_numbers)
    elif doc["source_kind"] == "cld_file":
        from matrx_rag.table_derivation import _fetch_pdf_to_temp

        local_path = await _fetch_pdf_to_temp(doc["source_id"])
        try:
            # CPU-bound (pymupdf page scan) — offload so it can't stall the loop.
            candidate_pages = await asyncio.to_thread(_detect_figure_pages, local_path)
        finally:
            try:
                os.unlink(local_path)
            except OSError:
                pass

    # Resume bookkeeping (mirrors derive_section_summaries). reset → clear the
    # whole set once via the empty-replace path (deletes prior caption chunks)
    # and treat nothing as done. Otherwise read which page_numbers are already
    # persisted; those are skipped below — BEFORE the vision call AND before the
    # auto-render pre-pass, so a resumed run neither re-captions nor re-renders a
    # page it already did. ``done`` is best-effort (empty on read error).
    if reset:
        await derive_chunk_set(
            parent_processed_id=processed_document_id,
            derivation_kind="page_image_caption",
            chunks=[],
            identity={"source": "page_image_caption"},
            name=f"{doc['name']} (figure captions)",
            rag_boost=rag_boost,
            embedding_model=embedding_model,
            chunker_name="page_image_caption:gemini-3.5-flash",
            replace=True,
        )
        done: set[int] = set()
    else:
        done = await existing_page_numbers(processed_document_id, "page_image_caption")

    # Drop already-captioned pages from the candidate set so the auto-render
    # pre-pass below never renders an image for a page we won't re-caption.
    if done and candidate_pages is not None:
        candidate_pages = {p for p in candidate_pages if p not in done}

    async def _load_image_pages() -> dict[int, str]:
        rows = await (
            get_db_model("ProcessedDocumentPages")
            .filter(processed_document_id=processed_document_id, image_cld_file_id__isnull=False)
            .order_by("page_index")
            .values("page_number", "image_cld_file_id")
        )
        return {int(r["page_number"]): str(r["image_cld_file_id"]) for r in rows}

    image_by_page = await _load_image_pages()

    # One-click U2: page images are NOT captured at ingest, so render any
    # candidate figure page that lacks one (idempotent; S3 eventual-consistency
    # settle-retry). Makes "Build figure captions" work on a fresh doc with no
    # separate render step. No-op when images already exist (e.g. the excerpt).
    # Rendering is a HOST capability (host document storage + file pipeline),
    # injected via matrx_rag.configure(page_image_renderer=...). Unconfigured
    # standalone installs skip the render and caption only the pages that
    # already carry an image — degraded, never a crash.
    render_page_image = get_page_image_renderer()
    if auto_render and candidate_pages and doc["source_kind"] == "cld_file" and render_page_image:
        missing = sorted(p for p in candidate_pages if p not in image_by_page)
        if missing:
            await on_progress(
                StageEvent(
                    stage="page_image_caption",
                    phase="progress",
                    message=f"Rendering {len(missing)} figure page image(s)…",
                    current=0,
                    total=len(missing),
                    extra={"granularity": "page_image_caption", "step": "render"},
                )
            )
            # Render concurrently under a small semaphore (rendering 300+ pages
            # one at a time is itself slow). Each render keeps its own 3-attempt
            # S3 settle-retry and per-page failure isolation; `render_done` is a
            # shared int incremented after each task's await so `current`
            # reflects the count actually completed (asyncio single-thread).
            render_sem = asyncio.Semaphore(max(1, min(4, max_concurrent)))
            render_total = len(missing)
            render_done = 0

            async def _render_one(pn: int) -> None:
                nonlocal render_done
                async with render_sem:
                    for _attempt in range(3):
                        try:
                            if await render_page_image(
                                processed_document_id=processed_document_id,
                                page_index=pn - 1,
                                dpi=150,
                                user_id=doc["created_by"],
                            ):
                                break
                        except Exception as exc:  # noqa: BLE001
                            log.warning("[image-caption] render page %s failed: %s", pn, exc)
                        await asyncio.sleep(3)
                    render_done += 1
                    await on_progress(
                        StageEvent(
                            stage="page_image_caption",
                            phase="progress",
                            message=f"Rendered figure image {render_done}/{render_total}",
                            current=render_done,
                            total=render_total,
                            extra={
                                "granularity": "page_image_caption",
                                "step": "render",
                                "page_number": pn,
                            },
                        )
                    )

            await asyncio.gather(*(_render_one(pn) for pn in missing))
            image_by_page = await _load_image_pages()

    if not image_by_page:
        log.info("[image-caption] doc=%s: no rendered page images", processed_document_id)
        await on_progress(
            StageEvent(
                stage="page_image_caption",
                phase="done",
                message="No rendered page images to caption",
                current=0,
                total=0,
                extra={"granularity": "page_image_caption", "captioned": 0, "chunks_written": 0},
            )
        )
        return ImageCaptionResult(processed_document_id, 0, 0, 0)

    # Caption candidate ∩ rendered, else all rendered pages — then drop pages
    # already captioned on a prior run (resume: no re-spend). When candidate_pages
    # is a set it was already stripped of `done` above (so auto-render skipped
    # them); subtract here too for the all-rendered (candidate_pages is None) path.
    if candidate_pages is not None:
        target = {p for p in candidate_pages if p in image_by_page}
    else:
        target = {p for p in image_by_page if p not in done}
    skipped = len(done)

    from matrx_files.cloud_sync.media_ref import MediaRef

    from matrx_rag._ext import get_cloud_file_manager
    from matrx_rag._ext import get_default_vision_model
    from matrx_rag.image_pipeline import analyze_image_unified

    # Nothing left to caption (e.g. every figure page already captioned on a
    # prior run). Never raise on nothing-to-do — emit a graceful done, return.
    if not target:
        log.info(
            "[image-caption] doc=%s: nothing to caption (%d already done)",
            processed_document_id,
            skipped,
        )
        await on_progress(
            StageEvent(
                stage="page_image_caption",
                phase="done",
                message=(
                    f"All figure page(s) already captioned ({skipped} done)"
                    if skipped
                    else "No figure pages to caption"
                ),
                current=0,
                total=0,
                extra={
                    "granularity": "page_image_caption",
                    "figure_pages": 0,
                    "captioned": 0,
                    "skipped": skipped,
                    "chunks_written": 0,
                },
            )
        )
        return ImageCaptionResult(processed_document_id, 0, 0, 0)

    fm = get_cloud_file_manager()
    chosen_model = vision_model or get_default_vision_model()
    ordered_pages = sorted(target)
    total_pages = len(ordered_pages)
    await on_progress(
        StageEvent(
            stage="page_image_caption",
            phase="started",
            message=f"Captioning {total_pages} figure page(s)"
            + (f" ({skipped} already done)" if skipped else ""),
            current=0,
            total=total_pages,
            extra={
                "granularity": "page_image_caption",
                "figure_pages": total_pages,
                "skipped": skipped,
            },
        )
    )

    # INCREMENTAL + RESUMABLE (mirrors derive_section_summaries). Caption pages
    # CONCURRENTLY in BATCHES, flushing each batch with an APPEND write so paid
    # vision work is durable the moment each batch commits — a mid-run death
    # keeps every completed batch instead of losing them all to one final write.
    #
    # asyncio is single-threaded, so shared accumulators need no lock: each task
    # mutates them only on its own coroutine turn after its awaits. `progressed`
    # is the cumulative completed counter across ALL batches (so `current` runs
    # 1..total over the whole document); `chunk_index` is a running monotonic
    # counter across batches. Per-batch results land in `batch_specs_by_page`
    # keyed by page and are assembled in stable page order AFTER that batch's
    # gather (so chunk_index is deterministic, not race-dependent).
    # Compatibility shape only: one permit per target means this never throttles
    # a provider call. UnifiedAIClient owns provider admission centrally.
    caption_sem = asyncio.Semaphore(max(1, total_pages))
    progressed = 0
    # On a RESUME the running chunk_index must continue from max existing + 1,
    # never restart at 0 — with the kg_038 unique set identity (derivative,
    # chunk_index, kind) a restarted counter collides with the previous run's
    # rows and the idempotent INSERT silently skips NEW paid captions. (This
    # exact restart produced the 2026-06-25 index-0/1 collisions the kg_038
    # migration repaired.)
    chunk_index = 0
    if not reset:
        chunk_index = (
            await existing_max_chunk_index(processed_document_id, "page_image_caption")
        ) + 1
    captioned = 0
    total_written = 0

    async def _caption_one(pn: int, batch_specs_by_page: dict[int, dict]) -> None:
        nonlocal progressed
        async with caption_sem:
            image_id = image_by_page[pn]
            # One page's transient failure (S3 resolve, vision call) must NOT
            # abort the batch and discard every already-paid caption — the batch
            # write happens only after this batch's gather. Skip the page, keep
            # the rest. (BUG-1 fix; preserved under concurrency.)
            enr: dict | None = None
            try:
                from matrx_utils.ctx import system_file_access

                # Internal caption job resolving a server-constructed ref.
                with system_file_access("rag-image-caption"):
                    resolved = await fm.resolve_media_async(
                        MediaRef(file_id=image_id), needs_bytes=True
                    )
                b64 = getattr(resolved, "base64_data", None) if resolved else None
                if not b64:
                    log.warning("[image-caption] page %s image %s: no bytes", pn, image_id)
                else:
                    enr = await analyze_image_unified(
                        bytes_b64=b64,
                        mime_type="image/png",
                        model=chosen_model,
                        file_id=str(image_id),
                    )
            except Exception as exc:  # noqa: BLE001
                # Loud AND durable: a page image left uncaptioned is unsearchable.
                log.error("[image-caption] page %s caption FAILED: %s", pn, exc)
                from matrx_rag.image_pipeline import _record_vision_failure

                await _record_vision_failure(
                    exc, context={"page": pn, "image_id": str(image_id)}
                )
                enr = None

            meaningful = bool(
                enr and (enr.get("caption") or enr.get("description") or enr.get("ocr_text"))
            )
            caption_preview = ""
            if meaningful and enr is not None:
                text = _caption_to_text(enr, pn)
                batch_specs_by_page[pn] = {"text": text, "image_id": image_id, "enr": enr}
                caption_preview = (
                    enr.get("caption")
                    or enr.get("description")
                    or enr.get("alt_text")
                    or text
                    or ""
                )[:160]

            # Increment AFTER the awaits so `current` reflects completed count;
            # this per-item event is BOTH the live-activity stream and the
            # cooperative cancel checkpoint (the run is canceled at this await).
            progressed += 1
            await on_progress(
                StageEvent(
                    stage="page_image_caption",
                    phase="progress",
                    message=f"Captioned page {pn} ({progressed} / {total_pages})",
                    current=progressed,
                    total=total_pages,
                    extra={
                        "granularity": "page_image_caption",
                        "page_number": pn,
                        "caption_preview": caption_preview,
                        "image_cld_file_id": image_id,
                        "current": progressed,
                        "total": total_pages,
                    },
                )
            )

    # Create EVERY caption task before awaiting any flush. Persistence remains in
    # stable page-order batches, but provider work is never serialized by those
    # durability batches.
    all_specs_by_page: dict[int, dict] = {}
    caption_tasks = {
        pn: asyncio.create_task(_caption_one(pn, all_specs_by_page))
        for pn in ordered_pages
    }
    owner_task = asyncio.current_task()
    if owner_task is not None:

        def _cancel_caption_tasks_if_owner_fails(done: asyncio.Task) -> None:
            if done.cancelled() or done.exception() is not None:
                for caption_task in caption_tasks.values():
                    if not caption_task.done():
                        caption_task.cancel()

        owner_task.add_done_callback(_cancel_caption_tasks_if_owner_fails)

    for batch_start in range(0, total_pages, _FLUSH_EVERY):
        batch_pages = ordered_pages[batch_start : batch_start + _FLUSH_EVERY]
        await asyncio.gather(*(caption_tasks[pn] for pn in batch_pages))
        batch_specs_by_page = {
            pn: all_specs_by_page[pn]
            for pn in batch_pages
            if pn in all_specs_by_page
        }

        # Assemble this batch's specs in stable page order; chunk_index is a
        # running counter so indexes stay monotonic across batches.
        specs: list[ChunkSpec] = []
        for pn in (p for p in batch_pages if p in batch_specs_by_page):
            rec = batch_specs_by_page[pn]
            enr = rec["enr"]
            specs.append(
                ChunkSpec(
                    content_text=rec["text"],
                    chunk_index=chunk_index,
                    page_numbers=[pn],
                    primary_page_number=pn,
                    chunk_kind="page_image_caption",
                    metadata={
                        "role": "page_image_caption",
                        "page_number": pn,
                        "image_cld_file_id": rec["image_id"],
                        "caption": enr.get("caption"),
                        "alt_text": enr.get("alt_text"),
                        "keywords": enr.get("keywords"),
                        "has_ocr": bool(enr.get("ocr_text")),
                    },
                )
            )
            chunk_index += 1

        if not specs:
            continue  # whole batch failed/empty — nothing durable to write

        result: DeriveResult = await derive_chunk_set(
            parent_processed_id=processed_document_id,
            derivation_kind="page_image_caption",
            chunks=specs,
            identity={"source": "page_image_caption"},
            name=f"{doc['name']} (figure captions)",
            rag_boost=rag_boost,
            embedding_model=embedding_model,
            chunker_name="page_image_caption:gemini-3.5-flash",
            metadata={"figure_pages": total_pages},
            replace=False,
        )
        total_written += result.chunks_written
        captioned += len(specs)

    await on_progress(
        StageEvent(
            stage="page_image_caption",
            phase="done",
            message=(
                f"Captioned {captioned} of {total_pages} figure page(s)"
                + (f" · {skipped} already done" if skipped else "")
            ),
            current=total_pages,
            total=total_pages,
            extra={
                "granularity": "page_image_caption",
                "figure_pages": total_pages,
                "captioned": captioned,
                "skipped": skipped,
                "chunks_written": total_written,
            },
        )
    )

    return ImageCaptionResult(
        processed_document_id=processed_document_id,
        figure_pages=total_pages,
        captioned=captioned,
        chunks_written=total_written,
    )


__all__ = ["derive_page_image_captions", "ImageCaptionResult"]
