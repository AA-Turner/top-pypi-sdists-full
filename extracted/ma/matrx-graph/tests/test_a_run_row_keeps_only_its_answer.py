"""A finished run's ROW keeps only its answer steps (L-SPEED round 6a, item 2).

Every step's output was interned into ``workflow.run.output`` at the terminal write, though each step
already has its ``node_outcome`` row. ``CompiledGraph.row_output_ids`` (deliverables, the declared
result, every terminal non-dispatcher step — what ``run_answer`` can choose from) and ``row_outputs``
cut the row to those; the answer a run gives is unchanged.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.types.deliverables import row_outputs, run_answer
from tests.test_a_spend_limit_is_read_only_after_a_step_that_may_spend import _chain
from tests.test_scheduler_ready_nodes_do_not_wait import _Sleeper


def _graph():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Sleeper())
    definition = _chain(None)
    return compile_graph(definition, registry=registry), definition


def test_by_default_the_row_keeps_every_step_readers_still_use() -> None:
    """The 2026-11-09 review: servers read a NON-terminal step from ``run.output`` (podcast race
    ``w0_out``). Until every reader goes through the one step reader, the row keeps every step."""
    graph, _ = _graph()
    outputs = {nid: {"value": nid} for nid in ("a", "b", "c", "d")}
    assert row_outputs(graph, outputs) == outputs


def test_the_row_keeps_the_terminal_step_and_drops_the_middle(monkeypatch) -> None:
    from matrx_graph.types import deliverables

    monkeypatch.setattr(deliverables, "TRIM_RUN_ROW", True)
    graph, definition = _graph()
    outputs = {nid: {"value": nid} for nid in ("a", "b", "c", "d")}
    kept = row_outputs(graph, outputs)
    assert set(kept) == {"d"}, kept
    full = run_answer(graph, definition, outputs)
    cut = run_answer(graph, definition, kept)
    assert full is not None and cut is not None and full.value == cut.value and full.step == cut.step


def test_without_a_compiled_set_or_a_step_map_nothing_is_cut(monkeypatch) -> None:
    from matrx_graph.types import deliverables

    monkeypatch.setattr(deliverables, "TRIM_RUN_ROW", True)
    outputs = {"a": 1, "b": 2}
    assert row_outputs(None, outputs) is outputs
    graph, _ = _graph()
    assert row_outputs(graph, {"a": 1}) == {"a": 1}  # nothing of the answer settled: the row keeps what there is
    assert row_outputs(graph, None) is None
