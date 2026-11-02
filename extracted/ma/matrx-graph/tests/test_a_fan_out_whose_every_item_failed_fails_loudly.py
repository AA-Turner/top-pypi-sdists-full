"""Guard (2026-10-22): a fan-out whose EVERY dispatched item failed fails the run loudly.

Live evidence: system workflow Brand discovery, run 87452569 — ``curate_map`` (control.map)
dispatched 16 calls to the fail-soft (``data.optional``) mandate step ``curate``; all 16 failed
(MandateResolutionError), every outgoing edge pruned, ``curate_gather`` and ``curate_land`` never
ran, and the run ended ``completed`` with ``error`` NULL. A screen or monitor saw success while the
stage did nothing.

The rule: ``data.optional`` lets SOME items fail and the run goes on (each failed item stays
visible as a ``node_failed`` event and a review flag). When EVERY fanned invocation of an optional
step in one super-step failed — across all its dispatches, counting items of the same dispatch that
settled in an earlier step (a resume) — the run parks ERRORED on that step with ONE summary of the
children's errors. Out of scope, by design (2026-10-22 review F1-F5): ``on_item_failure='hole'``
(gather receives the holes, so something reaches the steps after it), a failure routed over an
ERROR connection (author-handled), work-queue items (the queue owns failure accounting) and loop
iterations after the first (an earlier iteration already delivered).
"""

from __future__ import annotations

from typing import Any, ClassVar

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


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="all-failed fan-out test node",
        input_schema=_Open,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )


class _Worker:
    """Fails every item whose value starts with ``bad``; raises for ``boom``."""

    spec: ClassVar[NodeSpec] = _spec("test.allfail_worker")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        value = str(getattr(inputs, "value", ""))
        if value.startswith("boom"):
            raise RuntimeError("MandateResolutionError: brand_record_id: guaranteed offer missing")
        if value.startswith("bad"):
            return failure("mandate_unresolved", f"no holder for {value}")
        return success(_Out(text=value.upper()))


class _After:
    spec: ClassVar[NodeSpec] = _spec("test.allfail_after")

    def __init__(self) -> None:
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.seen.append(inputs.model_dump())
        return success(_Out(text="landed"))


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _definition(items: list[str], *, worker_data: dict[str, Any], error_edge: bool = False) -> dict:
    nodes = [
        {
            "id": "fan",
            "type": "control.map",
            "position": {"x": 0, "y": 0},
            "data": {
                "config": {"target_node_id": "worker", "payload_key": "value", "max_dispatches": 40},
                "input": {"items": items},
            },
        },
        {
            "id": "worker",
            "type": "test.allfail_worker",
            "position": {"x": 0, "y": 0},
            "data": {"config": {}, "label": "Suggest where each candidate belongs", **worker_data},
        },
        {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        {"id": "land", "type": "test.allfail_after", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
    ]
    edges = [
        {"id": "e_wg", "source": "worker", "target": "gather", "data": {"mappings": {"value": "text"}}},
        {"id": "e_gl", "source": "gather", "target": "land", "data": {"kind": "data"}},
    ]
    if error_edge:
        nodes.append(
            {"id": "handler", "type": "test.allfail_after", "position": {"x": 0, "y": 0}, "data": {"config": {}}}
        )
        edges.append({"id": "e_err", "source": "worker", "target": "handler", "data": {"kind": "error"}})
    return {"nodes": nodes, "edges": edges, "entry_nodes": ["fan"]}


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id), emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name]


# --- every item failed: loud --------------------------------------------------------------


async def test_an_optional_fan_out_whose_every_item_failed_errors_the_run_with_a_summary():
    land = _After()
    result, emitter = await _run(
        _definition(["boom1", "boom2", "bad3"], worker_data={"optional": True}),
        _registry(_Worker(), land),
        "allfail-optional",
    )
    assert result.status is RunStatus.ERRORED, "an all-failed stage must never read as a clean success"
    assert not _events(emitter, "run_completed")
    errored = _events(emitter, "run_errored")
    assert len(errored) == 1
    assert errored[0]["node_id"] == "worker"
    assert "All 3 items" in errored[0]["error_message"], errored[0]
    message = result.error or ""
    assert "All 3 items" in message, message
    assert "Suggest where each candidate belongs" in message, message
    # The children's errors, summarized by kind with counts.
    assert "×2" in message and "guaranteed offer" in message, message
    assert "no holder for bad3" in message, message
    assert "0 of 3 invocations in this step completed" in message, message
    # F5: one clean summary — the escalated items share one error, never re-listed as "more".
    assert "more invocation(s) failed" not in message, message
    assert message.count("All 3 items") == 1, message
    assert result.failure is not None
    assert not land.seen, "nothing downstream ran"


