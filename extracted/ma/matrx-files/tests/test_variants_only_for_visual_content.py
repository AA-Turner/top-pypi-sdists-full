"""Variants are made only for bytes that have a real visual — decided by content.

Live evidence (2026-10-21, Lane E): the desktop-synced text file 6ddac242
(``a.txt``) got three stored image variants — og.jpg, thumb.jpg, tiny.jpg —
each a rendered gray mime icon, i.e. three extra ``files.files`` rows per text
file. The pipeline rendered the SOCIAL_BASELINE for every mime and fell back to
the icon when there was nothing to draw.

SUT: ``thumbnails._process_source`` with the REAL sniff and the REAL icon
renderer; only the variant writer is recorded.
"""

from __future__ import annotations

import io

import pytest
from PIL import Image

from matrx_files.cloud_sync.processing import thumbnails as sut
from matrx_files.specific_handlers import thumbnail_source as ts


class _Variants:
    def __init__(self) -> None:
        self.render_calls: list[bytes] = []
        self.prerendered: list[dict] = []

    async def render_async(self, record, *, variants_specs, master_bytes, force_rerender=False):
        self.render_calls.append(master_bytes)
        return {s["key"]: object() for s in variants_specs if s.get("key")}

    async def persist_prerendered_async(self, record, **kwargs):
        self.prerendered.append(kwargs)


class _Db:
    async def update_file_async(self, file_id, updates):
        return None


class _Fm:
    def __init__(self) -> None:
        self.sync_engine = type("SE", (), {})()
        self.sync_engine.variants = _Variants()
        self.sync_engine.db = _Db()


def _png() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (40, 30), (200, 10, 10)).save(buf, format="PNG")
    return buf.getvalue()


async def _run(content: bytes, mime: str, name: str) -> _Fm:
    fm = _Fm()
    record = {"id": "f1", "owner_id": "u1", "file_name": name, "file_path": f"Docs/{name}", "mime_type": mime, "metadata": {}}
    await sut._process_source(fm, "f1", record, mime, ts, content=content, tmp_path=None, started=0.0)
    return fm


@pytest.mark.asyncio
async def test_a_text_file_gets_no_image_variants():
    fm = await _run(b"lane e dup probe, plain words\n", "text/plain", "a.txt")
    assert fm.sync_engine.variants.render_calls == [], "a .txt got stored image variants"
    assert fm.sync_engine.variants.prerendered == []


@pytest.mark.asyncio
async def test_text_bytes_named_and_claimed_as_png_get_none():
    fm = await _run(b"not pixels at all", "image/png", "fake.png")
    assert fm.sync_engine.variants.render_calls == []


@pytest.mark.asyncio
async def test_a_real_image_still_gets_its_variants():
    png = _png()
    fm = await _run(png, "image/png", "photo.png")
    assert len(fm.sync_engine.variants.render_calls) == 1


@pytest.mark.asyncio
async def test_a_real_image_with_a_wrong_name_still_gets_its_variants():
    fm = await _run(_png(), "application/octet-stream", "upload.bin")
    assert len(fm.sync_engine.variants.render_calls) == 1
