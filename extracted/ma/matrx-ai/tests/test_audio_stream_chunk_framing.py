"""Live TTS audio reaches the stream in frames small enough to journal.

Break named (2026-10-01, clone run e3fe5e59): once the podcast audio stage
forwarded its live audio again, one Gemini PCM segment (several MB once base64
encoded) — and ElevenLabs' dialogue path, which emitted the WHOLE episode as
one event — exceeded the operation-stream journal's per-frame bound. The
journal degraded ("one frame exceeds operation stream journal capacity"), so a
reloaded studio rejoined, replayed, and stopped mid-run ("Live replay stopped").

SUT: both providers' ``_emit_audio_stream_chunk`` (Google PCM, ElevenLabs MP3).
Double: the emitter (records the frames that would reach the wire).

Forcing: the frames' decoded bytes must re-assemble to the exact input, in
order, with contiguous seqs, each frame under the bound, PCM frames on whole
samples, and the returned next-seq equal to the frame count — so
``audio_stream_end.total_chunks`` still matches what the client received.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
from typing import Any

import pytest

from matrx_ai.providers.audio_stream import AUDIO_STREAM_CHUNK_MAX_BYTES
from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat
from matrx_ai.providers.google.google_api import GoogleChat

# The smallest bound an admin may set on the journal (runtime knob
# operation_stream_queued_bytes, min 65536). A frame must fit even then.
_JOURNAL_MIN_QUEUED_BYTES = 65536


class _Wire:
    def __init__(self) -> None:
        self.frames: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.frames.append(payload)


def _audio(n: int) -> bytes:
    # Deterministic, non-repeating bytes (a repeated pattern could hide reordering).
    out = bytearray()
    counter = 0
    while len(out) < n:
        out += hashlib.sha256(counter.to_bytes(8, "big")).digest()
        counter += 1
    return bytes(out[:n])


def _assert_framed(wire: _Wire, original: bytes, first_seq: int, next_seq: int, *, align: int) -> None:
    seqs = [f.seq for f in wire.frames]
    assert seqs == list(range(first_seq, first_seq + len(wire.frames)))
    assert next_seq == first_seq + len(wire.frames)
    pieces = [base64.b64decode(f.audio_base64) for f in wire.frames]
    assert b"".join(pieces) == original
    for piece in pieces:
        assert 0 < len(piece) <= AUDIO_STREAM_CHUNK_MAX_BYTES
        assert len(piece) % align == 0
    for frame in wire.frames:
        assert len(frame.model_dump_json().encode()) < _JOURNAL_MIN_QUEUED_BYTES


@pytest.mark.parametrize("size", [3_000_002, 48_000, 2], ids=["62s-segment", "1s-segment", "one-sample"])
def test_google_pcm_segment_is_framed_on_whole_samples(size: int) -> None:
    wire = _Wire()
    original = _audio(size)
    next_seq = asyncio.run(
        GoogleChat()._emit_audio_stream_chunk(wire, "ep-7c1f", 5, original, "audio/L16;codec=pcm;rate=24000")
    )
    _assert_framed(wire, original, 5, next_seq, align=2)


@pytest.mark.parametrize("size", [4_100_000, 31_000], ids=["whole-episode-mp3", "small-mp3"])
def test_elevenlabs_mp3_is_framed(size: int) -> None:
    wire = _Wire()
    original = _audio(size)
    next_seq = asyncio.run(
        ElevenLabsChat._emit_audio_stream_chunk(wire, stream_id="ep-7c1f", seq=0, data=original)
    )
    _assert_framed(wire, original, 0, next_seq, align=1)
