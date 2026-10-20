"""Required agent inputs: refused before any model call when enforcement is on; unchanged when off.

Exercises the real ``Agent.apply_variables`` door (the one every programmatic door runs) with the
real composition ladder, so the test goes red if the check is removed, moved before the ladder
(a saved default would then wrongly refuse) or stops reading the host switch.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.required_variables import (
    RequiredVariablesMissing,
    configure_required_variable_enforcement,
    missing_required_variables,
)
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig


@pytest.fixture(autouse=True)
def _reset_switch() -> Iterator[None]:
    yield
    configure_required_variable_enforcement(None)


def _agent(variables: list[dict[str, Any]]) -> Agent:
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-opus-5-5",
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": "Topic {{topic}} tone {{tone}}"}]},
            ],
        }
    )
    return Agent(config=config, variable_defaults=AgentVariable.from_list(variables), name="Probe")


REQUIRED_TOPIC = [{"name": "topic", "required": True}, {"name": "tone", "defaultValue": "warm"}]


def test_on_refuses_a_missing_required_input_naming_it() -> None:
    configure_required_variable_enforcement(lambda: True)
    agent = _agent(REQUIRED_TOPIC)
    with pytest.raises(RequiredVariablesMissing) as caught:
        agent.apply_variables()
    assert caught.value.missing == ["topic"]
    assert caught.value.error_info.status_code == 422
    assert caught.value.error_info.details["missing"] == ["topic"]
    assert agent._variables_applied is False  # nothing was filled, nothing can be sent


def test_on_blank_text_is_missing_too() -> None:
    configure_required_variable_enforcement(lambda: True)
    agent = _agent(REQUIRED_TOPIC).set_variables(topic="   ")
    with pytest.raises(RequiredVariablesMissing):
        agent.apply_variables()


def test_on_supplied_value_runs() -> None:
    configure_required_variable_enforcement(lambda: True)
    agent = _agent(REQUIRED_TOPIC).set_variables(topic="tea")
    agent.apply_variables()
    assert agent.config.system_instruction.base_instruction.startswith("Topic tea tone warm")


def test_on_a_saved_default_satisfies_required() -> None:
    configure_required_variable_enforcement(lambda: True)
    agent = _agent([{"name": "topic", "required": True, "defaultValue": "coffee"}, {"name": "tone"}])
    agent.apply_variables()
    assert agent.config.system_instruction.base_instruction.startswith("Topic coffee")


def test_off_a_missing_required_input_still_runs_as_before() -> None:
    configure_required_variable_enforcement(lambda: False)
    agent = _agent(REQUIRED_TOPIC)
    agent.apply_variables()
    assert agent.config.system_instruction.base_instruction.startswith("Topic  tone warm")


def test_unwired_is_off() -> None:
    configure_required_variable_enforcement(None)
    _agent(REQUIRED_TOPIC).apply_variables()


def test_unreadable_switch_falls_to_off() -> None:
    def broken() -> bool:
        raise RuntimeError("not primed")

    configure_required_variable_enforcement(broken)
    _agent(REQUIRED_TOPIC).apply_variables()


def test_missing_reads_dict_and_model_definitions() -> None:
    defs = {"a": {"required": True}, "b": AgentVariable(name="b", required=True), "c": {"required": False}}
    assert missing_required_variables(defs, {"a": [], "b": None, "c": ""}) == ["a", "b"]
    assert missing_required_variables(defs, {"a": ["x"], "b": False}) == []


def test_bound_variables_are_never_a_caller_requirement() -> None:
    """Mirrors the client selector: scope-bound and merge-field-bound vars are server-filled."""
    defs = {
        "scoped": {"required": True, "binding": {"itemKey": "brand_name", "onMissing": "empty"}},
        "merged": {"required": True, "binding": {"kind": "merge_field", "source": "x"}},
        "plain": {"required": True, "binding": None},
    }
    assert missing_required_variables(defs, {}) == ["plain"]


def test_a_pinned_version_run_is_not_enforced() -> None:
    configure_required_variable_enforcement(lambda: True)
    agent = _agent(REQUIRED_TOPIC)
    agent.source_is_version = True
    agent.apply_variables()  # pinned: skipped (announced), runs as before
