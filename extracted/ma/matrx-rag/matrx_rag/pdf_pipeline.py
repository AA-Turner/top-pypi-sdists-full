"""PDF → indexed chunks pipeline.

The user requirement: every PDF runs through

    fetch → per-page extract (native + OCR fallback)
          → per-page LLM cleanup (small windows, parallel, capped concurrency)
          → hierarchical chunking
          → embed
          → upsert

with full provenance: each chunk knows which page(s) of which source PDF
it came from, so generation can cite back to the page accurately.

Reuses ``matrx_files.specific_handlers.pdf.PDFHandler``
for the heavy lifting (download, native extract, OCR, table extract). We
add the missing pieces: per-page splitting, LLM cleanup, and the bridge
into ``rag.kg_chunks``.

Public entry:

    await ingest_pdf(
        cld_file_id=...,           # the cld_files.id we're indexing
        organization_id=...,
        owner_id=...,
        local_path=...,            # already-downloaded PDF on disk
        force_ocr=False,
        cleanup=True,              # turn off when ingesting trusted text PDFs
        embedding_model=None,      # None → default_text_model() (voyage-4-large)
    ) -> IngestionResult

The function is also exposed as a synchronous-ish wrapper through the
``cld_file`` resolver in ``sources.py``: when a cloud-files row's mime
type is ``application/pdf`` and a local cache or storage_uri can be
materialized, the resolver invokes ``ingest_pdf`` directly.

Why per-page (not full-document) cleanup
-----------------------------------------
The user's spec is explicit: small amounts at a time so the cleanup
model isn't overwhelmed. A typical legal/medical PDF page is 1k-5k
tokens; ``gpt-4o-mini`` handles 128k easily but the *quality* drops as
the context grows because the model has to track more state across the
prompt. Per-page is the sweet spot: tiny per-call latency and the model
can focus on layout artifacts and OCR cleanup instead of trying to
"understand" 200 pages.

Concurrency cap is configurable; default 8 in-flight pages keeps the
OpenAI rate limit well below the per-tenant ceiling on tier-1 keys.
"""

from __future__ import annotations

import contextlib

import asyncio
import hashlib
import logging
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from matrx_utils.splitting import pack
from matrx_files.specific_handlers.pdf import (
    PDFHandler,
    PdfPageText,
    PdfPipelineOptions,
)

# Phase 2b — DocumentWriter injection seam. Hosts that own the
# processed_documents schema (aidream) inject a writer; matrx-local
# uses the no-op default for local-RAG mode where it doesn't write
# to aidream's tables.
from matrx_rag._ext import (
    clean_single_flight,
    ensure_clean_held,
    follow_clean,
    get_db_model,
    get_document_writer,
)


class _DocSourceKinds:
    """Source-kind constants used by the writer's persist call.

    The writer protocol takes plain strings; we wrap the registry
    lookup so call sites can write ``_SOURCE_KINDS.cld_file`` as if it
    were an enum. The default values match aidream's SourceKind enum
    exactly; hosts can override via configure(source_kind_aliases=...).
    """

    @property
    def cld_file(self) -> str:
        from matrx_rag._ext import get_ext

        return get_ext("source_kind_cld_file", default="cld_file")


_SOURCE_KINDS = _DocSourceKinds()
from matrx_rag.chunking import (
    CHILD_OVERLAP,
    CHILD_SIZE,
    CHUNKER_VERSION,
    PARENT_OVERLAP,
    PARENT_SIZE,
    Chunk,
    _encoding,
    _tok_len,
)
from matrx_rag.embeddings import default_text_model, embed, spec_for
from matrx_rag.ingestion import (
    IngestionResult,
    _embed_text_for,
    attach_context_prefixes,
    contextual_retrieval_enabled,
    upsert_chunks,
)
from matrx_rag.llm import (
    CleanedPage,
    PageCleanIncompleteError,
    clean_incomplete_error,
    clean_pdf_pages,
    page_is_cleaned,
    page_text_for_downstream,
)
from matrx_rag.progress import from_emitter
from matrx_rag.text_hygiene import strip_control_chars
from matrx_rag.sources import ResolvedSource

logger = logging.getLogger(__name__)

# Use the same hierarchical structure as the prose chunker but track which
# pages contributed to each chunk so we can cite back.
DEFAULT_CONCURRENCY = 8


# Shared PDFHandler instance — System A's canonical extractor. We use it
# instead of a parallel pypdfium2 path so extraction logic + bounding
# boxes + the page model (PdfPageText) all match what /pdf/extract-text*
# already produces.
#
# Lazy-init: PDFHandler.__init__ reads matrx_utils settings.BASE_DIR.
# Constructing at module-import time fails in test / CLI contexts where
# the host hasn't called configure_settings yet. We delay the instance
# until the first ingestion call, which always runs after app startup.
_pdf_handler_singleton: PDFHandler | None = None


def _get_pdf_handler() -> PDFHandler:
    global _pdf_handler_singleton
    if _pdf_handler_singleton is None:
        _pdf_handler_singleton = PDFHandler(app_name="rag_pdf_pipeline")
    return _pdf_handler_singleton


@dataclass
class _ExtractedPage:
    """Compatibility shim for the chunker.

    Used to be a standalone shape produced by a duplicate pypdfium2
    extractor. Now we always extract via PDFHandler and produce PdfPageText
    instances; this dataclass adapts the fields the chunker reads
    (page_index, text, used_ocr, char_count). Any new code should use
    PdfPageText directly.
    """

    page_index: int  # 0-based
    text: str
    used_ocr: bool
    char_count: int

    @classmethod
    def from_pdf_page_text(cls, ppt: PdfPageText) -> _ExtractedPage:
        return cls(
            page_index=int(ppt.page_index),
            text=ppt.text or "",
            used_ocr=(ppt.extraction_method or "").lower() == "ocr",
            char_count=int(ppt.char_count or 0),
        )


# ---------------------------------------------------------------------------
# Per-page extraction (PDFHandler concats; we keep them split)
# ---------------------------------------------------------------------------


