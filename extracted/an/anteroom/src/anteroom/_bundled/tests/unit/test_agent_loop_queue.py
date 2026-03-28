"""Tests for enriched queued_message events in agent_loop (#1175)."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import AgentEvent, run_agent_loop

# -- Helpers --


def _make_stream_events(
    content: str = "",
    tool_calls: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build a list of stream events that ai_service.stream_chat would yield."""
    events: list[dict[str, Any]] = []
    if content:
        events.append({"event": "token", "data": {"content": content}})
    for tc in tool_calls or []:
        events.append({"event": "tool_call", "data": tc})
    events.append({"event": "done", "data": {}})
    return events


def _mock_ai_service(*rounds: list[dict[str, Any]]) -> AsyncMock:
    """Create a mock AIService that yields different stream events per call."""
    service = AsyncMock()
    call_count = 0

    async def _stream_chat(
        messages: Any,
        tools: Any = None,
        cancel_event: Any = None,
        extra_system_prompt: Any = None,
    ) -> Any:
        nonlocal call_count
        idx = min(call_count, len(rounds) - 1)
        call_count += 1
        for event in rounds[idx]:
            yield event

    service.stream_chat = _stream_chat
    return service


async def _collect_events(gen: Any) -> list[AgentEvent]:
    """Drain an async generator into a list."""
    events = []
    async for e in gen:
        events.append(e)
    return events


# =============================================================================
# Queue position enrichment tests
# =============================================================================


class TestQueuedMessageEnrichment:
    @pytest.mark.asyncio
    async def test_single_queued_message_has_position_and_depth(self) -> None:
        """A single queued message should have position=1, queue_depth=0."""
        # Round 1: initial response. Round 2: response to queued message.
        ai = _mock_ai_service(
            _make_stream_events(content="hello"),
            _make_stream_events(content="world"),
        )

        async def tool_exec(name: str, args: dict[str, Any]) -> dict[str, Any]:
            return {"output": "ok"}

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        await queue.put({"role": "user", "content": "follow-up"})

        messages: list[dict[str, Any]] = [{"role": "user", "content": "hi"}]
        events = await _collect_events(run_agent_loop(ai, messages, tool_exec, None, message_queue=queue))

        queued_events = [e for e in events if e.kind == "queued_message"]
        assert len(queued_events) == 1
        assert queued_events[0].data["position"] == 1
        assert queued_events[0].data["queue_depth"] == 0
        assert queued_events[0].data["content"] == "follow-up"

    @pytest.mark.asyncio
    async def test_multiple_queued_messages_fifo_order(self) -> None:
        """Multiple queued messages should process in FIFO order with correct positions."""
        ai = _mock_ai_service(
            _make_stream_events(content="r1"),
            _make_stream_events(content="r2"),
            _make_stream_events(content="r3"),
        )

        async def tool_exec(name: str, args: dict[str, Any]) -> dict[str, Any]:
            return {"output": "ok"}

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        await queue.put({"role": "user", "content": "first"})
        await queue.put({"role": "user", "content": "second"})

        messages: list[dict[str, Any]] = [{"role": "user", "content": "start"}]
        events = await _collect_events(run_agent_loop(ai, messages, tool_exec, None, message_queue=queue))

        queued_events = [e for e in events if e.kind == "queued_message"]
        assert len(queued_events) == 2
        # First dequeued message: position=1, queue_depth=1 (one remaining)
        assert queued_events[0].data["content"] == "first"
        assert queued_events[0].data["position"] == 1
        assert queued_events[0].data["queue_depth"] == 1
        # Second dequeued message: position=1, queue_depth=0 (processed in next iteration)
        assert queued_events[1].data["content"] == "second"
        assert queued_events[1].data["position"] == 1
        assert queued_events[1].data["queue_depth"] == 0

    @pytest.mark.asyncio
    async def test_empty_queue_no_queued_event(self) -> None:
        """An empty queue should produce no queued_message events."""
        ai = _mock_ai_service(_make_stream_events(content="done"))

        async def tool_exec(name: str, args: dict[str, Any]) -> dict[str, Any]:
            return {"output": "ok"}

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        messages: list[dict[str, Any]] = [{"role": "user", "content": "hi"}]
        events = await _collect_events(run_agent_loop(ai, messages, tool_exec, None, message_queue=queue))

        queued_events = [e for e in events if e.kind == "queued_message"]
        assert len(queued_events) == 0

    @pytest.mark.asyncio
    async def test_no_queue_no_queued_event(self) -> None:
        """When message_queue is None, no queued_message events are emitted."""
        ai = _mock_ai_service(_make_stream_events(content="done"))

        async def tool_exec(name: str, args: dict[str, Any]) -> dict[str, Any]:
            return {"output": "ok"}

        messages: list[dict[str, Any]] = [{"role": "user", "content": "hi"}]
        events = await _collect_events(run_agent_loop(ai, messages, tool_exec, None, message_queue=None))

        queued_events = [e for e in events if e.kind == "queued_message"]
        assert len(queued_events) == 0
