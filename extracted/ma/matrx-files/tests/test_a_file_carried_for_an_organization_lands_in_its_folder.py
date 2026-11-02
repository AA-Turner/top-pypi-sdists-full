"""A file a service carries FOR an organization lands in THAT organization's own folder.

SUT: ``FileService.upload_for_organization`` / ``ensure_organization_folder_async`` and
``SyncEngine.managed_write_async(exact_folder_organization=...)`` over the real
``DatabaseClient`` and the live folder constraint (``_files_db_double``: one folder tree per
person PER ORGANIZATION, unique on ``(created_by, organization_id, folder_path)`` since 2026-10-12). The request shape mirrors the record store's
caller without importing that host sibling, so this remains a standalone ``matrx-files`` test.

WHY THIS FILE EXISTS (production, 2026-09-25 09:11 UTC). admin@admin.com is a member of both
their own Workspace and Castellano & Reyes. The record store's context follow carried Castellano's
139,963-byte QME report into a file written as admin (the row's owner) at
``record-store/whole-values/...``. admin already owned ``record-store`` and
``record-store/whole-values`` in THEIR OWN organization (an earlier walk), so the engine found them
by ``(owner, path)``, logged "COERCED folder org mismatch" and reused them: Castellano's file sat
in a folder tree whose top half is admin's organization's. Nothing on the file said so.

Breaks guarded:
* a carried file's folder chain holds a folder of another organization (the live defect);
* a folder of another organization on an exact placement is reused instead of refused;
* a second carry of the same source makes a second folder (one folder per source);
* a person's ordinary upload into a path they hold in ANOTHER organization lands under that
  other organization's folder (the 2026-07-27 reuse ruling, retired 2026-10-12: it left 977 live
  files under another organization's folder, and every real move into one was refused
  "cross-organization move refused");
* a real move of such a file into a folder of its own organization is refused.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService

ADMIN = "87a6e699-0000-4000-8000-000000000001"
ADMIN_ORG = "884d1ce8-0000-4000-8000-00000000000a"
CLIENT_ORG = "7cd12da2-0000-4000-8000-00000000000b"
MATTER_TABLE = "1aaba65d-0000-4000-8000-0000000000c1"
REPORT = ("Qualified Medical Evaluator report — lumbar strain, 14 pages. " * 400).encode()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.update({(ADMIN, ADMIN_ORG), (ADMIN, CLIENT_ORG)})
    with db.bound():
        # What the earlier walk left: admin's OWN record-store tree, in admin's organization.
        root = db.folders.create_sync(
            created_by=ADMIN, folder_path="record-store", folder_name="record-store",
            organization_id=ADMIN_ORG,
        ).to_dict()
        db.folders.create_sync(
            created_by=ADMIN, folder_path="record-store/whole-values", folder_name="whole-values",
            organization_id=ADMIN_ORG, parent_id=root["id"],
        )
        yield db


@pytest.fixture
def service(files_db):
    # The operator's request carries admin's own organization — the file is for another one.
    engine = build_engine(files_db, user_id=ADMIN, organization_id=ADMIN_ORG)
    return FileService(SimpleNamespace(sync_engine=engine))


def _live_folder(db: FilesDB, folder_id: Any) -> dict[str, Any]:
    return db.folders.rows[str(folder_id)]


def _chain(db: FilesDB, file_row: dict[str, Any]) -> list[dict[str, Any]]:
    out, folder_id = [], file_row.get("parent_folder_id")
    while folder_id:
        folder = _live_folder(db, folder_id)
        out.append(folder)
        folder_id = folder.get("parent_id")
    return out


def _file(db: FilesDB, file_id: Any) -> dict[str, Any]:
    return db.files.rows[str(file_id)]


async def test_the_record_stores_carry_lands_in_the_organizations_record_store_folder(
    files_db, service
):
    """The record store's request shape: carry a value for Castellano as admin."""
    result = await service.upload_for_organization(
        REPORT,
        owner_id=ADMIN,
        organization_id=CLIENT_ORG,
        root="record-store",
        source_key=MATTER_TABLE,
        source_label="Matter",
        file_name="official_qme_report — 2645730c (v3).txt",
        mime_type="text/plain",
        published_to_web=False,
        file_id="ebad7d37-0000-5000-8000-000000000001",
        auto_thumbnail=False,
        auto_rekey=False,
    )
    file_id = result.file_id

    row = _file(files_db, file_id)
    assert row["organization_id"] == CLIENT_ORG
    chain = _chain(files_db, row)
    assert chain, "the file must sit in a folder"
    assert {f["organization_id"] for f in chain} == {CLIENT_ORG}, [
        (f["folder_path"], f["organization_id"]) for f in chain
    ]
    assert [f["folder_name"] for f in reversed(chain)] == ["Record store", "Matter"]
    assert "folder_placement" not in (row.get("metadata") or {})


