"""A long ElevenLabs speech script's live ``media_block`` fits the stream journal.

Break named (2026-10-01 review): the speech-script path stamps the whole
per-word ``alignment`` (and the performed script) on the audio block's
metadata, and the live ``media_block`` event carried ALL of it. A podcast
script of a thousand-odd words is well over 64 KiB — the operation-stream
journal's per-frame floor — so one event degraded the journal and broke rejoin
for the run. The live event now sheds the heaviest keys until it fits and
names what it shed (``live_omitted``); the persisted audio part keeps
everything, so a reload still has the full alignment.

SUT: ``ElevenLabsChat.execute`` (speech-script path) through
``_store_and_emit``. Doubles: the ElevenLabs client (returns a timestamped
response for the script it was given), storage, billing and the ambient
context.
"""

from __future__ import annotations

import base64
import json
from typing import Any

import pytest

from matrx_ai.config import TokenUsage, UnifiedConfig, UnifiedMessage

JOURNAL_FRAME_FLOOR_BYTES = 64 * 1024  # operation_stream_queued_bytes' lowest setting

_SENTENCES = [
    "Independent bakeries price sourdough by the cost of time, not flour.",
    "A loaf that proofs for thirty hours carries thirty hours of rent.",
    "Grocery chains sell a par-baked loaf finished in store for half the price.",
    "The baker wins on crust, crumb and the morning queue outside the door.",
]


class _Emitter:
    def __init__(self) -> None:
        self.data: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        return None

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)

    async def send_error(self, **kwargs: Any) -> None:
        return None


class _Ctx:
    def __init__(self, emitter: _Emitter) -> None:
        self.emitter = emitter
        self.request_id = "req-podcast-bakery-ep-9"
        self.user_id = None
        self.is_minor = False


@pytest.fixture
def emitter(monkeypatch: pytest.MonkeyPatch) -> _Emitter:
    import matrx_ai.config.usage_config as usage_config
    import matrx_ai.context.app_context as app_context
    import matrx_ai.media as media
    from matrx_ai.media import MediaPersistResult
    from matrx_ai.providers.eleven_labs import elevenlabs_api

    em = _Emitter()
    monkeypatch.setattr(app_context, "get_app_context", lambda: _Ctx(em))

    async def _billed(*, characters: int, matrx_model_name: str, api: str, **_: Any):
        return TokenUsage(input_tokens=characters, output_tokens=0, matrx_model_name=matrx_model_name, api=api)

    async def _store(content: Any = None, mime_type: str = "", **_: Any) -> MediaPersistResult:
        return MediaPersistResult(
            file_id="0b7c9e52-4f1a-4d3e-9a68-2c5e8f1d7b40",
            url="https://cdn.aimatrx.com/audio/bakery-ep-9.mp3",
            cdn_url="https://cdn.aimatrx.com/audio/bakery-ep-9.mp3",
            download_url="https://cdn.aimatrx.com/audio/bakery-ep-9.mp3?download=1",
            storage_uri="s3://matrx-media/audio/bakery-ep-9.mp3",
            file_path="generations/audio/bakery-ep-9.mp3",
            file_name="bakery-ep-9.mp3",
            mime_type=mime_type or "audio/mpeg",
            size_bytes=3,
            published_to_web=True,
            shown_to=None,
        )

    async def _no_capture(**_: Any) -> None:
        return None

    monkeypatch.setattr(usage_config, "build_character_billed_usage_async", _billed)
    monkeypatch.setattr(media, "save_media_envelope_async", _store)
    monkeypatch.setattr(elevenlabs_api, "stamp_call_meta", lambda **_: None)
    monkeypatch.setattr(elevenlabs_api, "emit_explicit_context_analysis", _no_capture)
    return em


def _chat():
    from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat

    class _Dialogue:
        def convert_with_timestamps(self, **kwargs: Any):
            from elevenlabs.types.audio_with_timestamps_and_voice_segments_response_model import (
                AudioWithTimestampsAndVoiceSegmentsResponseModel,
            )

            text = " ".join(
                (t["text"] if isinstance(t, dict) else t.text) for t in kwargs["inputs"]
            )
            starts = [i * 0.06 for i in range(len(text))]
            return AudioWithTimestampsAndVoiceSegmentsResponseModel.model_validate(
                {
                    "audio_base64": base64.b64encode(b"ID3").decode(),
                    "alignment": {
                        "characters": list(text),
                        "character_start_times_seconds": starts,
                        "character_end_times_seconds": [s + 0.06 for s in starts],
                    },
                    "normalized_alignment": None,
                    "voice_segments": [],
                }
            )

    class _Client:
        text_to_dialogue = _Dialogue()

    chat = ElevenLabsChat.__new__(ElevenLabsChat)
    chat.client = _Client()
    return chat


