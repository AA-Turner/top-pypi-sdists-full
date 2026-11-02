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

    async def list_sync_changes_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(kwargs)
        return self.rows[: kwargs["limit"]]

    async def list_all_folders_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(kwargs)
        return self.folders


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
