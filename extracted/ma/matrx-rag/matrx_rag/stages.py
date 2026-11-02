"""Per-stage runners for the RAG pipeline.

Each stage stands alone. Each stage:

  - Reads its inputs from the DB (so it can run regardless of what
    the previous stage did, as long as the prior outputs are persisted).
  - Reports progress via a typed callback at meaningful moments
    (per-page, per-chunk-batch, with heartbeats during silent work).
  - Writes its outputs to the DB before returning.
  - Is idempotent: re-running a stage replaces its prior outputs.

The stages map 1:1 to the user-facing model:

    [Cloud File] --extract--> [Raw Text]
                              processed_document_pages.raw_text

    [Raw Text]   --clean----> [Clean Text]
                              processed_document_pages.cleaned_text + section_*

    [Clean Text] --chunk----> [Chunks]
                              rag.kg_chunks rows (without embeddings)

    [Chunks]     --embed----> [Vectors]
                              rag.embeddings_oai_3_small_1536 / voyage_*

A separate ``run_all`` orchestrator chains all four for users who want
one-click full-pipeline behavior.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import tempfile
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from matrx_orm import transaction

# Phase 2b — DocumentWriter injection seam.
from matrx_rag._ext import (
    clean_single_flight,
    ensure_clean_held,
    follow_clean,
    get_db_model,
    get_document_writer,
)
from matrx_rag.chunking import CHUNKER_VERSION, Chunk
from matrx_rag.db import PACKAGE_DB_NAME
from matrx_rag.embeddings import (
    default_text_model,
    embed,
    orm_model_name_for_table,
    spec_for,
)
from matrx_rag.ingestion import (
    _embed_text_for,
    _format_vector,
    _merge_metadata,
)
from matrx_rag.llm import (
    CleanedPage,
    clean_incomplete_error,
    clean_pdf_pages,
    page_is_cleaned,
    page_text_for_downstream,
    page_text_is_raw,
)
from matrx_rag.pdf_pipeline import (
    _ExtractedPage,
    chunk_pdf_pages,
    extract_pages_full,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Progress reporting protocol
# ---------------------------------------------------------------------------


@dataclass
class StageEvent:
    """One progress event emitted during a stage run."""

    stage: str  # 'extract' | 'clean' | 'chunk' | 'embed'
    phase: str  # 'started' | 'progress' | 'page' | 'heartbeat' | 'done' | 'error'
    message: str
    current: int = 0  # work units done
    total: int = 0  # total work units (0 = unknown)
    extra: dict[str, Any] | None = None


ProgressCb = Callable[[StageEvent], Awaitable[None]]

# Wire budget for one streamed page of cleaned text (a CAPS constant, never an
# env toggle). A scanned or printed page runs well under this; a pathological
# page is truncated with ``truncated: true`` rather than blowing up the stream,
# and the durable row always holds the whole thing.
PAGE_CLEAN_STREAM_CHARS = 12_000


async def _noop(_evt: StageEvent) -> None:
    return None


# ---------------------------------------------------------------------------
# Heartbeat helper — fires every N seconds during silent stretches.
# ---------------------------------------------------------------------------


def _spawn_heartbeat(
    on_progress: ProgressCb,
    *,
    stage: str,
    interval: float = 3.0,
    label: str = "working",
) -> asyncio.Task[None]:
    """Background heartbeat. Cancel on a finally block.

    Heartbeats give the FE a "still alive" pulse during stages that
    don't naturally produce frequent progress events (e.g., a single
    long embed() call that batches internally).
    """
    started = time.monotonic()

    async def _beat() -> None:
        try:
            while True:
                await asyncio.sleep(interval)
                elapsed = int(time.monotonic() - started)
                await on_progress(
                    StageEvent(
                        stage=stage,
                        phase="heartbeat",
                        message=f"{label} ({elapsed}s elapsed)",
                    )
                )
        except asyncio.CancelledError:
            return

    return asyncio.create_task(_beat())


async def _await_cancel(task: asyncio.Task[None]) -> None:
    task.cancel()
    try:
        await asyncio.wait_for(task, timeout=1.0)
    except (asyncio.CancelledError, TimeoutError):
        pass


# ---------------------------------------------------------------------------
# DB load helpers
# ---------------------------------------------------------------------------
#
# The page-level loaders (and _load_doc / _fetch_cld_file_to_disk below) read
# docproc.processed_document_pages / docproc.processed_documents / files.files
# through the shared matrx_orm model_registry (get_db_model(...)) — the SAME
# global registry the host (aidream) registers its docproc.*/files.* models
# into at startup, so this resolves whether matrx-rag is hosted or standalone
# (matrx-rag CLAUDE.md rule 4).


async def _load_doc(processed_document_id: str) -> dict | None:
    rows = (
        await get_db_model("ProcessedDocuments")
        .filter(id=processed_document_id)
        .values(
            "id",
            "created_by",
            "organization_id",
            "name",
            "mime_type",
            "total_pages",
            "source_kind",
            "source_id",
            "storage_uri",
            "derivation_kind",
        )
    )
    if not rows:
        return None
    row = rows[0]
    # ::text casts in the old SQL — str() the id/created_by/organization_id
    # UUID columns so callers keep getting plain strings (org_id may be None).
    row["id"] = str(row["id"])
    row["created_by"] = str(row["created_by"])
    row["organization_id"] = (
        str(row["organization_id"]) if row["organization_id"] is not None else None
    )
    return row


async def _load_portion_locators(processed_document_id: str) -> list[dict[str, Any]]:
    """Each page row's locator (with its speaker), in page order."""
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values("locator", "speaker")
    )
    out: list[dict[str, Any]] = []
    for r in rows:
        loc = dict(r.get("locator") or {})
        if r.get("speaker") and not loc.get("speaker"):
            loc["speaker"] = r["speaker"]
        out.append(loc)
    return out


