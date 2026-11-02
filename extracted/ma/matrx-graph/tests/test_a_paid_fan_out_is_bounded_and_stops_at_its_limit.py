"""Guard (2026-10-27): a 200-item fan-out of paid steps is bounded, stops at its spend limit, never
re-dispatches a refusal, and reports exactly the cost its ledger holds.

Live evidence: run 1aa73a14 (workflow 90be8557). A ``control.map`` dispatched 199 paid
``ai.mandate.start`` items AT ONCE: ~141 paid calls ($1.49) landed in one minute before the $1-per-run
hold could fire, the pool (10 connections a process) saturated, and after the hold every refused item
was re-dispatched (615 node_failed, 3 resumes). The run's node_cost events said $0.46 while its ledger
held $2.25: items that raised or were cancelled after paying settled nothing.

The breaks each test names:
- the fan-out bound or the first-wave probe removed            → ``peak`` / ``first finished first`` fail
- the spend gate not asked per launch (or not latched)         → more than limit+bound items pay
- a caller refusal retried / re-run on replay                  → executor calls on refused items, retries
- the invocation spend tally not settled on raise              → node_cost sum != ledger
- the run's failure keeps "engine_error" for a refusal         → cause / approval_url assertions fail

Real ``Scheduler`` + ``MemoryCheckpointer``; the only doubles are the paid call itself (a counter that
writes one ledger row per call through ``note_request_spend`` — the host ledger writer's door) and the
host's spend gate (reads that ledger, refuses past the limit, exactly as aidream's does).
"""

from __future__ import annotations

