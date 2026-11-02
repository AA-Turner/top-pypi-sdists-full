"""Crop treats the box as the rectangle the person sees (rotation applied)."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

from matrx_files.specific_handlers.pdf.handler import PDFHandler
from matrx_files.specific_handlers.pdf.models import PdfCropBox


def _rotated_pdf(rotation: int) -> bytes:
    output = BytesIO()
    page = canvas.Canvas(output, pagesize=(612, 792))
    page.setFont("Helvetica", 12)
    page.drawString(400, 792 - 700, "BOTTOMRIGHT")
    page.drawString(50, 792 - 100, "TOPLEFT")
    page.showPage()
    page.save()

    reader = PdfReader(BytesIO(output.getvalue()))
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.pages[0].rotate(rotation)
    result = BytesIO()
    writer.write(result)
    return result.getvalue()


def _crop(rotation: int, box: PdfCropBox) -> bytes:
    handler = PDFHandler(app_name="test_pdf_crop_rotated")
    return handler.crop_pages_in_bytes(_rotated_pdf(rotation), crop_box=box, pages=[1]).content


def _text(data: bytes) -> str:
    pages = PDFHandler(app_name="test_pdf_crop_rotated").extract_text_pages_from_bytes(
        data, use_ocr_threshold=0
    )
    return "\n".join(page.text for page in pages)


def test_crop_whole_rotated_page_with_margins_succeeds() -> None:
    # A 90-degree page is 792x612 in visual space; 50pt margins leave 692x512.
    cropped = _crop(90, PdfCropBox(x0=50, y0=50, x1=742, y1=562))
    page = PdfReader(BytesIO(cropped)).pages[0]
    assert page.get("/Rotate", 0) == 90
    assert round(float(page.cropbox.height)) == 692
    assert round(float(page.cropbox.width)) == 512


def test_crop_keeps_the_text_inside_the_visual_box_on_every_rotation() -> None:
    # The two known text anchors switch visual corners under page rotation. The margin
    # box is deliberately drawn around the transformed BOTTOMRIGHT anchor only.
    boxes = {
        90: PdfCropBox(x0=80, y0=380, x1=120, y1=490),
        180: PdfCropBox(x0=120, y0=80, x1=220, y1=120),
        270: PdfCropBox(x0=680, y0=120, x1=720, y1=230),
    }
    for rotation, box in boxes.items():
        text = _text(_crop(rotation, box))
        assert "BOTTOMRIGHT" in text, rotation
        assert "TOPLEFT" not in text, rotation


def _a4_pdf(rotation: int = 0) -> bytes:
    output = BytesIO()
    page = canvas.Canvas(output, pagesize=(595.275590551181, 841.8897637795275))
    page.drawString(50, 700, "A4")
    page.showPage()
    page.save()
    if not rotation:
        return output.getvalue()
    writer = PdfWriter()
    writer.append_pages_from_reader(PdfReader(BytesIO(output.getvalue())))
    writer.pages[0].rotate(rotation)
    result = BytesIO()
    writer.write(result)
    return result.getvalue()


def test_crop_edge_rounded_up_by_the_client_is_the_page_edge() -> None:
    # Live defect: the client sent x1=595.2756 / y1=841.8898 against a page of
    # 595.27557 / 841.88977 and every crop failed with a 422.
    handler = PDFHandler(app_name="test_pdf_crop_edge")
    for rotation, box in (
        (0, PdfCropBox(x0=0, y0=5, x1=595.2756, y1=841.8898)),
        (90, PdfCropBox(x0=0, y0=5, x1=841.8898, y1=595.2756)),
    ):
        cropped = handler.crop_pages_in_bytes(_a4_pdf(rotation), crop_box=box, pages=[1]).content
        assert PdfReader(BytesIO(cropped)).pages[0].cropbox.height > 0


def test_crop_box_really_outside_the_page_is_still_refused() -> None:
    import pytest

    handler = PDFHandler(app_name="test_pdf_crop_edge")
    with pytest.raises(ValueError, match="outside page 1"):
        handler.crop_pages_in_bytes(
            _a4_pdf(), crop_box=PdfCropBox(x0=0, y0=0, x1=600, y1=800), pages=[1]
        )
