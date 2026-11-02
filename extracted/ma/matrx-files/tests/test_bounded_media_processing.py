"""Bounded-memory large-media processing (media capture Phase 6b).

Pins the size-aware source strategy in
``cloud_sync/processing/thumbnails.py``:

  - below LARGE_MEDIA_THRESHOLD_BYTES → in-memory fast path
    (``router.read_async``), unchanged behavior;
  - at/above it → streamed to a NamedTemporaryFile
    (``router.download_to_path_async``) and probed/rendered BY PATH —
    ``read_async`` must NEVER be called;
  - per-file in-flight guard: concurrent invocations for the same
    file_id run the pipeline exactly once;
  - temp file always deleted, including on failure;
  - path-based probe/waveform/frame correctness on small real samples
    (wav via stdlib; mp4 via ffmpeg when available).
"""

from __future__ import annotations

import asyncio
import math
import os
import shutil
import struct
import subprocess
import wave
from typing import Any

import pytest

from matrx_files.cloud_sync.processing import thumbnails as thumbs_mod
from matrx_files.cloud_sync.processing.thumbnails import (
    LARGE_MEDIA_THRESHOLD_BYTES,
    generate_thumbnail_for_file,
)
from matrx_files.specific_handlers import thumbnail_source as ts


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class FakeRouter:
    """Records which read strategy was used. ``download`` streams a
    server-side payload to the local path in chunks — the whole object is
    never held as one Python bytes object on the download path."""

    def __init__(self, *, payload: bytes = b"", payload_size: int | None = None):
        self._payload = payload
        self._payload_size = payload_size if payload_size is not None else len(payload)
        self.read_calls: list[str] = []
        self.download_calls: list[tuple[str, str]] = []

    async def read_async(self, uri: str) -> bytes:
        self.read_calls.append(uri)
        return self._payload

    async def download_to_path_async(self, uri: str, local_path: str) -> int:
        self.download_calls.append((uri, local_path))
        chunk = self._payload or b"\x00" * 8192
        remaining = self._payload_size
        with open(local_path, "wb") as f:  # noqa: ASYNC230 — test fake, tiny writes
            if self._payload:
                f.write(self._payload)
            else:
                while remaining > 0:
                    n = min(remaining, len(chunk))
                    f.write(chunk[:n])
                    remaining -= n
        return self._payload_size


class FakeVariants:
    def __init__(self):
        self.rendered_masters: list[bytes] = []
        self.persisted: list[str] = []

    async def render_async(
        self,
        record,
        *,
        variants_specs,
        master_bytes,
        force_rerender: bool = False,
    ):
        self.rendered_masters.append(master_bytes)
        return {"thumbnail_url": "https://cdn.example/x.png"}

    async def persist_prerendered_async(
        self,
        record,
        *,
        variant_key,
        content,
        mime_type,
        variant_family,
        force_rerender: bool = False,
    ):
        self.persisted.append(variant_key)


class FakeDb:
    def __init__(self, record: dict[str, Any]):
        self._record = record
        self.updates: list[dict[str, Any]] = []

    async def get_file_async(self, file_id: str) -> dict[str, Any]:
        return dict(self._record)

    async def update_file_async(self, file_id: str, updates: dict[str, Any]) -> None:
        self.updates.append(updates)


class FakeFm:
    def __init__(self, record: dict[str, Any], router: FakeRouter):
        variants = FakeVariants()
        db = FakeDb(record)
        self.sync_engine = type("Engine", (), {"db": db, "router": router, "variants": variants})()


def _record(size_bytes: int, mime: str = "video/mp4", file_id: str = "f1") -> dict[str, Any]:
    return {
        "id": file_id,
        "mime_type": mime,
        "size_bytes": size_bytes,
        "file_name": "capture.mp4",
        "storage_uri": "s3://bucket/u/capture.mp4",
        "metadata": {},
        "parent_file_id": None,
        "file_path": "user-files/capture.mp4",
    }


