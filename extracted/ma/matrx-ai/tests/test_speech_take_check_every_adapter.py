"""Every speech adapter refuses a cut-off paid audio body before storage (class fix of 2026-10-19 stub).

OpenAI is covered by ``test_speech_truncated_take.py``. Here: xAI, Groq, ElevenLabs and Gemini, each with a
fake at the HTTP/SDK boundary returning a 2,688-byte sliver for a long script. Each must raise a RETRYABLE
``incomplete_response`` and must never reach storage. Remove the check from an adapter and its test fails.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.speech.take_check import TruncatedSpeechError, raise_if_truncated_take
from matrx_ai.testing.profile_factory import make_profile

SCRIPT = "Discover the hand-painted ceramic butterfly plate from our studio today. " * 8  # ~560 chars
SLIVER = 2688


class _Emitter:
    async def send_info(self, *_: Any, **__: Any) -> None: ...
    async def send_data(self, *_: Any, **__: Any) -> None: ...


def _config(**kw: Any) -> UnifiedConfig:
    return UnifiedConfig(
        model="m", messages=[UnifiedMessage(role="user", content=[TextContent(text=SCRIPT)])], **kw
    )


def _profile(name: str, vendor: str):
    return make_profile(
        model_name=name,
        wire_format=f"{vendor}_chat",
        capabilities={"input": ["text"], "output": ["audio"], "features": [], "interaction": "turn"},
        rules={},
    ).model_copy(update={"tts_voice_ids": ("v1",), "tts_default_voice_id": "v1"})


@pytest.fixture
def no_storage(monkeypatch):
    """Storage and billing fakes; ``calls`` proves storage was never reached."""
    from matrx_ai import media
    from matrx_ai.config import usage_config

    calls: list[Any] = []

    async def _save(**kw: Any):
        calls.append(kw)
        raise AssertionError("a cut-off take reached storage")

    async def _usage(**_: Any):
        return "BILLED-USAGE"

    monkeypatch.setattr(media, "save_media_envelope_async", _save)
    monkeypatch.setattr(usage_config, "build_character_billed_usage_async", _usage)
    return calls


def _assert_retryable_cut_off(exc: TruncatedSpeechError, calls: list[Any], billed: bool = True) -> None:
    assert exc.error_info.error_type == "incomplete_response" and exc.error_info.is_retryable is True
    assert calls == []
    if billed:
        from matrx_ai.providers.errors import get_billed_usage

        assert get_billed_usage(exc) == "BILLED-USAGE"


def test_the_shared_check_accepts_a_real_take_and_refuses_a_sliver():
    raise_if_truncated_take(provider="x", audio_size_bytes=581_760, characters=556)
    with pytest.raises(TruncatedSpeechError):
        raise_if_truncated_take(provider="x", audio_size_bytes=SLIVER, characters=556)


@pytest.mark.asyncio
async def test_groq_sliver_is_refused(monkeypatch, no_storage):
    from matrx_ai.providers.groq import groq_api

    class _Resp:
        async def read(self) -> bytes:
            return b"\x00" * SLIVER

    class _Speech:
        async def create(self, **_: Any):
            return _Resp()

    chat = groq_api.GroqChat.__new__(groq_api.GroqChat)
    chat.client = SimpleNamespace(audio=SimpleNamespace(speech=_Speech()))
    monkeypatch.setattr(groq_api, "stamp_call_meta", lambda **_: None)
    monkeypatch.setattr(
        "matrx_ai.config.tts_config.GroqTTSRegistry.validate_input_length", lambda t: t
    )
    with pytest.raises(TruncatedSpeechError) as raised:
        await chat._execute_tts(_config(), _profile("orpheus", "groq"), _Emitter(), "orpheus")
    _assert_retryable_cut_off(raised.value, no_storage)


@pytest.mark.asyncio
async def test_xai_sliver_is_refused(monkeypatch, no_storage):
    from matrx_ai.providers.xai import xai_api

    class _Http:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_: Any):
            return False

        async def post(self, *_: Any, **__: Any):
            return SimpleNamespace(content=b"\x00" * SLIVER, raise_for_status=lambda: None)

    chat = xai_api.XAIChat.__new__(xai_api.XAIChat)
    monkeypatch.setattr(xai_api, "make_capture_http_client", lambda **_: _Http())
    monkeypatch.setattr(xai_api, "stamp_call_meta", lambda **_: None)
    monkeypatch.setattr(
        "matrx_ai.config.tts_config.XAITTSRegistry.validate_text_length",
        lambda t, truncate=True: t,
    )
    with pytest.raises(TruncatedSpeechError) as raised:
        await chat._execute_tts(_config(), _profile("grok-tts", "xai"), _Emitter(), "grok-tts")
    _assert_retryable_cut_off(raised.value, no_storage)


@pytest.mark.asyncio
async def test_elevenlabs_sliver_is_refused_at_the_shared_tail(no_storage):
    from matrx_ai.providers.eleven_labs import elevenlabs_api

    chat = elevenlabs_api.ElevenLabsChat.__new__(elevenlabs_api.ElevenLabsChat)
    with pytest.raises(TruncatedSpeechError) as raised:
        await chat._save_and_emit(
            all_audio_bytes=b"\x00" * SLIVER,
            batched_inputs=[[{"text": SCRIPT, "voice_id": "v1"}]],
            tts=None,
            codec="mp3",
            mime_type="audio/mpeg",
            model="eleven_v3",
            matrx_model_name="eleven_v3",
            emitter=_Emitter(),
            stream_id="s",
            seq=0,
            emit_mp3_chunks=False,
            is_dialogue=False,
        )
    _assert_retryable_cut_off(raised.value, no_storage)


def _gemini_chunk(size: int):
    part = SimpleNamespace(inline_data=SimpleNamespace(mime_type="audio/L16;rate=24000", data=b"\x00" * size))
    return SimpleNamespace(candidates=[SimpleNamespace(content=SimpleNamespace(parts=[part]))])


def test_gemini_sliver_is_refused_and_a_real_take_and_a_silent_block_are_not():
    from matrx_ai.providers.google.google_api import GoogleChat

    config = _config()
    with pytest.raises(TruncatedSpeechError) as raised:
        GoogleChat._refuse_truncated_speech([_gemini_chunk(SLIVER)], config)
    assert raised.value.error_info.is_retryable is True
    GoogleChat._refuse_truncated_speech([_gemini_chunk(len(SCRIPT) * 3000)], config)  # healthy PCM
    GoogleChat._refuse_truncated_speech([SimpleNamespace(candidates=[])], config)  # no audio: other class


def test_gemini_check_runs_before_the_paid_call_is_marked_complete_and_before_storage():
    """Wiring guard: both Gemini accept points call the check before from_google_async persists."""
    import inspect

    from matrx_ai.providers.google.google_api import GoogleChat

    src = inspect.getsource(GoogleChat)
    assert src.count("self._refuse_truncated_speech(accumulated_chunks, unified_config)") == 2
    for block in src.split("self._refuse_truncated_speech(accumulated_chunks, unified_config)")[1:]:
        assert block.index("paid_call_completed = True") < block.index("from_google_async")
