"""A declared context trim makes lawful ONLY the wire items holding the blocks it rewrote (C32 review 2).

The first version counted blocks: one Anthropic message carries several tool_result blocks, so a
trim of three blocks inside messages[0] declared 3 and let an unrelated re-rendered messages[3] pass
as "context trim rewrite"; real drift in messages[1] plus a one-block trim in messages[4] was called
lawful while the trimmed item was filed under the wrong name. Now each rewritten block is placed on
the wire by its call id; a changed item is lawful only when it holds one. A rewrite that cannot be
placed never whitelists anything: the change is filed and names the trim as a possible cause.

SUT: the real ``declared_history_rewrites`` (the executor's reader of ``SendPrep``) and
``observe_cache_usage``. Counterexamples: the second review's ``test_rev_c32_wire.py``.
"""

from __future__ import annotations

import asyncio
import copy
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


def _body(n: int) -> dict:
    msgs: list[dict] = []
    for i in range(n):
        if i % 2 == 0:
            msgs.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": f"{p}{i}", "content": c * 3000}
                for p, c in (("a", "x"), ("b", "y"), ("c", "z"))
            ]})
        else:
            msgs.append({"role": "assistant", "content": [{"type": "text", "text": f"turn {i}"}]})
    return {"model": "m", "system": "S", "tools": [{"name": "look", "input_schema": {"type": "object"}}], "messages": msgs}


def _prep(*call_ids: str, fit_blocks: int = 0) -> SimpleNamespace:
    report = SimpleNamespace(
        blocks_rewritten=len(call_ids),
        rewritten_blocks=[{"message_position": 99, "call_id": cid, "tool_name": "look"} for cid in call_ids],
    )
    fit = {"passes": [{"pass": "forced_trim_4_8", "blocks_rewritten": fit_blocks}]} if fit_blocks else None
    return SimpleNamespace(trim_report=report, fit=fit)


async def _two_rounds(prev_body: dict, new_body: dict, prep: SimpleNamespace) -> list[dict]:
    loop = uuid.uuid4().hex
    rows: list[dict] = []
    for body, trim in ((prev_body, None), (new_body, cache_guard.declared_history_rewrites(prep))):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-test", conversation_id="conv-c32b", request_id="req-c32b",
            loop_id=loop, system_text="S", tool_names=("look",),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=trim,
        )
    await asyncio.sleep(0.05)
    return rows


def _drift(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["kind"] == "prompt_cache_prefix_drift"]


def _next(body: dict) -> dict:
    new = copy.deepcopy(body)
    new["messages"].append({"role": "user", "content": "next"})
    return new


@pytest.mark.asyncio
async def test_a_three_block_trim_in_one_item_does_not_whitelist_another_item(captured) -> None:
    prev = _body(8)
    new = _next(prev)
    for block in new["messages"][0]["content"]:
        block["content"] = "[trimmed]"
    new["messages"][3]["content"][0]["text"] = "turn 3 (re-rendered with a timestamp)"
    await _two_rounds(prev, new, _prep("a0", "b0", "c0"))
    rows = _drift(captured)
    assert rows, "unrelated drift in messages[3] was accepted as a trim rewrite and never filed"
    assert any("messages[3]" in c for c in rows[0]["payload"]["changed"])
    assert not any("messages[0]" in c for c in rows[0]["payload"]["changed"]), "the trimmed item is lawful"


@pytest.mark.asyncio
async def test_drift_before_the_trimmed_item_is_filed_under_its_own_name(captured) -> None:
    prev = _body(8)
    new = _next(prev)
    new["messages"][1]["content"][0]["text"] = "DRIFT"
    new["messages"][4]["content"][0]["content"] = "[trimmed]"
    await _two_rounds(prev, new, _prep("a4"))
    changed = _drift(captured)[0]["payload"]["changed"]
    assert any("messages[1]" in c for c in changed), "the drifted item was named lawful"
    assert not any("messages[4]" in c for c in changed), "the trimmed item was filed"


