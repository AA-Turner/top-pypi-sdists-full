"""A run-once result referencing more stored values than one read returns still resolves whole.

``load_run_values`` reads at most MAX_HASHES_PER_READ hashes per call; the run-once store's
``resolve_output`` used to hand it every hash, so a reused output with >200 stored values lost
the rest and the step was re-run (and re-paid). It now batches; a genuinely missing value stays
a loud ``LookupError``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.values import REF_KEY
from matrx_graph.once import PostgresStepResultStore, StoredResult

N = value_store.MAX_HASHES_PER_READ * 2 + 37


def _result(output: dict[str, Any]) -> StoredResult:
    return StoredResult(
        input_digest="d", output=output, output_kind=None, verdict={}, emissions={},
        origin_run_id="origin", origin_node_id="n", origin_step=0, origin_dispatch_id="x",
        origin_item_index=0, origin_attempt=1, succeeded_at=datetime.now(UTC), expires_at=None,
    )


def _patch(monkeypatch: pytest.MonkeyPatch, stored: dict[str, Any]) -> None:
    async def _fetch(run_id: str, hashes: Any) -> dict[str, Any]:
        assert run_id == "origin"
        return {h: stored[h] for h in hashes if h in stored}

    monkeypatch.setattr(value_store, "fetch_stored_values", _fetch)


async def test_more_stored_values_than_one_read_all_resolve(monkeypatch):
    stored = {f"h{i:04d}": f"value-{i}" for i in range(N)}
    _patch(monkeypatch, stored)
    output = {f"k{i}": {REF_KEY: f"h{i:04d}"} for i in range(N)}
    got = await PostgresStepResultStore().resolve_output(_result(output))
    assert got == {f"k{i}": f"value-{i}" for i in range(N)}


async def test_a_genuinely_missing_value_is_loud(monkeypatch):
    stored = {f"h{i:04d}": f"value-{i}" for i in range(N) if i != N - 1}
    _patch(monkeypatch, stored)
    output = {f"k{i}": {REF_KEY: f"h{i:04d}"} for i in range(N)}
    with pytest.raises(LookupError):
        await PostgresStepResultStore().resolve_output(_result(output))
