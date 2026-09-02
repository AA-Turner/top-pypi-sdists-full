from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.tools.registry import (
    TOOL_REGISTRY_DEFINITION_LOAD_FAILED_KIND,
    ToolRegistry,
)


def _row(**overrides: Any) -> dict[str, Any]:
    row = {
        "id": "tool-row-id",
        "name": "mcp.docs.searchDocumentation",
        "description": "Search docs",
        "source_kind": "mcp_discovered",
        "parameters": {"type": "object", "properties": {}},
        "is_active": True,
    }
    row.update(overrides)
    return row


def test_registry_accepts_mcp_tool_annotations_object() -> None:
    annotations = {
        "title": "Search documentation",
        "readOnlyHint": True,
        "destructiveHint": False,
    }

    definition = ToolRegistry._row_to_definition(_row(annotations=annotations))

    assert definition.annotations == [annotations]


def test_registry_preserves_legacy_annotation_list() -> None:
    annotations = [{"timeout_seconds": 30}, {"readOnlyHint": True}]

    definition = ToolRegistry._row_to_definition(_row(annotations=annotations))

    assert definition.annotations == annotations
    assert definition.timeout_seconds == 30


@pytest.mark.asyncio
async def test_rejected_registry_row_creates_structured_capture(monkeypatch) -> None:
    captures: list[dict[str, Any]] = []

    async def fake_capture_error(exc: BaseException, **fields: Any) -> None:
        captures.append({"exc": exc, **fields})

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    registry = ToolRegistry()

    assert registry._load_rows([_row(annotations="invalid")]) == 0
    await asyncio.sleep(0)

    assert len(captures) == 1
    capture = captures[0]
    assert capture["kind"] == TOOL_REGISTRY_DEFINITION_LOAD_FAILED_KIND
    assert capture["route"] == "tool_registry.load"
    assert capture["context"] == {
        "tool_name": "mcp.docs.searchDocumentation",
        "tool_id": "tool-row-id",
        "source_kind": "mcp_discovered",
    }
    assert "annotations" not in capture["context"]
