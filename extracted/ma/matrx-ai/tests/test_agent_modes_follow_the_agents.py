"""An agent's modes reach the model on every call (Understanding v2, PLAN C4/C5).

The agent's ``understanding.modes`` ride the run config as ``agent_modes``; the conversation's mode is the
override ``agent_mode`` (a mode key; absent or unknown = the first mode). The send boundary appends the
``<agent_modes>`` block after the agent's own text on the WIRE copy only, on every call, so a switch inside a
tool loop shows on the next call.

Fails when: the block's text is not the contract's shape; the platform writes any words other than "Modes:"
and "Current mode:"; an agent without modes gets a block; the canonical (frozen) prompt changes; the mode or
the modes are lost on a restore; an old client's ``understanding_mode`` fails the turn; the loaded definition
drops its modes; a switch on the running config does not change the next call's text.
"""

from __future__ import annotations

import re
from types import SimpleNamespace

import pytest

from matrx_ai.client_host.agent_source import definition_from_row, definition_to_agent_config
from matrx_ai.config import UnifiedConfig
from matrx_ai.config.agent_modes import find_mode, render_block, running_modes_for
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send

AGENT = "You are a careful planner."


def _mode(key: str, name: str, description: str, instructions: str) -> dict[str, str]:
    return {"key": key, "name": name, "description": description, "instructions": instructions}


DISCOVERY = _mode("discovery", "Discovery", "learn first", "Ask; do not advise yet.")
ANSWER = _mode("answer", "Answer", "answer with your best", "Answer the person now.")
FIVE = [
    DISCOVERY,
    ANSWER,
    _mode("planning", "Planning", "work out the plan", "Plan it; do not act yet."),
    _mode("review", "Review", "check the work", "Read it back and mark what is missing."),
    _mode("wrap", "Wrap up", "close the conversation", "Summarize what was decided."),
]


def _config(modes: list[dict[str, str]] | None = None, mode: str | None = None) -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-haiku-4-5",
        system_instruction=AGENT,
        messages=[{"role": "user", "content": [{"type": "text", "text": "Help me plan."}]}],
    )
    config.agent_modes = modes
    config.agent_mode = mode
    return config


async def _wire_system(config: UnifiedConfig) -> str:
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="c1", request_id="r1", policy=TrimPolicy())
    wire = prep.wire_config if prep.wire_config is not None else config
    return wire.resolved_system_instruction or ""


# ── the block's text ─────────────────────────────────────────────────────────────────────────────


def test_one_mode() -> None:
    assert render_block([DISCOVERY], None) == (
        "<agent_modes>\n"
        "Modes:\n"
        "- Discovery — learn first\n"
        "Current mode: Discovery.\n"
        "Ask; do not advise yet.\n"
        "</agent_modes>"
    )


def test_two_modes_and_the_named_one_is_current() -> None:
    assert render_block([DISCOVERY, ANSWER], "answer") == (
        "<agent_modes>\n"
        "Modes:\n"
        "- Discovery — learn first\n"
        "- Answer — answer with your best\n"
        "Current mode: Answer.\n"
        "Answer the person now.\n"
        "</agent_modes>"
    )


def test_five_modes_in_menu_order() -> None:
    block = render_block(FIVE, "review") or ""
    assert block.splitlines()[1:7] == [
        "Modes:",
        "- Discovery — learn first",
        "- Answer — answer with your best",
        "- Planning — work out the plan",
        "- Review — check the work",
        "- Wrap up — close the conversation",
    ]
    assert "Current mode: Review." in block and "Read it back and mark what is missing." in block
    assert "Plan it" not in block, "only the current mode's instructions are sent"


def test_absent_or_unknown_mode_is_the_first() -> None:
    assert "Current mode: Discovery." in (render_block(FIVE, None) or "")
    assert "Current mode: Discovery." in (render_block(FIVE, "no-such-mode") or "")


def test_a_mode_without_a_description_is_its_name() -> None:
    bare = _mode("bare", "Bare", "", "Go.")
    assert render_block([bare], None) == "<agent_modes>\nModes:\n- Bare\nCurrent mode: Bare.\nGo.\n</agent_modes>"


def test_no_modes_no_block() -> None:
    assert render_block(None, "answer") is None
    assert render_block([], None) is None