async def _load_portion_kinds(processed_document_id: str) -> list[str]:
    """Each page row's portion kind, in page order ('page' for every PDF page)."""
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values("portion_kind")
    )
    return [str(r.get("portion_kind") or "page") for r in rows]


async def _load_pages(processed_document_id: str) -> list[_ExtractedPage]:
    """Reconstruct the chunker's narrow page view from persisted DB rows."""
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values("page_index", "raw_text", "used_ocr")
    )
    return [
        _ExtractedPage(
            page_index=int(r["page_index"]),
            text=r["raw_text"] or "",
            used_ocr=bool(r["used_ocr"]),
            char_count=len(r["raw_text"] or ""),
        )
        for r in rows
    ]


async def _load_cleaned_pages(processed_document_id: str) -> list[CleanedPage]:
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values(
            "page_index",
            "cleaned_text",
            "raw_text",
            "section_kind",
            "section_subtype",
            "section_title",
            "is_continuation",
        )
    )
    return [
        CleanedPage(
            text=page_text_for_downstream(r),
            section_kind=r["section_kind"] or "other",
            section_subtype=r["section_subtype"] or "",
            section_title=r["section_title"],
            is_continuation=bool(r["is_continuation"]),
        )
        for r in rows
    ]


async def _any_page_text_is_raw(processed_document_id: str) -> bool:
    """True when chunking this document would use RAW text for any page (never
    cleaned, or the cleaner gave up). Those chunks are marked ``text_basis='raw'``."""
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .values("cleaned_text", "section_kind", "portion_kind")
    )
    # Landed Source portions (sections, segments, messages) carry no cleaner pass.
    return any(
        str(r.get("portion_kind") or "page") == "page" and page_text_is_raw(r) for r in rows
    )


async def _load_page_id_lookup(processed_document_id: str) -> dict[int, str]:
    rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .values("page_index", "id")
    )
    return {int(r["page_index"]): str(r["id"]) for r in rows}


async def _fetch_cld_file_to_disk(cld_file_id: str) -> tuple[str, str | None, str | None]:
    """Pull the bytes of a cld_files row to a NamedTemporaryFile and return
    (local_path, file_name, storage_uri)."""
    rows = await get_db_model("Files").filter(id=cld_file_id).values("file_name", "storage_uri")
    if not rows:
        raise FileNotFoundError(f"cld_files row not found: {cld_file_id}")
    row = rows[0]

    storage_uri = row["storage_uri"]
    file_name = row["file_name"]
    if not storage_uri:
        raise RuntimeError(f"cld_files {cld_file_id} has no storage_uri")

    # Resolve through the canonical FileManager.resolve_media_async path
    # so byte cache + auth + audit hooks apply. Use MediaRef(file_id=...)
    # so the resolver looks up the authoritative cld_files row.
    import base64 as _base64

    from matrx_files.cloud_sync.media_ref import MediaRef
    from matrx_utils.ctx import system_file_access

    from matrx_rag._ext import get_cloud_file_manager

    fm = get_cloud_file_manager()
    # Internal RAG stage resolving a server-constructed ref — declare it.
    with system_file_access("rag-stage-pdf"):
        resolved = await fm.resolve_media_async(MediaRef(file_id=cld_file_id), needs_bytes=True)
    b64 = getattr(resolved, "base64_data", None) if resolved else None
    pdf_bytes = _base64.b64decode(b64) if b64 else None
    if not pdf_bytes:
        raise RuntimeError(f"cloud_sync read returned empty for cld_file_id={cld_file_id}")

    suffix = Path(file_name or "doc").suffix or ".bin"
    tmp = tempfile.NamedTemporaryFile(prefix="rag_stage_", suffix=suffix, delete=False)
    try:
        tmp.write(pdf_bytes)
    finally:
        tmp.close()
    return tmp.name, file_name, storage_uri


# ---------------------------------------------------------------------------
# Stage 1 — Extract
# ---------------------------------------------------------------------------


@dataclass
class ExtractResult:
    processed_document_id: str
    pages_count: int
    raw_chars: int
    ocr_pages: int
    skipped: bool = False


