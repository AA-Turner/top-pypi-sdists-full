"""``FileService.upload_with_intent`` must never dedup-alias empty content.

Sibling of the guard added in ``test_managed_write_dedup.py`` for
``SyncEngine``'s five internal write-path mirrors (db7eb7f09c, jobs-bar
cold-walk-11, 2026-09-18). That fix closed every implicit write path but left
the ONE explicit door open: ``dedup.resolve_async`` — the preflight
``upload_with_intent`` (create / alias_existing / force_new_copy) runs before
handing off to ``SyncEngine.managed_write_async`` — still hashed empty
content with ``compute_checksum`` and looked it up like any real payload.
SHA-256 of empty content is the same constant hash
(``e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855``) for
every zero-byte upload, ever, in a scope, so a blank upload through this door
would resolve to whatever unrelated file first happened to be uploaded empty
in that owner/org: ``create`` raised ``DuplicateFileError`` against it (409,
visible — better than the silent SyncEngine case, but still wrong: the two
files share no content) and ``alias_existing`` silently returned it in place
of creating the caller's own row.

SUT: ``dedup.resolve_async`` via ``FileService.upload_with_intent`` — the
same harness as ``test_force_new_upload.py`` (real engine, real
``DatabaseClient`` double, S3/IAM doubled).
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.dedup import DuplicateFileError
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


def _seed_unrelated_empty_canonical(files_db: FilesDB) -> dict[str, Any]:
    """A pre-existing, completely unrelated file that also happens to be
    empty — the production row was ``official-mcat-content-outline.pdf``."""
    return files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path="docs/official-mcat-content-outline.pdf",
        checksum=_sha(b""),
        storage_uri="s3://test-bucket/user-id/unrelated-empty",
    )


async def _upload(service: FileService, content: bytes, intent: str, **kw: Any) -> dict:
    kw.setdefault("file_path", "docs/blank-upload.txt")
    return await service.upload_with_intent(
        content,
        intent=intent,
        owner_id=USER,
        auto_thumbnail=False,
        auto_rekey=False,
        **kw,
    )


async def test_create_of_empty_content_never_raises_duplicate_against_an_unrelated_empty_row(
    files_db, engine, service
):
    """Break: intent='create' with empty content raises DuplicateFileError
    against an unrelated pre-existing empty file, or lands as its alias."""
    unrelated = _seed_unrelated_empty_canonical(files_db)

    upload = await _upload(service, b"", "create")

    assert upload["outcome"] == "created"
    assert upload["file_id"] != unrelated["id"]
    assert upload["duplicate_of_file_id"] is None
    row = files_db.files.rows[upload["file_id"]]
    assert row["file_path"] == "docs/blank-upload.txt"
    assert row["checksum"] is None
    assert engine._router.objects[row["storage_uri"]] == b""
    assert sorted(r["id"] for r in files_db.live_files()) == sorted(
        [unrelated["id"], upload["file_id"]]
    )


async def test_alias_existing_of_empty_content_never_aliases_an_unrelated_empty_row(
    files_db, engine, service
):
    """Break: intent='alias_existing' with empty content silently returns the
    unrelated pre-existing empty file instead of creating the caller's own
    row (the exact production defect: a blank file's upload resolved to a
    completely unrelated file)."""
    unrelated = _seed_unrelated_empty_canonical(files_db)

    upload = await _upload(service, b"", "alias_existing")

    assert upload["outcome"] == "created"
    assert upload["file_id"] != unrelated["id"]
    assert upload["file_path"] == "docs/blank-upload.txt"
    assert upload["result"] is not None, "must have actually written its own row"
    row = files_db.files.rows[upload["file_id"]]
    assert row["checksum"] is None
    assert sorted(r["id"] for r in files_db.live_files()) == sorted(
        [unrelated["id"], upload["file_id"]]
    )


async def test_force_new_copy_of_empty_content_degenerates_to_its_own_create(
    files_db, engine, service
):
    """A force_new_copy of empty content has nothing legitimate to alias
    (empty carries no dedup identity), so it must simply create its own row
    rather than stamping duplicate_of_file_id at an unrelated empty file."""
    unrelated = _seed_unrelated_empty_canonical(files_db)

    upload = await _upload(service, b"", "force_new_copy", reason="deliberate blank capture")

    assert upload["file_id"] != unrelated["id"]
    assert upload["duplicate_of_file_id"] is None
    row = files_db.files.rows[upload["file_id"]]
    assert row["duplicate_of_file_id"] is None
    assert row["checksum"] is None


async def test_create_of_empty_content_still_succeeds_with_no_prior_empty_row(
    files_db, engine, service
):
    """Sanity: the guard doesn't just suppress all empty-content behavior —
    a plain create with nothing seeded still writes a fresh empty row."""
    upload = await _upload(service, b"", "create")

    assert upload["outcome"] == "created"
    row = files_db.files.rows[upload["file_id"]]
    assert row["checksum"] is None


async def test_create_of_real_duplicate_content_still_raises(files_db, engine, service):
    """Sanity: the guard is scoped to empty content only — a genuine
    non-empty duplicate must still raise DuplicateFileError as before."""
    content = b"real duplicate content"
    canonical = files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path="docs/real.pdf",
        checksum=_sha(content),
    )

    with pytest.raises(DuplicateFileError) as error:
        await _upload(service, content, "create", file_path="docs/other.pdf")

    assert error.value.existing_file_id == canonical["id"]
