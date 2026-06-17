"""Asset generation for sage — images, vector graphics, video files.

Sage can produce assets in every common file format using only Pillow
and ffmpeg (the latter only for video). These are *procedural* assets
(shapes, gradients, animations), not AI-generated photographs — for
that you'd need a model like Stable Diffusion. But for the 90% of
real-world "make me a placeholder image / icon / chart / short clip"
needs, this module is enough.

All `make_*` functions write to a single path and return that path.
They never raise on valid input; they raise on bad path or unsupported
parameters.
"""

from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

__all__ = [
    "make_png",
    "make_jpg",
    "make_gif",
    "make_animated_gif",
    "make_svg",
    "make_webp",
    "make_bmp",
    "make_tiff",
    "make_pdf",
    "make_ico",
    "make_mp4",
    "make_webm",
    # Audio
    "make_wav",
    "make_mp3",
    "make_ogg",
    "make_flac",
    "make_m4a",
    "make_opus",
]


# ── Internal helpers ───────────────────────────────────────────────────


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _resolve_fill(fill: str | tuple, width: int, height: int):
    """Convert a fill spec to a PIL-ready value.

    Strings: hex (#abc, #aabbcc), color name (red), or 'gradient'.
    Tuples: passed through as RGB/RGBA.
    """
    from PIL import Image, ImageDraw

    if fill == "gradient":
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        for y in range(height):
            t = y / max(height - 1, 1)
            r = int(99 + (240 - 99) * t)
            g = int(102 + (180 - 102) * t)
            b = int(241 + (140 - 241) * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return img
    return Image.new("RGB", (width, height), fill)


def _new_image_with_text(
    width: int,
    height: int,
    fill: str | tuple,
    text: str | None,
):
    """Construct a base PIL image with optional centered text."""
    from PIL import Image, ImageDraw, ImageFont

    img = _resolve_fill(fill, width, height)
    if isinstance(img, Image.Image):
        base = img.convert("RGB") if img.mode != "RGB" else img
    else:
        base = Image.new("RGB", (width, height), fill)
    if text:
        draw = ImageDraw.Draw(base)
        # Try a nicer font; fall back to default
        font = ImageFont.load_default()
        try:
            # macOS / many distros ship this
            from PIL import ImageFont as _IF
            font = _IF.truetype(
                "/System/Library/Fonts/Helvetica.ttc",
                size=max(12, height // 6),
            )
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", size=max(12, height // 6))
            except OSError:
                pass
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((width - tw) / 2, (height - th) / 2),
            text,
            fill="#111111",
            font=font,
        )
    return base


# ── PNG / JPG / WEBP / BMP / TIFF / GIF ───────────────────────────────


def make_png(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
    text: str | None = None,
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, text)
    img.save(p, format="PNG")
    return p


def make_jpg(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
    text: str | None = None,
    quality: int = 85,
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, text)
    img.save(p, format="JPEG", quality=int(quality))
    return p


def make_webp(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
    text: str | None = None,
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, text)
    img.save(p, format="WEBP")
    return p


def make_bmp(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, None)
    img.save(p, format="BMP")
    return p


def make_tiff(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, None)
    img.save(p, format="TIFF")
    return p


def make_gif(
    path: str | Path,
    *,
    width: int = 256,
    height: int = 256,
    fill: str | tuple = "#ffffff",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, None)
    img.save(p, format="GIF")
    return p


def make_animated_gif(
    path: str | Path,
    *,
    width: int = 200,
    height: int = 200,
    frames: int = 12,
    duration_ms: int = 80,
    loop: int = 0,
) -> Path:
    """Animated GIF of a rotating colored circle. Loops by default."""
    from PIL import Image, ImageDraw

    p = Path(path)
    _ensure_parent(p)
    images = []
    for i in range(frames):
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        angle = 2 * math.pi * (i / max(frames, 1))
        cx = width // 2 + int(width * 0.25 * math.cos(angle))
        cy = height // 2 + int(height * 0.25 * math.sin(angle))
        r = min(width, height) // 8
        hue = int(360 * (i / max(frames, 1)))
        # Convert HSV → RGB via PIL's color converter
        from colorsys import hsv_to_rgb
        rr, gg, bb = hsv_to_rgb(hue / 360.0, 0.7, 0.95)
        color = (int(rr * 255), int(gg * 255), int(bb * 255))
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=color)
        images.append(img)
    images[0].save(
        p,
        format="GIF",
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=loop,
        optimize=False,
    )
    return p


# ── SVG ────────────────────────────────────────────────────────────────


