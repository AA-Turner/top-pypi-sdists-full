"""A REPLACED PICTURE'S SIZE FOLLOWS ITS BYTES (CGU-10 AND-V IMG18, live guard for the AND-IMG18 (b) probe rule).

``generate_thumbnail_for_file`` used to write width / height / duration only when the column was empty, so a
picture replaced in place kept the OLD picture's size. AND-IMG18 made the probe win whenever it differs, with no
test: reverting it to "only if empty" left every matrx-files suite green.
"""

from __future__ import annotations

import pytest

from test_bounded_media_processing import (  # the one media-processing harness
    LARGE_MEDIA_THRESHOLD_BYTES,
    FakeFm,
    FakeRouter,
    _record,
    generate_thumbnail_for_file,
    ts,
)

pytestmark = pytest.mark.asyncio


async def test_the_probe_replaces_an_old_pictures_size(monkeypatch) -> None:
    async def probe(path, mime, *, file_name=None):
        return {"width": 1920, "height": 1080, "duration_ms": 1000}

    async def raster(path, mime, *, file_name=None):
        return b"png", "image/png"

    async def kind(path, mime, *, file_name=None):
        return []

    monkeypatch.setattr(ts, "probe_source_metadata_from_path", probe)
    monkeypatch.setattr(ts, "render_thumbnail_source_from_path", raster)
    monkeypatch.setattr(ts, "render_kind_specific_variants_from_path", kind)
    record = {**_record(size_bytes=LARGE_MEDIA_THRESHOLD_BYTES * 2), "width": 640, "height": 480, "duration_ms": 500}
    fm = FakeFm(record, FakeRouter(payload_size=LARGE_MEDIA_THRESHOLD_BYTES * 2))
    await generate_thumbnail_for_file(fm, "replaced-1")
    updates = fm.sync_engine.db.updates
    assert updates and updates[0].get("width") == 1920 and updates[0].get("height") == 1080, updates
