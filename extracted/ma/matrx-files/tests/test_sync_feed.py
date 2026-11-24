"""Device-replica sync feed — /files/sync/changes + /files/sync/folders.

Pins the wire protocol the desktop file-sync engine (matrx-local) builds
against: keyset cursor (updated_at, id), tombstone-aware pagination, the
bootstrap→poll cursor flip, and the safe outbound field set (no storage_uri).

Bare-venv friendly: the FileService is stubbed, no DB required.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from matrx_files.api.router_files import (
    _decode_sync_cursor,
    _encode_sync_cursor,
    build_file_router,
)
from matrx_utils.source_guard import stable_source

T0 = datetime(2026, 7, 13, 12, 0, 0, tzinfo=UTC)
ORG_ID = "11111111-1111-1111-1111-111111111111"
ORIGIN_DEVICE = "22222222-2222-2222-2222-222222222222"


def _row(i: int, *, deleted: bool = False, ts: datetime | None = None) -> dict[str, Any]:
    return {
        "id": f"00000000-0000-0000-0000-{i:012d}",
        "file_path": f"Docs/file-{i}.txt",
        "file_name": f"file-{i}.txt",
        "mime_type": "text/plain",
        "size_bytes": 100 + i,
        "checksum": f"sha-{i}",
        "published_to_web": True,
        "shown_to": "my_team",
        "current_version": 1,
        "parent_folder_id": None,
        "created_at": T0,
        "updated_at": ts or (T0 + timedelta(seconds=i)),
        "deleted_at": (T0 + timedelta(seconds=i)) if deleted else None,
        # Feed v2 (SPEC-SERVER §2.3). organization_id is NOT optional on the
        # entry: v1 scoping stays on created_by, but every entry says which
        # organization the row belongs to so the engine stamps its own writes
        # explicitly instead of letting the database choose one.
        "origin_device_id": ORIGIN_DEVICE if i % 2 == 0 else None,
        "client_modified_at": (T0 - timedelta(minutes=i)) if i % 2 == 0 else None,
        "organization_id": ORG_ID,
    }


class _StubEngine:
    def __init__(self, rows: list[dict[str, Any]], folders: list[dict[str, Any]] | None = None):
        self.rows = rows
        self.folders = folders or []
        self.calls: list[dict[str, Any]] = []
        # Relocation-ledger marks: (entry, (feed_at, ledger_id)).
        self.moves: list[tuple[dict[str, Any], tuple[datetime, str]]] = []
        self.move_calls: list[dict[str, Any]] = []

    async def list_sync_changes_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(kwargs)
        return self.rows[: kwargs["limit"]]

    async def list_all_folders_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(kwargs)
        return self.folders

    async def list_sync_relocations_async(self, **kwargs: Any) -> tuple[list[dict[str, Any]], Any]:
        self.move_calls.append(kwargs)
        if not self.moves:
            return [], None
        page = self.moves[: kwargs["limit"]]
        return [{**r, "_move_pos": pos} for r, pos in page], page[-1][1]


def _client(engine: _StubEngine) -> TestClient:
    service = SimpleNamespace(file_manager=SimpleNamespace(sync_engine=engine))
    app = FastAPI()
    app.include_router(build_file_router(service))  # test-mode anonymous auth
    return TestClient(app)


def test_cursor_roundtrip() -> None:
    ts = datetime(2026, 7, 13, 8, 30, 15, 123456, tzinfo=UTC)
    cur = _encode_sync_cursor(ts, "abc-123", True)
    got_ts, got_id, got_d = _decode_sync_cursor(cur)
    assert (got_ts, got_id, got_d) == (ts, "abc-123", True)


@pytest.mark.parametrize("bad", ["", "!!!", "bm90LWpzb24", _encode_sync_cursor(T0, "x", False)[:-4] + "AAAA"])
def test_malformed_cursor_raises(bad: str) -> None:
    with pytest.raises(ValueError):
        _decode_sync_cursor(bad)


def test_malformed_cursor_is_a_400_on_the_wire() -> None:
    client = _client(_StubEngine([]))
    resp = client.get("/files/sync/changes", params={"cursor": "not-a-cursor"})
    assert resp.status_code == 400


def test_bootstrap_is_alive_only_and_flips_tombstone_aware_when_drained() -> None:
    engine = _StubEngine([_row(1), _row(2)])
    client = _client(engine)
    resp = client.get("/files/sync/changes")
    assert resp.status_code == 200
    body = resp.json()
    assert [f["file_id"] for f in body["files"]] == [_row(1)["id"], _row(2)["id"]]
    assert body["has_more"] is False
    # Bootstrap queries exclude tombstones…
    assert engine.calls[0]["include_deleted"] is False
    assert engine.calls[0]["cursor_ts"] is None
    # …but the drained cursor is tombstone-aware for all future polls.
    _, _, d = _decode_sync_cursor(body["next_cursor"])
    assert d is True


def test_mid_bootstrap_page_keeps_alive_only_cursor() -> None:
    engine = _StubEngine([_row(i) for i in range(1, 4)])
    client = _client(engine)
    resp = client.get("/files/sync/changes", params={"limit": 3})
    body = resp.json()
    assert body["has_more"] is True
    ts, row_id, d = _decode_sync_cursor(body["next_cursor"])
    assert d is False  # bootstrap not drained yet
    assert row_id == _row(3)["id"]
    assert ts == _row(3)["updated_at"]


def test_cursor_page_passes_composite_keyset_to_engine() -> None:
    engine = _StubEngine([])
    client = _client(engine)
    cur = _encode_sync_cursor(T0, "row-9", True)
    resp = client.get("/files/sync/changes", params={"cursor": cur})
    body = resp.json()
    call = engine.calls[0]
    assert call["cursor_ts"] == T0
    assert call["cursor_id"] == "row-9"
    assert call["include_deleted"] is True
    # Empty page: the client keeps its position.
    assert body["next_cursor"] == cur
    assert body["has_more"] is False


def test_since_entry_point_is_tombstone_aware() -> None:
    engine = _StubEngine([_row(5, deleted=True)])
    client = _client(engine)
    resp = client.get("/files/sync/changes", params={"since": T0.isoformat()})
    body = resp.json()
    assert engine.calls[0]["include_deleted"] is True
    entry = body["files"][0]
    assert entry["deleted_at"] is not None  # tombstone visible on the wire


def test_empty_bootstrap_still_returns_a_usable_cursor() -> None:
    client = _client(_StubEngine([]))
    body = client.get("/files/sync/changes").json()
    ts, row_id, d = _decode_sync_cursor(body["next_cursor"])
    assert ts.year == 1970 and row_id == "" and d is True


def test_no_server_only_fields_on_the_wire() -> None:
    row = _row(1)
    row["storage_uri"] = "s3://bucket/secret"  # must never surface
    client = _client(_StubEngine([row]))
    body = client.get("/files/sync/changes").json()
    assert "storage_uri" not in body["files"][0]


def test_sync_feed_preserves_both_row_access_words_and_the_transition_echo() -> None:
    """T-13 adds access words without taking the retiring level word away."""
    body = _client(_StubEngine([_row(1)])).get("/files/sync/changes").json()
    entry = body["files"][0]
    assert (entry["published_to_web"], entry["shown_to"]) == (True, "my_team")
    assert entry["visibility"] == "public"


def test_sync_folders_maps_rows() -> None:
    folders = [
        {
            "id": "11111111-0000-0000-0000-000000000001",
            "folder_path": "Docs",
            "folder_name": "Docs",
            "parent_id": None,
            "published_to_web": False,
            "shown_to": "only_me",
            "is_system": False,
            "created_at": T0,
            "updated_at": T0,
            "deleted_at": None,
        }
    ]
    client = _client(_StubEngine([], folders=folders))
    resp = client.get("/files/sync/folders")
    assert resp.status_code == 200
    body = resp.json()
    assert body["folders"][0]["folder_path"] == "Docs"
    assert body["folders"][0]["is_system"] is False
    assert body["folders"][0]["published_to_web"] is False
    assert body["folders"][0]["shown_to"] == "only_me"
    assert body["folders"][0]["visibility"] == "personal"


def test_sync_routes_not_captured_by_file_id_param() -> None:
    """/files/sync/changes must never resolve as GET /files/{file_id}."""
    engine = _StubEngine([])
    client = _client(engine)
    resp = client.get("/files/sync/changes")
    assert resp.status_code == 200
    assert "files" in resp.json()


def test_feed_entries_carry_device_provenance_and_the_organization() -> None:
    """Feed v2 (SPEC-SERVER §2.3) — three added fields, nothing removed.

    `origin_device_id` is what lets a daemon recognize its own echo instead of
    re-downloading a file it just uploaded; NULL means "not written by a
    registered device" (a browser upload), which the daemon treats as "not mine".
    `organization_id` is REQUIRED so the engine can stamp its writes explicitly --
    the database never chooses, inherits or defaults an organization.
    """
    engine = _StubEngine([_row(0), _row(1)])
    body = _client(engine).get("/files/sync/changes", params={"limit": 10}).json()
    first, second = body["files"]

    assert first["organization_id"] == ORG_ID
    assert second["organization_id"] == ORG_ID
    assert first["origin_device_id"] == ORIGIN_DEVICE
    assert second["origin_device_id"] is None, "a browser upload has no device"
    assert first["client_modified_at"].startswith("2026-07-13T12:00:00")
    assert second["client_modified_at"] is None

    # Nothing from v1 was removed.
    for key in ("file_id", "file_path", "file_name", "checksum", "version", "deleted_at"):
        assert key in first


def test_an_entry_without_an_organization_is_a_loud_failure() -> None:
    """A row that reached the feed with no organization is a data defect.

    Serving it as null would push the "pick an organization" decision onto the
    client, which is exactly what the no-db-assigned-org ruling forbids.
    """
    row = _row(0)
    del row["organization_id"]
    with pytest.raises(KeyError):
        _client(_StubEngine([row])).get("/files/sync/changes")


def test_folder_feed_and_file_feed_use_one_path_rule():
    """/files/sync/folders and /files/sync/changes leave out the same roots (.matrx-tmp/ included).

    Red before (2026-10-30): the folder feed used files.is_user_visible_folder_path, which keeps
    .matrx-tmp folders, so devices received hidden staging folders the file feed never filled.
    """

    from matrx_files.cloud_sync import db as cdb
    from matrx_files.user_visible import PATH_PREDICATE_FUNCTION

    src = stable_source(cdb.CloudDb.list_all_folders_async) if hasattr(cdb, "CloudDb") else stable_source(cdb)
    body = src[src.index("async def list_all_folders_async"):]
    body = body[: body.index("async def ", 10)]
    assert "PATH_PREDICATE_FUNCTION" in body and "FOLDER_PREDICATE_FUNCTION" not in body
    assert PATH_PREDICATE_FUNCTION == "files.is_user_visible_path"


# ---------------------------------------------------------------------------
# Source 2 — the relocation ledger (placement registry § 7, attack finding 3).
# The mover keeps updated_at, so a moved row never re-enters the (updated_at, id)
# keyset; the ledger marks deliver it (or its tombstone) once, after the cursor.
# ---------------------------------------------------------------------------

from matrx_files.api.router_files import _decode_sync_cursor_moves  # noqa: E402

MOVED_AT = T0 + timedelta(days=30)


def _moved(i: int, *, left: bool) -> dict[str, Any]:
    row = _row(i, ts=T0 - timedelta(days=200))  # an OLD updated_at the keyset passed long ago
    row["file_path"] = f"Images/Generated/img-{i}.png"
    if left:
        row["deleted_at"] = MOVED_AT  # the db layer marks a row that left the visible set
    return row


def test_a_moved_row_with_an_old_date_reaches_a_device_past_that_date() -> None:
    engine = _StubEngine([])
    engine.moves = [(_moved(7, left=False), (MOVED_AT, "ledger-7"))]
    client = _client(engine)
    cur = _encode_sync_cursor(T0, "row-9", True)  # a v1 cursor already far past the row's updated_at
    body = client.get("/files/sync/changes", params={"cursor": cur}).json()
    assert [f["file_id"] for f in body["files"]] == [_row(7)["id"]]
    assert body["files"][0]["file_path"] == "Images/Generated/img-7.png"
    assert body["files"][0]["deleted_at"] is None
    # the person's date is unchanged on the wire
    assert body["files"][0]["updated_at"].startswith((T0 - timedelta(days=200)).date().isoformat())
    # a pre-ledger cursor replays the ledger from the start…
    assert engine.move_calls[0]["after_ts"] is None
    # …and the next cursor carries the ledger position; the main keyset is untouched
    assert _decode_sync_cursor_moves(body["next_cursor"]) == (MOVED_AT, "ledger-7")
    assert _decode_sync_cursor(body["next_cursor"])[:2] == (T0, "row-9")


def test_a_row_that_left_the_visible_set_arrives_as_a_tombstone() -> None:
    engine = _StubEngine([])
    engine.moves = [(_moved(8, left=True), (MOVED_AT, "ledger-8"))]
    body = _client(engine).get(
        "/files/sync/changes", params={"cursor": _encode_sync_cursor(T0, "x", True)}
    ).json()
    assert body["files"][0]["deleted_at"] is not None


def test_the_ledger_position_is_passed_back_on_the_next_poll() -> None:
    engine = _StubEngine([])
    cur = _encode_sync_cursor(T0, "row-9", True, (MOVED_AT, "ledger-7"))
    body = _client(engine).get("/files/sync/changes", params={"cursor": cur}).json()
    assert engine.move_calls[0]["after_ts"] == MOVED_AT
    assert engine.move_calls[0]["after_id"] == "ledger-7"
    assert body["next_cursor"] == cur  # nothing new: position kept exactly


def test_bootstrap_never_serves_marks_but_anchors_the_ledger_position() -> None:
    engine = _StubEngine([_row(1)])
    engine.moves = [(_moved(7, left=False), (MOVED_AT, "ledger-7"))]
    body = _client(engine).get("/files/sync/changes").json()
    assert engine.move_calls == []  # alive-only bootstrap reads current state
    pos = _decode_sync_cursor_moves(body["next_cursor"])
    assert pos is not None and pos[0] > T0  # moves during the bootstrap arrive after it


def test_marks_and_keyset_rows_share_one_page_in_time_order() -> None:
    """The page is the merge of both sources by time; each cursor half moves only past what
    the page emitted (the first version served every mark first: review defect 1)."""
    engine = _StubEngine([_row(1), _row(2)])
    engine.moves = [(_moved(i, left=False), (MOVED_AT, f"ledger-{i}")) for i in range(10, 13)]
    cur = _encode_sync_cursor(T0, "row-0", True)
    body = _client(engine).get("/files/sync/changes", params={"cursor": cur, "limit": 3}).json()
    assert [f["file_id"] for f in body["files"]] == [_row(1)["id"], _row(2)["id"], _row(10)["id"]]
    assert body["has_more"] is True
    assert _decode_sync_cursor(body["next_cursor"])[:2] == (_row(2)["updated_at"], _row(2)["id"])
    assert _decode_sync_cursor_moves(body["next_cursor"]) == (MOVED_AT, "ledger-10")


def test_a_tombstone_is_served_before_a_later_move_onto_its_path() -> None:
    """Asleep: X at a path deleted (tombstone at t1), then Y moved onto that path (mark at t2).
    A device must see X leave before Y arrives, or it turns X into a conflict copy and then
    deletes Y by path."""
    x_gone = _row(3, deleted=True, ts=MOVED_AT - timedelta(minutes=5))
    x_gone["file_path"] = "Docs/report.txt"
    y = _moved(4, left=False)
    y["file_path"] = "Docs/report.txt"
    y["_move_pos"] = (MOVED_AT, "ledger-4")
    engine = _StubEngine([x_gone])
    engine.moves = [(y, (MOVED_AT, "ledger-4"))]
    body = _client(engine).get(
        "/files/sync/changes", params={"cursor": _encode_sync_cursor(T0, "row-0", True)}
    ).json()
    assert [(f["file_id"], f["deleted_at"] is not None) for f in body["files"]] == [
        (_row(3)["id"], True), (_row(4)["id"], False)]
    assert all("_move_pos" not in f for f in body["files"])

