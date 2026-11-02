"""Board row H8 — the OCR detector announces a missing binary ONCE, with a
real organization, instead of losing it per-page.

Drives `TextExtractionOcrDetector.run()` end to end against a real one-page
PDF (via PyMuPDF) and a fake OCR provider that raises
`pytesseract.TesseractNotFoundError` on every page. Pins three things at
once: (1) the detector never raises — a missing binary is a captured wall,
not a crashed pipeline; (2) `announce_block` is called exactly once, not
once per OCR page; (3) the organization is resolved from the ambient context
and passed EXPLICITLY — proving the fix for the gap found in the same
change: `announce_block`'s sink runs inside a `detached_task`
(context-stripped), so a call that relied on the sink's own ambient lookup
would silently drop the organization.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

pytest.importorskip("pymupdf")
pytest.importorskip("pytesseract")


def _build_ctx(ocr_pages: list[int]):
    import pymupdf

    from matrx_files.analysis.context import PipelineContext, ResolvedSettings

    doc = pymupdf.open()
    doc.new_page()
    doc.new_page()

    class _AlwaysMissingProvider:
        provider_id = "tesseract"

        async def ocr_page_image(self, image_bytes: bytes) -> str:
            import pytesseract

            raise pytesseract.TesseractNotFoundError()

    async def _emit(_result):
        return None

    ctx = PipelineContext(
        file_id="file-abc",
        owner_id="user-1",
        mime_type="application/pdf",
        bytes_in_memory=doc.tobytes(),
        settings=ResolvedSettings(),
        emit=_emit,
    )
    ctx.cache["pymupdf_doc"] = doc
    ctx.cache["ocr_pages_needed"] = ocr_pages
    ctx.cache["ocr_provider"] = _AlwaysMissingProvider()
    return ctx


@pytest.mark.asyncio
async def test_a_missing_ocr_binary_is_announced_once_with_the_active_organization():
    from matrx_files.specific_handlers.pdf.analyze.text_extraction import (
        TextExtractionOcrDetector,
    )

    ctx = _build_ctx(ocr_pages=[1, 2])
    detector = TextExtractionOcrDetector()

    # Both symbols are imported LAZILY inside the except block (module-level
    # patch targets), so patching the source modules is what actually takes
    # effect at call time.
    with (
        patch("matrx_utils.ctx.get_active_organization_id", return_value="org-active-1"),
        patch("matrx_utils.block_sink.announce_block") as mock_announce,
    ):
        result = await detector.run(ctx, tier="n/a")

    assert result.status != "failed"
    mock_announce.assert_called_once()
    kwargs = mock_announce.call_args.kwargs
    assert kwargs["organization_id"] == "org-active-1"
    assert kwargs["error_class"] == "ocr_binary_missing"
    assert kwargs["engine"] == "file_reader"
    assert kwargs["source_type"] == "file"
    assert kwargs["input_ref"] == "file-abc"
