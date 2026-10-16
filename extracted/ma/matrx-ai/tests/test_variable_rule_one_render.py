"""THE VARIABLE RULE — one render, one composition, one meaning of "empty" (WEAKNESSES W-01..W-22).

Exact strings only. Each test names the break that turns it red:
  W-01  a declared variable with no value became the word "None" in the SYSTEM prompt;
  W-02  a list/dict entered the system prompt as Python repr while messages got JSON;
  W-06  a toggle switched off (its off label) or ``False`` kept a ``{{#x}}`` section;
  W-03  the programmatic door and the route doors composed values differently;
  W-07  an agent with no variables skipped the ``{{!x}}`` escape;
  W-13  ``{{ name }}`` with spaces is NOT a declared slot — it stays exactly as written.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable, compose_variable_values
from matrx_ai.config.unified_config import UnifiedConfig

AUTHORED = "Name:[{{name}}] Tags:[{{tags}}] Meta:[{{meta}}]"


def _config(text: str) -> UnifiedConfig:
    return UnifiedConfig.from_dict(
        {
            "model": "claude-opus-5-5",
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": text}]},
                {"role": "user", "content": [{"type": "text", "text": text}]},
            ],
        }
    )


def _system_and_user(config: UnifiedConfig) -> tuple[str, str]:
    system = config.system_instruction.base_instruction
    user = config.messages[0].content[0].text
    return system, user


def test_w01_none_is_empty_in_the_system_prompt_too() -> None:
    config = _config("Hello [{{name}}].")
    config.replace_variables({"name": None})
    assert _system_and_user(config) == ("Hello [].", "Hello [].")


def test_w02_one_render_for_system_and_messages() -> None:
    config = _config(AUTHORED)
    config.replace_variables({"name": "Ada", "tags": ["red", "blue"], "meta": {"k": 1}})
    expected = 'Name:[Ada] Tags:[["red", "blue"]] Meta:[{"k": 1}]'
    assert _system_and_user(config) == (expected, expected)


SECTION = "A{{#flag}} FLAG ON{{/flag}}{{^flag}} FLAG OFF{{/flag}} B"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (False, "A FLAG OFF B"),
        (None, "A FLAG OFF B"),
        ("  ", "A FLAG OFF B"),
        ([], "A FLAG OFF B"),
        ({}, "A FLAG OFF B"),
        (True, "A FLAG ON B"),
        (0, "A FLAG ON B"),
        ("false", "A FLAG ON B"),
        ("No", "A FLAG ON B"),
    ],
)
def test_w06_empty_is_decided_once(value, expected) -> None:
    config = _config(SECTION)
    config.replace_variables({"flag": value})
    assert _system_and_user(config) == (expected, expected)


def _toggle(labels: list[str] | None = None) -> dict[str, AgentVariable]:
    cc: dict = {"type": "toggle"}
    if labels:
        cc["toggleValues"] = labels
    return {"flag": AgentVariable(name="flag", default_value=None, custom_component=cc)}


@pytest.mark.parametrize(
    ("labels", "sent", "expected"),
    [
        (None, "No", "A FLAG OFF B | No"),
        (None, "Yes", "A FLAG ON B | Yes"),
        (["Off", "On"], "Off", "A FLAG OFF B | Off"),
        (["Off", "On"], "On", "A FLAG ON B | On"),
        (["Off", "On"], "No", "A FLAG ON B | No"),
    ],
)
def test_w06_a_toggle_off_label_empties_its_section_but_still_fills_its_slot(
    labels, sent, expected
) -> None:
    values = compose_variable_values(_toggle(labels), {"flag": sent})
    config = _config(SECTION + " | {{flag}}")
    config.replace_variables(values)
    assert _system_and_user(config) == (expected, expected)


DEFINITIONS = {
    "a": AgentVariable(name="a", default_value="DEF-A"),
    "b": AgentVariable(name="b", default_value=None),
    "c": AgentVariable(name="c", default_value=["x", "y"]),
    "d": AgentVariable(name="d", default_value="DEF-D"),
}
DOORS_AUTHORED = "a=[{{a}}] b=[{{b}}] c=[{{c}}] d=[{{d}}] e=[{{e}}]"


@pytest.mark.parametrize(
    ("client", "expected"),
    [
        ({}, 'a=[DEF-A] b=[] c=[["x", "y"]] d=[DEF-D] e=[{{e}}]'),
        ({"a": None, "b": None, "c": [], "d": ""}, 'a=[DEF-A] b=[] c=[["x", "y"]] d=[DEF-D] e=[{{e}}]'),
        ({"a": "CLIENT", "b": "B", "d": "  "}, 'a=[CLIENT] b=[B] c=[["x", "y"]] d=[DEF-D] e=[{{e}}]'),
    ],
)
def test_w03_programmatic_and_route_doors_compose_identically(client, expected) -> None:
    # Programmatic door (Agent.execute / run_one_agent / mandates / agent-as-tool).
    agent = Agent(config=_config(DOORS_AUTHORED), variable_defaults=dict(DEFINITIONS))
    agent.set_variables(**client)
    agent.apply_variables()
    # Route doors (chat / agent route / manual): compose then substitute.
    routed = _config(DOORS_AUTHORED)
    routed.replace_variables(compose_variable_values(DEFINITIONS, client))
    assert _system_and_user(agent.config) == (expected, expected)
    assert _system_and_user(routed) == (expected, expected)


def test_w07_an_agent_with_no_variables_still_turns_the_escape_into_braces() -> None:
    agent = Agent(config=_config("Write {{!name}} and {{other}}."))
    agent.apply_variables()
    assert _system_and_user(agent.config) == ("Write {{name}} and {{other}}.",) * 2


def test_w13_a_spaced_token_is_not_a_declared_slot() -> None:
    config = _config("Hi {{ name }} and {{name}}.")
    config.replace_variables(compose_variable_values({"name": AgentVariable(name="name")}, {"name": "Ada"}))
    assert _system_and_user(config) == ("Hi {{ name }} and Ada.",) * 2
