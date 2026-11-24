"""matrx_files.ffmpeg against the REAL ffmpeg binary: decode, transcode, and loud failure.

These replaced pydub (retired 2026-10-30), so they pin what its consumers relied on: an
exact duration, a non-silent mono sample array, a real transcode, and an error carrying
ffmpeg's own words when the input is not audio — never an empty result.
"""

from __future__ import annotations

import io
import math
import shutil
import struct
import wave

import pytest

from matrx_files import ffmpeg

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg binary not installed")

_RATE = 8000


def _sine_wav(seconds: float = 1.0, hz: float = 440.0, channels: int = 2) -> bytes:
    frames = int(_RATE * seconds)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(_RATE)
        sample = (int(12000 * math.sin(2 * math.pi * hz * i / _RATE)) for i in range(frames))
        w.writeframes(b"".join(struct.pack("<h", s) * channels for s in sample))
    return buf.getvalue()


def test_decode_gives_exact_duration_and_real_mono_samples() -> None:
    pcm = ffmpeg.decode_mono_pcm(_sine_wav(1.0), sample_rate=4000, fmt_hint="wav")
    assert pcm.sample_rate == 4000 and pcm.sample_width == 2
    assert abs(pcm.duration_ms - 1000) <= 5, pcm.duration_ms
    assert max(abs(s) for s in pcm.samples) > 10000  # the sine, not silence


def test_decode_reads_a_path_without_loading_the_source(tmp_path) -> None:
    path = tmp_path / "tone.wav"
    path.write_bytes(_sine_wav(0.5))
    assert abs(ffmpeg.decode_mono_pcm(str(path), sample_rate=4000).duration_ms - 500) <= 5


def test_transcode_round_trips_through_mp3() -> None:
    mp3 = ffmpeg.transcode_audio_bytes(_sine_wav(1.0), source_format="wav", target_format="mp3")
    assert mp3[:3] == b"ID3" or mp3[0] == 0xFF
    # MP3 adds encoder delay + frame padding (1152-sample frames), and a piped encode cannot
    # write the gapless header that would let a decoder trim it: ~150 ms longer is MP3, not a bug.
    assert 1000 <= ffmpeg.decode_mono_pcm(mp3, sample_rate=4000, fmt_hint="mp3").duration_ms <= 1250


def test_garbage_input_raises_with_ffmpegs_own_words() -> None:
    with pytest.raises(RuntimeError, match="ffmpeg failed"):
        ffmpeg.transcode_audio_bytes(b"not audio at all", source_format="wav", target_format="mp3")
    with pytest.raises(RuntimeError):
        ffmpeg.decode_mono_pcm(b"not audio at all", sample_rate=4000, fmt_hint="wav")


def test_a_missing_binary_is_named_never_guessed(monkeypatch) -> None:
    monkeypatch.setattr(ffmpeg.shutil, "which", lambda _name: None)
    monkeypatch.delenv("FFPROBE_BINARY", raising=False)
    with pytest.raises(ffmpeg.FfmpegNotAvailableError, match="ffprobe"):
        ffmpeg.resolve_ffprobe_binary()
