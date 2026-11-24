"""A mode switch inside one turn is the ``agent_modes`` part's DECLARED seal break, never prefix drift.

``set_mode`` changes the ``<agent_modes>`` span the send boundary appends to the wire system text, so the
next call of the same loop carries a different system head. The part is registered with
``known_seal_break`` (platform_parts), and Layer 1b (``cache_guard.compare_wire_prefix``) now compares the
system head with every declared break's span removed: a change confined to those spans is lawful (said,
not filed); any other system change still files ``prompt_cache_prefix_drift``.

Fails when: a switch confined to the span files a drift row; a change outside declared spans is let pass.
"""

from __future__ import annotations

import asyncio
import uuid

import pytest

from matrx_ai.config.agent_modes import render_block
from matrx_ai.providers import cache_guard

AGENT = "You are a careful planner. " * 40
MODES = [
    {"key": "discovery", "name": "Discovery", "description": "learn first", "instructions": "Ask first."},
    {"key": "answer", "name": "Answer", "description": "answer now", "instructions": "Answer now."},
]


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


def _body(system: str, turns: int) -> dict:
    messages = [{"role": "user", "content": "Help me plan."}]
    for i in range(turns):
        messages.append({"role": "assistant", "content": [{"type": "tool_use", "id": f"t{i}", "name": "set_mode", "input": {}}]})
        messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": "ok"}]})
    return {
        "model": "m",
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "tools": [{"name": "set_mode", "input_schema": {"type": "object"}}],
        "messages": messages,
    }


async def _drift_rows(first_system: str, second_system: str, captured: list[dict]) -> list[dict]:
    loop = uuid.uuid4().hex
    for system, turns in ((first_system, 0), (second_system, 1)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-test", conversation_id="conv-modes", request_id="req-modes",
            loop_id=loop, system_text=AGENT, tool_names=("set_mode",),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=_body(system, turns),
        )
    await asyncio.sleep(0.05)
    return [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]


def _wire_system(mode: str | None, agent: str = AGENT) -> str:
    return f"{agent}\n\n{render_block(MODES, mode)}"


@pytest.mark.asyncio
async def test_a_switch_that_changes_only_the_modes_span_files_nothing(captured) -> None:
    assert await _drift_rows(_wire_system(None), _wire_system("answer"), captured) == []


@pytest.mark.asyncio
async def test_a_change_outside_the_declared_span_still_files(captured) -> None:
    rows = await _drift_rows(_wire_system(None), _wire_system("answer", agent=AGENT + "Today is Friday."), captured)
    assert len(rows) == 1 and rows[0]["payload"]["changed"] == ["system changed"]


def test_the_lawful_change_is_said_not_filed() -> None:
    prev = cache_guard.wire_prefix(_body(_wire_system(None), 0))
    new = cache_guard.wire_prefix(_body(_wire_system("answer"), 1), prev)
    drift = cache_guard.compare_wire_prefix(prev, new)
    assert drift.changed == () and any("declared seal break" in line for line in drift.lawful)
