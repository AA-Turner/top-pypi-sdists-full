"""A presigned upload minted by one worker must finalize on another.

SUT: ``PresignedManager`` (create / finalize / pending store). Real: both manager instances, the
SyncEngine and DatabaseClient. Replaced: the SQL tables (``_files_db_double``) and S3.

Live break this guards (2026-10-27): the pending upload lived in a per-process dict while the
server runs 4 tasks, so ``/files/finalize-upload`` answered 404 ``upload_not_found`` whenever it
landed on a task that had not minted the upload. Also guarded: exactly one concurrent finalize
wins, an expired upload is refused, another user's upload is refused without being consumed.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest

from _files_db_double import FilesDB, build_engine

from matrx_files.cloud_sync.transports.presigned import (
    OwnerMismatch,
    PresignedManager,
    UploadNotFound,
)

USER = "user-1"
ORG = "org-personal-0001"


class _S3:
    def get_presigned_put_url(self, path, **kw):
        return {"url": f"https://s3.test/{path}", "headers": {}, "expires_in": 900}


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, ORG))
    with db.bound():
        yield db


def _worker(files_db: FilesDB) -> PresignedManager:
    """A fresh manager + engine: its own process memory, the shared database."""
    engine = build_engine(files_db, user_id=USER, organization_id=ORG)
    engine._router.is_configured = lambda backend: backend == "s3"
    engine._router.s3 = _S3()
    engine.config.resolve_s3_bucket = lambda: "test-bucket"

    async def _urls(record):
        return {"url": None, "cdn_url": None}

    engine.build_urls_for_record_async = _urls
    return PresignedManager(engine)


async def test_upload_minted_on_one_worker_finalizes_on_another(files_db):
    minted = await _worker(files_db).create(owner_id=USER, file_path="docs/a.csv", content_type="text/csv")

    result = await _worker(files_db).finalize(
        upload_id=minted.upload_id, owner_id=USER, organization_id=ORG, actual_size_bytes=12
    )

    assert files_db.files.rows[result.file_id]["file_path"] == "docs/a.csv"


async def test_exactly_one_concurrent_finalize_wins(files_db):
    minted = await _worker(files_db).create(owner_id=USER, file_path="docs/b.csv", content_type="text/csv")
    a, b = _worker(files_db), _worker(files_db)

    results = await asyncio.gather(
        *(m.finalize(upload_id=minted.upload_id, owner_id=USER, organization_id=ORG) for m in (a, b)),
        return_exceptions=True,
    )

    assert sum(not isinstance(r, Exception) for r in results) == 1, results
    assert any(isinstance(r, UploadNotFound) for r in results), results


async def test_an_expired_upload_is_refused(files_db):
    minted = await _worker(files_db).create(owner_id=USER, file_path="docs/c.csv")
    for row in files_db.uploads_inflight.rows.values():
        row["expires_at"] = datetime.now(UTC) - timedelta(seconds=1)

    with pytest.raises(UploadNotFound):
        await _worker(files_db).finalize(upload_id=minted.upload_id, owner_id=USER, organization_id=ORG)


async def test_another_users_attempt_is_refused_and_does_not_consume_the_upload(files_db):
    minted = await _worker(files_db).create(owner_id=USER, file_path="docs/d.csv")

    with pytest.raises(OwnerMismatch):
        await _worker(files_db).finalize(upload_id=minted.upload_id, owner_id="user-2", organization_id=ORG)

    await _worker(files_db).finalize(upload_id=minted.upload_id, owner_id=USER, organization_id=ORG)


async def _finalize(files_db, path, checksum):
    minted = await _worker(files_db).create(owner_id=USER, file_path=path, content_type="text/csv")
    return await _worker(files_db).finalize(
        upload_id=minted.upload_id, owner_id=USER, organization_id=ORG, checksum=checksum
    )


async def test_same_bytes_at_another_path_get_their_own_row_linked_to_the_canonical(files_db):
    """Live 500 2026-10-27: the second same-content finalize hit cld_files_dedup_canonical."""
    first = await _finalize(files_db, "docs/one.csv", "sum-1")
    second = await _finalize(files_db, "docs/two.csv", "sum-1")

    assert second.file_id != first.file_id
    row = files_db.files.rows[second.file_id]
    assert row["file_path"] == "docs/two.csv" and row["duplicate_of_file_id"] == first.file_id


async def test_same_bytes_at_the_same_path_reuse_the_row(files_db):
    first = await _finalize(files_db, "docs/one.csv", "sum-2")
    again = await _finalize(files_db, "docs/one.csv", "sum-2")

    assert again.file_id == first.file_id and again.is_new is False


async def test_the_result_carries_the_share_fields_the_router_reads(files_db):
    """Live 500 2026-10-27: AttributeError 'PresignedFinalizeResult' has no 'share_token'."""
    result = await _finalize(files_db, "docs/e.csv", "sum-3")

    assert result.share_token is None and result.share_url is None
