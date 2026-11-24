"""THE SEND BOUNDARY NEVER WRITES THE STORED CONFIG (CGU-10 IMG6 finding 1, 2026-11-11).

The class: a setting meant for ONE call lands on the canonical ``UnifiedConfig``, which the chat
stores (``to_storage_dict``), so every later turn inherits it. Two members so far: the raised output
limit (IMG5 #8, 1,500 → 2,250 → 3,375 stored) and the empty-reply retry's reasoning off (IMG6 #1:
one empty reply switched thinking off for the rest of the chat).

Forcing, both doors:
  1. ``prepare_for_send`` at the loop stage, across every provider's thinking shape and with a
     one-call setting: the canonical config's stored form is byte-for-byte what it was before, and
     the one-call setting is on ``prep.wire_config``.
  2. The executor's empty-reply retry (``_turn_reasoning_off_for_retry``) writes nothing on the
     canonical config; the retry's reasoning off reaches the provider through ``send_once``.
  A refused send (the firewall raises) leaves the stored form untouched too.
"""

from __future__ import annotations

import copy
import json
from types import SimpleNamespace
from typing import Any

import pytest
from test_thinking_leaves_room_for_the_answer import OFFERINGS, _controls

from matrx_ai.catalog import resolve as catalog_resolve
from matrx_ai.config import context_preflight
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.knobs import configure_package_knobs
from matrx_ai.orchestrator.execution_state import ExecutionState

CONVERSATION_ID = "conv-boundary-never-writes-stored"
REQUEST_ID = "img6-1-req"

REASONING_OFF = {"reasoning_effort": "none", "thinking_budget": None, "thinking_level": None}


@pytest.fixture(autouse=True)
def _catalog(monkeypatch):
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    configure_package_knobs(None)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _profile(model: str, **_kw: Any) -> Any:
        return SimpleNamespace(model_name=model, offering_id="", controls=_controls(model))

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


def _stored(model: str, *, effort: str | None, budget: int | None) -> UnifiedConfig:
    messages = MessageList()
    messages.append_or_extend_user_text("Write a 150-word story ending in THE END.")
    config = UnifiedConfig(model=model, messages=messages, max_output_tokens=1500)
    config.reasoning_effort = effort  # type: ignore[assignment]
    config.thinking_budget = budget
    return config


def _snapshot(config: UnifiedConfig) -> str:
    return json.dumps(config.to_storage_dict(), sort_keys=True, default=str)


_CASES = [
    pytest.param("claude-haiku-5-5", None, None, id="claude-adaptive"),
    pytest.param("claude-haiku-4-5-20251001", None, 4000, id="claude-budget"),
    pytest.param("gemini-2.5-flash", "low", 1024, id="gemini-2.5-budget"),
    pytest.param("gemini-3.8-flash", None, None, id="gemini-3-level"),
    pytest.param("gpt-5.5", "medium", None, id="openai-effort"),
    pytest.param("plain-chat-model", None, None, id="no-reasoning"),
]


def test_every_case_is_a_known_offering() -> None:
    for case in _CASES:
        assert case.values[0] in OFFERINGS


@pytest.mark.asyncio
@pytest.mark.parametrize(("model", "effort", "budget"), _CASES)
@pytest.mark.parametrize("one_call", [None, REASONING_OFF], ids=["authored", "reasoning-off-retry"])
async def test_prepare_for_send_leaves_the_stored_config_exactly_as_it_came(
    model: str, effort: str | None, budget: int | None, one_call: dict[str, Any] | None
) -> None:
    stored = _stored(model, effort=effort, budget=budget)
    before = _snapshot(stored)
    for iteration in (1, 2, 3):  # later rounds of the same request, too
        prep = await prepare_for_send(
            stored,
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=iteration,
            one_call=copy.deepcopy(one_call),
        )
        assert _snapshot(stored) == before, f"round {iteration} wrote the stored config"
        if one_call:
            assert prep.wire_config is not None and prep.wire_config is not stored
            assert prep.wire_config.reasoning_effort == "none"
            assert prep.wire_config.thinking_budget is None
            assert "one_call_settings" in prep.steps


@pytest.mark.asyncio
async def test_a_refused_send_leaves_the_stored_config_exactly_as_it_came(monkeypatch) -> None:
    from matrx_ai.config import request_firewall

    def _refuse(_config: Any) -> None:
        raise RuntimeError("refused at the firewall")

    monkeypatch.setattr(request_firewall, "check_at_send", _refuse)
    stored = _stored("claude-haiku-5-5", effort="low", budget=None)
    before = _snapshot(stored)
    with pytest.raises(RuntimeError):
        await prepare_for_send(
            stored,
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=1,
            one_call=dict(REASONING_OFF),
        )
    assert _snapshot(stored) == before


