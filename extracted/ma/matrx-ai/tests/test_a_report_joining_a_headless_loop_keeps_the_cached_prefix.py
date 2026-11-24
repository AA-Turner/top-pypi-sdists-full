"""FORCING GUARD — a server notice joining a HEADLESS loop never moves the turn's platform block.

Live (lane DR, 2026-11-15 04:46Z): ``prompt_cache_prefix_drift`` row a059058b, openai gpt-5-nano,
conversation 2ca35cd7. The run was headless: its only "person" turn was the agent's own opening
(``authored_by: host``, ``authored_reason: agent_opening`` — ``mark_unspoken_opening_turn``). Sends 1-3
carried ``developer, CTX(1,811 B), opening, …tool loop``. A helper's report then drained into the loop as a
host-authored notice (``drain_pending_injections`` → ``host_authored_user_turn(reason="injection:…")``) and
send 4 carried ``developer, opening, …tool loop, CTX', <task-notification>``: the block left input[1] and
every later item shifted, so the whole cached prefix was written again.

Cause: with no person-written turn, ``typed_text_last.turn_person_index`` fell back to the NEWEST
host-authored user message — the notice — so the send boundary treated the report as a new turn, re-froze the
block for it, and ``_replay_kept_turn_context`` would not put the kept block back on the opening turn (it skips
every host-authored message). The opening turn is a turn boundary (``change_claims`` already says so); a notice
is not.

The test runs the real send boundary + translator per chat wire and compares sends with the real
``cache_guard`` (the alarm that filed the live row).
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    host_authored_user_turn,
)
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.providers.cache_guard import compare_wire_prefix, wire_prefix
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are the routing desk. " * 40
BLOCK = "<active_context><organization id=\"o-1\">Workspace</organization></active_context>"
ROSTER_RUNNING = "<your_helpers>- lookup-1 · running 0s</your_helpers>"
ROSTER_DONE = "<your_helpers>- lookup-1 · finished 3s ago; report delivered above</your_helpers>"

WIRES = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]


def _send(module: str, cls: str, wire_format: str, config: UnifiedConfig, iteration: int) -> Any:
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile, iteration=iteration)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _headless_config() -> UnifiedConfig:
    opening = UnifiedMessage(role="user", content=[TextContent(text="Move 4471: routing line, please.")])
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[opening]))
    config.system_instruction = SYSTEM
    assert config.mark_unspoken_opening_turn(), "the opening turn must be stamped host-authored (agent_opening)"
    config.messages.attach_turn_context(BLOCK, slot="active_context")
    return config


def _tool_round(config: UnifiedConfig, n: int) -> None:
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id=f"c{n}", name="agent", arguments={"n": n})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=f"c{n}", name="agent", content="R " * 60)])
    )


@pytest.mark.parametrize(("module", "cls", "wire_format"), WIRES)
def test_a_report_joining_a_headless_loop_keeps_the_cached_prefix(module: str, cls: str, wire_format: str) -> None:
    config = _headless_config()
    sends = [_send(module, cls, wire_format, config, iteration=1)]
    _tool_round(config, 1)
    config.messages.attach_turn_context(ROSTER_RUNNING, slot="your_helpers")
    sends.append(_send(module, cls, wire_format, config, iteration=2))
    _tool_round(config, 2)
    sends.append(_send(module, cls, wire_format, config, iteration=3))
    # The helper's report drains into the SAME loop as a server notice, right after a tool result.
    config.messages.attach_turn_context(ROSTER_DONE, slot="your_helpers")
    config.messages.append(
        host_authored_user_turn("<task-notification>hub: Los Angeles</task-notification>", reason="injection:system_message")
    )
    sends.append(_send(module, cls, wire_format, config, iteration=4))

    for n in range(len(sends) - 1):
        prev, new = wire_prefix(sends[n]), wire_prefix(sends[n + 1])
        assert prev is not None and new is not None, "the cache guard cannot read this wire"
        drift = compare_wire_prefix(prev, new)
        changed = [c for c in drift.changed if not _only_blocks_appended(sends[n], sends[n + 1], c)]
        assert not changed, f"{wire_format}: send {n + 1} -> {n + 2} rewrote the cached prefix: {changed}"


def _only_blocks_appended(prev: Any, new: Any, label: str) -> bool:
    """Anthropic merges the notice into the tool-result turn before it: that message only GAINS blocks after its
    old ones (marks aside). A cache read at the old breakpoint still hits (block-level prefix), so this one shape
    is not drift for this guard; every other change is. (``cache_guard`` compares whole messages — noted in the
    DR report.)"""
    import re

    from matrx_ai.providers.cache_guard import _without_cache_marks

    found = re.match(r"messages\[(\d+)\] \(user\) changed", label)
    if not found or not isinstance(prev, dict) or not isinstance(new, dict):
        return False
    i = int(found.group(1))
    old_blocks = _without_cache_marks(prev["messages"][i]["content"])
    new_blocks = _without_cache_marks(new["messages"][i]["content"])
    return isinstance(old_blocks, list) and len(new_blocks) > len(old_blocks) and new_blocks[: len(old_blocks)] == old_blocks


def test_the_opening_turn_stands_in_for_the_person_turn_over_a_later_notice() -> None:
    """The seam itself: with no person-written turn, the turn the loop answers is the opening, never a notice."""
    from matrx_ai.config.typed_text_last import turn_person_index

    config = _headless_config()
    _tool_round(config, 1)
    config.messages.append(host_authored_user_turn("<task-notification>x</task-notification>", reason="injection:x"))
    assert turn_person_index(list(config.messages)) == 0