def extract_tables(local_path: str) -> list[dict[str, Any]]:
    """Per-page table extraction via PyMuPDF (fitz). Returns a list of
    table records::

        [{
            "page_index": int,           # 0-based
            "bbox": [x0, y0, x1, y1],
            "rows": int,
            "cols": int,
            "header": list[str] | None,
            "markdown": str,             # rendered as a markdown table
            "raw":      list[list[str]], # cells
        }, ...]

    Empty list when the document has no detectable tables. PyMuPDF's
    detector is good enough for forms and clean tables; messy
    medical-imaging tables sometimes need OCR-plus-camelot territory
    which we'll add later if needed.
    """
    import pymupdf

    out: list[dict[str, Any]] = []
    doc = pymupdf.open(local_path)
    try:
        for i, page in enumerate(doc):
            try:
                tabs = page.find_tables()
            except Exception:
                continue
            for tab in tabs.tables:
                try:
                    rows = tab.extract()
                except Exception:
                    continue
                if not rows:
                    continue
                # Normalize cells → strings, strip whitespace.
                cells = [[("" if v is None else str(v)).strip() for v in row] for row in rows]
                if not any(any(c for c in r) for r in cells):
                    continue
                header = cells[0] if len(cells) > 1 else None
                # Markdown rendering — robust to ragged rows.
                md_lines: list[str] = []
                if header:
                    md_lines.append("| " + " | ".join(header) + " |")
                    md_lines.append("|" + "|".join(["---"] * len(header)) + "|")
                    body = cells[1:]
                else:
                    body = cells
                for row in body:
                    md_lines.append("| " + " | ".join(row) + " |")
                bbox_attr = getattr(tab, "bbox", None)
                bbox = list(bbox_attr) if bbox_attr is not None else None
                out.append(
                    {
                        "page_index": i,
                        "bbox": bbox,
                        "rows": len(cells),
                        "cols": max((len(r) for r in cells), default=0),
                        "header": header,
                        "markdown": "\n".join(md_lines),
                        "raw": cells,
                    }
                )
    finally:
        doc.close()
    return out


# Keep aligned with image_caption_derivation._DRAWINGS_FIGURE_THRESHOLD.
_FIGURE_DRAWINGS_THRESHOLD = 40


def count_tables_rows_and_figure_pages(local_path: str) -> tuple[int, int, int]:
    """Single-pass PyMuPDF scan for derivation cost estimates.

    Opens the PDF once and returns ``(n_tables, n_rows, n_figure_pages)``.
    CPU-bound — callers must run this off the event loop.
    """
    import pymupdf

    n_tables = 0
    n_rows = 0
    n_figure_pages = 0
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
            if n_images > 0 or n_draw > _FIGURE_DRAWINGS_THRESHOLD:
                n_figure_pages += 1

            try:
                tabs = page.find_tables()
            except Exception:
                continue
            for tab in tabs.tables:
                try:
                    rows = tab.extract()
                except Exception:
                    continue
                if not rows:
                    continue
                cells = [[("" if v is None else str(v)).strip() for v in row] for row in rows]
                if not any(any(c for c in r) for r in cells):
                    continue
                n_tables += 1
                header = cells[0] if len(cells) > 1 else None
                n_rows += len(cells[1:] if header else cells)
    finally:
        doc.close()
    return n_tables, n_rows, n_figure_pages


def _without_control_chars(pages: list[PdfPageText]) -> list[PdfPageText]:
    """Page text without non-printing control characters (the one extraction-side strip)."""
    out: list[PdfPageText] = []
    for p in pages:
        text = strip_control_chars(p.text)
        out.append(p if text == p.text else p.model_copy(update={"text": text, "char_count": len(text)}))
    return out


async def extract_pages_full(
    local_path: str,
    *,
    force_ocr: bool = False,
    ocr_threshold: int = 100,
    include_blocks: bool = True,
    include_words: bool = True,
    strip_repeated_regions: bool = False,
    repeated_regions_min_confidence: float = 0.7,
) -> list[PdfPageText]:
    """Per-page extraction via System A's PDFHandler.

    Returns a list of full PdfPageText (with width/height/rotation and
    optional blocks/words bounding boxes). The rich shape is the input to
    persist_processed_document; the chunker uses _ExtractedPage.from_pdf_page_text
    to adapt down to its narrower view.

    Native text is preferred; pages with fewer than ``ocr_threshold``
    chars trigger OCR fallback inside PDFHandler.

    When *strip_repeated_regions* is True, the Phase 3 detector runs over
    the document and any region whose confidence is at or above
    *repeated_regions_min_confidence* is stripped from the per-page text
    before the chunker sees it. Page-level bbox metadata stays intact so
    downstream persistence retains the original geometry; only the ``.text``
    field is rewritten.
    """
    handler = _get_pdf_handler()

    def _do() -> list[PdfPageText]:
        pages = handler.extract_text_pages(
            local_path,
            force_ocr=force_ocr,
            use_ocr_threshold=ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )
        pages = _without_control_chars(pages)
        if not strip_repeated_regions:
            return pages
        with open(local_path, "rb") as f:
            pdf_bytes = f.read()
        report = handler.detect_repeated_regions(
            pdf_bytes, min_confidence=repeated_regions_min_confidence
        )
        if not report.regions:
            return pages
        cleaned = handler.strip_repeated_regions_text([p.text for p in pages], report.regions)
        return [
            p.model_copy(update={"text": cleaned[i], "char_count": len(cleaned[i])})
            for i, p in enumerate(pages)
        ]

    # PyMuPDF + Tesseract are blocking C calls; offload to a thread.
    return await asyncio.to_thread(_do)


async def extract_pages(
    local_path: str,
    *,
    force_ocr: bool = False,
    ocr_threshold: int = 100,
) -> list[_ExtractedPage]:
    """Compatibility wrapper that returns the narrow _ExtractedPage shape.

    Kept for callers that don't need the full PdfPageText (block / word
    bounding boxes, dimensions). New code should call extract_pages_full
    so the page rows in processed_document_pages can be populated with
    the bounding-box artifacts.
    """
    full = await extract_pages_full(
        local_path,
        force_ocr=force_ocr,
        ocr_threshold=ocr_threshold,
        include_blocks=False,
        include_words=False,
    )
    return [_ExtractedPage.from_pdf_page_text(p) for p in full]


