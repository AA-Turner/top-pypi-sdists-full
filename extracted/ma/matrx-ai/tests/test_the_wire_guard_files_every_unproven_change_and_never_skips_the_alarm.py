"""The wire-prefix layer (Layer 1b) after review (C25 follow-up, 2026-11-08).

1. An old item that SHRANK was labelled "lawful" by size alone and never filed. Only a change the send
   boundary declares for this round (the context trim's rewritten blocks) is lawful; every other
   change before the previous round's last item is drift and is filed.
2. Every round re-hashed the whole history (~50 ms on a 130k-token prefix, on the event loop). Old
   items are now proven unchanged by one streaming digest; only new items get their own digest.
3. A bug inside the wire layer escaped ``_observe`` before Layer 2 ran, so the miss alarm never fired.
4. A provider that never captures a payload left the previous round's payload on the state, and the
   guard compared it to itself ("stable"). ``send_once`` now clears it before every provider call.
5. ``tool_choice``, Anthropic ``thinking`` and Chat Completions ``response_format`` are prefix fields.

SUT: the real ``cache_guard.observe_cache_usage`` and the real ``send_once``.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace

import pytest

from matrx_ai.providers import cache_guard


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


def _body(n: int, *, out: int = 3000) -> dict:
    msgs: list[dict] = []
    for i in range(n):
        if i % 2 == 0:
            msgs.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": "x" * out}]})
        else:
            msgs.append({"role": "assistant", "content": [{"type": "tool_use", "id": f"t{i + 1}", "name": "look", "input": {"q": i}}]})
    return {
        "model": "claude-test",
        "max_tokens": 1000,
        "system": [{"type": "text", "text": "sys " * 400, "cache_control": {"type": "ephemeral"}}],
        "tools": [{"name": "look", "input_schema": {"type": "object", "properties": {"q": {"type": "integer"}}}}],
        "messages": msgs,
    }


def _usage(read: int) -> dict:
    return {"input_tokens": 200, "cache_read_input_tokens": read, "cache_creation_input_tokens": 0, "output_tokens": 5}


async def _rounds(*payloads, read: int = 9000, trims: tuple | None = None, loop: str | None = None) -> None:
    loop = loop or uuid.uuid4().hex
    for index, payload in enumerate(payloads):
        extra = {} if trims is None else {"trimmed_blocks": trims[index]}
        cache_guard.observe_cache_usage(
            provider="anthropic",
            model="claude-test",
            conversation_id="conv-c32",
            request_id="req-c32",
            loop_id=loop,
            system_text="same system",
            tool_names=("look",),
            raw_usage=_usage(read),
            wire_payload=payload,
            **extra,
        )
    await asyncio.sleep(0.05)


def _drift(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["kind"] == "prompt_cache_prefix_drift"]


# ── 1. no size heuristic ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_shrunk_old_item_with_no_declared_trim_is_filed(captured) -> None:
    first, second = _body(6), _body(8)
    second["messages"][2]["content"][0]["content"] = "trimmed"
    await _rounds(first, second)
    rows = _drift(captured)
    assert len(rows) == 1, "an old item that shrank was waved through as lawful"
    assert "messages[2]" in str(rows[0]["payload"]["changed"])


@pytest.mark.asyncio
async def test_a_history_window_that_moved_is_filed(captured) -> None:
    await _rounds(_body(8), _body(4))
    rows = _drift(captured)
    assert rows and "history window" in str(rows[0]["payload"]["changed"])


@pytest.mark.asyncio
async def test_a_declared_trim_rewrite_is_lawful_and_not_filed(captured) -> None:
    first, second = _body(6), _body(8)
    second["messages"][2]["content"][0]["content"] = "trimmed"
    await _rounds(first, second, trims=(None, cache_guard.TrimDeclaration(results=frozenset({"t2"}))))
    assert _drift(captured) == []


@pytest.mark.asyncio
async def test_a_declared_trim_does_not_cover_more_items_than_it_rewrote(captured) -> None:
    first, second = _body(6), _body(8)
    second["messages"][0]["content"][0]["content"] = "trimmed"
    second["messages"][2]["content"][0]["content"] = "trimmed"
    await _rounds(first, second, trims=(None, cache_guard.TrimDeclaration(results=frozenset({"t2"}))))
    assert len(_drift(captured)) == 1


# ── 2. incremental: old items are not re-hashed one by one ──────────────────


@pytest.mark.asyncio
async def test_a_round_digests_only_its_new_items(monkeypatch, captured) -> None:
    calls = {"n": 0}
    real = cache_guard._short_digest

    def counting(raw: bytes) -> str:
        calls["n"] += 1
        return real(raw)

    monkeypatch.setattr(cache_guard, "_short_digest", counting)
    loop = uuid.uuid4().hex
    await _rounds(_body(40), loop=loop)
    calls["n"] = 0
    await _rounds(_body(42), loop=loop)
    # heads (system) + the new items (the previous round's last item and the two appended ones) +
    # at most one digest per unchanged tool block; the 39 old items are proven by one streaming
    # digest, never digested one by one.
    assert calls["n"] <= 6, f"{calls['n']} per-part digests for a round that added 2 items"
    assert _drift(captured) == []


@pytest.mark.asyncio
async def test_a_changed_old_item_is_still_named_on_the_incremental_path(captured) -> None:
    later = _body(42)
    later["messages"][10]["content"][0]["content"] = "y" * 3000  # same size, other bytes
    await _rounds(_body(40), later)
    rows = _drift(captured)
    assert rows and any("messages[10]" in c for c in rows[0]["payload"]["changed"])


# ── 3. a bug in the wire layer never skips the miss alarm ───────────────────


@pytest.mark.asyncio
async def test_a_broken_wire_layer_still_lets_the_miss_alarm_fire(monkeypatch, captured) -> None:
    def boom(*_a, **_k):
        raise RuntimeError("wire layer bug")

    monkeypatch.setattr(cache_guard, "compare_wire_prefix", boom)
    monkeypatch.setattr(cache_guard, "cacheable_input_threshold", lambda *_a: 100)
    misses: list[int] = []
    monkeypatch.setattr(cache_guard, "_scream_cache_miss", lambda **kw: misses.append(kw["call_index"]))
    loop = uuid.uuid4().hex
    await _rounds(_body(4), _body(6), _body(8), read=0, loop=loop)
    assert misses == [1, 2], "the wire layer's exception skipped Layer 2"
    state = next(s for k, s in cache_guard._LOOPS.items() if loop in k)
    assert state.call_count == 3, "the state update was skipped"


@pytest.mark.asyncio
async def test_a_broken_drift_notice_still_lets_the_miss_alarm_fire(monkeypatch, captured) -> None:
    def boom(**_k):
        raise RuntimeError("notice bug")

    monkeypatch.setattr(cache_guard, "_notice_wire_drift", boom)
    monkeypatch.setattr(cache_guard, "cacheable_input_threshold", lambda *_a: 100)
    misses: list[int] = []
    monkeypatch.setattr(cache_guard, "_scream_cache_miss", lambda **kw: misses.append(kw["call_index"]))
    second = _body(6)
    second["messages"][0]["content"][0]["content"] = "drift"
    await _rounds(_body(4), second, read=0)
    assert misses == [1]


# ── 4. a leftover payload is never compared to itself ──────────────────────


def test_send_once_clears_a_leftover_payload_when_the_provider_captures_none(monkeypatch) -> None:
    import matrx_ai.config.send_boundary as sb
    from matrx_ai.config.send_boundary import SendPrep
    from matrx_ai.orchestrator.execution_state import (
        ExecutionState,
        clear_execution_state,
        set_execution_state,
    )
    from matrx_ai.orchestrator.send_once import send_once

    class _NonCapturing:  # cohere / moonshot / mock: execute() never calls capture_request_payload
        async def execute(self, request):
            return SimpleNamespace(ok=True)

    async def _prep(config, **_kw):
        return SendPrep(stage=sb.STAGE_LOOP, wire_config=None)

    monkeypatch.setattr(sb, "prepare_for_send", _prep)
    state = ExecutionState()
    state.snapshot_payload = _body(4)  # left by the previous round (snapshots off: nobody popped it)
    token = set_execution_state(state)
    try:
        request = SimpleNamespace(config=SimpleNamespace(model="m", messages=[]), conversation_id=None, request_id=None)
        asyncio.run(send_once(_NonCapturing(), request, state=state, iteration=2))
    finally:
        clear_execution_state(token)
    assert state.snapshot_payload is None, "the previous round's payload survived into this round"


# ── 5. more prefix fields ──────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("key", "first", "second"),
    [
        ("tool_choice", {"type": "auto"}, {"type": "any"}),
        ("thinking", {"type": "enabled", "budget_tokens": 2000}, {"type": "enabled", "budget_tokens": 4000}),
        ("response_format", {"type": "json_object"}, {"type": "text"}),
    ],
)
def test_prefix_fields_are_compared(key, first, second) -> None:
    a, b = _body(4), _body(6)
    a[key], b[key] = first, second
    drift = cache_guard.compare_wire_prefix(cache_guard.wire_prefix(a), cache_guard.wire_prefix(b))
    assert any(key in c for c in drift.changed), drift
