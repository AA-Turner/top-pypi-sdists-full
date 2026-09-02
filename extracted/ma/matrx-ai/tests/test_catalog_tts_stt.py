from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.catalog.models import CatalogVoice
from matrx_ai.catalog.resolve import (
    resolve_tts_voice,
    select_tts_default_voice,
    validate_tts_voices,
)
from matrx_ai.config import AudioContent, MessageList, UnifiedMessage
from matrx_ai.processing.audio.audio_preprocessing import preprocess_audio_in_messages
from matrx_ai.processing.audio.groq_transcription import GroqSTT
from matrx_ai.processing.audio.stt import STTRequest, STTUsage
from matrx_ai.testing.profile_factory import make_profile


def _tts_profile(**updates: Any):
    base = make_profile(
        model_name="speech-model",
        provider_model_id="provider-speech-model",
        vendor="groq",
        wire_format="groq_chat",
        capabilities={
            "input": ["text"],
            "output": ["audio"],
            "features": [],
            "interaction": "turn",
            "multilingual": True,
        },
    )
    return base.model_copy(update=updates)


def test_tts_voice_resolution_is_model_linked_and_never_silent() -> None:
    profile = _tts_profile(
        tts_voice_ids=("voice-a", "voice-b"),
        tts_default_voice_id="voice-a",
    )

    assert resolve_tts_voice(profile, None) == "voice-a"
    assert resolve_tts_voice(profile, "voice-b") == "voice-b"
    validate_tts_voices(profile, ["voice-a", "voice-b"])

    with pytest.raises(ValueError, match="voice-missing.*speech-model"):
        resolve_tts_voice(profile, "voice-missing")
    with pytest.raises(ValueError, match="voice-missing.*speech-model"):
        validate_tts_voices(profile, ["voice-a", "voice-missing"])


def test_duplicate_catalog_default_voices_raise_loudly() -> None:
    voices = tuple(
        CatalogVoice(
            provider="vendor",
            provider_voice_id=voice_id,
            name=voice_id,
            metadata={"models": ["speech"], "default_for_models": ["speech"]},
        )
        for voice_id in ("one", "two")
    )
    with pytest.raises(ValueError, match="Multiple default TTS voices.*one.*two"):
        select_tts_default_voice("speech", voices)


def test_catalog_tts_tier_and_model_voice_links_are_data_driven() -> None:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[
            {
                "id": "ep",
                "vendor": "vendor",
                "internal_name": "vendor",
                "display_name": "Vendor",
            }
        ],
        apis=[
            {
                "id": "api",
                "name": "vendor_chat",
                "display_name": "Vendor Chat",
                "translator_key": "mock_chat",
                "rules": {"params": {}, "constraints": []},
            }
        ],
        offerings=[
            {
                "id": "fast",
                "model_id": "fast-model-id",
                "endpoint_id": "ep",
                "api_id": "api",
                "provider_model_id": "fast-model",
                "metadata": {"tts": {"quality_tiers": ["fast"], "is_default": True}},
            },
            {
                "id": "quality",
                "model_id": "quality-model-id",
                "endpoint_id": "ep",
                "api_id": "api",
                "provider_model_id": "quality-model",
                "metadata": {
                    "tts": {"quality_tiers": ["high_quality"], "is_default": True}
                },
            },
        ],
        settings=[],
        models=[
            {"id": "fast-model-id", "name": "fast-model"},
            {"id": "quality-model-id", "name": "quality-model"},
        ],
        voices=[
            {
                "provider": "vendor",
                "provider_voice_id": "fast-voice",
                "name": "Fast Voice",
                "metadata": {
                    "models": ["fast-model"],
                    "default_for_models": ["fast-model"],
                },
            },
            {
                "provider": "vendor",
                "provider_voice_id": "quality-voice",
                "name": "Quality Voice",
                "metadata": {
                    "models": ["quality-model"],
                    "default_for_models": ["quality-model"],
                },
            },
        ],
    )

    assert manager.tts_offering("vendor", "fast").id == "fast"
    assert manager.tts_offering("vendor", "high_quality").id == "quality"
    assert [v.provider_voice_id for v in manager.tts_voices("vendor", "fast-model")] == [
        "fast-voice"
    ]