# ---------------------------------------------------------------------------
# Sample media generators
# ---------------------------------------------------------------------------


def _make_wav(path: str, seconds: float = 1.0, rate: int = 8000) -> None:
    n = int(seconds * rate)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = b"".join(
            struct.pack("<h", int(12000 * math.sin(2 * math.pi * 440 * i / rate))) for i in range(n)
        )
        w.writeframes(frames)


def _ffmpeg() -> str | None:
    return shutil.which("ffmpeg")


def _make_mp4(path: str, seconds: float = 1.0) -> None:
    subprocess.run(
        [
            _ffmpeg(),
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"testsrc=duration={seconds}:size=320x240:rate=10",
            "-pix_fmt",
            "yuv420p",
            path,
        ],
        check=True,
        capture_output=True,
    )


# ---------------------------------------------------------------------------
# Threshold routing
# ---------------------------------------------------------------------------


def _tiny_png() -> bytes:
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (8, 8), (10, 120, 200)).save(buf, format="PNG")
    return buf.getvalue()


async def test_small_file_uses_in_memory_path(monkeypatch):
    # A real image: a text file makes no variants at all (only bytes with a
    # real visual do -- test_variants_only_for_visual_content.py).
    png = _tiny_png()
    router = FakeRouter(payload=png)
    fm = FakeFm(_record(size_bytes=len(png), mime="image/png"), router)

    ok = await generate_thumbnail_for_file(fm, "small-1")
    assert ok
    assert router.read_calls, "small file must use read_async"
    assert not router.download_calls


async def test_large_file_streams_and_never_calls_read_async(monkeypatch):
    """At/above the threshold the whole-object read must NOT happen."""
    seen_paths: list[str] = []

    async def fake_probe(path, mime, *, file_name=None):
        seen_paths.append(path)
        assert os.path.exists(path)
        return {"width": 1920, "height": 1080, "duration_ms": 1000}

    async def fake_raster(path, mime, *, file_name=None):
        assert os.path.exists(path)
        return b"png", "image/png"

    async def fake_kind(path, mime, *, file_name=None):
        return [("poster_url", b"jpg", "image/jpeg", "video")]

    monkeypatch.setattr(ts, "probe_source_metadata_from_path", fake_probe)
    monkeypatch.setattr(ts, "render_thumbnail_source_from_path", fake_raster)
    monkeypatch.setattr(ts, "render_kind_specific_variants_from_path", fake_kind)

    # Simulate a "large" object served only via streaming: 2x threshold,
    # written to disk in chunks — never materialized as one bytes object.
    router = FakeRouter(payload_size=LARGE_MEDIA_THRESHOLD_BYTES * 2)

    async def read_forbidden(uri):
        raise AssertionError("read_async must not be called above the threshold")

    router.read_async = read_forbidden  # type: ignore[method-assign]

    fm = FakeFm(_record(size_bytes=LARGE_MEDIA_THRESHOLD_BYTES * 2), router)
    ok = await generate_thumbnail_for_file(fm, "large-1")

    assert ok
    assert router.download_calls, "large file must use the streaming download"
    assert fm.sync_engine.variants.persisted == ["poster_url"]
    assert fm.sync_engine.db.updates and fm.sync_engine.db.updates[0]["width"] == 1920
    # Temp file cleaned up in the finally block.
    assert seen_paths and not os.path.exists(seen_paths[0])


async def test_exact_threshold_uses_streaming():
    router = FakeRouter(payload_size=LARGE_MEDIA_THRESHOLD_BYTES)
    fm = FakeFm(
        _record(size_bytes=LARGE_MEDIA_THRESHOLD_BYTES, mime="application/octet-stream"), router
    )
    await generate_thumbnail_for_file(fm, "edge-1")
    # Bytes with no visual make no variants (no gray-icon placeholder is ever
    # stored); what this test pins is the ROUTING at the threshold.
    assert router.download_calls and not router.read_calls


