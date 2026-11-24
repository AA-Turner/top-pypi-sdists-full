"""A batch of checkpoints names a settled large value ONCE, and the reference survives checkpoint,
resume and Pause.

2026-11-02 (L-SPEED, research pick child): a chain of pure steps lands as one save of up to nine
checkpoints, and every one of them re-walked and re-hashed the same ~10 MB of join bindings — 3.9 s on
the server, for values that were already stored. Ruled the same day (Arman): large values move
between steps and through checkpoints by reference — stored once, content-addressed, passed as a
small marker. ``InternMemo`` keys the interning of one save on the live objects, so each settled
value is walked and hashed once per save, and ``checkpoint_columns`` no longer deep-copies the
waiting bindings' payloads (a copy is a stranger to the memo).

Red before the fix: ``checkpoint_columns`` had no memo, so the batch hashed every checkpoint's copy.
"""

from __future__ import annotations

import hashlib
import json
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
from matrx_graph.checkpoint import values as values_module
from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation, NodeOutcome, PendingBinding
from matrx_graph.checkpoint.values import InternMemo, checkpoint_columns, referenced_hashes, resolve_values
from matrx_graph.knobs import STARTING_CHECKPOINT_POLICY
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_checkpoint_rows_stay_small import _Blob, _round_shape

LIMIT = STARTING_CHECKPOINT_POLICY.inline_value_max_bytes
LEDGER = [{"platform": "instagram", "handle": f"acct_{i}", "raw": "x" * 1000, "n": i} for i in range(300)]


class _HashedBytes:
    """Counts every byte ``values.py`` hashes."""

    def __init__(self) -> None:
        self.total = 0

    def sha256(self, data: bytes = b"") -> Any:
        self.total += len(data)
        return hashlib.sha256(data)


class _Live(MemoryCheckpointer):
    """Keeps each checkpoint exactly as the scheduler handed it (a chain's queue holds them live)."""

    def __init__(self) -> None:
        super().__init__()
        self.live: list[Checkpoint] = []
        self.at_save: list[dict[str, Any]] = []

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        cols, vals = checkpoint_columns(checkpoint, LIMIT)
        self.at_save.append({c: resolve_values(cols[c], vals) for c in ("channel_values", "pending_bindings", "next_invocations")})
        self.live.append(checkpoint)
        await super().save_checkpoint(checkpoint)


async def _wide_round() -> _Live:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Blob())
    checkpointer = _Live()
    scheduler = Scheduler(compile_graph(_round_shape(), registry=registry), checkpointer,
                          make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="lspeed-memo-round")
    assert result.status is RunStatus.COMPLETED, result.error
    return checkpointer


def _json(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


async def test_one_batch_hashes_each_settled_value_once_and_writes_the_same_rows(monkeypatch) -> None:
    cp = await _wide_round()
    assert len(cp.live) >= 5, "the round must save several checkpoints naming the same ledger"

    alone = _HashedBytes()
    monkeypatch.setattr(values_module, "hashlib", alone)
    for checkpoint in cp.live:
        checkpoint_columns(checkpoint, LIMIT)

    batched = _HashedBytes()
    monkeypatch.setattr(values_module, "hashlib", batched)
    memo = InternMemo()
    rows = [checkpoint_columns(checkpoint, LIMIT, memo)[0] for checkpoint in cp.live]

    assert batched.total * 3 < alone.total, (
        f"a batch of {len(cp.live)} checkpoints hashed {batched.total:,} bytes; one at a time hashed "
        f"{alone.total:,} — the settled ledger must be hashed once per batch, not once per checkpoint"
    )
    store = _json(memo.store)
    for row, at_save in zip(rows, cp.at_save, strict=True):
        assert referenced_hashes(row) <= set(store), "every reference a batch row names is in the batch's store"
        for col, value in at_save.items():
            assert resolve_values(_json(row[col]), store) == _json(value), (
                f"a batched row's {col} differs from the same checkpoint serialized when it was saved"
            )


# ── the reference through a real pause and resume ─────────────────────────────────────────────────


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Ledger:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.ledger", category=NodeCategory.DATA, display_name="Ledger", description="A 330 KB ledger.",
        input_schema=_In, output_schema=_Out, config_schema=_Cfg,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),
                 HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        return success(_Out(ledger=[dict(e) for e in LEDGER], question="Which accounts matter?"))


