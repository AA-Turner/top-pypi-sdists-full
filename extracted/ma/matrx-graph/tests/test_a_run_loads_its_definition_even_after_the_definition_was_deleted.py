"""A run that already exists keeps its graph when the definition is soft-deleted.

Live 2026-11-15: four runs failed ``worker: definition '<id>' not found`` because
their definition was soft-deleted between enqueue and claim. ``load`` (the live
reader) still hides deleted rows; ``include_deleted=True`` (the run reader) does not.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_graph.db import definition_store as ds


class _Query:
    def __init__(self, rows: list[dict[str, Any]], filters: dict[str, Any]) -> None:
        self._rows, self._filters = rows, filters

    async def values(self) -> list[dict[str, Any]]:
        out = self._rows
        if self._filters.get("deleted_at__isnull"):
            out = [r for r in out if r["deleted_at"] is None]
        return [r for r in out if r["id"] == self._filters["id"]]


class _Model:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **filters: Any) -> _Query:
        return _Query(self._rows, filters)


@pytest.mark.asyncio
async def test_deleted_definition_loads_only_for_a_run(monkeypatch: pytest.MonkeyPatch) -> None:
    def_id = str(uuid.uuid4())
    row = {"id": def_id, "deleted_at": "2026-11-15"}
    monkeypatch.setattr(ds, "get_model", lambda _n: _Model([row]))
    monkeypatch.setattr(ds, "_row_to_definition_row", lambda r, is_version: r)
    store = ds.DefinitionStore.__new__(ds.DefinitionStore)

    assert await store.load(def_id) is None
    assert await store.load(def_id, include_deleted=True) is row
