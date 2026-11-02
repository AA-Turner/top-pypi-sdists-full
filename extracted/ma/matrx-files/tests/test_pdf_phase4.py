"""Tests for the Phase 4 redaction surface.

Covers:
- Region redaction + mandatory verification step
- Pattern redaction across the builtin catalog (SSN / email / phone / MRN)
- Audit row shape (the host persists this; we just verify the payload)
- Scrub helpers — strip_metadata, strip_attachments, strip_javascript,
  flatten_annotations, strip_all_pii
- redact_repeated_regions bridges Phase 3 detector output
- Verification failure semantics (engine refuses to return the file)
"""

from __future__ import annotations

import pymupdf
import pytest

from matrx_files.specific_handlers.pdf import (
    BUILTIN_PATTERNS,
    PDFHandler,
    RedactionRegion,
    RedactionResult,
    detect_repeated_regions,
    flatten_annotations,
    list_builtin_patterns,
    redact_pattern,
    redact_regions,
    redact_repeated_regions,
    strip_all_pii,
    strip_attachments,
    strip_javascript,
    strip_metadata,
)



# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _pii_doc() -> bytes:
    """Single-page synthetic doc with planted PII and metadata."""
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((72, 100), "Patient: Jane Doe", fontsize=12)
        page.insert_text((72, 130), "SSN: 123-45-6789", fontsize=12)
        page.insert_text((72, 160), "Phone: (555) 867-5309", fontsize=12)
        page.insert_text((72, 190), "Email: jane@example.com", fontsize=12)
        page.insert_text((72, 220), "MRN: 99887766", fontsize=12)
        page.insert_text((72, 280), "Body content unaffected by redactions.", fontsize=12)
        doc.set_metadata(
            {"author": "Test Author", "title": "SENSITIVE", "subject": "private"}
        )
        return doc.tobytes()
    finally:
        doc.close()


def _multipage_legal_doc(page_count: int = 6) -> bytes:
    doc = pymupdf.open()
    try:
        for n in range(1, page_count + 1):
            page = doc.new_page(width=612, height=792)
            page.insert_text((72, 30), "Acme Law Firm — Confidential", fontsize=10)
            page.insert_text((72, 150), f"Body page {n}", fontsize=12)
            page.insert_text((72, 760), "Matter no. 12345", fontsize=8)
        return doc.tobytes()
    finally:
        doc.close()


def _page_text(pdf_bytes: bytes, page_idx: int = 0) -> str:
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        return doc[page_idx].get_text("text")


# ---------------------------------------------------------------------------
# Pattern redactor
# ---------------------------------------------------------------------------


def test_pattern_catalog_well_formed() -> None:
    catalog = list_builtin_patterns()
    assert catalog
    ids = {p["id"] for p in catalog}
    for required in ("ssn", "email", "phone_us", "mrn"):
        assert required in ids
    for entry in catalog:
        assert entry["pattern"]
        assert entry["description"]


def test_redact_pattern_ssn_removes_and_verifies() -> None:
    pdf_bytes = _pii_doc()
    result = redact_pattern(pdf_bytes, "ssn", reason="HIPAA: remove SSN")
    assert result.verification_passed
    assert result.audit.status == "success"
    assert result.audit.regions_count >= 1
    out_text = _page_text(result.content)
    assert "123-45-6789" not in out_text
    # Other PII still present (we only asked for SSN).
    assert "jane@example.com" in out_text
    # Body text untouched.
    assert "Body content unaffected" in out_text


def test_redact_pattern_email_removes() -> None:
    pdf_bytes = _pii_doc()
    result = redact_pattern(pdf_bytes, "email", reason="Strip email")
    assert result.verification_passed
    out_text = _page_text(result.content)
    assert "jane@example.com" not in out_text
    assert "123-45-6789" in out_text  # SSN survives — we only asked for email


def test_redact_pattern_no_targets_returns_original() -> None:
    pdf_bytes = _pii_doc()
    # Use a custom regex that matches nothing
    result = redact_pattern(pdf_bytes, r"\bXYZNOTINDOC\b", reason="no-op")
    assert result.audit.status == "no_targets"
    assert result.audit.regions_count == 0
    assert result.verification_passed


def test_redact_pattern_requires_reason() -> None:
    with pytest.raises(ValueError, match="non-empty reason"):
        redact_pattern(_pii_doc(), "ssn", reason="")


def test_redact_pattern_supports_custom_regex() -> None:
    pdf_bytes = _pii_doc()
    # Match the literal word "Jane"
    result = redact_pattern(pdf_bytes, r"\bJane\b", reason="Strip first name")
    assert result.verification_passed
    out_text = _page_text(result.content)
    assert "Jane" not in out_text
    # "Doe" remains
    assert "Doe" in out_text


# ---------------------------------------------------------------------------
# Region redactor + verification
# ---------------------------------------------------------------------------


