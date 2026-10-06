"""R38 (Agent Factory review 5 N5-4): every run keeps its own request record, but its
spend always counts toward its ROOT tree's cap.

44728051ad made every ``run_mandate`` run ``independent_request=True``. The tree-wide
dollar ceiling (``cost_budget``) was keyed by the run's own ``request_id``, so a mandate
run inside an agent tree accrued to a fresh, empty accumulator: a parent fanning out
mandate runs was no longer bounded by ``TREE_COST_CEILING_USD``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.orchestrator import cost_budget

USER_ID = "22222222-2222-2222-2222-222222222222"
ROOT = "44444444-4444-4444-4444-444444444444"


@pytest.mark.asyncio
async def test_a_mandate_run_inside_a_tree_is_capped_by_the_trees_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    """The run's own record is fresh; what it spends — and what it may still spend — is the tree's."""
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, get_app_context, set_app_context

    from matrx_ai.agents.executor import run_agent

    monkeypatch.setattr(cost_budget, "TREE_COST_CEILING_USD", 10.0)
    cost_budget.forget_tree(ROOT)  # a clean tree (a release keeps a tree whose members still run)
    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=ROOT, store=False))
    cost_budget.record_tree_cost(ROOT, 6.0)  # the parent tree has already spent $6
    seen: dict[str, Any] = {}

    async def _spend(user_input: Any = None, *, max_iterations: Any = None) -> Any:
        own = get_app_context().request_id
        # what the orchestrator does per billed call and before each tool round
        cost_budget.record_tree_cost(own, 3.0)
        seen.update(own=own, remaining=cost_budget.remaining_budget(own))
        return SimpleNamespace(output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
                               usage=None, usage_history=[], metadata={})

    agent = SimpleNamespace(name="m", config=SimpleNamespace(model="m", metadata={}), source_id=None,
                            source_is_version=False, execute=_spend, request_metadata={"mandate_key": "x.y"})
    result = await run_agent(agent, label="mandate", source_app="t", source_feature="mandate:x.y",  # type: ignore[arg-type]
                             emit_lifecycle=False, system_run=True, independent_request=True)
    assert result.success
    assert seen["own"] != ROOT  # its own request record (N4-7) …
    assert seen["remaining"] == pytest.approx(1.0)  # … capped by the TREE: 10 − 6 − 3
    assert cost_budget.remaining_budget(ROOT) == pytest.approx(1.0)
    assert cost_budget.tree_root_request_id(seen["own"]) == ROOT
    # A second mandate run that would cross the ceiling sees the tree exhausted.
    cost_budget.record_tree_cost(seen["own"], 2.0)
    assert cost_budget.remaining_budget(ROOT) < 0
    cost_budget.forget_tree(ROOT)


def test_a_child_finishing_never_releases_the_trees_total() -> None:
    cost_budget.forget_tree(ROOT)
    child, grandchild = "c-1", "g-1"
    cost_budget.link_tree_request(child, ROOT)
    cost_budget.link_tree_request(grandchild, child)  # nested independent runs reach the same root
    cost_budget.record_tree_cost(grandchild, 4.0)
    assert cost_budget.accrued_cost(ROOT) == pytest.approx(4.0)
    cost_budget.release_tree_budget(grandchild)  # the child's own request owner finalizes
    cost_budget.release_tree_budget(child)
    assert cost_budget.accrued_cost(ROOT) == pytest.approx(4.0)
    cost_budget.release_tree_budget(ROOT)
    assert cost_budget.accrued_cost(ROOT) == 0.0 and cost_budget.tree_root_request_id(child) == child
