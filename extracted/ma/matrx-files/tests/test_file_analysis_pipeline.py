"""End-to-end tests for the file-analysis pipeline.

Uses an in-memory PersistenceProtocol implementation + a no-op OCR provider
so the tests run without any external services.

Covers:
  - non-PDF mime types → status='not_applicable' with a stub row
  - PDF run through every fast detector (metadata, page_classification,
    text_extraction_native, redaction_candidates, repeated_regions,
    tables, duplicate_pages_*)
  - inline-vs-overflow payload split with a low INLINE_PAYLOAD_LIMIT
  - reversible redaction mask + restore round-trip via the in-memory store
"""

from __future__ import annotations

import asyncio
from typing import Any

import pymupdf
import pytest

# Importing the PDF analyze package registers all detector factories.
import matrx_files.specific_handlers.pdf.analyze  # noqa: F401
from matrx_files.analysis import (
    AnalysisOutcome,
    analyze_file,
    DETECTOR_FACTORIES,
)
from matrx_files.specific_handlers.pdf.redact import (
    InMemoryMappingStore,
    RedactionCandidate,
    mask_with_mapping,
    restore_text_from_response,
)


# ── stub persistence ─────────────────────────────────────────────────────────

class StubPersistence:
    def __init__(self) -> None:
        self.head: dict[str, Any] = {}
        self.results: list[dict[str, Any]] = []
        self.progress_updates: list[dict[str, Any]] = []
        self.extended_payloads: dict[str, str] = {}

    async def upsert_analysis_start(self, **kw: Any) -> None:
        self.head.update({**kw, "status": "running"})

    async def update_progress(self, **kw: Any) -> None:
        self.progress_updates.append(kw)

    async def record_detector_run(self, **kw: Any) -> None:
        pass

    async def insert_result(self, **kw: Any) -> None:
        self.results.append(kw)

    async def write_extended_payload(self, **kw: Any) -> str:
        uri = (
            f"mem://{kw['file_id']}/{kw['detector_kind']}/"
            f"{kw['confidence_tier']}__{kw['detector_version']}.json"
        )
        self.extended_payloads[uri] = kw["payload_json"]
        return uri

    async def finalize(self, **kw: Any) -> None:
        self.head.update(kw)

    async def stamp_cld_files_metadata(self, **kw: Any) -> None:
        self.head["stamped_metadata"] = kw["analysis_summary"]


class NoopOcrProvider:
    provider_id = "noop"

    async def ocr_page_image(self, image_bytes: bytes) -> str:
        return ""


# ── fixtures ────────────────────────────────────────────────────────────────

def _pdf_with_pii_and_repeats() -> bytes:
    doc = pymupdf.open()
    try:
        for i in range(3):
            page = doc.new_page(width=612, height=792)
            page.insert_text((72, 50), f"Page {i+1} of 3", fontsize=10)  # repeated header
            page.insert_text((72, 100), "Patient: Jane Doe", fontsize=12)
            page.insert_text((72, 130), "SSN: 123-45-6789", fontsize=12)
            page.insert_text((72, 160), "Phone: (555) 867-5309", fontsize=12)
            page.insert_text((72, 190), "Email: jane@example.com", fontsize=12)
            page.insert_text((72, 220), "MRN: 99887766", fontsize=12)
            page.insert_text((72, 280), f"Body for page {i+1}", fontsize=12)
            page.insert_text((72, 760), "CONFIDENTIAL — DO NOT COPY", fontsize=8)  # repeated footer
        return doc.tobytes()
    finally:
        doc.close()


def _pdf_with_duplicate_pages() -> bytes:
    doc = pymupdf.open()
    try:
        for i in range(4):
            page = doc.new_page(width=612, height=792)
            # First two pages identical text content.
            text = "Same content for duplicate detection." if i < 2 else f"Unique page {i}"
            page.insert_text((72, 100), text, fontsize=12)
        return doc.tobytes()
    finally:
        doc.close()


# ── tests ────────────────────────────────────────────────────────────────────

