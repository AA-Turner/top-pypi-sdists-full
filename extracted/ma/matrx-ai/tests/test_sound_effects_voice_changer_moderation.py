"""ElevenLabs Sound Effects + Voice Changer and OpenAI Moderation, at the provider layer.

Each adapter runs for real against a recording SDK stand-in: the tests read what it sent the
provider, what it billed (per second for the two ElevenLabs routes, an honest $0 for moderation),
and the shape it returned. Also: an ElevenLabs Text to Speech call with no voice speaks in the
model's catalog default voice instead of refusing ("No tts_voice configured", 2026-10-29).
"""

from __future__ import annotations

import asyncio
import base64
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import AudioContent, UnifiedConfig
from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import ModelPricing, PricingTier
from matrx_ai.providers.eleven_labs import sound_effects_api, voice_changer_api
from matrx_ai.providers.eleven_labs.sound_effects_api import (
    ElevenLabsSoundEffects,
    effect_length_seconds,
    mp3_seconds,
)
from matrx_ai.providers.eleven_labs.voice_changer_api import ElevenLabsVoiceChanger
from matrx_ai.providers.openai import moderation_api
from matrx_ai.providers.openai.moderation_api import OpenAIModeration, verdict_from_result

DEFAULT_VOICE = "CwhRBWXzGAHq8TQ4Fs17"
OTHER_VOICE = "EXAVITQu4vr4xnSDxMaL"


@pytest.fixture
def warm_pricing():
    saved, warned = uc._pricing_lookup_cache, set(uc._billing_warned)
    tier = lambda: [PricingTier(None, input_price=0, output_price=0.002, cached_input_price=0, usage_basis="audio_second_output")]  # noqa: E731
    uc._pricing_lookup_cache = {
        "eleven_text_to_sound_v2": ModelPricing("eleven_text_to_sound_v2", "elevenlabs", tier()),
        "eleven_multilingual_sts_v2": ModelPricing("eleven_multilingual_sts_v2", "elevenlabs", tier()),
    }
    yield
    uc._pricing_lookup_cache = saved
    uc._billing_warned.clear()
    uc._billing_warned.update(warned)


@pytest.fixture
def fake_store(monkeypatch):
    saved: dict[str, Any] = {}

    async def fake_save(**kw):
        saved.update(kw)
        return SimpleNamespace(url="https://cdn.test/a.mp3", file_id="f1", size_bytes=len(kw["content"]), duration_ms=None)

    monkeypatch.setattr("matrx_ai.media.save_media_envelope_async", fake_save)
    return saved


def _profile(model: str, *, voices: tuple[str, ...] = (), default: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        provider_model_id=model, model_name=model, vendor="elevenlabs",
        tts_voice_ids=voices, tts_default_voice_id=default,
        capabilities=SimpleNamespace(supports_dialogue=False),
    )


# ── the routes exist ──


@pytest.mark.parametrize(
    ("wire", "cls"),
    [("elevenlabs_sound_effects", ElevenLabsSoundEffects), ("elevenlabs_voice_changer", ElevenLabsVoiceChanger),
     ("openai_moderation", OpenAIModeration)],
)
def test_the_client_builds_each_adapter_for_its_wire(wire, cls):
    from matrx_ai import providers
    from matrx_ai.providers.unified_client import UnifiedAIClient

    assert getattr(providers, UnifiedAIClient._PROVIDER_FACTORIES[wire]) is cls


def test_the_three_capabilities_are_canonical_vocabulary():
    from matrx_ai.providers.capability_vocabulary import FEATURE_KEYS

    assert {"sound_effect_generation", "speech_to_speech", "moderation"} <= set(FEATURE_KEYS)


# ── sound effects ──


class _SfxClient:
    def __init__(self, body: bytes):
        self.calls: list[dict] = []
        self.text_to_sound_effects = SimpleNamespace(convert=self._convert)
        self._body = body

    def _convert(self, **kw):
        self.calls.append(kw)
        return iter([self._body[:1000], self._body[1000:]])


def _sfx(monkeypatch, body: bytes) -> ElevenLabsSoundEffects:
    monkeypatch.setattr(sound_effects_api, "get_elevenlabs_client", lambda: _SfxClient(body))
    return ElevenLabsSoundEffects()


def _text_config(model: str, text: str, **extra: Any) -> UnifiedConfig:
    return UnifiedConfig.from_dict({"model": model, "messages": [{"role": "user", "content": text}], **extra})


