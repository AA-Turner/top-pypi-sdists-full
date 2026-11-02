"""One content, many PLACEMENTS — and a write result never claims a path the
server discarded.

SUT: ``SyncEngine.managed_write_async`` and ``FileService.upload_with_intent``
over the real ``DatabaseClient`` and the insert constraints captured from Matrx
Main (``_files_db_double``). S3 and IAM RPCs are the only doubles.

WHY THIS FILE EXISTS (measured 2026-09-17 on production). A coding session's
artifacts are uploaded one file per (session, relative path). An undeclared
write is implicitly ``alias_existing``: when the bytes already exist for this
owner+organization the engine short-circuits to the CANONICAL row and the path
the caller asked for is recorded NOWHERE. 287 artifacts of three sessions were
therefore filed under another session's row, and the app's Artifacts panel —
which lists rows carrying a session's id — could not show them. The bytes were
never lost; the placement was. Two invariants keep that from recurring:

1. a declared placement gets a ROW OF ITS OWN at its own path, carrying its own
   metadata, linked to the canonical content by ``duplicate_of_file_id``;
2. an implicit alias is never dressed up as the caller's path — the result
   names the row it actually landed on, so a door cannot echo a path the server
   threw away (which is exactly how the desktop ledger came to believe in
   placements that did not exist).
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.service import FileService

USER = "user-id"
PERSONAL_ORG = "org-personal-user-id"
SESSION_A = "0fdede4a-2ca9-4985-98a0-c6135bf58500"
SESSION_B = "97ce06fb-fe43-496b-8c0d-08baed25bfa7"
BYTES = b"identical artifact bytes\n"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _artifact_path(session: str, rel: str) -> str:
    return f"coding-sessions/claude_code/{session}/{rel}"


def _artifact_metadata(session: str, rel: str) -> dict[str, Any]:
    return {
        "kind": "coding_session_artifact",
        "provider": "claude_code",
        "cli_session_id": session,
        "relative_path": rel,
        "sha256": _sha(BYTES),
    }


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


async def _place(service: FileService, session: str, rel: str) -> dict[str, Any]:
    """Upload one artifact the way the coding-session publisher now does."""
    return await service.upload_with_intent(
        BYTES,
        intent="force_new_copy",
        reason=f"coding-session artifact placement: session {session} path {rel}",
        file_path=_artifact_path(session, rel),
        owner_id=USER,
        metadata=_artifact_metadata(session, rel),
        auto_thumbnail=False,
        auto_rekey=False,
    )


async def test_two_sessions_with_identical_bytes_each_keep_their_own_row(
    files_db, service
):
    """Break: the second session's upload resolves to the first session's row,
    so a panel filtered on the second session's id shows nothing."""
    first = await _place(service, SESSION_A, "report.md")
    second = await _place(service, SESSION_B, "report.md")

    assert first["file_id"] != second["file_id"]

    rows = {
        str(row["id"]): row
        for row in files_db.files.rows.values()
        if row.get("deleted_at") is None
    }
    a, b = rows[str(first["file_id"])], rows[str(second["file_id"])]
    assert a["file_path"] == _artifact_path(SESSION_A, "report.md")
    assert b["file_path"] == _artifact_path(SESSION_B, "report.md")
    # Each row answers for ITS OWN session — this is the panel's filter.
    assert a["metadata"]["cli_session_id"] == SESSION_A
    assert b["metadata"]["cli_session_id"] == SESSION_B
    # One content behind them: the second row is the first's dedup alias.
    assert str(b["duplicate_of_file_id"]) == str(first["file_id"])
    assert a["checksum"] == b["checksum"] == _sha(BYTES)


async def test_one_session_with_two_paths_of_identical_bytes_keeps_both(
    files_db, service
):
    """Break: the session's two paths collapse into one entry in the panel."""
    first = await _place(service, SESSION_A, "docs/report.md")
    second = await _place(service, SESSION_A, "build/report.md")

    assert first["file_id"] != second["file_id"]
    paths = {
        str(row["file_path"])
        for row in files_db.files.rows.values()
        if row.get("deleted_at") is None
        and (row.get("metadata") or {}).get("cli_session_id") == SESSION_A
    }
    assert paths == {
        _artifact_path(SESSION_A, "docs/report.md"),
        _artifact_path(SESSION_A, "build/report.md"),
    }