import asyncio
from decimal import Decimal
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import knobs as graph_knobs
from matrx_graph.spend_gate import (
    SpendQuery,
    SpendRefusal,
    configure_spend_gate,
    note_request_spend,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

APPROVAL_URL = "https://manage.aimatrx.com/admin/automation/workflows/wf-quiz/approvals"


class _Item(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Card(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    usage: dict[str, JsonValue] = Field(default_factory=dict)


class _Ledger:
    """The host's ``chat.request`` for one run: one row per paid call, written through the door."""

    def __init__(self) -> None:
        self.rows: dict[str, Decimal] = {}

    def write(self, row_id: str, cost: Decimal) -> None:
        self.rows[row_id] = cost
        note_request_spend(row_id, cost=float(cost), input_tokens=120, output_tokens=40)

    @property
    def total(self) -> Decimal:
        return sum(self.rows.values(), start=Decimal(0))


class _QuizWriter:
    """A paid AI step: one flashcard per source paragraph. Every 7th paragraph pays, then raises
    (a save that timed out after the provider answered) — its spend must still be reported."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.quiz_writer",
        category=NodeCategory.AGENT,
        display_name="Write a flashcard",
        description="paid fan-out test step",
        input_schema=_Item,
        output_schema=_Card,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=3, initial_delay_ms=0),
    )

    def __init__(self, ledger: _Ledger, cost: Decimal) -> None:
        self.ledger = ledger
        self.cost = cost
        self.live = 0
        self.peak = 0
        self.calls: list[int] = []
        self.finished: list[int] = []
        self.started_before_first_finished = 0
        self.calls_at_refusal: int | None = None

    async def execute(self, ctx: NodeExecutionContext, inputs: _Item, config: _Cfg) -> NodeResult[_Card]:
        index = int(getattr(inputs, "index"))
        if self.calls and not self.finished:
            self.started_before_first_finished += 1
        self.calls.append(index)
        self.live += 1
        self.peak = max(self.peak, self.live)
        try:
            await asyncio.sleep(0.002)
            self.ledger.write(f"req-{index}-{len(self.calls)}", self.cost)
            if index % 7 == 3:
                raise RuntimeError("PoolAcquireTimeoutError: the answer could not be saved")
            return success(
                _Card(
                    question=f"What does paragraph {index} of the photosynthesis chapter say?",
                    usage={"cost_usd": float(self.cost), "input_tokens": 120, "output_tokens": 40},
                )
            )
        finally:
            self.live -= 1
            self.finished.append(index)


def _definition(count: int) -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "each_paragraph",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {
                        "target_node_id": "write_card",
                        "payload_key": "value",
                        "include_index": True,
                        "max_dispatches": 1000,
                    },
                    "input": {"items": [f"paragraph {i}" for i in range(count)]},
                },
            },
            {
                "id": "write_card",
                "type": "test.quiz_writer",
                "position": {"x": 0, "y": 0},
                "data": {"config": {}, "label": "Write a flashcard"},
            },
        ],
        "edges": [],
        "entry_nodes": ["each_paragraph"],
    }


@pytest.fixture
def bounded_policy(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(
            default_item_concurrency=4, max_item_concurrency=8, paid_first_wave=1
        )

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)
    yield
    configure_spend_gate(None)


def _gate(ledger: _Ledger, limit: Decimal, asked: list[str], writer: _QuizWriter):
    async def gate(query: SpendQuery) -> SpendRefusal | None:
        asked.append(query.node_id)
        if ledger.total <= limit:
            return None
        writer.calls_at_refusal = len(writer.calls)
        return SpendRefusal(
            code="run_spend_limit_reached",
            message="This run has spent more than its approval limit, so its remaining AI steps wait for an administrator to approve it.",
            approval_url=APPROVAL_URL,
        )

    return gate


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name]


async def _drive(count: int, cost: Decimal, limit: Decimal | None):
    ledger = _Ledger()
    writer = _QuizWriter(ledger, cost)
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(writer, overwrite=True)
    asked: list[str] = []
    configure_spend_gate(_gate(ledger, limit, asked, writer) if limit is not None else None)
    graph = compile_graph(Definition.model_validate(_definition(count)), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=f"paid-fan-out-{count}")
    return result, emitter, ledger, writer, asked, scheduler


def _node_cost_total(emitter: FakeEmitter) -> Decimal:
    return sum(
        (Decimal(str(e.get("cost_usd") or 0)) for e in _events(emitter, "node_cost")), start=Decimal(0)
    )


async def test_two_hundred_paid_items_run_four_at_a_time_after_one_probe(bounded_policy):
    result, emitter, ledger, writer, _asked, _ = await _drive(200, Decimal("0.004"), limit=None)
    # Every item ran (no limit), never more than the knob's 4 at once, and the probe ran ALONE.
    assert len(set(writer.calls)) == 200
    assert writer.peak == 4, writer.peak
    assert writer.started_before_first_finished == 0, "items launched before the first paid item settled"
    # The raising items retried (a save failure is retryable) — but every paid call is reported.
    assert ledger.total > Decimal("0.8")
    assert _node_cost_total(emitter) == ledger.total, (_node_cost_total(emitter), ledger.total)
    assert result.status is RunStatus.ERRORED  # the ~29 items that always raise park the run


async def test_the_run_stops_launching_paid_items_once_its_ledger_passes_the_limit(bounded_policy):
    cost, limit = Decimal("0.01"), Decimal("0.25")
    result, emitter, ledger, writer, asked, _ = await _drive(200, cost, limit=limit)

    # At most limit/cost paid calls, plus the ones already in flight (the bound) when it crossed.
    paid_calls = len(ledger.rows)
    assert paid_calls <= int(limit / cost) + 1 + 4, paid_calls
    assert paid_calls < 40, "the gate was not asked per launch"
    assert len(set(asked)) == 1 and len(asked) < 60, "a refusal must latch — later launches never ask again"

    # Once refused, no paid call STARTS again (an attempt already in flight finishes); a refused
    # item is never retried and ends once, as a refusal. An item that paid, raised and came back
    # for a retry after the limit is refused like the rest.
    assert writer.calls_at_refusal is not None
    assert len(writer.calls) == writer.calls_at_refusal, "a paid call started after the refusal"
    refused = [e for e in _events(emitter, "node_failed") if e.get("error_type") == "run_spend_limit_reached"]
    executed = set(writer.calls)
    refused_items = {e["item_index"] for e in refused}
    assert len(refused_items) == len(refused), "a refused item failed more than once"
    assert executed | refused_items == set(range(200))
    retries = [
        e for e in _events(emitter, "node_retry_scheduled") if e.get("error_type") == "run_spend_limit_reached"
    ]
    assert retries == []

    # The run parks honestly: the gate's sentence, the spend cause, and where to approve it.
    assert result.status is RunStatus.ERRORED
    assert result.failure is not None
    assert result.failure.cause == "spend_approval_required", result.failure
    assert result.failure.approval_url == APPROVAL_URL
    assert "approval limit" in result.failure.message
    assert "went wrong on our side" not in result.failure.message
    # And the cost truth: every paid call, including the ones that raised after paying.
    assert _node_cost_total(emitter) == ledger.total


async def test_a_launch_admitted_before_the_refusal_never_pays_after_it(bounded_policy, monkeypatch):
    # The CI race (run 40455895731), made certain: every admitted launch waits between the gate
    # and its paid call (here, on the step-clock knob), so siblings settle, cross the limit and
    # are refused while it waits. The latch must still stop it — no paid call starts after it.
    real_clock = graph_knobs.step_timeout_seconds

    async def _slow_clock(*args: Any, **kwargs: Any):
        await asyncio.sleep(0.01)
        return await real_clock(*args, **kwargs)

    monkeypatch.setattr(graph_knobs, "step_timeout_seconds", _slow_clock)
    cost, limit = Decimal("0.01"), Decimal("0.05")
    result, emitter, ledger, writer, _asked, _ = await _drive(60, cost, limit=limit)
    assert writer.calls_at_refusal is not None
    assert len(writer.calls) == writer.calls_at_refusal, "a paid call started after the refusal"
    refused = {
        e["item_index"]
        for e in _events(emitter, "node_failed")
        if e.get("error_type") == "run_spend_limit_reached"
    }
    assert set(writer.calls) | refused == set(range(60))
    assert result.status is RunStatus.ERRORED
    assert result.failure is not None and result.failure.cause == "spend_approval_required"
    assert _node_cost_total(emitter) == ledger.total


async def test_resuming_a_refused_run_never_re_dispatches_the_refused_items(bounded_policy):
    cost, limit = Decimal("0.01"), Decimal("0.05")
    result, emitter, ledger, writer, _asked, scheduler = await _drive(30, cost, limit=limit)
    assert result.status is RunStatus.ERRORED
    calls_before, rows_before = len(writer.calls), len(ledger.rows)
    refused_before = {
        e["item_index"]
        for e in _events(emitter, "node_failed")
        if e.get("error_type") == "run_spend_limit_reached"
    }
    assert refused_before

    # Recovery resumes the parked run (the incident's "auto_resume"). Nothing was approved.
    checkpoint = await scheduler.checkpointer.latest_checkpoint("paid-fan-out-30")
    assert checkpoint is not None
    resumed = await scheduler.resume(run_id="paid-fan-out-30", checkpoint_id=checkpoint.checkpoint_id)
    assert writer.calls[calls_before:] == [], "a refused item was dispatched again on resume"
    assert len(ledger.rows) == rows_before
    assert resumed.status is RunStatus.ERRORED
    assert resumed.failure is not None and resumed.failure.cause == "spend_approval_required"


async def test_a_run_under_its_limit_is_never_refused(bounded_policy):
    result, emitter, ledger, writer, asked, _ = await _drive(12, Decimal("0.001"), limit=Decimal("1"))
    assert len(set(writer.calls)) == 12
    assert not [e for e in _events(emitter, "node_failed") if e.get("error_type") == "run_spend_limit_reached"]
    assert len(asked) >= 12  # asked before every paid launch, including retries
