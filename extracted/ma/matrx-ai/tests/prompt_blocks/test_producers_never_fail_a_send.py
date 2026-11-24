"""NEVER-FAIL (Arman, 2026-11-13): an extracted producer that raises behaves exactly as the old injector
did on that error — the same guard, the same logging — and never fails a send the old code did not fail.

- ``conversation_instructions``: the old injector ran inside ``send_boundary._run_step``; a raise was
  announced (ERROR log) and the step skipped. The producer runs inside the same step: the send proceeds,
  the block is absent, the failure is logged.
- ``kind_directives``: ``SystemInstruction.__str__`` never guarded it (pure string formatting over the
  agent's action names); the producer is total over any list of names, so it cannot add a failure.
"""

from __future__ import annotations

import logging

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    prompt_block_producers,
)
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.instructions.core import SystemInstruction, render_kind_directives


def _config() -> UnifiedConfig:
    config = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]
        ),
    )
    config.system_instruction = "You are the desk."
    config.conversation_instructions = "Answer in French."
    return config


@pytest.mark.asyncio
async def test_a_raising_conversation_instructions_producer_never_fails_the_send(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def _boom(_config: object) -> str:
        raise RuntimeError("producer exploded")

    monkeypatch.setattr(prompt_block_producers, "produce_conversation_instructions", _boom)
    config = _config()
    with caplog.at_level(logging.ERROR, logger="matrx_ai.config.send_boundary"):
        prep = await prepare_for_send(
            config, stage=STAGE_LOOP, conversation_id="c-nf", request_id="r", policy=TrimPolicy()
        )
    wire = prep.wire_config if prep.wire_config is not None else config
    assert "Answer in French." not in str(getattr(wire, "system_instruction", ""))
    assert "conversation_instructions" not in prep.steps
    assert any(
        "conversation_instructions" in r.getMessage() and "failed (ignored)" in r.getMessage()
        for r in caplog.records
    )


@pytest.mark.asyncio
async def test_the_producer_feeds_the_send_when_it_works() -> None:
    """Green twin of the test above: the same send carries the block when the producer returns it."""
    config = _config()
    prep = await prepare_for_send(
        config, stage=STAGE_LOOP, conversation_id="c-nf2", request_id="r", policy=TrimPolicy()
    )
    assert "conversation_instructions" in prep.steps
    assert "Answer in French." in str(prep.wire_config.system_instruction)


@pytest.mark.parametrize("names", [[], ["a"], ["a", "b c", "{weird}", "ünïcode"]])
def test_the_kind_directives_producer_is_total_and_is_what_the_system_renders(
    names: list[str],
) -> None:
    text = render_kind_directives(names)
    assert text.startswith("## Available Kind Directives")
    if names:
        si = SystemInstruction(base_instruction="X", include_date=False, action_types=names)
        assert text in str(si)


@pytest.mark.asyncio
async def test_a_raising_live_date_producer_never_fails_the_send(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """The old ``_announce_live_date`` ran inside ``_run_step("announce_live_date")``; so does its producer."""
    from matrx_ai.config.send_boundary import STAGE_RESOLVE

    def _boom(*_a: object, **_k: object) -> str:
        raise RuntimeError("producer exploded")

    monkeypatch.setattr(prompt_block_producers, "produce_live_date", _boom)
    config = _config()
    config.system_instruction = SystemInstruction(
        base_instruction="X", include_date=True, date_anchor="2026-11-01"
    )
    with caplog.at_level(logging.ERROR, logger="matrx_ai.config.send_boundary"):
        prep = await prepare_for_send(
            config,
            stage=STAGE_RESOLVE,
            conversation_id="c-nf3",
            request_id="r",
            policy=TrimPolicy(),
        )
    assert "announce_live_date" not in prep.steps
    assert "live_date" not in config.messages.turn_context_blocks()
    assert any(
        "announce_live_date" in r.getMessage() and "failed (ignored)" in r.getMessage()
        for r in caplog.records
    )
