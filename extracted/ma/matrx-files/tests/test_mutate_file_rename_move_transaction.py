"""``FileService.mutate_file``'s rename + move stage is ONE transaction on the matrx-files pool.

SUT: stage 2 of ``FileService.mutate_file`` — it owns the order (folder chain, then move, then
rename) and the transaction boundary around all three. Real: ``FileService``, ``SyncEngine``,
``DatabaseClient`` and its RPC wrappers (SQLSTATE -> typed error). Replaced: only the SQL executor
(``tests/_files_db_double.py``): ``public.move_file`` / ``public.rename_file`` follow the live bodies,
and its ``matrx_orm.transaction`` refuses any pool but ``PACKAGE_DB_NAME`` — the pool every
``DatabaseClient`` RPC runs on — and rolls every row back on a raise, like Postgres.

Break guarded: the block opens ``transaction()`` with no database, which is the host's FIRST
configured database, while the RPCs run on the matrx-files pool; in a host with more than one
database a rename that conflicts after the move has landed leaves the file moved.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.dedup import FilePathConflictError
from matrx_files.service import FileService

USER = "user-1"
ORG = "org-personal-0001"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, ORG))
    with db.bound():
        yield db


def _world(files_db: FilesDB) -> tuple[FileService, dict[str, Any], dict[str, Any]]:
    engine = build_engine(files_db, user_id=USER, organization_id=ORG)
    service = FileService(SimpleNamespace(sync_engine=engine))
    archive = files_db.folders.create_sync(
        created_by=USER, organization_id=ORG, folder_path="archive", folder_name="archive"
    ).to_dict()
    report = files_db.seed_file(
        created_by=USER, organization_id=ORG, file_path="docs/report.pdf", storage_uri="s3://test-bucket/user-1/report"
    )
    files_db.seed_file(
        created_by=USER,
        organization_id=ORG,
        file_path="archive/taken.pdf",
        parent_folder_id=archive["id"],
        storage_uri="s3://test-bucket/user-1/taken",
    )
    engine.permissions.allowed.add((USER, report["id"], "write"))
    return service, archive, report


def _placement(files_db: FilesDB, file_id: str) -> tuple[Any, Any, Any]:
    row = files_db.files.rows[file_id]
    return row["file_path"], row["file_name"], row["parent_folder_id"]


# Break: the move commits on its own (wrong pool, or no shared transaction), so the
# rename's 409 is returned for a file that has already moved into archive/.
async def test_a_rename_that_conflicts_after_the_move_leaves_the_file_where_it_started(files_db):
    service, _archive, report = _world(files_db)

    with pytest.raises(FilePathConflictError):
        await service.mutate_file(report["id"], user_id=USER, name="taken.pdf", folder="archive")

    assert _placement(files_db, report["id"]) == ("docs/report.pdf", "report.pdf", None)


TEAM = "org-team-0002"


# AD240. Break: stage 2 calls ``ensure_folder_chain`` without an organization (the database
# then picks the owner's PERSONAL org, and move_file refuses the team file's move), or passes
# some organization other than the file's own. Two file organizations, two expected outcomes.
@pytest.mark.parametrize("file_org", [ORG, TEAM], ids=["personal-org-file", "team-org-file"])
async def test_a_move_into_a_new_folder_creates_it_in_the_files_own_organization(files_db, file_org):
    files_db.org_members.add((USER, TEAM))
    engine = build_engine(files_db, user_id=USER, organization_id=ORG)
    service = FileService(SimpleNamespace(sync_engine=engine))
    report = files_db.seed_file(
        created_by=USER,
        organization_id=file_org,
        file_path="docs/report.pdf",
        storage_uri=f"s3://test-bucket/user-1/report-{file_org}",
    )
    engine.permissions.allowed.add((USER, report["id"], "write"))

    try:
        await service.mutate_file(report["id"], user_id=USER, folder="projects/q3")
    except Exception as exc:
        pytest.fail(f"moving a {file_org} file into a new folder was refused: {exc!r}")

    folders = {r["folder_path"]: r for r in files_db.folders.rows.values()}
    assert {path: row["organization_id"] for path, row in folders.items()} == {
        "projects": file_org,
        "projects/q3": file_org,
    }, "a folder the move created does not carry the file's organization"
    assert _placement(files_db, report["id"]) == (
        "projects/q3/report.pdf",
        "report.pdf",
        folders["projects/q3"]["id"],
    )


# Break: either half is skipped, runs in the wrong order, or the block cannot open at all.
async def test_a_rename_and_move_that_both_succeed_land_together(files_db):
    service, archive, report = _world(files_db)

    envelope = await service.mutate_file(report["id"], user_id=USER, name="final.pdf", folder="archive")

    assert _placement(files_db, report["id"]) == ("archive/final.pdf", "final.pdf", archive["id"])
    assert [(c["old_path"], c["new_path"]) for c in envelope["path_changes"]] == [
        ("docs/report.pdf", "archive/report.pdf"),
        ("archive/report.pdf", "archive/final.pdf"),
    ]
