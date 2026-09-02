"""A workflow step names the JOB, not the agent.

Before this, `ai.agent.start` could only carry an `agent_id` — so every
workflow definition FROZE its agents at authoring time. That is a hardcoded
agent by another route: invisible to every org/user Binding, months stale the
moment it is written, and the reason `deep_research_v1` carries four ids in
`scripts/hardcoded_agents_baseline.json`. It was the named blocker on building
the podcast challenger graph, whose 27 stages are all Mandates.

The rule these tests force: a step may name a `mandate_key` and the DATABASE
decides which agent runs it, resolved fresh on EVERY run through the ONE door
— and when the mandate cannot be resolved the step REFUSES rather than running
something nobody chose.
"""

from __future__ import annotations

import pytest

from matrx_ai import mandates
from matrx_ai.agents.named import AgentRecordSource
from matrx_ai.graph_nodes.agent_action import AgentStartInput, resolve_step_agent

_HOLDER = "11111111-2222-3333-4444-555555555555"


@pytest.mark.asyncio
async def test_a_mandate_step_runs_whatever_the_database_currently_binds(monkeypatch):
    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        assert mandate_key == "podcast.deep_research"
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            config_overrides={"temperature": 0.2},
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)

    agent_id, is_version, overrides = await resolve_step_agent(
        AgentStartInput(mandate_key="podcast.deep_research"), consumer="test"
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
            AgentStartInput(mandate_key="podcast.script_educational"), consumer="test-step"
        )
    assert excinfo.value.mandate_key == "podcast.script_educational"
    assert excinfo.value.consumer == "test-step"


@pytest.mark.asyncio
async def test_a_step_naming_BOTH_selectors_is_REFUSED_naming_both_values(monkeypatch):
    """D-46 / C-32: exactly one selector. Which authority chose the agent is
    precisely the question a Mandate exists to answer, so a step carrying both
    is not reconcilable — it is refused.

    This test exists because the code shipped the OTHER way and nobody
    recorded a reversal: `resolve_step_agent` read the second value as a
    build-time "drift snapshot", logged a warning, and ran the mandate's
    Holder anyway. That is warn-and-continue over an id nobody re-chose —
    the silent-default shape the no-seed-fallback ruling deleted.

    The error must NAME BOTH VALUES: the whole repair is "drop the one that
    isn't the authority", and an author who cannot see which two values
    collided cannot do it.
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
            AgentStartInput(mandate_key="podcast.metadata", agent_id=pinned),
            consumer="test-step",
        )

    message = str(excinfo.value)
    assert "podcast.metadata" in message, "the mandate must be named"
    assert pinned in message, "the colliding agent id must be named"
    assert "test-step" in message, "the step must be named"
    # It refuses BEFORE spending a resolution — the conflict is in the
    # definition, and nothing about the database can settle it.
    assert resolver_calls == []


@pytest.mark.asyncio
async def test_BOTH_is_refused_even_when_the_id_MATCHES_the_holder(monkeypatch):
    """The refusal is about ambiguity of AUTHORITY, not disagreement of value.

    An id that happens to equal today's Holder is the most dangerous form of
    this shape, not the safe one: it reads as harmless, and it silently stops
    matching the moment a Binding swaps the Holder. If agreement excused it,
    every one of the 27 live nodes found on 2026-08-20 would have passed.
    """

    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False)
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)

    with pytest.raises(ValueError, match="BOTH"):
        await resolve_step_agent(
            AgentStartInput(mandate_key="podcast.metadata", agent_id=_HOLDER),
            consumer="test",
        )


@pytest.mark.asyncio
async def test_the_pinned_id_is_NEVER_a_fallback_for_an_unresolvable_mandate(
    monkeypatch,
):
    """Refusing both-set must not become a back door to the seed fallback:
    a step carrying both is refused for the CONFLICT, never quietly demoted to
    running the id because the mandate could not resolve."""
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    with pytest.raises(ValueError) as excinfo:
        await resolve_step_agent(
            AgentStartInput(mandate_key="podcast.metadata", agent_id=_HOLDER),
            consumer="test-step",
        )
    # Refused on the conflict, and in no case did the pinned id get executed.
    assert "BOTH" in str(excinfo.value)


@pytest.mark.asyncio
async def test_a_step_naming_NEITHER_is_refused():
    with pytest.raises(ValueError, match="names no agent"):
        await resolve_step_agent(AgentStartInput(), consumer="test")


@pytest.mark.asyncio
async def test_a_pinned_agent_id_still_works_unchanged():
    agent_id, is_version, overrides = await resolve_step_agent(
        AgentStartInput(agent_id=_HOLDER, is_version=True), consumer="test"
    )
    assert (agent_id, is_version, overrides) == (_HOLDER, True, None)
