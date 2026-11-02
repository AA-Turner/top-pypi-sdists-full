"""A workflow step's persistence costs a FIXED number of database round trips — ten.

Every step of every run pays this between its own work and the next step's start, so
each round trip here is paid N times per run (live 2026-10-28: a 600-item data.rules /
data.dedupe step spent 1.6–1.9 s beyond its own work on ~15 serial round trips). The
ledger below mirrors what matrx-orm puts on the wire: a ``transaction()`` is BEGIN +
the declared-GUC statement on entry and COMMIT on exit; a write outside one is wrapped
in its own BEGIN / GUCs / COMMIT (4); a read or a statement inside a transaction is 1.

A steady-state step with a large output now costs:

* the outcome — its new values and the row in ONE transaction: BEGIN, GUCs, values,
  row, COMMIT = 5 (was: the values in their own transaction, 4, then the row, 4);
* the checkpoint — BEGIN, GUCs, row, run pointer, COMMIT = 5;
* the pause/cancel poll — 0: the run-pointer UPDATE returns the run's status, and that
  answer is the next boundary's poll (was: its own status read, 1).

Per step is measured as the difference between a 4-step and a 3-step run, so run setup
and the final save never blur it. A new round trip on this path fails here first.
"""

from __future__ import annotations

import contextlib
import types
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import Definition, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint import value_store
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

pytestmark = pytest.mark.asyncio

PER_STEP_ROUND_TRIPS = 10
INLINE_MAX = 4096


