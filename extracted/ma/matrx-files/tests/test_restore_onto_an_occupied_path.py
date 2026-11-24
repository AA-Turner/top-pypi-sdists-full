"""Restoring a trashed file whose path a live file has since taken never crashes (production 2026-11-19).

POST /files/{id}/restore raised cld_files_owner_id_file_path_key: a trash releases the
(owner, file_path) slot, another live file took it, and the restore only cleared deleted_at.
Now the restored file (same file_id) comes back at the first free ``name (n).ext``; the
occupant is untouched.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService

USER = "87a6e699-0000-4000-8000-000000000001"
ORG = "884d1ce8-0000-4000-8000-00000000000a"
PATH = "Docs/report.pdf"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, ORG))
    with db.bound():
        yield db


def _row(db: FilesDB, name: str, path: str, *, deleted: bool, tag: str) -> dict:
    return db.files.create_sync(
        created_by=USER, file_path=path, file_name=name, organization_id=ORG, checksum=tag,
        storage_uri=f"s3://test-bucket/{USER}/{tag}", deleted_at="2026-11-19T00:00:00Z" if deleted else None,
    ).to_dict()


def _service(db: FilesDB) -> FileService:
    engine = build_engine(db, user_id=USER, organization_id=ORG)
    async def _allow(*a, **k):  # permission judge is not the subject here
        return None
    engine.permissions = SimpleNamespace(require_async=_allow)
    return FileService(SimpleNamespace(sync_engine=engine))


async def test_restore_onto_an_occupied_path_lands_beside_it(files_db):
    trashed = _row(files_db, "report.pdf", PATH, deleted=True, tag="a")
    live = _row(files_db, "report.pdf", PATH, deleted=False, tag="b")
    assert await _service(files_db).restore(trashed["id"], user_id=USER) is True
    restored = files_db.files.rows[str(trashed["id"])]
    assert restored["deleted_at"] is None
    assert restored["file_path"] == "Docs/report (2).pdf" and restored["file_name"] == "report (2).pdf"
    occupant = files_db.files.rows[str(live["id"])]
    assert occupant["file_path"] == PATH and occupant["deleted_at"] is None


async def test_restore_skips_taken_suffixes(files_db):
    trashed = _row(files_db, "report.pdf", PATH, deleted=True, tag="a")
    _row(files_db, "report.pdf", PATH, deleted=False, tag="b")
    _row(files_db, "report (2).pdf", "Docs/report (2).pdf", deleted=False, tag="c")
    await _service(files_db).restore(trashed["id"], user_id=USER)
    assert files_db.files.rows[str(trashed["id"])]["file_path"] == "Docs/report (3).pdf"


async def test_restore_with_a_free_path_keeps_the_path(files_db):
    trashed = _row(files_db, "report.pdf", PATH, deleted=True, tag="a")
    assert await _service(files_db).restore(trashed["id"], user_id=USER) is True
    assert files_db.files.rows[str(trashed["id"])]["file_path"] == PATH