# ---------------------------------------------------------------------------
# Page-aware hierarchical chunking
# ---------------------------------------------------------------------------


def _hard_split_oversized(block: str, max_tokens: int, overlap: int) -> list[str]:
    """Force a single block that ALONE exceeds ``max_tokens`` into slices that
    each fit. Tries line (``\\n``) boundaries first — keeps reference entries
    and table rows intact — then falls back to a raw tiktoken window for any
    single line still too big. GUARANTEES every output slice is ≤ max_tokens.

    Why this exists: ``_split_by_tokens`` groups on ``\\n\\n`` paragraphs. A
    references / bibliography section (entries separated by single ``\\n``) is
    ONE giant paragraph; without this it was emitted whole as a ~3000-token
    "child" chunk that silently overflowed the NER extractor's window and got
    dropped (the silent document-gutting class). No leaf chunk may exceed the
    window, ever.
    """
    out: list[str] = []
    buf: list[str] = []
    buf_tokens = 0

    def flush() -> None:
        nonlocal buf, buf_tokens
        if buf:
            out.append("\n".join(buf).strip())
            buf = []
            buf_tokens = 0

    for line in (ln for ln in block.split("\n") if ln.strip()):
        line_tokens = _tok_len(line)
        if line_tokens > max_tokens:
            # A single line bigger than the whole window — token-window split it.
            flush()
            enc = _encoding()
            toks = enc.encode(line)
            step = max(1, max_tokens - overlap)
            for i in range(0, len(toks), step):
                piece = enc.decode(toks[i : i + max_tokens]).strip()
                if piece:
                    out.append(piece)
            continue
        if buf_tokens + line_tokens > max_tokens and buf:
            flush()
        buf.append(line)
        buf_tokens += line_tokens
    flush()
    return [s for s in out if s]


def _split_by_tokens(text: str, max_tokens: int, overlap: int) -> list[str]:
    """Token-aware splitter that targets ~max_tokens per slice with
    overlap. Used for both parent and child chunking inside a page batch.
    Different from langchain RecursiveCharacterTextSplitter — keeps
    paragraphs intact when possible by preferring \\n\\n boundaries, but
    HARD-SPLITS any single paragraph that alone exceeds max_tokens so an
    unsplittable blob can never produce an oversized leaf chunk.
    """
    if not text or not text.strip():
        return []
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return [text.strip()]
    out: list[str] = []
    buf: list[str] = []
    buf_tokens = 0
    for para in paragraphs:
        para_tokens = _tok_len(para)
        # A single paragraph that alone overflows the window must be hard-split
        # NOW, or it becomes an oversized chunk that silently breaks NER.
        if para_tokens > max_tokens:
            if buf:
                out.append("\n\n".join(buf).strip())
                buf = []
                buf_tokens = 0
            out.extend(_hard_split_oversized(para, max_tokens, overlap))
            continue
        if buf_tokens + para_tokens > max_tokens and buf:
            out.append("\n\n".join(buf).strip())
            # Keep the last paragraph as overlap if small enough.
            tail = buf[-1]
            if _tok_len(tail) <= overlap:
                buf = [tail]
                buf_tokens = _tok_len(tail)
            else:
                buf = []
                buf_tokens = 0
        buf.append(para)
        buf_tokens += para_tokens
    if buf:
        out.append("\n\n".join(buf).strip())
    return out


#: A transcript window: consecutive timed segments merged up to about this many tokens, never
#: across a speaker change. A caption line (median 9 tokens) is not a retrievable unit — 24,624 of
#: 26,021 transcript chunks were under 20 tokens (audit 2026-09-26) — a 250–400 token window is.
SEGMENT_WINDOW_MIN_TOKENS = 250
SEGMENT_WINDOW_MAX_TOKENS = 400


def _segment_windows(
    rows: list[tuple[int, str, dict[str, Any]]],
) -> list[list[tuple[int, str, dict[str, Any]]]]:
    """Group consecutive ``(page_index, text, locator)`` segments into windows: a speaker change
    closes a window once it holds ``SEGMENT_WINDOW_MIN_TOKENS``; ``SEGMENT_WINDOW_MAX_TOKENS``
    always closes it. A single overlong segment is its own window."""
    windows: list[list[tuple[int, str, dict[str, Any]]]] = []
    buf: list[tuple[int, str, dict[str, Any]]] = []
    buf_tokens = 0
    for row in rows:
        # +1: the line break that joins it to the window (and a speaker prefix, when shown).
        tokens = _tok_len(row[1]) + 1 + (2 if (row[2] or {}).get("speaker") else 0)
        speaker = (row[2] or {}).get("speaker")
        prev_speaker = (buf[-1][2] or {}).get("speaker") if buf else None
        if buf and (
            buf_tokens + tokens > SEGMENT_WINDOW_MAX_TOKENS
            or (speaker != prev_speaker and buf_tokens >= SEGMENT_WINDOW_MIN_TOKENS)
        ):
            windows.append(buf)
            buf, buf_tokens = [], 0
        buf.append(row)
        buf_tokens += tokens
    if buf:
        windows.append(buf)
    return windows


