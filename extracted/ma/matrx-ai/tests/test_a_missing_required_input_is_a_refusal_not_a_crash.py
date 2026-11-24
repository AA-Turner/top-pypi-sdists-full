"""A run started without its declared required inputs is a caller refusal: the stream ends with
``required_variables_missing`` and the names to fill, and no ``stream_crash`` system_error is filed
(2026-11-03/04 live: 'X Search' / 'Brand Self-Page Reader' runs without inputs were filed as urgent crashes)."""

from __future__ import annotations

import json
import types
from typing import Any

import pytest

from matrx_ai.agents.required_variables import RequiredVariablesMissing
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.streaming import response as response_mod
from matrx_connect.streaming.response import create_streaming_response


def _ctx(emitter: Any) -> Any:
    return types.SimpleNamespace(request_id="req-required-1", user_id="user-1", conversation_id=None,
                                 source_app="test", agent_id=None, emitter=emitter)


@pytest.mark.asyncio
async def test_a_missing_required_input_ends_the_stream_without_filing_a_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []

    async def _capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    monkeypatch.setattr(response_mod, "capture_error", _capture)

    async def task(emitter: Any) -> None:
        raise RequiredVariablesMissing(["target"], agent_name="X Search")

    response = create_streaming_response(_ctx(StreamEmitter(heartbeat_interval=600)), task, debug_label="chat")
    events: list[dict[str, Any]] = []
    async for chunk in response.body_iterator:
        text = chunk.decode() if isinstance(chunk, bytes) else chunk
        events.extend(json.loads(line) for line in text.splitlines() if line.strip())

    errors = [e for e in events if e.get("event") == "error"]
    assert errors and errors[-1]["data"]["error_type"] == "required_variables_missing"
    assert errors[-1]["data"]["user_message"] == "Fill in target to run this agent."
    assert "stream_crash" not in captured, "a run refused for a missing input was filed as a crash"
