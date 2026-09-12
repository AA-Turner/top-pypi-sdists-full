"""Run Agent and Run Mandate are two step types, and they never blur again.

THE RULING (Arman, 2026-09-10). "Run Agent and Run Mandate have nothing in
common… a mandate is not a representation of an agent. It's a representation of
some sort of intelligence… Agents work with an ID, a version number, and then
mapping of inputs and outputs. And a mandate doesn't have that sort of thing."

Between 2026-08-17 and this split, ``ai.agent.start`` carried BOTH selectors
(D-46/C-32) and the studio rendered an agent picker and a mandate picker side by
side on one step. These tests are the layer that keeps them apart:

* Run Agent (``ai.agent.start``) has NO mandate field, and refuses one loudly —
  its input model allows extras, so without the refusal an un-migrated
  definition would fold the key into the agent's VARIABLES and run something
  else in silence.
* Run Mandate (``ai.mandate.start``) REQUIRES a mandate key and has no agent id
  and no version at all.
* The shared execution lift still resolves both, and still refuses the two step
  types that legitimately declare both selectors when they carry both values.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai import mandates
from matrx_ai.agents.named import AgentRecordSource
from matrx_ai.graph_nodes.agent_action import (
    AgentStartInput,
    resolve_step_agent,
)
from matrx_ai.graph_nodes.agent_produce_action import AgentProduceInput
from matrx_ai.graph_nodes.mandate_action import MandateStartInput

_HOLDER = "11111111-2222-3333-4444-555555555555"


# --------------------------------------------------------------------------
# The two contracts, as SHAPES
# --------------------------------------------------------------------------


def test_run_agent_has_no_mandate_field_and_run_mandate_has_no_agent_field():
    assert "mandate_key" not in AgentStartInput.model_fields
    assert "agent_id" in AgentStartInput.model_fields
    assert "is_version" in AgentStartInput.model_fields

    assert "mandate_key" in MandateStartInput.model_fields
    assert "agent_id" not in MandateStartInput.model_fields
    assert "is_version" not in MandateStartInput.model_fields
    assert MandateStartInput.model_fields["mandate_key"].is_required()


def test_a_run_agent_step_carrying_a_mandate_is_REFUSED_with_the_migration_hint():
    """The loudest case: extras are ALLOWED here, so silence would mean the key
    became an agent variable and the step ran something nobody chose."""
    with pytest.raises(ValidationError) as excinfo:
        AgentStartInput(mandate_key="podcast.deep_research")
    message = str(excinfo.value)
    assert "podcast.deep_research" in message, "the mandate must be named"
    assert "ai.mandate.start" in message, "the migration target must be named"
    assert "Run Mandate" in message


@pytest.mark.parametrize(
    "exposed_inputs",
    [
        {"topic": "", "audience": "high school", "material": '{"__kind":"structured_document"}'},
        {
            "count": "15",
            "difficulty_mix": "balanced",
            "material": '{"__kind":"structured_document"}',
        },
        {"mcq_count": "8", "fill_in_blank_count": "5", "free_response_count": "2"},
        {
            "tone": "conversational",
            "target_section_count": "5",
            "target_duration_seconds_per_section": "120",
        },
    ],
)
def test_agent_produce_preserves_authored_variable_ports(exposed_inputs: dict[str, str]):
    """Breaking this makes every Study Pack producer fail before the agent runs."""
    parsed = AgentProduceInput.model_validate(
        {"mandate_key": "education.study_pack", **exposed_inputs}
    )

    assert parsed.model_extra == exposed_inputs


def test_an_EMPTY_mandate_key_on_a_run_agent_step_is_dropped_not_fatal():
    """Live node ``n-vapf8MnirU``: the studio form wrote ``mandate_key: null``
    beside a pinned agent_id back when Run Agent declared the field. A null
    carries no instruction — it is cruft, and failing a run over it would break
    a step that was always doing exactly one thing."""
    parsed = AgentStartInput(agent_id=_HOLDER, mandate_key=None)
    assert parsed.model_extra == {}
    assert parsed.agent_id == _HOLDER


def test_a_run_mandate_step_with_no_job_named_is_not_a_step():
    with pytest.raises(ValidationError):
        MandateStartInput()


@pytest.mark.asyncio
async def test_a_run_mandate_step_carrying_an_agent_id_is_REFUSED(monkeypatch):
    """A vestigial id beside the job is still two authorities, and still refused.

    ``extra="allow"`` is for the author's exposed VARIABLES, so an ``agent_id``
    on a Run Mandate step parses — it lands in ``model_extra``. It must not
    then be INERT: the live migration found exactly this on the
    ``masterwork.understudy`` step of definition ``d955aac4`` (a crossed node
    carried over from the D-46 era), and a step naming both is the one thing
    D-46 settled forever. ``resolve_step_agent_full`` reads the selector with
    ``getattr``, which sees the extra, so the refusal holds on both sides of
    the split.
    """
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)
    parsed = MandateStartInput(mandate_key="podcast.script", agent_id=_HOLDER)
    assert parsed.model_extra == {"agent_id": _HOLDER}

    with pytest.raises(ValueError) as excinfo:
        await resolve_step_agent(parsed, consumer="test-step")
    message = str(excinfo.value)
    assert "BOTH" in message
    assert "podcast.script" in message and _HOLDER in message


# --------------------------------------------------------------------------
# The shared lift
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_run_mandate_step_runs_whatever_the_database_currently_binds(monkeypatch):
    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        assert mandate_key == "podcast.deep_research"
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            config_overrides={"temperature": 0.2},
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)

    agent_id, is_version, overrides = await resolve_step_agent(
        MandateStartInput(mandate_key="podcast.deep_research"), consumer="test"
    )
    assert agent_id == _HOLDER
    assert is_version is False
    assert overrides == {"temperature": 0.2}


@pytest.mark.asyncio
async def test_an_UNRESOLVABLE_mandate_REFUSES_instead_of_running_anything(monkeypatch):
    """No seed fallback in a workflow either — the law is the law everywhere."""
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    with pytest.raises(mandates.MandateResolutionUnavailable) as excinfo:
        await resolve_step_agent(
            MandateStartInput(mandate_key="podcast.script_educational"), consumer="test-step"
        )
    assert excinfo.value.mandate_key == "podcast.script_educational"
    assert excinfo.value.consumer == "test-step"


@pytest.mark.asyncio
async def test_a_step_that_may_declare_BOTH_selectors_is_refused_naming_both_values(
    monkeypatch,
):
    """``ai.agent.produce`` legitimately declares both — one of them, not two.

    The error must NAME BOTH VALUES: the whole repair is "drop the one that
    isn't the authority", and an author who cannot see which two values
    collided cannot do it. It also refuses BEFORE spending a resolution — the
    conflict is in the definition, and nothing about the database can settle it.
    """
    resolver_calls: list[str] = []

    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        resolver_calls.append(mandate_key)
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False)
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    pinned = "99999999-8888-7777-6666-555555555555"

    with pytest.raises(ValueError) as excinfo:
        await resolve_step_agent(
            AgentProduceInput(mandate_key="podcast.metadata", agent_id=pinned),
            consumer="test-step",
        )

    message = str(excinfo.value)
    assert "podcast.metadata" in message, "the mandate must be named"
    assert pinned in message, "the colliding agent id must be named"
    assert "test-step" in message, "the step must be named"
    assert resolver_calls == []


@pytest.mark.asyncio
async def test_the_pinned_id_is_NEVER_a_fallback_for_an_unresolvable_mandate(monkeypatch):
    """Refusing both-set must not become a back door to the seed fallback:
    a step carrying both is refused for the CONFLICT, never quietly demoted to
    running the id because the mandate could not resolve."""
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    with pytest.raises(ValueError) as excinfo:
        await resolve_step_agent(
            AgentProduceInput(mandate_key="podcast.metadata", agent_id=_HOLDER),
            consumer="test-step",
        )
    assert "BOTH" in str(excinfo.value)


@pytest.mark.asyncio
async def test_a_step_naming_NEITHER_is_refused():
    with pytest.raises(ValueError, match="names nothing to run"):
        await resolve_step_agent(AgentStartInput(), consumer="test")


@pytest.mark.asyncio
async def test_a_pinned_agent_id_still_works_unchanged():
    agent_id, is_version, overrides = await resolve_step_agent(
        AgentStartInput(agent_id=_HOLDER, is_version=True), consumer="test"
    )
    assert (agent_id, is_version, overrides) == (_HOLDER, True, None)
