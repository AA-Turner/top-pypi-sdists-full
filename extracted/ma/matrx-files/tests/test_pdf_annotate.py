"""Markup the browser editors cannot write (underline, strike-out, shapes, sticky note, links), written
by pikepdf and read back the way OTHER viewers read them: pypdf's annotation reading for the
dictionaries, pdfium (Chrome's engine) for what is drawn. No PyMuPDF.
"""

from __future__ import annotations

import io
from datetime import UTC, datetime

import pytest

pikepdf = pytest.importorskip("pikepdf")
pypdf = pytest.importorskip("pypdf")
pdfium = pytest.importorskip("pypdfium2")

from matrx_files.specific_handlers.pdf.ops.annotate import apply_annotation_ops, arrow_head  # noqa: E402


def _blank(pages: int = 2) -> bytes:
    pdf = pikepdf.new()
    for _ in range(pages):
        pdf.add_blank_page(page_size=(612, 792))
    out = io.BytesIO()
    pdf.save(out)
    return out.getvalue()


def _annots(data: bytes, page: int = 0) -> list[dict]:
    reader = pypdf.PdfReader(io.BytesIO(data))
    return [a.get_object() for a in (reader.pages[page].get("/Annots") or [])]


def _red_pixels(data: bytes, page: int = 0) -> int:
    doc = pdfium.PdfDocument(data)
    try:
        img = doc[page].render(scale=1, may_draw_forms=True).to_pil().convert("RGB")
    finally:
        doc.close()
    return sum(1 for r, g, b in img.get_flattened_data() if r > 200 and g < 120 and b < 120)


NOW = datetime(2026, 10, 30, 12, 0, tzinfo=UTC)
RED = "#ff2020"
QUAD = [100, 700, 300, 700, 100, 686, 300, 686]


def test_every_kind_is_written_with_an_appearance_other_viewers_read():
    ops = [
        {"op": "add", "page": 1, "kind": "underline", "quads": [QUAD], "color": RED},
        {"op": "add", "page": 1, "kind": "strikeout", "quads": [QUAD], "color": RED},
        {"op": "add", "page": 1, "kind": "square", "rect": [100, 400, 250, 500], "color": RED, "width": 3},
        {"op": "add", "page": 1, "kind": "circle", "rect": [300, 400, 450, 500], "color": RED, "width": 3},
        {"op": "add", "page": 1, "kind": "line", "points": [100, 300, 300, 300], "color": RED, "width": 2},
        {"op": "add", "page": 1, "kind": "arrow", "points": [100, 250, 300, 200], "color": RED, "width": 2},
        {"op": "add", "page": 1, "kind": "note", "rect": [500, 700, 520, 720], "color": "#ffd400", "contents": "Check this", "author": "Pat Tester"},
        {"op": "add", "page": 1, "kind": "link", "rect": [100, 100, 200, 130], "url": "example.com/a"},
        {"op": "add", "page": 1, "kind": "link", "rect": [300, 100, 400, 130], "dest_page": 2},
    ]
    out = apply_annotation_ops(_blank(), ops, now=NOW)
    annots = _annots(out)
    subtypes = [str(a["/Subtype"]) for a in annots]
    assert subtypes == ["/Underline", "/StrikeOut", "/Square", "/Circle", "/Line", "/Line", "/Text", "/Popup", "/Link", "/Link"]
    for a in annots:
        if a["/Subtype"] not in ("/Link", "/Popup"):
            assert "/N" in a["/AP"], a["/Subtype"]
    assert list(map(float, annots[0]["/QuadPoints"])) == QUAD
    assert [str(x) for x in annots[5]["/LE"]] == ["/None", "/OpenArrow"]
    note, popup = annots[6], annots[7]
    assert note["/Contents"] == "Check this" and note["/T"] == "Pat Tester"
    assert note["/M"] == "D:20261030120000Z"
    assert note["/Popup"].get_object()["/Subtype"] == "/Popup"
    assert popup["/Parent"].get_object()["/Contents"] == "Check this"
    assert annots[8]["/A"]["/URI"] == "https://example.com/a"
    reader = pypdf.PdfReader(io.BytesIO(out))
    assert reader.get_page_number(reader.pages[0]["/Annots"][9].get_object()["/Dest"][0].get_object()) == 1
    # Drawn by pdfium (Chrome's PDF engine) from the appearance streams alone.
    assert _red_pixels(out) > 1500


def test_saved_note_is_edited_and_a_saved_mark_deleted_by_reference():
    first = apply_annotation_ops(
        _blank(),
        [
            {"op": "add", "page": 1, "kind": "note", "rect": [50, 700, 70, 720], "contents": "old"},
            {"op": "add", "page": 1, "kind": "square", "rect": [100, 100, 200, 200]},
        ],
        now=NOW,
    )
    with pikepdf.open(io.BytesIO(first)) as pdf:
        refs = {str(a.Subtype): f"{a.objgen[0]}R" for a in pdf.pages[0].Annots}
    second = apply_annotation_ops(
        first,
        [{"op": "update", "ref": refs["/Text"], "contents": "new text"}, {"op": "delete", "ref": refs["/Square"]}],
        now=NOW,
    )
    subtypes = [str(a["/Subtype"]) for a in _annots(second)]
    assert subtypes == ["/Text", "/Popup"]
    assert _annots(second)[0]["/Contents"] == "new text"
    third = apply_annotation_ops(second, [{"op": "delete", "ref": refs["/Text"]}], now=NOW)
    assert _annots(third) == []  # the note's popup goes with it


def test_plain_refusals():
    with pytest.raises(ValueError, match="no page 3"):
        apply_annotation_ops(_blank(), [{"op": "add", "page": 3, "kind": "square", "rect": [0, 0, 10, 10]}])
    with pytest.raises(ValueError, match="web address or a page"):
        apply_annotation_ops(_blank(), [{"op": "add", "page": 1, "kind": "link", "rect": [0, 0, 50, 50]}])
    with pytest.raises(ValueError, match="not in this file|not on any page"):
        apply_annotation_ops(_blank(), [{"op": "delete", "ref": "999R"}])
    with pytest.raises(ValueError, match="selected text"):
        apply_annotation_ops(_blank(), [{"op": "add", "page": 1, "kind": "underline", "quads": [[None] * 8]}])
    assert apply_annotation_ops(b"untouched", []) == b"untouched"


def test_arrow_head_points_back_along_the_line():
    (ax, ay), (bx, by) = arrow_head(0, 0, 100, 0, 2)
    assert ax < 100 and bx < 100 and ay == pytest.approx(-by)
