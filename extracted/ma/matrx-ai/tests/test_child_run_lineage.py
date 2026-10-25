"""Every child agent run owns its own turn — and still spends, is admitted and is
stopped as part of its tree.

Owner ruling 2026-10-23: a child run is recorded exactly like a normal chat. The fork
mints the child's own ``request_id`` (its own ``chat.user_request``); lineage is the
``parent_request_id`` / ``root_request_id`` COLUMNS, written by the one writer rule
(``conversation_gate.lineage_columns``). Before it, ``agent_call`` / ``agent_tool`` /
visual-map repair children ran on their caller's id and filed their rows, cost and
outcome on the caller's turn; only callers that passed ``independent_request=True``
got a row of their own (with the link in metadata, lost at completion).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

USER_ID = "22222222-2222-2222-2222-222222222222"
PARENT = "33333333-3333-4333-8333-333333333333"
ORG = "44444444-4444-4444-8444-444444444444"
OTHER_ORG = "55555555-5555-4555-8555-555555555555"


def _ctx(**kw: Any) -> Any:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext

    fields: dict[str, Any] = {"emitter": ConsoleEmitter(), "user_id": USER_ID, "request_id": PARENT, "store": False}
    fields.update(kw)
    return AppContext(**fields)


def _agent(execute: Any, **kw: Any) -> Any:
    return SimpleNamespace(
        name="m", config=SimpleNamespace(model="m", metadata={}), source_id=None,
        source_is_version=False, execute=execute, request_metadata=dict(kw),
    )


def _result() -> Any:
    return SimpleNamespace(output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
                           usage=None, usage_history=[], metadata={})


@pytest.mark.asyncio
async def test_every_child_run_owns_its_turn_and_names_its_tree() -> None:
    """agent_call / agent_tool / mandate / fan-out children: no flag, each its own turn."""
    from matrx_connect.context.app_context import get_app_context, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(_ctx(conversation_id="66666666-6666-4666-8666-666666666666"))
    seen: list[Any] = []

    async def _capture(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        seen.append(get_app_context())
        return _result()

    for step in ("goal", "tool_choice", "instructions"):
        result = await run_agent(_agent(_capture), label=step, source_app="t", source_feature="agent_call",  # type: ignore[arg-type]
                                 emit_lifecycle=False)
        assert result.success
    ids = [c.request_id for c in seen]
    assert len(set(ids)) == 3 and PARENT not in ids, ids
    assert all(c.parent_request_id == PARENT and c.tree_request_id == PARENT for c in seen)


class _FakeUserRequests:
    def __init__(self, rows: dict[str, Any]) -> None:
        self.rows = rows
        self.reads: list[str] = []

    async def filter_user_requests(self, id: str) -> list[Any]:  # noqa: A002 — the manager's own signature
        self.reads.append(id)
        row = self.rows.get(id)
        return [row] if row is not None else []


@pytest.fixture
def fake_rows(monkeypatch: pytest.MonkeyPatch) -> _FakeUserRequests:
    from matrx_ai.db import conversation_gate as gate

    fake = _FakeUserRequests({})
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=fake))
    gate._request_org_memo.clear()
    return fake


@pytest.mark.asyncio
async def test_the_parent_link_names_a_real_row_of_the_same_organization_or_nothing(fake_rows: Any) -> None:
    from matrx_ai.db.conversation_gate import lineage_columns

    own = "77777777-7777-4777-8777-777777777777"
    # A synthetic parent (an MCP / machine request no row carries): root kept, no FK link.
    got = await lineage_columns(own_request_id=own, parent_request_id=PARENT, root_request_id=PARENT,
                                organization_id=ORG)
    assert got == {"root_request_id": PARENT}
    # A real parent row in the same organization: linked.
    fake_rows.rows[PARENT] = SimpleNamespace(organization_id=ORG)
    got = await lineage_columns(own_request_id=own, parent_request_id=PARENT, root_request_id=PARENT,
                                organization_id=ORG)
    assert got == {"root_request_id": PARENT, "parent_request_id": PARENT}
    # A parent filed in another organization: never a cross-org link (assert_same_org would refuse).
    got = await lineage_columns(own_request_id=own, parent_request_id=PARENT, root_request_id=PARENT,
                                organization_id=OTHER_ORG)
    assert got == {"root_request_id": PARENT}
    # A top-level turn has no lineage at all.
    assert await lineage_columns(own_request_id=own, parent_request_id=None, root_request_id=None,
                                 organization_id=ORG) == {}


@pytest.mark.asyncio
async def test_a_link_is_written_in_the_form_rows_carry(fake_rows: Any) -> None:
    """Live round 8: the spine handed a hex-form id (no dashes); the link never joined."""
    from matrx_ai.db.conversation_gate import lineage_columns

    dashed = "d1de9a70-1e9c-423e-b024-0807e9043833"
    fake_rows.rows[dashed] = SimpleNamespace(organization_id=ORG)
    got = await lineage_columns(own_request_id="77777777-7777-4777-8777-777777777777",
                                parent_request_id=dashed.replace("-", ""),
                                root_request_id=dashed.replace("-", ""), organization_id=ORG)
    assert got == {"root_request_id": dashed, "parent_request_id": dashed}


@pytest.mark.asyncio
async def test_a_parent_ensured_in_this_process_links_without_a_read(fake_rows: Any) -> None:
    """A parent row still queued in its coordinator is not readable yet; the writer's memo knows it."""
    from matrx_ai.db.conversation_gate import _stamp_lineage

    parent_row: dict[str, Any] = {"id": PARENT, "organization_id": ORG}
    await _stamp_lineage(parent_row, _ctx())
    child = _ctx().fork_for_child_agent("66666666-6666-4666-8666-666666666666")
    row: dict[str, Any] = {"id": child.request_id, "organization_id": ORG}
    await _stamp_lineage(row, child)
    assert row["parent_request_id"] == PARENT and row["root_request_id"] == PARENT
    assert fake_rows.reads == []