@pytest.mark.asyncio
async def test_a_one_call_setting_outside_the_per_call_fields_is_refused_loudly() -> None:
    stored = _stored("claude-haiku-5-5", effort="low", budget=None)
    before = _snapshot(stored)
    with pytest.raises(ValueError, match="not a per-call field"):
        await prepare_for_send(
            stored,
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=1,
            one_call={"model": "something-else"},
        )
    assert _snapshot(stored) == before


def test_the_empty_reply_retry_writes_nothing_on_the_stored_config() -> None:
    from matrx_ai.orchestrator.executor import _turn_reasoning_off_for_retry

    stored = _stored("claude-haiku-5-5", effort="low", budget=None)
    before = _snapshot(stored)
    state = ExecutionState()
    assert _turn_reasoning_off_for_retry(SimpleNamespace(config=stored), state) is True
    assert _snapshot(stored) == before
    assert state.one_call_settings == REASONING_OFF
    # Spent: a second empty reply falls through to the honest failure.
    assert _turn_reasoning_off_for_retry(SimpleNamespace(config=stored), state) is False


@pytest.mark.asyncio
async def test_send_once_hands_the_retry_setting_to_one_send_only(monkeypatch) -> None:
    from matrx_ai.config import send_boundary
    from matrx_ai.orchestrator import send_once as send_once_mod

    seen: list[Any] = []
    real = send_boundary.prepare_for_send

    async def _spy(config: Any, **kwargs: Any) -> Any:
        seen.append(kwargs.get("one_call"))
        return await real(config, **kwargs)

    monkeypatch.setattr(send_boundary, "prepare_for_send", _spy)

    class _Client:
        def __init__(self) -> None:
            self.efforts: list[Any] = []

        async def execute(self, request: Any) -> Any:
            self.efforts.append(request.config.reasoning_effort)
            return SimpleNamespace(messages=[], finish_reason="stop")

    stored = _stored("claude-haiku-5-5", effort="low", budget=None)
    before = _snapshot(stored)
    request = SimpleNamespace(
        config=stored, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, organization_id=None
    )
    state = ExecutionState()
    state.one_call_settings = dict(REASONING_OFF)
    client = _Client()
    monkeypatch.setattr("matrx_ai.mandate_taps.observe_first_send", lambda *_a, **_k: None)

    async def _warm() -> None:
        return None

    monkeypatch.setattr("matrx_ai.processing.blocks.saved_blocks.warm_kind_registry", _warm)
    for iteration in (1, 2):
        await send_once_mod.send_once(client, request, state=state, iteration=iteration)
        assert request.config is stored
        assert _snapshot(stored) == before
    assert seen == [REASONING_OFF, None]
    assert client.efforts == ["none", "low"]


@pytest.mark.asyncio
async def test_two_sends_at_once_on_one_config_each_send_the_reserve_and_store_nothing(monkeypatch) -> None:
    """CGU-10 IMG6 #8 (attack A3): send A is held mid-boundary AFTER its reserve raised the limit;
    send B starts on the SAME config. B read the raised limit as authored: B sent 3,375, the config
    stored 2,250. The loop-stage boundary now runs one at a time per config."""
    import asyncio

    from matrx_ai.config import send_boundary

    gate = asyncio.Event()
    parked = asyncio.Event()
    real_policy = send_boundary._resolve_org_trim_policy
    first = True

    async def _hold_first(prep: Any, organization_id: Any) -> Any:  # runs after the reserve
        nonlocal first
        if first:
            first = False
            parked.set()
            await gate.wait()
        return await real_policy(prep, organization_id)

    monkeypatch.setattr(send_boundary, "_resolve_org_trim_policy", _hold_first)
    stored = _stored("claude-haiku-5-5", effort=None, budget=None)
    before = _snapshot(stored)
    for rid in ("race-a", "race-b"):
        reset_loop_state(CONVERSATION_ID, rid)

    async def _one(rid: str) -> Any:
        return await prepare_for_send(
            stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=rid, iteration=1
        )

    a = asyncio.ensure_future(_one("race-a"))
    await asyncio.wait_for(parked.wait(), 5)
    b = asyncio.ensure_future(_one("race-b"))
    for _ in range(20):
        await asyncio.sleep(0)
    gate.set()
    preps = await asyncio.gather(a, b)
    for rid in ("race-a", "race-b"):
        reset_loop_state(CONVERSATION_ID, rid)
    assert [p.wire_config.max_output_tokens for p in preps] == [2250, 2250]
    assert _snapshot(stored) == before


