"""Tests for sage.core.asset_generator — image/video file generation.

Sage should be able to produce assets in every common format. Each
test creates a file, then validates it's actually openable (correct
magic bytes, parseable dimensions, expected mime type).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def _file_magic(path: Path) -> str:
    """Return `file -b --mime-type <path>` output, or '' if file missing."""
    if not path.exists():
        return ""
    if not shutil.which("file"):
        return ""
    r = subprocess.run(
        ["file", "-b", "--mime-type", str(path)],
        capture_output=True, text=True, timeout=5,
    )
    return r.stdout.strip()


def _ffprobe_streams(path: Path) -> dict:
    """Get ffprobe metadata as dict, or {} on failure."""
    if not shutil.which("ffprobe"):
        return {}
    import json as _json
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, timeout=10,
    )
    try:
        return _json.loads(r.stdout)
    except Exception:
        return {}


# ── PNG ────────────────────────────────────────────────────────────────


class TestPNG:

    def test_make_png_creates_valid_file(self, tmp_path):
        from sage.core.asset_generator import make_png
        path = tmp_path / "test.png"
        make_png(path, width=200, height=150, fill="#3b82f6")
        assert path.exists()
        assert _file_magic(path) == "image/png"

    def test_png_has_correct_dimensions(self, tmp_path):
        from sage.core.asset_generator import make_png
        from PIL import Image
        path = tmp_path / "x.png"
        make_png(path, width=300, height=200, fill="red")
        with Image.open(path) as img:
            assert img.size == (300, 200)
            assert img.format == "PNG"

    def test_png_with_text_overlay(self, tmp_path):
        from sage.core.asset_generator import make_png
        from PIL import Image
        path = tmp_path / "text.png"
        make_png(path, width=400, height=100, fill="#fff", text="Hello, world!")
        with Image.open(path) as img:
            assert img.size == (400, 100)


# ── JPG / JPEG ────────────────────────────────────────────────────────


class TestJPG:

    def test_make_jpg_creates_valid_file(self, tmp_path):
        from sage.core.asset_generator import make_jpg
        path = tmp_path / "out.jpg"
        make_jpg(path, width=320, height=240, fill="#22c55e")
        assert path.exists()
        assert _file_magic(path) == "image/jpeg"

    def test_jpg_quality_param_changes_size(self, tmp_path):
        from sage.core.asset_generator import make_jpg
        low = tmp_path / "low.jpg"
        high = tmp_path / "high.jpg"
        make_jpg(low, width=600, height=400, fill="gradient", quality=20)
        make_jpg(high, width=600, height=400, fill="gradient", quality=95)
        # Higher quality should produce a larger file
        assert high.stat().st_size > low.stat().st_size


# ── GIF (static + animated) ────────────────────────────────────────────


class TestGIF:

    def test_make_gif_static_creates_valid_file(self, tmp_path):
        from sage.core.asset_generator import make_gif
        path = tmp_path / "static.gif"
        make_gif(path, width=200, height=200, fill="#f97316")
        assert path.exists()
        assert _file_magic(path) == "image/gif"

    def test_make_animated_gif_has_multiple_frames(self, tmp_path):
        from sage.core.asset_generator import make_animated_gif
        from PIL import Image
        path = tmp_path / "anim.gif"
        make_animated_gif(path, width=100, height=100, frames=8, duration_ms=100)
        assert path.exists()
        assert _file_magic(path) == "image/gif"
        with Image.open(path) as img:
            count = 0
            try:
                while True:
                    img.seek(count)
                    count += 1
            except EOFError:
                pass
            assert count >= 8


# ── SVG ────────────────────────────────────────────────────────────────


class TestSVG:

    def test_make_svg_creates_valid_xml(self, tmp_path):
        from sage.core.asset_generator import make_svg
        path = tmp_path / "icon.svg"
        make_svg(path, width=64, height=64, shape="circle", fill="#0ea5e9")
        assert path.exists()
        content = path.read_text()
        # Either starts with XML declaration or directly with <svg
        first_tag = content.lstrip()
        assert first_tag.startswith("<?xml") or first_tag.startswith("<svg")
        assert "<svg" in content
        assert 'xmlns="http://www.w3.org/2000/svg"' in content
        assert "</svg>" in content
        magic = _file_magic(path)
        assert "svg" in magic or "xml" in magic or magic == "image/svg+xml"

    def test_svg_supports_multiple_shapes(self, tmp_path):
        from sage.core.asset_generator import make_svg
        for shape in ("circle", "rect", "star", "path"):
            p = tmp_path / f"{shape}.svg"
            make_svg(p, width=100, height=100, shape=shape)
            assert p.exists(), f"{shape} not generated"


# ── WEBP ───────────────────────────────────────────────────────────────


class TestWEBP:

    def test_make_webp_creates_valid_file(self, tmp_path):
        from sage.core.asset_generator import make_webp
        path = tmp_path / "out.webp"
        make_webp(path, width=300, height=200, fill="#8b5cf6")
        assert path.exists()
        magic = _file_magic(path)
        assert magic == "image/webp"


# ── BMP + TIFF ─────────────────────────────────────────────────────────


class TestBMP:

    def test_make_bmp(self, tmp_path):
        from sage.core.asset_generator import make_bmp
        path = tmp_path / "x.bmp"
        make_bmp(path, width=100, height=100, fill="red")
        assert path.exists()
        magic = _file_magic(path)
        assert "bmp" in magic.lower() or "x-bmp" in magic.lower()


class TestTIFF:

    def test_make_tiff(self, tmp_path):
        from sage.core.asset_generator import make_tiff
        path = tmp_path / "x.tiff"
        make_tiff(path, width=100, height=100, fill="blue")
        assert path.exists()
        magic = _file_magic(path)
        assert "tiff" in magic.lower()


# ── PDF ────────────────────────────────────────────────────────────────


class TestPDF:

    def test_make_pdf(self, tmp_path):
        from sage.core.asset_generator import make_pdf
        path = tmp_path / "doc.pdf"
        make_pdf(path, width=595, height=842, text="Hello PDF")
        assert path.exists()
        magic = _file_magic(path)
        assert "pdf" in magic.lower()
        # First 4 bytes should be %PDF
        assert path.read_bytes()[:4] == b"%PDF"


# ── MP4 + WEBM (video) ─────────────────────────────────────────────────


class TestMP4:

    def test_make_mp4_creates_valid_video(self, tmp_path):
        from sage.core.asset_generator import make_mp4
        path = tmp_path / "test.mp4"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_mp4(path, width=320, height=240, frames=20, fps=10)
            return
        path = tmp_path / "test.mp4"
        make_mp4(path, width=320, height=240, frames=20, fps=10)
        assert path.exists()
        magic = _file_magic(path)
        assert "mp4" in magic.lower() or "video" in magic.lower()

    def test_mp4_has_video_stream(self, tmp_path):
        from sage.core.asset_generator import make_mp4
        path = tmp_path / "video.mp4"
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            if not shutil.which("ffmpeg"):
                with pytest.raises(FileNotFoundError):
                    make_mp4(path, width=400, height=300, frames=30, fps=15)
            return
        make_mp4(path, width=400, height=300, frames=30, fps=15)
        info = _ffprobe_streams(path)
        streams = info.get("streams", [])
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        assert len(video_streams) >= 1
        # Width should match what we requested
        assert video_streams[0].get("width") == 400
        assert video_streams[0].get("height") == 300


class TestWEBM:

    def test_make_webm(self, tmp_path):
        from sage.core.asset_generator import make_webm
        path = tmp_path / "v.webm"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_webm(path, width=320, height=240, frames=10, fps=10)
            return
        make_webm(path, width=320, height=240, frames=10, fps=10)
        assert path.exists()
        magic = _file_magic(path)
        assert "webm" in magic.lower() or "video" in magic.lower()


# ── ICO (favicon) ──────────────────────────────────────────────────────


class TestICO:

    def test_make_ico(self, tmp_path):
        from sage.core.asset_generator import make_ico
        path = tmp_path / "favicon.ico"
        make_ico(path, sizes=(16, 32, 48), fill="#ef4444")
        assert path.exists()
        magic = _file_magic(path)
        assert "icon" in magic.lower() or "ms-windows" in magic.lower() or "ico" in magic.lower()


# ── Audio formats ──────────────────────────────────────────────────────


class TestWAV:

    def test_make_wav_creates_valid_riff(self, tmp_path):
        from sage.core.asset_generator import make_wav
        path = tmp_path / "tone.wav"
        make_wav(path, duration_s=1.0, frequency=440.0)
        assert path.exists()
        # WAV files start with "RIFF" and have "WAVE" at offset 8
        head = path.read_bytes()[:12]
        assert head[:4] == b"RIFF"
        assert head[8:12] == b"WAVE"
        assert "wav" in _file_magic(path).lower() or "audio" in _file_magic(path).lower()

    def test_wav_has_correct_duration(self, tmp_path):
        import wave
        from sage.core.asset_generator import make_wav
        path = tmp_path / "x.wav"
        make_wav(path, duration_s=2.0, sample_rate=22050)
        with wave.open(str(path), "rb") as r:
            frames = r.getnframes()
            assert r.getframerate() == 22050
            # 2 seconds at 22050 Hz = 44100 samples
            assert abs(frames - 44100) < 100

    def test_wav_melody(self, tmp_path):
        from sage.core.asset_generator import make_wav
        path = tmp_path / "melody.wav"
        make_wav(path, duration_s=2.0, melody=("C4", "E4", "G4", "C5"))
        assert path.exists()
        assert path.stat().st_size > 1000


class TestMP3:

    def test_make_mp3(self, tmp_path):
        from sage.core.asset_generator import make_mp3
        path = tmp_path / "tone.mp3"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_mp3(path, duration_s=1.0, frequency=523.25)
            return
        make_mp3(path, duration_s=1.0, frequency=523.25)  # C5
        assert path.exists()
        magic = _file_magic(path)
        assert "mpeg" in magic.lower() or "mp3" in magic.lower() or "audio" in magic.lower()

    def test_mp3_has_audio_stream(self, tmp_path):
        from sage.core.asset_generator import make_mp3
        path = tmp_path / "song.mp3"
        if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
            if not shutil.which("ffmpeg"):
                with pytest.raises(FileNotFoundError):
                    make_mp3(path, duration_s=2.0, melody=("C4", "E4", "G4"))
            return
        make_mp3(path, duration_s=2.0, melody=("C4", "E4", "G4"))
        info = _ffprobe_streams(path)
        streams = info.get("streams", [])
        audio = [s for s in streams if s.get("codec_type") == "audio"]
        assert len(audio) >= 1
        assert "mp3" in audio[0].get("codec_name", "").lower() or audio[0].get("codec_name") == "mp3"


class TestOGG:

    def test_make_ogg(self, tmp_path):
        from sage.core.asset_generator import make_ogg
        path = tmp_path / "x.ogg"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_ogg(path, duration_s=1.0)
            return
        make_ogg(path, duration_s=1.0)
        assert path.exists()
        # OGG magic: starts with "OggS"
        assert path.read_bytes()[:4] == b"OggS"


class TestFLAC:

    def test_make_flac(self, tmp_path):
        from sage.core.asset_generator import make_flac
        path = tmp_path / "x.flac"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_flac(path, duration_s=1.0)
            return
        make_flac(path, duration_s=1.0)
        assert path.exists()
        # FLAC magic: "fLaC"
        assert path.read_bytes()[:4] == b"fLaC"


class TestM4A:

    def test_make_m4a(self, tmp_path):
        from sage.core.asset_generator import make_m4a
        path = tmp_path / "x.m4a"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_m4a(path, duration_s=1.0)
            return
        make_m4a(path, duration_s=1.0)
        assert path.exists()
        magic = _file_magic(path)
        assert any(k in magic.lower() for k in ("mp4", "m4a", "audio", "aac"))


class TestOpus:

    def test_make_opus(self, tmp_path):
        from sage.core.asset_generator import make_opus
        path = tmp_path / "x.opus"
        if not shutil.which("ffmpeg"):
            with pytest.raises(FileNotFoundError):
                make_opus(path, duration_s=1.0)
            return
        make_opus(path, duration_s=1.0)
        assert path.exists()
        # Opus inside OGG container starts with "OggS"
        assert path.read_bytes()[:4] == b"OggS"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