@pytest.mark.asyncio
async def test_groq_stt_sends_only_catalog_translated_sdk_kwargs(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    class _Transcriptions:
        async def create(self, **kwargs: Any) -> dict[str, Any]:
            captured.update(kwargs)
            return {
                "text": "hello",
                "language": "en",
                "duration": 2.5,
                "segments": [{"avg_logprob": -0.2}],
            }

    class _Audio:
        transcriptions = _Transcriptions()
        translations = _Transcriptions()

    class _Client:
        audio = _Audio()

    async def _prepared(*args: Any, **kwargs: Any) -> tuple[tuple[str, bytes], float]:
        return ("clip.wav", b"audio"), 0.001

    import matrx_ai.processing.audio.groq_transcription as module

    monkeypatch.setattr(module, "_client", lambda: _Client())
    monkeypatch.setattr(module, "prepare_audio_file", _prepared)
    profile = make_profile(
        model_name="whisper-canonical",
        provider_model_id="whisper-wire",
        wire_format="groq_stt",
        vendor="groq",
        rules={
            "temperature": {},
            "language": {},
            "response_format": {},
            "timestamp_granularities": {},
        },
    ).model_copy(
        update={
            "usage_basis": "audio_second_input",
            "offering_metadata": {
                "stt": {"minimum_billed_seconds": 10, "max_file_size_mb": 100}
            }
        }
    )
    request = STTRequest(
        audio_source=b"ignored",
        model="stt-default",
        language="en",
        response_format="verbose_json",
        temperature=0.2,
        timestamp_granularities=["segment"],
    )

    result = await GroqSTT().execute(request, profile)

    assert captured == {
        "file": ("clip.wav", b"audio"),
        "model": "whisper-wire",
        "response_format": "verbose_json",
        "temperature": 0.2,
        "language": "en",
        "timestamp_granularities": ["segment"],
    }
    assert result.usage.matrx_model_name == "whisper-canonical"
    assert result.usage.to_token_usage().input_tokens == 1000
    assert result.usage.to_token_usage().offering_id == profile.offering_id


def test_stt_request_rejects_continuation_prompts() -> None:
    with pytest.raises(ValueError, match="Extra inputs are not permitted"):
        STTRequest.model_validate({
            "audio_source": b"audio",
            "model": "stt-default",
            "stt_prompt": "Key terms: AI Matrx, Rejuvina.",
        })


def test_stt_usage_converts_each_supported_catalog_basis() -> None:
    common = {
        "duration_seconds": 3600.0,
        "billed_duration": 3600.0,
        "model": "wire-model",
        "matrx_model_name": "catalog-model",
        "api": "provider",
    }
    per_second = STTUsage(**common, usage_basis="audio_second_input")
    per_hour = STTUsage(**common, usage_basis="audio_hour_input")

    assert per_second.to_token_usage().input_tokens == 360_000
    assert per_hour.to_token_usage().input_tokens == 1_000_000
    with pytest.raises(ValueError, match="unsupported"):
        STTUsage(**common, usage_basis="minute").to_token_usage()


@pytest.mark.asyncio
async def test_audio_preprocessing_preserves_audio_hour_billing_basis(monkeypatch) -> None:
    audio = AudioContent(base64_data="YXVkaW8=", auto_transcribe=True)

    async def _transcribe(self: AudioContent, force_refresh: bool = False) -> str:
        self.metadata["transcription"] = {
            "from_cache": False,
            "usage": {
                "duration_seconds": 3600,
                "billed_duration": 3600,
                "model": "scribe-wire",
                "matrx_model_name": "scribe-catalog",
                "api": "elevenlabs",
                "offering_id": "scribe-offering",
                "usage_basis": "audio_hour_input",
                "operation": "transcription",
            },
        }
        return "transcribed"

    monkeypatch.setattr(AudioContent, "get_transcription_async", _transcribe)
    messages = MessageList(
        _messages=[UnifiedMessage(role="user", content=[audio])]
    )

    _, usage = await preprocess_audio_in_messages(
        messages, supports_audio_input=False
    )

    assert len(usage) == 1
    assert usage[0].input_tokens == 1_000_000
    assert usage[0].matrx_model_name == "scribe-catalog"
    assert usage[0].offering_id == "scribe-offering"


def test_no_tts_registry_facts_or_direct_groq_transcription_seam() -> None:
    package = Path(__file__).parents[1] / "matrx_ai"
    tts_source = (package / "config" / "tts_config.py").read_text()
    for forbidden in (
        "VALID_MODELS",
        "DEFAULT_MODEL",
        "DEPRECATED_MODELS",
        "QUALITY_TIERS",
        "_VOICES_BY_MODEL",
        "OpenAITTSRegistry",
        "GoogleTTSRegistry",
        "ElevenLabsDialogueRegistry",
    ):
        assert forbidden not in tts_source

    production = "\n".join(
        path.read_text()
        for path in package.rglob("*.py")
        if path.name != "groq_transcription.py" and "tests" not in path.parts
    )
    assert "GroqTranscription" not in production
    assert "from groq import Groq" not in production

    migration = (
        Path(__file__).parents[3]
        / "db"
        / "migrations"
        / "ai_060_catalog_tts_stt_dispatch.sql"
    ).read_text()
    assert "HAVING count(v.id) <> 1" in migration
    assert "translator_key='groq_stt'" in migration
