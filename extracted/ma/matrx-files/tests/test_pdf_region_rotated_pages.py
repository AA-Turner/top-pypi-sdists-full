"""Drawn regions (annotate, snap, preview) are in the VISUAL page space - the rotated page the person sees."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from matrx_files.specific_handlers.pdf.extract.bbox import extract_at_bbox, snap_to_text_blocks


def _pdf(rotation: int) -> bytes:
    output = BytesIO()
    page = canvas.Canvas(output, pagesize=(612, 792))
    page.setFont("Helvetica", 12)
    page.drawString(400, 792 - 700, "BOTTOMRIGHT")
    page.drawString(50, 792 - 100, "TOPLEFT")
    page.showPage()
    page.save()
    writer = PdfWriter()
    writer.append_pages_from_reader(PdfReader(BytesIO(output.getvalue())))
    writer.pages[0].rotate(rotation)
    result = BytesIO()
    writer.write(result)
    return result.getvalue()


def _visual_box_of(data: bytes, word: str) -> dict[str, float]:
    # Helvetica 12pt anchors are known from the fixture: text starts at x=400,
    # baseline y=700 in the original top-origin page coordinates. Transform that
    # known rectangle into displayed top-left coordinates for each /Rotate value.
    assert word == "BOTTOMRIGHT"
    text_width = stringWidth("BOTTOMRIGHT", "Helvetica", 12)
    left, right = 400.0, 400.0 + text_width
    # ReportLab's baseline is 92pt from the bottom; convert it to the extractor's
    # top-origin page space and include Helvetica's ascender/descender bounds.
    top, bottom = 792.0 - 92.0 - 10.0, 792.0 - 92.0 + 2.5
    rotation = PdfReader(BytesIO(data)).pages[0].get("/Rotate", 0) % 360
    if rotation == 90:
        left, right, top, bottom = 792 - bottom, 792 - top, left, right
    elif rotation == 180:
        left, right, top, bottom = 612 - right, 612 - left, 792 - bottom, 792 - top
    elif rotation == 270:
        left, right, top, bottom = top, bottom, 612 - right, 612 - left
    return {"x0": left - 3, "y0": top - 3, "x1": right + 3, "y1": bottom + 3}


def test_text_and_preview_over_a_rotated_page_find_the_text_under_the_box() -> None:
    for rotation in (0, 90, 180, 270):
        data = _pdf(rotation)
        res = extract_at_bbox(
            data, page_number=1, bbox=_visual_box_of(data, "BOTTOMRIGHT"), ocr_fallback=False
        )
        assert "BOTTOMRIGHT" in res.extracted_text, rotation
        assert "TOPLEFT" not in res.extracted_text, rotation
        assert res.preview_png_base64, rotation


def test_snap_over_a_rotated_page_hugs_the_word_in_visual_space() -> None:
    for rotation in (90, 180, 270):
        data = _pdf(rotation)
        drawn = _visual_box_of(data, "BOTTOMRIGHT")
        snapped = snap_to_text_blocks(data, page_number=1, bbox=drawn, expand_pad_pt=0)
        # Snapping tightens inside the drawn box (it does not jump to another corner).
        assert drawn["x0"] < snapped.x0 and snapped.x1 < drawn["x1"], rotation
        assert drawn["y0"] < snapped.y0 and snapped.y1 < drawn["y1"], rotation
