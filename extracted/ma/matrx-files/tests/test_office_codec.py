"""Bare-venv smoke + round-trip tests for the Office codec.

These must pass with ONLY matrx-files (+ its declared deps) installed — no host,
no ORM, no network. They generate real Office bytes and read them back, proving
extract/generate are inverse enough for the AI ingest + generation paths.
"""

from __future__ import annotations

import base64

import pytest
from matrx_files.specific_handlers.office import (
    DocBlock,
    DocumentSpec,
    LegacyBinaryOfficeError,
    OfficeKind,
    PresentationSpec,
    SheetSpec,
    SlideSpec,
    SpreadsheetSpec,
    classify_office,
    extract_office,
    generate_office,
)
from matrx_files.specific_handlers.office.extract import UnsupportedOfficeError


def _bytes(result) -> bytes:
    return base64.b64decode(result.base64_data)


def test_classify_office_by_mime_and_ext():
    assert classify_office(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ) is OfficeKind.docx
    assert classify_office("application/octet-stream", "deck.pptx") is OfficeKind.pptx
    assert classify_office(None, "sheet.xlsx") is OfficeKind.xlsx
    assert classify_office("application/msword", "old.doc") is OfficeKind.doc
    assert classify_office("text/plain", "note.txt") is None


def test_docx_round_trip():
    spec = DocumentSpec(
        title="Quarterly Report",
        blocks=[
            DocBlock(type="heading", text="Summary", level=1),
            DocBlock(type="paragraph", text="Revenue grew 20% this quarter."),
            DocBlock(type="bullet", text="North region led growth"),
            DocBlock(type="table", rows=[["Region", "Rev"], ["North", "100"], ["South", "80"]]),
        ],
    )
    gen = generate_office(spec)
    assert gen.office_kind is OfficeKind.docx
    assert gen.byte_size > 0

    ex = extract_office(_bytes(gen), file_name="report.docx")
    assert ex.office_kind is OfficeKind.docx
    assert "Quarterly Report" in ex.markdown
    assert "Summary" in ex.markdown
    assert "Revenue grew 20%" in ex.markdown
    assert "North" in ex.markdown  # table survived
    assert len(ex.portions) == 1
    assert ex.raw_chars > 0


def test_pptx_round_trip():
    spec = PresentationSpec(
        title="Launch Deck",
        subtitle="2026",
        slides=[
            SlideSpec(title="Problem", bullets=["Users can't ingest Office", "It just sits there"]),
            SlideSpec(title="Solution", bullets=["One codec"], notes="Emphasize reuse"),
        ],
    )
    gen = generate_office(spec)
    assert gen.office_kind is OfficeKind.pptx

    ex = extract_office(_bytes(gen), file_name="deck.pptx")
    assert ex.office_kind is OfficeKind.pptx
    # cover slide + 2 content slides
    assert len(ex.portions) == 3
    assert any("Problem" in p.markdown for p in ex.portions)
    assert any("Solution" in p.markdown for p in ex.portions)
    assert any("Speaker notes" in p.markdown for p in ex.portions)
    assert all(p.kind == "slide" for p in ex.portions)


def test_xlsx_round_trip():
    spec = SpreadsheetSpec(
        sheets=[
            SheetSpec(
                name="Sales",
                columns=["Region", "Revenue"],
                rows=[["North", 100], ["South", 80]],
            ),
            SheetSpec(name="Notes", columns=["Note"], rows=[["Q1 strong"]]),
        ],
    )
    gen = generate_office(spec)
    assert gen.office_kind is OfficeKind.xlsx

    ex = extract_office(_bytes(gen), file_name="data.xlsx")
    assert ex.office_kind is OfficeKind.xlsx
    assert len(ex.portions) == 2
    assert any(p.title == "Sales" for p in ex.portions)
    sales = next(p for p in ex.portions if p.title == "Sales")
    assert "Region" in sales.markdown and "North" in sales.markdown
    assert all(p.kind == "sheet" for p in ex.portions)


def test_legacy_binary_rejected():
    # A .doc classification must refuse pure-python extraction loudly.
    try:
        extract_office(b"\xd0\xcf\x11\xe0fake-ole", file_name="legacy.doc")
        raise AssertionError("expected LegacyBinaryOfficeError")
    except LegacyBinaryOfficeError:
        pass