async def test_detector_factories_registered() -> None:
    expected = {
        "metadata",
        "page_classification",
        "text_extraction_native",
        "text_extraction_ocr",
        "redaction_candidates",
        "repeated_regions",
        "tables",
        "duplicate_pages_exact",
        "duplicate_pages_normalized",
        "duplicate_pages_shingle",
        "duplicate_pages_structural",
        "duplicate_pages_visual",
        "embedded_images",
    }
    missing = expected - set(DETECTOR_FACTORIES.keys())
    assert not missing, f"detector factories missing: {missing}"


async def test_non_pdf_writes_not_applicable_stub() -> None:
    p = StubPersistence()
    outcome = await analyze_file(
        file_id="file-1",
        owner_id="user-1",
        mime_type="text/plain",
        bytes_in_memory=b"hello world",
        persistence=p,
        ocr_provider=NoopOcrProvider(),
    )
    assert isinstance(outcome, AnalysisOutcome)
    assert outcome.status == "not_applicable"
    assert outcome.results_count == 0
    assert p.head.get("status") == "not_applicable"


async def test_pdf_full_pipeline_produces_results() -> None:
    p = StubPersistence()
    pdf_bytes = _pdf_with_pii_and_repeats()
    outcome = await analyze_file(
        file_id="file-2",
        owner_id="user-1",
        mime_type="application/pdf",
        bytes_in_memory=pdf_bytes,
        persistence=p,
        ocr_provider=NoopOcrProvider(),
    )
    assert outcome.status in ("complete", "partial"), f"unexpected: {outcome}"
    kinds = {r["detector_kind"] for r in p.results}
    # The fast tier always lands.
    assert "metadata" in kinds
    assert "page_classification" in kinds
    assert "text_extraction_native" in kinds
    assert "redaction_candidates" in kinds
    assert "repeated_regions" in kinds
    assert "tables" in kinds
    assert "duplicate_pages_exact" in kinds
    # The slow tier eventually too.
    assert "duplicate_pages_visual" in kinds

    # Tiered detectors should appear at all three tiers.
    redaction_tiers = {
        r["confidence_tier"] for r in p.results if r["detector_kind"] == "redaction_candidates"
    }
    assert redaction_tiers == {"low", "medium", "high"}

    # At least one PII pattern should fire — synthetic doc has SSN, email,
    # phone, MRN.
    pii_results = [r for r in p.results if r["detector_kind"] == "redaction_candidates"]
    total_spans = 0
    for r in pii_results:
        payload = r.get("payload") or {}
        total_spans += len(payload.get("spans", []))
    assert total_spans > 0


async def test_duplicate_pages_groups_match() -> None:
    p = StubPersistence()
    pdf_bytes = _pdf_with_duplicate_pages()
    await analyze_file(
        file_id="file-3",
        owner_id="user-1",
        mime_type="application/pdf",
        bytes_in_memory=pdf_bytes,
        persistence=p,
        ocr_provider=NoopOcrProvider(),
    )
    exact = [r for r in p.results if r["detector_kind"] == "duplicate_pages_exact"]
    assert exact, "expected duplicate_pages_exact result"
    groups = (exact[0].get("payload") or {}).get("groups") or []
    assert any(set(g["pages"]) == {1, 2} for g in groups)


async def test_inline_payload_overflows_to_extended_storage() -> None:
    p = StubPersistence()
    pdf_bytes = _pdf_with_pii_and_repeats()
    await analyze_file(
        file_id="file-4",
        owner_id="user-1",
        mime_type="application/pdf",
        bytes_in_memory=pdf_bytes,
        persistence=p,
        ocr_provider=NoopOcrProvider(),
        inline_payload_limit_bytes=128,  # tiny — every payload overflows
    )
    # Every row should have payload_uri set, payload None.
    rows_with_uri = [r for r in p.results if r.get("payload_uri") is not None]
    assert rows_with_uri, "expected at least one overflow payload"
    assert all(r.get("payload") is None for r in rows_with_uri)
    assert all(r["payload_uri"].startswith("mem://") for r in rows_with_uri)


