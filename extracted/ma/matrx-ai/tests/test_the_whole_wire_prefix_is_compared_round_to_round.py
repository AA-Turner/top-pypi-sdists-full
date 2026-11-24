"""The cache guard compares the WHOLE wire prefix between rounds of a loop, and names what moved.

PB-03 copy O (gpt-5-nano): ``prompt_cache_read_missing`` twice (f80519b6, 933ed1d3). The guard
compared only system text and tool NAMES, so it could not say whether a whole-prefix wobble caused
the zero read. Compared by hand, the two stored requests share every byte of the prefix; a replay of
them hit 18 of 18. The fixture is those two real requests (long strings trimmed), so every test
below runs on the shape OpenAI actually received.

SUT: the real ``cache_guard.observe_cache_usage``. Failed before the wire layer existed.
"""

from __future__ import annotations

import ast
import asyncio
import copy
import json
import uuid
from pathlib import Path

import pytest

from matrx_ai.providers import cache_guard

_FIX = json.loads((Path(__file__).parent / "fixtures" / "pb03_gpt5_nano_two_rounds.json").read_text())
_MODEL = "gpt-5-nano-2025-08-07"


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    cache_guard.reset_loop("conv-wire", "req-wire")
    if hasattr(cache_guard, "reset_stable_miss_streaks"):
        cache_guard.reset_stable_miss_streaks()
    return rows


def _usage(cached: int = 0) -> dict:
    return {"input_tokens": 11698, "input_tokens_details": {"cached_tokens": cached}, "output_tokens": 10}


async def _rounds(*payloads, provider="openai", model=_MODEL, cached=0) -> None:
    loop = uuid.uuid4().hex  # one fresh loop per test
    for payload in payloads:
        cache_guard.observe_cache_usage(
            provider=provider,
            model=model,
            conversation_id="conv-wire",
            request_id="req-wire",
            loop_id=loop,
            system_text="same system",
            tool_names=("agent",),
            raw_usage=_usage(cached),
            wire_payload=payload,
        )
    await asyncio.sleep(0.05)  # detached captures


def _kinds(rows: list[dict]) -> list[str]:
    return [r["kind"] for r in rows]


def _call(n: int) -> dict:
    return copy.deepcopy(_FIX[f"call_{n}"])


@pytest.mark.asyncio
async def test_the_two_real_rounds_are_stable_and_the_miss_says_so(captured) -> None:
    # The two real rounds share every byte of the prefix: the zero read was OpenAI's cache routing, not
    # our prefix, so it is a yellow line and never filed (2026-11-14). A direct replay of this loop at the
    # Responses API missed call 2 in 3 of 6 streamed runs (2026-11-15), so repeated misses in one loop are
    # ordinary too: none is filed while the wire stays proven stable.
    await _rounds(_call(1), _call(2))
    assert _kinds(captured) == [], "a routing miss on a proven-stable prefix is not filed"
    await _rounds(_call(1), _call(2), _call(2), _call(2))
    assert _kinds(captured) == [], "nor are repeated ones in the same loop"


@pytest.mark.asyncio
async def test_a_stable_wire_miss_streak_files_and_says_the_prefix_was_stable(captured, monkeypatch) -> None:
    """A cache that never hits still files once the streak is reached, and the row says the prefix was
    byte-stable, so the reader knows the zero read was the provider's."""
    cache_guard.reset_stable_miss_streaks()
    monkeypatch.setattr(cache_guard, "OPENAI_STABLE_MISS_STREAK_TO_FILE", 3)
    await _rounds(_call(1), _call(2), _call(2), _call(2))
    assert _kinds(captured) == ["prompt_cache_read_missing"]
    assert captured[0]["payload"]["wire_prefix_stable"] is True
    assert captured[0]["payload"]["stable_miss_streak"] == 3


@pytest.mark.asyncio
async def test_a_clock_inside_the_prefix_is_named(captured) -> None:
    second = _call(2)
    second["input"][1]["content"][0]["text"] = second["input"][1]["content"][0]["text"].replace(
        "<turn_context", "<turn_context at=\"02:15:11\""
    )
    await _rounds(_call(1), second, cached=5)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert len(rows) == 1
    assert "input[1]" in str(rows[0]["payload"]["changed"])
    assert "turn_context" not in repr(rows[0]), "no prompt text in the row"


@pytest.mark.asyncio
async def test_a_key_order_wobble_inside_a_tool_schema_is_caught(captured) -> None:
    second = _call(2)
    props = second["tools"][0]["parameters"]["properties"]
    second["tools"][0]["parameters"]["properties"] = dict(reversed(list(props.items())))
    await _rounds(_call(1), second, cached=5)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows and "tools[0] (agent)" in str(rows[0]["payload"]["changed"])


