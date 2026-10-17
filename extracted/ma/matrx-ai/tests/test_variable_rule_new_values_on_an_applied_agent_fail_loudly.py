"""New values on an agent whose variables were already applied fail LOUDLY and are logged.

``Agent.with_variables()`` / ``set_variables()`` after ``apply_variables()`` (no ``force``) used
to store the values and then do nothing: the prompt kept the old fill, nothing said so. Owner
ruling (2026-10-16): raise a clear error and record it through the error-capture seam — never
silently ignore the values, never silently re-apply them. Values already applied are not new.
A deliberate refill keeps its doors: ``clone().with_variables(...)`` and
``set_variable(...).apply_variables(force=True)``.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.template_substitution import VariablesAlreadyAppliedError
from matrx_ai.config.unified_config import UnifiedConfig


def _agent() -> Agent:
    config = UnifiedConfig.from_dict(
        {"model": "m", "messages": [{"role": "system", "content": "Guide for {{city}}."}]}
    )
    return Agent(
        config=config,
        variable_defaults=AgentVariable.from_list([{"name": "city", "defaultValue": "Lima"}]),
    )


@pytest.fixture()
def captured(monkeypatch):
    import matrx_ai._ext as ext

    seen: list[dict] = []

    def record_error(exc, **kw):
        seen.append({"exc": exc, **kw})

    real = ext.get_ext
    monkeypatch.setattr(
        ext, "get_ext", lambda name: record_error if name == "record_error" else real(name)
    )
    return seen


@pytest.mark.parametrize("door", ["with_variables", "set_variables"])
def test_new_values_on_an_applied_agent_raise_and_are_logged(door, captured) -> None:
    agent = _agent().with_variables(city="Quito")
    with pytest.raises(VariablesAlreadyAppliedError, match="city"):
        getattr(agent, door)(city="Cusco")
    assert agent.config.system_instruction.base_instruction == "Guide for Quito."
    assert agent.variable_values == {"city": "Quito"}
    assert captured and isinstance(captured[0]["exc"], VariablesAlreadyAppliedError)
    assert captured[0]["kind"] == "variables_already_applied"


def test_a_staged_value_applied_without_force_raises(captured) -> None:
    agent = _agent().apply_variables()
    agent.set_variable("city", "Cusco")
    with pytest.raises(VariablesAlreadyAppliedError):
        agent.apply_variables()
    assert agent.config.system_instruction.base_instruction == "Guide for Lima."


def test_values_already_applied_are_not_new(captured) -> None:
    agent = _agent().with_variables(city="Quito")
    agent.with_variables(city="Quito").apply_variables()
    assert agent.config.system_instruction.base_instruction == "Guide for Quito."
    assert captured == []


def test_the_deliberate_refill_doors_still_work(captured) -> None:
    agent = _agent().with_variables(city="Quito")
    assert agent.clone().with_variables(city="Cusco").config.system_instruction.base_instruction == (
        "Guide for Cusco."
    )
    agent.set_variable("city", "Cusco").apply_variables(force=True)
    assert agent.config.system_instruction.base_instruction == "Guide for Cusco."
    assert captured == []
