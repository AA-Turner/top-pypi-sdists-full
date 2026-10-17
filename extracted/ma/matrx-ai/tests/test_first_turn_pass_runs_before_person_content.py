"""THE FIRST-TURN PASS RUNS BEFORE ANY PERSON CONTENT JOINS THE CONFIG.

Only the AUTHOR's declared ``{{name}}`` is filled, once, on the first turn, and the
pass always runs (escape, sections, prompt blocks) even with no values. The person's
data and typed input are never filled. Each test names the door that broke it:

  * the batch lane appended the turn content BEFORE batch_render ran the fill, so the
    person's data was filled and the authored user turn was lifted unfilled;
  * the block-mode start (``AgentConfigResolver.from_id``) only filled ``if variables:``,
    so with none sent raw ``{{name}}``, no defaults and raw ``{{<block>}}`` reached
    the model;
  * ``agent_call`` prepended borrowed history before ``execute`` ran the fill.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.types import AgentConfig
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig

MODEL = "claude-opus-5-5"
DATA = "Customer wrote {{!raw}} and {{topic}}"


def _defaults() -> dict[str, AgentVariable]:
    return AgentVariable.from_list([{"name": "topic", "defaultValue": "tea"}])


def _config(*, blocks: bool = False) -> UnifiedConfig:
    system = "You write about {{topic}}. Keep {{!topic}}."
    if blocks:
        system += " {{<house>}}"
    payload: dict[str, Any] = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system}]},
            {"role": "user", "content": [{"type": "text", "text": "Topic: {{topic}}"}]},
        ],
    }
    if blocks:
        payload["prompt_blocks"] = ["house"]
    return UnifiedConfig.from_dict(payload)


def _texts(config: UnifiedConfig) -> list[str]:
    return [
        getattr(block, "text", "") or ""
        for message in config.messages
        for block in (message.content or [])
    ]


def _assert_filled_once(config: UnifiedConfig) -> None:
    si = config.system_instruction
    assert si.base_instruction.startswith("You write about tea. Keep {{topic}}.")
    # The authored opening turn was filled; nothing authored reaches the model raw.
    assert "Topic: {{topic}}" not in (si.opening_turn or "")
    assert "Topic: {{topic}}" not in _texts(config)


@pytest.mark.asyncio
async def test_batch_order_person_data_is_never_filled() -> None:
    """batch_lane: set_user_input(turn_content), THEN batch_render runs the pass."""
    agent = Agent(config=_config(), variable_defaults=_defaults())
    agent.set_user_input(DATA)
    # What batch_render.render_agent_provider_request does next.
    if not agent._variables_applied:
        await agent.prepare_variables()
        agent.apply_variables()
    _assert_filled_once(agent.config)
    texts = _texts(agent.config)
    assert DATA in texts, texts
    assert "Topic: tea" in texts, texts


@pytest.mark.asyncio
async def test_run_first_turn_pass_then_input() -> None:
    agent = Agent(config=_config(), variable_defaults=_defaults())
    await agent.run_first_turn_pass()
    agent.set_user_input(DATA)
    _assert_filled_once(agent.config)
    assert DATA in _texts(agent.config)


def _patch_load(monkeypatch: pytest.MonkeyPatch, *, blocks: bool) -> None:
    from matrx_ai.db.agx_manager import agx

    async def _load(_agent_id: str, is_version: bool = False) -> AgentConfig:
        return AgentConfig(name="t", config=_config(blocks=blocks), variable_defaults=_defaults())

    monkeypatch.setattr(agx, "load_for_execution", _load)

    async def _resolve(config: UnifiedConfig, **_kw: Any) -> None:
        config.prompt_block_texts = {"house": "House rules."}

    import matrx_ai.prompt_blocks as prompt_blocks

    monkeypatch.setattr(prompt_blocks, "resolve_declared_blocks", _resolve)


@pytest.mark.asyncio
@pytest.mark.parametrize("variables", [None, {}])
async def test_resolver_door_with_no_values_runs_the_pass(
    monkeypatch: pytest.MonkeyPatch, variables: dict[str, Any] | None
) -> None:
    """Block-mode start: no values sent still fills defaults, escapes and blocks."""
    from matrx_ai.agents.resolver import AgentConfigResolver

    _patch_load(monkeypatch, blocks=True)
    config = await AgentConfigResolver.from_id("00000000-0000-0000-0000-000000000001", variables=variables)
    _assert_filled_once(config)
    assert "<house>\nHouse rules.\n</house>" in config.system_instruction.base_instruction
    # Then the person's typed input joins — it is never filled.
    config.append_or_extend_user_input(DATA)
    _assert_filled_once(config)
    assert DATA in _texts(config)


@pytest.mark.asyncio
async def test_resolver_with_mandates_door_runs_the_pass(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agents.resolver import AgentConfigResolver

    _patch_load(monkeypatch, blocks=False)
    config, _policies, _off = await AgentConfigResolver.from_id_with_mandates(
        "00000000-0000-0000-0000-000000000001"
    )
    _assert_filled_once(config)


def test_set_user_input_fills_before_appending_without_async_prepare() -> None:
    """The synchronous door still fills BEFORE the person's content joins."""
    agent = Agent(config=_config(), variable_defaults=_defaults())
    agent.set_user_input(DATA)
    assert agent._variables_applied
    _assert_filled_once(agent.config)
    assert DATA in _texts(agent.config)


def test_set_user_input_refuses_an_unresolved_block_instead_of_sending_it_raw() -> None:
    from matrx_ai.prompt_blocks.errors import PromptBlocksNotResolved

    agent = Agent(config=_config(blocks=True), variable_defaults=_defaults())
    with pytest.raises(PromptBlocksNotResolved):
        agent.set_user_input(DATA)
