"""An orphan_tool_use_repaired row names the tools and call ids (feedback e1342691).

The rows said only "3 tool call(s) never produced a result", so nobody could join them to
cx_tool_call to see whether a client, a restart or a stream drop lost the call.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import tool_result_guard


@pytest.mark.asyncio
async def test_the_row_names_the_tools_and_the_call_ids(monkeypatch):
    seen: dict = {}

    async def capture_error(exc, **kw):
        seen["text"] = str(exc)
        seen.update(kw)

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", capture_error)
    await tool_result_guard.capture_orphan_tool_uses(
        layer="test",
        repaired=[{"tool_use_id": "toolu_a", "name": "page_check"}, {"tool_use_id": "toolu_b", "name": "records"}],
        context={"request_id": "r1"},
    )
    assert "page_check" in seen["text"] and "records" in seen["text"]
    assert seen["context"]["tool_use_ids"] == ["toolu_a", "toolu_b"]
    assert seen["context"]["tool_names"] == ["page_check", "records"]
