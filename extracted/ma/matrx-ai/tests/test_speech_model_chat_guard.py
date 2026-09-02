"""A speech model must never be translated into a chat-completions request.

Every TTS api_class shares its vendor's CHAT wire route — `groq_tts` and
`groq_standard` are both `groq_chat`, and likewise `openai_tts` -> `openai_chat`,
`google_tts` -> `google_chat`, `xai_tts` -> `xai_chat`, `elevenlabs_tts` ->
`elevenlabs_chat`. `translate_request` used to RAISE for a TTS model because no
translator was registered under its api_class; once dispatch moved to `wire_format`
it started quietly BUILDING a chat request for one instead.

The distinction is recovered from CAPABILITY data, never a name or a route:
`produces_audio and not produces_text`.

`produces_audio` alone would be wrong (xai_realtime emits audio AND text), and an
api_class check would be wrong in the other direction: `distil-whisper-large-v3-en`
carries `api_class='groq_tts'` but is speech-to-TEXT. The capability data is strictly
more correct than the api_class it replaces.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.providers import UnifiedAIClient


def _profile(*, produces_audio: bool, produces_text: bool, wire_format: str, name: str):
    return SimpleNamespace(
        model_name=name,
        provider_model_id=name,
        wire_format=wire_format,
        capabilities=SimpleNamespace(produces_audio=produces_audio, produces_text=produces_text),
    )


def _request():
    return SimpleNamespace(config=SimpleNamespace(model="m", matrx_model_name=""))


def _patch(monkeypatch, profile):
    async def _fake(model_ref, endpoint_hint=None, offering_id=None):
        return profile

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_call_profile", _fake)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("name", "wire_format"),
    [
        ("canopylabs/orpheus-v1-english", "groq_chat"),
        ("gpt-4o-mini-tts", "openai_chat"),
        ("gemini-2.5-flash-preview-tts", "google_chat"),
        ("xai-tts", "xai_chat"),
    ],
)
async def test_tts_model_on_a_chat_route_raises(monkeypatch, name, wire_format):
    _patch(
        monkeypatch,
        _profile(produces_audio=True, produces_text=False, wire_format=wire_format, name=name),
    )
    with pytest.raises(ValueError, match="cannot build a chat request for speech model"):
        await UnifiedAIClient().translate_request(_request())


async def _speech_guard_rejected(monkeypatch, profile) -> bool:
    """True iff the SPEECH guard is what stopped the call.

    A non-speech model passes the guard and proceeds into the real translator, which
    then trips over this test's stub config. That downstream failure is expected and
    irrelevant — all that is asserted is WHICH gate fired.
    """
    _patch(monkeypatch, profile)
    try:
        await UnifiedAIClient().translate_request(_request())
    except Exception as exc:  # noqa: BLE001 — the exception TYPE is not what's under test
        return "cannot build a chat request for speech model" in str(exc)
    return False


@pytest.mark.asyncio
async def test_speech_to_text_model_is_not_blocked(monkeypatch):
    # distil-whisper-large-v3-en: api_class='groq_tts', but input audio -> output TEXT.
    # An api_class-keyed guard would wrongly reject it; the capability data does not.
    assert not await _speech_guard_rejected(
        monkeypatch,
        _profile(
            produces_audio=False,
            produces_text=True,
            wire_format="groq_chat",
            name="distil-whisper-large-v3-en",
        ),
    )


@pytest.mark.asyncio
async def test_model_emitting_both_audio_and_text_is_not_blocked(monkeypatch):
    # xai_realtime is a real conversational model; `produces_audio` alone would kill it.
    assert not await _speech_guard_rejected(
        monkeypatch,
        _profile(
            produces_audio=True, produces_text=True, wire_format="xai_chat", name="realtime-api"
        ),
    )


@pytest.mark.asyncio
async def test_the_guard_is_what_rejects_a_tts_model(monkeypatch):
    # The positive control for the two negatives above: same helper, speech profile.
    assert await _speech_guard_rejected(
        monkeypatch,
        _profile(
            produces_audio=True,
            produces_text=False,
            wire_format="groq_chat",
            name="canopylabs/orpheus-v1-english",
        ),
    )
