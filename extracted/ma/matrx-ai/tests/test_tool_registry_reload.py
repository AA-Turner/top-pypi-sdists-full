from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from matrx_ai.tools.models import ToolDefinition
from matrx_ai.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_reload_keeps_old_snapshot_visible_until_atomic_swap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = ToolRegistry()
    registry.register(ToolDefinition(name="old_tool", description="old", parameters={}))
    registry._loaded = True

    replacement_load = AsyncMock(return_value=1)

    async def load_replacement(self: ToolRegistry) -> int:
        assert registry.get("old_tool") is not None
        self.register(ToolDefinition(name="new_tool", description="new", parameters={}))
        self._loaded = True
        return await replacement_load()

    monkeypatch.setattr(ToolRegistry, "load_from_database", load_replacement)

    loaded = await registry.reload_from_database()

    assert loaded == 1
    assert registry.get("old_tool") is None
    assert registry.get("new_tool") is not None