async def run_extract(
    *,
    cld_file_id: str,
    owner_id: str,
    organization_id: str | None,
    on_progress: ProgressCb = _noop,
    force_ocr: bool = False,
    force: bool = True,
    local_path: str | None = None,
    file_name: str | None = None,
    storage_uri: str | None = None,
) -> ExtractResult:
    """Stage 1 — extract per-page raw text from the cloud file.

    By default the bytes are pulled from the cld_files row (S3, via the
    canonical FileManager cache). A caller that already holds the bytes on
    disk — e.g. an upload handler running OCR "while still cached", before
    the file ever leaves memory — may pass ``local_path`` (plus the known
    ``file_name`` / ``storage_uri``) to skip the re-fetch entirely. When the
    caller supplies ``local_path`` it OWNS that file: this function will not
    delete it. When it is fetched here, the temp copy is removed before return.
    """
    await on_progress(
        StageEvent(
            stage="extract",
            phase="started",
            message=f"Fetching {cld_file_id[:8]}…",
        )
    )

    owns_temp = local_path is None
    if owns_temp:
        local_path, file_name, storage_uri = await _fetch_cld_file_to_disk(cld_file_id)
    try:
        await on_progress(
            StageEvent(
                stage="extract",
                phase="progress",
                message=f"Extracting pages from {file_name or cld_file_id[:8]}",
            )
        )
        full_pages = await extract_pages_full(
            local_path,
            force_ocr=force_ocr,
            include_blocks=True,
            include_words=True,
        )
    finally:
        if owns_temp:
            try:
                os.unlink(local_path)
            except OSError:
                pass

    if not full_pages:
        await on_progress(
            StageEvent(
                stage="extract",
                phase="error",
                message="No pages found in PDF",
            )
        )
        raise RuntimeError("no_pages_in_pdf")

    pages = [_ExtractedPage.from_pdf_page_text(p) for p in full_pages]
    raw_total = sum(p.char_count for p in pages)
    ocr_pages = sum(1 for p in pages if p.used_ocr)

    await on_progress(
        StageEvent(
            stage="extract",
            phase="progress",
            message=f"Extracted {len(pages)} pages — persisting",
            current=len(pages),
            total=len(pages),
            extra={"raw_chars": raw_total, "ocr_pages": ocr_pages},
        )
    )

    from matrx_files.specific_handlers.pdf import (
        PdfPipelineOptions,
        PdfResult,
    )

    raw_concat = "\n\n".join(p.text for p in pages if p.text.strip())
    pdf_result = PdfResult(raw_text=raw_concat, pages=full_pages)
    processed_document_id = await get_document_writer().persist_processed_document(
        owner_id=owner_id,
        organization_id=organization_id,
        name=file_name or Path(local_path).name,
        pdf_result=pdf_result,
        options=PdfPipelineOptions(
            force_ocr=force_ocr,
            include_block_metadata=True,
            include_word_metadata=True,
        ),
        source_kind="cld_file",
        source_id=cld_file_id,
        storage_uri=storage_uri,
        extra_metadata={"via": "rag.stages.extract"},
        method="pymupdf",
    )

    # Emit a real content sample so the FE dialog can show "look, here's
    # what we got" instead of just a counter. The user has been clear:
    # do not hide the data.
    first_page_preview = ""
    if pages:
        first_page_preview = (pages[0].text or "")[:1500]

    await on_progress(
        StageEvent(
            stage="extract",
            phase="done",
            message=f"Extracted + persisted {len(pages)} pages",
            current=len(pages),
            total=len(pages),
            extra={
                "processed_document_id": str(processed_document_id),
                "raw_chars": raw_total,
                "ocr_pages": ocr_pages,
                "preview": {
                    "kind": "page_text",
                    "label": f"First page raw text (~{len(first_page_preview)} chars)",
                    "page_index": 0,
                    "page_number": 1,
                    "text": first_page_preview,
                    "more": pages[0].char_count > len(first_page_preview) if pages else False,
                },
            },
        )
    )
    return ExtractResult(
        processed_document_id=str(processed_document_id),
        pages_count=len(pages),
        raw_chars=raw_total,
        ocr_pages=ocr_pages,
    )


# ---------------------------------------------------------------------------
# Stage 2 — Clean
# ---------------------------------------------------------------------------


@dataclass
class CleanResult:
    processed_document_id: str
    pages_cleaned: int
    cleaned_chars: int
    section_histogram: dict[str, int]


async def run_clean(
    *,
    processed_document_id: str,
    owner_id: str,
    on_progress: ProgressCb = _noop,
    concurrency: int = 8,
    force: bool = False,
) -> CleanResult:
    """Stage 2 — LLM cleanup + section classification per page.

    SINGLE-FLIGHT: runs inside the host's ``clean_single_flight`` seam, so two
    cleans of one document can never run (or write a page) at once — the
    seam raises for the loser. ``force`` re-cleans every page IN PLACE (the
    same page rows are updated; no second document or page set is created)."""
    async with clean_single_flight(processed_document_id):
        return await _run_clean_held(
            processed_document_id=processed_document_id,
            owner_id=owner_id,
            on_progress=on_progress,
            concurrency=concurrency,
            force=force,
        )


