"""An editor with a write grant saves a new version of a file SOMEONE ELSE owns.

SUT: ``SyncEngine.replace_file_async`` (the by-id write behind
``POST /files/{id}/versions``) with the REAL ``VersionManager`` over the
``_files_db_double``. Only S3 and the ACL judge are doubles.

Breaks guarded:
  * the new version's bytes land at the row's EXISTING storage_uri / path /
    owner (never under the editor);
  * the version row names the EDITOR as author and keeps ``change_summary``
    (it used to be stored null);
  * no write grant -> PermissionError and nothing is written.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_files.cloud_sync.versioning import VersionManager

from _files_db_double import FilesDB, build_engine

OWNER = "owner-1"
EDITOR = "editor-2"
STRANGER = "stranger-3"
ORG = "org-personal-0001"
URI = "s3://test-bucket/owner-1/notes.md"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((EDITOR, ORG))
    db.org_members.add((OWNER, ORG))
    with db.bound():
        yield db


def _engine(db: FilesDB):
    engine = build_engine(db, user_id=EDITOR, organization_id=ORG)
    engine.versions = VersionManager(
        engine._db,
        engine._router,
        SimpleNamespace(
            resolve_s3_bucket=lambda: "test-bucket",
            version_storage_prefix=".versions",
            storage_backend="s3",
        ),
    )
    return engine


def _seed(db: FilesDB, engine) -> dict:
    row = db.seed_file(
        created_by=OWNER,
        organization_id=ORG,
        file_path="docs/notes.md",
        storage_uri=URI,
        current_version=1,
        mime_type="text/markdown",
    )
    engine._router.objects[URI] = b"v1"
    return row


async def test_shared_editor_saves_a_version_under_the_owners_path(files_db):
    engine = _engine(files_db)
    row = _seed(files_db, engine)
    engine.permissions.allowed.add((EDITOR, row["id"], "write"))

    result = await engine.replace_file_async(
        row["id"], b"v2 by editor", user_id=EDITOR, change_summary="Fixed the intro"
    )

    assert result.file_id == row["id"]
    assert result.version_number == 2
    assert result.is_new is False
    stored = files_db.files.rows[row["id"]]
    assert stored["created_by"] == OWNER
    assert stored["file_path"] == "docs/notes.md"
    assert stored["storage_uri"] == URI
    assert engine._router.objects[URI] == b"v2 by editor"
    versions = [v for v in files_db.file_versions.rows.values() if v["file_id"] == row["id"]]
    assert len(versions) == 1
    assert versions[0]["version_number"] == 2
    assert versions[0]["created_by"] == EDITOR
    assert versions[0]["change_summary"] == "Fixed the intro"


async def test_a_caller_without_write_cannot_save_and_nothing_is_written(files_db):
    engine = _engine(files_db)
    row = _seed(files_db, engine)
    engine.permissions.allowed.add((STRANGER, row["id"], "read"))

    with pytest.raises(PermissionError):
        await engine.replace_file_async(
            row["id"], b"vandalised", user_id=STRANGER, change_summary="x"
        )

    assert engine._router.objects[URI] == b"v1"
    assert files_db.files.rows[row["id"]]["current_version"] == 1
    assert not files_db.file_versions.rows
