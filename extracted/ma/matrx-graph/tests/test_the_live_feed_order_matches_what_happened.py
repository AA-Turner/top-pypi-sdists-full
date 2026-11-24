"""The live feed tells a run in the order it happened (benchmark ladder, 2026-11-12).

Pure steps hold their outcome ROWS for the step's (or the chain's) one checkpoint transaction. Their
``node_completed`` events used to wait with the rows, so the feed read: the next step started, a later
step FAILED, the run errored ... and only then did the earlier steps say they had completed (seen live on
the errors rung: ``node_started x3, node_failed, node_completed, node_completed, run_errored``). The rows
may wait; the announcement never does. A step's completion is on the feed before anything that came after
it, and before its own ``checkpoint_saved`` (the chain contract stays).

Red before: in both runs below a later step's start (or failure) preceded an earlier step's completion.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph import register_builtin_nodes
from tests._fixtures import FakeEmitter, make_app_context


def _chain(last_expression: str) -> Definition:
    exprs = ["{'n': 12 + 6}", "{'n': inputs['n'] / 2}", last_expression]
    nodes = [
        {"id": f"t{i}", "type": "data.transform", "position": {"x": i * 200, "y": 0},
         "data": {"label": f"Step {i}", "config": {"expression": e}}}
        for i, e in enumerate(exprs)
    ]
    edges = [
        {"id": f"e{i}", "source": f"t{i}", "target": f"t{i + 1}", "data": {"kind": "data", "mappings": {"n": "n"}}}
        for i in range(len(exprs) - 1)
    ]
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["t0"]})


def _feed(emitter: FakeEmitter) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    for kind, payload in emitter.events:
        if kind == "data" and isinstance(payload, dict):
            name = str(payload.get("event"))
            out.append((name, payload.get("step") if name == "checkpoint_saved" else payload.get("node_id")))
    return out


async def _run(definition: Definition, run_id: str) -> tuple[Any, list[tuple[str, Any]]]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    emitter = FakeEmitter()
    graph = compile_graph(definition, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id=run_id
    )
    return result, _feed(emitter)


def _assert_in_order(feed: list[tuple[str, Any]], done: list[str]) -> None:
    for i, node in enumerate(done):
        completed = feed.index(("node_completed", node))
        nxt = f"t{i + 1}"
        for later in (("node_started", nxt), ("node_failed", nxt), ("node_completed", nxt)):
            if later in feed:
                assert completed < feed.index(later), f"{later} came before ('node_completed', {node!r}): {feed}"


async def test_a_successful_chain_announces_each_completion_before_the_next_step() -> None:
    result, feed = await _run(_chain("{'n': inputs['n'] + 0}"), "order-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    _assert_in_order(feed, ["t0", "t1", "t2"])
    for i in range(3):
        assert feed.index(("node_completed", f"t{i}")) < feed.index(("checkpoint_saved", i)), feed


async def test_a_failing_run_announces_earlier_completions_before_the_failure() -> None:
    result, feed = await _run(_chain("{'n': inputs['n'] / 0}"), "order-fail")
    assert result.status is not RunStatus.COMPLETED
    _assert_in_order(feed, ["t0", "t1"])
    stop = next(i for i, (name, _) in enumerate(feed) if name in ("run_errored", "run_failed"))
    assert feed.index(("node_failed", "t2")) < stop, feed
