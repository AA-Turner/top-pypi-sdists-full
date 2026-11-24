"""A page is only ever rendered within the pixel budget.

Live 2026-11-04: a 724 KB phone photo saved as a PDF (2268 x 4032 pt pages) rendered
at OCR's 300 DPI became 159 megapixels; Tesseract peaked at 2.3 GB on top of a
server already using 3 GB of its 4 GB. Each of the four attempts killed a live
task and abandoned everything running on it. These tests render a page of exactly
that size through the real PyMuPDF and read the size Tesseract was actually handed.
"""

from __future__ import annotations

import io

import pymupdf
import pytest
from PIL import Image

from matrx_files.specific_handlers.pdf.analyze.text_extraction import _render_page_png
from matrx_files.specific_handlers.pdf.extract import ocr as ocr_module
from matrx_files.specific_handlers.pdf.ops.render import render_page_to_image_bytes
from matrx_files.specific_handlers.pdf.render_budget import (
    RENDER_MAX_MEGAPIXELS,
    bounded_render_dpi,
)

PHOTO_PAGE_PT = (2268, 4032)
BUDGET = RENDER_MAX_MEGAPIXELS * 1_000_000


def _photo_page_doc() -> pymupdf.Document:
    doc = pymupdf.open()
    doc.new_page(width=PHOTO_PAGE_PT[0], height=PHOTO_PAGE_PT[1])
    return doc


class _FakeTesseract:
    TesseractNotFoundError = RuntimeError

    def __init__(self) -> None:
        self.sizes: list[tuple[int, int]] = []

    def image_to_string(self, img: Image.Image, config: str | None = None) -> str:
        self.sizes.append(img.size)
        return ""


@pytest.fixture
def tesseract(monkeypatch: pytest.MonkeyPatch) -> _FakeTesseract:
    fake = _FakeTesseract()
    monkeypatch.setattr(ocr_module, "_tesseract", lambda: fake)
    return fake


def test_ocr_of_a_photo_sized_page_stays_within_the_budget(tesseract: _FakeTesseract) -> None:
    with _photo_page_doc() as doc:
        ocr_module.ocr_pymupdf_page(doc[0])
    width, height = tesseract.sizes[0]
    assert width * height <= BUDGET


def test_the_ocr_detector_render_stays_within_the_budget() -> None:
    with _photo_page_doc() as doc:
        png = _render_page_png(doc[0])
    with Image.open(io.BytesIO(png)) as img:
        assert img.size[0] * img.size[1] <= BUDGET


def test_a_requested_page_render_stays_within_the_budget_and_says_what_it_did() -> None:
    with _photo_page_doc() as doc:
        pdf_bytes = doc.tobytes()
    rendered = render_page_to_image_bytes(pdf_bytes, page=1, dpi=300)
    assert rendered.width * rendered.height <= BUDGET
    assert rendered.dpi < 300


def test_a_huge_uploaded_image_is_shrunk_before_ocr(tesseract: _FakeTesseract) -> None:
    buffer = io.BytesIO()
    Image.new("L", (9000, 6000), 255).save(buffer, format="PNG")
    ocr_module.ocr_image_bytes(buffer.getvalue())
    width, height = tesseract.sizes[0]
    assert width * height <= BUDGET


def test_an_ordinary_page_keeps_its_full_dpi(tesseract: _FakeTesseract) -> None:
    assert bounded_render_dpi(612, 792, 300) == 300
    with pymupdf.open() as doc:
        doc.new_page(width=612, height=792)
        ocr_module.ocr_pymupdf_page(doc[0])
    assert tesseract.sizes[0] == (2550, 3300)