async def test_a_hole_fan_out_whose_every_item_failed_delivers_its_holes_downstream():
    """F1: under ``hole`` the gather receives every failed item as a hole, so the step after it
    runs and can report them — never escalated, never "nothing reached the steps after it"."""
    land = _After()
    result, _ = await _run(
        _definition(["bad1", "bad2"], worker_data={"on_item_failure": "hole"}),
        _registry(_Worker(), land),
        "allfail-hole",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["gather"]
    assert gathered["count"] == 0 and gathered["expected"] == 2
    assert len(gathered["holes"]) == 2
    assert land.seen, "the step after the gather ran and received the holes"


async def test_a_single_item_optional_fan_out_that_failed_errors_the_run():
    result, _ = await _run(
        _definition(["boom"], worker_data={"optional": True}), _registry(_Worker(), _After()), "allfail-one"
    )
    assert result.status is RunStatus.ERRORED
    assert "All 1 item" in (result.error or "")


# --- partial failure: today's behavior, visible -------------------------------------------


async def test_an_optional_fan_out_with_some_failed_items_completes_and_counts_them():
    land = _After()
    result, emitter = await _run(
        _definition(["good", "boom", "fine", "bad"], worker_data={"optional": True}),
        _registry(_Worker(), land),
        "partial-optional",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["gather"]
    assert sorted(gathered["values"]) == ["FINE", "GOOD"]
    assert land.seen, "the stage landed what succeeded"
    failed = [e for e in _events(emitter, "node_failed") if e["node_id"] == "worker"]
    assert len(failed) == 2, "each failed item stays visible as its own node_failed event"


async def test_a_hole_fan_out_with_some_failed_items_reports_its_holes():
    result, _ = await _run(
        _definition(["good", "bad"], worker_data={"on_item_failure": "hole"}),
        _registry(_Worker(), _After()),
        "partial-hole",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["gather"]
    assert gathered["count"] == 1 and gathered["expected"] == 2
    assert len(gathered["holes"]) == 1


# --- an author-handled failure path is unchanged ------------------------------------------


async def test_an_all_failed_fan_out_with_an_error_connection_is_handled_by_its_author():
    handler = _After()
    result, _ = await _run(
        _definition(["bad1", "bad2"], worker_data={"optional": True}, error_edge=True),
        _registry(_Worker(), _After(), handler),
        "allfail-error-edge",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert handler.seen, "the ERROR connection received the failures"


# --- nested fan-out: judged per step across every dispatch (F2) ---------------------------


def _nested(outer: list[list[str]]) -> dict:
    return {
        "entry_nodes": ["outer"],
        "nodes": [
            {
                "id": "outer",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": "inner", "payload_key": "items", "max_dispatches": 40},
                    "input": {"items": outer},
                },
            },
            {
                "id": "inner",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"target_node_id": "worker", "payload_key": "value", "max_dispatches": 40}},
            },
            {
                "id": "worker",
                "type": "test.allfail_worker",
                "position": {"x": 0, "y": 0},
                "data": {"config": {}, "optional": True},
            },
            {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "land", "type": "test.allfail_after", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ],
        "edges": [
            {"id": "e_wg", "source": "worker", "target": "gather", "data": {"mappings": {"value": "text"}}},
            {"id": "e_gl", "source": "gather", "target": "land", "data": {"kind": "data"}},
        ],
    }


async def test_a_nested_fan_out_with_one_all_failed_inner_group_still_completes():
    land = _After()
    result, _ = await _run(
        _nested([["bad1"], ["good2", "good3"]]), _registry(_Worker(), land), "nested-partial"
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(result.last_outputs["gather"]["values"]) == ["GOOD2", "GOOD3"]
    assert land.seen


async def test_a_nested_fan_out_whose_every_inner_item_failed_errors_the_run():
    land = _After()
    result, _ = await _run(
        _nested([["bad1"], ["bad2", "bad3"]]), _registry(_Worker(), land), "nested-allfail"
    )
    assert result.status is RunStatus.ERRORED
    assert "All 3 items" in (result.error or ""), result.error
    assert not land.seen


# --- loop iterations (F3) -----------------------------------------------------------------


class _LoopBody:
    spec: ClassVar[NodeSpec] = _spec("test.allfail_loop_body")

    def __init__(self, fail_on: int) -> None:
        self.fail_on = fail_on
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        if self.calls == self.fail_on:
            return failure("transient", f"iteration {self.calls} failed")
        return success(_Out(text=f"it{self.calls}"))


def _loop(body_data: dict[str, Any]) -> dict:
    return {
        "entry_nodes": ["start"],
        "nodes": [
            {"id": "start", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "0"}}},
            {
                "id": "loop",
                "type": "control.loop",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"target_node_id": "body", "max_iterations": 3, "exit_expression": "1 > 2"}},
            },
            {
                "id": "body",
                "type": "test.allfail_loop_body",
                "position": {"x": 0, "y": 0},
                "data": {"config": {}, **body_data},
            },
            {"id": "final", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "'DONE'"}}},
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "loop"},
            {"id": "e2", "source": "body", "target": "loop"},
            {"id": "e3", "source": "loop", "sourceHandle": "done", "target": "final"},
        ],
    }


