"""Lazy tool calls (S6): a fold tool's tool_completed frame stays small; pinned tools keep the full result.

Forcing function: drives the real ToolStreamManager.completed() with a fake emitter and
asserts what actually goes over the wire AND what is persisted for execution_events.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.tools.models import ToolResult
from matrx_ai.tools.streaming import ToolStreamManager

@pytest.fixture(autouse=True)
def _lazy_on(monkeypatch, request):
    if "default_off" not in request.node.name:
        monkeypatch.setenv("MATRX_LAZY_TOOL_RESULTS", "1")


FRAME_BUDGET_BYTES = 4608  # 4.5 KB: the design's ceiling for a fold tool's frame


class _Emitter:
    def __init__(self) -> None:
        self.frames: list[dict] = []

    async def send_tool_event(self, payload: dict) -> None:
        self.frames.append(payload)


def _big_result() -> dict:
    return {"results": [{"title": f"Result {i}", "snippet": "lorem ipsum " * 20} for i in range(60)]}


async def _complete(tool_name: str, output: dict, *, row_id: str | None = "row-1"):
    emitter = _Emitter()
    stream = ToolStreamManager(emitter, "call-1", tool_name, row_id=row_id)
    await stream.completed("Done", result=ToolResult(success=True, output=output))
    return emitter.frames[-1], stream


@pytest.mark.asyncio
async def test_fold_tool_big_result_frame_is_small_and_flagged():
    big = _big_result()
    assert len(json.dumps(big)) > 10_000
    frame, stream = await _complete("web", big)
    assert len(json.dumps(frame).encode()) <= FRAME_BUDGET_BYTES
    data = frame["data"]
    assert data["result_omitted"] is True
    assert data["result"] is None
    assert len(data["result_preview"]) <= 500
    assert data["output_chars"] > 10_000
    assert data["tool_call_id"] == "row-1"
    # The persisted copy (execution_events) is untouched: still the full result.
    persisted = stream.get_events_for_persistence()[-1]
    assert persisted["data"]["result"] == big
    assert persisted["data"].get("result_omitted") in (None, False)


@pytest.mark.asyncio
async def test_fold_tool_small_result_rides_in_full():
    small = {"count": 3, "items": ["a", "b", "c"]}
    frame, _ = await _complete("web", small)
    assert frame["data"]["result"] == small
    assert frame["data"].get("result_omitted") in (None, False)


@pytest.mark.asyncio
@pytest.mark.parametrize("tool", ["ask_person", "update_plan", "request_user_takeover", "google_email_send"])
async def test_pinned_tool_keeps_the_full_result(tool: str):
    big = _big_result()
    frame, _ = await _complete(tool, big)
    assert frame["data"]["result"] == big
    assert frame["data"].get("result_omitted") in (None, False)


@pytest.mark.asyncio
async def test_a_held_write_is_pinned_by_its_result():
    held = {"awaiting_approval": True, "approval": {"x": 1}, "records": _big_result()["results"]}
    frame, _ = await _complete("records", held)
    assert frame["data"]["result"] == held


@pytest.mark.asyncio
async def test_default_off_an_old_client_still_gets_the_full_result():
    """Slim frames ship only when MATRX_LAZY_TOOL_RESULTS is on (old clients cannot read result_omitted)."""
    big = _big_result()
    frame, _ = await _complete("web", big)
    assert frame["data"]["result"] == big
    assert not frame["data"].get("result_omitted")


@pytest.mark.asyncio
async def test_an_unpersisted_run_keeps_the_full_result():
    """store=false has no chat.tool_call row to read by id: slimming would leave a blank."""
    big = _big_result()
    frame, _ = await _complete("web", big, row_id=None)
    assert frame["data"]["result"] == big
    assert frame["data"].get("result_omitted") in (None, False)
