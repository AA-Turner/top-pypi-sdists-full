"""A coding artifact lands with its identity in REAL COLUMNS, not only in JSONB.

SUT: the ONE upload door — ``FileService.upload_with_intent`` /
``SyncEngine.managed_write_async`` over the real ``DatabaseClient`` and the
insert constraints captured from Matrx Main (``_files_db_double``). S3 and IAM
RPCs are the only doubles.

WHY THIS FILE EXISTS (measured 2026-09-17 on production, CS-27/CS-30). The
coding-session Files tab filtered ``files.files`` by two JSONB paths —
``metadata->>'kind'`` and ``metadata->>'cli_session_id'`` — and 500'd about one
open in four. No index could save it: the table has RLS enabled and PostgreSQL
may not evaluate a non-LEAKPROOF qual before the security quals, so a ``->>``
qual can never become an index condition (161,861 rows walked, 4.8-29 s against
role ``authenticated``'s 8 s ceiling). The identity therefore lives in real
``text`` columns — ``artifact_kind`` and ``provider_session_id`` — where
``texteq`` is leakproof and a btree answers under RLS.

A column nobody fills is worse than no column: the panel would silently show an
empty session. These tests hold the door to filling BOTH columns on every shape
the coding-session publisher produces — a plain placement, and the
placement-ALIAS row a dedup'd upload creates (``duplicate_of_file_id``, CS-21)
— and to leaving them alone for a file that is not a produced artifact.

RED BEFORE: with the stamping removed from ``cloud_sync/sync_engine.py`` three
of these tests fail with ``artifact_kind`` absent from the written row (upload,
alias row, new version); the TUS leg covers the transport's own row insert,
which does not pass through that payload at all.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from _files_db_double import FilesDB, build_engine

from matrx_files.artifact_identity import artifact_identity_columns
from matrx_files.service import FileService

USER = "user-id"
PERSONAL_ORG = "org-personal-user-id"
SESSION = "0fdede4a-2ca9-4985-98a0-c6135bf58500"
OTHER_SESSION = "97ce06fb-fe43-496b-8c0d-08baed25bfa7"
BYTES = b"artifact bytes for the identity columns\n"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def _row(files_db: FilesDB, file_id: str) -> dict[str, Any]:
    return {str(r["id"]): r for r in files_db.files.rows.values()}[str(file_id)]


async def test_an_uploaded_coding_artifact_carries_both_columns(files_db, engine):
    """Break: the row lands with the identity ONLY in metadata, so the panel's
    indexed filter on the real columns finds nothing and the session looks
    empty."""
    result = await engine.managed_write_async(
        f"coding-sessions/claude_code/{SESSION}/docs/report.md",
        BYTES,
        user_id=USER,
        metadata=_artifact_metadata(SESSION, "docs/report.md"),
    )
    row = _row(files_db, result.file_id)

    assert row["artifact_kind"] == "coding_session_artifact"
    assert row["provider_session_id"] == SESSION
    # The JSONB contract is unchanged — the columns are a copy, not a move.
    assert row["metadata"]["cli_session_id"] == SESSION


async def test_the_placement_alias_row_carries_them_too(files_db, service):
    """Break: identical bytes at a second path become an alias row (CS-21) whose
    identity columns are empty, so that placement vanishes from its session."""
    first = await service.upload_with_intent(
        BYTES,
        intent="force_new_copy",
        reason=f"coding-session artifact placement: session {SESSION} path a.md",
        file_path=f"coding-sessions/claude_code/{SESSION}/a.md",
        owner_id=USER,
        metadata=_artifact_metadata(SESSION, "a.md"),
        auto_thumbnail=False,
        auto_rekey=False,
    )
    alias = await service.upload_with_intent(
        BYTES,
        intent="force_new_copy",
        reason=f"coding-session artifact placement: session {OTHER_SESSION} path a.md",
        file_path=f"coding-sessions/claude_code/{OTHER_SESSION}/a.md",
        owner_id=USER,
        metadata=_artifact_metadata(OTHER_SESSION, "a.md"),
        auto_thumbnail=False,
        auto_rekey=False,
    )

    alias_row = _row(files_db, alias["file_id"])
    assert str(alias_row["duplicate_of_file_id"]) == str(first["file_id"])
    assert alias_row["artifact_kind"] == "coding_session_artifact"
    assert alias_row["provider_session_id"] == OTHER_SESSION


async def test_a_new_version_of_an_artifact_keeps_the_columns(files_db, engine):
    """Break: the UPDATE path drops the columns the INSERT set, so a
    re-published artifact disappears from its session."""
    path = f"coding-sessions/claude_code/{SESSION}/changing.md"
    first = await engine.managed_write_async(
        path, BYTES, user_id=USER, metadata=_artifact_metadata(SESSION, "changing.md")
    )
    # The second write is an UPDATE of an existing row, which the door checks
    # write access for (the ACL stand-in denies by default).
    engine.permissions.allowed.add((USER, str(first.file_id), "write"))
    await engine.managed_write_async(
        path,
        BYTES + b"second version\n",
        user_id=USER,
        metadata=_artifact_metadata(SESSION, "changing.md"),
    )

    row = _row(files_db, first.file_id)
    assert row["artifact_kind"] == "coding_session_artifact"
    assert row["provider_session_id"] == SESSION


async def test_an_ordinary_upload_is_left_alone(files_db, engine):
    """Break: every file in the platform gets stamped, and `artifact_kind`
    becomes a dumping ground for every unrelated sense of the word `kind`."""
    result = await engine.managed_write_async(
        "documents/notes.md",
        b"not an artifact\n",
        user_id=USER,
        metadata={"kind": "user_upload", "cli_session_id": SESSION},
    )
    row = _row(files_db, result.file_id)

    assert row.get("artifact_kind") is None
    assert row.get("provider_session_id") is None


async def test_a_resumable_upload_lands_with_both_columns(monkeypatch):
    """Break: a coding artifact uploaded through the TUS transport (its own direct
    row insert, not the SyncEngine payload) is invisible to its session."""
    from _tus_harness import build_world, upload_file

    world = build_world(monkeypatch)
    owner = "tus-owner"
    _, result = await upload_file(
        world,
        owner=owner,
        path=f"coding-sessions/claude_code/{SESSION}/resumable.md",
        content=BYTES,
        metadata=_artifact_metadata(SESSION, "resumable.md"),
    )
    row = world.files.rows[result.file_id]

    assert row["artifact_kind"] == "coding_session_artifact"
    assert row["provider_session_id"] == SESSION


def test_the_derivation_itself_is_explicit_about_what_it_recognises():
    """The helper is the single place that decides; keep its answers honest."""
    assert artifact_identity_columns({"kind": "coding_session_artifact", "cli_session_id": "s"}) == {
        "artifact_kind": "coding_session_artifact",
        "provider_session_id": "s",
    }
    # A recognized kind with no session id is stamped as what it is, not guessed.
    assert artifact_identity_columns({"kind": "coding_session_artifact"}) == {
        "artifact_kind": "coding_session_artifact",
        "provider_session_id": None,
    }
    assert artifact_identity_columns({"kind": "variant"}) == {}
    assert artifact_identity_columns({}) == {}
    assert artifact_identity_columns(None) == {}