def _segment_window_chunks(
    rows: list[tuple[int, str, dict[str, Any]]], start_index: int
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for window in _segment_windows(rows):
        first, last = window[0], window[-1]
        speakers = [str((r[2] or {}).get("speaker")) for r in window if (r[2] or {}).get("speaker")]
        lines = []
        for _, text, loc in window:
            who = (loc or {}).get("speaker")
            lines.append(f"{who}: {text}" if who and len(set(speakers)) > 1 else text)
        text = "\n".join(lines).strip()
        meta: dict[str, Any] = {
            "role": "parent",
            "first_page": first[0],
            "last_page": last[0],
            "portion_kind": "segment",
            "section_kind": "segment",
            "segment_count": len(window),
        }
        t0 = (first[2] or {}).get("t0_ms")
        t1 = (last[2] or {}).get("t1_ms")
        if isinstance(t0, int):
            meta["t0_ms"] = t0
        if isinstance(t1, int):
            meta["t1_ms"] = t1
        if speakers:
            meta["speakers"] = list(dict.fromkeys(speakers))
        chunks.append(
            Chunk(
                chunk_id=str(uuid.uuid4()),
                parent_chunk_id=None,
                chunk_index=start_index + len(chunks),
                chunk_kind="text",
                content_text=text,
                token_count=_tok_len(text),
                language=None,
                metadata=meta,
            )
        )
    return chunks


def chunk_portions(
    pages: list[_ExtractedPage],
    cleaned_pages: list[CleanedPage],
    portion_kinds: list[str],
    portion_locators: list[dict[str, Any]] | None = None,
) -> list[Chunk]:
    """One chunk per PORTION (a section, a timed segment, a message) — never a merge across them.

    A portion is already a reader-sized unit with its own locator (SOURCE-CONVERGENCE §2.2), so it
    is its own parent chunk, and it gets children only when it is longer than a child: a short
    portion is chunked ONCE, never as a parent plus an identical child (the duplicate the Phase 1a
    verifier found on a two-turn transcript). ``first_page``/``last_page`` carry the portion's
    index so every chunk anchors to exactly one portion row.
    """
    chunks: list[Chunk] = []
    chunk_index = 0
    locators = portion_locators or [{} for _ in pages]
    if portion_kinds and all(k == "segment" for k in portion_kinds):
        # A transcript: timed segments are windowed (speaker-aware), each window anchored to its
        # first and last segment (t0_ms of the first, t1_ms of the last) so "Play from" still works.
        rows = [
            (page.page_index, (cleaned.text or page.text or "").strip(), loc or {})
            for page, cleaned, loc in zip(pages, cleaned_pages, locators, strict=True)
            if (cleaned.text or page.text or "").strip()
        ]
        return _segment_window_chunks(rows, 0)
    for page, cleaned, kind in zip(pages, cleaned_pages, portion_kinds, strict=True):
        text = (cleaned.text or page.text or "").strip()
        if not text:
            continue
        idx = page.page_index
        meta = {
            "first_page": idx,
            "last_page": idx,
            "portion_kind": kind,
            "section_kind": cleaned.section_kind or kind,
        }
        parent_id = str(uuid.uuid4())
        chunks.append(
            Chunk(
                chunk_id=parent_id,
                parent_chunk_id=None,
                chunk_index=chunk_index,
                chunk_kind="text",
                content_text=text,
                token_count=_tok_len(text),
                language=None,
                metadata={"role": "parent", **meta},
            )
        )
        chunk_index += 1
        if _tok_len(text) <= CHILD_SIZE:
            continue
        for child_text in _split_by_tokens(text, CHILD_SIZE, CHILD_OVERLAP):
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    parent_chunk_id=parent_id,
                    chunk_index=chunk_index,
                    chunk_kind="text",
                    content_text=child_text,
                    token_count=_tok_len(child_text),
                    language=None,
                    metadata={"role": "child", **meta},
                )
            )
            chunk_index += 1
    return chunks


def chunk_pdf_pages(
    pages: list[_ExtractedPage],
    cleaned_pages: list[CleanedPage],
) -> list[Chunk]:
    """Two-tier chunking with page + section provenance.

    Strategy:
      * Group consecutive cleaned pages into ``parent`` chunks of
        ~PARENT_SIZE tokens. **A section change forces a parent
        boundary** so a "medical_progress_note" parent never bleeds into
        a "legal_subpoena" parent — that would defeat downstream filters.
      * Each parent records the section_kind that dominates its pages,
        plus a list of section_titles that fed into it.
      * Within each parent, split into ~CHILD_SIZE tokens using
        paragraph-aware splitting; children inherit section metadata.
    """
    triples = [
        (p.page_index, c)
        for p, c in zip(pages, cleaned_pages, strict=True)
        if c.text and c.text.strip()
    ]
    if not triples:
        return []

    chunks: list[Chunk] = []
    chunk_index = 0

    parent_buf: list[tuple[int, CleanedPage]] = []
    parent_tokens = 0

    def flush_parent() -> None:
        nonlocal chunk_index, parent_buf, parent_tokens
        if not parent_buf:
            return
        parent_text = "\n\n".join(c.text for _, c in parent_buf).strip()
        first_page = parent_buf[0][0]
        last_page = parent_buf[-1][0]
        # Dominant section + titles list.
        kinds: dict[str, int] = {}
        subtypes: dict[str, int] = {}
        titles: list[str] = []
        for _, c in parent_buf:
            kinds[c.section_kind] = kinds.get(c.section_kind, 0) + 1
            if c.section_subtype:
                subtypes[c.section_subtype] = subtypes.get(c.section_subtype, 0) + 1
            if c.section_title and c.section_title not in titles:
                titles.append(c.section_title)
        # Empty ⇒ no page in the span was classified (honestly unknown), NEVER
        # the fake bucket "other". section_kind is open-vocabulary now.
        section_kind = max(kinds.items(), key=lambda kv: kv[1])[0] if kinds else ""
        # Dominant SPECIFIC document type within the span (only when at
        # least one page named one). Empty string ⇒ no specific identity.
        section_subtype = max(subtypes.items(), key=lambda kv: kv[1])[0] if subtypes else ""

        parent_id = str(uuid.uuid4())
        parent_meta = {
            "role": "parent",
            "first_page": first_page,
            "last_page": last_page,
            "n_pages": last_page - first_page + 1,
            "section_kind": section_kind,
            "section_subtype": section_subtype,
            "section_titles": titles,
            "section_kinds_in_span": list(kinds.keys()),
            "section_subtypes_in_span": list(subtypes.keys()),
        }
        chunks.append(
            Chunk(
                chunk_id=parent_id,
                parent_chunk_id=None,
                chunk_index=chunk_index,
                chunk_kind="text",
                content_text=parent_text,
                token_count=_tok_len(parent_text),
                language=None,
                metadata=parent_meta,
            )
        )
        chunk_index += 1
        for child_text in _split_by_tokens(parent_text, CHILD_SIZE, CHILD_OVERLAP):
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    parent_chunk_id=parent_id,
                    chunk_index=chunk_index,
                    chunk_kind="text",
                    content_text=child_text,
                    token_count=_tok_len(child_text),
                    language=None,
                    metadata={
                        "role": "child",
                        "first_page": first_page,
                        "last_page": last_page,
                        "section_kind": section_kind,
                        "section_subtype": section_subtype,
                    },
                )
            )
            chunk_index += 1
        parent_buf = []
        parent_tokens = 0

    # Parents are the shared splitter's packing (matrx_utils.splitting.pack — the
    # same packer data.batch runs in a workflow): fill to PARENT_SIZE tokens, and a
    # section change forces a parent boundary unless the page is a continuation.
    for part in pack(
        triples,
        budget=PARENT_SIZE,
        size_of=lambda t: _tok_len(t[1].text),
        must_cut=lambda prev, t: (
            t[1].section_kind != prev[1].section_kind and not t[1].is_continuation
        ),
    ):
        parent_buf = list(part.items)
        flush_parent()
    return chunks


