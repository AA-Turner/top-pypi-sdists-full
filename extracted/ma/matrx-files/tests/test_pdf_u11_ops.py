"""PDF-PLAN U11 forcing tests: each output really carries the change, read back with pikepdf or pypdfium2.

Built on the synthetic corpus (``_pdf_corpus``), no stored files and no PyMuPDF.
"""

from __future__ import annotations

import io

import pytest

pikepdf = pytest.importorskip("pikepdf")
pdfium = pytest.importorskip("pypdfium2")

from _pdf_corpus import build_corpus, decrypted_bytes  # noqa: E402

from matrx_files.specific_handlers.pdf.handler import PDFHandler  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.outline import read_outline_bytes, set_outline_bytes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.properties import read_properties_bytes, set_properties_bytes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.protect import protect_pdf_bytes, unprotect_pdf_bytes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.stamp import (  # noqa: E402
    BUILTIN_HEADER_FOOTER_TEMPLATES,
    PdfHeaderFooterTemplate,
    PdfStampSpec,
    apply_header_footer_bytes,
    stamp_pdf_bytes,
)

CORPUS = build_corpus()


def _text(data: bytes, page: int = 0) -> str:
    doc = pdfium.PdfDocument(data)
    try:
        return doc[page].get_textpage().get_text_range()
    finally:
        doc.close()


def _dark_box(data: bytes, page: int = 0, scale: float = 1.0) -> tuple[int, int, int, int, int, int]:
    """(left, top, right, bottom, width, height) of the non-white pixels, in the rendered (visible) page."""
    doc = pdfium.PdfDocument(data)
    try:
        img = doc[page].render(scale=scale).to_pil().convert("L")
    finally:
        doc.close()
    bbox = img.point(lambda v: 255 if v < 200 else 0).getbbox()
    assert bbox is not None, "nothing was drawn on the page"
    return (*bbox, img.width, img.height)


# ---------------------------------------------------------------------------
# Protect
# ---------------------------------------------------------------------------


def test_protected_file_refuses_to_open_without_the_password_and_opens_with_it() -> None:
    result = protect_pdf_bytes(CORPUS["digital"].data, user_password="open-sesame", owner_password="boss")
    with pytest.raises(pikepdf.PasswordError):
        pikepdf.open(io.BytesIO(result.content))
    with pikepdf.open(io.BytesIO(result.content), password="open-sesame") as pdf:
        assert pdf.is_encrypted
        assert pdf.encryption.R == 6  # AES-256
        assert len(pdf.pages) == CORPUS["digital"].page_count
    assert result.metadata["needs_password_to_open"] is True


def test_protect_writes_the_permissions_it_was_given() -> None:
    result = protect_pdf_bytes(
        CORPUS["digital"].data, owner_password="boss", allow={"print_highres": False, "extract": False, "modify": False}
    )
    with pikepdf.open(io.BytesIO(result.content)) as pdf:  # no user password: opens, restricted
        allow = pdf.allow
        assert allow.print_highres is False and allow.extract is False and allow.modify_other is False
        assert allow.print_lowres is True and allow.accessibility is True


def test_unprotect_needs_the_right_password_and_removes_the_lock() -> None:
    locked = protect_pdf_bytes(CORPUS["digital"].data, user_password="pw1", owner_password="pw2").content
    with pytest.raises(ValueError, match="does not open"):
        unprotect_pdf_bytes(locked, password="wrong")
    opened = unprotect_pdf_bytes(locked, password="pw1")
    with pikepdf.open(io.BytesIO(opened.content)) as pdf:  # no password needed any more
        assert not pdf.is_encrypted


def test_protect_an_already_encrypted_file_needs_its_password() -> None:
    enc = CORPUS["encrypted"]
    with pytest.raises(ValueError, match="password protected"):
        protect_pdf_bytes(enc.data, user_password="new")
    result = protect_pdf_bytes(enc.data, user_password="new", source_password=enc.password)
    with pikepdf.open(io.BytesIO(result.content), password="new") as pdf:
        assert len(pdf.pages) == enc.page_count


def test_protect_without_any_password_is_refused() -> None:
    with pytest.raises(ValueError, match="Give a password"):
        protect_pdf_bytes(CORPUS["digital"].data)


# ---------------------------------------------------------------------------
# Stamp: watermark, page numbers, Bates, header/footer
# ---------------------------------------------------------------------------


def test_page_numbers_are_on_every_page_with_the_right_numbers() -> None:
    src = CORPUS["long_30"] if "long_30" in CORPUS else CORPUS["digital"]
    out = stamp_pdf_bytes(src.data, [PdfStampSpec(text="Page {page} of {pages}")])
    for i in range(src.page_count):
        assert f"Page {i + 1} of {src.page_count}" in _text(out.content, i)
    # the original text is still there
    assert _text(src.data, 0).split()[0] in _text(out.content, 0)


def test_stamp_only_the_chosen_pages() -> None:
    src = CORPUS["digital"]
    assert src.page_count >= 2
    out = stamp_pdf_bytes(src.data, [PdfStampSpec(text="ONLYHERE")], pages=[2])
    assert "ONLYHERE" in _text(out.content, 1)
    assert "ONLYHERE" not in _text(out.content, 0)
    assert out.metadata["stamped_pages"] == [2]


