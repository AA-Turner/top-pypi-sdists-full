"""R38 (Agent Factory review 6 N6-4 / N4-7): no run inside a tree escapes the root's cap,
and a run's lineage link names a request that has a record.

Live, by reading (review 6 §2):
* a workflow-holder mandate's step agent runs on ``fork_for_workflow_step`` — the ROOT's
  ``request_id`` with ``parent_request_id=None`` — so at finalize it read as the request
  owner and called ``release_tree_budget(<root>)``: the whole tree's spend reset to 0
  mid-tree;
* an assignment item ran on a fresh ``uuid5`` request id, unlinked: a fresh $25 per item;
* a root released while a detached child still ran: the child then accrued to a fresh 0;
* 99 of 112 ``metadata.parent_request_id`` links (3 h, live) named an ambient synthetic
  request no row carries.
Each test below was run RED on the code before this round.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.orchestrator import cost_budget

USER_ID = "22222222-2222-2222-2222-222222222222"
ROOT = "55555555-5555-5555-5555-555555555555"
CHILD = "66666666-6666-6666-6666-666666666666"


def _ctx(**kw: Any) -> Any:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext

    return AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=ROOT, store=False, **kw)


def test_a_workflow_step_never_owns_the_tree_it_runs_in() -> None:
    root_ctx = _ctx()
    step_ctx = root_ctx.fork_for_workflow_step("77777777-7777-7777-7777-777777777777")
    assert step_ctx.request_id == ROOT and step_ctx.parent_request_id is None  # the live shape
    assert cost_budget.owns_tree(root_ctx) is True
    assert cost_budget.owns_tree(step_ctx) is False
    assert cost_budget.owns_tree(None) is True


def test_the_executor_asks_owns_tree_before_releasing() -> None:
    from matrx_ai.orchestrator import executor

    src = inspect.getsource(executor)
    at = src.index("release_tree_budget(req_id)")
    window = src[at - 1500 : at]
    assert "owns_tree(" in window, "the finalize release must ask cost_budget.owns_tree, not parent_request_id alone"


def test_a_root_released_while_a_child_runs_keeps_the_trees_total(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cost_budget, "TREE_COST_CEILING_USD", 10.0)
    cost_budget.release_tree_budget(ROOT)
    cost_budget.record_tree_cost(ROOT, 7.0)
    cost_budget.link_tree_request(CHILD, ROOT)  # a detached child, still running
    cost_budget.release_tree_budget(ROOT)  # the root's own run finished first
    cost_budget.record_tree_cost(CHILD, 2.0)
    assert cost_budget.remaining_budget(CHILD) == pytest.approx(1.0)  # 10 − 7 − 2, never a fresh 0
    cost_budget.release_tree_budget(CHILD)  # the last member finishing closes the tree
    assert cost_budget.accrued_cost(ROOT) == 0.0
    assert cost_budget.tree_root_request_id(CHILD) == CHILD


def test_the_accumulator_maps_are_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cost_budget, "_MAX_TREES", 5)
    for i in range(20):
        cost_budget.record_tree_cost(f"tree-{i}", 1.0)
    assert len(cost_budget._accrued) <= 5
    for i in range(20):
        cost_budget.release_tree_budget(f"tree-{i}")


def test_an_assignment_item_is_linked_to_the_tree() -> None:
    from matrx_ai.graph_nodes import agent_assignment_action

    tree = ast.parse(Path(agent_assignment_action.__file__).read_text("utf-8"))
    execute = next(n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef) and n.name == "execute")
    calls = {
        (c.func.attr if isinstance(c.func, ast.Attribute) else getattr(c.func, "id", ""))
        for c in ast.walk(execute)
        if isinstance(c, ast.Call)
    }
    assert "link_tree_request" in calls, "an assignment item's own request id must spend against the tree"


def test_a_lineage_link_names_only_a_request_with_a_record() -> None:
    from matrx_ai.db import conversation_gate as gate

    unknown = "88888888-8888-8888-8888-888888888888"
    assert gate.request_has_record(unknown) is False  # an ambient synthetic id: no row
    gate.mark_request_durable(unknown)
    assert gate.request_has_record(unknown) is True


@pytest.mark.asyncio
async def test_an_independent_run_under_a_recordless_request_carries_no_dangling_link(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_connect.context.app_context import get_app_context, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.db.conversation_gate import PARENT_REQUEST_ID_KEY, mark_request_durable

    seen: list[dict[str, Any]] = []

    async def _run(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        seen.append(dict(get_app_context().metadata))
        return SimpleNamespace(output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
                               usage=None, usage_history=[], metadata={})

    def agent() -> Any:
        return SimpleNamespace(name="m", config=SimpleNamespace(model="m", metadata={}), source_id=None,
                               source_is_version=False, execute=_run, request_metadata={})

    synthetic = "99999999-9999-9999-9999-999999999999"
    set_app_context(_ctx().with_overrides(request_id=synthetic))
    await run_agent(agent(), label="m", source_app="t", source_feature="f",  # type: ignore[arg-type]
                    emit_lifecycle=False, system_run=True, independent_request=True)
    assert PARENT_REQUEST_ID_KEY not in seen[-1], "a link to a request no row carries dangles"
    # …and the tree cap still holds for it (R38 is in-memory, independent of rows).

    real = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    mark_request_durable(real)
    set_app_context(_ctx().with_overrides(request_id=real))
    await run_agent(agent(), label="m", source_app="t", source_feature="f",  # type: ignore[arg-type]
                    emit_lifecycle=False, system_run=True, independent_request=True)
    assert seen[-1].get(PARENT_REQUEST_ID_KEY) == real


@pytest.mark.asyncio
async def test_a_lineage_link_is_written_in_the_form_rows_carry() -> None:
    """Live round 8: the spine handed a hex-form id (no dashes); the link never joined."""
    from matrx_connect.context.app_context import get_app_context, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.db.conversation_gate import PARENT_REQUEST_ID_KEY, mark_request_durable

    seen: list[dict[str, Any]] = []

    async def _run(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        seen.append(dict(get_app_context().metadata))
        return SimpleNamespace(output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
                               usage=None, usage_history=[], metadata={})

    hexform = "d1de9a701e9c423eb0240807e9043833"
    mark_request_durable(hexform)
    set_app_context(_ctx().with_overrides(request_id=hexform))
    await run_agent(SimpleNamespace(name="m", config=SimpleNamespace(model="m", metadata={}), source_id=None,  # type: ignore[arg-type]
                                    source_is_version=False, execute=_run, request_metadata={}),
                    label="m", source_app="t", source_feature="f", emit_lifecycle=False, system_run=True,
                    independent_request=True)
    assert seen[-1].get(PARENT_REQUEST_ID_KEY) == "d1de9a70-1e9c-423e-b024-0807e9043833"
