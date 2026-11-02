"""
U1 — Table Extractor → structured ROW chunks (a Knowledge Asset derivation).

The hero problem: the AMA Guides' impairment-rating tables. A whole-table blob
buries the one row an attorney needs ("DRE Lumbar Category III → 10-13% WPI").
This utility extracts every table with PyMuPDF and indexes each DATA ROW as its
own retrievable chunk — column headers paired with cell values — so a query for
a specific rating value lands on the exact row, with a page anchor for
verification.

It is a thin *generator* on top of :func:`matrx_rag.derivation.derive_chunk_set`
(the platform primitive): fetch the source PDF, run
:func:`matrx_rag.pdf_pipeline.extract_tables`, project each row to text, hand
the specs to ``derive_chunk_set(derivation_kind='table_row')``. Re-running
replaces the doc's ``table_row`` set; nothing else is touched.

Generic by construction — runs on ANY processed_document whose source is a PDF
``cld_file``, library asset or a user's own doc.
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from dataclasses import dataclass

from matrx_rag._ext import NotFoundError, get_db_model
from matrx_rag.derivation import ChunkSpec, DeriveResult, derive_chunk_set
from matrx_rag.stages import ProgressCb, StageEvent, _noop

log = logging.getLogger(__name__)

_CELL_LIMIT = 600  # per-cell char cap so a runaway merged cell can't bloat a row
_MAX_COLS = 60  # ignore absurd "tables" the detector occasionally hallucinates


@dataclass(frozen=True)
class TableDerivationResult:
    processed_document_id: str
    derivative_id: str | None
    tables_found: int
    rows_indexed: int
    chunks_written: int
    derivative_outcome: str | None


def _decode_b64_pdf_to_temp(b64: str) -> str:
    """CPU + disk work for a resolved PDF — must run off the event loop."""
    import base64

    data = base64.b64decode(b64)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(data)
        return tmp.name


async def _fetch_pdf_to_temp(cld_file_id: str) -> str:
    """Resolve a cld_file's bytes through the canonical FileManager and write
    them to a temp file. Mirrors ingestion._maybe_dispatch_pdf's fetch so the
    byte cache / auth hooks apply. Returns the local path (caller deletes)."""
    from matrx_files.cloud_sync.media_ref import MediaRef
    from matrx_utils.ctx import system_file_access

    from matrx_rag._ext import get_cloud_file_manager

    fm = get_cloud_file_manager()
    # Internal RAG table derivation resolving a server-constructed ref — declare it.
    with system_file_access("rag-table-derivation"):
        resolved = await fm.resolve_media_async(MediaRef(file_id=cld_file_id), needs_bytes=True)
    b64 = getattr(resolved, "base64_data", None) if resolved else None
    if not b64:
        raise NotFoundError(f"cld_file {cld_file_id} returned no bytes")
    return await asyncio.to_thread(_decode_b64_pdf_to_temp, b64)


def _row_to_text(
    header: list[str] | None,
    row: list[str],
    *,
    page_number: int,
    table_title: str | None,
) -> str:
    """Project one table row to embeddable text: page anchor + table title +
    one ``Header: value`` line per cell (or bare cells when headerless). The
    header pairing is what lets "DRE Lumbar Category III" hit the right row."""
    lines = [f"PAGE: {page_number}"]
    if table_title:
        lines.append(f"TABLE: {table_title}")
    for j, cell in enumerate(row):
        val = (cell or "").strip()
        if len(val) > _CELL_LIMIT:
            val = val[:_CELL_LIMIT] + "…"
        label = header[j].strip() if header and j < len(header) and header[j] else None
        if label:
            lines.append(f"{label}: {val}")
        elif val:
            lines.append(val)
    return "\n".join(lines).strip()


async def derive_table_rows(
    processed_document_id: str,
    *,
    embedding_model: str | None = None,
    rag_boost: int = 0,
    table_title_from: str | None = None,
    on_progress: ProgressCb = _noop,
) -> TableDerivationResult:
    """Extract every table from the doc's source PDF and index each data row
    as a ``derivation_kind='table_row'`` chunk via ``derive_chunk_set``.

    ``table_title_from`` is reserved for pulling a per-table caption from the
    page's section_title later; today tables are titled by page.
    """
    ProcessedDocuments = get_db_model("ProcessedDocuments")
    doc_rows = await ProcessedDocuments.filter(id=processed_document_id).values(
        "id", "source_kind", "source_id", "name", "organization_id"
    )
    doc = doc_rows[0] if doc_rows else None
    if doc is None:
        raise NotFoundError(f"processed_document {processed_document_id} not found")
    if doc["source_kind"] != "cld_file":
        raise ValueError(f"table derivation needs a cld_file source; got {doc['source_kind']!r}")

    local_path = await _fetch_pdf_to_temp(doc["source_id"])
    try:
        from matrx_rag.pdf_pipeline import extract_tables

        # CPU-bound (pymupdf find_tables) — offload so it can't stall the loop.
        tables = await asyncio.to_thread(extract_tables, local_path)
    finally:
        try:
            os.unlink(local_path)
        except OSError:
            pass

    # Total indexable rows up front so the progress bar has a denominator and
    # we can throttle a high-cardinality loop the way run_clean does.
    total_rows = 0
    for table in tables:
        cells_pre: list[list[str]] = table.get("raw") or []
        if not cells_pre:
            continue
        if int(table.get("cols") or 0) > _MAX_COLS:
            continue
        total_rows += len(cells_pre[1:] if table.get("header") else cells_pre)
    await on_progress(
        StageEvent(
            stage="table_row",
            phase="started",
            message=f"Indexing rows from {len(tables)} table(s)",
            current=0,
            total=total_rows,
            extra={"granularity": "table_row", "tables_found": len(tables)},
        )
    )
    emit_every = max(1, total_rows // 50)
    seen_rows = 0
    last_emit = 0

    specs: list[ChunkSpec] = []
    chunk_index = 0
    for t_idx, table in enumerate(tables):
        cells: list[list[str]] = table.get("raw") or []
        if not cells:
            continue
        cols = int(table.get("cols") or 0)
        if cols > _MAX_COLS:
            log.warning(
                "[table-derive] doc=%s table#%d has %d cols (>%d); skipping",
                processed_document_id,
                t_idx,
                cols,
                _MAX_COLS,
            )
            continue
        header = table.get("header")
        page_number = int(table.get("page_index", 0)) + 1  # 0-based -> 1-based
        body = cells[1:] if header else cells
        table_title = f"page {page_number}, table {t_idx + 1}"
        for r_idx, row in enumerate(body):
            seen_rows += 1
            # Throttled, and ALSO the cooperative cancel point (a canceled
            # on_progress raises CancelledError — do not catch it here).
            if seen_rows == total_rows or (seen_rows - last_emit) >= emit_every:
                last_emit = seen_rows
                await on_progress(
                    StageEvent(
                        stage="table_row",
                        phase="progress",
                        message=f"Row {seen_rows} / {total_rows} (page {page_number})",
                        current=seen_rows,
                        total=total_rows,
                        extra={
                            "granularity": "table_row",
                            "page_number": page_number,
                            "table_index": t_idx,
                        },
                    )
                )
            if not any((c or "").strip() for c in row):
                continue  # blank row
            text = _row_to_text(header, row, page_number=page_number, table_title=table_title)
            if not text or text == f"PAGE: {page_number}":
                continue  # nothing but the anchor — skip
            specs.append(
                ChunkSpec(
                    content_text=text,
                    chunk_index=chunk_index,
                    page_numbers=[page_number],
                    primary_page_number=page_number,
                    chunk_kind="table_row",
                    metadata={
                        "role": "table_row",
                        "page_number": page_number,
                        "table_index": t_idx,
                        "row_index": r_idx,
                        "header": header,
                        "cells": row,
                        "cols": cols,
                        "bbox": table.get("bbox"),
                    },
                )
            )
            chunk_index += 1

    if not specs:
        log.info(
            "[table-derive] doc=%s: %d tables, 0 indexable rows",
            processed_document_id,
            len(tables),
        )
        await on_progress(
            StageEvent(
                stage="table_row",
                phase="done",
                message=f"{len(tables)} table(s), 0 indexable rows",
                current=0,
                total=total_rows,
                extra={
                    "granularity": "table_row",
                    "tables_found": len(tables),
                    "rows_indexed": 0,
                    "chunks_written": 0,
                },
            )
        )
        return TableDerivationResult(
            processed_document_id=processed_document_id,
            derivative_id=None,
            tables_found=len(tables),
            rows_indexed=0,
            chunks_written=0,
            derivative_outcome=None,
        )

    result: DeriveResult = await derive_chunk_set(
        parent_processed_id=processed_document_id,
        derivation_kind="table_row",
        chunks=specs,
        identity={"source": "table_extract", "extractor": "pymupdf"},
        name=f"{doc['name']} (table rows)",
        rag_boost=rag_boost,
        embedding_model=embedding_model,
        chunker_name="table_extract:pymupdf",
        metadata={"tables_found": len(tables), "rows_indexed": len(specs)},
    )

    await on_progress(
        StageEvent(
            stage="table_row",
            phase="done",
            message=f"Indexed {len(specs)} row(s) from {len(tables)} table(s)",
            current=total_rows,
            total=total_rows,
            extra={
                "granularity": "table_row",
                "tables_found": len(tables),
                "rows_indexed": len(specs),
                "chunks_written": result.chunks_written,
            },
        )
    )

    return TableDerivationResult(
        processed_document_id=processed_document_id,
        derivative_id=result.derivative_id,
        tables_found=len(tables),
        rows_indexed=len(specs),
        chunks_written=result.chunks_written,
        derivative_outcome=result.derivative_outcome,
    )


__all__ = ["derive_table_rows", "TableDerivationResult"]
