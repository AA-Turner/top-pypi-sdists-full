"""A check that could not run says so, durably — never a plausible degraded result.

Found 2026-09-25 (review of the mandate conversion): claim extraction that could
not run fell back to "the whole answer is ONE claim" with a warning log, and the
image caption call returned ``{}`` on any failure so ingestion reported the
generic "vision_analysis_failed_or_empty".
"""

from __future__ import annotations

import pytest

import matrx_rag
from matrx_rag import grounding, image_pipeline


class _FailingProvider:
    async def chat(self, messages, **kwargs):
        raise RuntimeError("holder refused: no Holder for rag.grounding_claim_extract")

    async def chat_stream(self, messages, **kwargs):
        raise RuntimeError("never reached")


@pytest.fixture
def captured(monkeypatch):
    seen: list[dict] = []

    async def _capture(exc, *, kind, **fields):
        seen.append({"kind": kind, "error": str(exc), **fields})

    monkeypatch.setattr("matrx_utils.capture_error", _capture)
    matrx_rag._ext._reset_for_tests()
    matrx_rag.configure(llm_provider=_FailingProvider())
    yield seen
    matrx_rag._ext._reset_for_tests()


async def test_claim_extraction_failure_is_an_unavailable_report(captured) -> None:
    report = await grounding.verify_grounded(answer="Paris is in France.", retrieved=[])

    assert report.error and "Claim extraction failed" in report.error
    assert report.claims == []
    assert captured and captured[0]["kind"] == "rag_grounding_unavailable"


async def test_vision_failure_raises_a_named_error(captured) -> None:
    with pytest.raises(image_pipeline.VisionAnalysisError, match="caption call failed"):
        await image_pipeline.analyze_image_unified(
            bytes_b64="aGVsbG8=", mime_type="image/png", model="any"
        )
