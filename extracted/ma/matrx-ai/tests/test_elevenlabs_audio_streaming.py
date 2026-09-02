from __future__ import annotations

import asyncio
import base64
import threading
from collections.abc import Iterator

from matrx_connect.context.data_types import AudioStreamChunkData

from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat


class _CapturingEmitter:
    def __init__(self) -> None:
        self.events: list[object] = []
        self.first_event = asyncio.Event()

    async def send_data(self, payload: object) -> None:
        self.events.append(payload)
        self.first_event.set()


async def test_elevenlabs_mp3_chunk_is_emitted_before_provider_stream_finishes() -> None:
    emitter = _CapturingEmitter()
    release_provider = threading.Event()

    def stream() -> Iterator[bytes]:
        yield b"first-mp3-frames"
        release_provider.wait(timeout=2)
        yield b"second-mp3-frames"

    chat = object.__new__(ElevenLabsChat)
    task = asyncio.create_task(
        chat._collect_streaming_bytes(
            stream,
            emitter,
            stream_id="run-123",
            first_seq=0,
            emit_mp3_chunks=True,
        )
    )

    try:
        await asyncio.wait_for(emitter.first_event.wait(), timeout=1)
        assert not task.done(), "the first audio event must not wait for the completed MP3"
    finally:
        release_provider.set()

    audio, next_seq = await asyncio.wait_for(task, timeout=1)
    assert audio == b"first-mp3-framessecond-mp3-frames"
    assert next_seq == 2
    assert len(emitter.events) == 2

    first = emitter.events[0]
    assert isinstance(first, AudioStreamChunkData)
    assert first.stream_id == "run-123"
    assert first.seq == 0
    assert first.encoding == "mp3"
    assert first.mime_type == "audio/mpeg"
    assert base64.b64decode(first.audio_base64) == b"first-mp3-frames"


async def test_non_mp3_stream_is_collected_without_encoded_preview_events() -> None:
    emitter = _CapturingEmitter()
    chat = object.__new__(ElevenLabsChat)

    audio, next_seq = await chat._collect_streaming_bytes(
        lambda: iter((b"complete-file",)),
        emitter,
        stream_id="run-456",
        first_seq=4,
        emit_mp3_chunks=False,
    )

    assert audio == b"complete-file"
    assert next_seq == 4
    assert emitter.events == []


def test_audio_stream_contract_accepts_mp3_and_preserves_pcm_default() -> None:
    mp3 = AudioStreamChunkData(
        stream_id="mp3",
        seq=0,
        audio_base64="AA==",
        mime_type="audio/mpeg",
        encoding="mp3",
        sample_rate=44100,
        bits_per_sample=16,
        channels=1,
    )
    pcm = AudioStreamChunkData(stream_id="pcm", seq=0, audio_base64="AA==")

    assert mp3.encoding == "mp3"
    assert pcm.encoding == "pcm_s16le"
