"""Search hits carry the RIGHT snippet, page and box (live walk 2026-10-22).

Searching "fox" in the workspace's Analysis > Search showed "131,119 mple." on both pages: the literal
path took its boxes from PyMuPDF's ``search_for`` but cut the snippet out of a different text with an
end offset of 0, so every hit on a page showed the same garbled slice, and ``case_sensitive`` was
ignored. One matcher over one text now serves both modes.
"""

from __future__ import annotations

import pytest
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from matrx_files.specific_handlers.pdf.handler import PDFHandler
from matrx_files.specific_handlers.pdf.extract.search import search_text

FILLER = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor."


def _pdf(pages: list[list[str]]) -> bytes:
    output = BytesIO()
    page = canvas.Canvas(output, pagesize=(612, 792))
    page.setFont("Helvetica", 11)
    for lines in pages:
        for i, line in enumerate(lines):
            page.drawString(72, 792 - (72 + i * 20), line)
        page.showPage()
    page.save()
    writer = PdfWriter()
    writer.append_pages_from_reader(PdfReader(BytesIO(output.getvalue())))
    result = BytesIO()
    writer.write(result)
    return result.getvalue()


PDF = _pdf([
    [FILLER, FILLER, "The quick brown fox jumps over the lazy dog.", FILLER, "A closing sample."],
    [FILLER, "Two Foxes crossed; one more fox", "waited at the river bank.", FILLER],
])


def test_each_literal_hit_shows_the_words_around_its_own_match() -> None:
    hits = search_text(PDF, query="fox")
    assert [h.page_number for h in hits] == [1, 2, 2]
    first, foxes, last = hits
    assert "quick brown fox jumps over" in first.snippet
    assert "Two Foxes crossed" in foxes.snippet
    assert "one more fox waited at the river" in last.snippet  # a line break reads as a space
    assert len({h.snippet for h in hits}) == 3
    for h in hits:
        assert h.matched_text.lower() == "fox"
        assert h.char_start is not None and h.char_end == h.char_start + 3
        # The snippet never starts or ends inside a word.
        assert not h.snippet.startswith("mple")


def test_the_box_is_the_glyphs_of_the_match_on_its_line() -> None:
    hits = search_text(PDF, query="fox")
    foxes = hits[1]
    # Inside "Foxes" the box covers "Fox", not the whole word.
    pages = PDFHandler(app_name="test_pdf_search_hits").extract_text_pages_from_bytes(
        PDF, use_ocr_threshold=0, include_words=True
    )
    page = pages[1]
    first_page = pages[0]
    word_box = next(w for w in page.words or [] if w.word == "Foxes")
    expected_match_width = (
        word_box.x1 - word_box.x0
    ) * stringWidth("Fox", "Helvetica", 11) / stringWidth("Foxes", "Helvetica", 11)
    assert foxes.bbox.x0 == pytest.approx(word_box.x0, abs=1)
    assert foxes.bbox.x1 == pytest.approx(word_box.x0 + expected_match_width, abs=1)
    assert 95 < hits[0].bbox.y0 < 120
    assert hits[0].bbox.y1 < first_page.height


def test_case_sensitive_is_honoured_and_a_phrase_crosses_a_line_break() -> None:
    assert [h.page_number for h in search_text(PDF, query="Fox", case_sensitive=True)] == [2]
    phrase = search_text(PDF, query="more fox waited")
    assert len(phrase) == 1 and phrase[0].page_number == 2
    assert phrase[0].matched_text == "more fox waited"


def test_regex_hits_keep_their_offsets_and_snippets() -> None:
    hits = search_text(PDF, query=r"fox(es)?", regex=True)
    assert len(hits) == 3
    assert {h.matched_text.lower() for h in hits} == {"fox", "foxes"}
