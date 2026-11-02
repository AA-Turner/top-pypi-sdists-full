"""A round's checkpoints stay under the knob, however wide its fan-in (MKT-111).

The failure (2026-10-15): a Smart Add identify round fans one step's output (a
311 KB social-lookup ledger) into nine capture points that also wait on slower
steps. Every waiting target buffered its own copy in ``pending_bindings``, every
scheduled invocation carried its merged copy, every super-step's checkpoint
repeated all of it: rows up to 11 MB, 37 MB per round, and three concurrent rounds
took a 4 GB server out of memory.

This runs the same SHAPE through the real Scheduler — one big output fanned into
nine targets that each also wait on a chain of different depth — and measures
every checkpoint exactly as the Postgres checkpointer stores it
(``checkpoint_columns``). Every row must stay under the
``workflow.checkpoint_write.warn_bytes`` knob, and the values stored by
reference must be the distinct data, not nine copies per step.
"""

from __future__ import annotations

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
from matrx_graph.checkpoint.protocol import Checkpoint
from matrx_graph.checkpoint.values import (
    checkpoint_columns,
    resolve_values,
    row_bytes,
)
from matrx_graph.knobs import STARTING_CHECKPOINT_POLICY
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

TARGETS = 9
LEDGER_ENTRIES = 300  # ~1 KB each → a ~330 KB ledger, the measured size


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""
    ledger: list[dict[str, Any]] = []


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ledger: int = 0


class _Blob:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.blob",
        category=NodeCategory.DATA,
        display_name="Blob",
        description="Emits a ledger of the configured length.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        ledger = [
            {"platform": "instagram", "handle": f"acct_{i}", "raw": "x" * 1000, "n": i}
            for i in range(config.ledger)
        ]
        return success(_Out(value=ctx.node_id, ledger=ledger))


def _node(node_id: str, ledger: int = 0) -> dict[str, Any]:
    return {"id": node_id, "type": "test.blob", "position": {"x": 0, "y": 0},
            "data": {"config": {"ledger": ledger}}}


def _edge(src: str, tgt: str, mappings: dict[str, str]) -> dict[str, Any]:
    return {"id": f"e_{src}_{tgt}", "source": src, "target": tgt,
            "data": {"kind": "data", "mappings": mappings}}


def _round_shape() -> Definition:
    """``socials`` (big) fans into nine points; point i also waits on chain hop i."""
    nodes = [_node("start"), _node("socials", LEDGER_ENTRIES)]
    edges = [_edge("start", "socials", {"seed": "value"})]
    prev = "start"
    for i in range(TARGETS):
        hop = f"hop{i}"
        nodes.append(_node(hop))
        edges.append(_edge(prev, hop, {"seed": "value"}))
        prev = hop
        point = f"point{i}"
        nodes.append(_node(point))
        edges.append(_edge("socials", point, {"requests": "ledger", "evidence": "value"}))
        edges.append(_edge(hop, point, {"gate": "value"}))
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["start"]})


class _Measuring(MemoryCheckpointer):
    def __init__(self, max_inline_bytes: int) -> None:
        super().__init__()
        self.max_inline_bytes = max_inline_bytes
        self.rows: list[int] = []
        self.store: dict[str, Any] = {}
        self.round_trips: list[tuple[Checkpoint, dict[str, Any]]] = []

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        columns, values = checkpoint_columns(checkpoint, self.max_inline_bytes)
        self.rows.append(row_bytes(columns))
        self.store.update(values)
        self.round_trips.append((checkpoint, columns))
        await super().save_checkpoint(checkpoint)


async def _run(max_inline_bytes: int) -> _Measuring:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Blob())
    graph = compile_graph(_round_shape(), registry=registry)
    checkpointer = _Measuring(max_inline_bytes)
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="mkt-111-round")
    assert result.status is RunStatus.COMPLETED, result.error
    return checkpointer


async def test_every_checkpoint_row_of_a_wide_round_stays_under_the_knob() -> None:
    limit = STARTING_CHECKPOINT_POLICY.warn_bytes
    cp = await _run(STARTING_CHECKPOINT_POLICY.inline_value_max_bytes)
    assert cp.rows, "the round saved no checkpoint"
    assert max(cp.rows) <= limit, (
        f"a checkpoint row is {max(cp.rows):,} bytes — over the warn_bytes knob ({limit:,}); "
        f"rows: {cp.rows}"
    )
    # The ledger is stored ONCE (plus its entries), not once per target per step.
    stored = sum(len(json.dumps(v)) for v in cp.store.values())
    ledger_bytes = len(json.dumps([{"platform": "instagram", "handle": f"acct_{i}", "raw": "x" * 1000, "n": i}
                                   for i in range(LEDGER_ENTRIES)]))
    assert stored < 3 * ledger_bytes, f"stored {stored:,} bytes by reference for a {ledger_bytes:,}-byte ledger"