def test_effect_length_is_clamped_and_empty_lets_the_model_choose():
    assert effect_length_seconds(SimpleNamespace(duration_seconds=0.1)) == 0.5
    assert effect_length_seconds(SimpleNamespace(duration_seconds=99)) == 30.0
    assert effect_length_seconds(SimpleNamespace(duration_seconds=None)) is None
    assert mp3_seconds(b"x" * 32_000) == 2.0


def test_a_sound_effect_is_asked_for_its_length_and_billed_per_second(monkeypatch, warm_pricing, fake_store):
    adapter = _sfx(monkeypatch, b"x" * 64_000)
    cfg = _text_config("eleven_text_to_sound_v2", "door creak", duration_seconds=3)
    resp = asyncio.run(adapter.execute(cfg, _profile("eleven_text_to_sound_v2")))
    call = adapter.client.calls[0]
    assert call["text"] == "door creak" and call["duration_seconds"] == 3.0 and call["model_id"] == "eleven_text_to_sound_v2"
    assert resp.usage.calculate_cost() == pytest.approx(3 * 0.002)
    assert resp.messages[0].content[0].file_id == "f1" and fake_store["provider"] == "elevenlabs"


def test_an_automatic_length_is_billed_by_the_length_returned(monkeypatch, warm_pricing, fake_store):
    adapter = _sfx(monkeypatch, b"x" * 80_000)  # 5 s of 128 kbps mp3
    resp = asyncio.run(adapter.execute(_text_config("eleven_text_to_sound_v2", "rain"), _profile("eleven_text_to_sound_v2")))
    assert "duration_seconds" not in adapter.client.calls[0]
    assert resp.usage.calculate_cost() == pytest.approx(5 * 0.002)


# ── voice changer ──


class _StsClient:
    def __init__(self, body: bytes):
        self.calls: list[dict] = []
        self.speech_to_speech = SimpleNamespace(convert=self._convert)
        self._body = body

    def _convert(self, voice_id, **kw):
        self.calls.append({"voice_id": voice_id, **kw})
        return iter([self._body])


def _sts(monkeypatch, body: bytes) -> ElevenLabsVoiceChanger:
    monkeypatch.setattr(voice_changer_api, "get_elevenlabs_client", lambda: _StsClient(body))
    return ElevenLabsVoiceChanger()


def _speech_config(**extra: Any) -> UnifiedConfig:
    speech = base64.b64encode(b"SPEECH-BYTES").decode()
    return UnifiedConfig.from_dict({
        "model": "eleven_multilingual_sts_v2",
        "messages": [{"role": "user", "content": [{"type": "audio", "base64_data": speech, "mime_type": "audio/mpeg"}]}],
        **extra,
    })


def test_the_source_audio_is_the_user_messages_audio_part():
    part = voice_changer_api.source_audio_part(_speech_config())
    assert isinstance(part, AudioContent)
    assert asyncio.run(voice_changer_api.source_audio_bytes(part)) == b"SPEECH-BYTES"


def test_no_voice_speaks_in_the_models_catalog_default_voice(monkeypatch, warm_pricing, fake_store):
    adapter = _sts(monkeypatch, b"y" * 48_000)  # 3 s out
    profile = _profile("eleven_multilingual_sts_v2", voices=(DEFAULT_VOICE, OTHER_VOICE), default=DEFAULT_VOICE)
    resp = asyncio.run(adapter.execute(_speech_config(), profile))
    call = adapter.client.calls[0]
    assert call["voice_id"] == DEFAULT_VOICE and call["audio"][1] == b"SPEECH-BYTES"
    assert call["model_id"] == "eleven_multilingual_sts_v2"
    assert resp.usage.calculate_cost() == pytest.approx(3 * 0.002)
    assert resp.messages[0].content[0].file_id == "f1"


def test_a_chosen_voice_is_sent_and_an_unknown_one_is_refused(monkeypatch, warm_pricing, fake_store):
    from matrx_ai.catalog.errors import CatalogRoutingError

    profile = _profile("eleven_multilingual_sts_v2", voices=(DEFAULT_VOICE, OTHER_VOICE), default=DEFAULT_VOICE)
    adapter = _sts(monkeypatch, b"y" * 16_000)
    asyncio.run(adapter.execute(_speech_config(tts_voice=OTHER_VOICE), profile))
    assert adapter.client.calls[0]["voice_id"] == OTHER_VOICE
    with pytest.raises(CatalogRoutingError):
        asyncio.run(_sts(monkeypatch, b"y").execute(_speech_config(tts_voice="nope"), profile))


