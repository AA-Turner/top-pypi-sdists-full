"""PDF-PLAN U12 forcing tests: after redaction the content is GONE from the file, proven by reading the output
with pdfplumber, pypdfium2 and pikepdf (never PyMuPDF). Built on the synthetic corpus helpers."""

from __future__ import annotations

import io

import pytest

pikepdf = pytest.importorskip("pikepdf")
pdfium = pytest.importorskip("pypdfium2")
pdfplumber = pytest.importorskip("pdfplumber")
PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

from _pdf_corpus import PAGE_H, PAGE_W, _add_text_page, _new_pdf, _save  # noqa: E402

from matrx_files.specific_handlers.pdf.ops.redact_real import (  # noqa: E402
    RedactBox,
    find_redaction_hits_bytes,
    redact_pdf_bytes,
    sanitize_report_bytes,
)

SSN = "123-45-6789"


def _doc(rotate: int = 0, extra=None) -> bytes:
    pdf, font = _new_pdf()
    page = _add_text_page(
        pdf, font,
        [(72, 700, f"Applicant social security number {SSN} on file."), (72, 660, "Second line stays untouched.")],
        rotate=rotate,
    )
    if extra:
        extra(pdf, page)
    return _save(pdf)


def _text_pdfium(data: bytes, page: int = 0) -> str:
    doc = pdfium.PdfDocument(data)
    try:
        return doc[page].get_textpage().get_text_range()
    finally:
        doc.close()


def _text_plumber(data: bytes, page: int = 0) -> str:
    with pdfplumber.open(io.BytesIO(data)) as d:
        return d.pages[page].extract_text() or ""


def _hit_boxes(data: bytes) -> list[RedactBox]:
    found = find_redaction_hits_bytes(data, {"pii": True})
    return [RedactBox(page_number=h["page_number"], x0=h["x0"], y0=h["y0"], x1=h["x1"], y1=h["y1"]) for h in found["hits"] if h["text"] == SSN]


@pytest.mark.parametrize("rotate", [0, 90, 180, 270])
def test_pattern_found_and_text_really_gone_on_every_rotation(rotate: int) -> None:
    data = _doc(rotate)
    boxes = _hit_boxes(data)
    assert len(boxes) == 1
    result = redact_pdf_bytes(data, boxes)
    assert result.metadata["tier"] == "stream_rewrite", result.metadata
    out = result.content
    for text in (_text_pdfium(out), _text_plumber(out)):
        flat = "".join(text.split())
        assert SSN not in text and "6789" not in text and "123" not in flat
        for kept in ("Secondlinestaysuntouched", "Applicantsocialsecuritynumber"):
            assert kept in flat or kept[::-1] in flat
    # nothing of the string survives anywhere in the raw bytes either (uncompressed streams are searched too)
    assert SSN.encode() not in out and b"6789" not in out


def test_copy_paste_of_the_area_is_empty() -> None:
    data = _doc()
    box = _hit_boxes(data)[0]
    out = redact_pdf_bytes(data, [box]).content
    with pdfplumber.open(io.BytesIO(out)) as d:
        p = d.pages[0]
        assert (p.crop((box.x0 - 1, box.y0 - 1, box.x1 + 1, box.y1 + 1)).extract_text() or "").strip() == ""
    doc = pdfium.PdfDocument(out)
    try:
        tp = doc[0].get_textpage()
        assert tp.get_text_bounded(left=box.x0, bottom=PAGE_H - box.y1, right=box.x1, top=PAGE_H - box.y0).strip() == ""
    finally:
        doc.close()


def test_drawn_region_over_plain_words_and_audit_metadata_carries_no_content() -> None:
    data = _doc()
    with pdfplumber.open(io.BytesIO(data)) as d:
        w = [w for w in d.pages[0].extract_words() if w["text"] == "Second"][0]
    result = redact_pdf_bytes(data, [RedactBox(page_number=1, x0=w["x0"] - 1, y0=w["top"] - 1, x1=w["x1"] + 1, y1=w["bottom"] + 1)])
    assert "Second" not in _text_plumber(result.content) and "line stays untouched" in _text_plumber(result.content)
    assert result.metadata["glyphs_removed"] == len("Second")
    assert "Second" not in repr(result.metadata)