@pytest.mark.asyncio
async def test_reordered_tools_are_named_on_the_miss(captured) -> None:
    """A tool CONTENT change is Layer 0b's row; the miss still names it."""
    second = _call(2)
    second["tools"][0], second["tools"][1] = second["tools"][1], second["tools"][0]
    await _rounds(_call(1), second)
    miss = next(r for r in captured if r["kind"] == "prompt_cache_read_missing")
    assert "tools[0] (agent) is now send_message" in miss["payload"]["wire_prefix_changed"]


@pytest.mark.asyncio
async def test_a_changing_cache_key_is_named(captured) -> None:
    second = _call(2)
    second["prompt_cache_key"] = "matrx_another"
    await _rounds(_call(1), second, cached=5)
    assert "prompt_cache_key" in str(_changed(captured))


def _changed(rows: list[dict]) -> list:
    return [r["payload"]["changed"] for r in rows if r["kind"] == "prompt_cache_prefix_drift"]


@pytest.mark.asyncio
async def test_a_new_round_only_appends_and_nothing_is_filed(captured) -> None:
    await _rounds(_call(1), _call(2), cached=5)
    assert captured == []


@pytest.mark.asyncio
async def test_the_previous_rounds_last_item_may_move(captured) -> None:
    second = _call(2)
    second["input"][2] = {"role": "developer", "content": [{"type": "input_text", "text": "later tail"}]}
    await _rounds(_call(1), second, cached=5)
    assert captured == [], "the item that ended the previous round is behind the stable line"


@pytest.mark.asyncio
async def test_a_shrunk_old_tool_output_is_drift_unless_a_trim_declared_it(captured) -> None:
    """Size never decides (C25 review): a shrunk old item is filed; only the send boundary's
    declared trim makes it lawful (``tests/test_the_wire_guard_files_every_unproven_change_...``)."""
    first = _call(2)
    first["input"].append({"role": "user", "content": []})  # input[5] is now behind the stable line
    second = copy.deepcopy(first)
    second["input"].append({"role": "user", "content": []})
    second["input"][5]["output"] = "trimmed"
    await _rounds(first, second, cached=5)
    assert "input[5]" in str(_changed(captured))


@pytest.mark.asyncio
async def test_the_alarm_still_fires_when_the_wire_drifted(captured) -> None:
    second = _call(2)
    second["prompt_cache_key"] = "matrx_another"
    await _rounds(_call(1), second)
    assert "prompt_cache_read_missing" in _kinds(captured), "the firing rule is unchanged"
    miss = next(r for r in captured if r["kind"] == "prompt_cache_read_missing")
    assert miss["payload"]["wire_prefix_stable"] is False
    assert "prompt_cache_key" in str(miss["payload"]["wire_prefix_changed"])


@pytest.mark.asyncio
async def test_a_moved_anthropic_mark_is_not_drift(captured) -> None:
    def body(marked: int) -> dict:
        msgs = [
            {"role": "user", "content": [{"type": "text", "text": f"m{i}"}]}
            for i in range(3)
        ]
        msgs[marked]["content"][0]["cache_control"] = {"type": "ephemeral"}
        return {
            "model": "claude-test",
            "system": [{"type": "text", "text": "sys", "cache_control": {"type": "ephemeral"}}],
            "tools": [{"name": "t", "input_schema": {"type": "object"}}],
            "messages": msgs,
        }

    await _rounds(body(0), body(2), provider="anthropic", model="claude-test", cached=5)
    assert _changed(captured) == []


@pytest.mark.asyncio
async def test_google_system_inside_config_is_compared(captured) -> None:
    def body(system: str) -> dict:
        return {
            "model": "gemini-test",
            "contents": [{"role": "user", "parts": [{"text": "hi"}]}, {"role": "user", "parts": [{"text": "b"}]}],
            "config": {"system_instruction": {"parts": [{"text": system}]}, "tools": []},
        }

    await _rounds(body("a"), body("b"), provider="google", model="gemini-test", cached=5)
    assert "system" in str(_changed(captured))


def test_the_executor_hands_the_guard_the_wire_body() -> None:
    src = (Path(cache_guard.__file__).parent.parent / "orchestrator" / "executor.py").read_text()
    calls = [
        n for n in ast.walk(ast.parse(src))
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "observe_cache_usage"
    ]
    assert calls and all(any(k.arg == "wire_payload" for k in c.keywords) for c in calls)