async def test_temp_file_cleaned_up_on_failure(monkeypatch):
    """Even when path-processing blows up, the temp file must be deleted."""
    seen: list[str] = []

    async def exploding_probe(path, mime, *, file_name=None):
        seen.append(path)
        raise RuntimeError("boom")

    async def exploding_raster(path, mime, *, file_name=None):
        raise RuntimeError("boom")

    monkeypatch.setattr(ts, "probe_source_metadata_from_path", exploding_probe)
    monkeypatch.setattr(ts, "render_thumbnail_source_from_path", exploding_raster)

    router = FakeRouter(payload_size=LARGE_MEDIA_THRESHOLD_BYTES + 1)
    fm = FakeFm(_record(size_bytes=LARGE_MEDIA_THRESHOLD_BYTES + 1), router)

    ok = await generate_thumbnail_for_file(fm, "fail-1")
    assert ok is False  # never raises
    assert seen and not os.path.exists(seen[0])


# ---------------------------------------------------------------------------
# Concurrency guard
# ---------------------------------------------------------------------------


async def test_concurrent_calls_run_pipeline_once(monkeypatch):
    executions = 0
    real_impl = thumbs_mod._generate_impl

    async def counting_impl(fm, file_id, **kw):
        nonlocal executions
        executions += 1
        await asyncio.sleep(0.05)  # hold the in-flight slot open
        return await real_impl(fm, file_id, **kw)

    monkeypatch.setattr(thumbs_mod, "_generate_impl", counting_impl)

    router = FakeRouter(payload=b"tiny")
    fm = FakeFm(_record(size_bytes=4, mime="text/plain", file_id="c1"), router)

    results = await asyncio.gather(
        generate_thumbnail_for_file(fm, "c1"),
        generate_thumbnail_for_file(fm, "c1"),
        generate_thumbnail_for_file(fm, "c1"),
    )
    assert executions == 1, "concurrent triggers must join the canonical run"
    assert all(r == results[0] for r in results)
    assert thumbs_mod._INFLIGHT.get("c1") is None or thumbs_mod._INFLIGHT["c1"].done()


async def test_different_files_run_independently(monkeypatch):
    executions: list[str] = []
    real_impl = thumbs_mod._generate_impl

    async def counting_impl(fm, file_id, **kw):
        executions.append(file_id)
        return await real_impl(fm, file_id, **kw)

    monkeypatch.setattr(thumbs_mod, "_generate_impl", counting_impl)

    router = FakeRouter(payload=b"tiny")
    fm_a = FakeFm(_record(size_bytes=4, mime="text/plain", file_id="a"), router)
    fm_b = FakeFm(_record(size_bytes=4, mime="text/plain", file_id="b"), router)
    await asyncio.gather(
        generate_thumbnail_for_file(fm_a, "a"),
        generate_thumbnail_for_file(fm_b, "b"),
    )
    assert sorted(executions) == ["a", "b"]


# ---------------------------------------------------------------------------
# Path-based probe / render correctness on real samples
# ---------------------------------------------------------------------------


def test_audio_probe_and_waveform_from_path(tmp_path):
    pytest.importorskip("pydub")
    if _ffmpeg() is None:
        pytest.skip("ffmpeg not available")
    wav = str(tmp_path / "tone.wav")
    _make_wav(wav, seconds=1.0)

    probed = ts.probe_source_metadata_from_path_sync(wav, "audio/wav")
    assert 900 <= probed.get("duration_ms", 0) <= 1100

    png, mime = ts.render_thumbnail_source_from_path_sync(wav, "audio/wav")
    assert mime == "image/png" and png[:8] == b"\x89PNG\r\n\x1a\n"


