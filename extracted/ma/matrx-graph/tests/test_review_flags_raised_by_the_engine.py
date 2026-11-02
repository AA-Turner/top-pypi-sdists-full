"""Guard (review flags, 0117 — 2026-10-17): the run SUCCEEDS and the engine records a review
flag for each thing that should never have been needed.

Author marks: ``data.review`` on a step flags every attempt that starts; on a connection it
flags every time the connection is TAKEN (never when pruned). Engine auto-flags: a retry, a
failure caught by an ERROR connection, an optional step failing, a fan-out item becoming a
hole, an output that does not match its kind. Every write goes through the ONE run_log writer
(swapped here for an in-memory recorder via ``configure_run_log_writer``) and a writer that
blows up never fails the run. A replayed outcome never re-raises a step flag, and a replayed
routing produces the SAME occurrence keys the writer dedupes on.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import run_log
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"


Behavior = Callable[[int, _Open, NodeExecutionContext], Any]


class _Step:
    def __init__(self, node_type: str, behavior: Behavior | None = None, *, attempts: int = 1) -> None:
        self.spec: NodeSpec = NodeSpec(
            type=node_type,
            category=NodeCategory.DATA,
            display_name=node_type,
            description="review-flag test node",
            input_schema=_Open,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
                HandleSpec(id="yes", direction=HandleDirection.OUTPUT),
                HandleSpec(id="no", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=RetryPolicy(max_attempts=attempts),
        )
        self.behavior = behavior or (lambda _c, _i, _ctx: success(_Out(text="ok")))
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        return self.behavior(self.calls, inputs, ctx)


class _Recorder:
    """In-memory stand-in for the run_log database path."""

    def __init__(self, *, explode: bool = False) -> None:
        self.rows: list[dict[str, Any]] = []
        self.explode = explode

    async def __call__(self, **kw: Any) -> RunLogEntry:
        if self.explode:
            raise RuntimeError("database is on fire")
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])

    def flags(self, label: str | None = None) -> list[dict[str, Any]]:
        return [r for r in self.rows if r["needs_review"] and (label is None or r["label"] == label)]


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


def _registry(*steps: _Step) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for s in steps:
        reg.register(s, overwrite=True)
    return reg


def _node(node_id: str, node_type: str, **data: Any) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}, **data}}


def _edge(edge_id: str, source: str, target: str, **data: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"id": edge_id, "source": source, "target": target, "data": {"kind": "data", **data}}
    handle = data.pop("source_handle", None)
    if handle:
        out["sourceHandle"] = handle
        out["data"].pop("source_handle", None)
    return out


async def _run(definition: dict[str, Any], registry: NodeRegistry, run_id: str, checkpointer: Any = None):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(
        graph, checkpointer or MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return await scheduler.run(run_id=run_id)


REVIEW = {"reason": "Fallback lookup should never be needed", "category": "fallback"}


# ── author mark on a step ────────────────────────────────────────────────────


async def test_a_flagged_step_raises_one_flag_each_time_it_runs(recorder: _Recorder):
    ok = _Step("test.rf_ok")
    definition = {
        "nodes": [_node("start", "test.rf_ok"), _node("fallback", "test.rf_ok", review=REVIEW)],
        "edges": [_edge("e1", "start", "fallback")],
    }
    result = await _run(definition, _registry(ok), "rf-step")
    assert result.status is RunStatus.COMPLETED, result.error
    flags = recorder.flags()
    assert len(flags) == 1, recorder.rows
    flag = flags[0]
    assert flag["label"] == "flagged_step.fallback"
    assert flag["source"] == "flagged_step"
    assert flag["category"] == "fallback"
    assert flag["node_id"] == "fallback"
    assert flag["message"] == REVIEW["reason"]
    assert flag["occurrence_key"]


async def test_an_unflagged_workflow_raises_nothing(recorder: _Recorder):
    definition = {
        "nodes": [_node("start", "test.rf_ok"), _node("next", "test.rf_ok")],
        "edges": [_edge("e1", "start", "next")],
    }
    result = await _run(definition, _registry(_Step("test.rf_ok")), "rf-none")
    assert result.status is RunStatus.COMPLETED
    assert recorder.flags() == []


async def test_a_flagged_step_with_a_custom_label_keeps_it(recorder: _Recorder):
    definition = {"nodes": [_node("solo", "test.rf_ok", review={**REVIEW, "label": "fixer_agent_ran"})], "edges": []}
    await _run(definition, _registry(_Step("test.rf_ok")), "rf-label")
    assert [f["label"] for f in recorder.flags()] == ["fixer_agent_ran"]


# ── author mark on a connection: taken vs pruned ─────────────────────────────


def _brancher(handle: str) -> _Step:
    def behavior(_c: int, _i: _Open, ctx: NodeExecutionContext) -> NodeResult[_Out]:
        ctx.emit(handle, {"text": handle})
        return success(_Out(text=handle))

    return _Step("test.rf_branch", behavior)


def _branch_definition() -> dict[str, Any]:
    return {
        "nodes": [
            _node("decide", "test.rf_branch"),
            _node("normal", "test.rf_ok"),
            _node("rescue", "test.rf_ok"),
        ],
        "edges": [
            _edge("e_yes", "decide", "normal", source_handle="yes"),
            _edge("e_no", "decide", "rescue", source_handle="no", review=REVIEW),
        ],
    }


async def test_a_flagged_connection_taken_raises_a_flag_on_its_target(recorder: _Recorder):
    result = await _run(_branch_definition(), _registry(_brancher("no"), _Step("test.rf_ok")), "rf-taken")
    assert result.status is RunStatus.COMPLETED, result.error
    flags = recorder.flags()
    assert len(flags) == 1, recorder.rows
    assert flags[0]["label"] == "flagged_path.e_no"
    assert flags[0]["source"] == "flagged_path"
    assert flags[0]["edge_id"] == "e_no"
    assert flags[0]["node_id"] == "rescue"


async def test_a_flagged_connection_pruned_raises_nothing(recorder: _Recorder):
    result = await _run(_branch_definition(), _registry(_brancher("yes"), _Step("test.rf_ok")), "rf-pruned")
    assert result.status is RunStatus.COMPLETED, result.error
    assert recorder.flags() == []


# ── engine auto-flags ────────────────────────────────────────────────────────


async def test_a_retry_raises_an_engine_retry_flag(recorder: _Recorder):
    def flaky(call: int, _i: _Open, _ctx: NodeExecutionContext) -> NodeResult[_Out]:
        if call == 1:
            raise RuntimeError("upstream timed out")
        return success(_Out(text="second time lucky"))

    flaky_step = _Step("test.rf_flaky", flaky, attempts=2)
    definition = {"nodes": [_node("fetch", "test.rf_flaky", review=REVIEW)], "edges": []}
    result = await _run(definition, _registry(flaky_step), "rf-retry")
    assert result.status is RunStatus.COMPLETED, result.error
    retries = recorder.flags("engine.retry")
    assert len(retries) == 1, recorder.rows
    assert retries[0]["category"] == "retry" and retries[0]["source"] == "engine"
    assert retries[0]["attempt"] == 1
    # The marked step started twice (attempt 1 and its retry) — one flag per attempt.
    assert sorted(f["attempt"] for f in recorder.flags("flagged_step.fetch")) == [1, 2]


def _boom(_c: int, _i: _Open, _ctx: NodeExecutionContext) -> NodeResult[_Out]:
    return failure("lookup_failed", "the primary source refused")


async def test_a_failure_caught_by_an_error_connection_raises_caught_failure(recorder: _Recorder):
    definition = {
        "nodes": [_node("primary", "test.rf_boom"), _node("handler", "test.rf_ok")],
        "edges": [{"id": "e_err", "source": "primary", "target": "handler", "data": {"kind": "error", "review": REVIEW}}],
    }
    result = await _run(definition, _registry(_Step("test.rf_boom", _boom), _Step("test.rf_ok")), "rf-caught")
    assert result.status is RunStatus.COMPLETED, result.error
    caught = recorder.flags("engine.caught_failure")
    assert len(caught) == 1, recorder.rows
    assert caught[0]["category"] == "recovered_error" and caught[0]["node_id"] == "primary"
    # The error connection carried a review mark and was taken.
    taken = recorder.flags("flagged_path.e_err")
    assert len(taken) == 1 and taken[0]["node_id"] == "handler"


async def test_an_optional_step_failure_raises_optional_step_failed(recorder: _Recorder):
    definition = {
        "nodes": [_node("start", "test.rf_ok"), _node("side", "test.rf_boom", optional=True)],
        "edges": [_edge("e1", "start", "side")],
    }
    result = await _run(definition, _registry(_Step("test.rf_ok"), _Step("test.rf_boom", _boom)), "rf-opt")
    assert result.status is RunStatus.COMPLETED, result.error
    flags = recorder.flags()
    assert [f["label"] for f in flags] == ["engine.optional_step_failed"], recorder.rows
    assert flags[0]["category"] == "recovered_error"


async def test_a_fan_out_hole_raises_item_skipped(recorder: _Recorder):
    def worker(_c: int, inputs: _Open, _ctx: NodeExecutionContext) -> NodeResult[_Out]:
        value = getattr(inputs, "value", None)
        if value == "bad":
            return failure("scrape_failed", "404 not found")
        return success(_Out(text=str(value)))

    definition = {
        "nodes": [
            {
                "id": "map1",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": "worker", "payload_key": "value"},
                    "input": {"items": ["good", "bad", "fine"]},
                },
            },
            _node("worker", "test.rf_worker", on_item_failure="hole"),
            _node("gather", "control.gather"),
        ],
        "edges": [{"id": "e_wg", "source": "worker", "target": "gather", "data": {"mappings": {"value": "text"}}}],
        "entry_nodes": ["map1"],
    }
    result = await _run(definition, _registry(_Step("test.rf_worker", worker)), "rf-hole")
    assert result.status is RunStatus.COMPLETED, result.error
    holes = recorder.flags("engine.item_skipped")
    assert len(holes) == 1, recorder.rows
    assert holes[0]["category"] == "skipped_item" and holes[0]["node_id"] == "worker"


# ── never fails the run; replay never double-flags ──────────────────────────


async def test_a_writer_that_explodes_never_fails_the_run():
    run_log.configure_run_log_writer(_Recorder(explode=True))
    try:
        definition = {"nodes": [_node("solo", "test.rf_ok", review=REVIEW)], "edges": []}
        result = await _run(definition, _registry(_Step("test.rf_ok")), "rf-explode")
        assert result.status is RunStatus.COMPLETED, result.error
    finally:
        run_log.configure_run_log_writer(None)


async def test_a_replayed_run_does_not_re_raise_step_flags_and_reuses_occurrence_keys(recorder: _Recorder):
    checkpointer = MemoryCheckpointer()
    registry = _registry(_brancher("no"), _Step("test.rf_ok"))
    definition = _branch_definition()
    definition["nodes"][2]["data"]["review"] = REVIEW  # flag the rescue step too
    first = await _run(definition, registry, "rf-replay", checkpointer)
    assert first.status is RunStatus.COMPLETED
    first_keys = {f["occurrence_key"] for f in recorder.flags()}
    assert {f["label"] for f in recorder.flags()} == {"flagged_path.e_no", "flagged_step.rescue"}

    recorder.rows.clear()
    again = await _run(definition, registry, "rf-replay", checkpointer)  # every outcome replays
    assert again.status is RunStatus.COMPLETED
    assert recorder.flags("flagged_step.rescue") == [], "a replayed outcome is not a new attempt"
    # Routing re-runs on replay; its flag carries the SAME occurrence key, which the
    # writer finds already recorded and does not write twice.
    assert {f["occurrence_key"] for f in recorder.flags()} <= first_keys


# ── validation offers, never blocks ─────────────────────────────────────────


def test_review_marks_validate_as_warnings():
    from matrx_graph.validation import validate_definition

    definition = _branch_definition()
    definition["nodes"][1]["data"]["review"] = {"reason": "", "category": "nonsense"}
    definition["edges"][0]["data"]["review"] = "please look"
    report = validate_definition(
        Definition.model_validate(definition), registry=_registry(_brancher("no"), _Step("test.rf_ok"))
    )
    review_issues = [i for i in report.issues if ".data.review" in i.path]
    paths = {i.path for i in review_issues}
    assert "nodes[normal].data.review.reason" in paths
    assert "nodes[normal].data.review.category" in paths
    assert "edges[e_yes].data.review" in paths
    assert all(i.severity == "warning" for i in review_issues)
    assert report.valid, "a review mark never blocks a workflow"


def test_review_marks_compile_onto_nodes_and_edges():
    definition = _branch_definition()
    definition["nodes"][1]["data"]["review"] = {"reason": "Should not run", "category": "bogus"}
    graph = compile_graph(Definition.model_validate(definition), registry=_registry(_brancher("no"), _Step("test.rf_ok")))
    assert graph.nodes["normal"].review is not None
    assert graph.nodes["normal"].review.category == "other", "unknown category reads as other"
    assert graph.edges["e_no"].review is not None and graph.edges["e_no"].review.category == "fallback"
    assert graph.edges["e_yes"].review is None


async def test_an_output_that_does_not_match_its_kind_raises_output_shape(
    recorder: _Recorder, monkeypatch: pytest.MonkeyPatch
):
    from matrx_graph import kinds as kinds_mod
    from matrx_graph.kinds import KindCheck

    async def wrong_shape(_value: Any, _slug: str) -> KindCheck:
        return KindCheck(checked=True, errors=["text: expected a list"], kind_version=1, kind_active=True)

    monkeypatch.setattr(kinds_mod, "check_against_kind", wrong_shape)
    monkeypatch.setattr(kinds_mod, "kind_enforcement_enabled", lambda _family: False)
    definition = {"nodes": [_node("draft", "test.rf_ok", output_kind="article_draft")], "edges": []}
    result = await _run(definition, _registry(_Step("test.rf_ok")), "rf-shape")
    assert result.status is RunStatus.COMPLETED, result.error
    shape = recorder.flags("engine.output_shape")
    assert len(shape) == 1, recorder.rows
    assert shape[0]["category"] == "degraded_output"
    assert shape[0]["payload"]["kind"] == "article_draft"
