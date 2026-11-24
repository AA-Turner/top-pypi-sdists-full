"""A page that is provably blank is never sent to OCR; a faint page with writing always is.

Review 2026-11-19 (Matrx Scan): a blank scanned page was still rendered at 300 DPI and read by
Tesseract (it came back ``ocr``, 0 characters); only indexing was skipped. With a ``BlankPageTest``
the extractor measures the page small in grey first and skips OCR only when the ink is at most the
test's limit. Faint, light-pencil and low-contrast writing must still be read: when unsure, OCR.
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from matrx_files.specific_handlers.pdf.extract import text as text_mod
from matrx_files.specific_handlers.pdf.extract.text import BlankPageTest, extract_text_pages

#: The host's starting values (aidream knobs documents.pdf_extract.blank_page_*).
TEST = BlankPageTest(max_ink_ppm=5, min_contrast=8)
W, H = 1275, 1650  # a phone crop of a Letter page at 150 DPI


def _font(size: int):  # noqa: ANN202
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def _photo(*, paper: int = 255, ink: int | None = None, words: str = "Call Dana at 4", size: int = 28,
           line: int | None = None, jpeg: bool = False) -> bytes:
    image = Image.new("L", (W, H), paper)
    draw = ImageDraw.Draw(image)
    if ink is not None:
        draw.text((200, 300), words, fill=ink, font=_font(size))
    if line is not None:  # one light pencil tick, a pixel wide
        draw.line([(300, 900), (340, 880), (380, 905)], fill=line, width=1)
    buf = io.BytesIO()
    image.save(buf, "JPEG" if jpeg else "PNG", quality=80)
    return buf.getvalue()


PAGES = {
    "blank": _photo(),
    "blank_grey_paper": _photo(paper=200, jpeg=True),
    "faint_writing": _photo(ink=225),
    "very_faint_writing": _photo(ink=240),
    "faint_small_word": _photo(ink=245, size=14, words="ok"),
    "light_pencil_tick": _photo(line=200),
    "low_contrast": _photo(paper=200, ink=170, jpeg=True),
    "one_tiny_mark": _photo(ink=0, size=10, words="x"),
}
WRITTEN = [name for name in PAGES if not name.startswith("blank")]


def _scan_pdf(path: Path, photos: list[bytes]) -> str:
    """Each photo full-bleed on a Letter page (reportlab embeds the pixels losslessly; no PyMuPDF)."""
    pdf = canvas.Canvas(str(path), pagesize=(612, 792))
    for raw in photos:
        pdf.drawImage(ImageReader(io.BytesIO(raw)), 0, 0, width=612, height=792)
        pdf.showPage()
    pdf.save()
    return str(path)


@pytest.fixture
def scan(tmp_path: Path) -> str:
    return _scan_pdf(tmp_path / "scan.pdf", list(PAGES.values()))


@pytest.fixture
def ocr_calls(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    calls: list[int] = []

    def _ocr(page, *_a, **_k) -> str:  # noqa: ANN001
        calls.append(page.number)
        return f"words on page {page.number + 1}"

    monkeypatch.setattr(text_mod, "ocr_pymupdf_page", _ocr)
    return calls


def test_only_the_blank_pages_skip_ocr(scan: str, ocr_calls: list[int]) -> None:
    pages = extract_text_pages(scan, use_ocr_threshold=100, blank_page=TEST)
    names = list(PAGES)
    read = sorted(names[i] for i in ocr_calls)
    assert read == sorted(WRITTEN), "every page with writing, however faint, is read by OCR"
    for name, page in zip(names, pages, strict=True):
        if name.startswith("blank"):
            assert page.blank_ink_ppm is not None and page.blank_ink_ppm <= TEST.max_ink_ppm
            assert page.text == "" and page.extraction_method == "native" and page.ocr_error is None
        else:
            assert page.blank_ink_ppm is None and page.extraction_method == "ocr"


def test_without_the_test_every_textless_page_is_read(scan: str, ocr_calls: list[int]) -> None:
    pages = extract_text_pages(scan, use_ocr_threshold=100)
    assert len(ocr_calls) == len(PAGES)
    assert all(p.blank_ink_ppm is None for p in pages)


def test_forced_ocr_reads_a_blank_page_too(scan: str, ocr_calls: list[int]) -> None:
    extract_text_pages(scan, force_ocr=True, blank_page=TEST)
    assert len(ocr_calls) == len(PAGES)


def test_a_page_with_a_text_layer_is_never_measured(tmp_path: Path, ocr_calls: list[int],
                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    def _no_measure(*_a, **_k) -> int:  # noqa: ANN002
        raise AssertionError("a page with native text is judged on its text, not measured")

    monkeypatch.setattr(text_mod, "page_ink_ppm", _no_measure)
    path = tmp_path / "short.pdf"
    pdf = canvas.Canvas(str(path), pagesize=(612, 792))
    pdf.drawString(72, 720, "Page 3")  # short: OCR is wanted
    pdf.save()
    pages = extract_text_pages(str(path), use_ocr_threshold=100, blank_page=TEST)
    assert ocr_calls == [0] and pages[0].extraction_method == "ocr"


def test_a_measure_that_fails_means_the_page_is_read(scan: str, ocr_calls: list[int],
                                                     monkeypatch: pytest.MonkeyPatch) -> None:
    def _broken(*_a, **_k) -> int:  # noqa: ANN002
        raise RuntimeError("render failed")

    monkeypatch.setattr(text_mod, "page_ink_ppm", _broken)
    extract_text_pages(scan, use_ocr_threshold=100, blank_page=TEST)
    assert len(ocr_calls) == len(PAGES)


def test_the_measure_counts_light_writing_on_dark_paper(tmp_path: Path, ocr_calls: list[int]) -> None:
    path = _scan_pdf(tmp_path / "dark.pdf", [_photo(paper=40, ink=90)])
    pages = extract_text_pages(path, use_ocr_threshold=100, blank_page=TEST)
    assert ocr_calls == [0], "light writing on dark paper is ink, so the page is read"
    assert pages[0].blank_ink_ppm is None and pages[0].extraction_method == "ocr"
