"""An outcome row the database refused for a lock collision is written again, never raised at once.

Live 2026-11-01, run 188426a6 step 45 item 38: the success outcome's upsert ran inside the declared
host context's own ``transaction()``, so when Postgres canceled it (55P03 lock timeout) matrx-orm did
not re-run it — and the first refusal escaped into the step and parked the run. The upsert is keyed
by the outcome's correlation key, so writing it again is safe. Red before the fix: the first
``LockContentionError`` propagates and no row lands.
"""

from __future__ import annotations

import types
from typing import Any

import pytest
from matrx_orm import LockContentionError
from matrx_orm.core import write_retry

from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint.protocol import NodeOutcome

pytestmark = pytest.mark.asyncio

ORG = "11111111-1111-1111-1111-111111111111"
RUN = "33333333-3333-3333-3333-333333333333"


class _BusyThenFree:
    """``workflow.node_outcome``: the first ``refusals`` writes are canceled by a lock collision."""

    def __init__(self, refusals: int) -> None:
        self.refusals = refusals
        self.rows: list[dict[str, Any]] = []
        self.attempts = 0

    async def upsert(self, row: dict[str, Any], **_kw: Any) -> None:
        self.attempts += 1
        if self.attempts <= self.refusals:
            raise LockContentionError(query="INSERT INTO workflow.node_outcome", in_transaction=True)
        self.rows.append(row)

    async def get_or_none(self, **_kw: Any) -> Any:
        return types.SimpleNamespace(organization_id=ORG)

    def get_database_name(self) -> str:
        return "outcomes_test"

    _fields: dict[str, Any] = {}


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch):
    def _make(refusals: int) -> _BusyThenFree:
        store = _BusyThenFree(refusals)
        monkeypatch.setattr(module, "get_model", lambda _key: store)
        monkeypatch.setattr(module, "_input_envelope_capability", None)
        monkeypatch.setattr(module, "_value_store_available", lambda: False)
        module._RUN_ORGANIZATION.pop(RUN, None)

        async def _cache() -> int:
            return 64

        async def _policy(_db: str) -> write_retry.WriteRetryPolicy:
            return write_retry.WriteRetryPolicy(max_retries=3, backoff_base_ms=1, backoff_max_ms=2)

        monkeypatch.setattr(knobs, "run_org_cache_size", _cache)
        monkeypatch.setattr(write_retry, "resolve_policy", _policy)
        return store

    return _make


def _outcome() -> NodeOutcome:
    return NodeOutcome(run_id=RUN, step=45, node_id="ingest", attempt=1, dispatch_id="d", item_index=38,
                       output={"chunks_written": 1})


async def test_a_refused_outcome_write_is_written_again(table) -> None:
    store = table(refusals=2)

    await module.PostgresCheckpointer().record_outcome(_outcome())

    assert len(store.rows) == 1, "the outcome row never landed after a transient lock collision"
    assert store.attempts == 3


async def test_a_collision_that_never_clears_still_says_so(table) -> None:
    store = table(refusals=99)

    with pytest.raises(LockContentionError):
        await module.PostgresCheckpointer().record_outcome(_outcome())
    # One first try plus the knob's budget (1 + max_retries) — bounded, never a spin.
    assert store.attempts == 1 + 1 + 3