_SVG_SHAPES: dict[str, callable] = {
    "circle": lambda w, h, fill: (
        f'<circle cx="{w/2}" cy="{h/2}" r="{min(w, h)/2 - 2}" fill="{fill}"/>'
    ),
    "rect": lambda w, h, fill: (
        f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="{min(w, h)/8}" fill="{fill}"/>'
    ),
    "star": lambda w, h, fill: _svg_star(w, h, fill),
    "path": lambda w, h, fill: (
        f'<path d="M{w*0.1},{h*0.5} Q{w*0.5},{h*0.1} {w*0.9},{h*0.5} '
        f'T{w*0.9},{h*0.9}" stroke="{fill}" stroke-width="3" fill="none"/>'
    ),
}


def _svg_star(w: float, h: float, fill: str) -> str:
    cx, cy = w / 2, h / 2
    r1, r2 = min(w, h) / 2 - 2, min(w, h) / 5
    pts: list[str] = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        r = r1 if i % 2 == 0 else r2
        pts.append(f"{cx + r * math.cos(ang):.2f},{cy + r * math.sin(ang):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def make_svg(
    path: str | Path,
    *,
    width: int = 64,
    height: int = 64,
    shape: str = "circle",
    fill: str = "#0ea5e9",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    shape_fn = _SVG_SHAPES.get(shape, _SVG_SHAPES["circle"])
    body = shape_fn(width, height, fill)
    svg = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">\n'
        f"  {body}\n"
        f'</svg>\n'
    )
    p.write_text(svg, encoding="utf-8")
    return p


# ── PDF (single-page via Pillow) ─────────────────────────────────────


def make_pdf(
    path: str | Path,
    *,
    width: int = 595,
    height: int = 842,
    text: str = "PDF document",
    fill: str | tuple = "#ffffff",
) -> Path:
    """Single-page PDF using Pillow's PDF backend.

    Width/height are in pixels at 72 DPI (595x842 ≈ A4).
    """
    p = Path(path)
    _ensure_parent(p)
    img = _new_image_with_text(width, height, fill, text)
    # Pillow can save a PDF directly
    img.save(p, "PDF", resolution=72.0)
    return p


# ── ICO (Windows favicon) ────────────────────────────────────────────


def make_ico(
    path: str | Path,
    *,
    sizes: tuple[int, ...] = (16, 32, 48),
    fill: str | tuple = "#ef4444",
) -> Path:
    from PIL import Image

    p = Path(path)
    _ensure_parent(p)
    max_size = max(sizes)
    img = _new_image_with_text(max_size, max_size, fill, None)
    img.save(p, format="ICO", sizes=[(s, s) for s in sizes])
    return p


# ── Video: MP4 / WEBM via ffmpeg ─────────────────────────────────────