class _Any(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BigStep:
    """A data step whose output is over the inline limit — a 600-item list, in miniature."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.big_step",
        category=NodeCategory.DATA,
        display_name="big step",
        description="test step",
        input_schema=_Any,
        output_schema=_Any,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _Any, config: _Cfg) -> NodeResult[_Any]:
        return success(_Any(items=[f"{ctx.node_id} item {i} " + "x" * 64 for i in range(200)]))


class PureStep:
    """A PURE data step (Transform / Rules / Filter): milliseconds of work, replayable."""

    spec: ClassVar[NodeSpec] = BigStep.spec.model_copy(
        update={"node_type": "test.pure_step", "determinism": ActionTier.PURE}
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _Any, config: _Cfg) -> NodeResult[_Any]:
        return success(_Any(items=[f"{ctx.node_id} item {i}" for i in range(3)]))


class PureBigStep(BigStep):
    spec: ClassVar[NodeSpec] = BigStep.spec.model_copy(
        update={"node_type": "test.pure_big_step", "determinism": ActionTier.PURE}
    )


class Ledger:
    def __init__(self) -> None:
        self.round_trips = 0
        self.depth = 0

    def statement(self, *, write: bool) -> None:
        # A write outside a transaction is wrapped by the ORM: BEGIN, GUCs, it, COMMIT.
        self.round_trips += 1 if (self.depth or not write) else 4

    @contextlib.asynccontextmanager
    async def transaction(self, *_a: Any, **_k: Any):
        self.round_trips += 2
        self.depth += 1
        try:
            yield None
        finally:
            self.depth -= 1
            self.round_trips += 1


class _Query:
    def __init__(self, ledger: Ledger, status: str) -> None:
        self.ledger, self.status, self.cols = ledger, status, ("*",)

    def returning(self, *cols: str) -> _Query:
        self.cols = cols
        return self

    async def update(self, **_kw: Any) -> Any:
        self.ledger.statement(write=True)
        row = {"id": "x", "status": self.status}
        return types.SimpleNamespace(rows_affected=1, updated_rows=[{c: row[c] for c in self.cols if c in row}])


class _Models:
    def __init__(self, ledger: Ledger, org: str) -> None:
        self.ledger, self.org = ledger, org

    # WfRun
    async def get_or_none(self, **_kw: Any) -> Any:
        self.ledger.statement(write=False)
        return types.SimpleNamespace(organization_id=self.org)

    def filter(self, **_kw: Any) -> _Query:
        return _Query(self.ledger, "running")

    # WfCheckpoint / WfNodeOutcome / WfCheckpointValue
    _fields: ClassVar[dict[str, Any]] = {}

    async def insert_returning(self, data: dict[str, Any], **_kw: Any) -> dict[str, Any]:
        self.ledger.statement(write=True)
        return {"id": data["id"]}

    async def upsert(self, *_a: Any, **_kw: Any) -> None:
        self.ledger.statement(write=True)

    async def bulk_insert_ignore(self, *_a: Any, **_kw: Any) -> None:
        self.ledger.statement(write=True)


@pytest.fixture
def ledger(monkeypatch: pytest.MonkeyPatch) -> Ledger:
    led = Ledger()
    models = _Models(led, "11111111-1111-1111-1111-111111111111")
    monkeypatch.setattr(module, "get_model", lambda _key: models)
    monkeypatch.setattr(value_store, "get_model", lambda _key: models)
    monkeypatch.setattr(module, "_outcome_transaction", led.transaction, raising=False)
    monkeypatch.setattr(module, "_input_envelope_capability", None)
    monkeypatch.setattr(module, "_value_store_available", lambda: True)
    import sys

    stub = types.ModuleType("matrx_orm")
    stub.transaction = led.transaction  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matrx_orm", stub)
    policy = knobs.CheckpointWritePolicy(
        statement_timeout_ms=30_000, max_retries=0, retry_backoff_ms=1, warn_bytes=10_000_000,
        inline_value_max_bytes=INLINE_MAX,
    )

    async def _policy() -> knobs.CheckpointWritePolicy:
        return policy

    async def _inline() -> int:
        return INLINE_MAX

    async def _cache() -> int:
        return 64

    monkeypatch.setattr(module, "checkpoint_write_policy", _policy)
    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", _inline)
    monkeypatch.setattr(knobs, "run_org_cache_size", _cache)
    return led


async def _run(led: Ledger, steps: int, run_id: str, step_type: str = "test.big_step") -> int:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(BigStep(), overwrite=True)
    reg.register(PureStep(), overwrite=True)
    reg.register(PureBigStep(), overwrite=True)
    nodes = [
        {"id": f"s{i}", "type": step_type, "position": {"x": i, "y": 0}, "data": {"config": {}}}
        for i in range(steps)
    ]
    edges = [
        {"id": f"e{i}", "source": f"s{i}", "target": f"s{i + 1}", "data": {"kind": "data", "mappings": {"items": "items"}}}
        for i in range(steps - 1)
    ]
    graph = compile_graph(Definition.model_validate({"nodes": nodes, "edges": edges}), registry=reg)

    async def _control_check() -> str:
        led.statement(write=False)  # run_store.control_status: one read of the run's status
        return "running"

    before = led.round_trips
    result = await Scheduler(
        graph,
        module.PostgresCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=reg,
        control_check=_control_check,
        control_check_reads_own_row=True,
        fresh_history=True,
    ).run(run_id=run_id)
    assert result.status is RunStatus.COMPLETED, result.error
    return led.round_trips - before


async def test_a_step_with_a_large_output_costs_ten_round_trips(ledger: Ledger) -> None:
    from uuid import uuid4

    three = await _run(ledger, 3, str(uuid4()))
    four = await _run(ledger, 4, str(uuid4()))

    assert four - three == PER_STEP_ROUND_TRIPS, (
        f"one more step cost {four - three} database round trips, not {PER_STEP_ROUND_TRIPS} "
        "— something on the per-step persistence path went back to its own transaction or read"
    )


async def test_the_status_the_checkpoint_read_is_the_boundary_poll(ledger: Ledger) -> None:
    from uuid import uuid4

    polls: list[str] = []
    real = module.PostgresCheckpointer.pop_run_status

    def _pop(self: Any, run_id: str) -> str | None:
        got = real(self, run_id)
        polls.append(str(got))
        return got

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(module.PostgresCheckpointer, "pop_run_status", _pop)
        await _run(ledger, 3, str(uuid4()))

    assert polls and all(p == "running" for p in polls), polls


# A super-step of only PURE members lands its outcomes in the checkpoint's own transaction
# (Scheduler._step_defers_outcomes, 2026-10-29): one BEGIN / GUCs / COMMIT for the step, not two.
# Live before: a pure Transform cost ~9 round trips (~63 ms on ECS); the planning sub-run of Smart
# Add is eleven of them in a row.
PURE_STEP_ROUND_TRIPS = 6  # BEGIN, GUCs, outcome row, checkpoint row, run pointer, COMMIT
PURE_BIG_STEP_ROUND_TRIPS = 7  # ... plus the output's by-reference values, in the same transaction


@pytest.mark.parametrize(
    ("step_type", "budget"),
    [("test.pure_step", PURE_STEP_ROUND_TRIPS), ("test.pure_big_step", PURE_BIG_STEP_ROUND_TRIPS)],
)
async def test_a_pure_step_writes_its_outcome_inside_its_checkpoint(ledger: Ledger, step_type: str, budget: int) -> None:
    from uuid import uuid4

    three = await _run(ledger, 3, str(uuid4()), step_type)
    four = await _run(ledger, 4, str(uuid4()), step_type)

    assert four - three == budget, (
        f"one more PURE step cost {four - three} database round trips, not {budget} — its outcome "
        "went back to a transaction of its own instead of riding the step's checkpoint"
    )


async def test_a_pure_steps_outcome_lands_before_its_completion_event(ledger: Ledger) -> None:
    """The outcome row is written before node_completed leaves, and node_completed before
    checkpoint_saved — the order every reader of the event stream relies on."""
    from uuid import uuid4

    order: list[str] = []
    real_upsert = _Models.upsert

    async def _upsert(self: Any, *a: Any, **k: Any) -> None:
        order.append("outcome_row")
        await real_upsert(self, *a, **k)

    emitter = FakeEmitter()
    real_send = emitter.send_data

    async def _send(payload: Any) -> None:
        name = getattr(payload, "event", None)
        if name in ("node_completed", "checkpoint_saved"):
            order.append(str(name))
        await real_send(payload)

    emitter.send_data = _send  # type: ignore[method-assign]
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(PureStep(), overwrite=True)
    graph = compile_graph(
        Definition.model_validate({"nodes": [
            {"id": "a", "type": "test.pure_step", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ], "edges": []}),
        registry=reg,
    )
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(_Models, "upsert", _upsert)
        result = await Scheduler(
            graph, module.PostgresCheckpointer(), make_app_context(emitter), registry=reg, fresh_history=True
        ).run(run_id=str(uuid4()))
    assert result.status is RunStatus.COMPLETED, result.error
    assert order == ["outcome_row", "node_completed", "checkpoint_saved"], order
