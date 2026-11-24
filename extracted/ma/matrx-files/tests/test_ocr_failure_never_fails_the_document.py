"""OCR that cannot run never fails a document that has a native text layer.

Feedback 95779990: with OCR unavailable on the host (or failing on one page), the OCR fallback
in ``extract_text_pages`` raised out of the loop and the WHOLE extraction failed — a PDF whose
every word was in its native text layer came back with no text at all. Native text must always
come through; the OCR failure is stated on the page (``ocr_error``), never fatal.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from matrx_files.specific_handlers.pdf.extract import text as text_mod
from matrx_files.specific_handlers.pdf.extract.text import extract_text_pages

NATIVE = "Quarterly revenue rose to 4.2 million dollars on strong renewals."


def _two_page_pdf(path: Path) -> None:
    import pymupdf

    doc = pymupdf.open()
    try:
        doc.new_page(width=612, height=792).insert_text((72, 72), NATIVE)
        doc.new_page(width=612, height=792)  # blank: a page OCR would be asked to read
        doc.save(str(path))
    finally:
        doc.close()


def _ocr_unavailable(_page, *_a, **_kw) -> str:
    raise RuntimeError("tesseract is not installed or it's not in your PATH")


@pytest.fixture
def pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setattr(text_mod, "ocr_pymupdf_page", _ocr_unavailable)
    path = tmp_path / "report.pdf"
    _two_page_pdf(path)
    return str(path)


def test_native_text_comes_through_when_ocr_fallback_fails(pdf: str) -> None:
    pages = extract_text_pages(pdf, use_ocr_threshold=100)

    assert len(pages) == 2
    assert NATIVE in pages[0].text
    # Page 1 is short enough to ask for OCR; OCR failed, its native text stays and says why.
    assert pages[0].extraction_method == "native"
    assert pages[0].ocr_error and "tesseract" in pages[0].ocr_error
    assert pages[1].ocr_error, "the blank page's OCR failure must be announced on that page"


def test_forced_ocr_failure_falls_back_to_native_text(pdf: str) -> None:
    pages = extract_text_pages(pdf, force_ocr=True)

    assert NATIVE in pages[0].text
    assert pages[0].extraction_method == "native"
    assert pages[0].ocr_error


def test_a_page_that_needs_no_ocr_carries_no_ocr_error(pdf: str) -> None:
    pages = extract_text_pages(pdf, use_ocr_threshold=0)

    assert NATIVE in pages[0].text
    assert pages[0].ocr_error is None
