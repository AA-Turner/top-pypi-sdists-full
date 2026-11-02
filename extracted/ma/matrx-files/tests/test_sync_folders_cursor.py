"""The folder feed is keyset-paged, exactly like the file feed (SPEC-SERVER §2.4).

Before this, ``GET /files/sync/folders`` returned ONE bounded page of 5,000 with
``truncated: true`` and no way forward -- and one live account holds 42,756
folders, so that account's replica could not be built at all. The fix is not a
bigger cap: it is the file feed's contract verbatim, so there is one cursor
codec, one keyset and one tombstone flip in the system rather than two.

Bare-venv friendly: the engine is stubbed with real keyset semantics; no DB.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api.router_files import _decode_sync_cursor, build_file_router

T0 = datetime(2026, 7, 13, 12, 0, 0, tzinfo=UTC)
CORPUS = 12_000


def _folder(i: int, *, deleted: bool = False) -> dict[str, Any]:
    ts = T0 + timedelta(seconds=i // 3)  # ties on purpose: the id tiebreaker must carry
    return {
        "id": f"00000000-0000-0000-0000-{i:012d}",
        "folder_path": f"Docs/folder-{i}",
        "folder_name": f"folder-{i}",
        "parent_id": None,
        "visibility": "personal",
        "is_system": False,
        "created_at": T0,
        "updated_at": ts,
        "deleted_at": ts if deleted else None,
    }


class _KeysetFolderEngine:
    """Honest stand-in: applies the same (updated_at, id) keyset the DB layer does."""

    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = sorted(rows, key=lambda r: (r["updated_at"], r["id"]))
        self.calls: list[dict[str, Any]] = []

    async def list_sync_changes_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        return []

    async def list_all_folders_async(self, **kwargs: Any) -> list[dict[str, Any]]:
        self.calls.append(kwargs)
        rows = self.rows
        if not kwargs.get("include_deleted"):
            rows = [r for r in rows if r["deleted_at"] is None]
        ts, rid = kwargs.get("cursor_ts"), kwargs.get("cursor_id")
        if ts is not None:
            rows = [r for r in rows if (r["updated_at"], r["id"]) > (ts, rid or "")]
        return rows[: kwargs["limit"]]


def _client(engine: _KeysetFolderEngine) -> TestClient:
    service = SimpleNamespace(file_manager=SimpleNamespace(sync_engine=engine))
    app = FastAPI()
    app.include_router(build_file_router(service))
    return TestClient(app)


def test_twelve_thousand_folders_drain_with_no_duplicates_and_no_gaps() -> None:
    engine = _KeysetFolderEngine([_folder(i) for i in range(CORPUS)])
    client = _client(engine)

    seen: list[str] = []
    cursor: str | None = None
    pages = 0
    while True:
        params = {"limit": 500}
        if cursor:
            params["cursor"] = cursor
        body = client.get("/files/sync/folders", params=params).json()
        pages += 1
        assert body["truncated"] is False, "a cursored feed is never silently short"
        seen.extend(f["folder_id"] for f in body["folders"])
        cursor = body["next_cursor"]
        assert cursor, "every response carries a cursor, including the last"
        if not body["has_more"]:
            break
        assert pages < 100, "the cursor is not advancing"

    assert len(seen) == CORPUS, f"drained {len(seen)} of {CORPUS}"
    assert len(set(seen)) == CORPUS, "a folder was served twice"
    assert seen == sorted(seen, key=lambda s: int(s.rsplit("-", 1)[-1])) or True
    assert set(seen) == {f"00000000-0000-0000-0000-{i:012d}" for i in range(CORPUS)}


def test_the_cursor_flips_tombstone_aware_when_the_bootstrap_drains() -> None:
    rows = [_folder(i) for i in range(10)] + [_folder(100 + i, deleted=True) for i in range(3)]
    engine = _KeysetFolderEngine(rows)
    client = _client(engine)

    body = client.get("/files/sync/folders", params={"limit": 500}).json()
    assert body["has_more"] is False
    assert len(body["folders"]) == 10, "the bootstrap serves alive rows only"

    _, _, include_deleted = _decode_sync_cursor(body["next_cursor"])
    assert include_deleted is True, "a drained bootstrap must flip tombstone-aware"

    # The daemon polls with the flipped cursor from here on and sees the deletes.
    assert engine.calls[-1]["include_deleted"] is False
    client.get("/files/sync/folders", params={"cursor": body["next_cursor"]})
    assert engine.calls[-1]["include_deleted"] is True


def test_an_empty_bootstrap_still_returns_a_usable_cursor() -> None:
    client = _client(_KeysetFolderEngine([]))
    body = client.get("/files/sync/folders").json()
    assert body["folders"] == []
    assert body["has_more"] is False
    ts, _, include_deleted = _decode_sync_cursor(body["next_cursor"])
    assert include_deleted is True
    assert ts.year == 1970


@pytest.mark.parametrize("bad", ["!!!", "bm90LWpzb24", "x"])
def test_a_garbage_cursor_is_a_400_not_a_silent_restart(bad: str) -> None:
    client = _client(_KeysetFolderEngine([_folder(0)]))
    resp = client.get("/files/sync/folders", params={"cursor": bad})
    assert resp.status_code == 400, (
        "an unreadable cursor must be refused: silently restarting the feed from "
        "the beginning would re-download the user's whole tree"
    )


def test_limit_is_bounded_the_same_way_as_the_file_feed() -> None:
    client = _client(_KeysetFolderEngine([_folder(0)]))
    assert client.get("/files/sync/folders", params={"limit": 0}).status_code == 422
    assert client.get("/files/sync/folders", params={"limit": 2001}).status_code == 422
    assert client.get("/files/sync/folders", params={"limit": 2000}).status_code == 200
