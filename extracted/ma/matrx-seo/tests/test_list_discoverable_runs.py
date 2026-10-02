"""A runs list asks the kernel ONCE which runs the person may enumerate, then intersects it with
the newest rows — never once per row (that was 10s for a 25-row page, 2026-09-25)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_seo import access


class _Query:
    def __init__(self, rows):
        self._rows, self._offset, self._limit = rows, 0, None

    def filter(self, **_):
        return self

    def order_by(self, *_):
        return self

    def offset(self, n):
        self._offset = n
        return self

    def limit(self, n):
        self._limit = n
        return self

    async def all(self):
        return self._rows[self._offset : self._offset + self._limit]


@pytest.fixture
def world(monkeypatch):
    rows = [SimpleNamespace(id=f"run-{i}") for i in range(200)]
    calls = {"discoverable": 0, "per_row": 0}

    async def discoverable(user_id, *, level="viewer"):
        calls["discoverable"] += 1
        return {f"run-{i}" for i in range(200) if i % 2 == 0}  # every other run is hers

    async def per_row(*_a, **_k):  # pragma: no cover - must never be called
        calls["per_row"] += 1
        return True

    import matrx_seo.db.models_seo as models

    monkeypatch.setattr(models, "CollectionRun", SimpleNamespace(filter=lambda **_: _Query(rows)))
    monkeypatch.setattr(access, "discoverable_collection_run_ids", discoverable)
    monkeypatch.setattr(access, "collection_run_discoverable", per_row)
    return calls


@pytest.mark.asyncio
async def test_one_set_check_and_only_discoverable_rows_and_a_full_page(world):
    rows, _ = await access.list_discoverable_runs("u1", limit=25)
    assert len(rows) == 25
    assert all(int(r.id.split("-")[1]) % 2 == 0 for r in rows), "a run she may not enumerate never appears"
    assert world["discoverable"] == 1 and world["per_row"] == 0


@pytest.mark.asyncio
async def test_nothing_discoverable_is_an_empty_page(world, monkeypatch):
    async def none(*_a, **_k):
        return set()

    monkeypatch.setattr(access, "discoverable_collection_run_ids", none)
    assert (await access.list_discoverable_runs("u1", limit=25))[0] == []


@pytest.mark.asyncio
async def test_receipt_callback_never_receives_undiscoverable_candidate_rows(world):
    received: list[str] = []

    async def receipts(rows):
        received.extend(str(row.id) for row in rows)
        return {str(row.id): "receipt" for row in rows}

    rows, extra = await access.list_discoverable_runs("u1", limit=6, while_waiting=receipts)

    assert [str(row.id) for row in rows] == ["run-0", "run-2", "run-4", "run-6", "run-8", "run-10"]
    assert received == [str(row.id) for row in rows]
    assert extra == {str(row.id): "receipt" for row in rows}