def test_video_probe_frame_and_poster_from_path(tmp_path):
    pytest.importorskip("cv2")
    if _ffmpeg() is None:
        pytest.skip("ffmpeg not available")
    mp4 = str(tmp_path / "clip.mp4")
    _make_mp4(mp4, seconds=1.0)

    probed = ts.probe_source_metadata_from_path_sync(mp4, "video/mp4")
    assert probed.get("width") == 320 and probed.get("height") == 240
    assert 800 <= probed.get("duration_ms", 0) <= 1300

    jpg, mime = ts.render_thumbnail_source_from_path_sync(mp4, "video/mp4")
    assert mime == "image/jpeg" and jpg[:2] == b"\xff\xd8"

    variants = ts.render_kind_specific_variants_from_path_sync(mp4, "video/mp4")
    assert [v[0] for v in variants] == ["poster_url"]


def test_large_image_and_pdf_skip_generic_rasterization(tmp_path):
    """Images/PDFs on the bounded path get the mime icon, never a decode."""
    fake = str(tmp_path / "big.jpg")
    with open(fake, "wb") as f:
        f.write(b"\x00" * 128)
    png, mime = ts.render_thumbnail_source_from_path_sync(fake, "image/jpeg")
    assert mime == "image/png"  # icon, not a passthrough of the source

    assert ts.render_kind_specific_variants_from_path_sync(fake, "application/pdf") == []
    assert ts.probe_source_metadata_from_path_sync(fake, "application/pdf") == {}


def test_heic_browser_preview_variant_is_emitted_from_bytes(monkeypatch):
    monkeypatch.setattr(ts, "_render_browser_preview_from_bytes", lambda content: b"browser-jpeg")

    assert ts.render_kind_specific_variants_sync(
        b"heic-source", "image/heic", file_name="Product.HEIC"
    ) == [("preview_url", b"browser-jpeg", "image/jpeg", "image")]


def test_heic_browser_preview_variant_is_emitted_from_path(monkeypatch, tmp_path):
    source = tmp_path / "Product.HEIC"
    source.write_bytes(b"heic-source")
    monkeypatch.setattr(ts, "_render_browser_preview_from_path", lambda path: b"browser-jpeg")

    assert ts.render_kind_specific_variants_from_path_sync(
        str(source), "image/heif", file_name=source.name
    ) == [("preview_url", b"browser-jpeg", "image/jpeg", "image")]


# ---------------------------------------------------------------------------
# Synthetic-large end-to-end: streaming path exercised with a real video
# ---------------------------------------------------------------------------


async def test_synthetic_large_video_uses_streaming_end_to_end(tmp_path, monkeypatch):
    """A real (small) mp4 declared above a lowered threshold must flow
    through download→temp-file→path-probe→path-poster with NO whole-object
    read. This is the harness for the real ≥2 GB measurement — only the
    threshold monkeypatch and the sample size differ."""
    pytest.importorskip("cv2")
    if _ffmpeg() is None:
        pytest.skip("ffmpeg not available")

    mp4 = str(tmp_path / "clip.mp4")
    _make_mp4(mp4, seconds=1.0)
    payload = (tmp_path / "clip.mp4").read_bytes()

    monkeypatch.setattr(thumbs_mod, "LARGE_MEDIA_THRESHOLD_BYTES", 1024)

    router = FakeRouter(payload=payload)

    async def read_forbidden(uri):
        raise AssertionError("streaming path must not whole-read")

    router.read_async = read_forbidden  # type: ignore[method-assign]

    fm = FakeFm(_record(size_bytes=len(payload), file_id="e2e"), router)
    ok = await generate_thumbnail_for_file(fm, "e2e")

    assert ok
    assert router.download_calls
    assert fm.sync_engine.variants.persisted == ["poster_url"]
    upd = fm.sync_engine.db.updates[0]
    assert upd["width"] == 320 and upd["height"] == 240 and upd["duration_ms"] > 0
    # temp file gone
    tmp_used = router.download_calls[0][1]
    assert not os.path.exists(tmp_used)
