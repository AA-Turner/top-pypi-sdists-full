"""Audio generator — MusicGen for music tracks, FFmpeg synth for SFX.

Two roles:
  - Music (longer, atmospheric — looped background): Replicate's
    `facebookresearch/musicgen-small` model. ~30s generations cost
    ~$0.005 each. We fall back to FFmpeg if no Replicate token.
  - SFX (short, sub-1s — bleeps, jumps, hits): FFmpeg's lavfi sine/triangle/
    aevalsrc generators. No external API needed, zero cost, sub-second.

When neither backend works, we write a 1-second silent WAV so the
manifest stays consistent. Engine adapters skip silent assets in their
default sound pools.
"""

from __future__ import annotations

import os
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AudioResult:
    role: str
    path: Path
    backend: str         # "musicgen" | "ffmpeg" | "silent"
    duration_s: float


class AudioGenerator:
    def __init__(self, out_dir: Path) -> None:
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate_music(
        self, role: str, prompt: str, *, seconds: int = 30,
    ) -> AudioResult:
        path = self.out_dir / f"{role}.ogg"
        token = os.environ.get("REPLICATE_API_TOKEN")
        if token:
            try:
                _musicgen(prompt, seconds, path, token)
                return AudioResult(role, path, "musicgen", float(seconds))
            except Exception:  # noqa: BLE001 — fall through
                pass
        # FFmpeg fallback: chord pad with a slow LFO to give it some life.
        # Wrap in try so a missing encoder (e.g. ffmpeg-on-Windows often
        # ships without libvorbis) still degrades to silent rather than
        # propagating into the pipeline and dropping the asset.
        if _ffmpeg_available():
            try:
                _ffmpeg_music(prompt, seconds, path)
                return AudioResult(role, path, "ffmpeg", float(seconds))
            except Exception:  # noqa: BLE001 — fall through to silent
                pass
        _write_silent(path, seconds)
        return AudioResult(role, path, "silent", float(seconds))

    def generate_sfx(self, role: str, prompt: str) -> AudioResult:
        path = self.out_dir / f"{role}.wav"
        if _ffmpeg_available():
            try:
                _ffmpeg_sfx(prompt, path)
                return AudioResult(role, path, "ffmpeg", 0.3)
            except Exception:  # noqa: BLE001 — fall through to silent
                pass
        _write_silent(path, 1, fmt="wav")
        return AudioResult(role, path, "silent", 1.0)


# ─────────────────────────── helpers ───────────────────────────────────


def _ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def _musicgen(prompt: str, seconds: int, out_path: Path, token: str) -> None:
    """Call Replicate's musicgen-small model, save the OGG output."""
    import httpx
    headers = {"Authorization": f"Token {token}",
               "Content-Type": "application/json"}
    # Submit prediction.
    resp = httpx.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json={
            "version": "7be0f12c54a8d033a0fbd14418c9af98962da9a86f5ff7811f9b3423a1f0b7d7",
            "input": {"prompt": prompt, "duration": seconds, "output_format": "ogg"},
        },
        timeout=30,
    )
    resp.raise_for_status()
    pred = resp.json()
    pred_url = pred["urls"]["get"]
    # Poll until done — up to 90s.
    import time
    for _ in range(45):
        time.sleep(2)
        poll = httpx.get(pred_url, headers=headers, timeout=10)
        poll.raise_for_status()
        body = poll.json()
        if body["status"] == "succeeded":
            audio_url = body["output"]
            r = httpx.get(audio_url, timeout=60)
            r.raise_for_status()
            out_path.write_bytes(r.content)
            return
        if body["status"] == "failed":
            raise RuntimeError(f"musicgen failed: {body.get('error')}")
    raise TimeoutError("musicgen prediction did not complete in 90s")


def _ffmpeg_music(prompt: str, seconds: int, out_path: Path) -> None:
    """Chord pad. Tweak frequencies based on prompt mood keywords."""
    lower = prompt.lower()
    if any(w in lower for w in ("dark", "horror", "ominous", "tense", "scary")):
        freqs = (110, 138.59, 164.81)   # A minor triad — moody
    elif any(w in lower for w in ("epic", "adventure", "battle", "fight")):
        freqs = (146.83, 196, 220)      # D minor power-chord
    else:
        freqs = (261.63, 329.63, 392)   # C major triad — neutral
    src = "+".join(f"sine=frequency={f}:duration={seconds}" for f in freqs)
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", src,
         "-filter:a", f"volume=0.2,tremolo=f=0.4:d=0.3",
         "-ac", "2", "-acodec", "libvorbis",
         str(out_path)],
        capture_output=True, text=True, timeout=60, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg music failed: {proc.stderr[-300:]}")


def _ffmpeg_sfx(prompt: str, out_path: Path) -> None:
    """One-shot SFX. Match keywords → generator."""
    lower = prompt.lower()
    if any(w in lower for w in ("jump", "hop", "bounce", "boing")):
        src = "sine=frequency=440:duration=0.15,aformat=sample_fmts=s16:channel_layouts=mono"
        flt = "afade=t=out:st=0.1:d=0.05,asetrate=22050,atempo=2.0"
    elif any(w in lower for w in ("explode", "blast", "boom", "bang", "hit", "crash")):
        src = "anoisesrc=duration=0.3:color=brown"
        flt = "afade=t=out:st=0.15:d=0.15,volume=0.6"
    elif any(w in lower for w in ("pickup", "coin", "collect", "gem")):
        src = "sine=frequency=880:duration=0.05,aformat=sample_fmts=s16"
        flt = ("aevalsrc=val=0:duration=0.0,sine=frequency=880:duration=0.05,"
               "concat=n=2:v=0:a=1") if False else "afade=t=out:st=0.04:d=0.01"
    elif any(w in lower for w in ("laser", "shoot", "fire", "blaster")):
        src = "sine=frequency=1200:duration=0.2"
        flt = "atempo=2.0,afade=t=out:st=0.1:d=0.1"
    else:
        src = "sine=frequency=660:duration=0.2"
        flt = "afade=t=out:st=0.15:d=0.05"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", src,
         "-af", flt, str(out_path)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg sfx failed: {proc.stderr[-300:]}")


def _write_silent(path: Path, seconds: int, *, fmt: str = "ogg") -> None:
    """Minimal silent audio file. We use WAV for ultra-portable silence."""
    sr = 22050
    n_samples = sr * seconds
    if fmt != "wav":
        # An empty .ogg with zero pages still works in most engines; if not,
        # the engine adapter can swap in its own default. Sage's job is to
        # keep the manifest consistent — silent is fine for v1.
        path.write_bytes(b"")
        return
    # 16-bit PCM mono, all zeros.
    data = b"\x00\x00" * n_samples
    chunk = b"WAVE" + b"fmt \x10\x00\x00\x00" + struct.pack(
        "<HHIIHH", 1, 1, sr, sr * 2, 2, 16,
    ) + b"data" + struct.pack("<I", len(data)) + data
    riff = b"RIFF" + struct.pack("<I", len(chunk)) + chunk
    path.write_bytes(riff)