def _render_video(
    path: Path,
    width: int,
    height: int,
    frames: int,
    fps: int,
    codec: str,
    pix_fmt: str,
    extra_args: list[str],
) -> Path:
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not installed. Install it for video generation:\n"
            "  macOS:  brew install ffmpeg\n"
            "  Ubuntu: sudo apt install ffmpeg\n"
        )
    from PIL import Image, ImageDraw

    with tempfile.TemporaryDirectory(prefix="sage-frames-") as td:
        td_path = Path(td)
        # Generate frames as PNGs
        for i in range(frames):
            img = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(img)
            t = i / max(frames - 1, 1)
            cx = int(width * (0.2 + 0.6 * t))
            cy = height // 2
            r = min(width, height) // 6
            from colorsys import hsv_to_rgb
            rr, gg, bb = hsv_to_rgb(t, 0.7, 0.95)
            color = (int(rr * 255), int(gg * 255), int(bb * 255))
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=color)
            img.save(td_path / f"frame_{i:04d}.png")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(fps),
            "-i", str(td_path / "frame_%04d.png"),
            "-c:v", codec,
            "-pix_fmt", pix_fmt,
            *extra_args,
            str(path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {r.stderr[:300]}")
    return path


def make_mp4(
    path: str | Path,
    *,
    width: int = 320,
    height: int = 240,
    frames: int = 20,
    fps: int = 10,
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _render_video(
        p, width, height, frames, fps,
        codec="libx264", pix_fmt="yuv420p",
        extra_args=["-movflags", "+faststart"],
    )


def make_webm(
    path: str | Path,
    *,
    width: int = 320,
    height: int = 240,
    frames: int = 20,
    fps: int = 10,
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _render_video(
        p, width, height, frames, fps,
        codec="libvpx-vp9", pix_fmt="yuv420p",
        extra_args=["-b:v", "0", "-crf", "30"],
    )


# ── Audio: WAV / MP3 / OGG / FLAC / M4A / OPUS ────────────────────────


_NOTE_HZ = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25,
}


def _synthesize_pcm(
    *,
    duration_s: float,
    sample_rate: int,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
) -> bytes:
    """Generate 16-bit PCM samples (mono) as raw bytes.

    `melody` is an optional tuple of note names; if provided, the
    duration is split evenly across notes and each is played in turn.
    Otherwise a single tone at `frequency` is rendered.
    """
    import array
    import math as _math

    total_samples = int(duration_s * sample_rate)
    samples = array.array("h", [0] * total_samples)

    if melody:
        seg = total_samples // len(melody)
        for i, note in enumerate(melody):
            freq = _NOTE_HZ.get(note.upper(), 440.0)
            start = i * seg
            end = (i + 1) * seg if i < len(melody) - 1 else total_samples
            for n in range(start, end):
                t = n / sample_rate
                amp = 0.3
                # 20ms attack/release envelope to avoid clicks
                env_len = int(sample_rate * 0.02)
                local = n - start
                if local < env_len:
                    amp *= local / env_len
                elif (end - n) < env_len:
                    amp *= (end - n) / env_len
                value = amp * _math.sin(2 * _math.pi * freq * t)
                samples[n] = int(value * 32767)
    else:
        for n in range(total_samples):
            t = n / sample_rate
            if waveform == "square":
                value = 0.3 if _math.sin(2 * _math.pi * frequency * t) >= 0 else -0.3
            elif waveform == "sawtooth":
                value = 0.3 * (2 * (t * frequency - _math.floor(0.5 + t * frequency)))
            elif waveform == "triangle":
                value = 0.3 * (2 * abs(2 * (t * frequency - _math.floor(0.5 + t * frequency))) - 1)
            else:  # sine
                value = 0.3 * _math.sin(2 * _math.pi * frequency * t)
            samples[n] = int(value * 32767)
    return samples.tobytes()


def make_wav(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 44100,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
) -> Path:
    """Write a 16-bit mono PCM WAV file. Uses Python's stdlib `wave`."""
    import wave
    p = Path(path)
    _ensure_parent(p)
    pcm = _synthesize_pcm(
        duration_s=duration_s, sample_rate=sample_rate,
        melody=melody, frequency=frequency, waveform=waveform,
    )
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)  # 16-bit
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return p


def _encode_audio_via_ffmpeg(
    output: Path,
    *,
    duration_s: float,
    sample_rate: int,
    melody: tuple[str, ...] | None,
    frequency: float,
    waveform: str,
    codec: str,
    extra_args: list[str],
) -> Path:
    """Render WAV via Python, then transcode to target format with ffmpeg."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not installed. Required for non-WAV audio. "
            "macOS: `brew install ffmpeg`; Ubuntu: `sudo apt install ffmpeg`."
        )
    with tempfile.TemporaryDirectory(prefix="sage-audio-") as td:
        wav_path = Path(td) / "src.wav"
        make_wav(
            wav_path,
            duration_s=duration_s, sample_rate=sample_rate,
            melody=melody, frequency=frequency, waveform=waveform,
        )
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_path),
            "-c:a", codec,
            *extra_args,
            str(output),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {(r.stderr or '')[:300]}")
    return output


def make_mp3(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 44100,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
    bitrate: str = "192k",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _encode_audio_via_ffmpeg(
        p, duration_s=duration_s, sample_rate=sample_rate, melody=melody,
        frequency=frequency, waveform=waveform,
        codec="libmp3lame", extra_args=["-b:a", bitrate],
    )


def make_ogg(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 44100,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _encode_audio_via_ffmpeg(
        p, duration_s=duration_s, sample_rate=sample_rate, melody=melody,
        frequency=frequency, waveform=waveform,
        codec="libvorbis", extra_args=["-q:a", "5"],
    )


def make_flac(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 44100,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _encode_audio_via_ffmpeg(
        p, duration_s=duration_s, sample_rate=sample_rate, melody=melody,
        frequency=frequency, waveform=waveform,
        codec="flac", extra_args=[],
    )


def make_m4a(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 44100,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
    bitrate: str = "192k",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _encode_audio_via_ffmpeg(
        p, duration_s=duration_s, sample_rate=sample_rate, melody=melody,
        frequency=frequency, waveform=waveform,
        codec="aac", extra_args=["-b:a", bitrate],
    )


def make_opus(
    path: str | Path,
    *,
    duration_s: float = 2.0,
    sample_rate: int = 48000,
    melody: tuple[str, ...] | None = None,
    frequency: float = 440.0,
    waveform: str = "sine",
) -> Path:
    p = Path(path)
    _ensure_parent(p)
    return _encode_audio_via_ffmpeg(
        p, duration_s=duration_s, sample_rate=sample_rate, melody=melody,
        frequency=frequency, waveform=waveform,
        codec="libopus", extra_args=["-b:a", "96k"],
    )
