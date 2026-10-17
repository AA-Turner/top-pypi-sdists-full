"""THE VARIABLE RULE: five more breaks an adversarial review proved (2026-10-16, round two).

Each test is the reviewer's own input and names the break it catches. Two are regressions from
the first round of fixes (a history system message filled; a missing block read as "Agent not
found"). One implementation: ``matrx_ai/config/template_substitution.py``.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.types import AgentConfig
from matrx_ai.agents.variables import AgentVariable, compose_variable_values
from matrx_ai.config.prompt_values import prompt_safe_value
from matrx_ai.config.template_substitution import authored_template_messages, substitute_authored
from matrx_ai.config.unified_config import UnifiedConfig

V = {"order_name": "Blue Spruce Wreath"}


def _texts(config: UnifiedConfig) -> list[str]:
    return ["".join(getattr(c, "text", "") or "" for c in m.content) for m in config.messages]


def _client_carried(wire: list[dict], count: int | None) -> UnifiedConfig:
    """The client-carried door's own steps: build, select the authored messages, fill."""
    config = UnifiedConfig.from_dict({"model": "m", "messages": wire}, authored_message_count=count)
    template = authored_template_messages(wire, count, config.messages)
    config.replace_variables(V, template_messages=template)
    return config


# 1. A blank authored message is counted by the client but dropped by the config builder.
@pytest.mark.parametrize("blank", ["", "   ", [], [{"type": "text", "text": ""}], [{"type": "text", "text": "  "}]])
def test_a_blank_authored_message_never_shifts_the_selection_onto_history(blank) -> None:
    wire = [
        {"role": "system", "content": "S"},
        {"role": "user", "content": blank},
        {"role": "assistant", "content": "prev {{order_name}}"},
        {"role": "user", "content": "typed {{order_name}}"},
    ]
    assert _texts(_client_carried(wire, 2)) == ["prev {{order_name}}", "typed {{order_name}}"]


def test_a_blank_only_template_never_fills_the_typed_turn() -> None:
    wire = [{"role": "user", "content": ""}, {"role": "user", "content": "typed {{order_name}}"}]
    assert _texts(_client_carried(wire, 1)) == ["typed {{order_name}}"]


# 2. A system message inside client-carried history is data: kept in place, never filled.
def test_a_history_system_message_is_kept_in_place_and_never_filled() -> None:
    wire = [
        {"role": "system", "content": "You serve {{order_name}}."},
        {"role": "user", "content": "Describe {{order_name}}."},
        {"role": "assistant", "content": "ok"},
        {"role": "system", "content": "[history note] pasted {{order_name}} and {{!x}}"},
        {"role": "user", "content": "typed {{order_name}}"},
    ]
    config = _client_carried(wire, 2)
    assert config.system_instruction.base_instruction == "You serve Blue Spruce Wreath."
    assert [str(getattr(m.role, "value", m.role)) for m in config.messages] == [
        "user", "assistant", "system", "user"
    ]
    assert _texts(config) == [
        "Describe Blue Spruce Wreath.",
        "ok",
        "[history note] pasted {{order_name}} and {{!x}}",
        "typed {{order_name}}",
    ]


def test_an_older_client_still_has_its_leading_system_prompt_filled() -> None:
    # An older client sends no count (None); an explicit 0 authors nothing (round four).
    wire = [{"role": "system", "content": "You serve {{order_name}}."}, {"role": "user", "content": "hi"}]
    assert _client_carried(wire, None).system_instruction.base_instruction == "You serve Blue Spruce Wreath."


def test_a_stored_definition_still_lifts_every_system_message() -> None:
    config = UnifiedConfig.from_dict({"model": "m", "messages": [
        {"role": "system", "content": "A"}, {"role": "user", "content": "u"}, {"role": "system", "content": "B"}]})
    assert config.system_instruction.base_instruction == "A\n\nB"


