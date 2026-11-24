"""A PRESET VARIANT (thumbnail, OG, social size) IS OF ITS MASTER'S CURRENT BYTES (CGU-10 AND-V IMG17, finding b).

AND-IMG17 #1 made ``render_variant_async`` (the vision variants) compare ``metadata.master_version`` with the master's
``current_version``. Its sibling ``VariantsService.render_async`` (thumbnails, OG, social and asset presets) still
reuses a variant by ``(master_id, key)`` alone: a picture replaced in place keeps serving the old picture's
thumbnail. Live 2026-11-12: 154 replaced image masters carry a preset variant rendered before their current version.

Enabled with the fix (AND-IMG18): the catalog keeps only the current version's variants; a new one is stamped and named .v{N}.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any


from matrx_files.cloud_sync.variants_service import VariantsService

MASTER = {"id": "m1", "owner_id": "u", "storage_uri": "s3://b/m1.jpg", "file_path": "photos/m1.jpg",
          "current_version": 2, "organization_id": "o", "metadata": {}}
OLD_THUMB = {"id": "v-old", "metadata": {"variant_key": "thumbnail", "derived_from": "m1"}}  # rendered at version 1


def test_a_replaced_master_gets_a_new_thumbnail(monkeypatch) -> None:
    writes: list[str] = []

    async def list_variants(_master_id: str) -> list[dict[str, Any]]:
        return [OLD_THUMB]

    async def read_async(_uri: str) -> bytes:
        return b"new-master-bytes"

    async def managed_write_async(path: str, data: bytes, **_: Any) -> Any:
        writes.append(path)
        return SimpleNamespace(file_id="v-new", size_bytes=len(data), url=None, cdn_url=None, download_url=None)

    engine = SimpleNamespace(
        db=SimpleNamespace(list_variants_by_master_async=list_variants),
        router=SimpleNamespace(read_async=read_async),
        fm=SimpleNamespace(image_handler=SimpleNamespace(
            _render_variants=lambda _b, specs: [(s["key"], s["key"], "JPEG", b"thumb") for s in specs])),
        managed_write_async=managed_write_async,
    )
    svc = VariantsService(engine)  # type: ignore[arg-type]

    async def reused(row: dict[str, Any], spec: dict[str, Any]) -> Any:
        return SimpleNamespace(file_id=row["id"])

    monkeypatch.setattr(svc, "_existing_to_asset_variant", reused)
    out = asyncio.run(svc.render_async(MASTER, variants_specs=[{"key": "thumbnail", "width": 200, "height": 200}]))
    assert out["thumbnail"].file_id != "v-old", "the old picture's thumbnail was served for the replaced picture"
    assert writes, "nothing was rendered for the master's current version"


def test_the_new_variant_is_named_and_stamped_for_its_version() -> None:
    from matrx_files.cloud_sync.variants_service import _current_catalog, _versioned_name

    assert _versioned_name("thumbnail", "jpg", MASTER) == "thumbnail.v2.jpg"
    assert _versioned_name("thumbnail", "jpg", {**MASTER, "current_version": 1}) == "thumbnail.jpg"
    current = {"id": "v-new", "metadata": {"variant_key": "thumbnail", "master_version": 2}}
    assert _current_catalog(MASTER, [OLD_THUMB, current]) == {"thumbnail": current}
    # A master that was never replaced keeps every variant rendered before versions were recorded.
    assert _current_catalog({**MASTER, "current_version": 1}, [OLD_THUMB]) == {"thumbnail": OLD_THUMB}


def test_a_replaced_pictures_size_follows_its_bytes() -> None:
    from matrx_utils.source_guard import stable_source

    from matrx_files.cloud_sync.processing import thumbnails

    source = stable_source(thumbnails._process_source)
    assert 'record.get("width") is None' not in source  # the probe of the current bytes wins
