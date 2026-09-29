"""`agent_call` loads the agent and the history conversation AS THE PERSON.

Defect (2026-09-27): agent_call loaded ``agent_id`` on the privileged connection
and decided access in Python (owner comparison, then ``agent_viewer_access`` →
``iam.has_access_for``), and gated a history conversation with a hand-written
``created_by=<caller>`` filter. Chair ruling: RLS owns access. Both reads now run
inside the caller's RLS session (``as_the_person`` → host ``acting_as_caller``)
and Postgres decides; a hidden agent or conversation is ``not_found`` naming
its id. The child RUN itself is not held inside that session.

Scenario: a property-management firm. Priya (leasing lead) built the agent
"Lease renewal letter writer"; Marco, a contractor at another company, must not
be able to run it by id from his own chat, nor fork Priya's conversation.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any

import pytest

PRIYA = "c1d2e3f4-0000-4000-8000-00000000e001"
MARCO = "c1d2e3f4-0000-4000-8000-00000000f002"
AGENT_ID = "a9e8d7c6-0000-4000-8000-000000000001"
PRIYA_CONV = "a9e8d7c6-0000-4000-8000-0000000000c1"
MARCO_CONV = "a9e8d7c6-0000-4000-8000-0000000000c2"

_acting: ContextVar[str | None] = ContextVar("fake_acting_user_agents", default=None)


async def _value(v):
    return v


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    import matrx_ai.db as db_pkg
    from matrx_ai import _ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents import resolver as resolver_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db import agx_manager
    from matrx_ai.db.agx_manager import AgxDefinition

    bag: dict[str, Any] = {
        "violations": [],
        "db_calls": 0,
        "runs": [],
        "run_in_session": [],
        "agent_readers": {PRIYA},
        "conv_readers": {PRIYA_CONV: {PRIYA}, MARCO_CONV: {MARCO}},
        "admin_lane_opened": 0,
    }

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        from matrx_connect.context.app_context import get_app_context

        token = _acting.set(get_app_context().user_id)
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)

    def who(seam: str) -> str | None:
        bag["db_calls"] += 1
        w = _acting.get()
        if w is None:
            bag["violations"].append(f"{seam}: ran on the privileged connection")
        return w

    async def load_agent(_cls, agent_id):
        w = who("agent.load_by_id_or_none")
        if agent_id == AGENT_ID and w in bag["agent_readers"]:
            return SimpleNamespace(id=AGENT_ID, created_by=PRIYA, is_active=True, is_archived=False)
        return None

    monkeypatch.setattr(AgxDefinition, "load_by_id_or_none", classmethod(load_agent))

    async def viewer_access(*_a, **_k):
        bag["violations"].append("agent_viewer_access: app code asked an access question")
        return True

    monkeypatch.setattr(agx_manager, "agent_viewer_access", viewer_access, raising=False)

    async def filter_items(**kwargs):
        w = who("conversation.filter_items")
        if "created_by" in kwargs:
            bag["violations"].append("conversation gate filtered by created_by in app code")
        cid = kwargs.get("id")
        return [SimpleNamespace(id=cid, deleted_at=None)] if w in bag["conv_readers"].get(cid, set()) else []

    monkeypatch.setattr(
        db_pkg,
        "cxm",
        SimpleNamespace(conversation=SimpleNamespace(filter_items=filter_items)),
        raising=False,
    )

    class _Child:
        name = "Lease renewal letter writer"
        output_schema = None

        def __init__(self) -> None:
            self.config = SimpleNamespace(messages=[SimpleNamespace(role="user", authored=True)])

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _c, *_a, **_k: _value(_Child())))

    async def run_agent(_agent, **kwargs):
        bag["runs"].append(kwargs)
        bag["run_in_session"].append(_acting.get() is not None)
        return AgentRunResult(success=True, output="Dear tenant, your lease renews on Nov 1.")

    monkeypatch.setattr(executor_mod, "run_agent", run_agent)

    async def load_history(conversation_id: str):
        return SimpleNamespace(messages=[SimpleNamespace(role="user", position=0, authored=False)])

    monkeypatch.setattr(resolver_mod, "_load_unified_config", load_history)
    return bag


async def _call(user: str, args: dict[str, Any], *, conversation_id: str | None = None):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=user, conversation_id=conversation_id))
    try:
        return await agent_call({"agent_id": AGENT_ID, **args}, ToolContext(call_id="call-lease"))
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_the_owner_runs_the_agent_and_the_run_is_not_held_in_the_session(world):
    result = await _call(PRIYA, {})
    assert result.success, result.error
    assert len(world["runs"]) == 1
    assert world["run_in_session"] == [False], "the child run must not hold the person's transaction"
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_an_outsider_cannot_run_the_agent_and_is_told_so_by_id(world):
    result = await _call(MARCO, {})
    assert not result.success
    assert result.error.error_type == "not_found"
    assert AGENT_ID in result.error.message
    assert "Lease" not in result.error.message
    assert world["runs"] == []
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_an_outsider_cannot_snapshot_someone_elses_conversation(world):
    world["agent_readers"].add(MARCO)  # the agent itself is shared with Marco
    result = await _call(
        MARCO,
        {"history_mode": "snapshot", "history_conversation_id": PRIYA_CONV},
        conversation_id=MARCO_CONV,
    )
    assert not result.success
    assert result.error.error_type == "not_found"
    assert PRIYA_CONV in result.error.message
    assert world["runs"] == []

    own = await _call(MARCO, {"history_mode": "snapshot"}, conversation_id=MARCO_CONV)
    assert own.success, own.error
    assert world["violations"] == [], world["violations"]


@pytest.mark.asyncio
async def test_without_a_person_session_the_tool_refuses_and_never_touches_the_db(world, monkeypatch):
    from matrx_ai import _ext

    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    result = await _call(PRIYA, {})
    assert not result.success
    assert result.error.error_type == "unavailable", result.error
    assert world["db_calls"] == 0
    assert world["runs"] == []
