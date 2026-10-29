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