async def test_one_folder_per_source_and_admins_own_tree_untouched(files_db, service):
    kwargs = dict(
        owner_id=ADMIN, organization_id=CLIENT_ORG, root="record-store",
        source_key=MATTER_TABLE, source_label="Matter", mime_type="text/plain",
        auto_thumbnail=False, auto_rekey=False,
    )
    first = await service.upload_for_organization(REPORT, file_name="a.txt", **kwargs)
    second = await service.upload_for_organization(REPORT + b"!", file_name="b.txt", **kwargs)

    a, b = _file(files_db, first.file_id), _file(files_db, second.file_id)
    assert a["parent_folder_id"] == b["parent_folder_id"]
    matter = [f for f in files_db.folders.rows.values() if f["folder_name"] == "Matter"]
    assert len(matter) == 1
    admins = {
        f["folder_path"]: f["organization_id"]
        for f in files_db.folders.rows.values()
        if f["folder_path"].startswith("record-store/") or f["folder_path"] == "record-store"
    }
    assert admins == {"record-store": ADMIN_ORG, "record-store/whole-values": ADMIN_ORG}


async def test_a_folder_of_another_organization_at_the_path_is_never_used(files_db, service):
    """A folder of admin's organization already sits at the organization-keyed path: the carry
    gets CLIENT_ORG's own folder there; admin's folder is untouched."""
    theirs = files_db.folders.create_sync(
        created_by=ADMIN, folder_path=f"record-store-{CLIENT_ORG}", folder_name="Record store",
        organization_id=ADMIN_ORG,
    ).to_dict()
    result = await service.upload_for_organization(
        REPORT, owner_id=ADMIN, organization_id=CLIENT_ORG, root="record-store",
        source_key=MATTER_TABLE, source_label="Matter", file_name="a.txt",
        mime_type="text/plain", auto_thumbnail=False, auto_rekey=False,
    )
    chain = _chain(files_db, _file(files_db, result.file_id))
    assert {f["organization_id"] for f in chain} == {CLIENT_ORG}
    assert theirs["id"] not in {f["id"] for f in chain}
    assert _live_folder(files_db, theirs["id"])["organization_id"] == ADMIN_ORG


async def test_a_persons_upload_lands_in_their_folder_tree_of_the_files_organization(
    files_db, service
):
    """admin holds ``record-store/whole-values`` in ADMIN_ORG; an upload there for CLIENT_ORG
    lands in CLIENT_ORG's own folders at the same path — never under ADMIN_ORG's — and the file
    says nothing about a coerced placement because there is none."""
    result = await service.upload_simple(
        REPORT, file_path="record-store/whole-values/notes.txt", user_id=ADMIN,
        organization_id=CLIENT_ORG, mime_type="text/plain",
        auto_thumbnail=False, auto_rekey=False,
    )
    row = _file(files_db, result.file_id)
    assert row["organization_id"] == CLIENT_ORG
    chain = _chain(files_db, row)
    assert [(f["folder_path"], f["organization_id"]) for f in reversed(chain)] == [
        ("record-store", CLIENT_ORG),
        ("record-store/whole-values", CLIENT_ORG),
    ]
    assert "folder_placement" not in (row.get("metadata") or {})
    # admin's own tree in ADMIN_ORG is still exactly one folder per path there.
    in_admin_org = sorted(
        f["folder_path"] for f in files_db.folders.rows.values()
        if f["organization_id"] == ADMIN_ORG and f.get("deleted_at") is None
    )
    assert in_admin_org == ["record-store", "record-store/whole-values"]


async def test_an_exact_write_by_path_lands_in_the_organizations_own_chain(files_db, service):
    result = await service.upload_simple(
        REPORT, file_path="record-store/whole-values/x/official_qme_report-v3.txt",
        user_id=ADMIN, organization_id=CLIENT_ORG, mime_type="text/plain",
        auto_thumbnail=False, auto_rekey=False, exact_folder_organization=True,
    )
    chain = _chain(files_db, _file(files_db, result.file_id))
    assert {f["organization_id"] for f in chain} == {CLIENT_ORG}


async def test_a_real_move_after_upload_into_a_path_held_in_another_org_succeeds(
    files_db, service
):
    """The reported defect end to end: the upload used to land under ADMIN_ORG's folder, and the
    next real move into another ``record-store`` folder was refused 403 "cross-organization move
    refused". Now the upload lands in CLIENT_ORG's chain and the move goes through."""
    result = await service.upload_simple(
        REPORT, file_path="record-store/whole-values/notes.txt", user_id=ADMIN,
        organization_id=CLIENT_ORG, mime_type="text/plain",
        auto_thumbnail=False, auto_rekey=False,
    )
    service._fm.sync_engine.permissions.allowed.add((ADMIN, str(result.file_id), "write"))
    envelope = await service.mutate_file(
        str(result.file_id), user_id=ADMIN, folder="record-store/archive"
    )
    assert not [e for e in envelope.get("errors") or [] if e.get("sub_op") == "move"]
    row = _file(files_db, result.file_id)
    assert row["file_path"] == "record-store/archive/notes.txt"
    chain = _chain(files_db, row)
    assert [(f["folder_path"], f["organization_id"]) for f in reversed(chain)] == [
        ("record-store", CLIENT_ORG),
        ("record-store/archive", CLIENT_ORG),
    ]
