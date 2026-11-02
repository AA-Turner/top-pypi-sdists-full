"""A large step result reaches the next step's "Only when" whole — in a run AND in the design-time check.

2026-10-28, "Build the offerings list" (7d2b7ff7): a 312-page list from an earlier step "never reached
the next step's 'only when'". Step outputs over the ``workflow.event_payload.inline_value_max_bytes`` knob
are kept in ``workflow.node_outcome`` by reference (``{"__matrx_checkpoint_value__": <sha256>}``, MKT-171).
The run itself hands the condition the whole value (first test). But ``adopt_live_outputs`` copied
``node_outcome.output`` VERBATIM into the definition's ``last_live_output`` sample slot — so the slot held
the reference marker, a one-key dict whose hash only means something inside the run that stored it. The
design-time check (``dry_run``), the step inspector, mapping pickers and the node agent all read that
slot: ``len(inputs['pages']) > 24`` saw ``len({marker}) == 1`` and the step looked like it never runs.
Live on 2026-10-28: 1,567 of 10,732 ``last_live_output`` slots (247 workflows) held markers.

The guard: a slot adopted from a run holds the step's WHOLE result (references resolved through the one
run value-store read path), and the design-time "Only when" over it evaluates the real list.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.values import REF_KEY, outcome_input_row, referenced_hashes
from matrx_graph.db import node_data_slot_store as slot_module
from matrx_graph.db.node_data_slot_store import NodeDataSlotStore
from matrx_graph.dry_run import DryRunSample, dry_run
from tests._fixtures import FakeEmitter, make_app_context

PAGES = [
    {
        "url": f"https://example.com/products/item-{i}",
        "title": f"Item {i} soy candle, hand poured in small batches",
    }
    for i in range(312)
]
CONDITION = "len(inputs['pages']) > 24"


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _definition() -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "rows",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "{'pages': inputs['pages']}"}},
            },
            {
                "id": "count",
                "type": "data.transform",
                "position": {"x": 300, "y": 0},
                "data": {
                    "config": {"expression": "{'showing': len(inputs['pages'])}"},
                    "when": CONDITION,
                },
            },
        ],
        "edges": [
            {
                "id": "e",
                "source": "rows",
                "target": "count",
                "data": {"kind": "data", "mappings": {"pages": "pages"}},
            },
        ],
    }


def test_the_list_is_over_every_by_reference_threshold() -> None:
    size = len(json.dumps({"pages": PAGES}))
    assert size > 32 * 1024, size  # over the event knob (32 KB) and the checkpoint knob (4 KB)


@pytest.mark.asyncio
async def test_a_run_hands_only_when_the_whole_list() -> None:
    registry = _registry()
    graph = compile_graph(Definition.model_validate(_definition()), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id=str(uuid4()), inputs={"pages": PAGES})

    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["count"] == {"showing": 312}


class _Query:
    def __init__(self, rows: list[dict[str, Any]], filters: dict[str, Any]) -> None:
        def _match(r: dict[str, Any], key: str, want: Any) -> bool:
            if key.endswith("__isnull"):
                return (r[key.removesuffix("__isnull")] is None) is want
            if key.endswith("__in"):
                return r[key.removesuffix("__in")] in want
            return r[key] == want

        self._rows = [r for r in rows if all(_match(r, k, v) for k, v in filters.items())]

    def order_by(self, *fields: str) -> _Query:
        for field in reversed(fields):
            key = field.lstrip("-")
            self._rows.sort(key=lambda r, k=key: r[k], reverse=field.startswith("-"))
        return self

    def filter(self, **filters: Any) -> _Query:
        return _Query(self._rows, filters)

    async def values(self, *cols: str) -> list[dict[str, Any]]:
        return [{c: r[c] for c in cols} if cols else dict(r) for r in self._rows]


class _Outcomes:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def filter(self, **filters: Any) -> _Query:
        return _Query(self.rows, filters)


def _wire(
    monkeypatch: pytest.MonkeyPatch,
    run_id: str,
    outcomes: list[dict[str, Any]],
    stored: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    """Fakes for the outcome table, the slot table and the run value store; returns the slot table."""
    slots: dict[tuple[str, str], dict[str, Any]] = {}
    model = _Outcomes(outcomes)
    # The value store's size column, as store_run_values writes it (the value's own JSON size).
    sizes = _Outcomes(
        [{"value_hash": h, "size_bytes": len(json.dumps(v)), "run_id": run_id} for h, v in stored.items()]
    )
    import matrx_graph.db._registry as registry

    monkeypatch.setattr(
        registry,
        "get_model",
        lambda key: {"WfNodeOutcome": model, "WfCheckpointValue": sizes}.get(key, object()),
    )
    loads: list[set[str]] = []
    slots_loads = loads

    async def _load(rid: str, hashes: Any) -> dict[str, Any]:
        assert rid == run_id, "a reference resolves only inside the run that stored it"
        slots_loads.append(set(hashes))
        return {h: stored[h] for h in hashes if h in stored}

    monkeypatch.setattr(value_store, "load_run_values", _load)

    async def _upsert(_model: Any, data: dict[str, Any], **_kw: Any) -> dict[str, Any]:
        row = {
            **data,
            "id": uuid4(),
            "value": json.loads(data["value"].text),
            "emissions": json.loads(data["emissions"].text),
        }
        slots[(data["node_id"], data["slot"])] = row
        return row

    import matrx_orm.operations.conflict_writes as conflict_writes

    monkeypatch.setattr(conflict_writes, "upsert_with_conflict", _upsert)

    async def _latest_per_group(
        plan: Any,
    ) -> int:  # what the one-statement adoption did: copy the column
        best: dict[str, dict[str, Any]] = {}
        for r in sorted(outcomes, key=lambda r: (r["step"], r["attempt"])):
            if r["run_id"] == run_id and r["error"] is None and r["source"] == "executor":
                best[r["node_id"]] = r
        for node_id, r in best.items():
            slots[(node_id, "last_live_output")] = {
                "value": r["output"],
                "emissions": r["emissions"],
            }
        return len(best)

    import matrx_orm.operations.latest_rows as latest_rows

    monkeypatch.setattr(latest_rows, "upsert_latest_per_group", _latest_per_group)
    slots_loads_by_run[run_id] = loads
    return slots


#: run id → every load_run_values call adoption made (the hashes it asked for).
slots_loads_by_run: dict[str, list[set[str]]] = {}


@pytest.mark.asyncio
async def test_a_slot_adopted_from_a_run_holds_the_whole_result_and_only_when_sees_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_id = str(uuid4())
    # The outcome row exactly as PostgresCheckpointer.record_outcome writes it (32 KB knob).
    row_output, stored = outcome_input_row(
        {"pages": PAGES, "brand_name": "Example Candles"}, 32 * 1024
    )
    assert referenced_hashes(row_output), "the outcome row must hold the list by reference"
    outcomes = [
        {
            "run_id": run_id,
            "node_id": "rows",
            "step": 0,
            "attempt": 1,
            "error": None,
            "source": "executor",
            "output": row_output,
            "emissions": {},
            "output_kind": None,
        },
    ]
    slots = _wire(monkeypatch, run_id, outcomes, stored)

    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )

    assert adopted == 1
    value = slots[("rows", "last_live_output")]["value"]
    assert REF_KEY not in json.dumps(value), (
        "a definition's sample must never hold a run's reference marker"
    )
    assert value["pages"] == PAGES

    # The design-time check over that sample — the conditional connection "Only when" expands into: the
    # step after it RUNS (satisfied). Over the marker it was pruned: len({marker}) == 1.
    assert _design_time_state(value) == "satisfied"
    assert _design_time_state(row_output) == "pruned", (
        "the marker is exactly what made the step look dead"
    )


def _design_time_state(sample: Any) -> str:
    defn = _definition()
    defn["nodes"][1]["data"].pop("when")
    defn["edges"][0]["data"].update({"kind": "conditional", "condition": CONDITION})
    graph = compile_graph(Definition.model_validate(defn), registry=_registry())
    report = dry_run(graph, samples={"rows": DryRunSample(value=sample, slot="last_live_output")})
    return report.edges["e"].state


@pytest.mark.asyncio
async def test_a_result_whose_stored_value_is_gone_is_not_adopted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Never a marker as the sample: a value the run no longer has leaves the slot as it was."""
    run_id = str(uuid4())
    row_output, _stored = outcome_input_row({"pages": PAGES}, 32 * 1024)
    outcomes = [
        {
            "run_id": run_id,
            "node_id": "rows",
            "step": 0,
            "attempt": 1,
            "error": None,
            "source": "executor",
            "output": row_output,
            "emissions": {},
            "output_kind": None,
        },
        {
            "run_id": run_id,
            "node_id": "small",
            "step": 0,
            "attempt": 1,
            "error": None,
            "source": "executor",
            "output": {"ok": True},
            "emissions": {},
            "output_kind": None,
        },
    ]
    slots = _wire(monkeypatch, run_id, outcomes, stored={})

    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )

    assert adopted == 1
    assert ("rows", "last_live_output") not in slots
    assert slots[("small", "last_live_output")]["value"] == {"ok": True}


