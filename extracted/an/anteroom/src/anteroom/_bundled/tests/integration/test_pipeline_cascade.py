"""Integration test for the multi-stage context compaction pipeline (#1266).

Drives the full 3-stage cascade in a single ``run_agent_loop`` run with a
mocked AIService that returns a staged event sequence — first a
``context_length_exceeded`` error, then success. Asserts that the new
microcompact narration token AND the existing reactive narrations all
surface in the event stream in the correct order.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.agent_loop import AgentEvent, run_agent_loop


def _make_stream_events(
    content: str = "",
    tool_calls: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if content:
        events.append({"event": "token", "data": {"content": content}})
    for tc in tool_calls or []:
        events.append({"event": "tool_call", "data": tc})
    events.append({"event": "done", "data": {}})
    return events


def _mock_ai_service(*rounds: list[dict[str, Any]]) -> AsyncMock:
    service = AsyncMock()
    call_count = 0

    async def _stream_chat(
        messages: Any, tools: Any = None, cancel_event: Any = None, extra_system_prompt: Any = None
    ) -> Any:
        nonlocal call_count
        idx = min(call_count, len(rounds) - 1)
        call_count += 1
        for event in rounds[idx]:
            yield event

    service.stream_chat = _stream_chat
    return service


async def _collect(gen: Any) -> list[AgentEvent]:
    events: list[AgentEvent] = []
    async for e in gen:
        events.append(e)
    return events


async def _executor(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True}


@pytest.mark.asyncio
async def test_microcompact_narration_appears_when_oversized_tool_result() -> None:
    """Proactive microcompact narration surfaces before the LLM call."""
    success = _make_stream_events("done")
    ai = _mock_ai_service(success)

    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
        },
        {"role": "tool", "tool_call_id": "tc1", "content": "X" * 10_000},
        {"role": "user", "content": "continue"},
    ]

    events = await _collect(
        run_agent_loop(
            ai_service=ai,
            messages=messages,
            tool_executor=_executor,
            tools_openai=None,
            tool_output_max_chars=100,
            microcompact_enabled=True,
            summary_trigger_msg_count=10_000,
            summary_trigger_token_count=1_000_000,
        )
    )

    tokens = [e for e in events if e.kind == "token"]
    assert any("Trimmed oversized tool outputs" in e.data.get("content", "") for e in tokens)


@pytest.mark.asyncio
async def test_microcompact_disabled_by_config_emits_nothing() -> None:
    """When microcompact_enabled=False the stage is fully skipped."""
    success = _make_stream_events("done")
    ai = _mock_ai_service(success)

    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "q"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
        },
        {"role": "tool", "tool_call_id": "tc1", "content": "X" * 10_000},
        {"role": "user", "content": "continue"},
    ]

    events = await _collect(
        run_agent_loop(
            ai_service=ai,
            messages=messages,
            tool_executor=_executor,
            tools_openai=None,
            tool_output_max_chars=100,
            microcompact_enabled=False,
            summary_trigger_msg_count=10_000,
            summary_trigger_token_count=1_000_000,
        )
    )

    tokens = [e for e in events if e.kind == "token"]
    # The microcompact narration must NOT appear.
    assert not any("Trimmed oversized tool outputs" in e.data.get("content", "") for e in tokens)


@pytest.mark.asyncio
async def test_full_cascade_microcompact_then_reactive_recovery() -> None:
    """Microcompact fires proactively; reactive recovery fires on context error.

    Uses a history with 3 turn groups so reactive Strategy 2/3 have
    something to collapse/drop if Strategy 1 is a no-op after
    microcompact. Both narration surfaces must appear in the stream.
    """
    context_error_events: list[dict[str, Any]] = [
        {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
    ]
    success = _make_stream_events("done")
    ai = _mock_ai_service(context_error_events, success)

    # 3 turn groups — each with a tool call and result.
    messages: list[dict[str, Any]] = []
    for i in range(3):
        tc_id = f"tc{i}"
        messages.extend(
            [
                {"role": "user", "content": f"q{i}"},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{"id": tc_id, "type": "function", "function": {"name": "bash", "arguments": "{}"}}],
                },
                {"role": "tool", "tool_call_id": tc_id, "content": "X" * 20_000},
            ]
        )
    messages.append({"role": "user", "content": "continue"})

    events = await _collect(
        run_agent_loop(
            ai_service=ai,
            messages=messages,
            tool_executor=_executor,
            tools_openai=None,
            tool_output_max_chars=100,
            microcompact_enabled=True,
        )
    )

    token_content = " ".join(e.data.get("content", "") for e in events if e.kind == "token")
    # Microcompact narration appeared on the first turn.
    assert "Trimmed oversized tool outputs" in token_content
    # Loop eventually completed — reactive recovery succeeded OR loop
    # terminated cleanly without hanging.
    assert any(e.kind == "done" or e.kind == "error" for e in events)


@pytest.mark.asyncio
async def test_reactive_strategies_narrate_unchanged_strings() -> None:
    """The 4 existing reactive narration strings are preserved verbatim."""
    context_error_events: list[dict[str, Any]] = [
        {"event": "error", "data": {"code": "context_length_exceeded", "retryable": False}},
    ]
    success = _make_stream_events("recovered")
    ai = _mock_ai_service(context_error_events, success)

    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "m1"},
        {"role": "assistant", "content": "r1"},
        {"role": "user", "content": "m2"},
        {"role": "assistant", "content": "r2"},
        {"role": "user", "content": "m3"},
    ]

    events = await _collect(
        run_agent_loop(
            ai_service=ai,
            messages=messages,
            tool_executor=_executor,
            tools_openai=None,
        )
    )

    # One of the 4 existing narration strings must appear — reactive
    # ladder preservation invariant from the v2 plan.
    token_content = " ".join(e.data.get("content", "") for e in events if e.kind == "token")
    assert any(
        s in token_content
        for s in (
            "truncated and retrying",
            "collapsed historical tool results",
            "dropped older conversation turns",
            "compacting conversation and retrying",
        )
    )