def test_image_pixels_under_the_box_are_blank_and_other_pixels_survive() -> None:
    def add_image(pdf, page):
        img = Image.new("RGB", (100, 100), (250, 10, 10))
        stream = pdf.make_stream(img.tobytes())
        stream.Type, stream.Subtype = pikepdf.Name.XObject, pikepdf.Name.Image
        stream.Width = stream.Height = 100
        stream.ColorSpace, stream.BitsPerComponent = pikepdf.Name.DeviceRGB, 8
        page.Resources.XObject = pikepdf.Dictionary(Im1=stream)
        page.Contents = pdf.make_stream(bytes(page.Contents.read_bytes()) + b"\nq 200 0 0 200 100 300 cm /Im1 Do Q\n")

    data = _doc(extra=add_image)
    # image occupies x 100..300, y(up) 300..500 -> top-left y 292..492; cover its right-hand half
    box = RedactBox(page_number=1, x0=200, y0=292, x1=300, y1=492)
    result = redact_pdf_bytes(data, [box])
    assert result.metadata["images_blanked"] == 1 and result.metadata["tier"] == "stream_rewrite"
    with pikepdf.open(io.BytesIO(result.content)) as pdf:
        imgs = [pikepdf.PdfImage(x).as_pil_image() for x in pdf.pages[0].Resources.XObject.values() if x.get("/Subtype") == "/Image"]
    blanked = [im for im in imgs if im.getpixel((75, 50)) == (0, 0, 0)]
    assert blanked and blanked[0].getpixel((10, 50)) == (250, 10, 10)
    # the original, unredacted pixel colour is nowhere under the box
    assert all(im.getpixel((99, 50)) != (250, 10, 10) for im in blanked)


def test_text_inside_a_form_xobject_is_cut_without_touching_the_shared_form() -> None:
    def add_form(pdf, page):
        form = pdf.make_stream(b"BT /F1 12 Tf 72 560 Td (Account 457-55-5462 in a form) Tj ET")
        form.Type, form.Subtype = pikepdf.Name.XObject, pikepdf.Name.Form
        form.BBox = [0, 0, PAGE_W, PAGE_H]
        form.Resources = pikepdf.Dictionary(Font=page.Resources.Font)
        page.Resources.XObject = pikepdf.Dictionary(Fm1=form)
        page.Contents = pdf.make_stream(bytes(page.Contents.read_bytes()) + b"\n/Fm1 Do\n")

    data = _doc(extra=add_form)
    found = find_redaction_hits_bytes(data, {"pii": True})
    hit = [h for h in found["hits"] if h["text"] == "457-55-5462"]
    assert hit, found
    h = hit[0]
    result = redact_pdf_bytes(data, [RedactBox(page_number=1, x0=h["x0"], y0=h["y0"], x1=h["x1"], y1=h["y1"])])
    assert "457-55-5462" not in _text_plumber(result.content) and "5462" not in _text_pdfium(result.content)
    assert "in a form" in _text_plumber(result.content)
    assert b"457-55-5462" not in result.content


def test_annotations_form_fields_and_metadata_under_the_box_are_removed() -> None:
    def add_extras(pdf, page):
        widget = pdf.make_indirect(pikepdf.Dictionary(
            Type=pikepdf.Name.Annot, Subtype=pikepdf.Name.Widget, FT=pikepdf.Name.Tx, T=pikepdf.String("ssn_field"),
            V=pikepdf.String(SSN), Rect=[260, 695, 400, 715], F=4, P=page.obj))
        note = pdf.make_indirect(pikepdf.Dictionary(
            Type=pikepdf.Name.Annot, Subtype=pikepdf.Name.Text, Contents=pikepdf.String(f"call about {SSN}"),
            Rect=[260, 698, 280, 712], P=page.obj))
        far = pdf.make_indirect(pikepdf.Dictionary(
            Type=pikepdf.Name.Annot, Subtype=pikepdf.Name.Text, Contents=pikepdf.String("far away"), Rect=[10, 10, 30, 30], P=page.obj))
        page.Annots = pikepdf.Array([widget, note, far])
        pdf.Root.AcroForm = pikepdf.Dictionary(Fields=pikepdf.Array([widget]))
        pdf.docinfo["/Title"] = f"File for {SSN}"
        with pdf.open_metadata() as meta:
            meta["dc:description"] = f"holder {SSN}"
        pdf.docinfo["/Author"] = "kept author"

    data = _doc(extra=add_extras)
    box = _hit_boxes(data)[0]
    box = RedactBox(page_number=1, x0=box.x0, y0=box.y0 - 6, x1=box.x1 + 60, y1=box.y1 + 6)  # wide enough to cover the field
    out = redact_pdf_bytes(data, [box])
    assert out.metadata["annotations_removed"] == 2 and out.metadata["form_fields_removed"] >= 1
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        subtypes = [str(a.Subtype) for a in pdf.pages[0].Annots]
        assert subtypes == ["/Text"] and str(pdf.pages[0].Annots[0].Contents) == "far away"
        assert len(pdf.Root.AcroForm.Fields) == 0
        assert SSN not in str(pdf.docinfo.get("/Title", "")) and str(pdf.docinfo["/Author"]) == "kept author" and SSN not in str(pdf.docinfo.get("/Subject", ""))
        assert SSN.encode() not in bytes(pdf.Root.Metadata.read_bytes())
    assert SSN.encode() not in out.content


