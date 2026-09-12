"""ToolRegistry.reload_from_database — the resolved registry after a DB change.

SUT: ``ToolRegistry.reload_from_database`` (and the real ``load_from_database``
→ ``_load_rows`` → ``_row_to_definition`` / ``_index_bindings`` chain it drives).
The only double is the external row source — the host ``tool_source`` seam the
registry reads BEFORE the ORM — serving ``tool.definition`` / ``tool.binding``
row shapes. Every assertion reads the registry's own resolved state.

Breaks each test names:
* a removed tool must disappear (a merge instead of a swap keeps it callable);
* a changed definition must take effect (a merge that prefers the old entry,
  or a stale id index, serves yesterday's schema);
* executor bindings must be replaced (a stale binding map routes a tool to an
  executor the DB no longer names);
* the previous snapshot keeps serving until the swap (clear-then-load exposes
  an empty registry to concurrent requests).
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

import matrx_ai.tools.registry as registry_module
from matrx_ai._ext import configure_ext
from matrx_ai.tools.registry import ToolRegistry

_KEEP_ID = "0d6f1c52-8f3e-4f0e-9a0b-2b4c7c1e5a11"
_REMOVED_ID = "7a2e9d40-3c1b-4b8e-8f6d-5e0a1c9b2d33"


def _row(tool_id: str, name: str, description: str, parameters: dict[str, Any]) -> dict[str, Any]:
    """A ``tool.definition`` row as the host source serves it."""
    return {
        "id": tool_id,
        "name": name,
        "description": description,
        "source_kind": "agent_authored",
        "parameters": parameters,
        "annotations": None,
        "is_active": True,
    }


_V1_KEEP = _row(
    _KEEP_ID,
    "lookup_order",
    "Look up an order by number.",
    {
        "type": "object",
        "properties": {"order_number": {"type": "string"}},
        "required": ["order_number"],
    },
)
_V1_REMOVED = _row(
    _REMOVED_ID,
    "legacy_refund",
    "Issue a refund (retired).",
    {"type": "object", "properties": {"amount": {"type": "number"}}},
)
_V2_KEEP = _row(
    _KEEP_ID,
    "lookup_order",
    "Look up an order by number and region.",
    {
        "type": "object",
        "properties": {
            "order_number": {"type": "string"},
            "region": {"type": "string"},
        },
        "required": ["order_number", "region"],
    },
)


class _VersionedSource:
    """External row source whose served snapshot the test flips between loads."""

    def __init__(
        self,
        tools: list[dict[str, Any]],
        bindings: list[dict[str, Any]] | None = None,
    ) -> None:
        self.tools = tools
        self.bindings = bindings or []
        self.gate: asyncio.Event | None = None
        self.entered = asyncio.Event()

    async def list_tools(self) -> list[dict[str, Any]]:
        self.entered.set()
        if self.gate is not None:
            await self.gate.wait()
        return [dict(row) for row in self.tools]

    async def list_bindings(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.bindings]


async def _loaded_registry(source: _VersionedSource) -> ToolRegistry:
    configure_ext(tool_source=source)
    registry = ToolRegistry()  # never the process singleton
    assert await registry.load_from_database() == len(source.tools)
    return registry


@pytest.mark.asyncio
async def test_removed_tool_is_gone_by_name_and_by_id_after_reload() -> None:
    source = _VersionedSource([_V1_KEEP, _V1_REMOVED])
    registry = await _loaded_registry(source)
    assert registry.get("legacy_refund") is not None

    source.tools = [_V1_KEEP]
    loaded = await registry.reload_from_database()

    assert loaded == 1
    assert registry.get("legacy_refund") is None
    assert registry.get(_REMOVED_ID) is None
    assert registry.count == 1
    assert [t.name for t in registry.all_tools()] == ["lookup_order"]


@pytest.mark.asyncio
async def test_changed_definition_takes_effect_after_reload() -> None:
    source = _VersionedSource([_V1_KEEP])
    registry = await _loaded_registry(source)

    source.tools = [_V2_KEEP]
    await registry.reload_from_database()

    resolved = registry.get("lookup_order")
    assert resolved is not None
    assert resolved.description == "Look up an order by number and region."
    assert set(resolved.parameters) == {"order_number", "region"}
    assert resolved.required_params == ["order_number", "region"]
    # The id edge resolves to the NEW definition, not a cached object.
    assert registry.get(_KEEP_ID) is resolved


@pytest.mark.asyncio
async def test_renamed_tool_resolves_by_id_to_its_new_name_after_reload() -> None:
    source = _VersionedSource([_V1_KEEP])
    registry = await _loaded_registry(source)

    source.tools = [{**_V1_KEEP, "name": "find_order"}]
    await registry.reload_from_database()

    assert registry.get("lookup_order") is None
    by_id = registry.get(_KEEP_ID)
    assert by_id is not None
    assert by_id.name == "find_order"


@pytest.mark.asyncio
async def test_executor_bindings_are_replaced_not_accumulated_on_reload() -> None:
    source = _VersionedSource(
        [_V1_KEEP],
        bindings=[{"tool_id": _KEEP_ID, "executor_name": "aidream"}],
    )
    registry = await _loaded_registry(source)
    assert registry.bindings_for_tool("lookup_order") == {"aidream"}

    source.bindings = [{"tool_id": _KEEP_ID, "executor_name": "matrx-local"}]
    await registry.reload_from_database()

    assert registry.bindings_for_tool("lookup_order") == {"matrx-local"}


@pytest.mark.asyncio
async def test_previous_snapshot_keeps_serving_until_the_swap() -> None:
    source = _VersionedSource([_V1_KEEP, _V1_REMOVED])
    registry = await _loaded_registry(source)

    source.tools = [_V2_KEEP]
    source.gate = asyncio.Event()
    source.entered = asyncio.Event()
    reload_task = asyncio.create_task(registry.reload_from_database())
    try:
        await asyncio.wait_for(source.entered.wait(), timeout=5)

        # Mid-reload: the replacement rows are being fetched. Concurrent
        # requests must still see the complete previous snapshot.
        assert registry.count == 2
        assert registry.get("legacy_refund") is not None
        mid = registry.get("lookup_order")
        assert mid is not None
        assert mid.description == "Look up an order by number."
    finally:
        source.gate.set()
    await asyncio.wait_for(reload_task, timeout=5)

    assert registry.get("legacy_refund") is None
    swapped = registry.get("lookup_order")
    assert swapped is not None
    assert swapped.description == "Look up an order by number and region."


@pytest.mark.asyncio
async def test_orm_tool_serialization_is_off_the_event_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    """A large persisted schema must not freeze LISTEN-driven registry refreshes."""

    class _ToolRow:
        def to_dict(self) -> dict[str, str]:
            return {"name": "slow_schema"}

    class _Manager:
        async def filter_items(self, **_kwargs: object) -> list[_ToolRow]:
            return [_ToolRow()]

    entered_thread = asyncio.Event()
    release_thread = asyncio.Event()

    async def controlled_to_thread(
        func: object, /, *args: object, **kwargs: object
    ) -> object:
        entered_thread.set()
        await release_thread.wait()
        return func(*args, **kwargs)  # type: ignore[operator]

    monkeypatch.setattr(registry_module, "get_tool_def_manager", lambda: _Manager())
    monkeypatch.setattr(registry_module.asyncio, "to_thread", controlled_to_thread)

    fetch_task = asyncio.create_task(ToolRegistry._fetch_tools_async())
    await asyncio.wait_for(entered_thread.wait(), timeout=1)
    assert not fetch_task.done()
    release_thread.set()
    assert await fetch_task == [{"name": "slow_schema"}]
