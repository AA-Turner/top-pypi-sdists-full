"""Office attachments are converted to Markdown (anydoc first, plain-text
extractors as fallback), and text-based PDFs skip the native page-image
attachment in favor of their extracted Markdown."""

import os
from typing import Optional

import pytest

from xpander_sdk.media.files import (
    _DOCUMENT_EXTS,
    PDF_INLINE_MIN_CHARS,
    _document_markdown,
    _pdf_markdown_or_none,
    categorize_files,
)


def test_anydoc_is_installed_so_conversion_tests_are_not_silently_skipped():
    """anydoc is a base dependency; a missing wheel must fail here rather than skip every conversion test."""
    if os.getenv("XPANDER_ALLOW_MISSING_ANYDOC", "").strip():
        pytest.skip("anydoc deliberately absent in this environment")
    import anydoc

    assert callable(anydoc.to_markdown_bytes)


def test_office_documents_are_categorized_as_documents():
    urls = [f"https://files.example.com/report{ext}" for ext in sorted(_DOCUMENT_EXTS)]
    cat = categorize_files(urls)
    assert cat.documents == urls
    assert cat.pdfs == [] and cat.images == [] and cat.files == []


def test_categorization_is_extension_case_insensitive_and_ignores_query():
    cat = categorize_files(["https://files.example.com/Q3%20deck.PPTX?token=abc"])
    assert len(cat.documents) == 1


def test_pdf_image_and_readable_routing_unchanged():
    cat = categorize_files([
        "https://files.example.com/a.pdf",
        "https://files.example.com/b.png",
        "https://files.example.com/c.csv",
    ])
    assert cat.pdfs == ["https://files.example.com/a.pdf"]
    assert cat.images == ["https://files.example.com/b.png"]
    assert cat.files == ["https://files.example.com/c.csv"]


def test_document_markdown_converts_rtf_preserving_formatting():
    pytest.importorskip("anydoc")
    md = _document_markdown(rb"{\rtf1\ansi Hello \b world\b0}", ".rtf")
    assert md is not None and "Hello" in md and "**world**" in md


def test_document_markdown_returns_none_on_garbage():
    md = _document_markdown(b"garbage-not-a-document", ".docx")
    assert md is None  # caller falls back to python-docx, which then errors -> ''


def _minimal_text_pdf(text_lines):
    """Build a minimal one-page PDF with the given text lines (no external deps)."""
    stream = "BT /F1 10 Tf 50 750 Td " + " ".join(
        f"({line}) Tj 0 -12 Td" for line in text_lines
    ) + " ET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{obj}\nendobj\n".encode()
    xref_pos = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode()
    return out


def test_text_dense_pdf_converts_to_markdown():
    pytest.importorskip("anydoc")
    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    md = _pdf_markdown_or_none(pdf)
    assert md is not None and "Quarterly revenue" in md
    assert len(md) >= PDF_INLINE_MIN_CHARS


def test_sparse_pdf_keeps_native_attachment():
    pytest.importorskip("anydoc")
    # A near-empty PDF (like a scanned page) extracts almost no text -> stay native
    pdf = _minimal_text_pdf(["scan artifact"])
    assert _pdf_markdown_or_none(pdf) is None


def test_garbage_pdf_keeps_native_attachment():
    assert _pdf_markdown_or_none(b"not-a-pdf") is None


def test_plain_text_variants_route_to_readable():
    urls = [f"https://files.example.com/x{ext}" for ext in (".tsv", ".log", ".toml", ".ipynb", ".eml")]
    cat = categorize_files(urls)
    assert cat.files == urls


def test_unreadable_format_gets_explicit_note_not_silence():
    from types import SimpleNamespace
    from xpander_sdk.media.files import plan_attachments

    caps = SimpleNamespace(
        supports_vision=True, supports_native_pdf=True,
        max_fetch_bytes=10_000_000, max_images=10,
    )
    plan = plan_attachments(["https://files.example.com/diagram.vsdx"], caps)
    assert plan.items[0].action == "url_only"
    assert any("cannot be read" in note for note in plan.notes)


def _iwork_bytes(
    preview_pdf: Optional[bytes] = None, preview_name: str = "QuickLook/Preview.pdf"
) -> bytes:
    """Build an iWork-shaped zip: a proprietary payload plus an optional QuickLook preview."""
    import io
    import zipfile

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("Index/Document.iwa", b"\x00proprietary-iwa-blob")
        if preview_pdf is not None:
            zf.writestr(preview_name, preview_pdf)
    return buf.getvalue()


