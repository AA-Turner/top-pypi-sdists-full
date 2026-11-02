"""PDF-PLAN U14 forcing tests: OCR to a searchable PDF, convert to Office, compare, find and replace.

Each output is read back with a different tool than wrote it (pdfplumber / pypdfium2 / python-docx / openpyxl /
python-pptx). Built on the synthetic corpus: no stored files, no PyMuPDF.
"""

from __future__ import annotations

import io

import pytest

pikepdf = pytest.importorskip("pikepdf")
pdfium = pytest.importorskip("pypdfium2")
pdfplumber = pytest.importorskip("pdfplumber")
ocrmypdf = pytest.importorskip("ocrmypdf")
if not getattr(ocrmypdf, "__file__", None):  # pragma: no cover - an empty namespace left by a broken install
    pytest.skip("ocrmypdf is a namespace stub here", allow_module_level=True)
import shutil

pytestmark = pytest.mark.skipif(shutil.which("tesseract") is None, reason="tesseract is not installed")

from _pdf_corpus import SCAN_WORDS, _add_scanned_page, _new_pdf, _save, build_corpus  # noqa: E402

from matrx_files.specific_handlers.pdf.ops.compare import compare_pdf_bytes, text_changes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.convert import convert_pdf_bytes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.ocr import ocr_pdf_bytes, page_text_counts  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.replace import find_replace_preview, replace_pdf_bytes  # noqa: E402

CORPUS = build_corpus()


def _words(data: bytes, page: int = 0) -> set[str]:
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        return {w["text"].lower().strip(".,") for w in pdf.pages[page].extract_words()}


def _pdfium_text(data: bytes, page: int = 0) -> str:
    doc = pdfium.PdfDocument(data)
    try:
        return doc[page].get_textpage().get_text_range()
    finally:
        doc.close()


