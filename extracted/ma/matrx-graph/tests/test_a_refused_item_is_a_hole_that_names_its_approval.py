"""Guard (2026-10-27): a For Each item refused by a spend approval is a HOLE that says so.

Live evidence: shared unit "Run a mandate over a list" (mandate.run_each, c50a9cdd), run 5c5db16c.
Its Run Mandate step declares ``on_item_failure: "hole"``; Arman had declined the approval for
``news.coarse_relevance``, so every call was refused. The run completed with 29 holes, each carrying
``details.approval_id`` / ``approval_url`` / ``caller_refusal`` — but the hole's ``cause`` read
``engine_error`` ("something went wrong on our side"), because the per-item outcome classified the
step's returned failure by its code (``ai_turn_failed``) instead of by the refusal it carries. A
workflow branching on ``$item.error.cause`` could not tell a refusal from a crash, and the skipped-item
review flag never named where to approve it.

The rules this file pins (each test names the break that turns it red):

- a refused fanned item under ``hole`` becomes a hole; its siblings succeed; the run completes
  → hole/route logic removed: run ERRORS (in-test red proof below)
- the hole's error reads ``cause: spend_approval_required`` with the approval id and link
  → refusal classified by code again: ``cause == "engine_error"``
- a refusal is final: never retried, never re-asked on resume  → executor called again
- the skipped-item review flag says "refused" and carries the approval id and link
- WITHOUT ``hole`` the run still stops on the refusal (unchanged), with the refusal's cause

Real ``Scheduler`` + ``MemoryCheckpointer``; the only double is the paid step, which returns the same
failure shape ``ai.mandate.start`` returns for a declined approval (live outcome of run 5c5db16c).
"""

from __future__ import annotations

from collections.abc import Iterator
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
from matrx_graph.executor.scheduler import Scheduler as _SchedulerClass
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context

APPROVAL_ID = "c74aa333-b163-4db2-b25e-6483b56573c5"
APPROVAL_URL = "https://manage.aimatrx.com/admin/intelligence/mandates/news.story_origin/approvals"
DECLINED = "An administrator declined this agent's spending, so it was not run."
STORIES = ["Harbor bridge reopens", "Mayor announces budget", "Storm closes schools", "Ferry fares rise"]
REFUSED_INDEX = 2


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_public: str


def _spec(node_type: str, category: NodeCategory) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=category,
        display_name=node_type,
        description="approval-refusal hole test node",
        input_schema=_Open,
        output_schema=_Finding,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=3, initial_delay_ms=0),
    )