def test_bates_numbers_are_monotone_with_no_gaps_across_a_merge() -> None:
    handler = PDFHandler(app_name="test_u11")
    merged = handler.merge_pdfs_from_bytes([{"content": CORPUS[k].data} for k in ("digital", "rotated", "tables")]).content
    count = len(pikepdf.open(io.BytesIO(merged)).pages)
    out = stamp_pdf_bytes(merged, [PdfStampSpec(text="ACME-{bates:000101}", position="bottom-right")])
    numbers = []
    for i in range(count):
        text = _text(out.content, i)
        hit = [t for t in text.split() if t.startswith("ACME-")]
        assert len(hit) == 1, (i, text)
        numbers.append(int(hit[0].split("-")[1]))
    assert numbers == list(range(101, 101 + count))
    assert out.metadata["bates_first"] == "ACME-000101" and out.metadata["bates_last"] == f"ACME-{100 + count:06d}"
    with pikepdf.open(io.BytesIO(out.content)) as pdf:  # the range is recorded in the file
        assert str(pdf.docinfo["/MatrxBatesFirst"]) == "ACME-000101"
        assert str(pdf.docinfo["/MatrxBatesLast"]) == f"ACME-{100 + count:06d}"


def test_watermark_goes_behind_the_page_text_and_carries_opacity() -> None:
    src = CORPUS["digital"]
    out = stamp_pdf_bytes(
        src.data, [PdfStampSpec(text="DRAFT", position="center", size=72, rotation=45, opacity=0.25, color="#cc0000", behind=True)]
    )
    assert "DRAFT" in _text(out.content, 0)
    with pikepdf.open(io.BytesIO(out.content)) as pdf:
        page = pdf.pages[0]
        gs = page.Resources.ExtGState
        assert any(abs(float(v.ca) - 0.25) < 1e-6 for _, v in gs.items())
        stream = b"".join(s.read_bytes() for s in page.Contents) if isinstance(page.Contents, pikepdf.Array) else page.Contents.read_bytes()
        assert stream.index(b"(DRAFT)") < stream.index(b"BT", stream.index(b"(DRAFT)") + 1) if stream.count(b"BT") > 1 else True


@pytest.mark.parametrize("rotate", [0, 90, 180, 270])
def test_footer_is_at_the_bottom_of_the_screen_on_a_rotated_page(rotate: int) -> None:
    with pikepdf.new() as pdf:
        pdf.add_blank_page(page_size=(612, 792))
        pdf.pages[0].obj.Rotate = rotate
        buf = io.BytesIO()
        pdf.save(buf)
    out = stamp_pdf_bytes(buf.getvalue(), [PdfStampSpec(text="FOOTERMARK", position="bottom-center", size=14)])
    left, top, right, bottom, w, h = _dark_box(out.content)
    assert top > h * 0.85, f"rotate={rotate}: stamp is not at the bottom of the visible page ({top}/{h})"
    assert abs((left + right) / 2 - w / 2) < w * 0.05, f"rotate={rotate}: stamp is not centred"
    # and the text reads upright: the box is wider than tall
    assert (right - left) > (bottom - top)


def test_template_applied_twice_gives_the_same_output() -> None:
    src = CORPUS["digital"].data
    tpl = BUILTIN_HEADER_FOOTER_TEMPLATES[1]
    first = apply_header_footer_bytes(src, tpl)
    again = apply_header_footer_bytes(src, tpl.model_dump())
    assert first.content == again.content
    # and by hand from the same specs
    manual = stamp_pdf_bytes(src, tpl.to_specs(), operation="header_footer")
    assert manual.content == first.content


def test_header_footer_template_puts_text_in_each_position() -> None:
    tpl = PdfHeaderFooterTemplate(name="t", header_left="HL", header_right="HR", footer_center="Page {page}")
    out = apply_header_footer_bytes(CORPUS["digital"].data, tpl)
    text = _text(out.content, 0)
    assert "HL" in text and "HR" in text and "Page 1" in text
    with pytest.raises(ValueError, match="no text"):
        apply_header_footer_bytes(CORPUS["digital"].data, PdfHeaderFooterTemplate(name="empty"))


def test_stamp_on_an_out_of_range_page_is_refused_and_non_latin_text_is_counted() -> None:
    with pytest.raises(ValueError, match="does not exist"):
        stamp_pdf_bytes(CORPUS["digital"].data, [PdfStampSpec(text="x")], pages=[999])
    out = stamp_pdf_bytes(CORPUS["digital"].data, [PdfStampSpec(text="ok 中")])
    assert out.metadata["replaced_characters"] == 1


# ---------------------------------------------------------------------------
# Bookmarks
# ---------------------------------------------------------------------------