def test_redact_regions_removes_text_in_bbox() -> None:
    pdf_bytes = _pii_doc()
    # Cover the SSN line (y≈130)
    region = RedactionRegion(page_number=1, x0=60, y0=120, x1=400, y1=145)
    result = redact_regions(pdf_bytes, [region], reason="Manual SSN bbox redact")
    assert result.verification_passed
    assert result.audit.status == "success"
    assert result.audit.regions_count == 1
    out_text = _page_text(result.content)
    assert "123-45-6789" not in out_text
    assert "jane@example.com" in out_text


def test_redact_regions_empty_list_returns_no_targets() -> None:
    pdf_bytes = _pii_doc()
    result = redact_regions(pdf_bytes, [], reason="empty test")
    assert result.audit.status == "no_targets"
    assert result.verification_passed
    assert result.content == pdf_bytes


def test_redact_regions_rejects_invalid_bbox() -> None:
    with pytest.raises(ValueError, match="must have x1>x0 and y1>y0"):
        RedactionRegion(page_number=1, x0=100, y0=100, x1=50, y1=200)


def test_redact_regions_rejects_out_of_range_page() -> None:
    pdf_bytes = _pii_doc()  # 1 page
    region = RedactionRegion(page_number=5, x0=0, y0=0, x1=100, y1=100)
    with pytest.raises(ValueError, match="document has 1 page"):
        redact_regions(pdf_bytes, [region], reason="bad page")


def test_redact_regions_requires_reason() -> None:
    with pytest.raises(ValueError, match="non-empty reason"):
        redact_regions(
            _pii_doc(),
            [RedactionRegion(page_number=1, x0=0, y0=0, x1=10, y1=10)],
            reason="",
        )


# ---------------------------------------------------------------------------
# Audit payload shape
# ---------------------------------------------------------------------------


def test_audit_payload_carries_required_fields() -> None:
    pdf_bytes = _pii_doc()
    result = redact_pattern(
        pdf_bytes,
        "ssn",
        reason="Test audit",
        user_id="abc-123",
        parent_file_id="parent-file-uuid",
    )
    audit = result.audit
    assert audit.reason == "Test audit"
    assert audit.user_id == "abc-123"
    assert audit.parent_file_id == "parent-file-uuid"
    assert audit.redaction_kind == "pattern"
    assert audit.tier_used == "stream_rewrite"
    assert audit.status == "success"
    assert audit.regions_count >= 1
    assert audit.bytes_removed_estimate >= 0
    # The audit must NOT leak the redacted content itself.
    serialised = audit.model_dump_json()
    assert "123-45-6789" not in serialised


# ---------------------------------------------------------------------------
# Scrub helpers
# ---------------------------------------------------------------------------


def test_strip_metadata_wipes_info_dict() -> None:
    pdf_bytes = _pii_doc()
    result = strip_metadata(pdf_bytes, reason="Test strip")
    assert result.audit.redaction_kind == "metadata"
    with pymupdf.open(stream=result.content, filetype="pdf") as doc:
        md = doc.metadata
        # Author / title / subject are wiped
        assert not md.get("author")
        assert not md.get("title")
        assert not md.get("subject")


def test_strip_attachments_returns_audit() -> None:
    pdf_bytes = _pii_doc()
    result = strip_attachments(pdf_bytes, reason="Test")
    assert result.audit.redaction_kind == "attachments"
    assert result.verification_passed


def test_strip_javascript_returns_audit() -> None:
    pdf_bytes = _pii_doc()
    result = strip_javascript(pdf_bytes, reason="Test")
    assert result.audit.redaction_kind == "javascript"


def test_flatten_annotations_returns_audit() -> None:
    pdf_bytes = _pii_doc()
    result = flatten_annotations(pdf_bytes, reason="Test")
    assert result.audit.redaction_kind == "annotations"


def test_strip_all_pii_composite_audit() -> None:
    pdf_bytes = _pii_doc()
    result = strip_all_pii(pdf_bytes, reason="Outbound scrub")
    assert result.audit.redaction_kind == "composite"
    assert "metadata" in result.audit.redaction_params["fields"]
    assert "attached_files" in result.audit.redaction_params["fields"]
    assert "javascript" in result.audit.redaction_params["fields"]


# ---------------------------------------------------------------------------
# from_regions bridge (Phase 3 → Phase 4)
# ---------------------------------------------------------------------------


def test_redact_repeated_regions_strips_detected_header() -> None:
    pdf_bytes = _multipage_legal_doc(page_count=6)
    report = detect_repeated_regions(pdf_bytes)
    assert report.regions, "expected detector to find header+footer"
    result = redact_repeated_regions(
        pdf_bytes, report.regions, reason="FOIA release: strip headers"
    )
    assert result.verification_passed
    assert result.audit.regions_count >= 1
    # Header / footer text gone from every page.
    for page_index in range(report.page_count):
        text = _page_text(result.content, page_index)
        assert "Acme Law Firm" not in text
        assert "Matter no. 12345" not in text


