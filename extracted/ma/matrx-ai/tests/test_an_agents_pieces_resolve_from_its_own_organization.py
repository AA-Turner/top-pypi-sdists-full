"""An agent's DECLARED prompt blocks resolve from the agent's OWN organization (defect 39, PB-02 M6).

A user binding follows the person into a second organization by design. The agent's definition is
owned by organization A; the run happens in organization B (the run is stamped, billed and written in
B — unchanged). A block the definition declares by name must still be found in A. The run's
organization keeps its override rung (an organization can swap in its own block of the same name,
plan R1), so the ladder is: personal > run organization > the agent's organization > system.

The organization id rides the definition in-process only: it never joins the portable wire shape
or its content hash (installed client hosts validate that shape with ``extra="forbid"``).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.client_host.agent_source import definition_from_row, definition_to_agent_config
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.prompt_blocks import BlockRow, PromptBlocksMissing, resolve_declared_blocks

CREATOR = "11111111-1111-1111-1111-111111111111"
RUNNER = "22222222-2222-2222-2222-222222222222"
AGENT_ORG = "aaaaaaaa-0000-0000-0000-000000000000"  # Safety Net Real Tests (the agent's owner)
RUN_ORG = "bbbbbbbb-0000-0000-0000-000000000000"  # admin's Workspace (the active organization)


class OrgKeyedSource:
    """Answers like the server source: organization rows ONLY for the organization asked."""

    def __init__(self, rows: list[tuple[str | None, BlockRow]]):
        self.rows = rows
        self.asked_orgs: list[str | None] = []

    async def candidates(self, names, *, organization_id, personal_user_id):
        self.asked_orgs.append(organization_id)
        out = []
        for org, r in self.rows:
            if r.name not in names:
                continue
            if r.level == "organization" and org != organization_id:
                continue
            if r.level == "personal" and not personal_user_id:
                continue
            out.append(r)
        return out

    async def skill(self, skill_id):
        return None

    async def model_facts(self, model):
        return None

    async def personal_rung_enabled(self, organization_id):
        return True


def _row(name: str, level: str, content: str, org: str | None) -> tuple[str | None, BlockRow]:
    return org, BlockRow(id=f"{level}-{org}-{name}", name=name, level=level, content=content)


def _config(*names: str, agent_org: str | None = AGENT_ORG) -> UnifiedConfig:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "messages": [{"role": "system", "content": " ".join("{{<" + n + ">}}" for n in names)}],
            "prompt_blocks": list(names),
        }
    )
    config.prompt_block_creator = CREATOR
    config.agent_organization_id = agent_org
    return config


def _resolve(config: UnifiedConfig, source: OrgKeyedSource, *, run_org: str = RUN_ORG):
    return asyncio.run(
        resolve_declared_blocks(config, runner_id=RUNNER, organization_id=run_org, source=source)
    )


def test_a_block_only_in_the_agents_organization_resolves_in_another_organizations_run() -> None:
    source = OrgKeyedSource([_row("compass_lane_safety", "organization", "LANE RULES", AGENT_ORG)])
    config = _config("compass_lane_safety")
    _resolve(config, source)
    assert config.prompt_block_texts == {"compass_lane_safety": "LANE RULES"}
    assert config.prompt_block_report[0]["level"] == "agent_organization"
    # The run's organization was asked first (its override rung), then the agent's.
    assert source.asked_orgs == [RUN_ORG, AGENT_ORG]


def test_the_run_organization_still_overrides_the_agents_block_of_the_same_name() -> None:
    source = OrgKeyedSource(
        [
            _row("rules", "organization", "AGENT ORG", AGENT_ORG),
            _row("rules", "organization", "RUN ORG", RUN_ORG),
            _row("rules", "system", "SYS", None),
        ]
    )
    config = _config("rules")
    _resolve(config, source)
    assert config.prompt_block_texts == {"rules": "RUN ORG"}
    assert config.prompt_block_report[0]["level"] == "organization"


def test_the_agents_organization_outranks_system() -> None:
    source = OrgKeyedSource(
        [_row("rules", "organization", "AGENT ORG", AGENT_ORG), _row("rules", "system", "SYS", None)]
    )
    config = _config("rules")
    _resolve(config, source)
    assert config.prompt_block_texts == {"rules": "AGENT ORG"}


def test_a_run_in_the_agents_own_organization_asks_once() -> None:
    source = OrgKeyedSource([_row("rules", "organization", "AGENT ORG", AGENT_ORG)])
    config = _config("rules")
    _resolve(config, source, run_org=AGENT_ORG)
    assert config.prompt_block_texts == {"rules": "AGENT ORG"}
    assert config.prompt_block_report[0]["level"] == "organization"
    assert source.asked_orgs == [AGENT_ORG]


def test_a_block_in_neither_organization_still_refuses_naming_it() -> None:
    source = OrgKeyedSource([_row("rules", "organization", "ELSEWHERE", "cccccccc-0000-0000-0000-000000000000")])
    config = _config("rules")
    with pytest.raises(PromptBlocksMissing) as err:
        _resolve(config, source)
    assert err.value.names == ["rules"]


def _agent_row(org: str | None) -> SimpleNamespace:
    return SimpleNamespace(
        id="d7fbe234-1adf-415d-aeb5-9f5343df9725",
        agent_id="d7fbe234-1adf-415d-aeb5-9f5343df9725",
        version_number=3,
        changed_at=None,
        name="Compass Mandate Desk",
        model_id="model-1",
        messages=[{"role": "system", "content": "{{<compass_lane_safety>}}"}],
        prompt_blocks=[{"name": "compass_lane_safety"}],
        created_by=CREATOR,
        organization_id=org,
    )


def test_the_definition_carries_its_organization_onto_the_run_config() -> None:
    definition = definition_from_row(_agent_row(AGENT_ORG), is_version=True)
    assert definition.organization_id == AGENT_ORG
    agent_config = definition_to_agent_config(definition)
    assert getattr(agent_config.config, "agent_organization_id", None) == AGENT_ORG


def test_the_organization_never_joins_the_portable_wire_shape_or_its_hash() -> None:
    with_org = definition_from_row(_agent_row(AGENT_ORG), is_version=True)
    without = definition_from_row(_agent_row(None), is_version=True)
    assert with_org.definition_hash == without.definition_hash
    assert "organization_id" not in with_org.model_dump()
    assert "organization_id" not in with_org.model_dump_json()


def test_the_agents_organization_survives_the_config_round_trip() -> None:
    config = _config("rules")
    again = UnifiedConfig.from_dict(config.to_dict())
    assert again.agent_organization_id == AGENT_ORG
