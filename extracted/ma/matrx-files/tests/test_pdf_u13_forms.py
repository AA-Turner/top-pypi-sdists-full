"""PDF-PLAN U13 forcing tests: filled values read back from the file, a flattened form has no fields left, and a
placed signature is present. pikepdf / PyPDFForm / pdfplumber / pypdfium2 only."""

from __future__ import annotations

import base64
import io

import pytest

pikepdf = pytest.importorskip("pikepdf")
pytest.importorskip("PyPDFForm")
pdfplumber = pytest.importorskip("pdfplumber")
pdfium = pytest.importorskip("pypdfium2")
from PIL import Image, ImageDraw  # noqa: E402

from _pdf_corpus import build_corpus  # noqa: E402
from _pdf_forms_fixture import build_form  # noqa: E402

from matrx_files.specific_handlers.pdf.ops.forms import (  # noqa: E402
    fill_form_bytes,
    flatten_form_bytes,
    list_form_fields_bytes,
    list_marks_bytes,
    place_marks_bytes,
    read_form_values_bytes,
)

FORM = build_form()
FILL = {"full_name": "Ada Lovelace", "signed_date": "10/29/2026", "agree": True, "size": "Large", "country": "USA"}


def _page_text(data: bytes) -> str:
    with pdfplumber.open(io.BytesIO(data)) as d:
        return d.pages[0].extract_text() or ""


def test_fields_are_detected_with_type_options_and_a_box_on_the_visible_page() -> None:
    found = list_form_fields_bytes(FORM)
    by = {f["name"]: f for f in found["fields"]}
    assert found["has_form"] and set(by) == {"full_name", "signed_date", "agree", "size", "country"}
    assert by["full_name"]["type"] == "text" and by["signed_date"]["type"] == "date"
    assert by["agree"]["type"] == "checkbox" and by["size"]["type"] == "radio" and by["size"]["options"] == ["Small", "Large"]
    assert by["country"]["type"] == "dropdown" and by["country"]["options"] == ["Canada", "Mexico", "USA"]
    r = by["full_name"]["rect"]
    assert (r["x0"], r["x1"]) == (150, 400) and 70 < r["y0"] < 110  # y flipped: 792 - 710 = 82
    assert by["full_name"]["page_number"] == 1


def test_filled_values_read_back_from_the_file_by_pypdfform_and_pikepdf() -> None:
    out = fill_form_bytes(FORM, FILL)
    assert out.operation == "fill-form" and out.metadata["flattened"] is False
    data = read_form_values_bytes(out.content)
    assert data["full_name"] == "Ada Lovelace" and data["signed_date"] == "10/29/2026"
    assert data["agree"] is True and data["size"] == 1 and data["country"] == 2
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        values = {str(f.T): f.get("/V") for f in pdf.Root.AcroForm.Fields}
    assert str(values["full_name"]) == "Ada Lovelace" and str(values["agree"]) == "/Yes" and str(values["country"]) == "USA"
    again = {f["name"]: f["value"] for f in list_form_fields_bytes(out.content)["fields"]}
    assert again["size"] == "Large" and again["agree"] == "Yes"


def test_flatten_leaves_no_fields_and_the_values_stay_visible() -> None:
    out = fill_form_bytes(FORM, FILL, flatten=True)
    assert out.metadata["fields_flattened"] == 5
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        assert "/AcroForm" not in pdf.Root
        assert not (pdf.pages[0].get("/Annots") or [])
    assert list_form_fields_bytes(out.content)["has_form"] is False
    text = _page_text(out.content)
    assert "Ada Lovelace" in text and "10/29/2026" in text and "USA" in text
    # flatten on request alone, from a form filled earlier
    filled = fill_form_bytes(FORM, FILL).content
    flat = flatten_form_bytes(filled)
    assert "Ada Lovelace" in _page_text(flat.content) and not list_form_fields_bytes(flat.content)["has_form"]


def test_bad_values_are_plain_errors_not_silent_skips() -> None:
    with pytest.raises(ValueError, match="not in the form"):
        fill_form_bytes(FORM, {"nope": "x"})
    with pytest.raises(ValueError, match="not a choice"):
        fill_form_bytes(FORM, {"country": "Atlantis"})
    with pytest.raises(ValueError, match="no fillable form"):
        fill_form_bytes(build_corpus()["digital"].data, {"a": "b"})
    with pytest.raises(ValueError):
        flatten_form_bytes(build_corpus()["digital"].data)


def _signature_png() -> str:
    img = Image.new("RGBA", (300, 100), (0, 0, 0, 0))
    ImageDraw.Draw(img).line([(10, 80), (100, 10), (150, 80), (290, 20)], fill=(0, 0, 160, 255), width=6)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def test_placed_text_date_check_and_signature_are_present_and_read_back() -> None:
    src = build_corpus()["digital"].data
    marks = [
        {"kind": "text", "page_number": 1, "x": 100, "y": 300, "width": 200, "height": 20, "text": "Ada Lovelace"},
        {"kind": "date", "page_number": 1, "x": 100, "y": 340, "width": 120, "height": 20, "text": "10/29/2026"},
        {"kind": "check", "page_number": 1, "x": 100, "y": 380, "width": 16, "height": 16},
        {"kind": "signature", "page_number": 2, "x": 120, "y": 500, "width": 180, "height": 60, "image": _signature_png()},
    ]
    out = place_marks_bytes(src, marks)
    assert out.metadata["marks"] == 4 and out.page_count == 2
    read_back = list_marks_bytes(out.content)
    assert sorted((m["page_number"], m["kind"]) for m in read_back) == [(1, "check"), (1, "date"), (1, "text"), (2, "signature")]
    text = _page_text(out.content)
    assert "Ada Lovelace" in text and "10/29/2026" in text and "Lease agreement clause marker-1" in text
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        sig = [x for x in pdf.pages[1].Resources.XObject.values() if "/MatrxMark" in x][0]
        assert sig.Resources.XObject.Sig.Subtype == "/Image"
    # the signature is really drawn where it was placed (blue ink inside the box, none outside)
    doc = pdfium.PdfDocument(out.content)
    try:
        img = doc[1].render(scale=1).to_pil().convert("RGB")
    finally:
        doc.close()
    inside = img.crop((120, 500, 300, 560))
    assert any(b > 120 and r < 60 for r, g, b in inside.getdata())
    assert not any(b > 120 and r < 60 for r, g, b in img.crop((0, 0, 100, 450)).getdata())


def test_marks_land_in_the_right_place_on_a_rotated_page_and_errors_are_plain() -> None:
    rot = build_corpus()["rotated"].data
    out = place_marks_bytes(rot, [{"kind": "check", "page_number": 2, "x": 50, "y": 60, "width": 30, "height": 30}])
    doc = pdfium.PdfDocument(out.content)
    try:
        img = doc[1].render(scale=1).to_pil().convert("L")  # displayed page (rotated 90)
    finally:
        doc.close()
    ink = img.crop((50, 60, 80, 90)).point(lambda v: 255 if v < 128 else 0).getbbox()
    assert ink is not None
    with pytest.raises(ValueError):
        place_marks_bytes(rot, [{"kind": "check", "page_number": 9, "x": 1, "y": 1, "width": 5, "height": 5}])
    with pytest.raises(ValueError):
        place_marks_bytes(rot, [])
    with pytest.raises(ValueError):
        place_marks_bytes(rot, [{"kind": "signature", "page_number": 1, "x": 1, "y": 1, "width": 50, "height": 20, "image": "!!!"}])
