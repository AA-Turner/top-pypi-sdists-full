"""The agent's helpers list rides every send, in the per-turn context channel, never persisted.

Arman, 2026-10-28: "at every turn, the agent is able to see exactly where all of its sub-agents
are at… it will not bloat context because we're not going to keep the old ones."
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import helper_roster
from matrx_ai.config.helper_roster import HELPER_ROSTER_SLOT, stage_helper_roster
from matrx_ai.config.message_config import MessageList


def _config():
    return SimpleNamespace(messages=MessageList())


async def test_the_block_is_staged_in_its_own_slot_and_replaced_each_send(monkeypatch):
    texts = iter(["<your_helpers>FIRST-ROSTER</your_helpers>", "<your_helpers>SECOND-ROSTER</your_helpers>"])

    async def source(cid, org):
        assert (cid, org) == ("c", "o")
        return next(texts)

    monkeypatch.setattr(helper_roster, "_SOURCE", source)
    config = _config()
    assert await stage_helper_roster(config, conversation_id="c", organization_id="o")
    assert await stage_helper_roster(config, conversation_id="c", organization_id="o")
    rendered = config.messages.render_turn_context() or ""
    assert "SECOND-ROSTER" in rendered and "FIRST-ROSTER" not in rendered
    # Never a message: nothing the history persists.
    assert len(config.messages) == 0


async def test_no_helpers_clears_the_slot(monkeypatch):
    async def source(cid, org):
        return None

    monkeypatch.setattr(helper_roster, "_SOURCE", source)
    config = _config()
    config.messages.attach_turn_context("stale", slot=HELPER_ROSTER_SLOT)
    assert not await stage_helper_roster(config, conversation_id="c", organization_id=None)
    assert "stale" not in (config.messages.render_turn_context() or "")


async def test_a_failing_source_never_leaves_a_stale_roster(monkeypatch):
    async def source(cid, org):
        raise RuntimeError("db down")

    monkeypatch.setattr(helper_roster, "_SOURCE", source)
    config = _config()
    config.messages.attach_turn_context("stale", slot=HELPER_ROSTER_SLOT)
    with pytest.raises(RuntimeError):
        await stage_helper_roster(config, conversation_id="c", organization_id=None)
    assert "stale" not in (config.messages.render_turn_context() or "")


async def test_standalone_has_no_roster(monkeypatch):
    monkeypatch.setattr(helper_roster, "_SOURCE", None)
    config = _config()
    assert not await stage_helper_roster(config, conversation_id="c", organization_id=None)


def test_the_send_boundary_stages_it_on_every_loop_send():
    import inspect

    from matrx_ai.config import send_boundary

    source = inspect.getsource(send_boundary.prepare_for_send)
    loop_part = source.split("if stage == STAGE_LOOP:")[-1]
    assert "_stage_helper_roster(" in loop_part


# ── on the wire: every send, exactly once (HL-PB-02 run 1, 2026-10-30) ─────────────────────────────
# The roster rode only the per-turn context channel, which a translator renders only on a send whose
# newest message is NOT a tool result (owner ruling 2026-10-18). So the send right after the agent
# started or stopped a helper — the moment it most needs the list — went out without it (live lead
# requests 49ad2f97 and 869bee96). These fail the day either kind of send loses it or carries it twice.

ROSTER = '<your_helpers source="platform">\n1 in all, 1 running\n- rye-card-b08e08 · running 3s\n</your_helpers>'


def _wire_config(*, newest_is_tool_result: bool, model: str = "claude-sonnet-5"):
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.instructions.core import SystemInstruction

    messages = [UnifiedMessage(role="user", content=[TextContent(text="Fetch the rye card in the background.")])]
    if newest_is_tool_result:
        messages += [
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="a1", name="agent", arguments={"agent_id": "x"})]),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="a1", call_id="a1", name="agent", content='{"status": "running"}')],
            ),
        ]
    return UnifiedConfig(
        model=model, messages=messages, system_instruction=SystemInstruction(base_instruction="You coordinate helpers.")
    )


def _profile(model: str, wire_format: str):
    from matrx_ai.testing.profile_factory import make_profile

    return make_profile(
        model_name=model,
        wire_format=wire_format,
        capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"},
    )


@pytest.mark.parametrize("newest_is_tool_result", [True, False])
async def test_the_anthropic_wire_carries_the_roster_once_on_every_send(monkeypatch, newest_is_tool_result):
    from matrx_ai.config.context_trim import TrimPolicy
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    async def source(cid, org):
        return ROSTER

    monkeypatch.setattr(helper_roster, "_SOURCE", source)
    config = _wire_config(newest_is_tool_result=newest_is_tool_result)
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    wire = AnthropicTranslator().to_anthropic(config, _profile("claude-sonnet-5", "anthropic_chat"))
    assert str(wire).count("<your_helpers") == 1, wire
    if newest_is_tool_result:
        # Its own host turn AFTER the tool result, never inside it (the 2026-10-18 ruling).
        assert "<your_helpers" not in str(wire["messages"][-2])


@pytest.mark.parametrize("newest_is_tool_result", [True, False])
async def test_the_openai_wire_carries_the_roster_once_on_every_send(monkeypatch, newest_is_tool_result):
    from matrx_ai.config.context_trim import TrimPolicy
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
    from matrx_ai.providers.openai.translator import OpenAITranslator

    async def source(cid, org):
        return ROSTER

    monkeypatch.setattr(helper_roster, "_SOURCE", source)
    config = _wire_config(newest_is_tool_result=newest_is_tool_result, model="gpt-5")
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    wire = OpenAITranslator().to_openai(config, _profile("gpt-5", "openai_responses"))
    assert str(wire).count("<your_helpers") == 1, wire
