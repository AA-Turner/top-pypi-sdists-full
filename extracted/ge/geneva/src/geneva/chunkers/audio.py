# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Audio chunking UDTF.

Splits audio bytes into fixed-length windows, emitting one output row per
window. Shares the low-level decode/resample/window helpers with the Whisper
transcription pipeline via :mod:`geneva.udfs.audio._chunking`.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import pyarrow as pa

import geneva
from geneva.udfs.audio._chunking import (
    CHUNK_SECONDS,
    MAX_AUDIO_SECONDS,
    TARGET_SAMPLE_RATE,
    _chunk_samples,
    _decode_audio,
    _resample,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

_LOG = logging.getLogger(__name__)

_CHUNK_OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("chunk_id", pa.int32()),
        pa.field("start_sec", pa.float32()),
        pa.field("end_sec", pa.float32()),
        pa.field("samples", pa.list_(pa.float32())),
    ]
)


def chunk_audio_udtf(
    max_audio_s: float = MAX_AUDIO_SECONDS,
    chunk_seconds: int = CHUNK_SECONDS,
) -> geneva.Chunker:
    """Create a scalar UDTF that chunks audio into fixed-length windows.

    Each chunk is yielded as a separate output row and materialised directly
    by ``create_udtf_view`` / ``refresh()``.

    Parameters
    ----------
    max_audio_s : float
        Maximum audio duration in seconds.  Audio longer than this is
        skipped entirely.  Defaults to ``MAX_AUDIO_SECONDS`` (15 min).
    chunk_seconds : int
        Duration of each chunk in seconds.  Defaults to ``CHUNK_SECONDS``
        (30 s).
    """
    limit = float(max_audio_s)
    cs = int(chunk_seconds)

    @geneva.chunker(  # type: ignore[reportCallIssue]
        output_schema=_CHUNK_OUTPUT_SCHEMA,
        num_cpus=1,
        num_gpus=0,
    )
    def _chunk_audio(
        audio_bytes: bytes,
        num_clips: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        if audio_bytes is None:
            return

        try:
            samples, sample_rate = _decode_audio(audio_bytes)
            duration = len(samples) / float(sample_rate) if sample_rate else 0.0
            if duration > limit:
                _LOG.info(
                    "Skipping audio longer than %ss (%.2fs)",
                    limit,
                    duration,
                )
                return

            samples = _resample(samples, sample_rate, TARGET_SAMPLE_RATE)
            max_clips = int(num_clips) if num_clips is not None else None
            chunks = _chunk_samples(
                samples, TARGET_SAMPLE_RATE, max_clips=max_clips, chunk_seconds=cs
            )
            yield from chunks
        except Exception as exc:
            _LOG.warning("Failed to decode audio: %s", exc)
            return

    return _chunk_audio  # type: ignore[return-value]
