from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from matrx_graph.db.definition_store import (
    _row_to_definition_row_or_skip,
)

ROW_ID = "33333333-3333-4333-8333-333333333333"


def _base_row(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "id": ROW_ID,
        "name": "List victim",
        "description": None,
        "nodes": nodes,
        "edges": [],
        "viewport": {"x": 0, "y": 0, "zoom": 1},
        "channels": [],
        "strict_channels": False,
        "entry_nodes": [],
        "variables": [],
        "metadata": {},
        "tags": [],
        "category": None,
        "version": 1,
        "is_active": True,
        "is_archived": False,
        "published_to_web": False,
        "is_favorite": False,
        "created_by": None,
        "organization_id": None,
        "project_id": None,
        "task_id": None,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }


def test_well_formed_row_parses() -> None:
    row = _base_row(
        [
            {
                "id": "a",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"spec_type": "data.transform", "config": {}, "input": {}},
            }
        ]
    )
    parsed = _row_to_definition_row_or_skip(row, is_version=False)
    assert parsed is not None
    assert parsed.id == ROW_ID


def test_malformed_row_is_skipped_not_raised() -> None:
    # The exact production incident: a probe row whose node lacked
    # `position` raised ValidationError inside the LIST path and 500'd the
    # entire /workflows catalog for every user. The list path must skip it.
    row = _base_row(
        [
            {
                "id": "agent",
                "type": "ai.agent.start",
                "data": {"spec_type": "ai.agent.start", "config": {}, "input": {}},
            }
        ]
    )
    assert _row_to_definition_row_or_skip(row, is_version=False) is None
