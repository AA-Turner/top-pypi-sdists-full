"""THE declared result IS the run's answer (P5 Daily close walk, 2026-11-15).

A workflow declares its result by marking ONE step ``data.is_primary`` — the Studio's
"Use as the workflow's result" switch and the ``set_result`` patch op write that same field.
``run_answer`` must hand that step's output back FIRST (and say it was declared), even when the
step is in the middle of the chain and a later terminal step also settled; with no mark it
falls back to the last terminal step and says it was NOT declared. Every page that shows a
workflow's result reads this answer, so this is the contract P3's placed face relies on.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.types.deliverables import run_answer
from tests.test_a_spend_limit_is_read_only_after_a_step_that_may_spend import _chain
from tests.test_scheduler_ready_nodes_do_not_wait import _Sleeper


def _graph(mark: str | None):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Sleeper())
    definition = _chain(None)
    if mark is not None:
        for node in definition.nodes:
            if node.id == mark:
                node.data["is_primary"] = True
                node.data["deliverable"] = True
    return compile_graph(definition, registry=registry), definition


OUTPUTS = {nid: {"rows": [nid]} for nid in ("a", "b", "c", "d")}


def test_the_marked_middle_step_answers_and_says_it_was_declared() -> None:
    graph, definition = _graph("b")
    answer = run_answer(graph, definition, OUTPUTS)
    assert answer is not None
    assert answer.step == "b"
    assert answer.value == {"rows": ["b"]}
    assert answer.declared is True


def test_with_no_mark_the_last_step_answers_and_is_not_declared() -> None:
    graph, definition = _graph(None)
    answer = run_answer(graph, definition, OUTPUTS)
    assert answer is not None
    assert answer.step == "d"
    assert answer.declared is False


def test_a_marked_step_that_did_not_settle_falls_back_honestly() -> None:
    graph, definition = _graph("b")
    outputs = {k: v for k, v in OUTPUTS.items() if k != "b"}
    answer = run_answer(graph, definition, outputs)
    assert answer is not None and answer.step == "d" and answer.declared is False
