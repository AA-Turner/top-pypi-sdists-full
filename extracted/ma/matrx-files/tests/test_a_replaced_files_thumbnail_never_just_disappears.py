"""A REPLACED FILE'S THUMBNAIL NEVER JUST DISAPPEARS (CGU-10 AND-V IMG18, finding F3).

AND-IMG18 (b) made ``VariantsService.list_existing_async`` keep only the variants stamped with the master's CURRENT
version (an unstamped row counts as version 1). That is right for a render, but ``resolve_thumbnail_url_async`` —
the file list's thumbnail, the one reader — only READS that catalog: for a master at version 2+ whose thumbnail
was rendered before the stamp existed it now returns ``None`` and renders nothing. "Re-rendered on next use" holds
for a render call, never for the list. Live 2026-11-12: 436 files (154 pictures, 136 text, 120 documents, 18 audio,
8 video) at version 2+ have a thumbnail that is no longer served.

Fixed: on a miss for a master that HAS an older-version thumbnail, the resolver
queues the render (or the backfill is run once for these rows) — never a silent blank.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any


from matrx_files.cloud_sync.thumbnail_resolver import resolve_thumbnail_url_async
from matrx_files.cloud_sync.variants_service import VariantsService

MASTER = {"id": "m1", "owner_id": "u", "storage_uri": "s3://b/m1.jpg", "current_version": 2, "metadata": {}}
OLD_THUMB = {"id": "v-old", "metadata": {"variant_key": "thumbnail_url", "derived_from": "m1"}}


def test_the_list_thumbnail_of_a_replaced_file_is_served_or_rendered(monkeypatch) -> None:
    renders: list[str] = []

    async def list_variants(_master_id: str) -> list[dict[str, Any]]:
        return [OLD_THUMB]

    async def build_urls(row: dict[str, Any]) -> dict[str, Any]:
        return {"url": f"https://cdn/{row['id']}"}

    engine = SimpleNamespace(db=SimpleNamespace(list_variants_by_master_async=list_variants))
    variants = VariantsService(engine)  # type: ignore[arg-type]

    async def render_async(master: dict[str, Any], **_: Any) -> dict[str, Any]:
        renders.append(master["id"])
        return {}

    monkeypatch.setattr(variants, "render_async", render_async)
    fm = SimpleNamespace(sync_engine=SimpleNamespace(variants=variants, build_urls_for_record_async=build_urls))
    url = asyncio.run(resolve_thumbnail_url_async(fm, MASTER))
    assert url is not None or renders, "the file's thumbnail vanished from the list and nothing renders a new one"
