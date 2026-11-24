"""A SAVE OF WHAT IS ALREADY SAVED WRITES NOTHING (P5 walk 2026-11-16).

Every draft write is a revision, so a save whose definition, name and description already match the stored
row must answer the current row and leave the version alone; a real edit still writes, and a stale token
still conflicts.
"""

from __future__ import annotations

import copy
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.db._registry import configure_db
from matrx_graph.db.definition_store import DefinitionStore
from matrx_graph.types.definition import Definition

WID = str(uuid4())


class _Result:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows_affected = len(rows)
        self.updated_rows = rows


class _Query:
    async def values(self, *_: str) -> list[dict[str, Any]]:
        return [copy.deepcopy(_Model.row)]


class _Model:
    row: dict[str, Any] = {}
    writes = 0

    @classmethod
    def filter(cls, **_: Any) -> _Query:
        return _Query()

    @classmethod
    async def update_where(cls, _f: dict[str, Any], *, expected_version: int | None = None, **updates: Any) -> _Result:
        cls.writes += 1
        new = {**cls.row, **{k: v for k, v in updates.items() if k not in ("version",)}}
        new["version"] = cls.row["version"] + 1
        cls.row = new
        return _Result([copy.deepcopy(new)])


def _row() -> dict[str, Any]:
    return {
        "id": uuid4(), "name": "Month-end close", "description": None, "nodes": [], "edges": [],
        "viewport": {"x": 0, "y": 0, "zoom": 1}, "channels": [], "strict_channels": False,
        "entry_nodes": [], "variables": [], "metadata": {}, "version": 5, "is_active": True,
        "is_archived": False, "published_to_web": False, "is_favorite": False, "tags": [],
        "category": None, "created_by": None, "organization_id": None, "project_id": None,
        "task_id": None, "input_kind": None, "output_kind": None, "created_at": None, "updated_at": None,
    }


@pytest.fixture
def store() -> DefinitionStore:
    configure_db(models={"WfDefinition": _Model})
    _Model.row = _row()
    _Model.writes = 0
    return DefinitionStore()


@pytest.mark.asyncio
async def test_an_identical_save_writes_nothing_and_answers_the_current_version(store: DefinitionStore) -> None:
    row = await store.save_draft(WID, definition=Definition(nodes=[], edges=[]), name="Month-end close")
    assert _Model.writes == 0
    assert row.version == 5


@pytest.mark.asyncio
async def test_a_real_edit_still_writes(store: DefinitionStore) -> None:
    row = await store.save_draft(WID, definition=Definition(nodes=[], edges=[]), name="Month-end close v2")
    assert _Model.writes == 1
    assert row.version == 6


@pytest.mark.asyncio
async def test_a_stale_token_is_not_swallowed_by_the_no_op(store: DefinitionStore) -> None:
    await store.save_draft(WID, definition=Definition(nodes=[], edges=[]), name="Month-end close", expected_version=4)
    # identical content, stale token: the write path (and its conflict check) must still run
    assert _Model.writes == 1
