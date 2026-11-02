"""The OCR detector is bounded — a big PDF never times out and never loses the
pages it already read.

2026-09-26: a 133-page slide deck (128 sparse pages flagged for OCR) hit the
dispatcher's 120 s ``wait_for`` twice; the detector OCR'd serially, ran
Tesseract twice per page, and the timeout threw every finished page away —
the PDF studio got only "failed". These tests drive the detector through the
real dispatcher wrapper (``_run_detector``) with a slow fake provider and a
short spec timeout.
"""

from __future__ import annotations

import asyncio
import time

import pytest

pytest.importorskip("pymupdf")
pytest.importorskip("pytesseract")

PAGE_SECONDS = 0.2
PAGES = 40


class _SlowProvider:
    provider_id = "slow-cloud"

    async def ocr_page_image(self, image_bytes: bytes) -> str:
        await asyncio.sleep(PAGE_SECONDS)
        return "recognized words"


def _ctx(pages: int):
    import pymupdf

    from matrx_files.analysis.context import PipelineContext, ResolvedSettings

    doc = pymupdf.open()
    for _ in range(pages):
        doc.new_page()

    async def _emit(_result):
        return None

    ctx = PipelineContext(
        file_id="file-big",
        owner_id="user-1",
        mime_type="application/pdf",
        bytes_in_memory=doc.tobytes(),
        settings=ResolvedSettings(),
        emit=_emit,
    )
    ctx.cache["pymupdf_doc"] = doc
    ctx.cache["ocr_pages_needed"] = list(range(1, pages + 1))
    ctx.cache["ocr_provider"] = _SlowProvider()
    return ctx


@pytest.mark.asyncio
async def test_a_document_too_big_for_the_timeout_returns_partial_not_failed(monkeypatch):
    from matrx_files.analysis import dispatcher
    from matrx_files.analysis.protocol import DetectorSpec
    from matrx_files.specific_handlers.pdf.analyze import text_extraction

    # Confidence scoring is real Tesseract; stub it so the test measures the
    # detector's scheduling, not this machine's CPU.
    monkeypatch.setattr(text_extraction, "_ocr_confidence_for_image", lambda png: 0.9)

    async def _no_capture(*a, **k):
        return None

    monkeypatch.setattr(dispatcher, "capture_error", _no_capture)

    # Serial cost would be PAGES * PAGE_SECONDS = 8 s; the hard timeout is 2 s.
    spec = DetectorSpec(kind="text_extraction_ocr", cost_class="slow", timeout_seconds=2.0)
    started = time.monotonic()
    result = await dispatcher._run_detector(spec, "n/a", _ctx(PAGES))
    elapsed = time.monotonic() - started

    assert result.status == "success", result.error
    assert elapsed < 2.0
    s = result.summary
    assert s["pages_requested"] == PAGES
    assert 0 < s["pages_ocred"] < PAGES
    assert s["pages_pending"] == PAGES - s["pages_ocred"]
    assert s["complete"] is False
    assert s["stopped_reason"] == "time_budget"
    # What was read is kept, page by page.
    assert len(result.payload["pages"]) == s["pages_ocred"]
    assert result.payload["pages_pending"]


@pytest.mark.asyncio
async def test_a_document_that_fits_is_complete(monkeypatch):
    from matrx_files.analysis import dispatcher
    from matrx_files.analysis.protocol import DetectorSpec
    from matrx_files.specific_handlers.pdf.analyze import text_extraction

    monkeypatch.setattr(text_extraction, "_ocr_confidence_for_image", lambda png: 0.9)
    spec = DetectorSpec(kind="text_extraction_ocr", cost_class="slow", timeout_seconds=30.0)
    result = await dispatcher._run_detector(spec, "n/a", _ctx(5))
    assert result.status == "success"
    assert result.summary["complete"] is True
    assert result.summary["pages_ocred"] == 5
    assert result.payload["pages_pending"] == []


def test_one_tesseract_pass_gives_text_and_confidence():
    """The in-process provider reads a page ONCE for both text and confidence."""
    import pymupdf

    from matrx_files.specific_handlers.pdf.analyze.text_extraction import (
        _ocr_text_and_confidence,
        _render_page_png,
    )

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 144), "Atoms molecules and ions", fontsize=28)
    try:
        text, confidence = _ocr_text_and_confidence(_render_page_png(page))
    except Exception as exc:  # noqa: BLE001
        if type(exc).__name__ == "TesseractNotFoundError":
            pytest.skip("tesseract binary not installed")
        raise
    assert "molecules" in text.lower()
    assert confidence is not None and 0 < confidence <= 1
