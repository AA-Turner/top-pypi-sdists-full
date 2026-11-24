"""A whole-tree folder or file list never converts its rows ON the event loop.

``GET /files/folders`` for a person with 67,000 folders spent ~5 s in ``to_dict()``
on the loop (event_loop_stall, 2026-11-02): the whole API froze. Big lists convert
in a worker thread and keep exactly the shape ``_rows`` produced.
"""

from __future__ import annotations

import threading
from typing import Any

import pytest

from matrx_files.cloud_sync import db as cloud_db


class _Row:
    def __init__(self, i: int, seen: list[str]) -> None:
        self._i = i
        self._seen = seen

    def to_dict(self) -> dict[str, Any]:
        self._seen.append(threading.current_thread().name)
        return {"id": f"f{self._i}", "created_by": "u1", "folder_path": f"p/{self._i}"}


class _Query:
    def __init__(self, rows: list[_Row]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Query:
        return self

    def order_by(self, *_a: Any) -> _Query:
        return self

    async def all(self) -> list[_Row]:
        return self._rows


class _Model:
    def __init__(self, rows: list[_Row]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Query:
        return _Query(self._rows)


def _client(monkeypatch: pytest.MonkeyPatch, n: int) -> tuple[cloud_db.DatabaseClient, list[str]]:
    seen: list[str] = []
    rows = [_Row(i, seen) for i in range(n)]

    class _MF:
        Folders = _Model(rows)
        Files = _Model(rows)

    monkeypatch.setattr(cloud_db, "_models", lambda: (_MF, None))
    return cloud_db.DatabaseClient.__new__(cloud_db.DatabaseClient), seen


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["list_folders_async", "list_files_async"])
async def test_a_big_list_converts_off_the_loop(monkeypatch: pytest.MonkeyPatch, method: str) -> None:
    client, seen = _client(monkeypatch, 500)
    loop_thread = threading.current_thread().name
    out = await getattr(client, method)("u1")
    assert len(out) == 500
    assert loop_thread not in set(seen), "to_dict ran on the event loop thread"
    assert out[0] == {"id": "f0", "created_by": "u1", "folder_path": "p/0", "owner_id": "u1"}


@pytest.mark.asyncio
async def test_a_small_list_stays_inline(monkeypatch: pytest.MonkeyPatch) -> None:
    client, seen = _client(monkeypatch, 3)
    out = await client.list_folders_async("u1")
    assert [r["id"] for r in out] == ["f0", "f1", "f2"]
    assert set(seen) == {threading.current_thread().name}