async def test_the_same_round_without_references_breaks_the_knob() -> None:
    """Proves the guard can fail: inline, the measured shape is far over the knob."""
    cp = await _run(0)
    assert max(cp.rows) > STARTING_CHECKPOINT_POLICY.warn_bytes, cp.rows


async def test_a_stored_row_resolves_back_to_the_checkpoint_it_came_from() -> None:
    cp = await _run(STARTING_CHECKPOINT_POLICY.inline_value_max_bytes)
    for checkpoint, columns in cp.round_trips:
        original, _ = checkpoint_columns(checkpoint, 0)
        for col in ("channel_values", "pending_bindings", "next_invocations"):
            assert resolve_values(columns[col], cp.store) == json.loads(json.dumps(original[col], default=str))


def _wide_binding_columns(limit: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """MKT-130: a join target buffering 30 values of ~3 KB each (each under the knob, 90 KB together)."""
    from matrx_graph.checkpoint.values import checkpoint_row

    bindings = {
        "point": {
            "firing": 1,
            "loop_stack": [],
            "edges": {
                "e1": {
                    "state": "delivered",
                    "source_node_id": "s",
                    "source_step": 1,
                    "payload": {f"arg{i}": "y" * 3000 + str(i) for i in range(30)},
                }
            },
        }
    }
    return checkpoint_row(
        channel_values={}, pending_bindings=bindings, next_invocations=[], interrupt_payload=None,
        max_inline_bytes=limit,
    )


def test_a_binding_of_many_mid_size_values_goes_by_reference() -> None:
    limit = STARTING_CHECKPOINT_POLICY.inline_value_max_bytes
    inline_cols, _ = _wide_binding_columns(0)
    cols, store = _wide_binding_columns(limit)
    before = len(json.dumps(inline_cols["pending_bindings"]))
    after = len(json.dumps(cols["pending_bindings"]))
    assert before > 20 * limit, before
    assert after <= limit, f"pending_bindings is {after:,} bytes inline (was {before:,}); knob {limit:,}"
    # Loading resolves it back to exactly what was saved; an old row with inline values loads unchanged.
    assert resolve_values(cols["pending_bindings"], store) == inline_cols["pending_bindings"]
    assert resolve_values(inline_cols["pending_bindings"], {}) == inline_cols["pending_bindings"]


def _shared_edge_map_columns(limit: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """MKT-130: six join targets each buffering the same ~4 KB edge map (every value under the knob)."""
    from matrx_graph.checkpoint.values import checkpoint_row

    edges = {
        f"e{i}": {
            "state": "delivered",
            "source_node_id": "s",
            "source_step": 1,
            "payload": {"homepage_text": "h" * 700 + str(i), "note": f"n{i}"},
        }
        for i in range(5)
    }
    bindings = {
        f"{name}_point": {"firing": 1, "loop_stack": [], "edges": edges}
        for name in ("a", "b", "c", "d", "e", "f")
    }
    return checkpoint_row(
        channel_values={}, pending_bindings=bindings, next_invocations=[], interrupt_payload=None,
        max_inline_bytes=limit,
    )


def test_identical_edge_maps_on_many_nodes_are_stored_once_and_the_column_fits_the_knob() -> None:
    limit = STARTING_CHECKPOINT_POLICY.inline_value_max_bytes
    inline_cols, _ = _shared_edge_map_columns(0)
    cols, store = _shared_edge_map_columns(limit)
    before = len(json.dumps(inline_cols["pending_bindings"]))
    after = len(json.dumps(cols["pending_bindings"]))
    assert before > 5 * limit, before
    assert after <= limit, f"pending_bindings is {after:,} bytes (was {before:,}); knob {limit:,}"
    assert len(store) == 1, "six identical edge maps must be ONE stored value"
    assert all(b["firing"] == 1 for b in cols["pending_bindings"].values())
    assert resolve_values(cols["pending_bindings"], store) == inline_cols["pending_bindings"]