def test_unsupported_rejected():
    try:
        extract_office(b"hello", file_name="note.txt")
        raise AssertionError("expected UnsupportedOfficeError")
    except UnsupportedOfficeError:
        pass


def test_legacy_ole_bytes_named_docx_still_rejected():
    # A real legacy OLE file MISNAMED .docx (or carrying an OpenXML mime) must
    # be caught as legacy by its BYTES, not blow up with a raw BadZipFile.
    ole = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 32
    try:
        extract_office(
            ole,
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            file_name="mislabeled.docx",
        )
        raise AssertionError("expected LegacyBinaryOfficeError")
    except LegacyBinaryOfficeError:
        pass


def test_malformed_full_size_ole_header_is_rejected_before_conversion():
    malformed = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 504
    try:
        extract_office(malformed, file_name="malformed.doc")
        raise AssertionError("expected LegacyBinaryOfficeError")
    except LegacyBinaryOfficeError:
        pass


def test_corrupt_zip_raises_documented_error():
    # Garbage named .docx must raise the DOCUMENTED error type, never a raw
    # zipfile.BadZipFile — callers do `except OfficeExtractionError`.
    from matrx_files.specific_handlers.office import OfficeExtractionError

    try:
        extract_office(b"PK\x03\x04not-a-real-zip-body", file_name="broken.docx")
        raise AssertionError("expected UnsupportedOfficeError")
    except OfficeExtractionError:
        pass


def test_extensionless_docx_identified_by_bytes():
    # A real .docx with NO recognizable filename and NO mime must still extract
    # (byte-sniff finds the word/ archive). This is the crash path the router
    # could hit when a file was renamed extensionless.
    spec = DocumentSpec(blocks=[DocBlock(type="paragraph", text="extensionless body")])
    gen = generate_office(spec)
    ex = extract_office(_bytes(gen), mime_type=None, file_name="somefile")
    assert ex.office_kind is OfficeKind.docx
    assert "extensionless body" in ex.markdown


def test_pptx_blank_layout_keeps_content():
    # A titled slide with bullets on a placeholder-less layout must NOT silently
    # drop its content (was a data-loss bug).
    spec = PresentationSpec(
        slides=[SlideSpec(title="Kept", bullets=["one", "two"], layout="blank")],
    )
    gen = generate_office(spec)
    ex = extract_office(_bytes(gen), file_name="d.pptx")
    all_md = "\n".join(p.markdown for p in ex.portions)
    assert "Kept" in all_md
    assert "one" in all_md and "two" in all_md


def test_libreoffice_lane_degrades_loudly_when_absent():
    # When soffice is unavailable, legacy handling must raise the documented
    # error (never silently return nothing), and convert_* must raise
    # LibreOfficeUnavailable — the "loud recovery, no silent default" rule.
    from matrx_files.specific_handlers.office import (
        LibreOfficeUnavailable,
        convert_to_pdf,
        libreoffice_available,
    )
    from matrx_files.specific_handlers.office.models import OfficeKind

    if libreoffice_available():
        pytest.skip("LibreOffice present — the absent-host contract can't be tested here")
    ole = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 32
    # Legacy bytes with LibreOffice off → LegacyBinaryOfficeError (not a crash).
    try:
        extract_office(ole, file_name="legacy.doc", allow_libreoffice=True)
        raise AssertionError("expected LegacyBinaryOfficeError")
    except LegacyBinaryOfficeError:
        pass
    # Direct convert call → explicit unavailable error.
    try:
        convert_to_pdf(b"x", source_kind=OfficeKind.docx)
        raise AssertionError("expected LibreOfficeUnavailable")
    except LibreOfficeUnavailable:
        pass


def test_docx_plain_indented_paragraph_not_bulleted():
    # A "List Paragraph"-styled paragraph with NO numbering must render as a
    # plain paragraph, not a bullet.
    import io as _io

    import docx

    d = docx.Document()
    p = d.add_paragraph("indented body text")
    p.style = d.styles["List Paragraph"]  # style present, but no numPr
    buf = _io.BytesIO()
    d.save(buf)
    ex = extract_office(buf.getvalue(), file_name="x.docx")
    assert "indented body text" in ex.markdown
    assert "- indented body text" not in ex.markdown