async def test_reversible_redaction_roundtrip() -> None:
    pdf_bytes = _pdf_with_pii_and_repeats()
    spans = [
        RedactionCandidate(
            pattern_id="ssn_us",
            page_number=1,
            bbox={"x0": 100, "y0": 120, "x1": 250, "y1": 145},
            original_text="123-45-6789",
            confidence_tier="high",
        ),
        RedactionCandidate(
            pattern_id="email",
            page_number=1,
            bbox={"x0": 100, "y0": 180, "x1": 300, "y1": 205},
            original_text="jane@example.com",
            confidence_tier="medium",
        ),
    ]
    store = InMemoryMappingStore()
    result = await mask_with_mapping(
        pdf_bytes,
        spans,
        file_id="file-5",
        redacted_by="user-1",
        mapping_store=store,
        mode="reversible",
    )
    assert result.mapping_count == 2
    assert result.session_id
    assert result.session_key_b64, "expected fresh per-session AES key"

    # Simulate an LLM-style consumer: text version contains both substitutes.
    fake_response = (
        "The patient with SSN [SSN_001] and email [EMAIL_001] needs follow-up."
    )
    restored = await restore_text_from_response(
        fake_response,
        session_id=result.session_id,
        session_key_b64=result.session_key_b64,
        mapping_store=store,
    )
    assert "123-45-6789" in restored
    assert "jane@example.com" in restored
    assert "[SSN_001]" not in restored
    assert "[EMAIL_001]" not in restored


async def test_annotation_mode_does_not_modify_file() -> None:
    pdf_bytes = _pdf_with_pii_and_repeats()
    spans = [
        RedactionCandidate(
            pattern_id="ssn_us",
            page_number=1,
            bbox={"x0": 100, "y0": 120, "x1": 250, "y1": 145},
            original_text="123-45-6789",
            confidence_tier="high",
        ),
    ]
    store = InMemoryMappingStore()
    result = await mask_with_mapping(
        pdf_bytes,
        spans,
        file_id="file-6",
        redacted_by="user-1",
        mapping_store=store,
        mode="annotation",
    )
    assert result.mode == "annotation"
    assert result.file_bytes == pdf_bytes  # unchanged
    assert result.mapping_count == 1


async def test_wrong_key_fails_decryption_safely() -> None:
    """Restoring with the wrong key returns the substitutes unchanged."""
    import base64
    import os
    spans = [
        RedactionCandidate(
            pattern_id="ssn_us",
            page_number=1,
            bbox={"x0": 100, "y0": 120, "x1": 250, "y1": 145},
            original_text="123-45-6789",
            confidence_tier="high",
        ),
    ]
    store = InMemoryMappingStore()
    result = await mask_with_mapping(
        _pdf_with_pii_and_repeats(),
        spans,
        file_id="file-wrong-key",
        redacted_by="user-1",
        mapping_store=store,
    )
    wrong_key = base64.b64encode(os.urandom(32)).decode("ascii")
    restored = await restore_text_from_response(
        "The SSN is [SSN_001].",
        session_id=result.session_id,
        session_key_b64=wrong_key,
        mapping_store=store,
    )
    # Wrong key — substitute stays put, original is NOT leaked.
    assert "[SSN_001]" in restored
    assert "123-45-6789" not in restored


async def test_revoked_session_blocks_restore() -> None:
    spans = [
        RedactionCandidate(
            pattern_id="ssn_us",
            page_number=1,
            bbox={"x0": 100, "y0": 120, "x1": 250, "y1": 145},
            original_text="123-45-6789",
            confidence_tier="high",
        ),
    ]
    store = InMemoryMappingStore()
    result = await mask_with_mapping(
        _pdf_with_pii_and_repeats(),
        spans,
        file_id="file-7",
        redacted_by="user-1",
        mapping_store=store,
    )
    await store.revoke_session(session_id=result.session_id)
    restored = await restore_text_from_response(
        "The SSN is [SSN_001].",
        session_id=result.session_id,
        session_key_b64=result.session_key_b64 or "",
        mapping_store=store,
    )
    # Substitute should NOT be replaced after revocation.
    assert "[SSN_001]" in restored
    assert "123-45-6789" not in restored