def test_iwork_pages_extracts_via_preview_pdf():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    pdf = _minimal_text_pdf([f"Board meeting agenda item {i}" for i in range(40)])
    data = _iwork_bytes(preview_pdf=pdf)
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")):
        out = extract_document_text("https://x/report.pages")
    assert "Board meeting agenda" in out


def test_iwork_without_preview_reports_unreadable():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    data = _iwork_bytes(preview_pdf=None)
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")):
        out = extract_document_text("https://x/deck.key")
    assert out.startswith("Error: attachment could not be read")


def test_iwork_files_route_to_documents_bucket():
    cat = categorize_files([
        "https://x/a.pages", "https://x/b.key", "https://x/c.numbers",
    ])
    assert len(cat.documents) == 3


def test_prepare_pdf_routes_text_dense_pdf_to_markdown():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, note = prepare_pdf("https://x/report.pdf", ModelCapabilities())
    assert action == "text"
    assert "Quarterly revenue" in payload


def test_prepare_pdf_keeps_native_for_sparse_pdf():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _minimal_text_pdf(["scan artifact"])
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, note = prepare_pdf("https://x/scan.pdf", ModelCapabilities())
    assert action == "file"


def test_iwork_corrupt_preview_gets_conversion_error_not_no_preview():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    data = _iwork_bytes(preview_pdf=b"corrupt-not-a-pdf")
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")):
        out = extract_document_text("https://x/report.pages")
    assert "could not be converted" in out and "no embedded preview" not in out


def test_pem_key_file_gets_generic_error_not_iwork_guidance():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    pem = b"-----BEGIN PRIVATE KEY-----\nMIIEvQ...\n-----END PRIVATE KEY-----\n"
    with patch.object(files_mod, "_download", return_value=(pem, "application/octet-stream")):
        out = extract_document_text("https://x/server.key")
    assert out.startswith("Error: attachment could not be read (unsupported file format)")
    assert "iWork" not in out and "PRIVATE" not in out


def test_zip_bomb_preview_is_skipped():
    import io
    import zipfile
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import _iwork_preview_pdf

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("QuickLook/Preview.pdf", b"x")
    data = buf.getvalue()
    with patch.object(files_mod, "_MAX_DOC_BYTES", 0):
        preview, status = _iwork_preview_pdf(data)
    assert preview is None and status == "too_large"


def test_oversized_first_candidate_falls_through_to_next_preview():
    import io
    import zipfile
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import _iwork_preview_pdf

    small_pdf = b"%PDF-tiny"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("QuickLook/Preview.pdf", b"x" * 64)  # oversized under the patched cap
        zf.writestr("QuickLook/fallback.pdf", small_pdf)
    data = buf.getvalue()
    with patch.object(files_mod, "_MAX_DOC_BYTES", 32):
        preview, status = _iwork_preview_pdf(data)
    assert preview == small_pdf and status == "ok"


def _long_text_pdf() -> bytes:
    """A text PDF whose Markdown comfortably exceeds the per-file inline cap."""
    # Only ~60 lines fit inside the MediaBox, so the volume has to come from line length.
    return _minimal_text_pdf(
        [f"Quarterly revenue line item number {i} " + "with supporting commentary " * 8
         for i in range(60)]
    )


def test_long_pdf_markdown_keeps_native_attachment_for_native_model():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.files import _MAX_INLINE_TEXT_CHARS
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _long_text_pdf()
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, _ = prepare_pdf("https://x/long.pdf", ModelCapabilities())
    # Inlined text would be clipped to _MAX_INLINE_TEXT_CHARS; the native attachment is whole.
    assert action == "file"
    assert len(_document_markdown(pdf, ".pdf")) > _MAX_INLINE_TEXT_CHARS


def test_long_pdf_markdown_still_inlines_when_provider_rejects_file_blobs():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _long_text_pdf()
    caps = ModelCapabilities(supports_native_pdf=False)
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, _ = prepare_pdf("https://x/long.pdf", caps)
    assert action == "text" and "Quarterly revenue" in payload


def test_pdf_too_large_for_native_still_inlines_markdown():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _long_text_pdf()
    caps = ModelCapabilities(max_pdf_bytes=len(pdf) - 1)
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, _ = prepare_pdf("https://x/long.pdf", caps)
    assert action == "text"


def test_disabled_injection_keeps_native_pdf_instead_of_dropping_it():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, _ = prepare_pdf(
            "https://x/report.pdf", ModelCapabilities(), allow_text=False
        )
    assert action == "file" and payload is not None


def test_disabled_injection_without_native_pdf_says_content_is_absent():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import NO_INJECTION_NOTE, prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    caps = ModelCapabilities(supports_native_pdf=False)
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, payload, note = prepare_pdf("https://x/report.pdf", caps, allow_text=False)
    assert action == "url_only" and payload is None and note == NO_INJECTION_NOTE


