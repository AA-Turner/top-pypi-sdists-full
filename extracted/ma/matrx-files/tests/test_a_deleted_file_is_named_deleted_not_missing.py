"""A FILE ID WHOSE ROW WAS DELETED RESOLVES AS ``file_deleted``, NOT ``file_not_found`` (system_error 2026-11-12).

Three ``media_pass_read_failed`` rows ("media pass read failed: file_not_found") were each a picture whose file row
was soft-deleted ~2 s before the turn read it. The resolver said ``file_not_found`` for both "deleted" and "no such
id", so the media pass could not tell an expected outcome (the person or a cleanup removed it) from a lookup defect,
and filed every deletion as a server error. RED before ``_missing_file_reason``: both cases answered file_not_found.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files.cloud_sync import _media_resolution as mr
from matrx_files.cloud_sync.media_ref import MediaRef


class _Db:
    def __init__(self, deleted_row: dict[str, Any] | None) -> None:
        self._deleted_row = deleted_row

    async def get_file_async(self, file_id: str, *, include_deleted: bool = False) -> dict[str, Any] | None:
        return self._deleted_row if include_deleted else None

    def get_file(self, file_id: str, *, include_deleted: bool = False) -> dict[str, Any] | None:
        return self._deleted_row if include_deleted else None


def _resolve(db: _Db, sync: bool) -> MediaRef:
    fm = SimpleNamespace(_sync_engine=SimpleNamespace(db=db, _router=None))
    ref = MediaRef(file_id="stored-photo")
    if sync:
        return mr._resolve_media_sync(fm, ref, needs_bytes=True, presigned_ttl_seconds=60)
    return asyncio.run(mr._resolve_media_async_impl(fm, ref, needs_bytes=True, presigned_ttl_seconds=60))


@pytest.mark.parametrize("sync", [False, True])
def test_a_deleted_row_is_named_deleted(sync: bool) -> None:
    out = _resolve(_Db({"id": "stored-photo", "deleted_at": "2026-11-12T13:25:27Z"}), sync)
    assert out.resolver_error == "file_deleted", out.resolver_error


@pytest.mark.parametrize("sync", [False, True])
def test_an_unknown_id_stays_not_found(sync: bool) -> None:
    out = _resolve(_Db(None), sync)
    assert out.resolver_error == "file_not_found", out.resolver_error