def test_a_request_without_audio_says_so():
    with pytest.raises(ValueError, match="no audio"):
        voice_changer_api.source_audio_part(_text_config("eleven_multilingual_sts_v2", "hi"))


# ── moderation ──


def test_the_verdict_keeps_every_category_with_its_score_highest_first():
    result = SimpleNamespace(
        flagged=True,
        categories={"harassment": True, "violence": False, "self-harm/intent": False},
        category_scores={"harassment": 0.91, "violence": 0.02, "self-harm/intent": 0.001},
    )
    v = verdict_from_result(result, model="omni-moderation-latest")
    assert v["flagged"] is True and v["flagged_categories"] == ["harassment"]
    assert [c["name"] for c in v["categories"]] == ["harassment", "violence", "self-harm/intent"]
    assert v["categories"][0]["score"] == pytest.approx(0.91)


def test_moderation_sends_the_text_and_records_an_honest_zero(monkeypatch):
    sent: dict[str, Any] = {}

    async def create(**kw):
        sent.update(kw)
        return SimpleNamespace(id="modr-1", model="omni-moderation-latest", results=[
            SimpleNamespace(flagged=False, categories={"hate": False}, category_scores={"hate": 0.0003})])

    monkeypatch.setattr(moderation_api, "get_openai_client", lambda: SimpleNamespace(moderations=SimpleNamespace(create=create)))
    resp = asyncio.run(OpenAIModeration().execute(_text_config("omni-moderation-latest", "have a nice day"),
                                                  _profile("omni-moderation-latest")))
    assert sent == {"model": "omni-moderation-latest", "input": "have a nice day"}
    verdict = resp.messages[0].metadata["moderation"]
    assert verdict["flagged"] is False and verdict["categories"] == [{"name": "hate", "flagged": False, "score": 0.0003}]
    assert resp.usage.input_tokens == 0 and resp.usage.output_tokens == 0 and resp.usage.metadata["billing_kind"] == "free:moderation"


# ── ElevenLabs Text to Speech with no voice ──


class _Spoken(Exception):
    pass


def test_elevenlabs_tts_with_no_voice_uses_the_catalog_default_voice(monkeypatch):
    from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat

    sent: dict[str, Any] = {}

    def stream(**kw):
        sent.update(kw)
        raise _Spoken

    adapter = ElevenLabsChat.__new__(ElevenLabsChat)
    adapter.client = SimpleNamespace(text_to_speech=SimpleNamespace(stream=stream))

    async def send_info(*_a, **_k):
        return None

    emitter = SimpleNamespace(send_info=send_info, send_data=send_info)
    profile = _profile("eleven_flash_v2_5", voices=(DEFAULT_VOICE, OTHER_VOICE), default=DEFAULT_VOICE)
    cfg = _text_config("eleven_flash_v2_5", "Hello there.")
    assert cfg.tts_voice_config is None
    with pytest.raises(_Spoken):
        asyncio.run(adapter._execute_tts(cfg, profile, emitter, "eleven_flash_v2_5"))
    assert sent["voice_id"] == DEFAULT_VOICE and sent["text"] == "Hello there."


def test_a_file_id_is_opened_through_the_hosts_file_manager_not_left_unresolved(monkeypatch):
    """The client resolves image and document parts, never audio: a file-id speech part reached the adapter
    with no bytes and no URL, and every Voice to Voice step on a platform file failed (live, 2026-10-29)."""
    from matrx_ai import _ext
    from matrx_ai.providers import unified_client

    opened: list[str] = []

    async def fake_resolve(fm, item):
        opened.append(item.file_id)
        item.base64_data = base64.b64encode(b"FILE-SPEECH").decode()

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: object())
    monkeypatch.setattr(unified_client, "_resolve_media_ref_item", fake_resolve)
    part = AudioContent(file_id="11111111-2222-3333-4444-555555555555", mime_type="audio/mpeg")
    assert asyncio.run(voice_changer_api.source_audio_bytes(part)) == b"FILE-SPEECH"
    assert opened == ["11111111-2222-3333-4444-555555555555"]