async def _chunk_pdf_pages_async(
    pages: list[_ExtractedPage],
    cleaned_pages: list[CleanedPage],
) -> list[Chunk]:
    return await asyncio.to_thread(chunk_pdf_pages, pages, cleaned_pages)


def _append_pdf_table_chunks(
    chunks: list[Chunk],
    tables: list[dict[str, Any]],
) -> None:
    """Build table chunks synchronously; callers isolate this CPU work."""
    page_to_parent: dict[int, str] = {}
    for chunk in chunks:
        if chunk.parent_chunk_id is not None:
            continue
        metadata = chunk.metadata or {}
        first_page = int(metadata.get("first_page", -1))
        last_page = int(metadata.get("last_page", -1))
        for page_index in range(first_page, last_page + 1):
            page_to_parent.setdefault(page_index, chunk.chunk_id)

    next_index = max((chunk.chunk_index for chunk in chunks), default=-1) + 1
    for table in tables:
        markdown = table.get("markdown", "").strip()
        if not markdown:
            continue
        parent_id = page_to_parent.get(int(table.get("page_index", 0)))
        section_kind = ""
        section_subtype = ""
        if parent_id:
            for chunk in chunks:
                if chunk.chunk_id == parent_id and chunk.metadata:
                    section_kind = chunk.metadata.get("section_kind", "")
                    section_subtype = chunk.metadata.get("section_subtype", "")
                    break
        chunks.append(
            Chunk(
                chunk_id=str(uuid.uuid4()),
                parent_chunk_id=parent_id,
                chunk_index=next_index,
                chunk_kind="table",
                content_text=markdown,
                token_count=_tok_len(markdown),
                language=None,
                metadata={
                    "role": "child",
                    "first_page": table.get("page_index"),
                    "last_page": table.get("page_index"),
                    "section_kind": section_kind,
                    "section_subtype": section_subtype,
                    "table_rows": table.get("rows"),
                    "table_cols": table.get("cols"),
                    "table_header": table.get("header"),
                },
            )
        )
        next_index += 1


async def _add_pdf_table_chunks(
    chunks: list[Chunk],
    tables: list[dict[str, Any]],
) -> None:
    await asyncio.to_thread(_append_pdf_table_chunks, chunks, tables)


async def _local_path_exists(local_path: str) -> bool:
    return await asyncio.to_thread(Path(local_path).exists)


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


