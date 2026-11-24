"""An ``agent`` call that names no agent the caller can run is refused WITH the agents it can run.

Defect (PB-03, conversations 9fe2bdce / 8a068517 / 2b85804f, C55 replays): gpt-5-nano called
``agent`` with an invented ``agent_id`` ("lane-planner-mxcity") instead of the uuid its
instructions gave. The refusal said only "not an agent id", so the model guessed again.

Now the refusal names the agents the caller can actually run (name + id, closest names first,
bounded, with a count), read through the SAME session the run gate uses
(``load_agent_as_the_person``: the caller's RLS session, admin lane on an admin surface) and the
same runnable rule (active, not archived). A non-uuid that equals exactly one reachable agent's
name (as a slug) is refused with that one suggested, never run.

Scenario: a freight dispatcher's routing desk calls the "Lane Planner" agent.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any

import pytest

ME = "c1d2e3f4-0000-4000-8000-00000000a001"
MY_ORG = "c1d2e3f4-0000-4000-8000-00000000b001"
OTHER_ORG = "c1d2e3f4-0000-4000-8000-00000000b002"
LANE_PLANNER = "20624bc2-1828-4fe2-9379-2aabc1ceca44"
DOCK_CLERK = "20624bc2-0000-4000-8000-000000000002"
ARCHIVED = "20624bc2-0000-4000-8000-000000000003"
INACTIVE = "20624bc2-0000-4000-8000-000000000004"
HIDDEN = "20624bc2-0000-4000-8000-000000000005"

_acting: ContextVar[str | None] = ContextVar("fake_acting_reachable", default=None)

#: What the database holds; ``readers`` is who RLS lets see the row.
ROWS = [
    {"id": LANE_PLANNER, "name": "Lane Planner", "organization_id": MY_ORG, "is_active": True,
     "is_archived": False, "readers": {ME}},
    {"id": DOCK_CLERK, "name": "Dock Clerk", "organization_id": OTHER_ORG, "is_active": True,
     "is_archived": False, "readers": {ME}},
    {"id": ARCHIVED, "name": "Lane Planner (old)", "organization_id": MY_ORG, "is_active": True,
     "is_archived": True, "readers": {ME}},
    {"id": INACTIVE, "name": "Lane Scout", "organization_id": MY_ORG, "is_active": False,
     "is_archived": False, "readers": {ME}},
    {"id": HIDDEN, "name": "Lane Planner Secret", "organization_id": OTHER_ORG, "is_active": True,
     "is_archived": False, "readers": {"someone-else"}},
]


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from matrx_ai import _ext
    from matrx_ai.db.agx_manager import AgxDefinition

    bag: dict[str, Any] = {"violations": []}

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        token = _acting.set(ME)
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)

    class _Query:
        async def values(self, *fields: str) -> list[dict[str, Any]]:
            who = _acting.get()
            if who is None:
                bag["violations"].append("agent list read on the privileged connection")
            return [
                {k: v for k, v in r.items() if k in fields}
                for r in ROWS
                if who in r["readers"]
            ]

    monkeypatch.setattr(AgxDefinition, "filter", classmethod(lambda _c, **_k: _Query()))

    async def load_agent(_cls, agent_id):
        who = _acting.get()
        if who is None:
            bag["violations"].append("agent load on the privileged connection")
        for r in ROWS:
            if r["id"] == agent_id and who in r["readers"]:
                return SimpleNamespace(**{k: v for k, v in r.items() if k != "readers"})
        return None

    monkeypatch.setattr(AgxDefinition, "load_by_id_or_none", classmethod(load_agent))
    return bag


def _app() -> Any:
    return SimpleNamespace(user_id=ME, organization_id=MY_ORG, metadata={}, is_admin=False)


@pytest.mark.asyncio
async def test_reachable_agents_are_exactly_what_the_run_gate_accepts(world) -> None:
    from matrx_ai.tools.implementations.agent_call import load_agent_as_the_person, reachable_agents

    app = _app()
    listed = {a["id"] for a in await reachable_agents(app)}
    assert listed == {LANE_PLANNER, DOCK_CLERK}
    # Same answer as the gate, row by row: every listed id loads and is runnable; nothing
    # hidden, archived or inactive is offered.
    for agent_id in listed:
        row = await load_agent_as_the_person(agent_id, app)
        assert row is not None and row.is_active and not row.is_archived
    assert world["violations"] == []


@pytest.mark.asyncio
async def test_an_invented_name_gets_the_closest_reachable_agents_first(world) -> None:
    from matrx_ai.tools.implementations.agent_call import unknown_agent_refusal

    text = await unknown_agent_refusal("lane-planner-mxcity", _app())
    assert f"Lane Planner: {LANE_PLANNER}" in text
    assert text.index(LANE_PLANNER) < text.index(DOCK_CLERK)
    assert "2 of 2" in text
    for never in (ARCHIVED, INACTIVE, HIDDEN):
        assert never not in text
    assert world["violations"] == []


@pytest.mark.asyncio
async def test_a_camel_case_invention_still_finds_the_agent(world) -> None:
    from matrx_ai.tools.implementations.agent_call import reachable_agents, unknown_agent_message

    agents = await reachable_agents(_app())
    # Caller sits in Dock Clerk's org, so only the name match can put Lane Planner first.
    text = unknown_agent_message("LanePlannerMexicoCity", agents, organization_id=OTHER_ORG)
    assert text.index(LANE_PLANNER) < text.index(DOCK_CLERK)


@pytest.mark.asyncio
async def test_an_exact_name_is_suggested_never_run(world) -> None:
    from matrx_ai.tools.implementations.agent_call import unknown_agent_refusal

    text = await unknown_agent_refusal("lane_planner", _app())
    assert f"agent_id='{LANE_PLANNER}'" in text
    assert DOCK_CLERK not in text


def test_the_list_is_bounded_with_a_count() -> None:
    from matrx_ai.tools.implementations.agent_call import (
        REACHABLE_AGENTS_SHOWN,
        unknown_agent_message,
    )

    agents = [
        {"id": f"20624bc2-0000-4000-8000-{i:012d}", "name": f"Agent {i}", "organization_id": MY_ORG}
        for i in range(25)
    ]
    text = unknown_agent_message("nope", agents, organization_id=MY_ORG)
    assert f"{REACHABLE_AGENTS_SHOWN} of 25" in text
    assert sum(a["id"] in text for a in agents) == REACHABLE_AGENTS_SHOWN


@pytest.mark.asyncio
async def test_agent_call_not_found_names_the_reachable_agents(world, monkeypatch) -> None:
    """A uuid the caller cannot run: agent_call's own not_found refusal carries the list."""
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=ME, organization_id=MY_ORG, conversation_id=None))
    try:
        result = await agent_call(
            {"agent_id": HIDDEN, "user_input": "Route move 4471 to Mexico City."},
            ToolContext(call_id="call-1"),
        )
    finally:
        clear_app_context(token)
    assert not result.success
    assert result.error.error_type == "not_found"
    assert f"Lane Planner: {LANE_PLANNER}" in result.error.message
    assert HIDDEN not in result.error.message.split("Agents you can call")[1]
    assert world["violations"] == []
