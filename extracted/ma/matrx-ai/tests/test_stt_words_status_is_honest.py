"""Asking an STT provider for words it cannot supply announces itself (words_status)."""

from __future__ import annotations

import pytest

from matrx_ai.processing.audio import STTRequest, STTResult, STTUsage, STTWord
from matrx_ai.processing.audio.stt import words_status_for


def _usage() -> STTUsage:
    return STTUsage(model="m", matrx_model_name="m", api="a", usage_basis="seconds")


def _req(*gran: str) -> STTRequest:
    return STTRequest(audio_source=b"x", model="m", timestamp_granularities=list(gran) or None)


def test_not_requested_when_word_granularity_absent() -> None:
    res = STTResult(text="t", usage=_usage())
    assert words_status_for(_req("segment"), res, supported=False) == "not_requested"


def test_unsupported_provider_is_flagged_not_silent() -> None:
    res = STTResult(text="t", usage=_usage())
    assert words_status_for(_req("segment", "word"), res, supported=False) == "unsupported_by_provider"


def test_supported_provider_with_no_words_says_none_returned() -> None:
    res = STTResult(text="t", usage=_usage())
    assert words_status_for(_req("word"), res, supported=True) == "none_returned"


def test_words_provided() -> None:
    res = STTResult(text="t", usage=_usage(), words=[STTWord(text="a", start=0, end=1)])
    assert words_status_for(_req("word"), res, supported=True) == "provided"


@pytest.mark.asyncio
async def test_execute_stt_stamps_status_from_the_adapter_capability(monkeypatch) -> None:
    from types import SimpleNamespace

    from matrx_ai.processing.audio import stt as S
    from matrx_ai.providers.unified_client import UnifiedAIClient

    class NoWords:
        async def execute(self, request, profile):
            return STTResult(text="t", usage=_usage())

    class Words(NoWords):
        supports_word_timestamps = True

    async def fake_profile(model, offering_id=None):
        return SimpleNamespace(client_attr="stt", wire_format="fake_stt", model_name="m")

    async def fake_dispatch(send, **kw):
        return await send()

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_call_profile", fake_profile)
    monkeypatch.setattr(UnifiedAIClient, "_dispatch_with_billing_net", staticmethod(fake_dispatch))

    for client, expected in ((NoWords(), "unsupported_by_provider"), (Words(), "none_returned")):
        monkeypatch.setattr(UnifiedAIClient, "fake_stt", client, raising=False)
        res = await S.execute_stt(_req("segment", "word"))
        assert res.words_status == expected