def _profile():
    from matrx_ai.testing.profile_factory import make_profile

    caps = {"input": ["text"], "output": ["audio"], "features": ["dialogue"], "interaction": "turn"}
    return make_profile(
        model_name="eleven_v3",
        wire_format="elevenlabs_chat",
        capabilities=caps,
        rules={"multi_speaker": {"clamp": {"max": 10}}, "performance_direction": {}},
    ).model_copy(update={"tts_voice_ids": ("kore", "puck"), "tts_default_voice_id": "kore"})


def _script(turn_count: int) -> UnifiedConfig:
    from matrx_ai.config.speech_script_config import SpeechScriptContent

    turns = [
        {
            "speaker": "Maya" if i % 2 == 0 else "Sam",
            "voice": "kore" if i % 2 == 0 else "puck",
            "text": " ".join(_SENTENCES[(i + k) % len(_SENTENCES)] for k in range(3)),
        }
        for i in range(turn_count)
    ]
    content = SpeechScriptContent(turns=turns)
    return UnifiedConfig(model="eleven_v3", messages=[UnifiedMessage(role="user", content=[content])])


def _media_blocks(em: _Emitter) -> list[Any]:
    return [d for d in em.data if getattr(d, "type", None) == "media_block"]


def _persisted_alignment_words(response: Any) -> int:
    audio = response.messages[0].content[0]
    return len(audio.metadata["alignment"]["words"])


async def test_a_long_script_live_block_fits_the_journal_and_names_what_it_shed(emitter) -> None:
    response = await _chat().execute(_script(40), _profile())

    (block_event,) = _media_blocks(emitter)
    wire = block_event.model_dump_json()
    assert len(wire.encode()) <= JOURNAL_FRAME_FLOOR_BYTES, f"{len(wire.encode())} bytes on one frame"
    live_meta = json.loads(wire)["block"]["metadata"]
    assert "alignment" in live_meta.get("live_omitted", [])
    assert "alignment" not in live_meta
    # Nothing is lost: the persisted audio part keeps the whole timeline.
    assert _persisted_alignment_words(response) > 1000


async def test_a_short_script_live_block_keeps_its_alignment(emitter) -> None:
    await _chat().execute(_script(2), _profile())

    (block_event,) = _media_blocks(emitter)
    live_meta = json.loads(block_event.model_dump_json())["block"]["metadata"]
    assert "live_omitted" not in live_meta
    assert len(live_meta["alignment"]["words"]) > 20
    assert live_meta["speech_script"]


def test_every_audio_adapters_builder_sheds_an_oversized_script_too() -> None:
    """The OpenAI / Groq / xAI / Gemini audio paths carry only ``speech_script``
    — a 45-minute episode's script alone outgrows the frame. The shared builder
    sheds it from the live event; a small one rides as-is."""
    from matrx_ai.providers.media_frames import fitted_media_block

    record = {
        "id": "0b7c9e52-4f1a-4d3e-9a68-2c5e8f1d7b40",
        "storage_uri": "s3://matrx-media/audio/bakery-ep-9.mp3",
        "mime_type": "audio/mpeg",
        "size_bytes": 3,
    }
    long_script = {"turns": [{"speaker": "Maya", "text": " ".join(_SENTENCES)} for _ in range(400)]}
    short_script = {"turns": [{"speaker": "Maya", "text": _SENTENCES[0]}]}

    big = fitted_media_block({**record, "metadata": {"speech_script": long_script}}, kind_override="audio")
    small = fitted_media_block({**record, "metadata": {"speech_script": short_script}}, kind_override="audio")

    big_wire = big.model_dump_json()
    assert len(big_wire.encode()) <= JOURNAL_FRAME_FLOOR_BYTES
    assert json.loads(big_wire)["block"]["metadata"]["live_omitted"] == ["speech_script"]
    assert json.loads(small.model_dump_json())["block"]["metadata"]["speech_script"] == short_script
