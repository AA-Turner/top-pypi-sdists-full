# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared low-level audio decode / resample / windowing helpers.

Used by both the Whisper transcription pipeline
(:mod:`geneva.udfs.audio.whisper_transcription`) and the audio chunker
(:mod:`geneva.chunkers.audio`). Kept in a dependency-free-of-either module so
the two can share these primitives without a circular import.
"""

from __future__ import annotations

import io
import math
from typing import Any

TARGET_SAMPLE_RATE = 16000
CHUNK_SECONDS = 30
MAX_AUDIO_SECONDS = 15 * 60


def _decode_audio(audio_bytes: bytes) -> tuple[Any, int]:
    import numpy as np
    import soundfile as sf

    with sf.SoundFile(io.BytesIO(audio_bytes)) as f:
        samples = f.read(dtype="float32")
        sample_rate = f.samplerate

    if samples.ndim == 2:
        samples = np.mean(samples, axis=1)

    return samples, int(sample_rate)


def _resample(samples, sample_rate: int, target_rate: int):  # noqa: ANN202
    if sample_rate == target_rate:
        return samples

    import numpy as np
    from scipy.signal import resample_poly

    gcd = math.gcd(sample_rate, target_rate)
    up = target_rate // gcd
    down = sample_rate // gcd
    resampled = resample_poly(samples, up, down)
    return np.asarray(resampled, dtype=np.float32)


def _chunk_samples(
    samples,
    sample_rate: int,
    max_clips: int | None = None,
    chunk_seconds: int = CHUNK_SECONDS,
) -> list[dict[str, Any]]:
    chunk_size = chunk_seconds * sample_rate
    total_samples = len(samples)
    chunks: list[dict[str, Any]] = []

    if total_samples == 0:
        return chunks

    if max_clips is not None and max_clips <= 0:
        return chunks

    chunk_id = 0
    for start in range(0, total_samples, chunk_size):
        if max_clips is not None and chunk_id >= max_clips:
            break
        end = min(start + chunk_size, total_samples)
        chunk = samples[start:end]
        if len(chunk) == 0:
            continue
        chunks.append(
            {
                "chunk_id": int(chunk_id),
                "start_sec": float(start / sample_rate),
                "end_sec": float(end / sample_rate),
                "samples": chunk.tolist(),
            }
        )
        chunk_id += 1

    return chunks
