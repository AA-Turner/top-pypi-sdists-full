"""A file a service carries FOR an organization lands under its PATHWAY, never ``<root>-<org uuid>``.

SUT: ``FileService.upload_for_organization`` / ``ensure_organization_folder_async`` over the real
``DatabaseClient`` double (folders unique per ``(created_by, organization_id, folder_path)``; files
unique per ``(created_by, file_path)`` with no organization).

WHY (placement registry Lane 5, 2026-10-31). The mover took 13,792 carried rows out of
``<root>-<org uuid>/…`` trees into the one System folder, but the door kept writing the old trees,
so every moved family grew back at its old root. The door now resolves the pathway that claims the
root (its ``legacy_prefixes`` name ``"<root>-"``) and stamps it. Breaks guarded:
* a carried file lands at ``<root>-<org uuid>/…`` or unstamped;
* the folder chain holds a folder of another organization;
* a second organization's file at the same path converges on the first organization's row (the
  path key has no organization in it) instead of taking the mover's ``name (<org8>).ext``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files import placement
from matrx_files.service import FileService

ADMIN = "87a6e699-0000-4000-8000-000000000001"
ADMIN_ORG = "884d1ce8-0000-4000-8000-00000000000a"
CLIENT_ORG = "7cd12da2-0000-4000-8000-00000000000b"
KEY = "carrytest.big_value"


@pytest.fixture(autouse=True)
def carried_pathway():
    placement.register_pathway(
        KEY, owner_feature="platform/records", audience="automated", root="system",
        subfolder="carrytest/{source}", naming="id_only", description="Test: values carried for an org.",
        legacy_prefixes=("record-store-",),
    )
    yield
    placement._PATHWAYS.pop(KEY, None)


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.update({(ADMIN, ADMIN_ORG), (ADMIN, CLIENT_ORG)})
    with db.bound():
        yield db


def _service(db: FilesDB, org: str) -> FileService:
    return FileService(SimpleNamespace(sync_engine=build_engine(db, user_id=ADMIN, organization_id=org)))


def _carry(svc: FileService, org: str, body: bytes):
    return svc.upload_for_organization(
        body, owner_id=ADMIN, organization_id=org, root="record-store",
        source_key="imports", source_label="Imports", sub_folders=["abc123"], file_name="value.txt",
        mime_type="text/plain", published_to_web=False, auto_thumbnail=False, auto_rekey=False,
    )


def test_the_root_resolves_to_the_pathway_that_claims_it():
    assert placement.pathway_for_carried_root("record-store").key <= KEY
    assert placement.carried_folder_segments(KEY, "imports", "Imports") == [
        ("system-files", "System"), ("carrytest", "carrytest"), ("imports", "Imports"),
    ]
    # A base that already ends with the source does not repeat it.
    assert [s for s, _ in placement.carried_folder_segments(KEY, "carrytest", "x")] == ["system-files", "carrytest"]
    assert placement.org_suffixed_name("a.tar.gz", CLIENT_ORG) == "a.tar (7cd12da2).gz"
    assert placement.org_suffixed_name("README", CLIENT_ORG) == "README (7cd12da2)"


async def test_a_carried_file_lands_in_system_stamped_in_its_organization(files_db):
    result = await _carry(_service(files_db, ADMIN_ORG), CLIENT_ORG, b"value one")
    row = files_db.files.rows[str(result.file_id)]
    assert row["file_path"] == "system-files/carrytest/imports/abc123/value.txt"
    assert row["organization_id"] == CLIENT_ORG
    assert row.get("file_pathway") == KEY
    assert (row.get("metadata") or {}).get("system_artifact") is True
    chain_orgs = {
        f["organization_id"] for f in files_db.folders.rows.values() if f["folder_path"].startswith("system-files")
    }
    assert chain_orgs == {CLIENT_ORG}
    assert not any(f["folder_path"].startswith("record-store-") for f in files_db.folders.rows.values())


async def test_a_second_organization_never_converges_on_the_first_ones_row(files_db):
    first = await _carry(_service(files_db, ADMIN_ORG), CLIENT_ORG, b"client value")
    second = await _carry(_service(files_db, ADMIN_ORG), ADMIN_ORG, b"admin value")
    a, b = files_db.files.rows[str(first.file_id)], files_db.files.rows[str(second.file_id)]
    assert a["id"] != b["id"]
    assert a["organization_id"] == CLIENT_ORG and b["organization_id"] == ADMIN_ORG
    assert b["file_path"] == "system-files/carrytest/imports/abc123/value (884d1ce8).txt"