async def ingest_pdf(
    *,
    cld_file_id: str,
    organization_id: str | None,
    owner_id: str,
    local_path: str,
    file_name: str | None = None,
    storage_uri: str | None = None,
    force_ocr: bool = False,
    cleanup: bool = True,
    cleanup_concurrency: int = DEFAULT_CONCURRENCY,
    embedding_model: str | None = None,
    extra_metadata: dict[str, Any] | None = None,
    force: bool = False,
    emitter: Any | None = None,
    allow_global_org: bool = False,
) -> IngestionResult:
    """Run the full PDF pipeline for one cloud-files row, into rag.kg_chunks.

    When ``force=False`` and existing chunks for this resource already match
    the raw-text hash, the pipeline short-circuits before LLM cleanup —
    the expensive part — and returns ``skipped_unchanged=True``.

    ``emitter`` is an optional matrx-connect ``Emitter`` — when provided,
    every stage (fetch / extract / cleanup / chunk / embed / upsert /
    complete) sends a ``rag.ingest.progress`` event the FE can render
    as a real-time progress bar.
    """
    # None → the configured prose default (voyage-4-large since 2026-07). NEVER
    # hardcode the legacy model here: both callers (ingestion._maybe_dispatch_pdf,
    # library.ingest_library_pdf) rely on this default, so a stale literal here
    # silently writes every cld_file PDF's vectors to the DEAD oai table, making
    # them invisible to the voyage-4 search lane (2026-07-07 orphan-chunk class).
    embedding_model = embedding_model or default_text_model()

    progress = from_emitter(emitter, source_kind="cld_file", source_id=cld_file_id)
    await progress.stage("fetch", message=f"Reading {file_name or local_path}")

    if not await _local_path_exists(local_path):
        await progress.stage("error", error="local_path_missing")
        return IngestionResult(
            source_kind="cld_file",
            source_id=cld_file_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embedding_model,
            error="local_path_missing",
        )

    # 1. Per-page extract via System A's PDFHandler. We get the FULL
    # PdfPageText (with width/height/rotation + optional blocks/words) so
    # processed_document_pages can be populated with bounding boxes for
    # the 4-pane viewer.
    await progress.stage("extract", message="Extracting pages (native + OCR fallback)")
    full_pages: list[PdfPageText] = await extract_pages_full(
        local_path,
        force_ocr=force_ocr,
        include_blocks=True,
        include_words=True,
    )
    if not full_pages:
        await progress.stage("error", error="no_pages_in_pdf")
        return IngestionResult(
            source_kind="cld_file",
            source_id=cld_file_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embedding_model,
            error="no_pages_in_pdf",
        )

    # Adapt to the chunker's narrower view.
    pages: list[_ExtractedPage] = [_ExtractedPage.from_pdf_page_text(p) for p in full_pages]

    raw_total = sum(p.char_count for p in pages)
    raw_concat = "\n\n".join(p.text for p in pages if p.text.strip())
    source_hash = hashlib.sha256(raw_concat.encode("utf-8")).hexdigest()
    # Emit a real content sample so the FE dialog can render "look,
    # here's what we got" instead of just a counter.
    _first_page_text = (pages[0].text or "")[:1500] if pages else ""
    await progress.stage(
        "extract",
        message=f"Extracted {len(pages)} pages ({raw_total} chars, "
        f"{sum(1 for p in pages if p.used_ocr)} via OCR)",
        pages_total=len(pages),
        pages_done=len(pages),
        extra={
            "preview": {
                "kind": "page_text",
                "label": f"First page raw text (~{len(_first_page_text)} chars)",
                "page_index": 0,
                "page_number": 1,
                "text": _first_page_text,
                "more": pages[0].char_count > len(_first_page_text) if pages else False,
            },
        },
    )

    # 1b. Dedup against existing chunks before paying for LLM cleanup.
    if not force:
        _dedup_rows = await (
            get_db_model("KgChunks")
            .filter(source_kind="cld_file", source_id=cld_file_id, field_id__isnull=True)
            .order_by("-created_at")
            .limit(1)
            .values("source_hash")
        )
        existing = _dedup_rows[0]["source_hash"] if _dedup_rows else None
        if existing == source_hash:
            await progress.stage(
                "complete",
                message="Skipped (unchanged content hash)",
            )
            return IngestionResult(
                source_kind="cld_file",
                source_id=cld_file_id,
                field_id=None,
                chunks_written=0,
                embeddings_written=0,
                skipped_unchanged=True,
                embedding_model=embedding_model,
            )

    # 1c. Persist (or upsert) the processed_documents row + page rows.
    # This is the single source of truth for "we've seen this PDF" — the
    # 4-pane viewer reads from these tables, and the kg_chunks rows below
    # FK back to them.
    from matrx_files.specific_handlers.pdf import (
        PdfResult as _PdfResult,
    )

    pdf_result = _PdfResult(raw_text=raw_concat, pages=full_pages)
    _writer = get_document_writer()
    try:
        processed_document_id = await _writer.persist_processed_document(
            owner_id=owner_id,
            organization_id=organization_id,
            name=file_name or Path(local_path).name,
            pdf_result=pdf_result,
            options=PdfPipelineOptions(
                force_ocr=force_ocr,
                include_block_metadata=True,
                include_word_metadata=True,
            ),
            source_kind=_SOURCE_KINDS.cld_file,
            source_id=cld_file_id,
            storage_uri=storage_uri,
            extra_metadata={
                "via": "rag.ingest_pdf",
                "embedding_model": embedding_model,
            },
            method="pymupdf",
        )
        # Build a page_index → processed_document_pages.id lookup so
        # upsert_chunks can populate primary_page_id on single-page chunks.
        _rows = await (
            get_db_model("ProcessedDocumentPages")
            .filter(processed_document_id=processed_document_id)
            .values("page_index", "id")
        )
        page_id_lookup: dict[int, str] = {int(r["page_index"]): str(r["id"]) for r in _rows}
    except Exception as exc:  # noqa: BLE001
        # Persistence failure shouldn't break ingestion — continue with
        # the legacy path (kg_chunks without processed_document_id FK).
        logger.warning(
            "persist_processed_document failed for cld_file=%s: %s",
            cld_file_id,
            exc,
        )
        processed_document_id = None
        page_id_lookup = {}

    # 2. Per-page LLM cleanup + section classification (parallel, capped)
    clean_incomplete: PageCleanIncompleteError | None = None
    if cleanup:
        # RESUMABILITY: look up which pages already have cleaned_text from
        # a previous run. We will NOT re-pay the LLM bill for those.
        # This is the fix for the "618-page run died at 50%, lost all the
        # cleanup work" failure mode that destroyed days of money + time.
        # SINGLE-FLIGHT (host seam): resume read + clean run under ONE claim, so
        # no second clean of this document can run or write a page meanwhile.
        async def _clean_pages_under_claim() -> tuple[set[int], list[CleanedPage]]:
            async with (
                clean_single_flight(processed_document_id)
                if processed_document_id
                else contextlib.nullcontext()
            ):
                already_cleaned_indexes: set[int] = set()
                if processed_document_id:
                    try:
                        _r_rows = await (
                            get_db_model("ProcessedDocumentPages")
                            .filter(processed_document_id=processed_document_id)
                            .values("page_index", "cleaned_text", "section_kind")
                        )
                        already_cleaned_indexes = {
                            int(r["page_index"])
                            for r in _r_rows
                            if page_is_cleaned(r["cleaned_text"], r["section_kind"])
                        }
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("cleanup resume lookup failed: %s", exc)

                if already_cleaned_indexes:
                    await progress.stage(
                        "cleanup",
                        message=(
                            f"Resuming cleanup — {len(already_cleaned_indexes)} of "
                            f"{len(pages)} pages already cleaned, will skip them"
                        ),
                        pages_total=len(pages),
                        pages_done=len(already_cleaned_indexes),
                    )
                else:
                    await progress.stage(
                        "cleanup",
                        message=f"LLM cleanup + section classification over {len(pages)} pages "
                        f"(concurrency={cleanup_concurrency})",
                        pages_total=len(pages),
                        pages_done=0,
                    )

                # Downsample stream emits.
                _emit_every = max(1, len(pages) // 50)  # ~50 events for any size
                _last_emitted = {"n": 0}

                async def _on_cleanup_progress(done: int, total: int) -> None:
                    if done == total or (done - _last_emitted["n"]) >= _emit_every:
                        _last_emitted["n"] = done
                        await progress.stage(
                            "cleanup",
                            message=f"Cleaning page {done} / {total}",
                            pages_total=total,
                            pages_done=done,
                        )

                # DURABILITY: persist each cleaned page the MOMENT it returns.
                # Without this, a 600-page LLM cleanup that dies at page 312
                # throws away 311 already-LLM'd pages — exactly the failure
                # mode that just burned the user's money. With it, every
                # page is safe on disk as soon as it's produced.
                async def _persist_one_page(idx: int, cleaned: CleanedPage) -> None:
                    if not processed_document_id:
                        return
                    # FENCE (outside the swallow below): a lost hold fails the run.
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
                        logger.error("per-page cleanup persist failed page=%d: %s", idx, exc)

                cleaned_pages = await clean_pdf_pages(
                    [p.text for p in pages],
                    concurrency=cleanup_concurrency,
                    on_progress=_on_cleanup_progress,
                    persist_one=_persist_one_page,
                    skip_indexes=already_cleaned_indexes,
                    before_page=lambda _idx: ensure_clean_held(processed_document_id),
                )
                # If we skipped some pages on a resume, the in-memory cleaned_pages
                # slots for those skipped indexes are placeholders. Replace them
                # with the persisted cleaned text so downstream chunking sees the
                # real cleaned content (not the raw text fallback).
                if already_cleaned_indexes and processed_document_id:
                    try:
                        _rows = await (
                            get_db_model("ProcessedDocumentPages")
                            .filter(
                                processed_document_id=processed_document_id,
                                page_index__in=sorted(already_cleaned_indexes),
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
                        _by_idx = {int(r["page_index"]): r for r in _rows}
                        for i, _ in enumerate(cleaned_pages):
                            if i in _by_idx:
                                _r = _by_idx[i]
                                cleaned_pages[i] = CleanedPage(
                                    text=page_text_for_downstream(_r),
                                    section_kind=_r["section_kind"] or "other",
                                    section_subtype=_r.get("section_subtype") or "",
                                    section_title=_r.get("section_title"),
                                    is_continuation=bool(_r.get("is_continuation")),
                                )
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("cleanup resume hydrate failed: %s", exc)
                # 2b. Each page's cleaned_text was ALREADY persisted incrementally
                # by clean_pdf_pages via persist_one. Write the joined clean_content
                # blob (legacy /pdf/documents readers) HERE, still inside the clean
                # claim and fenced like every other write of a held clean. Only when
                # every page cleaned; the writer stamps metadata.clean_mode="pages".
                if (
                    processed_document_id
                    and cleaned_pages
                    and clean_incomplete_error(cleaned_pages, already_cleaned_indexes) is None
                ):
                    # FENCE (outside the swallow below): a lost hold fails the run.
                    await ensure_clean_held(processed_document_id)
                    try:
                        joined_clean = "\n\n".join(c.text or "" for c in cleaned_pages)
                        await get_document_writer().update_clean_content(
                            processed_document_id, joined_clean, owner_id
                        )
                    except Exception as exc:  # noqa: BLE001
                        # A hold lost DURING the write is a stop, not a warning.
                        await ensure_clean_held(processed_document_id)
                        logger.warning(
                            "update_doc_clean_content failed for processed_document_id=%s: %s",
                            processed_document_id,
                            exc,
                        )
            return already_cleaned_indexes, cleaned_pages

        # A clean already running on this document is FOLLOWED (host seam): wait for
        # it, then run again — the resume read below skips every page it cleaned.
        _cleaned = await (
            follow_clean(processed_document_id, _clean_pages_under_claim, resume=True)
            if processed_document_id
            else _clean_pages_under_claim()
        )
        if not isinstance(_cleaned, tuple):
            # The followed holder handed this document's pages to the batch lane (still
            # in flight): cleaning them live would pay twice, chunking the raw text
            # would index them uncleaned. Say so; the batch barrier resumes the document.
            await progress.stage("error", error="clean_awaiting_batch")
            return IngestionResult(
                source_kind="cld_file",
                source_id=cld_file_id,
                field_id=None,
                chunks_written=0,
                embeddings_written=0,
                skipped_unchanged=False,
                embedding_model=embedding_model,
                error="clean_awaiting_batch",
            )
        already_cleaned_indexes, cleaned_pages = _cleaned
        clean_incomplete = clean_incomplete_error(cleaned_pages, already_cleaned_indexes)
        if clean_incomplete is not None:
            # Chunking below still uses the raw text of these pages (search must
            # work), but the document never claims it was cleaned.
            await progress.stage(
                "cleanup",
                message="Cleanup incomplete",
                pages_total=len(pages),
                pages_done=len(pages) - clean_incomplete.degraded,
                error=str(clean_incomplete),
            )

        # Surface a section histogram so the FE can render "this PDF
        # contains 12 medical reports, 4 subpoenas, 3 billing pages".
        section_hist: dict[str, int] = {}
        for c in cleaned_pages:
            section_hist[c.section_kind] = section_hist.get(c.section_kind, 0) + 1
        # Cleaned-page sample for the FE — show before/after for page 1.
        _first_clean = (cleaned_pages[0].text or "")[:1500] if cleaned_pages else ""
        _first_raw = (pages[0].text or "")[:1500] if pages else ""
        await progress.stage(
            "cleanup",
            message="Cleanup + classification complete",
            pages_total=len(pages),
            pages_done=len(pages),
            extra={
                "section_histogram": section_hist,
                "preview": {
                    "kind": "page_clean",
                    "label": "First page — raw vs cleaned",
                    "page_number": 1,
                    "raw_text": _first_raw,
                    "cleaned_text": _first_clean,
                    "section_kind": cleaned_pages[0].section_kind if cleaned_pages else None,
                    "section_subtype": (cleaned_pages[0].section_subtype or None)
                    if cleaned_pages
                    else None,
                    "section_title": cleaned_pages[0].section_title if cleaned_pages else None,
                },
            },
        )
    else:
        # cleanup disabled ⇒ pages are not classified. "" honestly means
        # "unclassified", never the fake bucket "other".
        cleaned_pages = [CleanedPage(text=p.text, section_kind="") for p in pages]
        section_hist = {"": len(cleaned_pages)}

    cleaned_total = sum(len(c.text) for c in cleaned_pages)

    # 3. Hierarchical chunking with page + section provenance
    await progress.stage("chunk", message="Hierarchical page-aware chunking")
    chunks = await _chunk_pdf_pages_async(pages, cleaned_pages)
    if not chunks:
        await progress.stage("error", error="no_chunks_produced")
        return IngestionResult(
            source_kind="cld_file",
            source_id=cld_file_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embedding_model,
            error="no_chunks_produced",
        )

    # 3a. Per-page table chunks. We attach them with the same parent
    # span as their containing text chunk so generation can pull the
    # surrounding prose alongside.
    try:
        tables = await asyncio.to_thread(extract_tables, local_path)
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.pdf_pipeline.extract_tables: %s", exc)
        tables = []

    if tables:
        await _add_pdf_table_chunks(chunks, tables)

    # First-3-chunks sample so the FE can show what content was split into.
    _chunk_samples: list[dict[str, Any]] = []
    for _c in chunks[:3]:
        _meta = _c.metadata or {}
        _fp = _meta.get("first_page")
        _lp = _meta.get("last_page", _fp)
        _page_numbers: list[int] | None = None
        if _fp is not None:
            try:
                _page_numbers = list(range(int(_fp) + 1, int(_lp or _fp) + 2))
            except (TypeError, ValueError):
                _page_numbers = None
        _chunk_samples.append(
            {
                "chunk_index": _c.chunk_index,
                "chunk_kind": _c.chunk_kind,
                "token_count": _c.token_count,
                "page_numbers": _page_numbers,
                "content_text": (_c.content_text or "")[:1200],
            }
        )
    await progress.stage(
        "chunk",
        message=f"Produced {len(chunks)} chunks ({sum(1 for c in chunks if c.chunk_kind == 'table')} tables)",
        chunks_total=len(chunks),
        chunks_done=len(chunks),
        extra={
            "section_histogram": section_hist,
            "preview": {
                "kind": "chunks_sample",
                "label": f"First 3 of {len(chunks)} chunks",
                "samples": _chunk_samples,
            },
        },
    )

    # 3b. Optional contextual retrieval prefixes (per child chunk).
    if contextual_retrieval_enabled():
        await progress.stage("enrich", message="Generating contextual prefixes")
        await attach_context_prefixes(chunks)

    # 4. Embed
    await progress.stage(
        "embed",
        message=f"Embedding {len(chunks)} chunks via {embedding_model}",
        chunks_total=len(chunks),
        chunks_done=0,
    )
    spec_for(embedding_model)  # validate the model early — raises on unknown

    # Background heartbeat: fires every 3s while embed() runs so the UI
    # progress bar doesn't sit silent. embed() itself doesn't expose a
    # per-batch callback, but a simple time-based ping is enough to show
    # the pipeline is alive.
    async def _embed_heartbeat() -> None:
        elapsed = 0
        try:
            while True:
                await asyncio.sleep(3)
                elapsed += 3
                await progress.stage(
                    "embed",
                    message=(
                        f"Embedding {len(chunks)} chunks via {embedding_model} ({elapsed}s elapsed)"
                    ),
                    chunks_total=len(chunks),
                    chunks_done=0,
                )
        except asyncio.CancelledError:
            return

    _hb_task = asyncio.create_task(_embed_heartbeat())
    try:
        vectors = await embed(
            embedding_model,
            [_embed_text_for(c) for c in chunks],
            input_type="document",
            # Provenance on the shared embedding cache: this ingest run's
            # organization, carried in from the record being ingested.
            organization_id=organization_id,
        )
    finally:
        _hb_task.cancel()
        # Don't block shutdown on the heartbeat coroutine winding down.
        try:
            await asyncio.wait_for(_hb_task, timeout=1.0)
        except (asyncio.CancelledError, TimeoutError):
            pass

    await progress.stage(
        "embed",
        message="Embeddings complete",
        chunks_total=len(chunks),
        chunks_done=len(chunks),
    )

    # 5. Upsert via the shared ingestion path
    extra = dict(extra_metadata or {})
    extra.update(
        {
            "file_name": file_name,
            "storage_uri": storage_uri,
            "raw_chars": raw_total,
            "cleaned_chars": cleaned_total,
            "page_count": len(pages),
            "ocr_pages": sum(1 for p in pages if p.used_ocr),
            "cleanup_applied": cleanup,
            "section_histogram": section_hist,
        }
    )
    resolved = ResolvedSource(
        source_kind="cld_file",
        source_id=cld_file_id,
        field_id=None,
        owner_id=owner_id,
        organization_id=organization_id,
        text=raw_concat,
        mime_type="application/pdf",
        language=None,
        source_hash=source_hash,
        metadata=extra,
    )
    await progress.stage("upsert", message="Persisting chunks + embeddings")
    write_result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model=embedding_model,
        allow_global_org=allow_global_org,
        embeddings=vectors,
        processed_document_id=processed_document_id,
        page_id_lookup=page_id_lookup,
    )
    written = write_result["chunks_written"]
    await progress.stage(
        "complete",
        message=f"Indexed {written} chunks across {len(pages)} pages",
        pages_total=len(pages),
        pages_done=len(pages),
        chunks_total=written,
        chunks_done=written,
    )

    return IngestionResult(
        source_kind="cld_file",
        source_id=cld_file_id,
        field_id=None,
        chunks_written=written,
        embeddings_written=written,
        skipped_unchanged=False,
        embedding_model=embedding_model,
        error=(str(clean_incomplete) if clean_incomplete is not None else None),
    )


# Silence the lint complaints about unused dataclass-side imports.
_ = (PARENT_SIZE, PARENT_OVERLAP, CHILD_SIZE, CHILD_OVERLAP, CHUNKER_VERSION)


__all__ = ["chunk_pdf_pages", "extract_pages", "ingest_pdf"]
