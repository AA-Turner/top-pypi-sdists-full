"""Text chunking with overlap and per-page source mapping.

``chunk_text`` is the simple character-overlap chunker the legacy callers use.
``chunk_page_text`` produces ``PdfTextChunk`` records with page-span
back-references — the contract consumed by the large-document pipeline at
``docs/PDF_LARGE_DOCUMENT_PIPELINE.md``.
"""

from __future__ import annotations

import hashlib

from ..models import PdfChunkedTextResult, PdfPageSpan, PdfPageText, PdfTextChunk


def chunk_text(
    text: str,
    chunk_size: int = 2000,
    overlap_size: int = 200,
) -> list[str]:
    chunks: list[str] = []
    text_length = len(text)
    step = max(chunk_size - overlap_size, 1)
    for i in range(0, text_length, step):
        chunk = text[i : i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def chunk_page_text(
    pages: list[PdfPageText],
    chunk_size: int = 2000,
    overlap_size: int = 200,
    include_page_markers: bool = False,
    document_label: str | None = None,
    document_id: str | None = None,
) -> PdfChunkedTextResult:
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1.")
    if overlap_size < 0:
        raise ValueError("overlap_size must be >= 0.")
    if overlap_size >= chunk_size:
        raise ValueError("overlap_size must be smaller than chunk_size.")

    parts: list[str] = []
    page_segments: list[tuple[PdfPageText, int, int, int, int]] = []
    cursor = 0
    label = document_label or document_id or "document"

    for page in pages:
        segment_start = cursor
        if include_page_markers:
            marker = (
                f"--- PDF_PAGE_START document={label} page={page.page_number} ---\n"
            )
            parts.append(marker)
            cursor += len(marker)

        page_start = cursor
        parts.append(page.text)
        cursor += len(page.text)
        page_end = cursor

        if not page.text.endswith("\n"):
            parts.append("\n")
            cursor += 1

        if include_page_markers:
            marker = (
                f"--- PDF_PAGE_END document={label} page={page.page_number} ---\n"
            )
            parts.append(marker)
            cursor += len(marker)
        segment_end = cursor
        page_segments.append((page, segment_start, segment_end, page_start, page_end))

    full_text = "".join(parts)
    source_document = document_id or document_label
    source_key = (
        source_document
        or hashlib.sha256(full_text.encode("utf-8")).hexdigest()[:16]
    )

    chunks: list[PdfTextChunk] = []
    step = chunk_size - overlap_size
    starts = list(range(0, len(full_text), step)) if full_text else []

    for chunk_index, start in enumerate(starts):
        end = min(start + chunk_size, len(full_text))
        chunk_text_value = full_text[start:end]
        if not chunk_text_value.strip():
            continue

        page_spans: list[PdfPageSpan] = []
        for page, segment_start, segment_end, page_start, page_end in page_segments:
            intersect_start = max(start, segment_start)
            intersect_end = min(end, segment_end)
            if intersect_start >= intersect_end:
                continue
            page_spans.append(
                PdfPageSpan(
                    page_number=page.page_number,
                    page_index=page.page_index,
                    page_char_start=max(0, intersect_start - page_start),
                    page_char_end=min(
                        len(page.text), max(0, intersect_end - page_start)
                    ),
                    chunk_char_start=intersect_start - start,
                    chunk_char_end=intersect_end - start,
                )
            )

        previous_end = (
            min(starts[chunk_index - 1] + chunk_size, len(full_text))
            if chunk_index > 0
            else start
        )
        next_start = (
            starts[chunk_index + 1] if chunk_index + 1 < len(starts) else end
        )
        overlap_previous_chars = max(0, previous_end - start)
        overlap_next_chars = max(0, end - next_start)
        page_numbers = sorted({span.page_number for span in page_spans})

        chunks.append(
            PdfTextChunk(
                chunk_id=f"{source_key}:chunk:{chunk_index}",
                chunk_index=chunk_index,
                text=chunk_text_value,
                document_char_start=start,
                document_char_end=end,
                char_count=len(chunk_text_value),
                page_numbers=page_numbers,
                page_spans=page_spans,
                overlap_previous_chars=overlap_previous_chars,
                overlap_next_chars=overlap_next_chars,
                previous_overlap_text=(
                    chunk_text_value[:overlap_previous_chars]
                    if overlap_previous_chars > 0
                    else None
                ),
                next_overlap_text=(
                    chunk_text_value[-overlap_next_chars:]
                    if overlap_next_chars > 0
                    else None
                ),
                token_estimate=max(1, len(chunk_text_value) // 4),
                source_document=source_document,
            )
        )

    return PdfChunkedTextResult(
        text=full_text,
        chunks=chunks,
        page_count=len(pages),
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )


__all__ = ["chunk_text", "chunk_page_text"]
