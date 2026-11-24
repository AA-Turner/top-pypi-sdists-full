"""The person's saved memories and custom instructions reach a chat turn — and only when allowed (CGU-10).

ChatGPT's behaviour: saved memories and the two instruction boxes reach every new chat; a temporary
chat uses them only when the person opts in, and never saves a new one; our confidential (sealed)
chat never reads or writes them. The gate is ``person_context_decision`` on the carried AppContext;
the block rides the per-turn context channel, staged by the send boundary
(``matrx_ai/config/person_context.py``), never the cached system prefix.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage, person_context
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.person_context import (
    PERSON_CONTEXT_OPEN,
    PERSON_CONTEXT_SLOT,
    USE_PERSON_MEMORY_KEY,
    frame,
    person_context_decision,
)
from matrx_ai.config.platform_parts import platform_parts_in_request
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.instructions.core import SystemInstruction

_TOKENS: list[Any] = []


def _install(ctx: AppContext) -> None:
    _TOKENS.append(set_app_context(ctx))


def _clear() -> None:
    while _TOKENS:
        clear_app_context(_TOKENS.pop())


BLOCK = frame([("about_me", "I keep bees in Lisbon."), ("how_to_respond", "Answer in one sentence.")])


def _ctx(**kw: Any) -> AppContext:
    base: dict[str, Any] = {"emitter": None, "user_id": "person-1", "request_id": f"req-{id(kw)}-{len(kw)}"}
    base.update(kw)
    return AppContext(**base)


@pytest.mark.parametrize(
    ("fields", "allowed"),
    [
        ({}, True),  # a saved chat
        ({"metadata": {USE_PERSON_MEMORY_KEY: False}}, False),  # turned off for this turn
        ({"store": False}, False),  # temporary, no opt-in
        ({"store": False, "metadata": {USE_PERSON_MEMORY_KEY: True}}, True),  # temporary, opted in
        # confidential beats every opt-in
        ({"store": False, "sealed_conversation_id": "c-1", "metadata": {USE_PERSON_MEMORY_KEY: True}}, False),
        ({"system_run": True}, False),
        ({"is_internal_agent": True}, False),
        ({"parent_request_id": "parent-req"}, False),  # a child run is not the person's chat
        ({"user_id": ""}, False),
    ],
)
def test_the_gate(fields: dict[str, Any], allowed: bool) -> None:
    assert person_context_decision(_ctx(**fields))[0] is allowed


@pytest.fixture
def source():
    calls: list[str] = []

    async def read(ctx: Any) -> str | None:
        calls.append(str(ctx.user_id))
        return BLOCK

    person_context.set_person_context_source(read)
    reset_loop_state()
    yield calls
    person_context.set_person_context_source(None)
    reset_loop_state()
    _clear()


def _config() -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-sonnet-4-6",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="Hi")])]),
    )
    config.system_instruction = SystemInstruction.from_value("You are a helpful chat.")
    return config


async def _send(ctx: AppContext, config: UnifiedConfig) -> Any:
    token = set_app_context(ctx)
    try:
        return await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    finally:
        clear_app_context(token)


def _block(config: UnifiedConfig) -> str:
    return config.messages.turn_context_blocks().get(PERSON_CONTEXT_SLOT, "")


@pytest.mark.asyncio
async def test_a_saved_chat_carries_the_block_in_the_turn_context_never_the_system_prefix(source) -> None:
    ctx = _ctx(request_id="r-saved")
    config = _config()
    prep = await _send(ctx, config)
    assert "person_context" in prep.steps
    assert "I keep bees in Lisbon." in _block(config)
    assert "bees" not in (config.resolved_system_instruction or "")
    # A long tool loop reads the store once per turn.
    await _send(ctx, config)
    assert source == ["person-1"]


@pytest.mark.asyncio
async def test_a_temporary_chat_without_opt_in_never_reads_the_store(source) -> None:
    ctx = _ctx(request_id="r-temp", store=False)
    config = _config()
    prep = await _send(ctx, config)
    assert _block(config) == ""
    assert "person_context_withheld:temporary chat" in prep.steps
    assert source == []


@pytest.mark.asyncio
async def test_a_temporary_chat_that_opted_in_carries_it(source) -> None:
    ctx = _ctx(request_id="r-opt", store=False, metadata={USE_PERSON_MEMORY_KEY: True})
    config = _config()
    await _send(ctx, config)
    assert "Answer in one sentence." in _block(config)


@pytest.mark.asyncio
async def test_a_confidential_chat_never_reads_it_even_opted_in(source) -> None:
    ctx = _ctx(request_id="r-sealed", store=False, sealed_conversation_id="c-9", metadata={USE_PERSON_MEMORY_KEY: True})
    config = _config()
    await _send(ctx, config)
    assert _block(config) == "" and source == []


@pytest.mark.asyncio
async def test_a_failing_source_costs_the_block_never_the_send(source) -> None:
    async def broken(ctx: Any) -> str | None:
        raise RuntimeError("database down")

    person_context.set_person_context_source(broken)
    ctx = _ctx(request_id="r-broken")
    config = _config()
    prep = await _send(ctx, config)
    assert _block(config) == "" and "request_firewall" in prep.steps


def test_the_builder_finds_it_as_a_registered_platform_part() -> None:
    found = platform_parts_in_request({"system": "x " + BLOCK + " y"})
    assert [p["id"] for p in found] == ["person_context"]
    assert BLOCK.startswith(PERSON_CONTEXT_OPEN)
    assert frame([("about_me", "  ")]) == ""


@pytest.mark.asyncio
async def test_the_memory_tool_never_saves_from_a_temporary_chat_or_touches_a_confidential_one() -> None:
    from matrx_ai.tools.implementations.memory import person_memory_refusal

    try:
        _install(_ctx(store=False, metadata={USE_PERSON_MEMORY_KEY: True}))
        assert person_memory_refusal("store") and person_memory_refusal("forget")
        assert person_memory_refusal("recall") is None  # opted in: it may read
        _install(_ctx(store=False))
        assert person_memory_refusal("recall")
        _install(_ctx(store=False, sealed_conversation_id="c-1"))
        assert person_memory_refusal("search")
        _install(_ctx())
        assert person_memory_refusal("store") is None
    finally:
        _clear()
