"""A TRASHED FILE'S THUMBNAIL STAYS ITS READERS' (Matrx Scan Trash Bin, 2026-11-19).

A Trash view's tile had no picture: every door that hands out a file's thumbnail (``GET /files/{id}``'s
``thumbnail_url``, the variant lookup) read live rows only, so a trashed scan — and, after a folder Delete, its
trashed ``v/`` thumbnail variant — answered nothing, and Recover was picked blind.

SUT: the real ``read_thumbnail_async`` and the real ``VariantsService`` catalog. Replaced: the two gated reads
(``read_file_row`` / ``read_stored_bytes`` — the access judge stays the host's ``iam.has_access_for``, emulated
by a readable set) and the DB's variant query, which honors ``include_deleted`` exactly as the real one does.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files import gated_reads
from matrx_files.cloud_sync.thumbnail_resolver import read_thumbnail_async
from matrx_files.cloud_sync.variants_service import VariantsService

TRASHED = "2026-11-19T00:00:00Z"


def _world(*, master_deleted: str | None, variant_deleted: str | None, readers: set[str]):
    master = {
        "id": "m1", "deleted_at": master_deleted, "current_version": 1, "metadata": {},
        "mime_type": "image/png", "derivation_kind": None,
    }
    variant = {
        "id": "v1", "storage_uri": "s3://b/m1/v/thumb.jpg", "mime_type": "image/jpeg", "deleted_at": variant_deleted,
        "metadata": {"variant_key": "thumbnail_url", "derived_from": "m1"},
    }
    master_bytes_read: list[str] = []

    async def list_variants(master_id: str, *, include_deleted: bool = False) -> list[dict[str, Any]]:
        rows = [variant] if master_id == "m1" else []
        return [r for r in rows if include_deleted or r["deleted_at"] is None]

    async def read_file_row(file_id: str, columns, *, live_only: bool = False, user_id=None, **_: Any):
        assert not live_only, "the thumbnail read must reach a trashed master"
        if file_id != "m1" or user_id not in readers:
            return None
        return {k: master[k] for k in ("id", *columns)}

    async def read_stored_bytes(_fm, file_id: str, storage_uri: str, *, user_id=None, **_: Any) -> bytes:
        if user_id not in readers:
            raise PermissionError("not readable")
        if file_id != "v1" or storage_uri != variant["storage_uri"]:
            master_bytes_read.append(file_id)
            raise AssertionError("only the thumbnail variant's own bytes may be served")
        return b"JPEG-THUMB"

    engine = SimpleNamespace(db=SimpleNamespace(list_variants_by_master_async=list_variants))
    fm = SimpleNamespace(sync_engine=SimpleNamespace(variants=VariantsService(engine)))  # type: ignore[arg-type]
    return fm, read_file_row, read_stored_bytes


@pytest.mark.parametrize(
    "variant_deleted",
    [None, TRASHED],
    ids=["file-deleted-alone (variant live)", "folder-deleted (variant trashed with it)"],
)
def test_a_reader_gets_a_trashed_files_thumbnail(monkeypatch, variant_deleted) -> None:
    fm, row, stored = _world(master_deleted=TRASHED, variant_deleted=variant_deleted, readers={"u1"})
    monkeypatch.setattr(gated_reads, "read_file_row", row)
    monkeypatch.setattr(gated_reads, "read_stored_bytes", stored)
    got = asyncio.run(read_thumbnail_async(fm, "m1", user_id="u1"))
    assert got == (b"JPEG-THUMB", "image/jpeg"), "the Trash tile of a file its reader deleted has no picture"


def test_a_non_reader_gets_nothing_and_no_hint(monkeypatch) -> None:
    fm, row, stored = _world(master_deleted=TRASHED, variant_deleted=TRASHED, readers={"u1"})
    monkeypatch.setattr(gated_reads, "read_file_row", row)
    monkeypatch.setattr(gated_reads, "read_stored_bytes", stored)
    with pytest.raises(FileNotFoundError):
        asyncio.run(read_thumbnail_async(fm, "m1", user_id="stranger"))


def test_a_live_file_never_serves_a_trashed_variant(monkeypatch) -> None:
    fm, row, stored = _world(master_deleted=None, variant_deleted=TRASHED, readers={"u1"})
    monkeypatch.setattr(gated_reads, "read_file_row", row)
    monkeypatch.setattr(gated_reads, "read_stored_bytes", stored)
    assert asyncio.run(read_thumbnail_async(fm, "m1", user_id="u1")) is None
