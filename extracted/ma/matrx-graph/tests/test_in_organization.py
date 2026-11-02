"""Run one step in another organization (``data.in_organization``) — the real Scheduler.

Each rule in ``matrx_graph/in_organization.py`` is driven through ``Scheduler.run`` with a real
executor that records the organization it ran in (its own context AND the ambient AppContext every
AI call and write reads), and a host admission seam that admits only real members.
"""

from __future__ import annotations

import dataclasses
import uuid
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import CompilationError, Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.in_organization import OrganizationNotAdmitted, configure_organization_switch
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

PERSON = "1d2e3f40-5a6b-4c7d-8e9f-a0b1c2d3e4f5"
ORG_RUN = "11111111-1111-4111-8111-111111111111"
ORG_MEMBER = "22222222-2222-4222-8222-222222222222"
ORG_STRANGER = "33333333-3333-4333-8333-333333333333"


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid")  # closed: the setting must consume its own input

    text: str = ""


class _OpenIn(_In):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Where:
    """Records where each call ran: the step context's organization and the ambient one."""

    def __init__(self, node_type: str) -> None:
        open_inputs = node_type == "test.after"
        self.spec = NodeSpec(
            type=node_type,
            category=NodeCategory.DATA,
            display_name="Where am I",
            description="in_organization test step",
            input_schema=_OpenIn if open_inputs else _In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=RetryPolicy(max_attempts=1),
        )
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        from matrx_connect.context.app_context import get_app_context

        ambient = get_app_context()
        row = {
            "ctx_org": ctx.organization_id,
            "ambient_org": ambient.organization_id,
            "user": ambient.user_id,
            "request_id": ambient.request_id,
            "text": getattr(inputs, "text", ""),
        }
        self.seen.append(row)
        return success(_Out(**row))


class _Admission:
    """The host seam: admits only a member, carries the actor, mints a new request id."""

    def __init__(self, members: dict[str, set[str]]) -> None:
        self.members = members
        self.asked: list[tuple[str, str]] = []

    def __call__(self, app: Any, organization_id: str) -> Any:
        @asynccontextmanager
        async def _cm() -> AsyncIterator[Any]:
            self.asked.append((app.user_id, organization_id))
            if organization_id not in self.members.get(app.user_id, set()):
                raise OrganizationNotAdmitted("You are not a member of that organization.", organization_id=organization_id)
            yield dataclasses.replace(app, organization_id=organization_id, request_id=str(uuid.uuid4()))

        return _cm()


@pytest.fixture
def admission() -> Iterator[_Admission]:
    seam = _Admission({PERSON: {ORG_RUN, ORG_MEMBER}})
    previous = configure_organization_switch(seam)
    try:
        yield seam
    finally:
        configure_organization_switch(previous)


def _registry(*executors: _Where) -> NodeRegistry:
    reg = NodeRegistry()
    for ex in executors:
        reg.register(ex)
    return reg


def _definition(setting: Any, inputs: dict[str, Any], *, then: bool = True) -> dict[str, Any]:
    data: dict[str, Any] = {"config": {}, "input": inputs}
    if setting is not None:
        data["in_organization"] = setting
    nodes = [{"id": "there", "type": "test.where", "position": {"x": 0, "y": 0}, "data": data}]
    edges = []
    if then:
        nodes.append({"id": "after", "type": "test.after", "position": {"x": 1, "y": 0}, "data": {"config": {}, "input": {"text": "after"}}})
        edges.append({"id": "e1", "source": "there", "target": "after"})
    return {"nodes": nodes, "edges": edges}


async def _run(definition: dict[str, Any], reg: NodeRegistry, *, user: str = PERSON) -> Any:
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    app = dataclasses.replace(make_app_context(FakeEmitter()), organization_id=ORG_RUN, user_id=user)
    return await Scheduler(graph, MemoryCheckpointer(), app, registry=reg).run(run_id=f"run-{uuid.uuid4().hex[:8]}")


async def test_an_admitted_step_runs_and_bills_in_the_named_organization_and_only_that_step(admission):
    there, after = _Where("test.where"), _Where("test.after")
    result = await _run(_definition({"input": "organization_id"}, {"text": "x", "organization_id": ORG_MEMBER}), _registry(there, after))
    assert result.status is RunStatus.COMPLETED, result.error
    [row] = there.seen
    # The step's own context AND the ambient one (what every AI call, write and charge reads).
    assert row["ctx_org"] == ORG_MEMBER and row["ambient_org"] == ORG_MEMBER
    assert row["user"] == PERSON  # the actor is carried, never rebuilt
    assert row["text"] == "x"  # the closed step never saw the setting's input
    # Admitted before anything can stand in for the call (run once per key), then at the switch.
    assert set(admission.asked) == {(PERSON, ORG_MEMBER)}
    # The next step is back in the run's organization.
    assert after.seen[0]["ctx_org"] == ORG_RUN and after.seen[0]["ambient_org"] == ORG_RUN


async def test_a_person_who_is_not_a_member_is_refused_in_words_and_nothing_runs(admission):
    there, after = _Where("test.where"), _Where("test.after")
    result = await _run(_definition({"input": "organization_id"}, {"organization_id": ORG_STRANGER}), _registry(there, after))
    assert result.status is not RunStatus.COMPLETED
    assert there.seen == [] and after.seen == []
    assert "not a member" in str(result.error)
    assert admission.asked == [(PERSON, ORG_STRANGER)]


