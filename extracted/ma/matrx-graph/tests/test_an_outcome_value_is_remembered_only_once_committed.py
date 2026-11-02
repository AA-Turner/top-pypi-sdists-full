"""An outcome's large value is remembered as stored only after its transaction COMMITS.

``record_outcome`` writes an outcome's new large values and its row in ONE transaction.
The per-process "already stored" memory was updated INSIDE that transaction, before the
commit. Fan-out siblings run concurrently (``asyncio.gather``), so a sibling with the same
large value saw the hash as stored and wrote only a REFERENCE — to a value that a rollback
then never stored (and, even on commit, its row was visible before the value). Red before
the fix: the sibling's committed row references a hash the store does not hold.
"""

from __future__ import annotations

import asyncio
import contextlib
import types
from typing import Any

import pytest

from matrx_graph import knobs
from matrx_graph.checkpoint import postgres as module
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.checkpoint.values import REF_KEY

pytestmark = pytest.mark.asyncio

ORG = "11111111-1111-1111-1111-111111111111"
RUN = "22222222-2222-2222-2222-222222222222"
INLINE_MAX = 256
BIG = {"items": ["the same large shared value " + "x" * 64 for _ in range(20)]}


class _Db:
    """Committed rows and values; writes inside a transaction land only on its commit."""

    def __init__(self) -> None:
        self.values: dict[str, Any] = {}
        self.rows: list[dict[str, Any]] = []
        self._pending: dict[Any, tuple[dict[str, Any], list[dict[str, Any]]]] = {}
        self.a_in_transaction = asyncio.Event()
        self.b_done = asyncio.Event()

    def _sink(self) -> tuple[dict[str, Any], list[dict[str, Any]]] | None:
        return self._pending.get(asyncio.current_task())

    @contextlib.asynccontextmanager
    async def transaction(self, *_a: Any, **_k: Any):
        task = asyncio.current_task()
        self._pending[task] = ({}, [])
        try:
            yield None
        except BaseException:
            self._pending.pop(task)  # rollback
            raise
        values, rows = self._pending.pop(task)
        self.values.update(values)
        self.rows.extend(rows)

    async def bulk_insert_ignore(self, rows: list[dict[str, Any]], **_kw: Any) -> None:
        sink = self._sink()
        target = sink[0] if sink else self.values
        for r in rows:
            target.setdefault(r["value_hash"], r["value"])

    async def upsert(self, row: dict[str, Any], **_kw: Any) -> None:
        sink = self._sink()
        if sink is not None and row["node_id"] == "a":
            # Sibling A is mid-transaction: B runs now, then A's transaction fails.
            self.a_in_transaction.set()
            await self.b_done.wait()
            raise RuntimeError("connection reset")
        (sink[1] if sink else self.rows).append(row)

    async def get_or_none(self, **_kw: Any) -> Any:
        return types.SimpleNamespace(organization_id=ORG)

    _fields: dict[str, Any] = {}


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch) -> _Db:
    store = _Db()
    monkeypatch.setattr(module, "get_model", lambda _key: store)
    monkeypatch.setattr(value_store, "get_model", lambda _key: store)
    monkeypatch.setattr(module, "_outcome_transaction", store.transaction)
    monkeypatch.setattr(module, "_input_envelope_capability", None)
    monkeypatch.setattr(module, "_value_store_available", lambda: True)
    monkeypatch.setattr(module, "_stored_value_hashes", {})
    module._RUN_ORGANIZATION.pop(RUN, None)

    async def _inline() -> int:
        return INLINE_MAX

    async def _cache() -> int:
        return 64

    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", _inline)
    monkeypatch.setattr(knobs, "run_org_cache_size", _cache)
    return store


def _outcome(node_id: str, index: int) -> NodeOutcome:
    return NodeOutcome(run_id=RUN, step=1, node_id=node_id, attempt=1, item_index=index, output=dict(BIG))


def _refs(value: Any) -> set[str]:
    if isinstance(value, dict):
        if set(value) == {REF_KEY}:
            return {str(value[REF_KEY])}
        return set().union(*(_refs(v) for v in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(_refs(v) for v in value)) if value else set()
    return set()


async def test_a_sibling_never_references_a_value_its_twin_rolled_back(db: _Db) -> None:
    checkpointer = module.PostgresCheckpointer()

    async def sibling_a() -> None:
        await checkpointer.record_outcome(_outcome("a", 0))

    async def sibling_b() -> None:
        await db.a_in_transaction.wait()
        try:
            await checkpointer.record_outcome(_outcome("b", 1))
        finally:
            db.b_done.set()

    await asyncio.gather(sibling_a(), sibling_b())

    b_row = next(r for r in db.rows if r["node_id"] == "b")
    dangling = _refs(b_row["output"]) - set(db.values)
    assert not dangling, (
        f"sibling b's committed row references {len(dangling)} value(s) that were never "
        "committed — its twin's rolled-back transaction had marked them stored"
    )
    # A's rollback fell back to its whole row; nothing it wrote is remembered as stored.
    assert all(h in db.values for h in module._stored_value_hashes.get(RUN, set()))


async def test_a_committed_value_is_remembered_so_the_next_write_skips_it(db: _Db) -> None:
    db.b_done.set()  # no sibling races here
    checkpointer = module.PostgresCheckpointer()
    await checkpointer.record_outcome(_outcome("c", 0))
    stored = module._stored_value_hashes.get(RUN, set())
    assert stored and stored <= set(db.values)
