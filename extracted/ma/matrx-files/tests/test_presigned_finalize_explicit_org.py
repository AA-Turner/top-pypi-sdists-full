"""The presigned upload lane names the upload's organization on every write (AD240).

SUT: ``PresignedManager.finalize`` — it owns the refusal of a missing organization, the folder
chain call, and the ``files.files`` payload. Real: ``PresignedManager``, ``SyncEngine``,
``DatabaseClient`` (the upsert and the RPC wrapper). Replaced: the SQL executor
(``tests/_files_db_double.py``, whose ``ensure_folder_chain`` follows package sql 041 and refuses
the retired 2-argument form), S3 (not configured, so the HEAD step is skipped) and the URL minter.

Breaks guarded: finalize calls ``ensure_folder_chain`` without the organization; passes a
different organization than the request's; omits it from the file row; swallows a refused chain
and lands the file with ``parent_folder_id`` NULL; or consumes the pending upload before refusing
a missing organization.
"""

from __future__ import annotations

import pytest

from _files_db_double import FilesDB, build_engine

from matrx_files.cloud_sync.transports.presigned import PresignedManager, _PendingEntry

USER = "user-1"
PERSONAL = "org-personal-0001"
TEAM = "org-team-0002"


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.update({(USER, PERSONAL), (USER, TEAM)})
    with db.bound():
        yield db


async def _manager(files_db: FilesDB, upload_id: str, file_path: str) -> PresignedManager:
    engine = build_engine(files_db, user_id=USER, organization_id=PERSONAL)
    engine._router.is_configured = lambda backend: False  # no S3: HEAD step skipped

    async def _urls(record):  # the URL minter is an external dependency here
        return {"url": None, "cdn_url": None}

    engine.build_urls_for_record_async = _urls
    manager = PresignedManager(engine)
    await manager._put_pending(
        upload_id,
        _PendingEntry(
            user_id=USER,
            file_path=file_path,
            storage_uri=f"s3://test-bucket/{USER}/{file_path}",
            content_type="application/pdf",
            published_to_web=False,
            shown_to="only_me",
        ),
    )
    return manager


@pytest.mark.parametrize("org", [PERSONAL, TEAM], ids=["personal-org-request", "team-org-request"])
async def test_finalize_writes_every_folder_and_the_file_in_the_requests_organization(files_db, org):
    manager = await _manager(files_db, "up-1", "projects/q3/report.pdf")

    try:
        result = await manager.finalize(upload_id="up-1", owner_id=USER, organization_id=org)
    except Exception as exc:
        pytest.fail(f"finalize into a new folder for {org} was refused: {exc!r}")

    folders = {r["folder_path"]: r for r in files_db.folders.rows.values()}
    assert {p: r["organization_id"] for p, r in folders.items()} == {"projects": org, "projects/q3": org}
    row = files_db.files.rows[result.file_id]
    assert (row["organization_id"], row["parent_folder_id"], row["file_path"]) == (
        org,
        folders["projects/q3"]["id"],
        "projects/q3/report.pdf",
    )


@pytest.mark.parametrize("missing", [None, ""], ids=["none", "empty"])
async def test_finalize_refuses_a_missing_organization_before_consuming_the_upload(files_db, missing):
    manager = await _manager(files_db, "up-2", "projects/q3/report.pdf")

    with pytest.raises(ValueError, match="organization_id is required"):
        await manager.finalize(upload_id="up-2", owner_id=USER, organization_id=missing)

    assert files_db.folders.rows == {} and files_db.files.rows == {}, "a write happened before the refusal"
    assert await manager._peek_pending("up-2") is not None, "the refusal consumed the pending upload; no retry possible"