def _sideways_native_scan() -> bytes:
    """A full page of text scanned with the paper fed sideways and no /Rotate flag: it shows sideways until fixed."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("L", (1700, 2200), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=64)
    lines = ["Invoice number 48213 for the harbour office", "Total payable seven hundred dollars", "Balance carried forward from last month", "Signed by the authorised officer today"]
    for i, line in enumerate(lines):
        draw.text((120, 300 + i * 200), line, font=font, fill=0)
    buf = io.BytesIO()
    img.rotate(90, expand=True).save(buf, "PDF", resolution=200)
    return buf.getvalue()


# ── OCR ──────────────────────────────────────────────────────────────────────


def test_scanned_pdf_becomes_searchable_and_the_words_exist_only_in_the_ocr_layer() -> None:
    src = CORPUS["scanned"].data
    assert page_text_counts(src) == [0], "the forcing input has no text layer at all"
    out = ocr_pdf_bytes(src)
    assert set(SCAN_WORDS) <= _words(out.content), "pdfplumber finds the scanned words"
    assert all(w in _pdfium_text(out.content).lower() for w in SCAN_WORDS)
    assert out.metadata["pages_read"] == [1] and out.metadata["pages_still_empty"] == []
    # The page image is kept: the text is invisible, the page still looks like the scan.
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        assert len(pdf.pages[0].images) >= 1


def test_ocr_of_a_page_with_rotate_90_reads_the_words_and_keeps_the_rotation() -> None:
    """The U1 known limit: scanned pages with /Rotate 90 used to come out as garbage."""
    src = CORPUS["scanned_rotated"].data
    out = ocr_pdf_bytes(src)
    assert set(SCAN_WORDS) <= _words(out.content)
    assert all(w in _pdfium_text(out.content).lower() for w in SCAN_WORDS)
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        assert int(pdf.pages[0].obj.get("/Rotate", 0)) == 90, "the page looks as it did"


def test_a_scan_fed_sideways_with_no_rotate_flag_is_read_and_turned_upright() -> None:
    src = _sideways_native_scan()
    out = ocr_pdf_bytes(src)
    assert set(SCAN_WORDS) <= _words(out.content)
    assert out.metadata["pages_turned_upright"] == [1]
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        assert int(pdf.pages[0].obj.get("/Rotate", 0)) in (90, 270)


def test_text_layer_lines_up_with_the_scan_after_ocr() -> None:
    """The invisible word sits over dark ink of the image, on a page that carries /Rotate 90 (checked in the
    page's own unrotated frame, where the image and the text layer both live)."""
    out = ocr_pdf_bytes(CORPUS["scanned_rotated"].data).content
    doc = pdfium.PdfDocument(out)
    try:
        page = doc[0]
        page.set_rotation(0)
        image = page.render(scale=1).to_pil().convert("L")
        tp = page.get_textpage()
        text = tp.get_text_range().lower()
        start = text.index("invoice")
        boxes = [tp.get_charbox(i) for i in range(start, start + len("invoice"))]
        left, right = min(b[0] for b in boxes), max(b[2] for b in boxes)
        bottom, top = min(b[1] for b in boxes), max(b[3] for b in boxes)
        w, h = image.size
        crop = image.crop((max(0, int(left)), max(0, int(h - top)), min(w, int(right)), min(h, int(h - bottom))))
        assert crop.size[0] > 8 and crop.size[1] > 8
        dark = sum(1 for px in crop.getdata() if px < 110)
        assert dark / (crop.size[0] * crop.size[1]) > 0.08, "dark ink under the recognized word"
    finally:
        doc.close()


def test_skip_mode_leaves_pages_with_text_alone_and_reads_only_the_scan() -> None:
    out = ocr_pdf_bytes(CORPUS["mixed"].data)
    assert out.metadata["pages_read"] == [2] and out.metadata["pages_skipped"] == [1, 3]
    assert "marker-first" in _pdfium_text(out.content, 0)
    assert set(SCAN_WORDS) <= _words(out.content, 1)


def test_a_pdf_that_is_already_searchable_is_returned_unchanged() -> None:
    src = CORPUS["digital"].data
    out = ocr_pdf_bytes(src)
    assert out.metadata["already_searchable"] is True and out.metadata["pages_read"] == []


def test_ocr_refuses_a_page_that_does_not_exist_and_a_bad_language_code() -> None:
    with pytest.raises(ValueError, match="does not exist"):
        ocr_pdf_bytes(CORPUS["scanned"].data, pages=[4])
    with pytest.raises(ValueError, match="language"):
        ocr_pdf_bytes(CORPUS["scanned"].data, languages=["english; rm"])


# ── Convert ──────────────────────────────────────────────────────────────────


def _ruled_table_pdf() -> bytes:
    """A real ruled table (lines drawn), the kind a table finder reads."""
    pdf, font = _new_pdf()
    page = pdf.add_blank_page(page_size=(612, 792))
    page.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
    ops = ["BT /F1 18 Tf 72 740 Td (Quarterly report) Tj ET"]
    xs, ys = [72, 200, 330, 460], [700, 670, 640, 610]
    for x in xs:
        ops.append(f"{x} {ys[0]} m {x} {ys[-1]} l S")
    for y in ys:
        ops.append(f"{xs[0]} {y} m {xs[-1]} {y} l S")
    cells = [["Item", "Qty", "Price"], ["Widget", "4", "9.50"], ["Gadget", "12", "3.25"]]
    for r, row in enumerate(cells):
        for c, text in enumerate(row):
            ops.append(f"BT /F1 11 Tf {xs[c] + 6} {ys[r] - 20} Td ({text}) Tj ET")
    page.Contents = pdf.make_stream("\n".join(ops).encode())
    return _save(pdf)


def test_pdf_to_word_carries_the_text_and_the_table() -> None:
    docx = pytest.importorskip("docx")
    r = convert_pdf_bytes(_ruled_table_pdf(), target="docx")
    doc = docx.Document(io.BytesIO(r.content))
    assert any("Quarterly report" in p.text for p in doc.paragraphs)
    assert [c.text for c in doc.tables[0].rows[1].cells] == ["Widget", "4", "9.50"]
    assert "approximated" in r.metadata["limits"] or "Columns" in r.metadata["limits"]


def test_pdf_to_excel_makes_a_sheet_per_table_with_numbers_as_numbers() -> None:
    openpyxl = pytest.importorskip("openpyxl")
    r = convert_pdf_bytes(_ruled_table_pdf(), target="xlsx")
    ws = openpyxl.load_workbook(io.BytesIO(r.content))["p1-table1"]
    assert [c.value for c in ws[3]] == ["Gadget", 12, 3.25]


def test_pdf_with_no_tables_gives_one_text_sheet_and_says_so() -> None:
    openpyxl = pytest.importorskip("openpyxl")
    r = convert_pdf_bytes(CORPUS["digital"].data, target="xlsx")
    wb = openpyxl.load_workbook(io.BytesIO(r.content))
    assert wb.sheetnames == ["Text"] and r.metadata["no_tables_found"] is True


def test_pdf_to_powerpoint_is_one_slide_per_page_with_the_text() -> None:
    pptx = pytest.importorskip("pptx")
    r = convert_pdf_bytes(CORPUS["digital"].data, target="pptx")
    prs = pptx.Presentation(io.BytesIO(r.content))
    assert len(prs.slides) == 2
    texts = " ".join(s.text_frame.text for s in prs.slides[0].shapes if s.has_text_frame)
    assert "marker-1" in texts


def test_a_scanned_page_is_listed_as_having_no_text_to_carry() -> None:
    r = convert_pdf_bytes(CORPUS["scanned"].data, target="docx")
    assert r.metadata["pages_without_text"] == [1]


def test_convert_refuses_an_unknown_target() -> None:
    with pytest.raises(ValueError):
        convert_pdf_bytes(CORPUS["digital"].data, target="doc")


# ── Compare ──────────────────────────────────────────────────────────────────


def test_compare_lists_a_planted_edit_in_the_text_and_boxes_it_on_the_page() -> None:
    a = CORPUS["digital"].data
    b = replace_pdf_bytes(a, find="tenant", replace="lessee").content
    result = compare_pdf_bytes(a, b)
    assert result["changed_pages"] == [1] and result["identical"] is False
    page1, page2 = result["pages"]
    assert page2["status"] == "same"
    change = page1["text_changes"][0]
    assert change["op"] == "replace" and change["before"] == "tenant" and change["after"] == "lessee"
    assert page1["regions"], "the changed sentence is boxed"
    box = page1["regions"][0]
    assert 0 <= box["x"] < 1 and 0 <= box["y"] < 1 and box["width"] > 0 and box["height"] > 0


def test_compare_of_a_file_with_itself_is_identical_and_a_missing_page_is_removed() -> None:
    a = CORPUS["digital"].data
    assert compare_pdf_bytes(a, a)["identical"] is True
    with pikepdf.open(io.BytesIO(a)) as pdf:
        del pdf.pages[1]
        out = io.BytesIO()
        pdf.save(out)
    result = compare_pdf_bytes(a, out.getvalue())
    assert result["pages"][1]["status"] == "removed" and result["identical"] is False


def test_text_changes_are_word_level() -> None:
    assert text_changes("a b c".split(), "a x c d".split()) == [
        {"op": "replace", "before": "b", "after": "x"},
        {"op": "insert", "before": "", "after": "d"},
    ]


# ── Find and replace ─────────────────────────────────────────────────────────


def test_preview_shows_the_line_before_and_after_and_writes_nothing() -> None:
    src = CORPUS["digital"].data
    pv = find_replace_preview(src, find="rent", replace="fees")
    row = pv["rows"][0]
    assert row["replaceable"] and "rent" in row["before"] and "fees" in row["after"]
    assert pv["found_in_text"] == pv["replaceable"] >= 1 and "re-set" in pv["label"]


def test_replace_changes_the_text_in_the_file_and_only_where_asked() -> None:
    src = CORPUS["digital"].data
    out = replace_pdf_bytes(src, find="tenant", replace="lessee", pages=[1])
    assert "lessee" in _pdfium_text(out.content, 0) and "tenant" not in _pdfium_text(out.content, 0)
    assert _pdfium_text(out.content, 1) == _pdfium_text(src, 1), "page 2 is untouched"
    assert out.metadata["label"] == "Text re-set"


def test_replace_is_refused_on_a_scan_until_ocr_has_run_then_works() -> None:
    scan = CORPUS["scanned"].data
    with pytest.raises(ValueError, match="Recognize text"):
        replace_pdf_bytes(scan, find="invoice", replace="bill")
    searchable = ocr_pdf_bytes(scan).content
    pv = find_replace_preview(searchable, find="invoice", replace="bill")
    assert pv["found_in_text"] >= 1


def test_a_character_the_font_cannot_show_is_listed_not_replaced() -> None:
    src = CORPUS["digital"].data
    pv = find_replace_preview(src, find="tenant", replace="租户")
    assert pv["replaceable"] == 0 and pv["not_replaceable"] == 1
    assert "cannot show" in pv["rows"][0]["reason"]
    with pytest.raises(ValueError, match="Nothing could be replaced"):
        replace_pdf_bytes(src, find="tenant", replace="租户")


def test_a_match_that_is_not_there_is_an_honest_error() -> None:
    with pytest.raises(ValueError, match="Nothing could be replaced"):
        replace_pdf_bytes(CORPUS["digital"].data, find="zebra", replace="giraffe")
