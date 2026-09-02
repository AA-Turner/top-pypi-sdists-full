from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext, ToolResult

ctx_module = importlib.import_module("matrx_ai.tools.implementations.ctx")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("arguments", "delegate_name"),
    [
        ({"key": "profile"}, "ctx_get"),
        ({"requests": [{"key": "profile"}]}, "ctx_batch"),
    ],
)
async def test_context_recovers_omitted_action_at_implementation_boundary(
    monkeypatch: pytest.MonkeyPatch,
    arguments: dict[str, Any],
    delegate_name: str,
) -> None:
    received: dict[str, Any] = {}

    async def delegate(args: dict[str, Any], _ctx: ToolContext) -> ToolResult:
        received.update(args)
        return ToolResult(success=True, output={"ok": True})

    monkeypatch.setattr(ctx_module, delegate_name, delegate)

    result = await ctx_module.context(arguments, ToolContext(call_id="call-1"))

    assert result.success is True
    assert received == {key: value for key, value in arguments.items() if key != "action"}


@pytest.mark.asyncio
async def test_context_still_rejects_empty_arguments() -> None:
    result = await ctx_module.context({}, ToolContext(call_id="call-1"))

    assert result.success is False
    assert result.error is not None
    assert "could not be inferred" in result.error.message
