"""A run that holds a tool family is handed that family's briefing, staged by the send boundary alone.

Arman (custom-data VISION, the agent paragraph): agents "are just as confused as me ... if we don't
have a way to generate a concise, really good schema for them". The first consumer is the records
data index: every run holding a records tool gets the short list of tables it can open. The briefing
is prompt text added per send, so it has ONE path: the per-turn context channel, staged inside
``prepare_for_send`` (``_stage_tool_briefings``), whose first send of a turn freezes the block. A
source whose answer changes mid-turn never rewrites what a provider already cached.

RED before: ``matrx_ai.config.tool_briefings`` does not exist and no send carries a briefing.
"""

from __future__ import annotations

from copy import copy
from types import SimpleNamespace

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai.config import tool_briefings
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.tool_briefings import (
    register_tool_briefing,
    stage_tool_briefings,
    tool_names_of,
)

SLOT = "data_index"
INDEX = '<data_index tables="2">\n- Clients (12)\n- Jobs (340)\n</data_index>'


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.setattr(tool_briefings, "_BRIEFINGS", {})
    monkeypatch.setattr(tool_briefings, "_MEMO", type(tool_briefings._MEMO)())


def _config(tools=("records_read",)):
    return SimpleNamespace(messages=MessageList(), tools=list(tools), dynamic_tools=None, custom_tools=[])


async def test_a_run_holding_any_of_the_tools_gets_the_block_in_its_own_slot():
    async def source(ctx):
        return INDEX

    register_tool_briefing(SLOT, {"records", "records_read"}, source)
    config = _config()
    staged, failed = await stage_tool_briefings(config, None)
    assert (staged, failed) == ([SLOT], [])
    assert config.messages.turn_context_blocks() == {SLOT: INDEX}
    # Never a message: nothing the history persists, and the person's turn is untouched.
    assert len(config.messages) == 0


async def test_a_run_without_the_tools_gets_nothing_and_a_stale_block_is_cleared():
    calls = []

    async def source(ctx):
        calls.append(ctx)
        return INDEX

    register_tool_briefing(SLOT, {"records"}, source)
    config = _config(tools=("web_search",))
    config.messages.attach_turn_context("stale", slot=SLOT)
    assert await stage_tool_briefings(config, None) == ([], [])
    assert config.messages.turn_context_blocks() == {} and calls == [], "the source is never asked for a run without the tools"


async def test_a_tool_found_mid_conversation_or_declared_as_an_object_counts():
    config = _config(tools=())
    config.dynamic_tools = ["records_write"]
    config.custom_tools = [SimpleNamespace(name="my_tool")]
    assert tool_names_of(config) == {"records_write", "my_tool"}


async def test_the_source_is_asked_once_per_turn_however_long_the_loop():
    asked = []

    async def source(ctx):
        asked.append(ctx.request_id)
        return f"index #{len(asked)}"

    register_tool_briefing(SLOT, {"records_read"}, source)
    config = _config()
    turn = SimpleNamespace(request_id="req-1")
    for _ in range(5):
        await stage_tool_briefings(config, turn)
    assert asked == ["req-1"] and config.messages.turn_context_blocks()[SLOT] == "index #1"
    # The next turn reads again: a table made between turns is on the next turn's index.
    await stage_tool_briefings(config, SimpleNamespace(request_id="req-2"))
    assert asked == ["req-1", "req-2"] and config.messages.turn_context_blocks()[SLOT] == "index #2"


async def test_a_failing_source_clears_its_slot_and_is_handed_back_never_raised():
    async def broken(ctx):
        raise RuntimeError("db down")

    async def fine(ctx):
        return "other briefing"

    register_tool_briefing(SLOT, {"records_read"}, broken)
    register_tool_briefing("other", {"records_read"}, fine)
    config = _config()
    config.messages.attach_turn_context("stale", slot=SLOT)
    staged, failed = await stage_tool_briefings(config, None)
    assert staged == ["other"] and [(slot, type(exc)) for slot, exc in failed] == [(SLOT, RuntimeError)]
    assert config.messages.turn_context_blocks() == {"other": "other briefing"}


def test_a_briefing_needs_a_slot_and_a_tool():
    async def source(ctx):
        return None

    with pytest.raises(ValueError):
        register_tool_briefing("", {"records"}, source)
    with pytest.raises(ValueError):
        register_tool_briefing(SLOT, set(), source)