@pytest.mark.asyncio
async def test_a_trim_alone_is_lawful_and_not_filed(captured) -> None:
    prev = _body(8)
    new = _next(prev)
    for block in new["messages"][2]["content"][:2]:
        block["content"] = "[trimmed]"
    await _two_rounds(prev, new, _prep("a2", "b2"))
    assert _drift(captured) == []


@pytest.mark.asyncio
async def test_a_rewrite_that_cannot_be_placed_is_filed_and_named_as_a_possible_cause(captured) -> None:
    """A make-it-fit pass records counts, no call ids: the change it made is filed, never allowed by count."""
    prev = _body(8)
    new = _next(prev)
    new["messages"][2]["content"][0]["content"] = "[trimmed]"
    await _two_rounds(prev, new, _prep(fit_blocks=1))
    rows = _drift(captured)
    assert rows and any("messages[2]" in c and "possible cause" in c for c in rows[0]["payload"]["changed"])


def test_the_reviewers_mark_and_byte_counterexamples_hold() -> None:
    prev_body = _body(6)
    prev_body["messages"][4]["content"][-1]["cache_control"] = {"type": "ephemeral"}
    new_body = copy.deepcopy(prev_body)
    del new_body["messages"][4]["content"][-1]["cache_control"]
    new_body["messages"].append({"role": "user", "content": [{"type": "text", "text": "n", "cache_control": {"type": "ephemeral", "ttl": "1h"}}]})
    prev = cache_guard.wire_prefix(prev_body)
    assert cache_guard.compare_wire_prefix(prev, cache_guard.wire_prefix(new_body, prev)).stable
    item = {"role": "user", "content": [{"type": "text", "text": 'he said "cache_control":{"x":1} ok', "cache_control": {"type": "ephemeral"}}]}
    assert cache_guard._fast_bytes(item) == cache_guard._wire_bytes(item)
    inc_prev = cache_guard.wire_prefix(_body(10))
    later = _next(_body(10))
    later["messages"][5]["content"][0]["text"] = "x"
    assert cache_guard.wire_prefix(later, inc_prev).items == cache_guard.wire_prefix(later).items


# ── minors ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_failing_failure_report_still_lets_the_miss_alarm_fire(monkeypatch, captured) -> None:
    def boom(*_a, **_k):
        raise RuntimeError("wire layer bug")

    def report_boom(*_a, **_k):
        raise RuntimeError("the failure report itself broke")

    monkeypatch.setattr(cache_guard, "compare_wire_prefix", boom)
    monkeypatch.setattr(cache_guard, "_wire_layer_failed", report_boom)
    monkeypatch.setattr(cache_guard, "cacheable_input_threshold", lambda *_a: 100)
    misses: list[int] = []
    monkeypatch.setattr(cache_guard, "_scream_cache_miss", lambda **kw: misses.append(kw["call_index"]))
    loop = uuid.uuid4().hex
    for body in (_body(4), _body(6)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-test", conversation_id="c", request_id="r", loop_id=loop,
            system_text="S", tool_names=("look",),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
            wire_payload=body,
        )
    assert misses == [1]


def test_send_once_clears_the_payload_provider_too(monkeypatch) -> None:
    import matrx_ai.config.send_boundary as sb
    from matrx_ai.config.send_boundary import SendPrep
    from matrx_ai.orchestrator.execution_state import (
        ExecutionState,
        clear_execution_state,
        set_execution_state,
    )
    from matrx_ai.orchestrator.send_once import send_once

    class _NonCapturing:
        async def execute(self, request):
            return SimpleNamespace(ok=True)

    async def _p(config, **_kw):
        return SendPrep(stage=sb.STAGE_LOOP, wire_config=None)

    monkeypatch.setattr(sb, "prepare_for_send", _p)
    state = ExecutionState()
    state.snapshot_payload, state.snapshot_provider = {"messages": []}, "anthropic"
    token = set_execution_state(state)
    try:
        request = SimpleNamespace(config=SimpleNamespace(model="m", messages=[]), conversation_id=None, request_id=None)
        asyncio.run(send_once(_NonCapturing(), request, state=state, iteration=2))
    finally:
        clear_execution_state(token)
    assert state.snapshot_provider is None, "the previous round's provider stamp survived into this round"
