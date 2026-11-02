"""A node outcome row keeps a step's large inputs BY REFERENCE, never inline (MKT-170).

Run b0310478 stored 12.5 MB of raw step inputs in workflow.node_outcome (one input 1.8 MB).
Outcomes use the SAME run value store as events and checkpoints; reading the outcome back
resolves the references, so a replay or a reviewer still sees the full input.
"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.checkpoint.values import REF_KEY, referenced_hashes
from tests.test_checkpoint_postgres_org_write import _FakeWfNodeOutcome, _FakeWfRun

BIG = {f"row_{i}": "x" * 2000 for i in range(400)}  # ~800 KB


class _Outcomes(_FakeWfNodeOutcome):
    _fields = {"input": object(), "input_kind": object()}


def _outcome(run_id: str) -> NodeOutcome:
    return NodeOutcome(
        id=str(uuid4()), run_id=run_id, step=1, node_id="first_point", attempt=1, dispatch_id="d",
        item_index=0, output={}, channel_writes=[], sends=[], duration_ms=0, source="executor",
        completed_at=datetime.now(UTC), inputs={"provision": BIG, "small": "ok"},
    )


@pytest.mark.asyncio
async def test_a_large_step_input_is_stored_once_by_reference(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id, org = str(uuid4()), str(uuid4())
    outcomes = _Outcomes()
    models = {"WfNodeOutcome": outcomes, "WfRun": _FakeWfRun({run_id: org})}
    monkeypatch.setattr(module, "get_model", lambda key: models[key])
    monkeypatch.setattr(module, "_input_envelope_capability", None)
    monkeypatch.setattr(module, "_value_store_available", lambda: True)

    @asynccontextmanager
    async def _no_db_transaction():
        yield

    # The seam for tests: a real matrx_orm transaction needs a registered database,
    # which CI (and any bare install) does not have.
    monkeypatch.setattr(module, "_outcome_transaction", _no_db_transaction)
    stored: dict[str, Any] = {}

    async def _store(_run: str, values: dict[str, Any], **_k: Any) -> None:
        stored.update(values)

    async def _limit() -> int:
        return 65536

    monkeypatch.setattr(value_store, "store_run_values", _store)
    monkeypatch.setattr(value_store, "event_inline_value_max_bytes", _limit, raising=False)
    import matrx_graph.knobs as knobs

    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", _limit)

    await module.PostgresCheckpointer().record_outcome(_outcome(run_id))

    row = outcomes.upsert_calls[0]["input"]
    assert len(json.dumps(row)) < 2000, "the row must hold a reference, not the 800 KB value"
    assert row["small"] == "ok"
    assert referenced_hashes(row) and stored, "the value went to the run's value store"
    digest = next(iter(referenced_hashes(row)))
    assert REF_KEY in row["provision"] and stored[digest] == BIG
