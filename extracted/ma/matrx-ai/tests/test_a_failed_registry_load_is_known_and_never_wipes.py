"""A failed tool-registry load is KNOWN (``load_failed``) and never wipes a good snapshot.

THE INCIDENT (2026-10-02, clone reload): the database dropped connections while the server
loaded its tools. ``_fetch_tools_async`` swallowed the error and returned ``[]``, so:
- a boot looked like "a catalog with no tools" — surface manifests built on it were cached
  with their tools stripped, silently;
- a background ``reload_from_database`` that hit the same blip swapped an EMPTY registry in
  over a working one.

1. A failed fetch sets ``load_failed`` (RED while the fetch returned ``[]`` like an empty catalog).
2. A failed reload keeps the previous snapshot (RED while reload always swapped).
3. A successful load clears ``load_failed``.
"""

from __future__ import annotations

from typing import Any

import pytest

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


def _orm_path(monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]] | None) -> None:
    async def _fetch() -> list[dict[str, Any]] | None:
        return None if rows is None else [dict(r) for r in rows]

    async def _noop(self: ToolRegistry) -> None:
        return None

    monkeypatch.setattr(ToolRegistry, "_resolve_tool_source", staticmethod(lambda: None))
    monkeypatch.setattr(ToolRegistry, "_fetch_tools_async", staticmethod(_fetch))
    monkeypatch.setattr(ToolRegistry, "_load_bindings_async", _noop)
    monkeypatch.setattr(ToolRegistry, "_load_executors_async", _noop)


async def test_a_failed_fetch_is_known(monkeypatch: pytest.MonkeyPatch) -> None:
    _orm_path(monkeypatch, None)
    registry = ToolRegistry()
    await registry.load_from_database()
    assert registry.load_failed is True, "a failed fetch looked like an empty catalog"


async def test_a_failed_reload_keeps_the_working_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    _orm_path(monkeypatch, [_ROW])
    registry = ToolRegistry()
    await registry.load_from_database()
    assert registry.get("lookup_order") is not None and registry.load_failed is False

    _orm_path(monkeypatch, None)
    await registry.reload_from_database()
    assert registry.get("lookup_order") is not None, (
        "a failed reload swapped an empty registry in over a working one"
    )


async def test_a_good_load_clears_the_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    _orm_path(monkeypatch, None)
    registry = ToolRegistry()
    await registry.load_from_database()
    _orm_path(monkeypatch, [_ROW])
    await registry.reload_from_database()
    assert registry.load_failed is False and registry.get("lookup_order") is not None
