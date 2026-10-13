"""A capture run (Model view) must never make a paid call that is not the main request.

Two layers, each able to fail alone:

1. Declared pre-steps skip themselves and SAY so (audio transcription): no STT call,
   no stand-in in the transcription cache or on the audio part, a ``pre_steps`` entry
   on the capture.
2. The backstop: any httpx send to a paid provider host (an SDK client built without
   the capture hook, a pre-step nobody declared) is refused at the transport.
"""

from __future__ import annotations

import groq as groq_sdk
import pytest

from matrx_ai.config import AudioContent
from matrx_ai.providers import request_capture
from matrx_ai.providers.request_capture import (
    PaidSendBlockedInCapture,
    capturing_provider_request,
)


@pytest.mark.asyncio
async def test_transcription_is_skipped_marked_and_never_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.processing.audio.stt as stt
    from matrx_ai.processing.audio.transcription_cache import get_cache

    calls: list[object] = []

    async def _boom(request: object) -> None:
        calls.append(request)
        raise AssertionError("execute_stt (a paid Groq call) ran inside a capture")

    monkeypatch.setattr(stt, "execute_stt", _boom)
    audio = AudioContent(base64_data="UklGRg==", mime_type="audio/wav", auto_transcribe=True)
    source = f"data:audio/wav;base64,{audio.base64_data}"

    with capturing_provider_request() as slot:
        text = await audio.get_transcription_async()

    assert calls == []
    assert text and "not generated in a Model view capture" in text
    assert [s["kind"] for s in slot.pre_steps] == ["audio_transcription"]
    assert slot.pre_steps[0]["status"] == "skipped"
    assert audio.transcription_result in (None, "")  # the stand-in is not remembered on the part
    assert (
        get_cache().get(audio_source=source, model=audio.transcription_model, language=audio.transcription_language)
        is None
    )


@pytest.mark.asyncio
async def test_unhooked_provider_client_is_refused_at_the_transport_in_capture() -> None:
    """The exact leak: a Groq SDK client built WITHOUT the capture hook."""
    client = groq_sdk.AsyncGroq(api_key="gsk-test-never-sent", max_retries=0)
    with capturing_provider_request():
        with pytest.raises(PaidSendBlockedInCapture) as stop:
            await client.audio.transcriptions.create(file=("a.wav", b"RIFF"), model="whisper-large-v3")
    assert "api.groq.com" in stop.value.url


def test_guard_ignores_non_provider_hosts_and_is_inert_off() -> None:
    import httpx

    request_capture.install_paid_send_guard()
    with capturing_provider_request():
        request_capture.guard_paid_send(httpx.Request("GET", "https://files.example.test/a.wav"))
        with pytest.raises(PaidSendBlockedInCapture):
            request_capture.guard_paid_send(httpx.Request("POST", "https://api.openai.com/v1/embeddings"))
    request_capture.guard_paid_send(httpx.Request("POST", "https://api.openai.com/v1/embeddings"))  # not capturing
