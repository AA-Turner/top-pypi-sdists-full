"""Every content-bearing send of the ConsoleEmitter logs ONE capped line in production (review 6h, M2).

L-SPEED 6c made ``send_data`` one line; ``send_tool_event`` (tool arguments and results), ``send_completion``,
``send_info`` and ``send_error`` still printed whole on the same headless mandate lane. The summary also printed
values uncapped and ``sorted()`` raised on a dict with mixed-type keys. Red before: the secret reached the log, a
long node id printed whole, and ``{1: 'a', 'b': 2}`` raised TypeError out of ``send_data``.
"""

from __future__ import annotations

import asyncio
import logging
import re

import pytest

from matrx_connect.context.events import InfoPayload, ToolEventPayload
from matrx_connect.context.operations import CompletionPayload
from matrx_connect.emitters.console_emitter import SUMMARY_LINE_MAX, ConsoleEmitter

SECRET = "my SSN is 123-45-6789"


@pytest.fixture
def production(monkeypatch):
    from matrx_utils.conf import settings

    monkeypatch.delenv("MATRX_LOG_CONTENT", raising=False)
    settings.reset_env_variables()
    yield
    monkeypatch.undo()
    settings.reset_env_variables()


def _sends(emitter: ConsoleEmitter):
    tool = ToolEventPayload(event="tool_completed", call_id="c1", tool_name="search", data={"args": SECRET})
    completion = CompletionPayload.model_construct(operation="chat", operation_id="op1", status="success",
                                                   result={"text": SECRET})
    info = InfoPayload(code="note", system_message=SECRET, metadata={"x": SECRET})
    return [
        emitter.send_tool_event(tool),
        emitter.send_tool_event({"event": "tool_started", "tool_name": "t", "arguments": SECRET}),
        emitter.send_completion(completion),
        emitter.send_info(info),
        emitter.send_error("boom", "failed", user_message=SECRET, details={"input": SECRET}),
        emitter.send_data({"event": "node_completed", "output": SECRET}),
    ]


def test_no_send_logs_content_in_production(production, capsys, caplog) -> None:
    emitter = ConsoleEmitter("t", accumulate=True)

    async def go():
        for send in _sends(emitter):
            await send

    with caplog.at_level(logging.DEBUG):
        asyncio.run(go())
    captured = capsys.readouterr()
    logged = [r.getMessage() for r in caplog.records if "[t]" in r.getMessage()]
    out = "\n".join([captured.out, captured.err, *logged])
    assert "123-45-6789" not in out
    lines = {re.sub(r"\x1b\[[0-9;]*m", "", ln).split("[t] ", 1)[1] for ln in out.splitlines() if "[t] " in ln}
    assert len(lines) == 6, out
    assert "tool_name=search" in out and "error_type=boom" in out and "message='failed'" in out
    assert emitter._accumulated["tool_events"][0]["data"] == {"args": SECRET}  # the caller still gets it all


def test_a_summary_is_capped_and_never_raises_on_mixed_keys(production, capsys) -> None:
    emitter = ConsoleEmitter("t", accumulate=False)
    asyncio.run(emitter.send_data({"event": "x", "node_id": "n" * 5000, "run_id": "r" * 5000}))
    asyncio.run(emitter.send_data({1: "a", "b": 2}))
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) == 2
    assert all(len(ln) <= SUMMARY_LINE_MAX + 40 for ln in lines), [len(ln) for ln in lines]
    assert "keys=['1', 'b']" in lines[1]