class _Echo:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.echo", category=NodeCategory.DATA, display_name="Echo", description="Hands its inputs on.",
        input_schema=_In, output_schema=_Out, config_schema=_Cfg,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),
                 HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        return success(_Out(**inputs.model_dump()))


class _ByReference(MemoryCheckpointer):
    """Saves like Postgres: each row interned (one memo per save, a chain is one save), JSON round
    tripped, its values in the run's store; a load resolves the references back."""

    def __init__(self) -> None:
        super().__init__()
        self.store: dict[str, Any] = {}
        self.row_refs: list[set[str]] = []

    async def _persist(self, checkpoint: Checkpoint, memo: InternMemo) -> None:
        cols, vals = checkpoint_columns(checkpoint, LIMIT, memo)
        cols = _json(cols)
        self.store.update(_json(vals))
        self.row_refs.append(referenced_hashes(cols))
        loaded = checkpoint.model_copy(update={
            "channel_values": resolve_values(cols["channel_values"], self.store),
            "pending_bindings": {k: PendingBinding.model_validate(v)
                                 for k, v in resolve_values(cols["pending_bindings"], self.store).items()},
            "next_invocations": [NextInvocation.model_validate(n)
                                 for n in resolve_values(cols["next_invocations"], self.store)],
        })
        self._checkpoints[loaded.checkpoint_id] = loaded
        self._run_checkpoints.setdefault(loaded.run_id, []).append(loaded.checkpoint_id)

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        await self._persist(checkpoint, InternMemo())

    async def save_checkpoint_with_outcomes(self, checkpoint: Checkpoint, outcomes: list[NodeOutcome]) -> None:
        for outcome in outcomes:
            await self.record_outcome(outcome)
        await self._persist(checkpoint, InternMemo())

    async def save_checkpoint_chain(self, items: list[tuple[Checkpoint, list[NodeOutcome]]]) -> None:
        memo = InternMemo()
        for checkpoint, outcomes in items:
            for outcome in outcomes:
                await self.record_outcome(outcome)
            await self._persist(checkpoint, memo)


def _pause_shape() -> Definition:
    def node(node_id: str, type_: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"id": node_id, "type": type_, "position": {"x": 0, "y": 0}, "data": {"config": config or {}}}

    def edge(src: str, tgt: str, mappings: dict[str, str]) -> dict[str, Any]:
        return {"id": f"e_{src}_{tgt}", "source": src, "target": tgt, "data": {"kind": "data", "mappings": mappings}}

    return Definition.model_validate({
        "nodes": [
            node("gather", "test.ledger"),
            node("hop1", "test.echo"),
            node("hop2", "test.echo"),
            node("ask", "control.human_input", {"title": "Check the accounts", "preset": "free_text",
                                                "prompt": "{question}"}),
            node("final", "test.echo"),
        ],
        "edges": [
            edge("gather", "hop1", {"ledger": "ledger", "question": "question"}),
            edge("hop1", "hop2", {"ledger": "ledger", "question": "question"}),
            edge("hop2", "ask", {"question": "question"}),
            # ``final`` waits through the pause holding the gathered ledger in its binding.
            edge("gather", "final", {"ledger": "ledger"}),
            edge("ask", "final", {"answer": "answer"}),
        ],
        "entry_nodes": ["gather"],
    })


async def test_a_large_value_survives_checkpoint_pause_and_resume_by_reference() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Ledger())
    registry.register(_Echo())
    checkpointer = _ByReference()
    scheduler = Scheduler(compile_graph(_pause_shape(), registry=registry), checkpointer,
                          make_app_context(FakeEmitter()), registry=registry)

    paused = await scheduler.run(run_id="lspeed-pause")
    assert paused.status is RunStatus.INTERRUPTED, paused.error
    assert any(checkpointer.row_refs), "the ledger never went by reference — the test proves nothing"
    parked = await checkpointer.latest_checkpoint("lspeed-pause")
    assert parked is not None and parked.interrupt_payload
    assert parked.pending_bindings["final"].edges["e_gather_final"].payload["ledger"] == LEDGER, (
        "the waiting binding did not come back whole from its reference"
    )

    resumed = await scheduler.resume(run_id="lspeed-pause", checkpoint_id=parked.checkpoint_id,
                                     resume_value={"answer": "The first ten."})
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs["final"]["ledger"] == LEDGER
    assert resumed.last_outputs["final"]["answer"] == "The first ten."
