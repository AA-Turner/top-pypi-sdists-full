"""Stored document text never carries non-printing control characters.

Live 2026-10-22: the 240-page AP Biology PDF's stored clean text held ~2% stray
U+0003 / U+0007 (broken font encodings) that reached the model unfiltered. The
strip lives once (``strip_control_chars``) and is applied at extraction, at the
cleaner's output and at every document-text write.
"""

from __future__ import annotations

import unicodedata

from matrx_rag.llm import normalize_cleaned_page
from matrx_rag.pdf_pipeline import _without_control_chars
from matrx_rag.text_hygiene import strip_control_chars

DIRTY = "Cell\x03 membranes\x07 are\x00 selectively\x1b permeable.\r\nSecond\tline\fthird\x7f\x85."


def _junk(s: str) -> int:
    return sum(1 for ch in s if unicodedata.category(ch) == "Cc" and ch not in "\n\t")


def test_controls_go_newlines_and_tabs_stay():
    out = strip_control_chars(DIRTY)
    assert _junk(out) == 0
    assert out == "Cell membranes are selectively permeable.\nSecond\tline\nthird."


def test_none_and_empty_are_empty():
    assert strip_control_chars(None) == "" and strip_control_chars("") == ""


def test_cleaner_output_is_stripped():
    page = normalize_cleaned_page({"text": DIRTY, "section_kind": "body"})
    assert _junk(page.text) == 0 and "selectively permeable" in page.text


def test_extracted_pages_are_stripped():
    from matrx_files.specific_handlers.pdf.models import PdfPageText  # noqa: PLC0415

    page = PdfPageText(
        page_index=0, page_number=1, width=1.0, height=1.0, rotation=0,
        extraction_method="native", text=DIRTY, char_count=len(DIRTY),
    )
    (out,) = _without_control_chars([page])
    assert _junk(out.text) == 0 and out.char_count == len(out.text)