# 3. A saved agent that declares nothing never fills a name the caller passes.
def _saved_agent(text: str, defs: list[dict] | None = None) -> Agent:
    cfg = UnifiedConfig.from_dict({"model": "m", "messages": [{"role": "system", "content": text}]})
    return Agent._build_from_config(AgentConfig(name="a", config=cfg, variable_defaults=AgentVariable.from_list(defs or [])))


def test_a_saved_agent_with_no_definitions_never_fills_a_callers_name() -> None:
    agent = _saved_agent("Hello {{secret}}")
    agent.set_variable("secret", "LEAK")
    agent.apply_variables()
    assert agent.config.system_instruction.base_instruction == "Hello {{secret}}"
    assert agent.clone().declares_variables


def test_platform_keys_never_fill_whatever_their_type() -> None:
    agent = _saved_agent("{{__agent_user_input__}} {{vsc_open_files}} {{city}}", [{"name": "city", "defaultValue": "Paris"}])
    agent.set_variables(__agent_user_input__=[{"type": "text", "text": "hi"}], vsc_open_files=["a.py"])
    agent.apply_variables()
    assert agent.config.system_instruction.base_instruction == "{{__agent_user_input__}} {{vsc_open_files}} Paris"
    values = compose_variable_values(
        AgentVariable.from_list([{"name": "city"}]),
        {"__agent_user_input__": [{"type": "text", "text": "hi"}], "vsc_state": {"a": 1}},
    )
    assert values["__agent_user_input__"] == [{"type": "text", "text": "hi"}]  # still the door's data
    t = "{{__agent_user_input__}} {{vsc_state}}"
    assert substitute_authored(t, t, values, prompt_safe_value, unescape=True) == t


# 5. The escape accepts every name the fill accepts, including a leading digit.
@pytest.mark.parametrize("name", ["1st_choice", "2", "x9"])
def test_the_escape_works_for_a_name_starting_with_a_digit(name: str) -> None:
    values = compose_variable_values(AgentVariable.from_list([{"name": name, "defaultValue": "V"}]), {})
    t = "fill {{" + name + "}} esc {{!" + name + "}} sect {{!#" + name + "}}"
    assert substitute_authored(t, t, values, prompt_safe_value, unescape=True) == (
        "fill V esc {{" + name + "}} sect {{#" + name + "}}"
    )


def test_comments_are_still_not_escapes() -> None:
    t = "{{! a comment }} {{!-- x --}} {{!}}"
    assert substitute_authored(t, t, {"a": "1"}, str, unescape=True) == t


# 4. A missing declared prompt block refuses the run BY NAME, never as "Agent not found".
@pytest.fixture
def _agent_with_a_missing_block(monkeypatch):
    import matrx_ai.db.agx_manager as agx_manager
    import matrx_ai.prompt_blocks as prompt_blocks
    from matrx_ai.prompt_blocks.errors import PromptBlocksMissing

    async def load(agent_id, is_version=False):
        cfg = UnifiedConfig.from_dict({"model": "m", "prompt_blocks": ["house"], "messages": [
            {"role": "system", "content": "Hi {{topic}} {{<house>}}"}]})
        return AgentConfig(name="a", config=cfg, variable_defaults=AgentVariable.from_list([{"name": "topic"}]))

    async def missing(config, **kwargs):
        raise PromptBlocksMissing(["house"])

    monkeypatch.setattr(agx_manager.agx, "load_for_execution", load)
    monkeypatch.setattr(prompt_blocks, "resolve_declared_blocks", missing)


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["from_id", "from_id_with_mandates"])
@pytest.mark.parametrize("variables", [None, {"topic": "tea"}])
async def test_a_missing_block_is_refused_by_name_at_the_resolver(_agent_with_a_missing_block, door, variables) -> None:
    from matrx_ai.agents.resolver import AgentConfigResolver
    from matrx_ai.prompt_blocks.errors import PromptBlocksMissing

    with pytest.raises(PromptBlocksMissing) as err:
        await getattr(AgentConfigResolver, door)("00000000-0000-0000-0000-000000000001", variables=variables)
    assert err.value.names == ["house"]