def test_empty_conversion_falls_back_to_the_plain_text_extractor():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text
    from tests.unit.test_files_inline import _docx_bytes

    data = _docx_bytes("hello from docx")
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")), \
         patch.object(files_mod, "_document_markdown", return_value=""):
        out = extract_document_text("https://x/c.docx")
    assert "hello from docx" in out


def test_raising_fallback_extractor_reports_unreadable_not_silence():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import DOC_UNREADABLE_NOTE, extract_document_text

    # anydoc declines and python-docx then chokes: the note is exactly this case.
    with patch.object(files_mod, "_download", return_value=(b"not-a-zip", "application/octet-stream")), \
         patch.object(files_mod, "_document_markdown", return_value=None):
        out = extract_document_text("https://x/broken.docx")
    assert out == DOC_UNREADABLE_NOTE


def test_document_without_fallback_extractor_reports_unreadable_not_silence():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import DOC_UNREADABLE_NOTE, extract_document_text

    with patch.object(files_mod, "_download", return_value=(b"whatever", "application/octet-stream")), \
         patch.object(files_mod, "_document_markdown", return_value=None):
        out = extract_document_text("https://x/notes.odt")
    assert out == DOC_UNREADABLE_NOTE


def test_converted_markdown_is_capped_before_it_leaves_the_converter():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod

    with patch.object(files_mod, "_MAX_DOC_MARKDOWN_CHARS", 5):
        md = _document_markdown(rb"{\rtf1\ansi Hello \b world\b0}", ".rtf")
    # The true length leads, so a second clip downstream cannot cut the marker away.
    assert md.startswith("[showing the first 5 of 16 characters]")
    assert md.endswith("Hello")


def test_documents_are_extracted_concurrently_in_order():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_documents_text

    urls = [f"https://x/doc{i}.docx" for i in range(4)]
    with patch.object(files_mod, "extract_document_text", side_effect=lambda url: f"text of {url}"):
        out = extract_documents_text(urls)
    assert out == [(u, f"text of {u}") for u in urls]


def test_unreadable_attachments_share_one_note():
    from types import SimpleNamespace
    from xpander_sdk.media.files import plan_attachments

    caps = SimpleNamespace(
        supports_vision=True, supports_native_pdf=True,
        max_fetch_bytes=10_000_000, max_images=10,
    )
    plan = plan_attachments(
        ["https://x/a.vsdx", "https://x/b.zip", "https://x/c.heic"], caps
    )
    assert len(plan.notes) == 1
    assert all(url in plan.notes[0] for url in ("a.vsdx", "b.zip", "c.heic"))


def test_pdf_markdown_route_has_an_env_kill_switch(monkeypatch):
    pytest.importorskip("anydoc")
    monkeypatch.setenv("XPANDER_PDF_MARKDOWN", "off")
    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    assert _pdf_markdown_or_none(pdf) is None


def test_text_routed_pdf_tells_a_vision_model_the_visuals_are_missing():
    pytest.importorskip("anydoc")
    from unittest.mock import patch
    from xpander_sdk.media import prepare as media_mod
    from xpander_sdk.media.prepare import PDF_AS_TEXT_NOTE, prepare_pdf
    from xpander_sdk.media.caps import ModelCapabilities

    pdf = _minimal_text_pdf([f"Quarterly revenue line item number {i}" for i in range(60)])
    with patch.object(media_mod, "_download", return_value=(pdf, "application/pdf")):
        action, _, native_note = prepare_pdf("https://x/report.pdf", ModelCapabilities())
        action_no_native, _, note_no_native = prepare_pdf(
            "https://x/report.pdf", ModelCapabilities(supports_native_pdf=False)
        )
    assert action == "text" and native_note == PDF_AS_TEXT_NOTE
    # A provider that could never render the pages loses nothing, so it gets no note.
    assert action_no_native == "text" and note_no_native is None


def test_iwork_preview_cap_follows_the_callers_max_bytes():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    data = _iwork_bytes(preview_pdf=b"x" * 64)
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")):
        out = extract_document_text("https://x/report.pages", max_bytes=32)
    assert "exceeds the size limit" in out


def test_oversized_preview_reports_size_limit_not_missing_preview():
    from unittest.mock import patch
    from xpander_sdk.media import files as files_mod
    from xpander_sdk.media.files import extract_document_text

    data = _iwork_bytes(preview_pdf=b"x" * 64)
    with patch.object(files_mod, "_download", return_value=(data, "application/octet-stream")), \
         patch.object(files_mod, "_MAX_DOC_BYTES", 32):
        out = extract_document_text("https://x/report.pages")
    assert "exceeds the size limit" in out and "no embedded preview" not in out
