from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_ai.client_host.agent_source import (
    ExecutionAgentDefinition,
    definition_from_row,
    definition_to_agent_config,
)


def _definition(**updates: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "definition_id": "agent-1",
        "agent_id": "agent-1",
        "name": "Canonical",
        "model_id": "model-top-level",
        "messages": [{"role": "system", "content": "Never drop this prompt."}],
        "settings": {
            "model": "model-from-settings-must-lose",
            "messages": [],
            "tools": True,
            "temperature": 0.2,
        },
        "tools": ["tool-id-1"],
        "variable_definitions": [{"name": "topic", "defaultValue": "safety"}],
        "context_policies": [{"key": "workspace"}],
        "tool_config": {
            "excluded_tools": ["dangerous"],
            "auto_tools_disabled": True,
        },
        "output_schema": {"name": "answer", "schema": {"type": "object"}},
        "matrx_actions": {"actions": ["apply"]},
        "skill_config": {},
    }
    payload.update(updates)
    return payload


def test_definition_mapper_uses_structural_fields_not_settings_projection() -> None:
    definition = ExecutionAgentDefinition.model_validate(_definition())
    config = definition_to_agent_config(definition)

    assert config.config.model == "model-top-level"
    assert config.config.system_instruction.base_instruction == "Never drop this prompt."
    assert config.config.tools == ["tool-id-1"]
    assert config.config.temperature == 0.2
    assert config.excluded_tools == ["dangerous"]
    assert config.auto_tools_disabled is True
    assert config.context_policies == [{"key": "workspace"}]
    assert config.matrx_actions == {"actions": ["apply"]}
    assert config.output_schema == {"name": "answer", "schema": {"type": "object"}}


@pytest.mark.parametrize(
    ("updates", "needle"),
    [
        ({"model_id": ""}, "model_id"),
        ({"messages": []}, "messages"),
    ],
)
def test_incomplete_definition_is_rejected_before_execution(
    updates: dict[str, object], needle: str
) -> None:
    with pytest.raises(ValidationError, match=needle):
        ExecutionAgentDefinition.model_validate(_definition(**updates))


def test_orm_row_projection_and_wire_definition_share_the_same_mapper() -> None:
    row = SimpleNamespace(
        id="agent-1",
        name="Canonical",
        model_id="model-top-level",
        messages=[{"role": "system", "content": "Never drop this prompt."}],
        settings={"temperature": 0.2},
        tools=["tool-id-1"],
        custom_tools=[],
        mcp_servers=[],
        variable_definitions=[],
        context_policies=[],
        tool_config={},
        output_schema=None,
        matrx_actions={},
        skill_config={},
        version=7,
        updated_at=None,
    )

    definition = definition_from_row(row, is_version=False)
    config = definition_to_agent_config(definition)

    assert definition.version_number == 7
    assert definition.definition_hash == definition.content_hash()
    assert config.config.model == "model-top-level"
    assert config.config.system_instruction.base_instruction == "Never drop this prompt."


@pytest.mark.asyncio
async def test_agx_facade_uses_configured_execution_source(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai import _ext
    from matrx_ai.db.agx_manager import agx

    class Source:
        async def load_for_execution(
            self, agent_id: str, *, is_version: bool = False
        ) -> dict[str, object]:
            assert agent_id == "agent-1"
            assert is_version is False
            return _definition()

    monkeypatch.setitem(_ext._registry, "execution_agent_source", Source())
    loaded = await agx.load_for_execution("agent-1")

    assert loaded.config.model == "model-top-level"
    assert loaded.config.system_instruction.base_instruction == "Never drop this prompt."


def test_agx_facade_proxies_manager_attributes() -> None:
    from matrx_ai.db._agx_manager_impl import agx as real_agx
    from matrx_ai.db.agx_manager import agx

    assert agx.agx_agent is real_agx.agx_agent
    assert agx.agx_version is real_agx.agx_version
    assert agx.definition is real_agx.definition
