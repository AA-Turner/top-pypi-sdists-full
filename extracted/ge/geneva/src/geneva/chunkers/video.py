# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Video chunking UDTF.

Splits a video (raw bytes) into fixed-length clips, emitting one output row per
clip. Each row carries the clip's timing metadata and a standalone re-encoded
mp4 (``clip_bytes``). Modeled on ``chunk_audio_udtf`` (bytes in, one row per
fixed window out), differing only in payload.

Uses PyAV (``av``) for demux/decode, duration metadata, and mp4 muxing. PyAV is
imported lazily inside the functions so importing this module never requires the
optional dependency.
"""

from __future__ import annotations

import io
import logging
from fractions import Fraction
from typing import TYPE_CHECKING, Any, cast

import pyarrow as pa

import geneva

if TYPE_CHECKING:
    from collections.abc import Iterator

_LOG = logging.getLogger(__name__)

DEFAULT_VIDEO_CHUNK_SECONDS = 1.0

# Codec used to re-encode each clip. ``libx264`` is bundled in PyAV's wheels and
# produces standard, widely-decodable H.264 mp4 output.
_CLIP_CODEC = "libx264"

_VIDEO_CLIP_SCHEMA = pa.schema(
    [
        # Echoed from the source so clips correlate back to their video.
        pa.field("video_id", pa.string()),
        pa.field("chunk_id", pa.int32()),
        pa.field("start_sec", pa.float32()),
        pa.field("end_sec", pa.float32()),
        pa.field(
            "clip_bytes",
            pa.large_binary(),
            # Clips can be large; store them as a blob column.
            metadata={b"lance-encoding:blob": b"true"},
        ),
    ]
)


def _clip_windows(
    duration: float,
    chunk_seconds: float,
    max_clips: int | None = None,
) -> list[tuple[float, float]]:
    """Split ``[0, duration)`` into fixed-length ``[start, end)`` windows.

    The final window is clamped to ``duration``. Returns an empty list for a
    non-positive duration or chunk length, or a non-positive ``max_clips``.
    Honors an optional ``max_clips`` cap.
    """
    if duration <= 0 or chunk_seconds <= 0:
        return []
    if max_clips is not None and max_clips <= 0:
        return []

    windows: list[tuple[float, float]] = []
    start = 0.0
    while start < duration:
        end = min(start + chunk_seconds, duration)
        windows.append((start, end))
        if max_clips is not None and len(windows) >= max_clips:
            break
        start += chunk_seconds
    return windows


def _probe_video(video_bytes: bytes) -> float:
    """Return the video duration in seconds via PyAV container metadata."""
    import av

    # PyAV lacks complete type stubs; treat containers/streams as Any.
    with cast("Any", av.open(io.BytesIO(video_bytes))) as container:
        stream = container.streams.video[0]
        if stream.duration is not None and stream.time_base is not None:
            return float(stream.duration * stream.time_base)
        if container.duration is not None:
            # ``container.duration`` is expressed in ``av.time_base`` (microseconds).
            return float(container.duration) / float(av.time_base)
    return 0.0


def _encode_clip(video_bytes: bytes, start: float, end: float) -> bytes | None:
    """Re-encode frames in ``[start, end)`` into a standalone mp4.

    Returns the mp4 bytes, or ``None`` if the window contains no frames.
    """
    import av

    out_buf = io.BytesIO()
    wrote = 0

    # PyAV lacks complete type stubs; treat containers/streams as Any.
    with cast("Any", av.open(io.BytesIO(video_bytes))) as inp:
        in_stream = inp.streams.video[0]
        rate = in_stream.average_rate or in_stream.guessed_rate or Fraction(30, 1)
        # Constant-frame-rate output: one pts tick per frame at 1/rate.
        time_base = Fraction(1, 1) / rate

        with cast("Any", av.open(out_buf, mode="w", format="mp4")) as out:
            out_stream = out.add_stream(_CLIP_CODEC, rate=rate)
            out_stream.width = in_stream.codec_context.width
            out_stream.height = in_stream.codec_context.height
            out_stream.pix_fmt = "yuv420p"
            out_stream.codec_context.time_base = time_base
            # Single-threaded encode: avoids EPERM from thread spawning in
            # restricted runtimes (sandboxes, Ray workers).
            out_stream.codec_context.thread_count = 1
            out_stream.codec_context.thread_type = "NONE"

            # Seek to the keyframe at/just before ``start`` to avoid decoding the
            # whole video for every clip; frames before ``start`` are filtered out.
            if start > 0 and in_stream.time_base is not None:
                inp.seek(int(start / in_stream.time_base), stream=in_stream)

            for frame in inp.decode(in_stream):
                ts = frame.time
                if ts is None:
                    continue
                if ts < start:
                    continue
                if ts >= end:
                    break
                # Re-base each frame onto the clip-local CFR timeline.
                frame.pts = wrote
                frame.time_base = time_base
                for packet in out_stream.encode(frame):
                    out.mux(packet)
                wrote += 1

            # Flush the encoder.
            for packet in out_stream.encode():
                out.mux(packet)

    if wrote == 0:
        return None
    return out_buf.getvalue()


def chunk_video_udtf(
    chunk_seconds: float = DEFAULT_VIDEO_CHUNK_SECONDS,
    max_video_s: float | None = None,
    num_clips: int | None = None,
) -> geneva.Chunker:
    """Create a scalar UDTF that chunks a video into fixed-length clips.

    Each clip is yielded as a separate output row carrying its timing metadata
    and a standalone re-encoded mp4 (``clip_bytes``), and is materialised
    directly by ``create_udtf_view`` / ``refresh()``.

    The source query must project a string ``video_id`` column and a
    ``video_bytes`` column. ``video_id`` is echoed onto every clip row so clips
    correlate back to their source video by a stable, caller-controlled key.
    The raw ``video_bytes`` are read to cut clips but are **not** copied into
    the view (``inherit_input_columns=False``), so there is no per-clip byte
    duplication.

    Parameters
    ----------
    chunk_seconds : float
        Duration of each clip in seconds. Defaults to
        ``DEFAULT_VIDEO_CHUNK_SECONDS`` (1 s).
    max_video_s : float | None
        Optional maximum video duration in seconds. Videos longer than this are
        skipped entirely. Defaults to ``None`` (never skip) so the caller
        decides what to backfill.
    num_clips : int | None
        Optional cap on the number of clips emitted per video. Defaults to
        ``None`` (emit clips for the whole video).

    Examples
    --------
    ::

        from geneva.chunkers import chunk_video_udtf

        # The source must carry a string video_id alongside the raw bytes.
        videos = db.create_table(
            "videos",
            pa.table({
                "video_id": ["clip_001", "clip_002"],
                "video_bytes": [a_bytes, b_bytes],  # raw mp4 bytes
            }),
        )

        view = db.create_udtf_view(
            "video_clips",
            videos.search(None).select(["video_id", "video_bytes"]),
            chunk_video_udtf(chunk_seconds=5.0),
        )
        view.refresh()

        # One row per clip: video_id, chunk_id, start_sec, end_sec, clip_bytes.
        # Correlate clips to their source by video_id (video_bytes is read to
        # cut clips but is not copied into the view).
        df = view.to_pandas()
    """
    cs = float(chunk_seconds)
    limit = None if max_video_s is None else float(max_video_s)
    max_clips = None if num_clips is None else int(num_clips)

    @geneva.chunker(  # type: ignore[reportCallIssue]
        output_schema=_VIDEO_CLIP_SCHEMA,
        input_columns=["video_id", "video_bytes"],
        # The raw bytes are read to cut clips but must not be copied onto every
        # output clip row. ``video_id`` is re-emitted via the output schema.
        inherit_input_columns=False,
        num_cpus=1,
        num_gpus=0,
        memory=1024**3,  # 1 GiB
    )
    def _chunk_video(video_id: str, video_bytes: bytes) -> Iterator[dict[str, Any]]:
        if video_bytes is None:
            return

        try:
            duration = _probe_video(video_bytes)
            if limit is not None and duration > limit:
                _LOG.info(
                    "Skipping video %s longer than %ss (%.2fs)",
                    video_id,
                    limit,
                    duration,
                )
                return

            # ``chunk_id`` counts emitted clips, not windows, so it stays dense
            # and aligned with the framework's ``__child_index`` (derived from
            # yield position) even when a window encodes to no clip.
            chunk_id = 0
            for start, end in _clip_windows(duration, cs, max_clips=max_clips):
                clip = _encode_clip(video_bytes, start, end)
                if clip is None:
                    continue
                yield {
                    "video_id": video_id,
                    "chunk_id": int(chunk_id),
                    "start_sec": float(start),
                    "end_sec": float(end),
                    "clip_bytes": clip,
                }
                chunk_id += 1
        except Exception as exc:
            _LOG.warning("Failed to chunk video %s: %s", video_id, exc)
            return

    return _chunk_video  # type: ignore[return-value]