@pytest.mark.parametrize("modes,mode", [([DISCOVERY], None), ([DISCOVERY, ANSWER], "answer"), (FIVE, "wrap")])
def test_the_platform_writes_only_the_two_headings(modes: list[dict[str, str]], mode: str | None) -> None:
    """Remove every maker-written value; what is left must be the tags, the two headings, the "- " list marker
    at the start of each mode line, and punctuation."""
    block = render_block(modes, mode) or ""
    rest = block
    for m in sorted(modes, key=lambda m: -len(m["instructions"] + m["description"] + m["name"])):
        for value in (m["instructions"], m["description"], m["name"]):
            rest = rest.replace(value, "")
    rest = rest.replace("<agent_modes>", "").replace("</agent_modes>", "")
    rest = rest.replace("Modes:", "").replace("Current mode:", "")
    rest = re.sub(r"(?m)^- ", "", rest)  # the list marker, allowed explicitly
    assert re.fullmatch(r"[\s.—]*", rest), f"platform text other than the headings: {rest!r}"


def test_a_mode_is_found_by_key_or_name_in_any_case() -> None:
    assert find_mode(FIVE, "WRAP") == FIVE[4]
    assert find_mode(FIVE, "wrap up") == FIVE[4]
    assert find_mode(FIVE, " Discovery ") == DISCOVERY
    assert find_mode(FIVE, "nothing") is None


# ── the send boundary ────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_it_reaches_the_wire_after_the_agents_text_and_never_the_stored_prompt() -> None:
    config = _config([DISCOVERY, ANSWER])
    text = await _wire_system(config)
    assert AGENT in text and text.endswith("</agent_modes>")
    assert text.index(AGENT) < text.index("<agent_modes>"), "the agent's own text comes first"
    assert "<agent_modes>" not in (config.resolved_system_instruction or "")
    assert all("agent_modes" not in str(m) for m in config.messages)


@pytest.mark.asyncio
async def test_an_agent_without_modes_sends_nothing_new() -> None:
    config = _config()
    assert "<agent_modes>" not in await _wire_system(config)
    assert config.agent_modes is None


@pytest.mark.asyncio
async def test_a_switch_on_the_running_config_changes_the_next_call() -> None:
    config = _config([DISCOVERY, ANSWER])
    assert "Current mode: Discovery." in await _wire_system(config)
    running = running_modes_for(config)
    assert running is not None and running.current == DISCOVERY
    running.switch("answer")
    second = await _wire_system(config)
    assert "Current mode: Answer." in second and "Answer the person now." in second
    assert running_modes_for(_config()) is None


# ── the setting and the agent's list travel ──────────────────────────────────────────────────────


def test_the_mode_and_the_modes_survive_a_restore_and_null_clears_the_mode() -> None:
    config = _config([DISCOVERY, ANSWER])
    config.apply_overrides(LLMParams(agent_mode="answer"))
    config.apply_overrides(LLMParams(temperature=0.2))
    stored = config.to_storage_dict()
    assert stored["config"]["agent_mode"] == "answer"
    restored = UnifiedConfig.from_dict(
        {"model": stored["model"], "system_instruction": stored["system_instruction"], **stored["config"], "messages": config.messages}
    )
    assert restored.agent_mode == "answer" and restored.agent_modes == [DISCOVERY, ANSWER]
    restored.apply_overrides(LLMParams.model_validate({"agent_mode": None}))
    assert restored.agent_mode is None
    assert "agent_mode" not in restored.to_storage_dict()["config"]


def test_an_old_clients_understanding_mode_is_dropped_not_refused() -> None:
    params = LLMParams.model_validate({"understanding_mode": "discovery", "temperature": 0.1})
    assert params.temperature == 0.1
    assert "understanding_mode" not in params.model_dump(exclude_none=True)
    with pytest.raises(Exception):
        LLMParams.model_validate({"agent_modez": "x"})


def test_the_loaded_definition_carries_its_modes_to_the_config() -> None:
    row = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        version=3,
        updated_at=None,
        name="Planner",
        model_id="claude-haiku-4-5",
        messages=[{"role": "system", "content": [{"type": "text", "text": AGENT}]}],
        understanding={"__kind": "understanding_set", "tables": [], "modes": [DISCOVERY, {"name": "no key"}, ANSWER]},
    )
    definition = definition_from_row(row, is_version=False)
    assert definition.modes == [DISCOVERY, ANSWER]
    assert "modes" not in definition.model_dump(), "in-process only: the portable shape is unchanged"
    config = definition_to_agent_config(definition).config
    assert config.agent_modes == [DISCOVERY, ANSWER]
    row.understanding = None
    assert definition_to_agent_config(definition_from_row(row, is_version=False)).config.agent_modes is None