async def _run_clean_held(
    *,
    processed_document_id: str,
    owner_id: str,
    on_progress: ProgressCb,
    concurrency: int,
    force: bool,
) -> CleanResult:
    await on_progress(
        StageEvent(
            stage="clean",
            phase="started",
            message="Loading pages from DB",
        )
    )

    pages = await _load_pages(processed_document_id)
    if not pages:
        raise RuntimeError("no_pages_persisted_for_doc")

    total = len(pages)
    await on_progress(
        StageEvent(
            stage="clean",
            phase="progress",
            message=f"Cleaning {total} pages (concurrency={concurrency})",
            current=0,
            total=total,
        )
    )

    emit_every = max(1, total // 50)
    last_emit = {"n": 0}

    async def _on_page(done: int, total_p: int) -> None:
        if done == total_p or (done - last_emit["n"]) >= emit_every:
            last_emit["n"] = done
            await on_progress(
                StageEvent(
                    stage="clean",
                    phase="progress",
                    message=f"Cleaned page {done} / {total_p}",
                    current=done,
                    total=total_p,
                )
            )

    # RESUMABILITY: skip pages that already have cleaned_text. This is
    # the difference between burning the LLM bill twice on a retry and
    # only paying for the work that hadn't completed.
    # ``page_is_cleaned``, never ``cleaned_text != ""``: a page the cleaner
    # classified illegible/blank is cleaned to "" and must not be re-paid.
    already_cleaned_rows = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .values("page_index", "cleaned_text", "section_kind")
    )
    already_cleaned: set[int] = (
        set()
        if force
        else {
            int(r["page_index"])
            for r in already_cleaned_rows
            if page_is_cleaned(r["cleaned_text"], r["section_kind"])
        }
    )
    if already_cleaned:
        await on_progress(
            StageEvent(
                stage="clean",
                phase="progress",
                message=(
                    f"Resuming — {len(already_cleaned)} of {total} pages "
                    f"already cleaned, skipping them"
                ),
                current=len(already_cleaned),
                total=total,
            )
        )

    # DURABILITY: persist each cleaned page the moment it's done so
    # work survives cancellation / OOM / network blip.
    async def _persist_one(idx: int, cleaned: CleanedPage) -> None:
        # FENCE: a hold lost mid-clean never writes a page (raises, fails the run).
        await ensure_clean_held(processed_document_id)
        try:
            await get_document_writer().update_page_cleanup(
                doc_id=processed_document_id,
                page_index=idx,
                cleaned_text=cleaned.text or "",
                section_kind=cleaned.section_kind,
                section_subtype=cleaned.section_subtype,
                section_title=cleaned.section_title,
                is_continuation=cleaned.is_continuation,
            )
        except Exception as exc:  # noqa: BLE001
            # NEVER silently swallow a failed persist of the (expensive, LLM-
            # produced) cleaned text — that is exactly how per-page clean work
            # gets lost while the doc-level clean_content (built from memory)
            # masks it. Surface it AND re-raise so the clean stage fails loudly
            # and the run is retried; resumability then skips the pages that DID
            # persist, so no work is redone and none is lost.
            await on_progress(
                StageEvent(
                    stage="clean",
                    phase="progress",
                    message=f"clean persist FAILED page {idx}: {exc}",
                    current=0,
                    total=total,
                )
            )
            raise
        # THE FLOATING LAW: a counter is not output. The clean stage is the
        # expensive multi-LLM pass over the user's own document, so every page
        # ships the model's ACTUAL rewrite the instant it is durable — the same
        # ``page_clean`` preview shape the stage's terminal event already uses,
        # so one renderer covers both. Emitted after persist, never before: a
        # preview the row does not back is a lie the next reload exposes.
        await on_progress(
            StageEvent(
                stage="clean",
                phase="page",
                message=f"Cleaned page {idx + 1}",
                current=idx + 1,
                total=total,
                extra={
                    "preview": {
                        "kind": "page_clean",
                        "label": cleaned.section_title or f"Page {idx + 1}",
                        "page_number": idx + 1,
                        "cleaned_text": (cleaned.text or "")[:PAGE_CLEAN_STREAM_CHARS],
                        "truncated": len(cleaned.text or "") > PAGE_CLEAN_STREAM_CHARS,
                        "section_kind": cleaned.section_kind,
                        "section_subtype": cleaned.section_subtype or None,
                        "section_title": cleaned.section_title,
                    }
                },
            )
        )

    cleaned_pages = await clean_pdf_pages(
        [p.text for p in pages],
        concurrency=concurrency,
        on_progress=_on_page,
        persist_one=_persist_one,
        skip_indexes=already_cleaned,
        error_context={"processed_document_id": processed_document_id, "owner_id": owner_id},
        before_page=lambda _idx: ensure_clean_held(processed_document_id),
    )

    # Hydrate the in-memory list for any skipped pages so the histogram +
    # cleaned_total reflect the persisted state, not stale placeholders.
    if already_cleaned:
        hydrate_rows = await (
            get_db_model("ProcessedDocumentPages")
            .filter(
                processed_document_id=processed_document_id,
                page_index__in=sorted(already_cleaned),
            )
            .values(
                "page_index",
                "cleaned_text",
                "raw_text",
                "section_kind",
                "section_subtype",
                "section_title",
                "is_continuation",
            )
        )
        _by_idx = {int(r["page_index"]): r for r in hydrate_rows}
        for i in range(len(cleaned_pages)):
            if i in _by_idx:
                _r = _by_idx[i]
                cleaned_pages[i] = CleanedPage(
                    text=page_text_for_downstream(_r),
                    section_kind=_r["section_kind"] or "other",
                    section_subtype=_r["section_subtype"] or "",
                    section_title=_r["section_title"],
                    is_continuation=bool(_r["is_continuation"]),
                )

    # NOTHING CLAIMS "CLEANED" UNLESS EVERY PAGE CLEANED. A refused / failed
    # page carries its RAW text in memory; joining that into ``clean_content``
    # and stamping ``clean_content_completed_at`` made a document whose cleaner
    # was refused (the person's AI usage limit) read "Cleaned" with ~raw text
    # (2026-10-07). The stage fails by name instead; the pages stay uncleaned so
    # a later run cleans exactly them, and chunking falls back to raw text so
    # the document is still searchable.
    incomplete = clean_incomplete_error(cleaned_pages, already_cleaned)
    if incomplete is not None:
        # The caller announces the failure (the orchestrator's stage ``error``
        # event / the manual clean stream's terminal error) from this exception.
        raise incomplete

    joined = "\n\n".join(c.text or "" for c in cleaned_pages)
    await ensure_clean_held(processed_document_id)
    await get_document_writer().update_clean_content(processed_document_id, joined, owner_id)
    histogram: dict[str, int] = {}
    cleaned_total = 0
    for cleaned in cleaned_pages:
        histogram[cleaned.section_kind] = histogram.get(cleaned.section_kind, 0) + 1
        cleaned_total += len(cleaned.text or "")

    # Sample of cleaned content so the FE can render a before/after preview.
    first_clean_preview = ""
    first_raw_preview = ""
    if cleaned_pages:
        first_clean_preview = (cleaned_pages[0].text or "")[:1500]
    if pages:
        first_raw_preview = (pages[0].text or "")[:1500]

    await on_progress(
        StageEvent(
            stage="clean",
            phase="done",
            message=f"Cleaned {total} pages, {cleaned_total:,} chars",
            current=total,
            total=total,
            extra={
                "section_histogram": histogram,
                "preview": {
                    "kind": "page_clean",
                    "label": "First page — raw vs cleaned",
                    "page_number": 1,
                    "raw_text": first_raw_preview,
                    "cleaned_text": first_clean_preview,
                    "section_kind": cleaned_pages[0].section_kind if cleaned_pages else None,
                    "section_subtype": (cleaned_pages[0].section_subtype or None)
                    if cleaned_pages
                    else None,
                    "section_title": cleaned_pages[0].section_title if cleaned_pages else None,
                },
            },
        )
    )
    return CleanResult(
        processed_document_id=processed_document_id,
        pages_cleaned=total,
        cleaned_chars=cleaned_total,
        section_histogram=histogram,
    )


