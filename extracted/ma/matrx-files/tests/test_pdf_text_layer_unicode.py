"""The invisible text layer carries ANY language, read back by three independent PDF readers.

SUT: ``add_text_layer_bytes`` (the "words in" writer behind the scan save door, Matrx Scan S2).
Break caught: the layer written in a single-byte encoding (WinAnsi/cp1252 with ``errors="replace"``),
which made every Cyrillic, Greek, Arabic, Hebrew, CJK, Polish/Hungarian letter and emoji come back
out of the saved PDF as "?" while the stats said nothing; a word drawn off the page; a box that is
not a finite number poisoning the page's content stream.
"""

from __future__ import annotations

import io
import math
import unicodedata

import pikepdf
import pypdfium2 as pdfium
import pytest

from matrx_files.specific_handlers.pdf.ops.text_layer import LayerPage, LayerWord, add_text_layer_bytes

PAGE_W, PAGE_H = 612.0, 792.0  # US Letter in points; the page image is 1224 x 1584 px (2 px per point)

# Real words a scanned page in each script carries (a menu, a sign, a letterhead, a receipt line).
SCRIPTS: list[tuple[str, str]] = [
    ("accented_latin", "Crème brûlée à la française"),
    ("polish_hungarian", "Łódź Gdańsk Kőszeg Győr"),
    ("cyrillic", "Привет мир"),
    ("greek", "Καλημέρα κόσμε"),
    ("arabic", "مرحبا بالعالم"),
    ("arabic_with_harakat_and_digits", "كِتَابٌ رقم7"),
    ("hebrew", "שלום עולם"),
    ("hebrew_with_niqqud", "שָׁלוֹם"),
    ("cjk", "東京都 서울특별시 漢字"),
    ("emoji", "Paid ✅ 🎉🙂 👩‍💻"),
    ("lone_symbol", "✓"),
]


def _blank_pdf() -> bytes:
    pdf = pikepdf.new()
    pdf.add_blank_page(page_size=(PAGE_W, PAGE_H))
    buf = io.BytesIO()
    pdf.save(buf)
    return buf.getvalue()


def _rtl(text: str) -> bool:
    return any(unicodedata.bidirectional(c) in ("R", "AL") for c in text)


def _layer(text: str, *, top: float = 200.0) -> LayerPage:
    """Boxes as a recogniser reports them: a right-to-left line starts at the right edge."""
    words = []
    x = 100.0
    parts = text.split()
    for part in reversed(parts) if _rtl(text) else parts:
        width = 40.0 * len(part)
        words.append(LayerWord(text=part, box=(x, top, x + width, top + 60.0)))
        x += width + 30.0
    if _rtl(text):
        words.reverse()  # sent in reading order, the first word being the right-most
    return LayerPage(width_px=PAGE_W * 2, height_px=PAGE_H * 2, words=words)


def _norm(s: str) -> str:
    return unicodedata.normalize("NFC", "".join(s.split()))


def _pdfium_text(data: bytes) -> str:
    doc = pdfium.PdfDocument(data)
    try:
        return doc[0].get_textpage().get_text_range()
    finally:
        doc.close()


def _pypdf_text(data: bytes) -> str:
    from pypdf import PdfReader

    return PdfReader(io.BytesIO(data)).pages[0].extract_text() or ""


def _pdfminer_chars(data: bytes) -> list:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTChar, LTTextContainer

    chars = []
    for page in extract_pages(io.BytesIO(data)):
        for el in page:
            if isinstance(el, LTTextContainer):
                for line in el:
                    for ch in getattr(line, "_objs", []):
                        if isinstance(ch, LTChar):
                            chars.append(ch)
    return chars


@pytest.mark.parametrize(("script", "text"), SCRIPTS, ids=[s for s, _ in SCRIPTS])
def test_every_script_reads_back_from_the_saved_pdf_exactly(script: str, text: str) -> None:
    out, stats = add_text_layer_bytes(_blank_pdf(), {1: _layer(text)})
    assert stats["replaced_characters"] == 0, f"{script}: the layer replaced characters"
    want = _norm(text)
    # pypdf reverses right-to-left runs but has no bidi algorithm, so a word mixing Arabic letters
    # with digits is beyond it; everything else must come back as typed.
    if not (_rtl(text) and any(c.isdigit() for c in text)):
        got = _pypdf_text(out)
        assert _norm(got) == want, f"{script}: pypdf read {got!r}"
    # pdfium (Chrome's / Android's / the web viewer's engine) reads it back exactly, as typed.
    assert _norm(_pdfium_text(out)) == want, f"{script}: pdfium read {_pdfium_text(out)!r}"
    # pdfminer (no bidi pass) sees every character, in page order, inside the page.
    chars = _pdfminer_chars(out)
    assert sorted(_norm("".join(c.get_text() for c in chars))) == sorted(want), f"{script}: pdfminer"
    for c in chars:
        assert 0 <= c.x0 <= PAGE_W and 0 <= c.x1 <= PAGE_W + 1 and 0 <= c.y0 <= PAGE_H and 0 <= c.y1 <= PAGE_H


def test_each_word_sits_where_its_box_is_on_the_page() -> None:
    # Top word at image y 100..160 px -> page top 50..80 pt from the top; bottom word near the foot.
    page = LayerPage(width_px=PAGE_W * 2, height_px=PAGE_H * 2, words=[
        LayerWord(text="Привет", box=(200.0, 100.0, 440.0, 160.0)),
        LayerWord(text="東京", box=(800.0, 1400.0, 1000.0, 1480.0)),
    ])
    out, _ = add_text_layer_bytes(_blank_pdf(), {1: page})
    chars = _pdfminer_chars(out)
    top = [c for c in chars if c.get_text() in "Привет"]
    low = [c for c in chars if c.get_text() in "東京"]
    assert top and low
    assert min(c.x0 for c in top) == pytest.approx(100.0, abs=2)
    assert max(c.x1 for c in top) == pytest.approx(220.0, abs=3)
    assert min(c.y0 for c in top) == pytest.approx(PAGE_H - 80.0, abs=3)
    assert min(c.x0 for c in low) == pytest.approx(400.0, abs=2)
    assert min(c.y0 for c in low) == pytest.approx(PAGE_H - 740.0, abs=3)


def test_a_layered_pdf_is_valid_and_reopens_cleanly() -> None:
    out, _ = add_text_layer_bytes(_blank_pdf(), {1: _layer("Привет 東京 🎉 שלום")})
    with pikepdf.open(io.BytesIO(out)) as pdf:
        assert pdf.check_pdf_syntax() == []
        font = next(iter(pdf.pages[0].Resources.Font.values()))
        assert font.Subtype == "/Type0" and font.Encoding == "/Identity-H" and "/ToUnicode" in font


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_a_word_with_a_non_finite_box_is_skipped_and_counted_and_the_rest_of_the_page_survives(bad: float) -> None:
    page = LayerPage(width_px=PAGE_W * 2, height_px=PAGE_H * 2, words=[
        LayerWord(text="Kőszeg", box=(100.0, 200.0, 340.0, 260.0)),
        LayerWord(text="broken", box=(100.0, bad, 340.0, 260.0)),
        LayerWord(text="Győr", box=(400.0, 200.0, 560.0, 260.0)),
    ])
    out, stats = add_text_layer_bytes(_blank_pdf(), {1: page})
    assert stats["skipped_words"] == 1 and stats["words"] == 2
    got = _norm(_pdfium_text(out))
    assert "Kőszeg" in got and "Győr" in got and "broken" not in got
