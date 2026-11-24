"""A local tool runs with ITS OWN stream in ``CURRENT_TOOL_STREAM`` (cleared after), so a step it emits is
persisted with the call (``execution_events``) instead of streamed live through a throwaway manager."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolResult
from matrx_ai.tools.streaming import CURRENT_TOOL_STREAM, ToolStreamManager


@pytest.mark.asyncio
async def test_local_tool_runs_with_its_own_stream() -> None:
    stream = ToolStreamManager(None, "call-1", "t")
    seen: list[object] = []

    async def func(_args, _ctx):
        seen.append(CURRENT_TOOL_STREAM.get())
        return ToolResult(success=True, output={"ok": True})

    tool_def = SimpleNamespace(_callable=func, name="t")
    ctx = SimpleNamespace(call_id="call-1")
    await ToolExecutor._execute_local(object(), tool_def, {}, ctx, stream)  # type: ignore[arg-type]
    assert seen == [stream]
    assert CURRENT_TOOL_STREAM.get() is None
