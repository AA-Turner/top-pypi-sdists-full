"""A PICTURE RESOLVED WITHOUT ITS BYTES STILL CARRIES ITS PIXEL SIZE (CGU-10 AND-V IMG17).

The AI Dream request boundary resolves a stored picture with ``needs_bytes=False`` (the media pass is the one byte
reader, AND-IMG17 #1); the prompt estimate then counts the picture by the size the file row carries. Removing
``_carry_dimensions`` from the resolver left every guard green (checker plant S13), so this pins it.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files.cloud_sync import _media_resolution as mr
from matrx_files.cloud_sync.media_ref import MediaRef


class _Db:
    async def get_file_async(self, file_id: str) -> dict[str, Any]:
        return {"id": file_id, "owner_id": "u", "mime_type": "image/jpeg", "size_bytes": 2_000_000,
                "storage_uri": "s3://bucket/p.jpg", "file_name": "p.jpg", "width": 3000, "height": 2250,
                "current_version": 1}


class _Router:
    def get_url(self, uri: str, expires_in: int = 0) -> str:
        return "https://signed.example/p.jpg"

    async def get_url_async(self, uri: str, expires_in: int = 0) -> str:
        return "https://signed.example/p.jpg"


@pytest.mark.parametrize("sync", [False, True])
def test_the_size_rides_a_byte_less_resolution(monkeypatch, sync: bool) -> None:
    monkeypatch.setattr(mr, "_authorized_or_error_async", lambda *a, **k: asyncio.sleep(0, None))
    monkeypatch.setattr(mr, "_authorized_or_error_sync", lambda *a, **k: None)
    db = _Db()

    class _SyncDb:
        def get_file(self, file_id: str) -> dict[str, Any]:
            return asyncio.run(db.get_file_async(file_id))

    engine = SimpleNamespace(db=_SyncDb() if sync else db, _router=_Router())
    fm = SimpleNamespace(_sync_engine=engine)
    ref = MediaRef(file_id="stored-photo")
    if sync:
        out = mr._resolve_media_sync(fm, ref, needs_bytes=False, presigned_ttl_seconds=60)
    else:
        out = asyncio.run(mr._resolve_media_async_impl(fm, ref, needs_bytes=False, presigned_ttl_seconds=60))
    assert out.resolver_error is None, out.resolver_error
    assert (getattr(out, "width", None), getattr(out, "height", None)) == (3000, 2250)
