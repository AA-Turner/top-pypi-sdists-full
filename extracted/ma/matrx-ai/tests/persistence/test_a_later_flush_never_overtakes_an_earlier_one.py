"""A later flush of one Coordinator never overtakes an earlier one (PB-08, defect 58).

Live/local evidence (conversation dabb3b5b…, 2026-10-18): the lead started two
background helpers. Tidewell's ``agent`` row was INSERTed in a flush whose
transaction began 03:33:35.79 (the helper's ``pre_fan_out`` finalize) and took
~4.7 s. Its completion UPDATE was queued into the rolled Session, and the turn's
``commit_async`` fired that Session at 03:33:39.54 — while the INSERT was still
uncommitted. Under READ COMMITTED the UPDATE matched 0 rows, so the row stayed
``running`` with no output, and nothing recorded a failure.

The contract these guards hold: every flush one Coordinator starts (background
commit, finalize's current cache, seal's residual, late one-shot) lands in the
order its Session was rolled. A later UPDATE always sees the earlier INSERT.

The fake database below applies an INSERT only when its (slow) transaction
commits, and an UPDATE only to rows already committed — Postgres's behaviour for
two concurrent transactions.
"""

from __future__ import annotations

import asyncio
import contextlib

import pytest

import matrx_ai.persistence.coordinator as coord_mod
from matrx_ai.persistence.coordinator import Coordinator
from matrx_ai.persistence.registry import register_table

_OUTER = 5.0
_SLOW_INSERT_SECONDS = 0.3


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_flush_order"
    db_schema = "public"


class _Model:
    _meta = _Meta()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table("public.cx_flush_order", _Model)


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture
def db(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    coord_mod._inflight_commits = 0
    committed: dict[str, dict] = {}
    lost: list[str] = []

    async def execute_tiers(tiers):
        staged: dict[str, dict] = {}
        written = 0
        for tier in tiers:
            for op in tier:
                if op.op_type == "insert":
                    staged[op.pk_value] = dict(op.payload)
                elif op.op_type == "update":
                    row = committed.get(op.pk_value) or staged.get(op.pk_value)
                    if row is None:
                        # READ COMMITTED: the other transaction's INSERT is
                        # invisible, so the UPDATE matches nothing.
                        lost.append(op.pk_value)
                    else:
                        row.update(op.payload)
                written += 1
        if staged:
            await asyncio.sleep(_SLOW_INSERT_SECONDS)
        committed.update(staged)
        return written

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", execute_tiers)
    yield committed, lost
    coord_mod._inflight_commits = 0


@pytest.mark.asyncio
async def test_a_turn_commit_waits_for_an_in_flight_finalize(db):
    """The Tidewell shape: pre_fan_out finalize in flight, then commit_async."""
    committed, lost = db
    coord = Coordinator(request_id="r-order", conversation_id="c-order")
    coord.queue("public.cx_flush_order", {"id": "tidewell", "status": "running"})

    fan_out = asyncio.create_task(coord.finalize(reason="pre_fan_out"))
    await asyncio.sleep(0.05)  # the INSERT's transaction is open, not committed
    coord.queue(
        "public.cx_flush_order",
        {"id": "tidewell", "status": "completed"},
        op_type="update",
    )
    coord.commit_async(reason="turn_1_commit")

    await asyncio.wait_for(fan_out, _OUTER)
    await asyncio.wait_for(coord.finalize(reason="request_final_commit"), _OUTER)

    assert lost == [], f"an UPDATE overtook its row's INSERT: {lost}"
    assert committed["tidewell"]["status"] == "completed"


@pytest.mark.asyncio
async def test_two_background_commits_land_in_order(db):
    committed, lost = db
    coord = Coordinator(request_id="r-order2", conversation_id="c-order2")
    coord.queue("public.cx_flush_order", {"id": "row", "status": "running"})
    coord.commit_async(reason="turn_1_commit")
    coord.queue(
        "public.cx_flush_order", {"id": "row", "status": "completed"}, op_type="update"
    )
    coord.commit_async(reason="turn_2_commit")

    await asyncio.wait_for(coord.finalize(reason="request_final_commit"), _OUTER)

    assert lost == [], f"an UPDATE overtook its row's INSERT: {lost}"
    assert committed["row"]["status"] == "completed"


@pytest.mark.asyncio
async def test_a_late_one_shot_waits_for_the_seal_residual(db):
    committed, lost = db
    coord = Coordinator(request_id="r-order3", conversation_id="c-order3")
    coord.queue("public.cx_flush_order", {"id": "late", "status": "running"})

    sealing = asyncio.create_task(coord.seal())
    await asyncio.sleep(0.05)  # residual INSERT in flight; phase already FLUSHED
    coord.queue(
        "public.cx_flush_order", {"id": "late", "status": "completed"}, op_type="update"
    )
    await asyncio.wait_for(sealing, _OUTER)
    await asyncio.wait_for(coord.drain_late_writes(), _OUTER)

    assert lost == [], f"a late UPDATE overtook its row's INSERT: {lost}"
    assert committed["late"]["status"] == "completed"