class _OriginFinder:
    """A paid AI step: when did this story first become public? The mandate behind one story is
    on a declined approval, so that call is refused exactly as ``ai.mandate.start`` refuses it."""

    spec: ClassVar[NodeSpec] = _spec("test.origin_finder", NodeCategory.AGENT)

    def __init__(self) -> None:
        self.calls: list[str] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Finding]:
        story = str(getattr(inputs, "value", ""))
        self.calls.append(story)
        if story == STORIES[REFUSED_INDEX]:
            return failure(
                "ai_turn_failed",
                DECLINED,
                details={
                    "usage": {"cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0},
                    "reason": "declined",
                    "status": "failed",
                    "error_type": "run_approval_required",
                    "subject_id": "news.story_origin",
                    "subject_kind": "mandate",
                    "approval_id": APPROVAL_ID,
                    "approval_url": APPROVAL_URL,
                    "refusal_code": "run_approval_required",
                    "caller_refusal": True,
                },
                technical=f"AI turn ended with status 'failed' (run_approval_required): {DECLINED}",
            )
        return success(_Finding(first_public=f"{story}: 2026-10-27T08:00:00Z"))


class _Report:
    """The step after the gather; fails ``fail_times`` times (a save that timed out) and then works —
    so a run can park AFTER the fan-out and be resumed."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.origin_report",
        category=NodeCategory.DATA,
        display_name="Report",
        description="approval-refusal hole test node",
        input_schema=_Open,
        output_schema=_Open,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )

    def __init__(self, fail_times: int = 0) -> None:
        self.fail_times = fail_times
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Open]:
        self.seen.append(inputs.model_dump())
        if self.fail_times > 0:
            self.fail_times -= 1
            raise RuntimeError("PoolAcquireTimeoutError: the report could not be saved")
        return success(_Open(done=True))


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


def _definition(*, hole: bool) -> dict[str, Any]:
    finder_data: dict[str, Any] = {"config": {}, "label": "When did it first become public?"}
    if hole:
        finder_data["on_item_failure"] = "hole"
    return {
        "nodes": [
            {
                "id": "each_story",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": "origin", "payload_key": "value", "max_dispatches": 40},
                    "input": {"items": STORIES},
                },
            },
            {"id": "origin", "type": "test.origin_finder", "position": {"x": 0, "y": 0}, "data": finder_data},
            {"id": "findings", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "report", "type": "test.origin_report", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ],
        "edges": [
            {"id": "e_of", "source": "origin", "target": "findings", "data": {"mappings": {"value": "first_public"}}},
            {"id": "e_fr", "source": "findings", "target": "report", "data": {"kind": "data"}},
        ],
        "entry_nodes": ["each_story"],
    }


def _scheduler(*, hole: bool, report: _Report, finder: _OriginFinder) -> tuple[Scheduler, FakeEmitter]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(finder, overwrite=True)
    registry.register(report, overwrite=True)
    graph = compile_graph(Definition.model_validate(_definition(hole=hole)), registry=registry)
    emitter = FakeEmitter()
    return Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry), emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name]


async def test_a_refused_item_is_a_hole_and_its_siblings_still_answer(recorder):
    finder, report = _OriginFinder(), _Report()
    scheduler, emitter = _scheduler(hole=True, report=report, finder=finder)
    result = await scheduler.run(run_id="origin-hole")

    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["findings"]
    assert gathered["count"] == 3 and gathered["expected"] == 4
    assert gathered["item_indexes"] == [0, 1, 3]
    assert report.seen, "the step after the gather ran with the three findings and the hole"

    # A refusal is final: the refused story was asked ONCE, never retried (max_attempts=3).
    assert finder.calls.count(STORIES[REFUSED_INDEX]) == 1, finder.calls
    assert not [e for e in _events(emitter, "node_retry_scheduled") if e.get("item_index") == REFUSED_INDEX]

    # The hole says what happened and where a person acts on it.
    (hole,) = gathered["holes"]
    assert hole["item_index"] == REFUSED_INDEX and hole["status"] == "failed"
    error = hole["error"]
    assert error["cause"] == "spend_approval_required", error
    assert error["message"] == DECLINED
    assert error["details"]["approval_id"] == APPROVAL_ID
    assert error["details"]["approval_url"] == APPROVAL_URL
    assert error["details"]["caller_refusal"] is True


async def test_the_skipped_item_flag_says_refused_and_names_the_approval(recorder):
    finder, report = _OriginFinder(), _Report()
    scheduler, _ = _scheduler(hole=True, report=report, finder=finder)
    await scheduler.run(run_id="origin-hole-flag")

    skipped = [r for r in recorder.rows if r["needs_review"] and r["label"] == "engine.item_skipped"]
    assert len(skipped) == 1, recorder.rows
    flag = skipped[0]
    assert "refused" in flag["message"] and APPROVAL_URL in flag["message"], flag["message"]
    payload = flag.get("payload") or {}
    assert payload.get("approval_id") == APPROVAL_ID, payload
    assert payload.get("approval_url") == APPROVAL_URL, payload
    assert payload.get("cause") == "spend_approval_required", payload


async def test_resuming_after_the_fan_out_never_asks_the_refused_item_again(recorder):
    finder, report = _OriginFinder(), _Report(fail_times=1)
    scheduler, _ = _scheduler(hole=True, report=report, finder=finder)
    first = await scheduler.run(run_id="origin-hole-resume")
    assert first.status is RunStatus.ERRORED, "the report's save failure parks the run after the fan-out"
    calls_before = list(finder.calls)
    assert calls_before.count(STORIES[REFUSED_INDEX]) == 1

    checkpoint = await scheduler.checkpointer.latest_checkpoint("origin-hole-resume")
    assert checkpoint is not None
    # Recovery resumes the parked run (the "auto_resume" path). Nothing was approved.
    await scheduler.resume(run_id="origin-hole-resume", checkpoint_id=checkpoint.checkpoint_id)
    assert finder.calls == calls_before, "a refused (or answered) item was asked again on resume"


async def test_without_hole_the_refusal_still_stops_the_run(recorder):
    finder, report = _OriginFinder(), _Report()
    scheduler, _ = _scheduler(hole=False, report=report, finder=finder)
    result = await scheduler.run(run_id="origin-no-hole")

    assert result.status is RunStatus.ERRORED
    assert not report.seen, "nothing after the fan-out ran"
    assert finder.calls.count(STORIES[REFUSED_INDEX]) == 1, "a refusal is never retried"
    assert result.failure is not None
    assert result.failure.cause == "spend_approval_required", result.failure
    assert result.failure.approval_url == APPROVAL_URL


async def test_red_proof_the_hole_is_what_keeps_the_run_going(recorder, monkeypatch):
    """In-test red proof: with the hole routing removed, the SAME refused item errors the run — so
    the first test's COMPLETED is the hole's doing, not an accident of the fixture."""
    original = _SchedulerClass._failure_is_routable

    def _no_hole(self: Any, node: Any, invocation: Any) -> bool:
        if invocation.dispatch_id and node.on_item_failure == "hole":
            return False
        return original(self, node, invocation)

    monkeypatch.setattr(_SchedulerClass, "_failure_is_routable", _no_hole)
    finder, report = _OriginFinder(), _Report()
    scheduler, _ = _scheduler(hole=True, report=report, finder=finder)
    result = await scheduler.run(run_id="origin-hole-red")
    assert result.status is RunStatus.ERRORED
