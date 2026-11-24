"""The ONE place the platform finds ffmpeg/ffprobe and decodes audio through them.

Replaces pydub (last release 2021; needs ``audioop``, which Python 3.13 removed): every
consumer only ever used it to locate the ffmpeg binary, to transcode audio bytes, or to
decode audio into samples for a waveform or a duration. All three are a subprocess call,
so they live here with no extra dependency. Every failure raises with ffmpeg's own stderr
tail — a decode that cannot run never returns an empty result.
"""

from __future__ import annotations

import array
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass


class FfmpegNotAvailableError(RuntimeError):
    """No usable ffmpeg/ffprobe binary — raised at call time, never at import."""


def resolve_ffmpeg_binary() -> str:
    """Locate ffmpeg: imageio-ffmpeg's bundled build, then ``$FFMPEG_BINARY``, then PATH."""
    try:
        import imageio_ffmpeg

        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except Exception:  # noqa: BLE001 — optional bundled build; fall through to the next source
        pass

    env_bin = os.environ.get("FFMPEG_BINARY")
    if env_bin and (os.path.exists(env_bin) or shutil.which(env_bin)):
        return env_bin

    which = shutil.which("ffmpeg")
    if which:
        return which

    raise FfmpegNotAvailableError(
        "No ffmpeg binary found. Install the bundled build with the matrx-files[media] extra "
        "(pip install 'matrx-files[media]'), set $FFMPEG_BINARY, or put ffmpeg on PATH."
    )


def resolve_ffprobe_binary() -> str:
    """Locate ffprobe: ``$FFPROBE_BINARY``, then PATH (imageio-ffmpeg ships no ffprobe)."""
    env_bin = os.environ.get("FFPROBE_BINARY")
    if env_bin and (os.path.exists(env_bin) or shutil.which(env_bin)):
        return env_bin
    which = shutil.which("ffprobe")
    if which:
        return which
    raise FfmpegNotAvailableError("No ffprobe binary found. Set $FFPROBE_BINARY or put ffprobe on PATH.")


def _run(cmd: list[str], *, stdin: bytes | None = None) -> bytes:
    proc = subprocess.run(cmd, input=stdin, capture_output=True)
    if proc.returncode != 0:
        tail = proc.stderr.decode(errors="replace")[-500:]
        raise RuntimeError(f"ffmpeg failed (rc={proc.returncode}): {tail}")
    return proc.stdout


def _input_args(source: bytes | str, fmt_hint: str | None) -> tuple[list[str], bytes | None]:
    if isinstance(source, str):
        return ["-i", source], None
    return [*(["-f", fmt_hint] if fmt_hint else []), "-i", "pipe:0"], source


def transcode_audio_bytes(content: bytes, *, source_format: str | None, target_format: str) -> bytes:
    """Any audio ffmpeg reads → ``target_format`` (an ffmpeg muxer name: mp3, wav, ogg, flac…)."""
    inputs, stdin = _input_args(content, source_format)
    out = _run([resolve_ffmpeg_binary(), "-v", "error", *inputs, "-vn", "-f", target_format, "pipe:1"], stdin=stdin)
    if not out:
        raise RuntimeError(f"ffmpeg produced no {target_format} output")
    return out


@dataclass(frozen=True)
class MonoPcm:
    """Signed 16-bit mono samples at ``sample_rate``; ``duration_ms`` is exact for that rate."""

    samples: array.array
    sample_rate: int

    sample_width: int = 2

    @property
    def duration_ms(self) -> int:
        return int(len(self.samples) * 1000 / self.sample_rate)


def decode_mono_pcm(source: bytes | str, *, sample_rate: int, fmt_hint: str | None = None) -> MonoPcm:
    """Decode audio (bytes, or a file path that never enters Python) to mono s16le PCM.

    Decoded size is bounded by duration × ``sample_rate``, not by the source's size.
    """
    inputs, stdin = _input_args(source, fmt_hint)
    raw = _run(
        [resolve_ffmpeg_binary(), "-v", "error", *inputs, "-vn", "-ac", "1", "-ar", str(sample_rate),
         "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1"],
        stdin=stdin,
    )
    samples = array.array("h")
    samples.frombytes(raw[: len(raw) - len(raw) % 2])
    if sys.byteorder == "big":
        samples.byteswap()
    if not samples:
        raise RuntimeError("audio decoded to zero samples")
    return MonoPcm(samples=samples, sample_rate=sample_rate)