# ---------------------------------------------------------------------------
# Stage 3 — Chunk
# ---------------------------------------------------------------------------


@dataclass
class ChunkResult:
    processed_document_id: str
    chunks_written: int
    parents: int
    children: int


async def run_chunk(
    *,
    processed_document_id: str,
    owner_id: str,
    on_progress: ProgressCb = _noop,
) -> ChunkResult:
    """Stage 3 — page-aware hierarchical chunking. Reads from DB, writes
    rag.kg_chunks rows WITHOUT embeddings (stage 4 fills those in).

    This deletes any prior chunks for the doc's source first (idempotent
    re-run) — same semantics as upsert_chunks, but without the embedding
    INSERT.
    """
    await on_progress(
        StageEvent(
            stage="chunk",
            phase="started",
            message="Loading pages + cleaned text from DB",
        )
    )

    doc = await _load_doc(processed_document_id)
    if not doc:
        raise RuntimeError("processed_document_not_found")

    # NULL-org write guard (2026-06-03 leak class): EVERY kg_chunks row
    # MUST carry a non-NULL org, and it is the PARENT DOCUMENT'S org — read off
    # the record, never resolved here. A parent with none REFUSES below, by
    # name; a chunk is never filed in a tenant chosen for the owner.
    from matrx_rag.ingestion import resolve_effective_org

    effective_org = await resolve_effective_org(doc["organization_id"], doc["created_by"])
    if effective_org is None:
        raise ValueError(
            f"run_chunk: processed_document {processed_document_id} has neither "
            "organization_id nor created_by; cannot resolve org for kg_chunks."
        )

    pages = await _load_pages(processed_document_id)
    cleaned_pages = await _load_cleaned_pages(processed_document_id)
    if not pages:
        raise RuntimeError("no_pages_persisted_for_doc")

    # If clean wasn't run, fall back to raw text so chunking still works.
    # "" honestly means "unclassified", never the fake bucket "other".
    raw_basis = await _any_page_text_is_raw(processed_document_id)
    if not cleaned_pages or all(not c.text for c in cleaned_pages):
        raw_basis = True
        cleaned_pages = [
            CleanedPage(text=p.text, section_kind="", section_title=None) for p in pages
        ]

    await on_progress(
        StageEvent(
            stage="chunk",
            phase="progress",
            message=f"Chunking {len(pages)} pages",
            current=0,
            total=len(pages),
        )
    )

    portion_kinds = await _load_portion_kinds(processed_document_id)
    if any(k != "page" for k in portion_kinds):
        # A landed Source's portions (sections, segments, messages) are chunked one by one.
        from matrx_rag.pdf_pipeline import chunk_portions

        locators = (
            await _load_portion_locators(processed_document_id)
            if "segment" in portion_kinds
            else None
        )
        chunks = chunk_portions(pages, cleaned_pages, portion_kinds, locators)
    else:
        chunks = chunk_pdf_pages(pages, cleaned_pages)
    if not chunks:
        raise RuntimeError("no_chunks_produced")

    parents = sum(1 for c in chunks if c.parent_chunk_id is None)
    children = len(chunks) - parents

    await on_progress(
        StageEvent(
            stage="chunk",
            phase="progress",
            message=f"Produced {len(chunks)} chunks ({parents} parents, {children} children) — persisting",
            current=len(pages),
            total=len(pages),
        )
    )

    # Persist: replicates upsert_chunks's chunk-INSERT half (without the
    # embeddings INSERT). Matches the schema added in migration 0008.
    raw_concat = "\n\n".join(p.text for p in pages if p.text.strip())
    source_hash = hashlib.sha256(raw_concat.encode("utf-8")).hexdigest()
    page_id_lookup = await _load_page_id_lookup(processed_document_id)

    def _chunk_page_columns(c: Chunk) -> tuple[str | None, list[int] | None, str | None]:
        meta = c.metadata or {}
        first_page = meta.get("first_page")
        last_page = meta.get("last_page", first_page)
        if first_page is None:
            return None, None, None
        try:
            fp = int(first_page)
            lp = int(last_page) if last_page is not None else fp
        except (TypeError, ValueError):
            return None, None, None
        page_numbers = list(range(fp + 1, lp + 2))
        # A transcript window anchors to its FIRST segment, so a hit plays from where it starts.
        primary = (
            page_id_lookup.get(fp) if (fp == lp or meta.get("portion_kind") == "segment") else None
        )
        spans = [{"page_index": idx, "page_number": idx + 1} for idx in range(fp, lp + 1)]
        return primary, page_numbers, spans

    page_cols = [_chunk_page_columns(c) for c in chunks]
    source_metadata: dict[str, Any] = {"via": "rag.stages.chunk"}
    # Built from raw text because the clean was refused / failed: a TOP-LEVEL flag
    # (not under ``source``) that recovery.preflight reads, so a later successful
    # clean re-chunks and the stale raw chunks do not outlive the cleaned text.
    basis_meta: dict[str, Any] = {"text_basis": "raw"} if raw_basis else {}
    chunk_source_kind = str(doc.get("source_kind") or "cld_file")

    KgChunks = get_db_model("KgChunks")
    chunk_rows = [
        {
            "id": c.chunk_id,
            "organization_id": effective_org,
            "created_by": doc["created_by"],
            # The document's OWN kind: a landed transcript's or web page's chunks are keyed on
            # the Source they came from (SOURCE-CONVERGENCE §3.4), not filed as a file's.
            "source_kind": chunk_source_kind,
            "source_id": doc["source_id"],
            "field_id": None,
            "parent_chunk_id": c.parent_chunk_id,
            "chunk_index": c.chunk_index,
            "chunk_kind": c.chunk_kind,
            "content_text": c.content_text,
            "token_count": c.token_count,
            "language": c.language,
            "mime_type": doc["mime_type"] or "application/pdf",
            "source_hash": source_hash,
            "chunker_name": "v1",
            "chunker_version": CHUNKER_VERSION,
            "metadata": {**_merge_metadata(source_metadata, c.metadata or {}), **basis_meta},
            "processed_document_id": processed_document_id,
            "primary_page_id": page_cols[i][0],
            "page_numbers": page_cols[i][1],
            "page_spans": page_cols[i][2],
            "token_estimate": c.token_count,
        }
        for i, c in enumerate(chunks)
    ]

    # Transactional mirror of upsert_chunks's chunk-INSERT half (without
    # embeddings): DELETE the doc's prior chunks + bulk INSERT the new set,
    # sharing ONE connection via matrx_orm.transaction() (ContextVar-bound) so
    # the delete+insert atomicity guarantee that makes stage re-runs safe is
    # preserved exactly like the old hand-rolled pool.acquire()+conn.transaction()
    # block. `field_id IS NOT DISTINCT FROM NULL` (always NULL here) is
    # `field_id__isnull=True`.
    async with transaction(PACKAGE_DB_NAME):
        # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
        await KgChunks.delete_where(
            source_kind=chunk_source_kind, source_id=doc["source_id"], field_id__isnull=True
        )
        await KgChunks.bulk_create(chunk_rows)

    # Sample of the first 3 chunks so the FE can show "here's what your
    # content was split into" instead of just a chunk count.
    chunk_samples = []
    for c in chunks[:3]:
        chunk_samples.append(
            {
                "chunk_index": c.chunk_index,
                "chunk_kind": c.chunk_kind,
                "token_count": c.token_count,
                "page_numbers": list(
                    range(
                        int((c.metadata or {}).get("first_page", 0)) + 1,
                        int((c.metadata or {}).get("last_page", 0)) + 2,
                    )
                )
                if c.metadata and "first_page" in c.metadata
                else None,
                "content_text": (c.content_text or "")[:1200],
            }
        )

    await on_progress(
        StageEvent(
            stage="chunk",
            phase="done",
            message=f"Wrote {len(chunks)} chunks to rag.kg_chunks",
            current=len(chunks),
            total=len(chunks),
            extra={
                "parents": parents,
                "children": children,
                "preview": {
                    "kind": "chunks_sample",
                    "label": f"First 3 of {len(chunks)} chunks",
                    "samples": chunk_samples,
                },
            },
        )
    )
    return ChunkResult(
        processed_document_id=processed_document_id,
        chunks_written=len(chunks),
        parents=parents,
        children=children,
    )