async def test_a_fixed_organization_is_admitted_the_same_way(admission):
    there, after = _Where("test.where"), _Where("test.after")
    result = await _run(_definition({"organization_id": ORG_MEMBER}, {"text": "y"}), _registry(there, after))
    assert result.status is RunStatus.COMPLETED, result.error
    assert there.seen[0]["ambient_org"] == ORG_MEMBER
    result = await _run(_definition({"organization_id": ORG_MEMBER}, {"text": "y"}), _registry(_Where("test.where"), _Where("test.after")), user="someone-else")
    assert result.status is not RunStatus.COMPLETED and "not a member" in str(result.error)


async def test_a_missing_organization_refuses_and_never_falls_back_to_the_run(admission):
    there = _Where("test.where")
    result = await _run(_definition({"input": "organization_id"}, {"text": "x"}, then=False), _registry(there))
    assert result.status is not RunStatus.COMPLETED
    assert there.seen == [] and admission.asked == []
    assert "got none" in str(result.error)


async def test_the_runs_own_organization_asks_nothing(admission):
    there = _Where("test.where")
    result = await _run(_definition({"input": "organization_id"}, {"organization_id": ORG_RUN}, then=False), _registry(there))
    assert result.status is RunStatus.COMPLETED, result.error
    assert there.seen[0]["ambient_org"] == ORG_RUN and admission.asked == []


async def test_a_host_with_no_admission_seam_never_switches():
    previous = configure_organization_switch(None)
    try:
        there = _Where("test.where")
        result = await _run(_definition({"input": "organization_id"}, {"organization_id": ORG_MEMBER}, then=False), _registry(there))
    finally:
        configure_organization_switch(previous)
    assert result.status is not RunStatus.COMPLETED and there.seen == []
    assert "cannot check membership" in str(result.error)


def test_a_malformed_setting_fails_compilation():
    reg = _registry(_Where("test.where"))
    with pytest.raises(CompilationError, match="in_organization"):
        compile_graph(Definition.model_validate(_definition({"input": "a", "organization_id": ORG_MEMBER}, {}, then=False)), registry=reg)
    with pytest.raises(CompilationError, match="not an organization id"):
        compile_graph(Definition.model_validate(_definition({"organization_id": "acme"}, {}, then=False)), registry=reg)


async def test_a_value_that_is_not_an_organization_id_refuses_in_words_before_anyone_is_asked(admission):
    """A malformed id never reaches the host's membership read (where it was a raw database error)."""
    there = _Where("test.where")
    result = await _run(_definition({"input": "organization_id"}, {"organization_id": "acme corp"}, then=False), _registry(there))
    assert result.status is not RunStatus.COMPLETED and there.seen == []
    assert "not an organization id" in str(result.error)
    assert admission.asked == []


@pytest.mark.parametrize("ending", ["raises", "cancelled"])
async def test_the_organization_is_given_back_when_the_step_raises_or_is_cancelled(admission, ending):
    """Whatever ends the step, its context and the ambient one are back in the run's organization."""
    import asyncio

    from matrx_connect.context.app_context import clear_app_context, get_app_context, set_app_context

    from matrx_graph.in_organization import in_organization

    app = dataclasses.replace(make_app_context(FakeEmitter()), organization_id=ORG_RUN, user_id=PERSON)
    token = set_app_context(app)
    try:
        ctx = type("Ctx", (), {"app": app})()
        failure = RuntimeError("boom") if ending == "raises" else asyncio.CancelledError()
        with pytest.raises(type(failure)):
            async with in_organization(ctx, ORG_MEMBER):
                assert ctx.app.organization_id == ORG_MEMBER == get_app_context().organization_id
                raise failure
        assert ctx.app is app and get_app_context() is app
    finally:
        clear_app_context(token)


@pytest.fixture
def once_store() -> Iterator[Any]:
    import time

    from matrx_graph import knobs
    from matrx_graph.once import MemoryStepResultStore, configure_step_result_store

    s = MemoryStepResultStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30, "miss_compare_limit": 10},
    )
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


def _once_in(org_setting: Any, inputs: dict[str, Any], *, shared: bool = False) -> dict[str, Any]:
    definition = _definition(org_setting, inputs, then=False)
    definition["nodes"][0]["data"]["once"] = {"key": ["text"], "scope": "organization", "share_across_users": shared}
    return definition


async def test_a_saved_result_from_another_organization_is_never_handed_to_a_non_member(admission, once_store):
    """Run once per key decides BEFORE the executor call: a person who is not a member of the step's
    organization must be refused there, never handed the result a member's run saved in it."""
    member_step = _Where("test.where")
    first = await _run(_once_in({"organization_id": ORG_MEMBER}, {"text": "q"}, shared=True), _registry(member_step))
    assert first.status is RunStatus.COMPLETED, first.error
    assert member_step.seen and member_step.seen[0]["ambient_org"] == ORG_MEMBER

    stranger_step = _Where("test.where")
    second = await _run(_once_in({"organization_id": ORG_MEMBER}, {"text": "q"}, shared=True), _registry(stranger_step), user="someone-else")
    assert second.status is not RunStatus.COMPLETED, "a non-member got the other organization's saved result"
    assert "not a member" in str(second.error)
    assert stranger_step.seen == []


async def test_a_saved_result_is_kept_in_the_organization_the_step_ran_in(admission, once_store):
    """Two items that differ only in the organization they run in never share a saved result."""
    admission.members[PERSON] = {ORG_RUN, ORG_MEMBER, ORG_STRANGER}
    there = _Where("test.where")
    for org in (ORG_MEMBER, ORG_STRANGER):
        result = await _run(_once_in({"input": "organization_id"}, {"text": "q", "organization_id": org}), _registry(there))
        assert result.status is RunStatus.COMPLETED, result.error
    assert [row["ambient_org"] for row in there.seen] == [ORG_MEMBER, ORG_STRANGER]
