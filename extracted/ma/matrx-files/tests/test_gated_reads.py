"""The gated column/byte reads answer the gate's question, fail-closed.

No user and no declared job → refused; a declared job → every row; a request
user → only the rows the host access checker clears; a stored-byte read only
serves an object that is the file's own.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_utils.ctx import system_file_access

import matrx_files.db.models_files as models_files
from matrx_files import gated_reads
from matrx_files.cloud_sync import permissions


class _Query:
    def __init__(self, rows: list[dict[str, Any]], filters: dict[str, Any], where: tuple[Any, ...] = ()) -> None:
        self._rows = rows
        self._filters = filters
        self._where = where

    def order_by(self, *_: str) -> _Query:
        return self

    def offset(self, _: int) -> _Query:
        return self

    def limit(self, _: int) -> _Query:
        return self

    async def values(self, *cols: str) -> list[dict[str, Any]]:
        def keep(row: dict[str, Any]) -> bool:
            if not all(pred(row) for pred in self._where):
                return False
            for key, want in self._filters.items():
                if key == "id__in":
                    if row["id"] not in want:
                        return False
                elif key == "deleted_at__isnull":
                    if (row.get("deleted_at") is None) != want:
                        return False
                elif row.get(key) != want:
                    return False
            return True

        return [{c: r.get(c) for c in cols} for r in self._rows if keep(r)]


class _Model:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def filter(self, *where: Any, **filters: Any) -> _Query:
        return _Query(self.rows, filters, where)


FILES = [
    {"id": "f-mine", "file_name": "mine.pdf", "storage_uri": "s3://b/mine", "deleted_at": None},
    {"id": "f-theirs", "file_name": "theirs.pdf", "storage_uri": "s3://b/theirs", "deleted_at": None},
    {"id": "f-trashed", "file_name": "old.pdf", "storage_uri": "s3://b/old", "deleted_at": "2026-01-01"},
]
FOLDERS = [
    {"id": "d-mine", "folder_name": "mine", "parent_id": None, "deleted_at": None},
    {"id": "d-theirs", "folder_name": "theirs", "parent_id": None, "deleted_at": None},
    {"id": "d-trashed", "folder_name": "old", "parent_id": None, "deleted_at": "2026-01-01"},
]
VERSIONS = [{"id": "v1", "file_id": "f-mine", "storage_uri": "s3://b/mine-v1"}]


@pytest.fixture(autouse=True)
def _tables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(models_files, "Files", _Model(FILES))
    monkeypatch.setattr(models_files, "FileVersions", _Model(VERSIONS))
    monkeypatch.setattr(models_files, "Folders", _Model(FOLDERS))
    monkeypatch.setattr(gated_reads, "_ambient_user_id", lambda: "")


def _as_user(monkeypatch: pytest.MonkeyPatch, readable: set[str]) -> None:
    async def checker(uid: str, rtype: str, rid: str, level: str) -> bool:
        return uid == "u-1" and rtype == "file" and rid in readable

    monkeypatch.setattr(gated_reads, "_ambient_user_id", lambda: "u-1")
    monkeypatch.setattr(permissions, "_access_checker", checker)


async def test_no_user_and_no_declared_job_is_refused() -> None:
    with pytest.raises(PermissionError):
        await gated_reads.read_file_rows(["file_name"], id__in=["f-mine"])


async def test_a_declared_job_reads_every_matching_row() -> None:
    with system_file_access("test-job"):
        rows = await gated_reads.read_file_rows(["file_name"], live_only=True, id__in=["f-mine", "f-theirs", "f-trashed"])
    assert sorted(r["id"] for r in rows) == ["f-mine", "f-theirs"]


async def test_a_request_user_sees_only_what_the_checker_clears(monkeypatch: pytest.MonkeyPatch) -> None:
    _as_user(monkeypatch, {"f-mine"})
    rows = await gated_reads.read_file_rows(["file_name"], id__in=["f-mine", "f-theirs"])
    assert [r["id"] for r in rows] == ["f-mine"]
    assert await gated_reads.read_file_row("f-theirs", ["file_name"]) is None


async def test_a_whole_table_scan_is_never_offered() -> None:
    with system_file_access("test-job"), pytest.raises(ValueError):
        await gated_reads.read_file_rows(["file_name"])


class _Router:
    async def read_async(self, uri: str) -> bytes:
        return f"bytes of {uri}".encode()


class _Fm:
    class sync_engine:  # noqa: N801 — mirrors FileManager.sync_engine
        router = _Router()


async def test_stored_bytes_serve_only_the_files_own_objects(monkeypatch: pytest.MonkeyPatch) -> None:
    _as_user(monkeypatch, {"f-mine"})
    assert await gated_reads.read_stored_bytes(_Fm(), "f-mine", "s3://b/mine-v1") == b"bytes of s3://b/mine-v1"
    with pytest.raises(FileNotFoundError):
        await gated_reads.read_stored_bytes(_Fm(), "f-mine", "s3://b/theirs")
    with pytest.raises(PermissionError):
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs")


async def test_a_named_principal_is_decided_like_an_ambient_one(monkeypatch: pytest.MonkeyPatch) -> None:
    async def checker(uid: str, rtype: str, rid: str, level: str) -> bool:
        return uid == "u-2" and rid == "f-mine"

    monkeypatch.setattr(permissions, "_access_checker", checker)
    # No ambient user, no declared job: the named principal alone is asked.
    assert await gated_reads.read_stored_bytes(_Fm(), "f-mine", "s3://b/mine", user_id="u-2") == b"bytes of s3://b/mine"
    with pytest.raises(PermissionError):
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs", user_id="u-2")


@pytest.fixture
def _post_door(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, frozenset[str]]]:
    """A registered parent door: post p-1 names f-theirs only."""
    asked: list[tuple[str, frozenset[str]]] = []

    async def reached(parent_id: str, file_ids: frozenset[str]) -> set[str]:
        asked.append((parent_id, file_ids))
        return {"f-theirs"} & file_ids if parent_id == "p-1" else set()

    monkeypatch.setattr(gated_reads, "_PARENT_DOORS", {})
    gated_reads.register_parent_door("test_post", reached)
    return asked


async def test_a_parent_door_serves_only_the_files_its_parent_names(
    _post_door: list[tuple[str, frozenset[str]]],
) -> None:
    assert (
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs", parent_grant="test_post:p-1")
        == b"bytes of s3://b/theirs"
    )
    assert _post_door[-1] == ("p-1", frozenset({"f-theirs"}))
    # The door never reaches a file its parent does not name, nor another parent's file.
    with pytest.raises(PermissionError):
        await gated_reads.read_stored_bytes(_Fm(), "f-mine", "s3://b/mine", parent_grant="test_post:p-1")
    with pytest.raises(PermissionError):
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs", parent_grant="test_post:p-2")
    # And it still serves only the file's own stored objects.
    with pytest.raises(FileNotFoundError):
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/mine", parent_grant="test_post:p-1")
    rows = await gated_reads.read_file_rows(["file_name"], parent_grant="test_post:p-1", id__in=["f-mine", "f-theirs"])
    assert [r["id"] for r in rows] == ["f-theirs"]


async def test_an_unregistered_or_unnamed_parent_door_is_refused(
    _post_door: list[tuple[str, frozenset[str]]],
) -> None:
    with pytest.raises(gated_reads.FileReadDenied):
        await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs", parent_grant="esign_envelope:e-1")
    for unnamed in ("", "test_post", "test_post:", ":p-1"):
        with pytest.raises(ValueError):
            await gated_reads.read_stored_bytes(_Fm(), "f-theirs", "s3://b/theirs", parent_grant=unnamed)
    with pytest.raises(ValueError):
        gated_reads.register_parent_door("bad:name", lambda *_: None)  # type: ignore[arg-type,return-value]


async def test_files_outside_the_door_fall_to_the_principal(
    monkeypatch: pytest.MonkeyPatch, _post_door: list[tuple[str, frozenset[str]]]
) -> None:
    async def checker(uid: str, rtype: str, rid: str, level: str) -> bool:
        return uid == "u-2" and rid == "f-mine"

    monkeypatch.setattr(permissions, "_access_checker", checker)
    allowed = await gated_reads.readable_file_ids(
        ["f-mine", "f-theirs", "f-trashed"], parent_grant="test_post:p-1", user_id="u-2"
    )
    assert allowed == {"f-mine", "f-theirs"}


async def test_a_granted_record_reads_the_row_only_through_a_registered_door(
    _post_door: list[tuple[str, frozenset[str]]],
) -> None:
    class _Db:
        async def get_file_async(self, fid: str) -> dict[str, Any]:
            return {"id": fid}

    class _GrantFm:
        class sync_engine:  # noqa: N801
            db = _Db()

    assert await gated_reads.read_granted_record(_GrantFm(), "f-theirs", parent_grant="test_post:p-1") == {"id": "f-theirs"}
    assert await gated_reads.read_granted_record(_GrantFm(), "f-mine", parent_grant="test_post:p-1") is None
    with pytest.raises(gated_reads.FileReadDenied):
        await gated_reads.read_granted_record(_GrantFm(), "f-theirs", parent_grant="social_post:p-1")


def _as_folder_user(monkeypatch: pytest.MonkeyPatch, readable: set[str]) -> None:
    async def checker(uid: str, rtype: str, rid: str, level: str) -> bool:
        return uid == "u-1" and rtype == "folder" and rid in readable

    monkeypatch.setattr(gated_reads, "_ambient_user_id", lambda: "u-1")
    monkeypatch.setattr(permissions, "_access_checker", checker)


async def test_folder_read_with_no_user_and_no_declared_job_is_refused() -> None:
    with pytest.raises(PermissionError):
        await gated_reads.read_folder_rows(["folder_name"], parent_id=None)


async def test_folder_read_denies_a_user_without_access(monkeypatch: pytest.MonkeyPatch) -> None:
    _as_folder_user(monkeypatch, set())
    assert await gated_reads.read_folder_rows(["folder_name"], parent_id=None) == []


async def test_folder_read_allows_only_the_folders_the_checker_clears(monkeypatch: pytest.MonkeyPatch) -> None:
    _as_folder_user(monkeypatch, {"d-mine"})
    rows = await gated_reads.read_folder_rows(["folder_name"], live_only=True, parent_id=None)
    assert [r["id"] for r in rows] == ["d-mine"]


async def test_folder_read_for_a_declared_job_reads_every_live_folder() -> None:
    with system_file_access("test-job"):
        rows = await gated_reads.read_folder_rows(["folder_name"], live_only=True, parent_id=None)
    assert sorted(r["id"] for r in rows) == ["d-mine", "d-theirs"]


async def test_folder_scan_needs_a_filter() -> None:
    with system_file_access("test-job"), pytest.raises(ValueError):
        await gated_reads.read_folder_rows(["folder_name"])


async def test_where_expression_narrows_rows_and_the_gate_still_decides(monkeypatch: pytest.MonkeyPatch) -> None:
    only_pdfs_named_m = lambda row: row["file_name"].startswith("m")  # noqa: E731
    with pytest.raises(PermissionError):
        await gated_reads.read_file_rows(["file_name"], where=only_pdfs_named_m)
    with system_file_access("test-job"):
        rows = await gated_reads.read_file_rows(["file_name"], where=only_pdfs_named_m)
    assert [r["id"] for r in rows] == ["f-mine"]
    _as_user(monkeypatch, set())
    assert await gated_reads.read_file_rows(["file_name"], where=only_pdfs_named_m) == []


_SCANS = [
    {"id": "s-a", "file_name": "a", "organization_id": "org-1", "file_pathway": "scan", "deleted_at": None},
    {"id": "s-b", "file_name": "b", "organization_id": "org-2", "file_pathway": "scan", "deleted_at": None},
    {"id": "s-x", "file_name": "x", "organization_id": "org-2", "file_pathway": "scan", "deleted_at": None},
]


async def test_pathway_read_spans_organizations_but_only_what_access_clears(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matrx_orm

    monkeypatch.setattr(models_files, "Files", _Model(_SCANS))

    async def many(uid: str, kind: str, ids: list[str], level: str, **_: Any) -> dict[str, bool]:
        assert (uid, kind) == ("u1", "file")
        return {i: i != "s-x" for i in ids}

    monkeypatch.setattr(matrx_orm, "platform_access_many", many)
    got = await gated_reads.read_pathway_file_rows_readable("scan", ("file_name",), user_id="u1")
    assert set(got) == {"s-a", "s-b"}  # both organizations, minus the row access refuses
    narrowed = await gated_reads.read_pathway_file_rows_readable(
        "scan", ("file_name",), user_id="u1", organization_id="org-2"
    )
    assert set(narrowed) == {"s-b"}  # the explicit organization only narrows


async def test_pathway_read_with_no_user_and_no_declared_job_is_refused() -> None:
    with pytest.raises(gated_reads.FileReadDenied):
        await gated_reads.read_pathway_file_rows_readable("scan", ("file_name",))
