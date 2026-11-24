"""EVERY definition writer lands a metadata-declared kind in its COLUMN.

7ba8c0df6 lifted ``definition.metadata.input_kind`` / ``output_kind`` into the real
columns, but only inside aidream's authoring service. ~15 writers (mandate starters,
plan services, system workflows, seed scripts, feature writers) call
``DefinitionStore.create`` / ``save_draft`` directly, so their declaration stayed a
metadata copy and the Action registry (which reads the column) never saw it. The lift
now lives in the store: one home, every writer.
"""

from __future__ import annotations

import contextlib
from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_graph.db import definition_store as ds
from matrx_graph.db._registry import configure_db
from matrx_graph.db.definition_store import DefinitionStore
from matrx_graph.types.definition import Definition


def _row(**over: Any) -> dict[str, Any]:
    row = {
        "id": uuid4(), "name": "w", "description": None, "nodes": [], "edges": [],
        "viewport": {"x": 0, "y": 0, "zoom": 1}, "channels": [], "strict_channels": False,
        "entry_nodes": [], "variables": [], "metadata": {}, "version": 1, "is_active": True,
        "is_archived": False, "published_to_web": False, "is_favorite": False, "tags": [],
        "category": None, "created_by": UUID(int=1), "organization_id": None, "project_id": None,
        "task_id": None, "input_kind": None, "output_kind": None, "created_at": None, "updated_at": None,
    }
    row.update(over)
    return row


class _Result:
    rows_affected = 1

    def __init__(self, row: dict[str, Any]) -> None:
        self.updated_rows = [row]


class _NoRow:
    async def values(self, *_a: str) -> list[dict[str, Any]]:
        return []


class _Model:
    @classmethod
    def filter(cls, **_: Any) -> _NoRow:
        return _NoRow()

    captured: dict[str, Any] = {}

    @classmethod
    async def update_where(cls, _filters: dict[str, Any], *, expected_version: int | None = None, **updates: Any) -> _Result:
        cls.captured = dict(updates)
        return _Result(_row())

    @classmethod
    async def create(cls, **values: Any) -> dict[str, Any]:
        cls.captured = dict(values)
        return _row(**{k: v for k, v in values.items() if k in _row()})


@pytest.fixture
def store(monkeypatch: pytest.MonkeyPatch) -> DefinitionStore:
    configure_db(models={"WfDefinition": _Model})
    _Model.captured = {}
    monkeypatch.setattr(ds, "_instance_to_mapping", lambda inst: inst)

    async def _no_snapshot(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ds, "_insert_version_snapshot", _no_snapshot)
    import matrx_orm

    monkeypatch.setattr(matrx_orm, "transaction", contextlib.nullcontext)
    import matrx_orm.core.transaction as tx

    monkeypatch.setattr(tx, "get_active_connection", lambda: None)
    return DefinitionStore()


def _definition(metadata: dict[str, Any]) -> Definition:
    return Definition(nodes=[], edges=[], metadata=metadata)


@pytest.mark.asyncio
async def test_create_writes_a_metadata_output_kind_to_the_column(store: DefinitionStore) -> None:
    await store.create(name="w", definition=_definition({"output_kind": " generated_image_set ", "notes": "keep"}))
    assert _Model.captured["output_kind"] == "generated_image_set", "the declaration must reach the column"
    assert _Model.captured["metadata"] == {"notes": "keep"}, "metadata keeps no second copy"


@pytest.mark.asyncio
async def test_create_explicit_column_wins_and_blank_is_not_a_declaration(store: DefinitionStore) -> None:
    await store.create(
        name="w",
        definition=_definition({"output_kind": "other", "input_kind": "  "}),
        output_kind="generated_image_set",
    )
    assert _Model.captured["output_kind"] == "generated_image_set"
    assert _Model.captured["input_kind"] is None
    assert _Model.captured["metadata"] == {}


@pytest.mark.asyncio
async def test_save_draft_writes_a_metadata_output_kind_to_the_column(store: DefinitionStore) -> None:
    await store.save_draft(str(uuid4()), definition=_definition({"output_kind": "generated_image_set", "input_kind": 3}))
    assert _Model.captured["output_kind"] == "generated_image_set"
    assert "input_kind" not in _Model.captured, "a non-string metadata value is not a declaration and clears nothing"
    assert _Model.captured["metadata"] == {}


@pytest.mark.asyncio
async def test_save_draft_explicit_value_even_null_wins(store: DefinitionStore) -> None:
    await store.save_draft(str(uuid4()), definition=_definition({"output_kind": "other"}), output_kind=None)
    assert _Model.captured["output_kind"] is None, "an explicit clear wins over metadata"
    assert _Model.captured["metadata"] == {}


@pytest.mark.asyncio
async def test_no_declaration_touches_no_column(store: DefinitionStore) -> None:
    await store.save_draft(str(uuid4()), definition=_definition({"notes": "x"}))
    assert "output_kind" not in _Model.captured and "input_kind" not in _Model.captured
    assert _Model.captured["metadata"] == {"notes": "x"}
