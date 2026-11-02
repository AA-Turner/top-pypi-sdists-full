"""DefinitionStore.set_tags — tags change alone, the change carries its author, a missing row is None."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_graph.db._registry import configure_db
from matrx_graph.db.definition_store import DefinitionStore

AUTHOR_ID = "87a6e699-3622-4869-8843-d0867456c0dd"


class _Result:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows_affected = len(rows)
        self.updated_rows = rows


class _Model:
    captured: dict[str, Any] = {}
    match = True

    @classmethod
    async def update_where(cls, _filters: dict[str, Any], **updates: Any) -> _Result:
        cls.captured = dict(updates)
        if not cls.match:
            return _Result([])
        return _Result([{
            "id": uuid4(), "name": "Unit", "description": None, "nodes": [], "edges": [],
            "viewport": {"x": 0, "y": 0, "zoom": 1}, "channels": [], "strict_channels": False,
            "entry_nodes": [], "variables": [], "metadata": {}, "version": 3, "is_active": True,
            "is_archived": False, "published_to_web": False, "is_favorite": False,
            "tags": updates["tags"], "category": None, "created_by": UUID(AUTHOR_ID),
            "organization_id": None, "project_id": None, "task_id": None, "input_kind": None,
            "output_kind": None, "created_at": None, "updated_at": None,
        }])


@pytest.fixture
def store() -> DefinitionStore:
    configure_db(models={"WfDefinition": _Model})
    _Model.captured, _Model.match = {}, True
    return DefinitionStore()


@pytest.mark.asyncio
async def test_set_tags_writes_only_tags_version_and_author(store: DefinitionStore) -> None:
    row = await store.set_tags(str(uuid4()), ["platform:brand_discovery"], user_id=AUTHOR_ID)
    assert row is not None and row.tags == ["platform:brand_discovery"]
    assert set(_Model.captured) == {"tags", "version", "updated_by"}  # never the graph


@pytest.mark.asyncio
async def test_set_tags_without_an_author_does_not_blank_one(store: DefinitionStore) -> None:
    await store.set_tags(str(uuid4()), [], user_id="admin")
    assert "updated_by" not in _Model.captured


@pytest.mark.asyncio
async def test_set_tags_on_a_missing_workflow_is_none(store: DefinitionStore) -> None:
    _Model.match = False
    assert await store.set_tags(str(uuid4()), ["a"]) is None
