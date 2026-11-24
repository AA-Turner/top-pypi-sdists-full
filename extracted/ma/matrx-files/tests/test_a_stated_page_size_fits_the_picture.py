"""A page size the person picked fits the picture into it, never stretches it, never refuses the save.

SUT: ``build_scan_pdf`` (the one place a scan page's geometry is decided). A stated page size whose
shape differs from the picture's (A4 asked for a Letter-shaped page, Letter for a long receipt) gets
the page exactly as asked, with the WHOLE picture on it at its own proportions, centred, the rest of
the page white — as a reference scanner app does when a document size is picked.

Breaks caught: the save refused for shape (the live refusal of request f168fe49, 2026-11-19: "page
size 595.28 x 841.89 pt does not have the picture's shape (259 x 374 px); it would be stretched");
the picture stretched to the page; the picture cropped or off-centre; a page size that is no size
(under 36 pt, over the PDF format's 14,400 pt) no longer refused in plain words.
"""

from __future__ import annotations

import io

import pdfplumber
import pytest
from PIL import Image

from matrx_files.specific_handlers.pdf.images_to_pdf import ScanPdfInputItem, build_scan_pdf

A4 = (595.28, 841.89)
LETTER = (612.0, 792.0)


def _jpeg(width: int, height: int) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (width, height), (200, 30, 30)).save(buf, "JPEG", quality=90)
    return buf.getvalue()


def _page_and_picture(pdf: bytes) -> tuple[tuple[float, float], tuple[float, float, float, float]]:
    with pdfplumber.open(io.BytesIO(pdf)) as doc:
        page = doc.pages[0]
        (info,) = page.images
        return (float(page.width), float(page.height)), (info["x0"], info["top"], info["x1"], info["bottom"])


@pytest.mark.parametrize(
    ("picture", "size", "box"),
    [
        # The live refusal: a nearly-A4 picture asked for as A4 -> height fills, thin white sides.
        ((259, 374), A4, (6.13, 0.0, 589.15, 841.89)),
        # A Letter-shaped page asked for as A4 -> width fills, white above and below.
        ((1275, 1650), A4, (0.0, 35.76, 595.28, 806.13)),
        # A long receipt asked for as Letter -> height fills, wide white sides.
        ((600, 2400), LETTER, (207.0, 0.0, 405.0, 792.0)),
        # A portrait page asked for as landscape A4 -> fits, never turned or stretched.
        ((1240, 1754), (A4[1], A4[0]), (210.53, 0.0, 631.36, 595.28)),
    ],
)
def test_the_picture_fits_the_page_asked_for_whole_unstretched_and_centred(picture, size, box) -> None:
    w, h = picture
    pdf, pages = build_scan_pdf([ScanPdfInputItem(raw_bytes=_jpeg(w, h), page_size_pt=size, label="page-1")])
    assert pages == 1
    (page_w, page_h), drawn = _page_and_picture(pdf)
    assert (round(page_w, 2), round(page_h, 2)) == (round(size[0], 2), round(size[1], 2)), "the page is the size asked for"
    assert drawn == pytest.approx(box, abs=0.05), "whole picture, centred"
    x0, y0, x1, y1 = drawn
    assert (x1 - x0) / (y1 - y0) == pytest.approx(w / h, rel=1e-3), "the picture keeps its proportions"
    assert x0 >= -0.01 and y0 >= -0.01 and x1 <= page_w + 0.01 and y1 <= page_h + 0.01, "nothing is cut off"


def test_the_build_says_where_each_picture_sits_on_its_page() -> None:
    from matrx_files.specific_handlers.pdf.images_to_pdf import assemble_scan_pdf

    built = assemble_scan_pdf([
        ScanPdfInputItem(raw_bytes=_jpeg(600, 2400), page_size_pt=LETTER, label="receipt"),
        ScanPdfInputItem(raw_bytes=_jpeg(1240, 1754), label="automatic"),
    ])
    assert built.page_count == 2
    assert built.picture_boxes[1] == pytest.approx((207.0 / 612.0, 0.0, 405.0 / 612.0, 1.0), abs=1e-4)
    assert built.picture_boxes[2] is None, "an Automatic page is the picture's own shape: it fills the page"


def test_a_page_of_nearly_the_pictures_shape_gets_a_sliver_never_a_squash() -> None:
    from matrx_files.specific_handlers.pdf.images_to_pdf import assemble_scan_pdf

    built = assemble_scan_pdf([ScanPdfInputItem(raw_bytes=_jpeg(1240, 1754), page_size_pt=A4, label="page-1")])
    (page_w, page_h), drawn = _page_and_picture(built.pdf_bytes)
    x0, y0, x1, y1 = drawn
    assert (x1 - x0) / (y1 - y0) == pytest.approx(1240 / 1754, rel=1e-4), "never squashed to the page"
    assert drawn == pytest.approx((0.0, 0.0, page_w, page_h), abs=0.1), "a sliver, not a margin"
    box = built.picture_boxes[1]
    assert box is not None and (box[0] * page_w, box[2] * page_w) == pytest.approx((x0, x1), abs=0.01), (
        "the build says exactly where the picture is, so a text layer sits on it"
    )


@pytest.mark.parametrize(
    ("size", "why"),
    [((10.0, 14.14), "under 36 pt"), ((0.0, 0.0), "under 36 pt"), ((-595.0, 842.0), "under 36 pt"),
     ((20000.0, 842.0), "over 14400 pt")],
)
def test_a_page_size_that_is_no_size_is_still_refused_in_plain_words(size, why: str) -> None:
    with pytest.raises(ValueError, match=why):
        build_scan_pdf([ScanPdfInputItem(raw_bytes=_jpeg(1240, 1754), page_size_pt=size, label="page-1")])
