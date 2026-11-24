"""Live 2026-11-06 on admin@admin.com's /staff: the stream said "Some tools configured for this request are not
registered and will be unavailable." and named none of them — the person (and the agent reading the screen) could
not tell which tool was gone. Nothing fails silently: the warning the person sees names every missing tool."""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools.registry import ToolRegistry


class _Recorder:
    def __init__(self) -> None:
        self.warnings: list = []

    async def send_warning(self, payload) -> None:
        self.warnings.append(payload)


@pytest.mark.asyncio
async def test_the_person_is_told_which_tools_are_missing() -> None:
    emitter = _Recorder()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        reg = ToolRegistry()
        reg._loaded = True
        reg._tools["present_tool"] = object()  # type: ignore[assignment]
        assert reg.get_provider_tools(["ghost_tool_one", "ghost_tool_two"], "anthropic") == []
        for _ in range(20):
            if emitter.warnings:
                break
            await asyncio.sleep(0.01)
    finally:
        clear_app_context(token)

    (warning,) = emitter.warnings
    assert warning.code == "tools_missing"
    for name in ("ghost_tool_one", "ghost_tool_two"):
        assert name in warning.user_message, warning.user_message
        assert name in warning.system_message
