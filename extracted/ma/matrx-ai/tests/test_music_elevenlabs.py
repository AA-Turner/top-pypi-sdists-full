"""ElevenLabs Eleven Music: billed per generated SECOND, an exact length, a cut-off body is never a bed, a declined wording
comes back as an empty content-filter response (so the caller's one safer-wording retry works for every music model).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import ModelPricing, PricingTier, build_audio_seconds_billed_usage
from matrx_ai.providers.eleven_labs import music_api
from matrx_ai.providers.eleven_labs.music_api import (
    ElevenLabsMusic,
    declined_status,
    music_length_seconds,
    music_prompt_text,
)
from matrx_ai.speech.take_check import TruncatedSpeechError, raise_if_truncated_music, truncated_music_reason


@pytest.fixture
def warm_pricing():
    saved, warned = uc._pricing_lookup_cache, set(uc._billing_warned)
    uc._billing_warned.clear()
    uc._pricing_lookup_cache = {
        "eleven_music_v2_5": ModelPricing("eleven_music_v2_5", "elevenlabs", [PricingTier(None, input_price=0, output_price=0.0025, cached_input_price=0, usage_basis="audio_second_output")]),
        "token-model": ModelPricing("token-model", "elevenlabs", [PricingTier(None, input_price=1, output_price=2, cached_input_price=0, usage_basis=None)]),
    }
    yield
    uc._pricing_lookup_cache = saved
    uc._billing_warned.clear()
    uc._billing_warned.update(warned)


def test_a_music_second_is_billed_at_the_per_second_price(warm_pricing):
    u = build_audio_seconds_billed_usage(seconds=60, matrx_model_name="eleven_music_v2_5", provider_model_name="music_v2_5", api="elevenlabs")
    assert u.calculate_cost() == pytest.approx(0.15)  # $0.15 a minute: the real cost, never $0 and never a token figure
    assert u.metadata["billed_audio_seconds"] == 60 and u.metadata["billing_kind"] == "synthetic:audio_second_output"


def test_a_basis_that_is_not_per_second_is_loud_and_zero_not_silent(warm_pricing, capsys):
    u = build_audio_seconds_billed_usage(seconds=60, matrx_model_name="token-model", provider_model_name="x", api="elevenlabs")
    assert u.output_tokens == 0 and u.metadata["billing_kind"] == "uncomputable_music_no_usage"


def test_take_check_floors_music_by_seconds():
    assert truncated_music_reason(2_000, 60) is not None  # a 2 KB stub for a minute of music
    assert truncated_music_reason(960_000, 60) is None  # a real 128 kbps minute
    with pytest.raises(TruncatedSpeechError) as exc:
        raise_if_truncated_music(provider="elevenlabs", audio_size_bytes=2_000, seconds=60, usage="u")
    assert exc.value.error_info.is_retryable and exc.value.error_info.error_type == "incomplete_response"


def test_length_is_exact_and_clamped_to_the_provider_limits():
    cfg = lambda n: SimpleNamespace(duration_seconds=n)  # noqa: E731
    assert music_length_seconds(cfg(62)) == 62
    assert music_length_seconds(cfg(1)) == 3
    assert music_length_seconds(cfg(9999)) == 300
    assert music_length_seconds(cfg(None)) == music_api.DEFAULT_MUSIC_SECONDS


def test_prompt_is_the_last_user_text():
    msg = lambda r, t: SimpleNamespace(role=r, content=[SimpleNamespace(text=t)])  # noqa: E731
    cfg = SimpleNamespace(messages=[msg("user", "old"), msg("assistant", "x"), msg("user", "warm bed")])
    assert music_prompt_text(cfg) == "warm bed"


def test_declined_status_reads_the_provider_body():
    assert declined_status(SimpleNamespace(body={"detail": {"status": "bad_prompt"}})) == "bad_prompt"
    assert declined_status(SimpleNamespace(body={"detail": {"status": "quota_exceeded"}})) is None
    assert declined_status(RuntimeError("x")) is None


class _Client:
    def __init__(self, body: bytes | Exception):
        self.calls: list[dict] = []
        self.music = SimpleNamespace(compose=self._compose)
        self._body = body

    def _compose(self, **kw):
        self.calls.append(kw)
        if isinstance(self._body, Exception):
            raise self._body
        return iter([self._body[:1000], self._body[1000:]])


def _adapter(monkeypatch, body):
    monkeypatch.setattr(music_api, "get_elevenlabs_client", lambda: _Client(body))
    return ElevenLabsMusic()


def _config(seconds=20):
    user = SimpleNamespace(role="user", content=[SimpleNamespace(text="Warm acoustic bed")])
    return SimpleNamespace(model="eleven_music_v2_5", duration_seconds=seconds, messages=[user])


_PROFILE = SimpleNamespace(provider_model_id="music_v2_5")


def test_the_call_asks_for_the_exact_length_instrumental(monkeypatch, warm_pricing):
    adapter = _adapter(monkeypatch, b"x" * 400_000)
    saved = {}

    async def fake_save(**kw):
        saved.update(kw)
        return SimpleNamespace(url="u", file_id="f1", size_bytes=len(kw["content"]), duration_ms=20_000)

    monkeypatch.setattr("matrx_ai.media.save_media_envelope_async", fake_save)
    resp = asyncio.run(adapter.execute(_config(20), _PROFILE))
    call = adapter.client.calls[0]
    assert call["music_length_ms"] == 20_000 and call["force_instrumental"] is True and call["model_id"] == "music_v2_5"
    assert resp.usage.calculate_cost() == pytest.approx(20 * 0.0025)
    assert resp.messages[0].content[0].file_id == "f1" and saved["provider"] == "elevenlabs"


def test_a_cut_off_body_is_a_retryable_failure_carrying_the_spend(monkeypatch, warm_pricing):
    adapter = _adapter(monkeypatch, b"x" * 2_000)  # 2 KB for 20 s
    with pytest.raises(TruncatedSpeechError) as exc:
        asyncio.run(adapter.execute(_config(20), _PROFILE))
    assert exc.value.error_info.is_retryable


def test_a_declined_wording_is_an_empty_content_filter_response_not_an_error(monkeypatch, warm_pricing):
    err = RuntimeError("bad prompt")
    err.body = {"detail": {"status": "bad_prompt"}}  # type: ignore[attr-defined]
    resp = asyncio.run(_adapter(monkeypatch, err).execute(_config(), _PROFILE))
    assert resp.finish_reason.value == "content_filter" and resp.usage is None
    assert resp.messages[0].content == [] and resp.messages[0].metadata["finish_reason"] == "content_filter"


def test_any_other_provider_failure_still_raises(monkeypatch, warm_pricing):
    with pytest.raises(RuntimeError):
        asyncio.run(_adapter(monkeypatch, RuntimeError("503")).execute(_config(), _PROFILE))


def test_the_client_can_build_the_music_adapter_for_its_wire():
    """The dispatch table names a factory; the provider package must declare its module (a missing case was a silent
    matrx_internal_error on the first live call)."""
    from matrx_ai import providers
    from matrx_ai.providers.unified_client import UnifiedAIClient

    factory = UnifiedAIClient._PROVIDER_FACTORIES["elevenlabs_music"]
    assert getattr(providers, factory) is ElevenLabsMusic
