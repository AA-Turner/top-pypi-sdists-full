"""A provider retry of a live TTS render is a NEW take, never seq 0 again in the old one.

Break named (2026-10-22, run 395d67ed / request 3b008710): Gemini TTS segment
3/4 answered Google 500 INTERNAL, the executor retried the whole provider call
(attempt 1 of 3), and the retry re-rendered the episode from seq 0 under the
SAME stream id (the request id). The journal held frames 0..365 then 0..576
with one identity; every live player read seq 0 as a gap and dropped live
playback for the rest of the render.

SUT: both providers' stream-id door (``_tts_stream_id`` -> ``open_audio_stream``)
and their chunk/end emitters. Double: the emitter (records the wire payloads).

Forcing: two renders in one request keep the stream id, the second render's
take is strictly larger, every chunk and the end marker carry the take of the
render that produced them, and the wire field survives JSON (what the journal
stores and the client reads).
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat
from matrx_ai.providers.google.google_api import GoogleChat


class _Wire:
    def __init__(self) -> None:
        self.frames: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.frames.append(payload)


def _in_request(request_id: str):
    ctx = AppContext(
        emitter=SilentEmitter(),
        user_id="00000000-0000-0000-0000-0000000000aa",
        auth_type="token",
        is_authenticated=True,
        request_id=request_id,
        origin_class="system",
    )
    return set_app_context(ctx)


def _takes(wire: _Wire) -> list[tuple[int, int]]:
    out = []
    for frame in wire.frames:
        data = json.loads(frame.model_dump_json())
        out.append((data["take"], data["seq"]))
    return out


def test_google_retry_opens_a_newer_take_under_the_same_stream_id() -> None:
    token = _in_request("3b008710-1c9a-4015-9257-f1c2a6a6a0c8")
    try:
        chat = GoogleChat()
        wire = _Wire()
        first = chat._tts_stream_id()
        asyncio.run(chat._emit_audio_stream_chunk(wire, first, 0, b"\x01\x00" * 40000, "audio/L16;rate=24000"))
        first_frames = len(wire.frames)
        # The executor's provider retry calls execute() again: a fresh render.
        second = chat._tts_stream_id()
        asyncio.run(chat._emit_audio_stream_chunk(wire, second, 0, b"\x02\x00" * 40000, "audio/L16;rate=24000"))
    finally:
        clear_app_context(token)

    assert first == second == "3b008710-1c9a-4015-9257-f1c2a6a6a0c8"
    takes = _takes(wire)
    take_a = takes[0][0]
    take_b = takes[first_frames][0]
    assert take_b > take_a > 0
    assert takes == [(take_a, i) for i in range(first_frames)] + [
        (take_b, i) for i in range(len(takes) - first_frames)
    ]


def test_elevenlabs_render_stamps_its_take_on_every_chunk() -> None:
    token = _in_request("6f1c0a52-8d1e-4e3b-9a4f-2b7d5c8e9f10")
    try:
        chat = ElevenLabsChat.__new__(ElevenLabsChat)  # no client needed to frame bytes
        wire = _Wire()
        first = chat._tts_stream_id()
        asyncio.run(ElevenLabsChat._emit_audio_stream_chunk(wire, stream_id=first, seq=0, data=b"\xff" * 70000))
        n = len(wire.frames)
        second = chat._tts_stream_id()
        asyncio.run(ElevenLabsChat._emit_audio_stream_chunk(wire, stream_id=second, seq=0, data=b"\xfe" * 10))
    finally:
        clear_app_context(token)

    takes = _takes(wire)
    assert first == second
    assert len({t for t, _ in takes[:n]}) == 1
    assert takes[n][0] > takes[0][0]
    assert takes[n][1] == 0


def test_end_marker_carries_the_current_take() -> None:
    from matrx_connect.context.data_types import AudioStreamEndData

    from matrx_ai.providers.audio_stream import current_audio_take, open_audio_take

    token = _in_request("9c2d4e6f-1a3b-4c5d-8e7f-0a1b2c3d4e5f")
    try:
        take = open_audio_take("end-marker-stream")
        assert current_audio_take("end-marker-stream") == take
        assert open_audio_take("end-marker-stream") > take
        end = AudioStreamEndData(
            stream_id="end-marker-stream", take=current_audio_take("end-marker-stream"), total_chunks=3
        )
    finally:
        clear_app_context(token)
    # A new request never inherits another request's takes.
    token = _in_request("0d1e2f3a-4b5c-4d6e-9f80-a1b2c3d4e5f6")
    try:
        assert current_audio_take("end-marker-stream") == 0
    finally:
        clear_app_context(token)
    assert json.loads(end.model_dump_json())["take"] > take
    # Older servers' payloads (no take) still parse as take 0.
    assert AudioStreamEndData(stream_id="x", total_chunks=1).take == 0