@pytest.mark.asyncio
async def test_a_resumed_turn_reads_its_tree_back_from_its_row(fake_rows: Any) -> None:
    from matrx_ai.db.conversation_gate import request_lineage

    own = "77777777-7777-4777-8777-777777777777"
    fake_rows.rows[own] = SimpleNamespace(parent_request_id=PARENT, root_request_id=PARENT)
    lineage = await request_lineage(own)
    assert lineage == {"parent_request_id": PARENT, "root_request_id": PARENT}
    resumed = _ctx(request_id=own).with_overrides(**lineage)
    assert resumed.tree_request_id == PARENT
    assert await request_lineage("not-a-uuid") == {"parent_request_id": None, "root_request_id": None}


def test_the_spend_cap_holds_across_a_child_that_outlives_its_root(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.orchestrator import cost_budget

    monkeypatch.setattr(cost_budget, "TREE_COST_CEILING_USD", 10.0)
    cost_budget.forget_tree(PARENT)
    root = _ctx()
    child = root.fork_for_child_agent("66666666-6666-4666-8666-666666666666")
    cost_budget.join_tree(child)  # the child's run start, before it spends anything
    cost_budget.record_tree_cost(PARENT, 7.0)
    cost_budget.release_tree_budget(PARENT)  # the root's own run finished first
    # The detached child spends against the TREE, never a fresh accumulator.
    cost_budget.record_tree_cost(child.request_id, 2.0, root_request_id=child.root_request_id)
    assert cost_budget.remaining_budget(child.request_id) == pytest.approx(1.0)
    # A child finalizing releases its OWN link (the owns_tree leak): the closed tree goes with it.
    assert cost_budget.owns_tree(child) is True
    cost_budget.release_tree_budget(child.request_id)
    assert cost_budget.accrued_cost(PARENT) == 0.0
    assert cost_budget.tree_root_request_id(child.request_id) == child.request_id


def test_a_child_that_has_not_spent_reads_its_roots_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_connect.context.app_context import set_app_context

    from matrx_ai.orchestrator import cost_budget

    monkeypatch.setattr(cost_budget, "TREE_COST_CEILING_USD", 10.0)
    cost_budget.forget_tree(PARENT)
    cost_budget.record_tree_cost(PARENT, 9.5)
    child = _ctx().fork_for_child_agent("66666666-6666-4666-8666-666666666666")
    set_app_context(child)
    assert cost_budget.remaining_budget(child.request_id) == pytest.approx(0.5)
    cost_budget.forget_tree(PARENT)


@pytest.mark.asyncio
async def test_fan_out_siblings_are_admitted_once_by_their_tree() -> None:
    from matrx_connect.context.app_context import set_app_context

    from matrx_ai.providers import usage_gate
    from matrx_ai.providers.usage_gate import UsageVerdict

    asked: list[str] = []

    def _resolver(user_id: str) -> UsageVerdict:
        asked.append(user_id)
        return UsageVerdict(state="ok", refuse=False, enforced=True)

    usage_gate.reset_usage_gate_state()
    usage_gate.set_usage_verdict_resolver(_resolver)
    try:
        root = _ctx(conversation_id="66666666-6666-4666-8666-666666666666", origin_class="human")
        first = root.fork_for_child_agent("77777777-7777-4777-8777-777777777777").with_overrides(origin_class="human")
        second = root.fork_for_child_agent("88888888-8888-4888-8888-888888888888").with_overrides(origin_class="human")
        set_app_context(first)
        await usage_gate.admit_paid_call()  # the tree's first paid call is in a child
        # The person crosses the line mid-action: a sibling is still never judged afresh.
        usage_gate.set_usage_verdict_resolver(lambda _u: UsageVerdict(state="over", refuse=True, enforced=True))
        set_app_context(second)
        await usage_gate.admit_paid_call()
        assert asked == [USER_ID]
    finally:
        usage_gate.set_usage_verdict_resolver(None)
        usage_gate.reset_usage_gate_state()


def test_run_approval_admits_a_tree_once() -> None:
    from matrx_connect.context.app_context import set_app_context

    from matrx_ai.providers import run_approval_gate

    calls: list[str] = []

    def _resolver(ctx: Any) -> Any:
        calls.append(ctx.request_id)
        return None

    run_approval_gate.reset_run_approval_gate_state()
    run_approval_gate.set_run_approval_resolver(_resolver)
    try:
        root = _ctx(conversation_id="66666666-6666-4666-8666-666666666666", origin_class="scheduled")
        first = root.fork_for_child_agent("77777777-7777-4777-8777-777777777777")
        second = root.fork_for_child_agent("88888888-8888-4888-8888-888888888888")
        set_app_context(first)
        run_approval_gate.admit_run_approval()
        set_app_context(second)
        run_approval_gate.admit_run_approval()
        assert calls == [first.request_id]
    finally:
        run_approval_gate.set_run_approval_resolver(None)
        run_approval_gate.reset_run_approval_gate_state()


def test_stop_on_a_child_id_stops_the_tree() -> None:
    from matrx_connect.request_controls import RequestControlRegistry, register_request_tree

    from matrx_ai.orchestrator import executor

    previous = RequestControlRegistry._instance
    RequestControlRegistry._instance = RequestControlRegistry()
    try:
        root = _ctx(conversation_id="66666666-6666-4666-8666-666666666666")
        helper = root.fork_for_child_agent("77777777-7777-4777-8777-777777777777")
        sibling = root.fork_for_child_agent("88888888-8888-4888-8888-888888888888")
        register_request_tree(helper)
        register_request_tree(sibling)
        assert not executor._is_request_cancelled(helper.request_id)
        asyncio.run(RequestControlRegistry.get_instance().cancel(helper.request_id))
        assert executor._is_request_cancelled(PARENT)
        assert executor._is_request_cancelled(sibling.request_id)
        assert executor._is_request_cancelled(helper.request_id)
    finally:
        RequestControlRegistry._instance = previous


def test_the_executor_links_every_run_to_its_tree_at_start() -> None:
    """A run rebuilt from its row in another process (resume, crash re-run) carries
    ``root_request_id``; the executor's entry links it before anything spends or polls."""
    from matrx_utils.source_guard import stable_source

    from matrx_ai.orchestrator import executor

    src = stable_source(executor.execute_ai_request)
    assert "join_tree(ctx)" in src and "register_request_tree(ctx)" in src