async def test_a_hole_loop_body_failing_one_iteration_keeps_looping():
    body = _LoopBody(fail_on=2)
    result, _ = await _run(_loop({"on_item_failure": "hole"}), _registry(body), "loop-hole")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs.get("final") is not None, "the loop finished and the step after it ran"


async def test_an_optional_loop_body_failing_a_later_iteration_is_not_escalated():
    body = _LoopBody(fail_on=2)
    result, _ = await _run(_loop({"optional": True}), _registry(body), "loop-optional-later")
    assert result.status is RunStatus.COMPLETED, result.error


async def test_an_optional_loop_body_failing_its_first_iteration_errors_the_run():
    body = _LoopBody(fail_on=1)
    result, _ = await _run(_loop({"optional": True}), _registry(body), "loop-optional-first")
    assert result.status is RunStatus.ERRORED
    assert "All 1 item" in (result.error or ""), result.error


# --- work-queue waves (F3) ----------------------------------------------------------------


async def test_a_work_queue_wave_whose_items_all_failed_does_not_error_the_run():
    from matrx_graph import MemoryWorkSetStore, configure_work_set_store
    from matrx_graph.workset import get_work_set_store
    from tests.test_workset import _CrawlWorker, _Report

    configure_work_set_store(MemoryWorkSetStore())
    try:
        worker = _CrawlWorker(pages={"a": ["x", "y"], "b": []}, fail_urls={"x", "y"})
        definition = {
            "nodes": [
                {
                    "id": "seed",
                    "type": "control.work_seed",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"key_template": "$item.url"},
                        "input": {"items": [{"url": "a"}, {"url": "b"}]},
                    },
                },
                {
                    "id": "queue",
                    "type": "control.work_queue",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"target_node_id": "crawl", "batch_size": 2}},
                },
                {"id": "crawl", "type": "test.crawl_worker", "position": {"x": 0, "y": 0}, "data": {"config": {}, "optional": True}},
                {"id": "report", "type": "test.report", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            ],
            "edges": [
                {"id": "e_seed_queue", "source": "seed", "target": "queue", "data": {}},
                {
                    "id": "e_queue_done",
                    "source": "queue",
                    "sourceHandle": "done",
                    "target": "report",
                    "data": {"mappings": {"value": "$FULL_PAYLOAD"}},
                },
            ],
            "entry_nodes": ["seed"],
        }
        reg = _registry(worker, _Report())
        result, _ = await _run(definition, reg, "wq-wave-allfail")
        assert result.status is RunStatus.COMPLETED, result.error
        counts = await get_work_set_store().counts(result.run_id, "default")
        assert counts.succeeded == 2 and counts.failed == 2
        assert counts.in_progress == 0, "no work item is left leased"
    finally:
        configure_work_set_store(None)


# --- items settling across a human-input gate (F4) ----------------------------------------


class _GateWorker:
    """``ask`` interrupts on its first attempt and fails once re-run; ``bad`` fails."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.allfail_gate_worker",
        category=NodeCategory.DATA,
        display_name="gate worker",
        description="all-failed fan-out test node",
        input_schema=_Open,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
        can_interrupt=True,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        value = str(getattr(inputs, "value", ""))
        if value.startswith("ask"):
            if ctx.attempt == 1:
                ctx.interrupt({"prompt": f"confirm {value}?"})
            return failure("rejected", f"{value} rejected after the answer")
        return failure("mandate_unresolved", f"no holder for {value}")


async def test_items_that_all_fail_around_a_human_input_gate_still_error_the_run():
    from uuid import uuid4

    from matrx_graph.checkpoint.protocol import Checkpoint

    land = _After()
    definition = _definition(["bad1", "ask2", "bad3"], worker_data={"optional": True})
    definition["nodes"][1]["type"] = "test.allfail_gate_worker"
    reg = _registry(_GateWorker(), land)
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    cp = MemoryCheckpointer()
    first = await Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=reg).run(run_id="gate")
    assert first.status is RunStatus.INTERRUPTED
    last = await cp.latest_checkpoint("gate")
    # Re-run the gated item (attempt bump, the way retry does) — it now fails too.
    bumped = [
        ni.model_copy(update={"attempt": ni.attempt + 1, "is_interrupted": False})
        if ni.node_id == "worker"
        else ni
        for ni in last.next_invocations
    ]
    cid = str(uuid4())
    await cp.save_checkpoint(
        Checkpoint(
            checkpoint_id=cid,
            run_id="gate",
            thread_id=last.thread_id,
            parent_checkpoint_id=last.checkpoint_id,
            step=last.step,
            channel_values=last.channel_values,
            pending_bindings=last.pending_bindings,
            next_invocations=bumped,
            interrupt_payload=None,
        )
    )
    resumed = await Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=reg).resume("gate", cid)
    assert resumed.status is RunStatus.ERRORED, "all 3 items failed — never a silent completion"
    message = resumed.error or ""
    assert "All 3 items" in message, message
    assert "rejected after the answer" in message and "no holder for bad1" in message, message
    assert not land.seen
