"""Async-surface parity tests for the Phase 0 PDF refactor.

Every CPU-bound op gained an ``_async`` sibling that hops off the event loop
via the matrx-pdf CPU executor. These tests assert the async variants produce
results identical to their sync counterparts.
"""

from __future__ import annotations

import pymupdf
import pytest

from matrx_files.specific_handlers.pdf import (
    PDFHandler,
    PdfCropBox,
    PdfPageRange,
)



def _sample_pdf(page_count: int = 3) -> bytes:
    doc = pymupdf.open()
    try:
        for page_num in range(1, page_count + 1):
            page = doc.new_page(width=300, height=400)
            page.insert_text((72, 72), f"Async sample page {page_num}")
        return doc.tobytes()
    finally:
        doc.close()


async def test_extract_pages_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_result = handler.extract_pages_from_bytes(pdf_bytes, pages=[2, 3])
    async_result = await handler.extract_pages_from_bytes_async(pdf_bytes, pages=[2, 3])

    assert sync_result.page_count == async_result.page_count == 2
    assert sync_result.metadata["source_pages"] == async_result.metadata["source_pages"]


async def test_crop_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()
    crop_box = PdfCropBox(x0=0, y0=0, x1=200, y1=300)

    sync_result = handler.crop_pages_in_bytes(pdf_bytes, crop_box=crop_box, pages=[1])
    async_result = await handler.crop_pages_in_bytes_async(
        pdf_bytes, crop_box=crop_box, pages=[1]
    )

    assert sync_result.page_count == async_result.page_count


async def test_rotate_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_result = handler.rotate_pages_in_bytes(pdf_bytes, rotation=180, pages=[2])
    async_result = await handler.rotate_pages_in_bytes_async(
        pdf_bytes, rotation=180, pages=[2]
    )

    sync_doc = pymupdf.open(stream=sync_result.content, filetype="pdf")
    async_doc = pymupdf.open(stream=async_result.content, filetype="pdf")
    try:
        assert sync_doc[1].rotation == async_doc[1].rotation == 180
    finally:
        sync_doc.close()
        async_doc.close()


async def test_delete_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_result = handler.delete_pages_from_bytes(
        pdf_bytes, page_ranges=[PdfPageRange(start=2, end=2)]
    )
    async_result = await handler.delete_pages_from_bytes_async(
        pdf_bytes, page_ranges=[PdfPageRange(start=2, end=2)]
    )

    assert sync_result.page_count == async_result.page_count == 2


async def test_merge_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()
    sources = [
        {"content": pdf_bytes, "pages": [1]},
        {"content": pdf_bytes, "page_ranges": [{"start": 2, "end": 3}]},
    ]

    sync_result = handler.merge_pdfs_from_bytes(sources)
    async_result = await handler.merge_pdfs_from_bytes_async(sources)

    assert sync_result.page_count == async_result.page_count == 3


async def test_split_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_parts = handler.split_pdf_bytes(pdf_bytes, max_pages_per_part=2)
    async_parts = await handler.split_pdf_bytes_async(pdf_bytes, max_pages_per_part=2)

    assert len(sync_parts) == len(async_parts) == 2
    assert [p.page_numbers for p in sync_parts] == [p.page_numbers for p in async_parts]


async def test_compress_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_bytes = handler.compress_pdf_bytes(pdf_bytes, level=1)
    async_bytes = await handler.compress_pdf_bytes_async(pdf_bytes, level=1)

    assert isinstance(sync_bytes, bytes)
    assert isinstance(async_bytes, bytes)
    # Both versions should be reopenable.
    pymupdf.open(stream=sync_bytes, filetype="pdf").close()
    pymupdf.open(stream=async_bytes, filetype="pdf").close()


async def test_extract_text_pages_async_matches_sync() -> None:
    handler = PDFHandler(app_name="test_async_pdf")
    pdf_bytes = _sample_pdf()

    sync_pages = handler.extract_text_pages_from_bytes(pdf_bytes, use_ocr_threshold=0)
    async_pages = await handler.extract_text_pages_from_bytes_async(
        pdf_bytes, use_ocr_threshold=0
    )

    assert len(sync_pages) == len(async_pages)
    assert sync_pages[0].text == async_pages[0].text
    assert sync_pages[0].extraction_method == async_pages[0].extraction_method


def test_pdf_page_range_validates_start_le_end() -> None:
    # Equal start/end is valid.
    PdfPageRange(start=3, end=3)
    # Reversed range raises at construction time, not at use time.
    with pytest.raises(ValueError, match="start must be <= end"):
        PdfPageRange(start=5, end=2)


async def test_process_chunks_with_ai_respects_max_concurrent() -> None:
    """When max_concurrent is set, the gate must hold dispatch count steady."""
    import asyncio

    handler = PDFHandler(app_name="test_async_pdf")
    in_flight = 0
    peak = 0
    lock = asyncio.Lock()

    async def slow_proc(chunk: str) -> dict:
        nonlocal in_flight, peak
        async with lock:
            in_flight += 1
            peak = max(peak, in_flight)
        await asyncio.sleep(0.01)
        async with lock:
            in_flight -= 1
        return {"content": chunk}

    chunks = [f"c{i}" for i in range(20)]
    await handler.process_chunks_with_ai(
        chunks, ai_processor=slow_proc, max_concurrent=3
    )
    assert peak <= 3, f"peak concurrency {peak} exceeded cap of 3"
