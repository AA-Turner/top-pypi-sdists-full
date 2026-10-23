"""Framing for live TTS audio on the wire.

A provider hands us audio in whatever segment size it likes — a Gemini PCM
segment can be seconds long, and ElevenLabs' dialogue path returns the whole
episode at once. Each ``audio_stream_chunk`` event is also a frame in the
operation-stream journal (the store a reloaded page rejoins from), whose
per-frame bound is a runtime knob that may be set as low as 64 KiB. One
oversized frame degraded the journal and broke every rejoin for that run
(2026-10-01). So every emitter splits provider audio into frames of at most
``AUDIO_STREAM_CHUNK_MAX_BYTES`` raw bytes (~43 KiB base64, under the knob's
floor), on whole PCM samples. Clients already append frames in ``seq`` order,
so playback is unchanged — and starts sooner. The budget and the partial-image
answer live in ``media_frames``. Guard: tests/test_audio_stream_chunk_framing.py.
"""

from __future__ import annotations

import time
import uuid

from matrx_ai.providers.media_frames import MEDIA_FRAME_MAX_BYTES

#: The one media-frame budget (``media_frames``), named for audio callers.
AUDIO_STREAM_CHUNK_MAX_BYTES = MEDIA_FRAME_MAX_BYTES


def split_audio_frames(
    data: bytes, *, max_bytes: int = AUDIO_STREAM_CHUNK_MAX_BYTES, align: int = 1
) -> list[bytes]:
    """Split ``data`` into ordered pieces of at most ``max_bytes``, each a multiple of ``align``."""
    if not data:
        return []
    align = max(1, align)
    step = max(align, max_bytes - (max_bytes % align))
    return [data[i : i + step] for i in range(0, len(data), step)]


# ---------------------------------------------------------------------------
# Takes — one provider render of a live audio stream
# ---------------------------------------------------------------------------
#
# The stream id is the request id, so it is the SAME across the run's own
# provider retries. A retry re-renders from the start (seq 0), so every render
# opens a new TAKE: a strictly larger number (epoch milliseconds, bumped past
# the previous take of this request), stamped on every chunk and the end
# marker. Clients replace the player when a newer take opens instead of
# reading seq 0 as a gap (2026-10-22, run 395d67ed: a Google 500 on TTS segment
# 3/4 retried the call; frames 0..365 then 0..576 under one id, live playback
# dropped). Epoch-based so a take opened on another replica (crash recovery)
# still sorts after the one before it.

#: ``AppContext.metadata`` key holding ``{stream_id: take}`` for this request's
#: renders. Per request, so it lives and dies with the request — no process table.
_TAKES_KEY = "live_audio_takes"


def _request_context():
    from matrx_ai.context.app_context import try_get_app_context

    return try_get_app_context()


def _request_stream_id() -> str:
    ctx = _request_context()
    rid = getattr(ctx, "request_id", None) if ctx is not None else None
    return str(rid) if rid else uuid.uuid4().hex


def _takes_of_request() -> dict[str, int] | None:
    ctx = _request_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    if not isinstance(metadata, dict):
        return None
    takes = metadata.get(_TAKES_KEY)
    if not isinstance(takes, dict):
        takes = {}
        metadata[_TAKES_KEY] = takes
    return takes


def open_audio_take(stream_id: str) -> int:
    """Open a new take for ``stream_id`` and return its number (strictly larger than the last).

    Outside a request (no AppContext) every render already has a fresh uuid
    stream id, so its take is simply 0.
    """
    takes = _takes_of_request()
    if takes is None:
        return 0
    take = max(time.time_ns() // 1_000_000, int(takes.get(stream_id, 0)) + 1)
    takes[stream_id] = take
    return take


def current_audio_take(stream_id: str) -> int:
    """The take ``stream_id`` is rendering now (0 when none was opened)."""
    takes = _takes_of_request()
    return int(takes.get(stream_id, 0)) if takes else 0


def open_audio_stream() -> str:
    """The live audio stream id for this render (the request id) with a NEW take opened.

    Every TTS render calls this once, before its first chunk; chunk and end
    payloads stamp ``take=current_audio_take(stream_id)``.
    """
    stream_id = _request_stream_id()
    open_audio_take(stream_id)
    return stream_id
