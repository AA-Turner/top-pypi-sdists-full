"""A node outcome row keeps a step's large OUTPUT by reference, never inline (MKT-171).

Run 118def1a stored 3.5 MB of step outputs in workflow.node_outcome.output. Outputs use the same
run value store as inputs (MKT-170), events and checkpoints; reading the outcome back resolves the
references. Rows written before this change (output inline) must keep loading unchanged.
"""
from __future__ import annotations

import contextlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.checkpoint.values import REF_KEY, referenced_hashes
from tests.test_checkpoint_postgres_org_write import _FakeWfNodeOutcome, _FakeWfRun

BIG = {f"row_{i}": "y" * 2000 for i in range(400)}  # ~800 KB


class _Outcomes(_FakeWfNodeOutcome):
    _fields = {"input": object(), "input_kind": object()}

    def __init__(self, rows: list[dict[str, Any]] | None = None) -> None:
        super().__init__()
        self.rows = rows or []

    def filter(self, **_kw: Any) -> _Outcomes:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        return self.rows


def _outcome(run_id: str, output: dict[str, Any]) -> NodeOutcome:
    return NodeOutcome(
        id=str(uuid4()), run_id=run_id, step=1, node_id="page", attempt=1, dispatch_id="d",
        item_index=0, output=output, channel_writes=[], sends=[], duration_ms=0, source="executor",
        completed_at=datetime.now(UTC),
    )


def _wire(monkeypatch: pytest.MonkeyPatch, run_id: str, outcomes: _Outcomes) -> dict[str, Any]:
    models = {"WfNodeOutcome": outcomes, "WfRun": _FakeWfRun({run_id: str(uuid4())})}
    monkeypatch.setattr(module, "get_model", lambda key: models[key])
    monkeypatch.setattr(module, "_input_envelope_capability", None)
    monkeypatch.setattr(module, "_value_store_available", lambda: True)
    # The outcome row and its new values share one transaction (a seam, 18ffc0d0): these
    # tests have no database, so the transaction is a no-op context.
    monkeypatch.setattr(module, "_outcome_transaction", contextlib.nullcontext, raising=False)
    stored: dict[str, Any] = {}

    async def _store(_run: str, values: dict[str, Any], **_k: Any) -> None:
        stored.update(values)

    async def _load(_run: str, hashes: Any, **_k: Any) -> dict[str, Any]:
        return {h: stored[h] for h in hashes if h in stored}

    async def _limit() -> int:
        return 65536

    monkeypatch.setattr(value_store, "store_run_values", _store)
    monkeypatch.setattr(value_store, "load_run_values", _load)
    import matrx_graph.knobs as knobs

    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", _limit)
    return stored


@pytest.mark.asyncio
async def test_a_large_step_output_is_stored_once_by_reference(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    outcomes = _Outcomes()
    stored = _wire(monkeypatch, run_id, outcomes)

    await module.PostgresCheckpointer().record_outcome(_outcome(run_id, {"pages": BIG, "ok": True}))

    row = outcomes.upsert_calls[0]["output"]
    assert len(json.dumps(row)) < 2000, "the row must hold a reference, not the 800 KB value"
    assert row["ok"] is True
    assert referenced_hashes(row) and stored, "the value went to the run's value store"
    assert REF_KEY in row["pages"] and stored[next(iter(referenced_hashes(row)))] == BIG


@pytest.mark.asyncio
async def test_reading_an_outcome_back_resolves_its_output(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    outcomes = _Outcomes()
    _wire(monkeypatch, run_id, outcomes)
    await module.PostgresCheckpointer().record_outcome(_outcome(run_id, {"pages": BIG}))
    written = outcomes.upsert_calls[0]
    outcomes.rows = [{**written, "run_id": run_id, "emissions": {}, "error": None,
                      "completed_at": datetime.now(UTC)}]

    got = await module.PostgresCheckpointer().get_outcome(run_id, 1, "page", 1, "d", 0)

    assert got is not None and got.output == {"pages": BIG}


@pytest.mark.asyncio
async def test_an_old_inline_output_row_still_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    outcomes = _Outcomes()
    _wire(monkeypatch, run_id, outcomes)
    outcomes.rows = [{
        "run_id": run_id, "step": 1, "node_id": "page", "attempt": 1, "dispatch_id": "d", "item_index": 0,
        "output": {"pages": BIG}, "channel_writes": [], "sends": [], "emissions": {}, "duration_ms": 0,
        "error": None, "source": "executor", "completed_at": datetime.now(UTC),
    }]

    got = await module.PostgresCheckpointer().get_outcome(run_id, 1, "page", 1, "d", 0)

    assert got is not None and got.output == {"pages": BIG}


@pytest.mark.asyncio
async def test_inputs_and_output_both_resolve_on_read(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    outcomes = _Outcomes()
    _wire(monkeypatch, run_id, outcomes)
    out = _outcome(run_id, {"pages": BIG}).model_copy(update={"inputs": {"provision": BIG}})
    await module.PostgresCheckpointer().record_outcome(out)
    written = outcomes.upsert_calls[0]
    outcomes.rows = [{**written, "run_id": run_id, "emissions": {}, "error": None,
                      "completed_at": datetime.now(UTC)}]

    got = await module.PostgresCheckpointer().get_outcome(run_id, 1, "page", 1, "d", 0)

    assert got is not None and got.output == {"pages": BIG} and got.inputs == {"provision": BIG}