@pytest.mark.asyncio
async def test_the_retrys_reasoning_off_survives_an_overload_on_its_send(monkeypatch) -> None:
    """CGU-10 IMG7 #5: ``send_once`` cleared the one-call settings BEFORE it sent, so a 529 on the
    empty-reply retry's send lost them and the next attempt went out with reasoning on. They are
    spent only when the provider answered."""
    from matrx_ai.orchestrator import send_once as send_once_mod

    class _Overloaded(Exception):
        pass

    class _Client:
        def __init__(self) -> None:
            self.efforts: list[Any] = []

        async def execute(self, request: Any) -> Any:
            self.efforts.append(request.config.reasoning_effort)
            if len(self.efforts) == 1:
                raise _Overloaded("529 overloaded")
            return SimpleNamespace(messages=[], finish_reason="stop")

    monkeypatch.setattr("matrx_ai.mandate_taps.observe_first_send", lambda *_a, **_k: None)

    async def _warm() -> None:
        return None

    monkeypatch.setattr("matrx_ai.processing.blocks.saved_blocks.warm_kind_registry", _warm)
    stored = _stored("claude-haiku-5-5", effort="low", budget=None)
    before = _snapshot(stored)
    request = SimpleNamespace(
        config=stored, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, organization_id=None
    )
    state = ExecutionState()
    state.one_call_settings = dict(REASONING_OFF)
    client = _Client()
    with pytest.raises(_Overloaded):
        await send_once_mod.send_once(client, request, state=state, iteration=1)
    assert state.one_call_settings == REASONING_OFF, "an unanswered send spent the retry's setting"
    await send_once_mod.send_once(client, request, state=state, iteration=1)  # the overload retry
    await send_once_mod.send_once(client, request, state=state, iteration=2)  # the next round
    assert client.efforts == ["none", "none", "low"]
    assert state.one_call_settings is None
    assert _snapshot(stored) == before


@pytest.mark.asyncio
async def test_a_nested_send_on_the_same_config_is_refused_loudly_never_hangs(monkeypatch) -> None:
    """CGU-10 IMG7 #6 (attack A3): with the boundary's lock held, a second ``prepare_for_send`` on the same
    config never returned. A stage hook that runs a model on its parent's config now gets a loud
    ``NestedSendError`` — in the same task and in a task it starts — and the stored config is untouched."""
    import asyncio

    from matrx_ai.config import send_boundary
    from matrx_ai.config.send_boundary import NestedSendError

    stored = _stored("claude-haiku-5-5", effort=None, budget=None)
    before = _snapshot(stored)
    seen: list[str] = []
    real_policy = send_boundary._resolve_org_trim_policy

    async def _nested_hook(prep: Any, organization_id: Any) -> Any:  # runs inside the outer boundary
        for where in ("same-task", "child-task"):
            call = prepare_for_send(
                stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id="nested", iteration=1
            )
            try:
                if where == "same-task":
                    await asyncio.wait_for(call, 2)
                else:
                    await asyncio.wait_for(asyncio.ensure_future(call), 2)
            except NestedSendError:
                seen.append(where)
        return await real_policy(prep, organization_id)

    monkeypatch.setattr(send_boundary, "_resolve_org_trim_policy", _nested_hook)
    reset_loop_state(CONVERSATION_ID, "nested")
    prep = await asyncio.wait_for(
        prepare_for_send(stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=1),
        5,
    )
    reset_loop_state(CONVERSATION_ID, "nested")
    assert seen == ["same-task", "child-task"]
    assert prep.wire_config is not None
    assert _snapshot(stored) == before
    # Released: the next send on the same config runs normally.
    monkeypatch.setattr(send_boundary, "_resolve_org_trim_policy", real_policy)
    await asyncio.wait_for(
        prepare_for_send(stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=2),
        5,
    )


@pytest.mark.asyncio
async def test_two_chats_never_wait_on_each_other(monkeypatch) -> None:
    """Survivor N12 (IMG7): the lock is PER CONFIG. One lock for every config would serialize every chat
    on the server behind whichever send is slowest; send B (another chat) must finish while A is parked."""
    import asyncio

    from matrx_ai.config import send_boundary

    gate = asyncio.Event()
    parked = asyncio.Event()
    real_policy = send_boundary._resolve_org_trim_policy
    first = True

    async def _hold_first(prep: Any, organization_id: Any) -> Any:
        nonlocal first
        if first:
            first = False
            parked.set()
            await gate.wait()
        return await real_policy(prep, organization_id)

    monkeypatch.setattr(send_boundary, "_resolve_org_trim_policy", _hold_first)
    chat_a = _stored("claude-haiku-5-5", effort=None, budget=None)
    chat_b = _stored("claude-haiku-5-5", effort=None, budget=None)
    for rid in ("chat-a", "chat-b"):
        reset_loop_state(CONVERSATION_ID, rid)
    a = asyncio.ensure_future(
        prepare_for_send(chat_a, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id="chat-a", iteration=1)
    )
    await asyncio.wait_for(parked.wait(), 5)
    try:
        await asyncio.wait_for(
            prepare_for_send(chat_b, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id="chat-b", iteration=1),
            2,
        )
    finally:
        gate.set()
        await a
        for rid in ("chat-a", "chat-b"):
            reset_loop_state(CONVERSATION_ID, rid)