@pytest.mark.asyncio
async def test_a_result_over_the_slot_cap_once_whole_is_not_adopted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The slot cap applies to the WHOLE value, as it did before outputs went by reference."""
    run_id = str(uuid4())
    huge = {"pages": [{"html": "x" * 4000} for _ in range(100)]}  # ~400 KB > 256 KB slot cap
    row_output, stored = outcome_input_row(huge, 32 * 1024)
    assert len(json.dumps(row_output)) < slot_module.MAX_SLOT_VALUE_BYTES
    outcomes = [
        {
            "run_id": run_id,
            "node_id": "rows",
            "step": 0,
            "attempt": 1,
            "error": None,
            "source": "executor",
            "output": row_output,
            "emissions": {},
            "output_kind": None,
        },
    ]
    slots = _wire(monkeypatch, run_id, outcomes, stored)

    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )

    assert adopted == 0
    assert slots == {}


class _Slots:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def filter(self, **_filters: Any) -> _Query:
        return _Query(self.rows, {})


@pytest.mark.asyncio
async def test_a_slot_adopted_before_the_fix_is_not_offered_as_a_sample(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Live slots written before this fix hold a marker and no run id to resolve it: they are absent."""
    from datetime import UTC, datetime

    import matrx_graph.db._registry as registry

    def _row(node_id: str, value: Any) -> dict[str, Any]:
        return {
            "id": uuid4(),
            "definition_id": uuid4(),
            "node_id": node_id,
            "slot": "last_live_output",
            "value": value,
            "emissions": {},
            "output_kind": None,
            "source": "live_run",
            "captured_at": datetime.now(UTC),
            "captured_by": None,
            "created_by": uuid4(),
        }

    marker_row, _ = outcome_input_row({"pages": PAGES}, 32 * 1024)
    model = _Slots([_row("rows", marker_row), _row("small", {"ok": True})])
    monkeypatch.setattr(registry, "get_model", lambda _key: model)

    slots = await NodeDataSlotStore().get_slots(str(uuid4()))

    assert [s.node_id for s in slots] == ["small"]


