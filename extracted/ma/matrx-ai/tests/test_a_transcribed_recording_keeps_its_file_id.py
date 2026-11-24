"""A recording the server transcribes still reaches the agent's turn WITH its file_id.

Live bug (CGU-09 study-coach-media, 2026-11-13): the iPhone sends a spoken answer as an audio part
carrying its ``file_id``. For a model that cannot hear, ``preprocess_audio_in_messages`` replaced the
part with ``[Audio Transcription]: ...`` and nothing else - the ``<attachment kind name id/>`` label
every other media part carries was gone, so the study coach could not hand the recording to
``study_grade_spoken`` unless the person typed the id. The transcript (and the could-not-transcribe
notice) now opens with the same label the media fallback puts on every converted attachment.
"""

from __future__ import annotations

import asyncio

from test_structured_inputs_reach_every_provider import TRANSLATORS

from matrx_ai.config import AudioContent, MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.processing.audio.audio_preprocessing import preprocess_audio_in_messages
from matrx_ai.testing.profile_factory import make_profile

FILE_ID = "6f1c2a9e-4b7d-4e2a-9c31-2d8f5e7a1b04"
SPOKEN = "Mitochondria make the cell's energy as ATP."


def _recording(**overrides) -> AudioContent:
    fields = {
        "file_id": FILE_ID,
        "mime_type": "audio/mp4",
        "transcription_result": SPOKEN,  # already transcribed: no STT call in the test
        "metadata": {"file_name": "spoken-answer.m4a"},
    }
    fields.update(overrides)
    return AudioContent(**fields)


def _transcribe(parts: list, role: str = "user") -> list:
    ml = MessageList(_messages=[UnifiedMessage(role=role, content=parts)])
    out, _usage = asyncio.run(preprocess_audio_in_messages(ml, supports_audio_input=False))
    return out.to_list()[0].content


def test_the_transcript_carries_the_recordings_file_id() -> None:
    parts = _transcribe([TextContent(text="Grade my answer."), _recording()])
    assert len(parts) == 2 and isinstance(parts[1], TextContent)
    text = parts[1].text
    assert text.startswith("<attachment "), text
    assert f'id="{FILE_ID}"' in text and 'kind="audio"' in text
    assert SPOKEN in text  # the transcript itself is unchanged
    assert parts[0].text == "Grade my answer."  # the person's words are untouched


def test_a_failed_transcription_still_names_the_recording(monkeypatch) -> None:
    async def _boom(self, force_refresh: bool = False):
        raise RuntimeError("stt down")

    monkeypatch.setattr(AudioContent, "get_transcription_async", _boom)
    parts = _transcribe([_recording(transcription_result=None)])
    assert f'id="{FILE_ID}"' in parts[0].text
    assert "could not be transcribed" in parts[0].text


def test_the_file_id_reaches_every_wire() -> None:
    parts = _transcribe([TextContent(text="Grade my answer."), _recording()])
    config = UnifiedConfig(model="m", system_instruction="Coach.", messages=MessageList(
        _messages=[UnifiedMessage(role="user", content=parts)]
    ))
    for translator_cls in TRANSLATORS:
        provider = translator_cls.PROVIDER
        profile = make_profile(model_name="m", wire_format=f"{provider}_chat", vendor=provider)
        request = translator_cls().build_request(config, profile)
        assert FILE_ID in repr(request), provider


def test_a_recording_without_identity_is_left_as_before() -> None:
    parts = _transcribe([_recording(file_id=None)])
    assert parts[0].text == f"[Audio Transcription]: {SPOKEN}"


def test_a_recording_with_only_a_url_never_puts_the_url_in_a_label() -> None:
    signed = "https://cdn.example.test/spoken-answer.m4a?X-Amz-Signature=abc123"
    parts = _transcribe([_recording(file_id=None, url=signed)])
    assert signed not in parts[0].text and not parts[0].text.startswith("<attachment ")
    assert parts[0].text == f"[Audio Transcription]: {SPOKEN}"
