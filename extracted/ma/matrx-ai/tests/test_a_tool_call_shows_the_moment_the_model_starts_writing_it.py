"""A tool call appears the instant the model starts writing it, not after its whole input.

Measured live 2026-11-08: a call with a 2,000-character input left the browser on heartbeats
for 14 s, then the card and the input landed together.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.partial_args import tool_args_started


class RecordingEmitter:
    def __init__(self) -> None:
        self.tool_events: list[dict[str, Any]] = []

    async def send_tool_event(self, event: dict[str, Any]) -> None:
        self.tool_events.append(event)


class BrokenEmitter:
    async def send_tool_event(self, event: dict[str, Any]) -> None:
        raise RuntimeError("wire is gone")


@pytest.mark.asyncio
async def test_an_unregistered_tool_announces_itself_when_its_input_begins() -> None:
    emitter = RecordingEmitter()

    await tool_args_started(emitter, 0, tool_name="table", call_id="toolu_1")

    assert len(emitter.tool_events) == 1
    event = emitter.tool_events[0]
    assert event["event"] == "tool_started"
    assert event["call_id"] == "toolu_1"
    assert event["tool_name"] == "table"
    assert event["data"]["arguments"] == {}


@pytest.mark.asyncio
async def test_a_failed_announcement_never_breaks_the_model_stream() -> None:
    await tool_args_started(BrokenEmitter(), 0, tool_name="table", call_id="toolu_2")


@pytest.mark.asyncio
async def test_a_call_with_no_id_is_not_announced() -> None:
    emitter = RecordingEmitter()

    await tool_args_started(emitter, 0, tool_name="table", call_id="")

    assert emitter.tool_events == []
