"""A tool registered at runtime survives a registry reload.

Live 2026-11-02 (Company Setup): the Action tool door registers an agent's declared Actions
(``org_section_place`` and eleven more) as runtime ``ToolDefinition``s — they have no tool row.
A tool-row NOTIFY made every process ``reload_from_database``, which swapped in a registry built
from rows only: mid-run the model was told "12 requested tool(s) not found in registry", and its
next call failed "Tool 'org_section_place' is not registered".
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry

pytestmark = pytest.mark.asyncio

_ROW: dict[str, Any] = {
    "id": "0d6f1c52-8f3e-4f0e-9a0b-2b4c7c1e5a11",
    "name": "lookup_order",
    "description": "Look up an order by number.",
    "source_kind": "agent_authored",
    "parameters": {"type": "object", "properties": {"order_number": {"type": "string"}}},
    "annotations": None,
    "is_active": True,
}


def _rows(monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]]) -> None:
    async def _fetch() -> list[dict[str, Any]]:
        return [dict(r) for r in rows]

    async def _noop(self: ToolRegistry) -> None:
        return None

    monkeypatch.setattr(ToolRegistry, "_resolve_tool_source", staticmethod(lambda: None))
    monkeypatch.setattr(ToolRegistry, "_fetch_tools_async", staticmethod(_fetch))
    monkeypatch.setattr(ToolRegistry, "_load_bindings_async", _noop)
    monkeypatch.setattr(ToolRegistry, "_load_executors_async", _noop)


def _action_tool(name: str) -> ToolDefinition:
    return ToolDefinition(name=name, description="an Action", parameters={}, tool_type=ToolType.LOCAL,
                          function_path=f"host.action_tool_door[{name}]", category="actions")


async def test_a_registered_tool_is_still_offered_after_a_reload(monkeypatch: pytest.MonkeyPatch) -> None:
    _rows(monkeypatch, [_ROW])
    registry = ToolRegistry()
    await registry.load_from_database()
    registry.register(_action_tool("org_section_place"))
    await registry.reload_from_database()
    assert registry.get("org_section_place") is not None, "a reload erased a runtime-registered tool"
    assert [t["name"] for t in registry.get_provider_tools(["org_section_place"], "anthropic")] == [
        "org_section_place"]
    # ...and survives the NEXT reload too.
    await registry.reload_from_database()
    assert registry.get("org_section_place") is not None


async def test_a_row_of_the_same_name_wins_over_the_runtime_copy(monkeypatch: pytest.MonkeyPatch) -> None:
    _rows(monkeypatch, [_ROW])
    registry = ToolRegistry()
    await registry.load_from_database()
    registry.register(_action_tool("lookup_order"))
    await registry.reload_from_database()
    assert registry.get("lookup_order").description == "Look up an order by number."


async def test_clear_still_wipes_everything(monkeypatch: pytest.MonkeyPatch) -> None:
    _rows(monkeypatch, [])
    registry = ToolRegistry()
    registry.register(_action_tool("org_section_place"))
    registry.clear()
    await registry.load_from_database()
    assert registry.get("org_section_place") is None