# ---------------------------------------------------------------------------
# Stage 4 — Embed
# ---------------------------------------------------------------------------


def _embedding_model_for_table(table: str) -> Any:
    """Resolve the matrx-orm Model that owns an embedding table.

    The mapping lives on ``EmbeddingSpec.orm_model`` (one source of truth for
    the whole package — see ``embeddings.orm_model_name_for_table``); a new
    embedding table is declared there and in matrx_rag/db/models_rag.py."""
    model_name = orm_model_name_for_table(table)
    if model_name is None:
        raise RuntimeError(
            f"no ORM model mapped for embedding table {table!r} — set "
            f"orm_model on its EmbeddingSpec in matrx_rag/embeddings.py"
        )
    return get_db_model(model_name)


async def embedded_chunk_count(
    processed_document_id: str, *, embedding_model: str | None = None
) -> int:
    """How many of a document's live chunks hold a vector for ``embedding_model``
    (default: the prose default) — MEASURED from the embedding table, the same
    two-query read ``run_embed`` uses to find what is already embedded."""
    embedding_model = embedding_model or default_text_model()
    KgChunks = get_db_model("KgChunks")
    emb_model = _embedding_model_for_table(spec_for(embedding_model).table)
    ids = [
        r["id"]
        for r in await KgChunks.filter(
            processed_document_id=processed_document_id, valid_to__isnull=True
        ).values("id")
    ]
    if not ids:
        return 0
    existing = await emb_model.filter(chunk_id__in=ids).values("chunk_id")
    return len({str(r["chunk_id"]) for r in existing})


