"""An empty write must never replace a file that holds bytes.

Production defect (2026-10-22): image files in ``files.files`` were replaced by
ZERO-byte content — the row's ``current_version`` advanced, ``size_bytes`` went
to 0, the new ``file_versions`` row carried no checksum, and every later read
returned an empty body that no browser could decode. The write doors accepted
the empty body without a word because the empty-content guard only nulled the
checksum (its job: stop an empty upload aliasing an unrelated file).

Every writer that OVERWRITES an existing row by path or by id refuses the
empty body before any storage write or row update. Writing empty bytes over
empty bytes stays allowed, and a brand-new empty file still creates its row.
"""

from __future__ import annotations

import hashlib

import pytest
from matrx_files.cloud_sync.sync_engine import EmptyOverwriteRefused

from _files_db_double import FilesDB, build_engine

USER_ID = "user-1"
PERSONAL_ORG = "org-personal-0001"
FILE_PATH = "photos/avatar.jpg"
AT_PATH_URI = "s3://test-bucket/user-1/at-path"
PRIOR_BYTES = b"the photo the person already saved"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER_ID, PERSONAL_ORG))
    with db.bound():
        yield db


def _seed_file_with_bytes(db: FilesDB, *, size_bytes: int) -> dict:
    content = PRIOR_BYTES if size_bytes else b""
    row = db.seed_file(
        created_by=USER_ID,
        organization_id=PERSONAL_ORG,
        file_path=FILE_PATH,
        mime_type="image/jpeg",
        checksum=_sha(content) if content else None,
        size_bytes=size_bytes,
        storage_uri=AT_PATH_URI,
        current_version=2,
    )
    return row


async def _overwrite(engine, writer: str, file_id: str, content: bytes):
    if writer == "replace_file_async":
        return await engine.replace_file_async(file_id, content, user_id=USER_ID)
    if writer == "track_write_async":
        return await engine.track_write_async(FILE_PATH, content, user_id=USER_ID)
    return await engine.managed_write_async(FILE_PATH, content, user_id=USER_ID)


@pytest.mark.asyncio
@pytest.mark.parametrize("writer", ["managed_write_async", "replace_file_async", "track_write_async"])
async def test_empty_write_over_bytes_is_refused_and_leaves_the_file_intact(files_db, writer):
    row = _seed_file_with_bytes(files_db, size_bytes=len(PRIOR_BYTES))
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    engine._router.objects[AT_PATH_URI] = PRIOR_BYTES
    engine.permissions.allowed.add((USER_ID, row["id"], "write"))

    with pytest.raises(EmptyOverwriteRefused) as refused:
        await _overwrite(engine, writer, row["id"], b"")

    assert refused.value.http_status == 409
    assert refused.value.code == "empty_overwrite_refused"
    stored = files_db.files.rows[row["id"]]
    assert (stored["current_version"], stored["size_bytes"]) == (2, len(PRIOR_BYTES))
    assert stored["checksum"] == _sha(PRIOR_BYTES)
    assert engine._router.objects[AT_PATH_URI] == PRIOR_BYTES


@pytest.mark.asyncio
@pytest.mark.parametrize("writer", ["managed_write_async", "replace_file_async", "track_write_async"])
async def test_empty_write_over_an_empty_file_is_still_allowed(files_db, writer):
    row = _seed_file_with_bytes(files_db, size_bytes=0)
    engine = build_engine(files_db, user_id=USER_ID, organization_id=PERSONAL_ORG)
    engine._router.objects[AT_PATH_URI] = b""
    engine.permissions.allowed.add((USER_ID, row["id"], "write"))

    await _overwrite(engine, writer, row["id"], b"")

    stored = files_db.files.rows[row["id"]]
    assert stored["current_version"] == 3
    assert stored["size_bytes"] == 0
