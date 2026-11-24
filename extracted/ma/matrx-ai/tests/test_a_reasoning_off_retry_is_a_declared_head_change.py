"""FORCING GUARD — the empty-reply retry's reasoning-off send is a declared wire-head change, not drift.

Live (system_error ``prompt_cache_prefix_drift``, request 72d3cd13, claude-haiku-5-5 on the iPhone,
2026-11-12): "Wire prefix changed between rounds of one provider loop: thinking changed". Attempt 1 spent
all 2,250 output tokens thinking; ``_turn_reasoning_off_for_retry`` sent the same call once with reasoning
off (``one_call``), as designed. The send boundary never declared that one-call change, so the cache guard
filed a lawful retry as an unexplained prefix break. The send boundary now records the one-call settings
on ``SendPrep``, ``declared_history_rewrites`` turns a reasoning setting into a declared ``thinking`` head
change, and the guard accepts it on that round and on the round after (which restores the authored
setting). An undeclared ``thinking`` change still files.

SUT: the real ``prepare_for_send`` (loop stage, one_call), the real ``declared_history_rewrites`` and
``observe_cache_usage``.
"""

from __future__ import annotations

import asyncio
import copy
import uuid

import pytest
from test_the_send_boundary_never_writes_the_stored_config import (  # noqa: F401 — autouse fixture
    CONVERSATION_ID,
    REASONING_OFF,
    REQUEST_ID,
    _catalog,
    _stored,
)

from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.providers import cache_guard


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


def _body(thinking: dict | None, turns: int) -> dict:
    body: dict = {
        "model": "claude-haiku-5-5",
        "system": "S",
        "messages": [
            {"role": "user" if i % 2 == 0 else "assistant", "content": [{"type": "text", "text": f"m{i}"}]}
            for i in range(turns)
        ],
    }
    if thinking is not None:
        body["thinking"] = thinking
    return body


def _observe(rounds: list[tuple[dict, cache_guard.TrimDeclaration | None]]) -> None:
    loop = uuid.uuid4().hex
    for body, declared in rounds:
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-haiku-5-5", conversation_id="c-retry", request_id="r-retry",
            loop_id=loop, system_text="S", tool_names=(),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 6000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=declared,
        )


@pytest.mark.asyncio
async def test_the_send_boundary_declares_a_one_call_reasoning_change() -> None:
    stored = _stored("claude-haiku-5-5", effort=None, budget=None)
    prep = await prepare_for_send(
        stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=1,
        one_call=copy.deepcopy(REASONING_OFF),
    )
    assert cache_guard.declared_history_rewrites(prep).heads == frozenset({"thinking"})
    plain = await prepare_for_send(
        stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=2,
    )
    assert cache_guard.declared_history_rewrites(plain).heads == frozenset()


@pytest.mark.asyncio
async def test_a_declared_reasoning_off_retry_and_its_restore_file_no_drift(captured) -> None:
    on = {"type": "adaptive"}
    retry = cache_guard.TrimDeclaration(heads=frozenset({"thinking"}))
    _observe([(_body(on, 3), None), (_body({"type": "disabled"}, 3), retry), (_body(on, 5), cache_guard.TrimDeclaration())])
    await asyncio.sleep(0.05)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows == [], f"a declared one-call retry was filed as drift: {rows and rows[0]['payload']['changed']}"


@pytest.mark.asyncio
async def test_an_undeclared_thinking_change_still_files(captured) -> None:
    _observe([(_body({"type": "adaptive"}, 3), None), (_body({"type": "disabled"}, 3), cache_guard.TrimDeclaration())])
    await asyncio.sleep(0.05)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows and rows[0]["payload"]["changed"] == ["thinking changed"], rows
