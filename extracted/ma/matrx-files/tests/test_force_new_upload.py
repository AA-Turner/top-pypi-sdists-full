"""FileService.upload_with_intent — the strict-intent upload contract.

SUT: ``FileService.upload_with_intent`` — it owns org resolution, the
preflight dedup decision (``dedup.resolve_async``), mapping each decision onto
``SyncEngine.managed_write_async`` (``create_only``, ``duplicate_of_file_id``,
the force-copy reason), and reconciling a canonical row that wins AFTER the
preflight. Every one of those runs for real here: the real engine, the real
``DatabaseClient`` checksum/path queries, and the insert constraints CAPTURED
from Matrx Main (``_files_db_double``). S3 and IAM RPCs are the only doubles.

A "winner after preflight" is produced honestly: the real checksum lookup runs,
returns its answer, and THEN a concurrent canonical row lands — so the
preflight misses and the engine's own lookup / insert sees the winner.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.dedup import DuplicateFileError, FilePathConflictError
from matrx_files.service import FileService

USER = "user-id"
PERSONAL_ORG = "org-personal-user-id"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def files_db():
    db = FilesDB()
    db.org_members.add((USER, PERSONAL_ORG))
    with db.bound():
        yield db


@pytest.fixture
def engine(files_db):
    return build_engine(files_db, user_id=USER, organization_id=PERSONAL_ORG)


@pytest.fixture
def service(engine):
    return FileService(SimpleNamespace(sync_engine=engine))


def _canonical_lands_after_preflight(files_db: FilesDB, engine: Any, content: bytes) -> dict:
    winner: dict[str, Any] = {}
    real_lookup = engine._db.get_file_by_checksum_async

    async def lookup_then_concurrent_insert(checksum, *, owner_id=None, organization_id=None):
        found = await real_lookup(checksum, owner_id=owner_id, organization_id=organization_id)
        if not winner:
            winner.update(
                files_db.seed_file(
                    created_by=USER,
                    organization_id=PERSONAL_ORG,
                    file_path="docs/winner.pdf",
                    checksum=_sha(content),
                    storage_uri="s3://test-bucket/user-id/winner-id",
                )
            )
        return found

    engine._db.get_file_by_checksum_async = lookup_then_concurrent_insert
    return winner


async def _upload(service: FileService, content: bytes, intent: str, **kw: Any) -> dict:
    kw.setdefault("file_path", "docs/upload.pdf")
    return await service.upload_with_intent(
        content,
        intent=intent,
        owner_id=USER,
        auto_thumbnail=False,
        auto_rekey=False,
        **kw,
    )


async def test_force_new_copy_of_owned_content_creates_a_distinct_alias_row(
    files_db, engine, service
):
    """Break: force_new_copy is treated as alias (no new row) or the new row
    does not point back at the canonical."""
    content = b"same bytes"
    canonical = files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path="docs/original.pdf",
        checksum=_sha(content),
    )

    upload = await _upload(service, content, "force_new_copy", reason="immutable capture")

    row = files_db.files.rows[upload["file_id"]]
    assert upload["outcome"] == "force_copy_created"
    assert upload["file_id"] != canonical["id"]
    assert upload["duplicate_of_file_id"] == canonical["id"]
    assert row["duplicate_of_file_id"] == canonical["id"]
    assert row["metadata"]["force_new_copy_reason"] == "immutable capture"
    assert engine._router.objects == {row["storage_uri"]: content}


async def test_force_new_retries_as_alias_when_canonical_wins_after_preflight(
    files_db, engine, service
):
    """Break: the post-preflight winner is returned as the "new" copy, or the
    retry does not mark itself as the winner's alias (the dedup index would
    then reject it)."""
    content = b"same bytes"
    winner = _canonical_lands_after_preflight(files_db, engine, content)

    upload = await _upload(
        service,
        content,
        "force_new_copy",
        file_path="system-files/scraper/capture-id/body.html",
        reason="immutable capture",
    )

    row = files_db.files.rows[upload["file_id"]]
    assert upload["outcome"] == "force_copy_created"
    assert upload["file_id"] != winner["id"]
    assert upload["duplicate_of_file_id"] == winner["id"]
    assert row["duplicate_of_file_id"] == winner["id"]
    assert row["file_path"] == "system-files/scraper/capture-id/body.html"
    assert sorted(r["id"] for r in files_db.live_files()) == sorted([winner["id"], row["id"]])


async def test_create_refuses_owned_content_before_writing_anything(files_db, engine, service):
    content = b"already uploaded"
    canonical = files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path="docs/original.pdf",
        checksum=_sha(content),
    )

    with pytest.raises(DuplicateFileError) as error:
        await _upload(service, content, "create")

    assert error.value.existing_file_id == canonical["id"]
    assert error.value.existing_path == "docs/original.pdf"
    assert engine._router.objects == {}
    assert [r["id"] for r in files_db.live_files()] == [canonical["id"]]


async def test_create_reports_conflict_when_canonical_wins_after_preflight(
    files_db, engine, service
):
    """Break: intent=create silently accepts the concurrent winner as its own
    upload instead of surfacing the duplicate."""
    content = b"same bytes"
    winner = _canonical_lands_after_preflight(files_db, engine, content)

    with pytest.raises(DuplicateFileError) as error:
        await _upload(service, content, "create")

    assert error.value.existing_file_id == winner["id"]
    assert error.value.existing_path == "docs/winner.pdf"
    assert engine._router.objects == {}
    assert [r["id"] for r in files_db.live_files()] == [winner["id"]]


async def test_alias_reuses_canonical_that_wins_after_preflight(files_db, engine, service):
    content = b"same bytes"
    winner = _canonical_lands_after_preflight(files_db, engine, content)

    upload = await _upload(service, content, "alias_existing")

    assert upload["outcome"] == "aliased"
    assert upload["file_id"] == winner["id"]
    assert upload["file_path"] == "docs/winner.pdf"
    assert upload["result"] is None
    assert engine._router.objects == {}


@pytest.mark.parametrize("intent", ["create", "alias_existing", "force_new_copy"])
async def test_strict_intents_never_overwrite_an_occupied_path(
    files_db, engine, service, intent
):
    """Break: a strict intent falls back to the legacy save-over-path update and
    replaces another file's bytes."""
    occupied = files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path="docs/occupied.pdf",
        checksum=_sha(b"the occupant"),
        storage_uri="s3://test-bucket/user-id/occupant",
        current_version=2,
    )
    engine.permissions.allowed.add((USER, occupied["id"], "write"))

    with pytest.raises(FilePathConflictError):
        await _upload(
            service,
            b"different bytes",
            intent,
            file_path="docs/occupied.pdf",
            reason="deliberate copy" if intent == "force_new_copy" else None,
        )

    row = files_db.files.rows[occupied["id"]]
    assert (row["checksum"], row["current_version"]) == (_sha(b"the occupant"), 2)
    assert engine._router.objects == {}
    assert [r["id"] for r in files_db.live_files()] == [occupied["id"]]