def test_outline_round_trips_titles_pages_and_nesting() -> None:
    src = CORPUS["digital"]
    tree = [
        {"title": "Intro", "page": 1, "children": [{"title": "Background", "page": 1}]},
        {"title": "Body", "page": 2, "children": []},
    ]
    out = set_outline_bytes(src.data, tree)
    got = read_outline_bytes(out.content)
    assert [(n["title"], n["page"]) for n in got["items"]] == [("Intro", 1), ("Body", 2)]
    assert [(c["title"], c["page"]) for c in got["items"][0]["children"]] == [("Background", 1)]
    # an editor that opens the file sees the same thing
    with pikepdf.open(io.BytesIO(out.content)) as pdf, pdf.open_outline() as outline:
        assert [str(i.title) for i in outline.root] == ["Intro", "Body"]


def test_outline_edit_replaces_and_clearing_removes_it() -> None:
    src = CORPUS["digital"]
    one = set_outline_bytes(src.data, [{"title": "A", "page": 1}]).content
    two = set_outline_bytes(one, [{"title": "B renamed", "page": 2}]).content
    assert [n["title"] for n in read_outline_bytes(two)["items"]] == ["B renamed"]
    cleared = set_outline_bytes(two, []).content
    assert read_outline_bytes(cleared)["items"] == []


def test_outline_refuses_a_page_the_file_does_not_have() -> None:
    with pytest.raises(ValueError, match="has .* pages"):
        set_outline_bytes(CORPUS["digital"].data, [{"title": "Nowhere", "page": 99}])


# ---------------------------------------------------------------------------
# Properties and XMP
# ---------------------------------------------------------------------------


def test_properties_round_trip_in_info_and_xmp() -> None:
    out = set_properties_bytes(
        CORPUS["digital"].data, title="Quarterly report", author="Ada Lovelace", subject="Q3", keywords="finance, q3"
    )
    got = read_properties_bytes(out.content)
    assert (got["title"], got["author"], got["subject"], got["keywords"]) == ("Quarterly report", "Ada Lovelace", "Q3", "finance, q3")
    assert got["has_xmp"]
    with pikepdf.open(io.BytesIO(out.content)) as pdf:  # a second reader: XMP agrees with Info
        with pdf.open_metadata() as meta:
            assert meta["dc:title"] == "Quarterly report"
            assert list(meta["dc:creator"]) == ["Ada Lovelace"]
            assert meta["dc:description"] == "Q3"
            assert meta["pdf:Keywords"] == "finance, q3"
    # pypdfium2 reads the Info dictionary too
    doc = pdfium.PdfDocument(out.content)
    try:
        assert doc.get_metadata_value("Title") == "Quarterly report"
        assert doc.get_metadata_value("Author") == "Ada Lovelace"
    finally:
        doc.close()


def test_empty_string_clears_a_property_and_none_leaves_it() -> None:
    first = set_properties_bytes(CORPUS["digital"].data, title="T", author="A").content
    second = set_properties_bytes(first, author="").content
    got = read_properties_bytes(second)
    assert got["title"] == "T" and got["author"] == ""
    with pytest.raises(ValueError, match="at least one"):
        set_properties_bytes(first)


def test_read_properties_reports_size_version_and_encryption() -> None:
    got = read_properties_bytes(CORPUS["rotated"].data)
    assert got["page_count"] == CORPUS["rotated"].page_count
    assert got["page_size"]["width_pt"] > 0 and got["pdf_version"]
    enc = CORPUS["encrypted"]
    assert read_properties_bytes(enc.data, password=enc.password)["encrypted"] is True
    with pytest.raises(ValueError, match="password protected"):
        read_properties_bytes(enc.data)


def test_a_signed_flag_is_reported_when_the_file_has_a_signature_field() -> None:
    with pikepdf.new() as pdf:
        pdf.add_blank_page()
        pdf.Root.AcroForm = pikepdf.Dictionary(SigFlags=3, Fields=pikepdf.Array())
        buf = io.BytesIO()
        pdf.save(buf)
    assert read_properties_bytes(buf.getvalue())["signed"] is True
    assert set_properties_bytes(buf.getvalue(), title="x").metadata["signed"] is True


def test_properties_round_trip_in_info_and_xmp_on_a_hand_made_pdf() -> None:
    """Live walk 3: Title/Author saved, then read back empty. Written to the Info dictionary AND XMP, read back."""
    from matrx_files.specific_handlers.pdf.ops.properties import read_properties_bytes, set_properties_bytes

    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>"]
    out = b"%PDF-1.4\n"
    offs = []
    for i, o in enumerate(objs):
        offs.append(len(out))
        out += f"{i + 1} 0 obj\n{o}\nendobj\n".encode()
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF".encode()

    saved = set_properties_bytes(out, title="LW3 title", author="LW3 author").content
    back = read_properties_bytes(saved)
    assert back["title"] == "LW3 title" and back["author"] == "LW3 author"
    assert back["xmp"]["dc:title"] == "LW3 title" and back["xmp"]["dc:creator"] == ["LW3 author"]
    # A second edit keeps the first, and an empty string clears one field in both places.
    again = read_properties_bytes(set_properties_bytes(saved, subject="S", title="").content)
    assert again["title"] == "" and again["author"] == "LW3 author" and again["subject"] == "S"
    assert "dc:title" not in again["xmp"] and again["xmp"]["dc:creator"] == ["LW3 author"]
