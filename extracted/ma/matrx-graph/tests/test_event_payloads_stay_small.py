"""A run's EVENTS stay small, however large the values it carries (MKT-167).

The failure (2026-10-15): one Smart Add run wrote 49.7 MB of events (106 rows).
Every ``node_started`` carried the full 1.4 MB provision block in its ``inputs``,
every ``node_completed`` its whole output, and ``run_completed`` repeated every
output again in ``last_outputs`` (13.4 MB). The browser loaded and replayed all of
it on reopen: the tab reached 513 MB.

This runs a provision-shaped round through the real Scheduler — one large block
fanned into nine steps — and measures every event exactly as it is stored and
streamed (``event_payload_row`` at the starting knob, the function both the event
store and the live emitter call). The run's total must be a small multiple of its
distinct data, no event may carry a large value inline, the small fields screens
fold (``__kind``, ``iteration``, decisions) stay inline, and every event resolves
back to exactly what the engine emitted.
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
from matrx_graph.checkpoint.values import REF_KEY, event_payload_row, resolve_values
from matrx_graph.knobs import STARTING_EVENT_INLINE_VALUE_MAX_BYTES
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

TARGETS = 9
BLOCK_ENTRIES = 1400  # ~1 KB each → the measured ~1.4 MB provision block


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""
    decision: str = "keep"
    provisions: list[dict[str, Any]] = []


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entries: int = 0


class _Block:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.provision_block",
        category=NodeCategory.DATA,
        display_name="Provision block",
        description="Emits a provision block of the configured length.",
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
        provisions = [
            {"field": f"brand.fact_{i}", "value": "y" * 1000, "source": "site", "n": i}
            for i in range(config.entries)
        ]
        return success(_Out(value=ctx.node_id, provisions=provisions))


def _node(node_id: str, entries: int = 0) -> dict[str, Any]:
    return {"id": node_id, "type": "test.provision_block", "position": {"x": 0, "y": 0},
            "data": {"config": {"entries": entries}}}


def _edge(src: str, tgt: str, mappings: dict[str, str]) -> dict[str, Any]:
    return {"id": f"e_{src}_{tgt}", "source": src, "target": tgt,
            "data": {"kind": "data", "mappings": mappings}}


def _round_shape() -> Definition:
    """``values`` (the big block) feeds nine steps' inputs."""
    nodes = [_node("start"), _node("values", BLOCK_ENTRIES)]
    edges = [_edge("start", "values", {"seed": "value"})]
    for i in range(TARGETS):
        step = f"step{i}"
        nodes.append(_node(step))
        edges.append(_edge("values", step, {"provision_values": "provisions", "seed": "value"}))
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["start"]})


async def _events() -> list[dict[str, Any]]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Block())
    graph = compile_graph(_round_shape(), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="mkt-167-round")
    assert result.status is RunStatus.COMPLETED, result.error
    events = [p for name, p in emitter.events if name == "data" and isinstance(p, dict) and p.get("event")]
    assert any(e["event"] == "run_completed" for e in events), "the run emitted no run_completed"
    return [json.loads(json.dumps(e, default=str)) for e in events]


def _size(value: Any) -> int:
    return len(json.dumps(value, default=str).encode())


def _block_bytes() -> int:
    return _size([{"field": f"brand.fact_{i}", "value": "y" * 1000, "source": "site", "n": i}
                  for i in range(BLOCK_ENTRIES)])


async def test_a_runs_events_stay_small_however_large_its_values() -> None:
    limit = STARTING_EVENT_INLINE_VALUE_MAX_BYTES
    events = await _events()
    stored = [event_payload_row(e, limit)[0] for e in events]
    sizes = [_size(e) for e in stored]
    total = sum(sizes)
    # Inline, this round is ~25 copies of the block (every step's inputs, outputs,
    # last_outputs). By reference, the whole event log is under ONE copy.
    assert total < _block_bytes(), f"events total {total:,} bytes for a {_block_bytes():,}-byte block"
    # No event field carries more than the knob inline (plus its readable keys).
    assert max(sizes) <= 4 * limit, f"largest event {max(sizes):,} bytes — sizes {sorted(sizes)[-5:]}"


async def test_the_same_round_inline_is_many_copies_of_the_block() -> None:
    """Proves the guard can fail: unreferenced, the log repeats the block per event."""
    events = await _events()
    total = sum(_size(event_payload_row(e, 0)[0]) for e in events)
    assert total > 10 * _block_bytes(), total


async def test_screens_still_read_the_small_fields_inline() -> None:
    events = await _events()
    for event in events:
        out, _ = event_payload_row(event, STARTING_EVENT_INLINE_VALUE_MAX_BYTES)
        if event["event"] == "node_completed" and event["node_id"] == "values":
            assert out["output"]["decision"] == "keep"
            assert out["output"]["value"] == "values"
            assert set(out["output"]["provisions"]) == {REF_KEY}
        if event["event"] == "node_started" and event["node_id"].startswith("step"):
            assert out["inputs"]["seed"] == "values"
            assert set(out["inputs"]["provision_values"]) == {REF_KEY}
        for key in ("event", "run_id", "node_id", "ts", "wrapper", "metadata"):
            if key in event:
                assert out[key] == event[key], key


async def test_every_event_resolves_back_to_what_the_engine_emitted() -> None:
    events = await _events()
    store: dict[str, Any] = {}
    for event in events:
        out, values = event_payload_row(event, STARTING_EVENT_INLINE_VALUE_MAX_BYTES)
        store.update(values)
        assert resolve_values(out, store) == event
        # Re-interning a stored event changes nothing (the store and the emitter both call it).
        again, more = event_payload_row(out, STARTING_EVENT_INLINE_VALUE_MAX_BYTES)
        assert again == out and not more


async def test_a_long_string_stored_by_reference_loads_back_as_that_string(monkeypatch) -> None:
    """The jsonb codec hands a stored STRING back as a str; loading must not json-decode it again.

    Seen on run 116c24f5 (2026-10-15): 7 of 115 stored values were long strings (page text) and
    the reader raised JSONDecodeError on them.
    """
    from matrx_graph.checkpoint import value_store

    page = "<html>" + "x" * 50_000 + "</html>"
    rows = [{"value_hash": "h1", "value": page}, {"value_hash": "h2", "value": "123"}]

    class _Query:
        def __init__(self, hashes: list[str]) -> None:
            self.hashes = hashes

        async def values(self, *_cols: str) -> list[dict[str, Any]]:
            return [r for r in rows if r["value_hash"] in self.hashes]

    class _Model:
        def filter(self, *, run_id: str, value_hash__in: list[str]) -> _Query:
            return _Query(value_hash__in)

    monkeypatch.setattr(value_store, "get_model", lambda _name: _Model())
    got = await value_store.load_run_values("run", ["h1", "h2"])
    assert got == {"h1": page, "h2": "123"}
