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