@dataclass
class EmbedResult:
    processed_document_id: str
    chunks_total: int
    chunks_embedded: int
    chunks_already_embedded: int
    model: str


async def run_embed(
    *,
    processed_document_id: str,
    on_progress: ProgressCb = _noop,
    embedding_model: str | None = None,
    batch_size: int = 64,
) -> EmbedResult:
    """Stage 4 — embed every chunk that doesn't already have a vector
    in the embeddings table for ``embedding_model``. Idempotent: re-running
    after partial completion only embeds what's missing.

    ``embedding_model=None`` resolves to the configured prose default
    (``default_text_model()`` — voyage-4-large since 2026-07). A hardcoded
    legacy default here writes to the dead oai table (invisible to search)."""
    embedding_model = embedding_model or default_text_model()
    await on_progress(
        StageEvent(
            stage="embed",
            phase="started",
            message=f"Loading chunks needing embedding for {embedding_model}",
        )
    )

    info = spec_for(embedding_model)
    table = info.table

    doc = await _load_doc(processed_document_id)
    if not doc:
        raise RuntimeError("processed_document_not_found")

    # NULL-org write guard (2026-06-03 leak class): embedding rows mirror the
    # chunk's org, read off the parent document's record. A parent with none
    # REFUSES below, by name — never a personal-org stand-in.
    from matrx_rag.ingestion import resolve_effective_org

    effective_org = await resolve_effective_org(doc["organization_id"], doc["created_by"])
    if effective_org is None:
        raise ValueError(
            f"run_embed: processed_document {processed_document_id} has neither "
            "organization_id nor created_by; cannot resolve org for embeddings."
        )

    KgChunks = get_db_model("KgChunks")
    emb_model = _embedding_model_for_table(table)

    chunks_total = int(
        await KgChunks.count(
            processed_document_id=processed_document_id,
            valid_to__isnull=True,
        )
        or 0
    )
    # Two-query port of the old anti-join (chunks LEFT JOIN <embedding table>
    # WHERE e.chunk_id IS NULL): fetch the doc's live chunks, fetch which of
    # them already have a vector, and set-difference in Python. Bounded
    # per-document work, so two round-trips are fine. The pool's uuid→str
    # codec keeps ``id`` a str (the old query's ``::text`` cast) and jsonb
    # metadata arrives in the same shape the raw query produced.
    candidate_rows = await (
        KgChunks.filter(
            processed_document_id=processed_document_id,
            valid_to__isnull=True,
        )
        .order_by("chunk_index")
        .values("id", "content_text", "metadata")
    )
    embedded_ids: set[str] = set()
    if candidate_rows:
        existing = await emb_model.filter(chunk_id__in=[r["id"] for r in candidate_rows]).values(
            "chunk_id"
        )
        embedded_ids = {str(r["chunk_id"]) for r in existing}
    rows = [r for r in candidate_rows if str(r["id"]) not in embedded_ids]

    needed = len(rows)
    already = chunks_total - needed
    if needed == 0:
        await on_progress(
            StageEvent(
                stage="embed",
                phase="done",
                message=f"All {chunks_total} chunks already embedded ({embedding_model})",
                current=chunks_total,
                total=chunks_total,
            )
        )
        return EmbedResult(
            processed_document_id=processed_document_id,
            chunks_total=chunks_total,
            chunks_embedded=0,
            chunks_already_embedded=already,
            model=embedding_model,
        )

    await on_progress(
        StageEvent(
            stage="embed",
            phase="progress",
            message=f"Embedding {needed} chunks via {embedding_model} ({already} already done)",
            current=0,
            total=needed,
        )
    )

    embedded = 0
    for batch_start in range(0, needed, batch_size):
        batch = rows[batch_start : batch_start + batch_size]
        adapters = [
            _RowAsChunk(r["id"], r["content_text"], _coerce_metadata(r["metadata"])) for r in batch
        ]
        texts = [_embed_text_for(a) for a in adapters]

        hb = _spawn_heartbeat(
            on_progress,
            stage="embed",
            label=f"Embedding batch {batch_start + 1}–{batch_start + len(batch)} / {needed}",
        )
        try:
            vectors = await embed(
                embedding_model,
                texts,
                input_type="document",
                # Provenance on the shared embedding cache: the organization of
                # the document being embedded, read off its record.
                organization_id=effective_org,
            )
        finally:
            await _await_cancel(hb)

        # ON CONFLICT (chunk_id) DO UPDATE SET embedding = EXCLUDED.embedding
        # — exactly the old statement; embedded_at stays on its DB default,
        # as the raw INSERT left it. One multi-row INSERT per batch (same
        # per-batch atomicity as the old transaction-wrapped executemany).
        await emb_model.bulk_upsert(
            [
                {
                    "chunk_id": r["id"],
                    "organization_id": effective_org,
                    "owner_id": doc["created_by"],
                    "embedding": _format_vector(v),
                }
                for r, v in zip(batch, vectors, strict=True)
            ],
            conflict_fields=["chunk_id"],
            update_fields=["embedding"],
        )
        embedded += len(batch)

        await on_progress(
            StageEvent(
                stage="embed",
                phase="progress",
                message=f"Embedded {embedded} / {needed} chunks",
                current=embedded,
                total=needed,
            )
        )

    await on_progress(
        StageEvent(
            stage="embed",
            phase="done",
            message=f"Embedded {embedded} new vectors via {embedding_model}",
            current=needed,
            total=needed,
            extra={"already_embedded": already, "newly_embedded": embedded},
        )
    )
    return EmbedResult(
        processed_document_id=processed_document_id,
        chunks_total=chunks_total,
        chunks_embedded=embedded,
        chunks_already_embedded=already,
        model=embedding_model,
    )


