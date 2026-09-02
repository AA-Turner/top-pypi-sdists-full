from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from matrx_ai.tools.implementations.tool_component import (
    WORKFLOW_RENDER_SURFACE,
    toolcomp_get_context,
)
from matrx_ai.tools.models import ToolContext


class _FakeInstance:
    """Stand-in for a matrx-orm Model instance — exposes row values as
    attributes and a ``_fields`` mapping so ``_row_dict(instance)`` (which
    iterates ``instance._fields.keys()`` when no explicit field tuple is
    given) works exactly like it does against a real generated Model."""

    def __init__(self, data: dict[str, Any]):
        self._data = data
        self._fields = dict.fromkeys(data)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)


class _FakeQuery:
    def __init__(self, rows: list[dict[str, Any]]):
        self._rows = rows

    def filter(self, **kwargs: Any) -> _FakeQuery:
        filtered = [r for r in self._rows if all(r.get(k) == v for k, v in kwargs.items())]
        return _FakeQuery(filtered)

    def order_by(self, *_args: Any, **_kwargs: Any) -> _FakeQuery:
        return self

    def limit(self, n: int) -> _FakeQuery:
        return _FakeQuery(self._rows[:n])

    async def all(self) -> list[_FakeInstance]:
        return [_FakeInstance(r) for r in self._rows]


class _FakeModel:
    """Stand-in for a whole registered matrx-orm Model — enough of the
    surface (``filter().all()``/``get_or_none()``) for tool_component.py's
    read paths."""

    def __init__(self, rows: list[dict[str, Any]]):
        self._rows = rows

    def filter(self, **kwargs: Any) -> _FakeQuery:
        return _FakeQuery(self._rows).filter(**kwargs)

    async def get_or_none(self, **kwargs: Any) -> _FakeInstance | None:
        for r in self._rows:
            if all(r.get(k) == v for k, v in kwargs.items()):
                return _FakeInstance(r)
        return None


def _fake_get_db_model(tables: dict[str, list[dict[str, Any]]]):
    """Build a ``get_db_model(name)`` stand-in keyed by the same registry
    names tool_component.py resolves: ToolUi / ToolDefinition / ToolTestSample
    / ToolUiIncident. ``tables`` uses the old bare-table-name convention
    ("ui" / "definition" / "test_sample" / "ui_incident") for readability."""
    by_key = {
        "ToolUi": _FakeModel(tables.get("ui", [])),
        "ToolDefinition": _FakeModel(tables.get("definition", [])),
        "ToolTestSample": _FakeModel(tables.get("test_sample", [])),
        "ToolUiIncident": _FakeModel(tables.get("ui_incident", [])),
    }

    def _get(name: str) -> _FakeModel:
        return by_key[name]

    return _get


@pytest.mark.asyncio
async def test_get_context_workflow_component_by_name_and_surface() -> None:
    workflow_comp = {
        "id": "comp-wf-1",
        "tool_id": None,
        "tool_name": "my_workflow_panel",
        "surface_name": WORKFLOW_RENDER_SURFACE,
        "display_name": "My Panel",
        "inline_code": "export default function X() { return null; }",
        "overlay_code": None,
        "language": "tsx",
        "semver": "1.0.0",
        "version": 1,
        "is_active": True,
    }

    with patch(
        "matrx_ai.tools.implementations.tool_component.get_db_model",
        side_effect=_fake_get_db_model({"ui": [workflow_comp], "ui_incident": []}),
    ):
        result = await toolcomp_get_context(
            {
                "tool_name": "my_workflow_panel",
                "surface_name": WORKFLOW_RENDER_SURFACE,
            },
            ToolContext(call_id="c1", tool_name="toolcomp_get_context"),
        )

    assert result.success is True
    assert result.output is not None
    assert result.output.summary.is_workflow_component is True
    assert result.output.summary.tool_id is None
    assert result.output.component_ids == ["comp-wf-1"]
    assert result.output.tool.is_workflow_component is True


@pytest.mark.asyncio
async def test_get_context_workflow_fallback_when_no_tool_def() -> None:
    workflow_comp = {
        "id": "comp-wf-2",
        "tool_id": None,
        "tool_name": "orphan_panel",
        "surface_name": WORKFLOW_RENDER_SURFACE,
        "display_name": "Orphan",
        "inline_code": "code",
        "language": "tsx",
        "semver": "1.0.0",
        "version": 1,
        "is_active": True,
    }

    with patch(
        "matrx_ai.tools.implementations.tool_component.get_db_model",
        side_effect=_fake_get_db_model({"definition": [], "ui": [workflow_comp]}),
    ):
        result = await toolcomp_get_context(
            {"tool_name": "orphan_panel"},
            ToolContext(call_id="c2", tool_name="toolcomp_get_context"),
        )

    assert result.success is True
    assert result.output.summary.is_workflow_component is True
    assert result.output.component_ids == ["comp-wf-2"]


@pytest.mark.asyncio
async def test_get_context_by_component_id() -> None:
    workflow_comp = {
        "id": "comp-wf-3",
        "tool_id": None,
        "tool_name": "by_id_panel",
        "surface_name": WORKFLOW_RENDER_SURFACE,
        "display_name": "By ID",
        "inline_code": "code",
        "language": "tsx",
        "semver": "1.0.0",
        "version": 1,
        "is_active": True,
    }

    with patch(
        "matrx_ai.tools.implementations.tool_component.get_db_model",
        side_effect=_fake_get_db_model({"ui": [workflow_comp], "ui_incident": []}),
    ):
        result = await toolcomp_get_context(
            {"component_id": "comp-wf-3"},
            ToolContext(call_id="c3", tool_name="toolcomp_get_context"),
        )

    assert result.success is True
    assert result.output.component_ids == ["comp-wf-3"]