@pytest.mark.asyncio
async def test_a_step_result_over_the_slot_cap_is_never_read_back_to_be_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Run 322b35c1 (2026-10-28): adoption read every step's 0.4-2 MB result back, one step at a time,
    on the run's completion path, only for the 256 KB slot cap to refuse it. The stored sizes decide
    first: an over-cap result is left out unread, and the rest resolve in ONE read."""
    from matrx_graph.db.node_data_slot_store import MAX_SLOT_VALUE_BYTES

    run_id = str(uuid4())
    big_pages = [{**PAGES[0], "text": "x" * 4096, "n": i} for i in range(2 * MAX_SLOT_VALUE_BYTES // 4096)]
    big_output, stored = outcome_input_row({"pages": big_pages, "brand_name": "Example Candles"}, 32 * 1024)
    small_output, small_stored = outcome_input_row({"pages": PAGES, "brand_name": "Example Candles"}, 32 * 1024)
    stored.update(small_stored)
    big_refs, small_refs = referenced_hashes(big_output), referenced_hashes(small_output)
    assert big_refs and small_refs
    outcomes = [
        {"run_id": run_id, "node_id": node_id, "step": step, "attempt": 1, "error": None,
         "source": "executor", "output": output, "emissions": {}, "output_kind": None}
        for step, (node_id, output) in enumerate([("big", big_output), ("rows", small_output), ("rows2", small_output)])
    ]
    slots = _wire(monkeypatch, run_id, outcomes, stored)

    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )

    assert adopted == 2
    assert ("big", "last_live_output") not in slots
    assert slots[("rows", "last_live_output")]["value"]["pages"] == PAGES
    assert slots[("rows2", "last_live_output")]["value"]["pages"] == PAGES
    loads = slots_loads_by_run[run_id]
    assert len(loads) == 1, f"one read for the whole run, not one per step: {loads}"
    assert not (loads[0] & big_refs), "the over-cap result was read back only to be refused"