@dataclass
class _RowAsChunk:
    """Adapter so ``_embed_text_for`` from ingestion (which expects
    Chunk-like objects) works on raw DB rows. Only ``content_text`` and
    ``metadata`` are accessed."""

    chunk_id: str
    content_text: str
    metadata: dict[str, Any]


def _coerce_metadata(value: Any) -> dict[str, Any]:
    """Normalize a chunk's ``metadata`` to a dict.

    ``KgChunks.filter(...).values("metadata")`` returns the jsonb column as a
    raw JSON STRING (the ORM ``.values()`` path does not apply asyncpg's jsonb
    decoder the way a raw pool query does). ``_embed_text_for`` calls
    ``metadata.get(...)``, so a str leaks an AttributeError. Parse it here.
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


# ---------------------------------------------------------------------------
# Orchestrator — run all 4 stages in sequence
# ---------------------------------------------------------------------------


async def run_all(
    *,
    cld_file_id: str | None = None,
    processed_document_id: str | None = None,
    owner_id: str,
    organization_id: str | None,
    on_progress: ProgressCb = _noop,
    embedding_model: str | None = None,
    force_ocr: bool = False,
    cleanup_concurrency: int = 8,
) -> dict[str, Any]:
    """Run extract → clean → chunk → embed end-to-end.

    ``embedding_model=None`` flows through to ``run_embed``, which resolves it
    to the configured prose default (voyage-4-large)."""
    if not (cld_file_id or processed_document_id):
        raise ValueError("must provide cld_file_id or processed_document_id")

    summary: dict[str, Any] = {}

    if cld_file_id and not processed_document_id:
        ex = await run_extract(
            cld_file_id=cld_file_id,
            owner_id=owner_id,
            organization_id=organization_id,
            on_progress=on_progress,
            force_ocr=force_ocr,
        )
        processed_document_id = ex.processed_document_id
        summary["extract"] = {
            "pages_count": ex.pages_count,
            "raw_chars": ex.raw_chars,
            "ocr_pages": ex.ocr_pages,
        }

    assert processed_document_id is not None

    # A clean already running on this document (a manual / auto clean, a recovery
    # re-drive) is FOLLOWED through the host seam — never a second concurrent clean
    # and never a false failure; the host's result carries the holder's page count.
    cl = await follow_clean(
        processed_document_id,
        lambda: run_clean(
            processed_document_id=processed_document_id,
            owner_id=owner_id,
            on_progress=on_progress,
            concurrency=cleanup_concurrency,
        ),
    )
    summary["clean"] = {
        "pages_cleaned": cl.pages_cleaned,
        "cleaned_chars": getattr(cl, "cleaned_chars", 0),
        "section_histogram": getattr(cl, "section_histogram", {}),
    }
    awaiting_batch = int(getattr(cl, "awaiting_batch", 0) or 0)
    if awaiting_batch:
        # The holder handed the pages to the batch lane; cleaning them live now would
        # pay twice and chunking raw text would index the uncleaned pages. The batch
        # barrier resumes this document when they land.
        summary["clean"]["awaiting_batch"] = awaiting_batch
        summary["processed_document_id"] = processed_document_id
        summary["status"] = "awaiting_batch"
        return summary

    ch = await run_chunk(
        processed_document_id=processed_document_id,
        owner_id=owner_id,
        on_progress=on_progress,
    )
    summary["chunk"] = {
        "chunks_written": ch.chunks_written,
        "parents": ch.parents,
        "children": ch.children,
    }

    em = await run_embed(
        processed_document_id=processed_document_id,
        on_progress=on_progress,
        embedding_model=embedding_model,
    )
    summary["embed"] = {
        "chunks_total": em.chunks_total,
        "chunks_embedded": em.chunks_embedded,
        "chunks_already_embedded": em.chunks_already_embedded,
        "model": em.model,
    }
    summary["processed_document_id"] = processed_document_id
    return summary


__all__ = [
    "embedded_chunk_count",
    "StageEvent",
    "ProgressCb",
    "ExtractResult",
    "CleanResult",
    "ChunkResult",
    "EmbedResult",
    "run_extract",
    "run_clean",
    "run_chunk",
    "run_embed",
    "run_all",
]
