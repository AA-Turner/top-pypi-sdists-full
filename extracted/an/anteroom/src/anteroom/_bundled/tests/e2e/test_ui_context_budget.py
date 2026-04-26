"""API-facing context-budget regression for web proactive compaction (#1571)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import AgentEvent, run_agent_loop

pytestmark = pytest.mark.e2e


async def _collect(gen: Any) -> list[AgentEvent]:
    events: list[AgentEvent] = []
    async for event in gen:
        events.append(event)
    return events


async def _executor(name: str, args: dict[str, Any]) -> dict[str, Any]:
    return {"result": "ok"}


@pytest.mark.asyncio
async def test_web_shared_loop_compacts_on_full_request_overhead() -> None:
    """The web/SSE path sees a compacting phase when fixed overhead crosses the threshold."""
    ai = AsyncMock()
    ai.config = SimpleNamespace(system_prompt="web system overhead " * 500)
    ai.complete = AsyncMock(return_value="Summary")

    async def _stream_chat(
        messages: Any,
        tools: Any = None,
        cancel_event: Any = None,
        extra_system_prompt: Any = None,
    ) -> Any:
        yield {"event": "token", "data": {"content": "ok"}}
        yield {"event": "done", "data": {}}

    ai.stream_chat = _stream_chat
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "short 1"},
        {"role": "assistant", "content": "short 2"},
        {"role": "user", "content": "short 3"},
        {"role": "assistant", "content": "short 4"},
        {"role": "user", "content": "short 5"},
    ]

    events = await _collect(
        run_agent_loop(
            ai_service=ai,
            messages=messages,
            tool_executor=_executor,
            tools_openai=[{"type": "function", "function": {"name": "web_tool", "description": "schema " * 100}}],
            extra_system_prompt="web dynamic overhead " * 100,
            summary_trigger_msg_count=10_000,
            summary_trigger_token_count=100,
        )
    )

    phase = next(event.data for event in events if event.kind == "phase" and event.data.get("phase") == "compacting")
    assert phase["reason"] == "token_threshold"
    assert phase["message_tokens"] < 100
    assert phase["estimated_tokens"] >= 100
    assert phase["system_prompt_tokens"] > 0
    assert phase["tool_schema_tokens"] > 0
