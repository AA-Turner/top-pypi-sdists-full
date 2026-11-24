"""A page edit reaches the browser when the model finishes writing THAT edit, not when the reply ends.

Before 2026-11-15 every ``apply_surface_write`` of a reply was held until the whole reply was over
and then sent together, so three edits written over ten seconds all appeared at once.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.partial_args import tool_args_delta, tool_args_finished, tool_args_started, tool_args_stream_ended


class RecordingEmitter:
    def __init__(self) -> None:
        self.tool_events: list[dict[str, Any]] = []

    async def send_tool_event(self, event: dict[str, Any]) -> None:
        self.tool_events.append(event)


def _ready(emitter: RecordingEmitter) -> list[dict[str, Any]]:
    return [e for e in emitter.tool_events if e["data"].get("args_ready")]


@pytest.mark.asyncio
async def test_each_edit_is_announced_whole_as_it_closes_while_the_next_is_still_open() -> None:
    emitter = RecordingEmitter()
    await tool_args_started(emitter, 0, tool_name="apply_surface_write", call_id="toolu_a")
    await tool_args_delta(emitter, 0, '{"target": "card_content", "value": {"card_id": "c1", ')
    await tool_args_delta(emitter, 0, '"back": "Bent"}}')
    assert _ready(emitter) == []
    await tool_args_finished(emitter, 0)
    await tool_args_started(emitter, 1, tool_name="apply_surface_write", call_id="toolu_b")

    ready = _ready(emitter)
    assert [e["call_id"] for e in ready] == ["toolu_a"]
    assert ready[0]["event"] == "tool_started"
    assert ready[0]["data"]["arguments"] == {"target": "card_content", "value": {"card_id": "c1", "back": "Bent"}}


@pytest.mark.asyncio
async def test_an_edit_cut_off_mid_input_is_never_announced_as_ready() -> None:
    emitter = RecordingEmitter()
    await tool_args_started(emitter, 0, tool_name="apply_surface_write", call_id="toolu_c")
    await tool_args_delta(emitter, 0, '{"target": "card_content", "value": {"card_id"')
    await tool_args_stream_ended(emitter)
    assert _ready(emitter) == []


@pytest.mark.asyncio
async def test_other_tools_are_not_announced_early() -> None:
    emitter = RecordingEmitter()
    await tool_args_started(emitter, 0, tool_name="table", call_id="toolu_d")
    await tool_args_delta(emitter, 0, '{"action": "list"}')
    await tool_args_finished(emitter, 0)
    assert _ready(emitter) == []