async def test_an_implicit_alias_result_names_the_row_it_landed_on(files_db, engine):
    """Break: the write result echoes the requested path although the engine
    kept the canonical row — the lie every door repeated to its client."""
    canonical = files_db.seed_file(
        created_by=USER,
        organization_id=PERSONAL_ORG,
        file_path=_artifact_path(SESSION_A, "report.md"),
        checksum=_sha(BYTES),
    )

    requested = _artifact_path(SESSION_B, "report.md")
    result = await engine.managed_write_async(
        requested,
        BYTES,
        user_id=USER,
        metadata=_artifact_metadata(SESSION_B, "report.md"),
    )

    assert str(result.file_id) == str(canonical["id"])
    assert result.is_new is False
    assert result.file_path == _artifact_path(SESSION_A, "report.md")
    assert result.file_path != requested


async def test_a_plain_write_to_a_free_path_reports_that_path(files_db, engine):
    """The honest case keeps working: no duplicate content, own row, own path."""
    result = await engine.managed_write_async(
        _artifact_path(SESSION_A, "notes.md"),
        b"unique bytes\n",
        user_id=USER,
        metadata=_artifact_metadata(SESSION_A, "notes.md"),
    )
    assert result.is_new is True
    assert result.file_path == _artifact_path(SESSION_A, "notes.md")


async def test_the_default_upload_door_gives_a_second_path_its_own_row(files_db, service):
    """Break (walker, 2026-10-21): ``a.txt`` then ``b.txt`` with the same bytes
    through the default ``alias_existing`` door answered ``b.txt`` with
    ``a.txt``'s id and recorded ``b.txt`` nowhere. Dedupe is a storage concern;
    it never means "no row" (main's ruling)."""

    async def put(path: str) -> dict[str, Any]:
        return await service.upload_with_intent(
            BYTES, intent="alias_existing", file_path=path, owner_id=USER,
            auto_thumbnail=False, auto_rekey=False,
        )

    first = await put("Docs/a.txt")
    second = await put("Docs/b.txt")
    again = await put("Docs/a.txt")

    assert first["file_id"] != second["file_id"]
    live = {
        str(r["file_path"]): r for r in files_db.files.rows.values() if r.get("deleted_at") is None
    }
    assert set(live) == {"Docs/a.txt", "Docs/b.txt"}
    assert str(live["Docs/b.txt"]["duplicate_of_file_id"]) == str(first["file_id"])
    # The same bytes at the SAME path are still the existing row, not a copy.
    assert str(again["file_id"]) == str(first["file_id"])


async def test_the_default_buffered_door_gives_a_second_path_its_own_row(files_db, service, engine):
    """Break (live probe 2026-10-21): POST /files/upload with no intent -- on
    files.matrxserver.com and on aidream, which both land in ``upload_simple``
    -- answered ``b.txt`` with ``a.txt``'s id and wrote no row at ``b.txt``."""

    async def put(path: str):
        return await service.upload_simple(
            BYTES, file_path=path, user_id=USER, auto_thumbnail=False, auto_rekey=False,
        )

    first = await put("Docs/a.txt")
    second = await put("Docs/b.txt")
    # The owner's write access on their own file, as the host checker answers it.
    engine.permissions.allowed.add((USER, str(first.file_id), "write"))
    again = await put("Docs/a.txt")

    assert str(first.file_id) != str(second.file_id)
    live = {
        str(r["file_path"]): r for r in files_db.files.rows.values() if r.get("deleted_at") is None
    }
    assert {"Docs/a.txt", "Docs/b.txt"} <= set(live)
    assert str(live["Docs/b.txt"]["duplicate_of_file_id"]) == str(first.file_id)
    assert str(again.file_id) == str(first.file_id), "same bytes at the same path stay the same file"