def test_unreadable_font_falls_back_to_a_flattened_page_that_says_so() -> None:
    pdf, font = _new_pdf()
    page = _add_text_page(pdf, font, [(72, 700, f"Secret {SSN} here")])
    # a font with no widths and an unknown name: positions are estimated, so the rewrite cannot be trusted
    page.Resources.Font.F1 = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type1, BaseFont=pikepdf.Name("/Zorp")))
    data = _save(pdf)
    with pdfplumber.open(io.BytesIO(data)) as d:
        words = d.pages[0].extract_words()
    assert words
    res = redact_pdf_bytes(data, [RedactBox(page_number=1, x0=60, y0=80, x1=300, y1=96)])
    assert res.metadata["tier"] in ("rasterize", "stream_rewrite")
    assert SSN not in _text_plumber(res.content) and SSN not in _text_pdfium(res.content)
    if res.metadata["tier"] == "rasterize":
        assert res.metadata["flattened_pages"] == [1] and res.metadata["notes"]


def test_input_is_never_modified_and_bad_requests_are_plain_errors() -> None:
    data = _doc()
    before = bytes(data)
    redact_pdf_bytes(data, _hit_boxes(data))
    assert data == before
    with pytest.raises(ValueError):
        redact_pdf_bytes(data, [])
    with pytest.raises(ValueError):
        redact_pdf_bytes(data, [RedactBox(page_number=9, x0=0, y0=0, x1=5, y1=5)])
    with pytest.raises(ValueError):
        RedactBox(page_number=1, x0=5, y0=0, x1=1, y1=5)


def test_find_uses_the_existing_pii_detector_validators_and_a_literal_and_a_regex() -> None:
    pdf, font = _new_pdf()
    _add_text_page(pdf, font, [(72, 700, f"SSN {SSN} card 4111 1111 1111 1111 bad card 4111 1111 1111 1112"), (72, 680, "mail jane@example.com ref ABC-77")])
    data = _save(pdf)
    texts = {h["text"] for h in find_redaction_hits_bytes(data, {"pii": True})["hits"]}
    assert SSN in texts and "jane@example.com" in texts and "4111 1111 1111 1111" in texts
    assert "4111 1111 1111 1112" not in texts  # fails the Luhn validator
    lit = find_redaction_hits_bytes(data, {"pii": False, "literals": ["ABC-77"]})["hits"]
    assert [h["text"] for h in lit] == ["ABC-77"]
    rx = find_redaction_hits_bytes(data, {"pii": False, "regexes": [r"ABC-\d+"]})["hits"]
    assert [h["text"] for h in rx] == ["ABC-77"]
    with pytest.raises(ValueError):
        find_redaction_hits_bytes(data, {"pii": False})
    with pytest.raises(ValueError):
        find_redaction_hits_bytes(data, {"pii": False, "regexes": ["("]})


def test_sanitize_removes_attachments_and_javascript_and_reports_them() -> None:
    def add(pdf, page):
        pdf.attachments["secret.txt"] = pikepdf.AttachedFileSpec(pdf, b"top secret")
        pdf.Root.Names = pdf.Root.get("/Names") or pikepdf.Dictionary()
        pdf.Root.Names.JavaScript = pikepdf.Dictionary(Names=pikepdf.Array([pikepdf.String("x"), pikepdf.Dictionary(S=pikepdf.Name.JavaScript, JS=pikepdf.String("app.alert(1)"))]))

    data = _doc(extra=add)
    rep = sanitize_report_bytes(data)
    assert rep["attachments"] >= 1 and rep["javascript_actions"] >= 1
    out = redact_pdf_bytes(data, _hit_boxes(data)).content
    rep2 = sanitize_report_bytes(out)
    assert rep2["attachments"] == 0 and rep2["javascript_actions"] == 0
    assert b"top secret" not in out


def test_rewrite_that_misses_is_caught_by_the_proof_and_the_page_is_flattened(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_files.specific_handlers.pdf.ops import redact_real

    data = _doc()
    boxes = _hit_boxes(data)
    # simulate a wrong glyph-width estimate: the rewrite cuts the wrong glyphs, so the proof must fail the page
    monkeypatch.setattr(redact_real._Font, "width", lambda self, code: 3000.0)
    result = redact_pdf_bytes(data, boxes)
    assert result.metadata["tier"] == "rasterize" and result.metadata["flattened_pages"] == [1]
    assert result.metadata["notes"] and "searchable" in result.metadata["notes"][0]
    assert SSN not in _text_plumber(result.content) and _text_pdfium(result.content).strip() == ""
    with pikepdf.open(io.BytesIO(result.content)) as pdf:
        assert len(pdf.pages) == 1 and "/Annots" not in pdf.pages[0].obj
    doc = pdfium.PdfDocument(result.content)
    try:
        img = doc[0].render(scale=1).to_pil().convert("L")
    finally:
        doc.close()
    b = boxes[0]
    assert img.crop((int(b.x0) + 1, int(b.y0) + 1, int(b.x1) - 1, int(b.y1) - 1)).getextrema()[1] < 10  # burned in black