def test_standalone_stages_nothing():
    assert tool_briefings.registered_tool_briefings() == {}


def test_the_send_boundary_is_where_it_is_staged_before_the_wire_is_built():
    from matrx_ai.config import send_boundary

    source = stable_source(send_boundary.prepare_for_send)
    loop_part = source.split("if stage == STAGE_LOOP:")[-1]
    assert "_stage_tool_briefings(" in loop_part
    assert loop_part.index("_stage_tool_briefings(") < loop_part.index("_build_wire(")


# ── on the wire: there once, and a cached prefix never changes under it ───────────────────────────


def _wire_config():
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.instructions.core import SystemInstruction

    return UnifiedConfig(
        model="claude-sonnet-5",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="How many open jobs do we have?")])],
        system_instruction=SystemInstruction(base_instruction="You keep the books."),
        tools=["records_read"],
    )


def _profile():
    from matrx_ai.testing.profile_factory import make_profile

    return make_profile(
        model_name="claude-sonnet-5",
        wire_format="anthropic_chat",
        capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"},
    )


@pytest.fixture
def known_model(monkeypatch):
    """The boundary orders her turn for the provider it sends to; no catalog here, so it is told."""
    from matrx_ai.config import send_boundary

    async def profile(config, **_kw):
        return _profile()

    monkeypatch.setattr(send_boundary, "_send_profile", profile)


def _anthropic(prep, config):
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    # The briefing is already staged; the tool declarations themselves need a loaded registry, which
    # is not what this test is about, so the wire is rendered without them.
    rendered = copy(prep.wire_config if prep.wire_config is not None else config)
    rendered.tools = []
    return AnthropicTranslator().to_anthropic(rendered, _profile())


def _texts(message: dict) -> list[str]:
    """A wire message's text, without the cache marks (the rolling mark moves every send by design)."""
    content = message["content"]
    return [content] if isinstance(content, str) else [b.get("text", "") for b in content]


async def test_the_index_is_on_the_wire_once_and_her_turn_is_byte_stable_through_the_tool_loop(known_model):
    from matrx_ai.config.context_trim import TrimPolicy
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    answers = iter([INDEX, INDEX.replace("(340)", "(341)")])

    async def source(ctx):
        return next(answers)

    register_tool_briefing(SLOT, {"records", "records_read"}, source)
    config = _wire_config()
    first = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", iteration=1, policy=TrimPolicy())
    assert f"tool_briefing:{SLOT}" in first.steps
    wire_1 = _anthropic(first, config)
    assert str(wire_1).count("<data_index") == 1, wire_1
    her_turn_1 = _texts(wire_1["messages"][0])
    # Before her words, on her turn: where a per-turn block is cached with the turn.
    assert "<data_index" in her_turn_1[0] and her_turn_1[-1] == "How many open jobs do we have?"

    # The agent calls the tool; a row is added meanwhile, so the source would now answer 341.
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="records_read", arguments={"action": "schema"})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c1", call_id="c1", name="records_read", content="{}")])
    )
    second = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", iteration=2, policy=TrimPolicy())
    wire_2 = _anthropic(second, config)
    # THE CACHE GATE'S PROPERTY: what the first send placed on her turn is what every later send places.
    assert _texts(wire_2["messages"][0]) == her_turn_1
    assert "(340)" in str(wire_2["messages"][0]) and "(341)" not in str(wire_2["messages"][0])
    assert [b["text"] for b in wire_2["system"]] == [b["text"] for b in wire_1["system"]]
    # What changed since rides AFTER the cache line, as the current copy; nothing before it moved.
    # (No carried request here, so the source was asked again; a real turn asks once and has no tail copy.)
    assert "(341)" in str(wire_2["messages"][-1]) and "(341)" not in str(wire_2["messages"][:-1])


async def test_a_run_without_a_records_tool_sends_no_index(known_model):
    from matrx_ai.config.context_trim import TrimPolicy
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send

    async def source(ctx):
        return INDEX

    register_tool_briefing(SLOT, {"records", "records_read"}, source)
    config = _wire_config()
    config.tools = ["web_search"]
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-2", iteration=1, policy=TrimPolicy())
    assert not any(step.startswith("tool_briefing") for step in prep.steps)
    assert "<data_index" not in str(_anthropic(prep, config))