def test_redact_repeated_regions_respects_subset() -> None:
    pdf_bytes = _multipage_legal_doc(page_count=6)
    report = detect_repeated_regions(pdf_bytes)
    if len(report.regions) < 2:
        pytest.skip("need >= 2 detected regions for subset test")
    # Accept only the first region.
    accepted = {report.regions[0].region_id}
    result = redact_repeated_regions(
        pdf_bytes,
        report.regions,
        accepted_region_ids=accepted,
        reason="Strip only header",
    )
    assert result.verification_passed


# ---------------------------------------------------------------------------
# Handler integration smoke
# ---------------------------------------------------------------------------


async def test_handler_redact_async_smoke() -> None:
    handler = PDFHandler(app_name="test_phase4")
    pdf_bytes = _pii_doc()

    sync_r = handler.redact_pattern(pdf_bytes, "ssn", reason="sync")
    async_r = await handler.redact_pattern_async(pdf_bytes, "ssn", reason="async")
    assert sync_r.verification_passed
    assert async_r.verification_passed
    # Byte-deltas should match (deterministic).
    assert sync_r.audit.regions_count == async_r.audit.regions_count


# ---------------------------------------------------------------------------
# Critical sub-agent regressions
# ---------------------------------------------------------------------------


def test_scrub_categories_metadata_only_does_not_strip_javascript() -> None:
    """Regression (R2): /pdf/scrub used to call strip_all_pii unconditionally,
    silently nuking categories the caller did not opt in to. The granular
    helper must touch only the categories its flags select.
    """
    from matrx_files.specific_handlers.pdf import (
        scrub_categories,
    )

    pdf_bytes = _pii_doc()
    result = scrub_categories(pdf_bytes, metadata=True, reason="metadata-only")
    fields = result.audit.redaction_params["fields"]
    assert fields == ["metadata"], f"expected just metadata; got {fields!r}"
    assert result.audit.redaction_kind == "composite"


def test_redact_pattern_flags_threaded_through_verifier() -> None:
    """Regression (R1): the verifier compiled the regex without the caller's
    flags. Case-insensitive redactions could pass verification even when
    case-insensitive survivors existed.
    """
    import re
    import pymupdf

    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        # MIXED-case email so case-insensitive matching can distinguish
        page.insert_text((72, 100), "Email: Foo@Example.COM", fontsize=12)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()

    result = redact_pattern(
        pdf_bytes,
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        reason="case-insensitive email scrub",
        flags=re.IGNORECASE,
    )
    assert result.verification_passed
    out = _page_text(result.content)
    assert "Foo@Example.COM" not in out


def test_redaction_region_preserve_text_default_false() -> None:
    """RedactionRegion.preserve_text defaults to False — the safe default
    where redact rects DO strip text. preserve_text=True is opt-in for
    image-only redaction workflows.
    """
    surgical = RedactionRegion(page_number=1, x0=0, y0=0, x1=10, y1=10)
    image_only = RedactionRegion(
        page_number=1, x0=0, y0=0, x1=10, y1=10, preserve_text=True
    )
    assert surgical.preserve_text is False
    assert image_only.preserve_text is True


def test_redact_regions_preserve_text_keeps_text() -> None:
    """When every region on a page sets preserve_text=True, the redaction
    affects images/graphics only and the underlying text survives.
    """
    doc = pymupdf.open()
    try:
        page = doc.new_page(width=612, height=792)
        page.insert_text((72, 130), "Caption stays", fontsize=12)
        pdf_bytes = doc.tobytes()
    finally:
        doc.close()

    region = RedactionRegion(
        page_number=1, x0=50, y0=115, x1=500, y1=140, preserve_text=True
    )
    result = redact_regions(pdf_bytes, [region], reason="image-only redact")
    # Verification passes because preserve_text regions are skipped in the
    # text-survival check — the engine knows text was kept intentionally.
    assert result.verification_passed is True
    assert result.audit.redaction_params["regions"][0]["preserve_text"] is True
    # And the text actually did survive in the output PDF.
    out = _page_text(result.content)
    assert "Caption stays" in out


def test_redact_regions_verification_tolerance_capped_at_subpixel() -> None:
    """Regression (W2): the verification shrink MUST stay at or below the
    per-pixel threshold at 72 DPI so a genuine surviving glyph (which is at
    least 1pt wide) still fails verification. 0.5pt is the compromise that
    eats PyMuPDF stream-rewrite bbox noise without re-introducing a leak.
    """
    from matrx_files.specific_handlers.pdf.redact.engine import (
        _VERIFY_SHRINK_PT,
    )

    assert _VERIFY_SHRINK_PT <= 0.5, (
        f"Verification shrink {_VERIFY_SHRINK_PT}pt exceeds the 0.5pt cap — "
        "review whether this re-introduces a leak window."
    )
