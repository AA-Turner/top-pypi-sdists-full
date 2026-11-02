"""A path row of an organization the writer has LEFT is never adopted by a new upload.

Production defect D1 (2026-10-24, brand photo upload): admin owned ``Images/People/square.png``
in organization f9cb3e35 (no longer a member). Uploading ``Images/People/square.png`` for the
brand's own organization 884d1ce8 found that row by ``(created_by, file_path)`` (unique per
person, not per organization), adopted ITS organization and refused "user ... is not a member of
organization f9cb3e35". The folders were already per organization; the file row was the adopted one.

SUT: ``FileService.upload_simple`` over the real ``SyncEngine`` / ``DatabaseClient`` on the files
double, with rows mirroring the production ones.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService

ADMIN = "87a6e699-0000-4000-8000-000000000001"
BRAND_ORG = "884d1ce8-0000-4000-8000-00000000000a"
FORMER_ORG = "f9cb3e35-0000-4000-8000-00000000000b"
STILL_MEMBER_ORG = "2c1d4319-0000-4000-8000-00000000000c"
PATH = "Images/People/square.png"


def _seed(db: FilesDB, org: str, body: bytes) -> dict:
    folder = db.folders.create_sync(
        created_by=ADMIN, folder_path="Images/People", folder_name="People", organization_id=org
    ).to_dict()
    return db.files.create_sync(
        created_by=ADMIN, file_path=PATH, file_name="square.png", organization_id=org,
        parent_folder_id=folder["id"], checksum="seed-" + org,
        storage_uri=f"s3://test-bucket/{ADMIN}/seed-{org}",
    ).to_dict()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((ADMIN, BRAND_ORG))
    db.org_members.add((ADMIN, STILL_MEMBER_ORG))
    with db.bound():
        yield db


def _service(db: FilesDB) -> FileService:
    engine = build_engine(db, user_id=ADMIN, organization_id=BRAND_ORG)
    return FileService(SimpleNamespace(sync_engine=engine))


async def test_a_left_organizations_row_at_the_path_does_not_refuse_the_upload(files_db):
    old = _seed(files_db, FORMER_ORG, b"x")
    result = await _service(files_db).upload_simple(
        b"new photo bytes", file_path=PATH, user_id=ADMIN, organization_id=BRAND_ORG,
        auto_thumbnail=False, auto_rekey=False,
    )
    row = files_db.files.rows[str(result.file_id)]
    assert str(row["organization_id"]) == BRAND_ORG
    assert str(row["id"]) != str(old["id"])
    assert row["file_path"] == "Images/People/square (2).png"
    folder = files_db.folders.rows[str(row["parent_folder_id"])]
    assert str(folder["organization_id"]) == BRAND_ORG
    # The former organization's row is untouched.
    assert str(files_db.files.rows[str(old["id"])]["organization_id"]) == FORMER_ORG


async def test_a_row_of_an_organization_the_writer_still_belongs_to_keeps_converging(files_db):
    old = _seed(files_db, STILL_MEMBER_ORG, b"x")
    service = _service(files_db)
    service.sync_engine.permissions.allowed.add((ADMIN, str(old["id"]), "write"))
    result = await service.upload_simple(
        b"edited bytes", file_path=PATH, user_id=ADMIN, organization_id=BRAND_ORG,
        auto_thumbnail=False, auto_rekey=False,
    )
    assert str(result.file_id) == str(old["id"])
