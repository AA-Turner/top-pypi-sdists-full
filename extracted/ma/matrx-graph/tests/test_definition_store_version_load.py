from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from matrx_graph.db.definition_store import DefinitionStore
from matrx_graph.errors import DefinitionError


DEFINITION_ID = "11111111-1111-4111-8111-111111111111"
VERSION_ID = "22222222-2222-4222-8222-222222222222"


class _Query:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    async def values(self) -> list[dict[str, Any]]:
        return self.rows


class _VersionModel:
    filters: dict[str, Any] = {}

    @classmethod
    def filter(cls, **filters: Any) -> _Query:
        cls.filters = filters
        return _Query(
            [
                {
                    "id": VERSION_ID,
                    "definition_id": DEFINITION_ID,
                    "version_number": 7,
                    "name": "Pinned",
                    "description": None,
                    "nodes": [],
                    "edges": [],
                    "viewport": {"x": 0, "y": 0, "zoom": 1},
                    "channels": [],
                    "strict_channels": False,
                    "entry_nodes": [],
                    "variables": [],
                    "metadata": {},
                    "tags": [],
                    "category": None,
                    "is_active": True,
                    "change_note": "test",
                    "changed_at": datetime.now(UTC),
                }
            ]
        )


@pytest.mark.asyncio
async def test_load_version_by_snapshot_id_keeps_definition_scope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_graph.db import definition_store

    monkeypatch.setattr(definition_store, "get_model", lambda name: _VersionModel)

    row = await DefinitionStore().load(
        DEFINITION_ID,
        is_version=True,
        version_id=VERSION_ID,
    )

    assert row is not None
    assert row.id == VERSION_ID
    assert row.definition_id == DEFINITION_ID
    assert _VersionModel.filters == {
        "definition_id": DEFINITION_ID,
        "id": VERSION_ID,
    }


@pytest.mark.asyncio
async def test_load_version_requires_an_exact_snapshot_selector() -> None:
    with pytest.raises(DefinitionError, match="version_number or version_id"):
        await DefinitionStore().load(DEFINITION_ID, is_version=True)
