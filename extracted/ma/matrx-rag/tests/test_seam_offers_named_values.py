"""Every matrx-rag seam call offers its data BY NAME (``offered``), 2026-09-26.

Workflow parity: a host that holds these calls by a mandate hands the named
values to whatever fills it. Before, the grounding claim extractor, the
grounding judge and the image captioner sent only one composed message, so a
WORKFLOW Holder had nothing it could read — the host's consumption pipeline
refused the run for the missing values. A provider written before ``offered``
existed (no such parameter) must keep working untouched.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_rag.grounding as grounding
import matrx_rag.image_pipeline as image_pipeline
from matrx_rag._ext import provider_call_kwargs

_JUDGE_JSON = (
    '[{"claim_index": 1, "verdict": "supported", "confidence": 0.9, '
    '"supporting_chunk_ids": ["c1"], "reasoning": "ok"}]'
)
_CAPTION_JSON = (
    '{"alt_text": "a", "caption": "b", "title": "c", "description": "d", '
    '"keywords": [], "dominant_colors": [], "ocr_text": ""}'
)


class _NamedProvider:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def chat(self, messages, *, model, purpose=None, offered=None, **_: Any) -> str:
        self.calls.append({"purpose": purpose, "offered": offered})
        if purpose == "grounding_judge":
            return _JUDGE_JSON
        if purpose == "image_caption":
            return _CAPTION_JSON
        return '["The sky is blue."]'

    async def chat_stream(
        self, messages, *, model, on_delta, purpose=None, offered=None, **_: Any
    ) -> str:
        self.calls.append({"purpose": purpose, "offered": offered, "stream": True})
        await on_delta(_JUDGE_JSON)
        return _JUDGE_JSON


class _LegacyProvider:
    """Written before ``offered`` existed: no such parameter, no **kwargs."""

    def __init__(self) -> None:
        self.calls = 0

    async def chat(self, messages, *, model, temperature=None, max_tokens=None,
                   response_format=None, timeout=None, purpose=None) -> str:
        self.calls += 1
        return '["claim"]'


async def test_claim_extraction_offers_the_answer(monkeypatch) -> None:
    provider = _NamedProvider()
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: provider)

    await grounding.extract_claims("The sky is blue.")

    assert provider.calls[0]["offered"] == {"answer": "The sky is blue."}


async def test_the_judge_offers_passages_and_claims(monkeypatch) -> None:
    provider = _NamedProvider()
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: provider)

    await grounding.judge_claims(
        ["The sky is blue."], [{"chunk_id": "c1", "content_text": "Skies look blue."}]
    )

    offered = provider.calls[0]["offered"]
    assert set(offered) == {"passages", "claims"}
    assert "c1" in offered["passages"] and "Skies look blue." in offered["passages"]
    assert offered["claims"] == "1. The sky is blue."


async def test_the_captioner_offers_the_image_by_its_file(monkeypatch) -> None:
    provider = _NamedProvider()
    monkeypatch.setattr("matrx_rag._ext.get_llm_provider", lambda: provider)

    await image_pipeline.analyze_image_unified(
        bytes_b64="aGVsbG8=", mime_type="image/png", model="m", file_id="f-123"
    )

    assert provider.calls[0]["offered"] == {"image": {"file_id": "f-123", "mime_type": "image/png"}}


async def test_a_provider_without_offered_still_works(monkeypatch) -> None:
    provider = _LegacyProvider()
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: provider)

    assert await grounding.extract_claims("The sky is blue.") == ["claim"]
    assert provider.calls == 1


def test_provider_call_kwargs_reads_the_signature() -> None:
    assert provider_call_kwargs(_NamedProvider().chat, {"a": 1}) == {"offered": {"a": 1}}
    assert provider_call_kwargs(_LegacyProvider().chat, {"a": 1}) == {}
    assert provider_call_kwargs(_NamedProvider().chat, None) == {}
