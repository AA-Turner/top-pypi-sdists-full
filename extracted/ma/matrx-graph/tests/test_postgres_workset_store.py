"""PostgresWorkSetStore integration tests — the production work-set frontier.

The store is wired in production (aidream package_integration configures
``PostgresWorkSetStore`` over ``workflow.work_item``) but had ZERO tests
until this file: its dedup insert, its FOR UPDATE SKIP LOCKED batch claim,
and its lease-expiry reclaim were unexercised against a real database.

Every test here is a forcing function on the REAL store + REAL Postgres:

- dedup at scale: hundreds of rows, overlapping duplicate canonical keys —
  only the unique-constraint path can produce the exact new-row counts.
- claim under GENUINE concurrency: many asyncio claimers race claim() on
  separate pool connections; only an atomic SKIP LOCKED claim yields zero
  double-claims with full coverage.
- real wall-clock lease expiry: a 1-second lease, an actual sleep, then
  reclaim_expired — no clock stubbing.

Skipped automatically when MATRX_GRAPH_TEST_DB is unset (same gate as
test_postgres_checkpointer.py). Bootstrap a scratch DB with
tests/ci/bootstrap_test_db.sh — NEVER production (tests/_db_guard.py
hard-fails on the production project ref).
"""

from __future__ import annotations

import asyncio
import os
from uuid import uuid4

import pytest

from matrx_graph.workset import PostgresWorkSetStore, WorkItemSeed

# Load the repo .env HERE, above the gate. The skip decision below reads
# process env, and other suites (anything importing aidream.config) load .env
# as an import side effect — so without this line the same commit skips when
# this file is collected alone and runs when it is collected second.
# Guard: scripts/check_test_gate_determinism.py
from dotenv import load_dotenv

load_dotenv()


pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("MATRX_GRAPH_TEST_DB"),
        reason="Set MATRX_GRAPH_TEST_DB=1 to run PostgresWorkSetStore integration tests.",
    ),
    pytest.mark.asyncio(loop_scope="session"),
]

TEST_USER_ID = os.environ.get("MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd")
TEST_ORGANIZATION_ID = os.environ.get(
    "MATRX_GRAPH_TEST_ORGANIZATION_ID", "3e790542-fdaf-40b2-8bf3-658bf94fe67f"
)


@pytest.fixture(scope="module", autouse=True)
def _bootstrap_db() -> None:
    from dotenv import load_dotenv

    load_dotenv()

    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="matrx-graph tests",
        additional_schemas=["auth"],
    )

    from ._db_guard import assert_not_production_db

    assert_not_production_db("supabase_automation_matrix")

    from matrx_graph.db import configure_standalone_db, reset_for_tests

    reset_for_tests()
    configure_standalone_db("supabase_automation_matrix")


async def _make_run():
    """workflow.work_item FKs workflow.run — every test needs a real run row.

    Returns (def_store, definition_row, run_id); archiving the definition
    cascades the run and its work items away.
    """
    from matrx_graph import Definition
    from matrx_graph.db import DefinitionStore, RunStore

    def_store = DefinitionStore()
    def_row = await def_store.create(
        name=f"workset-test-{uuid4()}", definition=Definition(), user_id=TEST_USER_ID
    )
    run_id = await RunStore().create(
        definition_id=def_row.id,
        definition_hash="workset-test",
        inputs={},
        user_id=TEST_USER_ID,
        organization_id=TEST_ORGANIZATION_ID,
    )
    return def_store, def_row, run_id


# ---------------------------------------------------------------------------
# bulk_insert_ignore dedup — at scale, across batches, across states
# ---------------------------------------------------------------------------


async def test_append_dedups_hundreds_of_items_across_batches():
    """400 unique keys arrive as three overlapping batches (300 + 300 with a
    200-key overlap + a full 400 replay). The exact new-row counts are only
    reachable through the (run_id, set_name, canonical_key) unique constraint
    — a store that inserted blindly or deduped in memory would diverge."""
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    try:
        batch_a = [WorkItemSeed(canonical_key=f"k{i}", payload={"i": i}) for i in range(300)]
        batch_b = [WorkItemSeed(canonical_key=f"k{i}", payload={"i": i}) for i in range(100, 500)]

        assert await store.append(run_id, "default", batch_a) == 300
        # 100..299 already exist — only 300..499 are new.
        assert await store.append(run_id, "default", batch_b) == 200
        # Full replay: every key exists in some state — zero new.
        assert await store.append(run_id, "default", batch_a + batch_b) == 0

        counts = await store.counts(run_id, "default")
        assert counts.discovered == 500
        assert counts.pending == 500

        # Dedup must hold across STATES too: settle one item, replay its key.
        [claim] = await store.claim(
            run_id, "default", limit=1, holder="h", lease_seconds=60, wave=1
        )
        assert await store.complete(claim.id, run_id=run_id)
        assert (
            await store.append(
                run_id,
                "default",
                [WorkItemSeed(canonical_key=claim.canonical_key, payload={"replayed": True})],
            )
            == 0
        )
        counts = await store.counts(run_id, "default")
        assert counts.discovered == 500  # not resurrected, not duplicated
        assert counts.succeeded == 1

        # A DIFFERENT set_name is a separate identity space.
        assert await store.append(run_id, "other", batch_a[:5]) == 5
    finally:
        await def_store.archive(def_row.id)


async def test_append_same_key_different_sets_and_runs_are_distinct():
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    def_store2, def_row2, run_id2 = await _make_run()
    try:
        seed = [WorkItemSeed(canonical_key="shared", payload={})]
        assert await store.append(run_id, "default", seed) == 1
        assert await store.append(run_id2, "default", seed) == 1
        assert (await store.counts(run_id, "default")).discovered == 1
        assert (await store.counts(run_id2, "default")).discovered == 1
    finally:
        await def_store.archive(def_row.id)
        await def_store2.archive(def_row2.id)


# ---------------------------------------------------------------------------
# claim_batch under genuine concurrency — FOR UPDATE SKIP LOCKED
# ---------------------------------------------------------------------------


async def test_concurrent_claimers_never_double_claim():
    """8 claimers drain 240 items concurrently, 10 at a time, on separate
    pool connections. SKIP LOCKED is the ONLY thing standing between them
    and a double-claim: a SELECT-then-UPDATE split (or a missing lock)
    hands the same row to two claimers and the id-multiset below gains a
    duplicate. Full coverage proves nothing was dropped either."""
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    try:
        total = 240
        await store.append(
            run_id,
            "default",
            [WorkItemSeed(canonical_key=f"c{i}", payload={"i": i}) for i in range(total)],
        )

        async def drain(holder: str) -> list[str]:
            claimed: list[str] = []
            while True:
                batch = await store.claim(
                    run_id, "default", limit=10, holder=holder, lease_seconds=120, wave=1
                )
                if not batch:
                    return claimed
                claimed.extend(c.id for c in batch)
                await asyncio.sleep(0)  # interleave with the other claimers

        results = await asyncio.gather(*[drain(f"claimer-{n}") for n in range(8)])
        all_ids = [item_id for ids in results for item_id in ids]

        assert len(all_ids) == total, "items dropped or over-claimed"
        assert len(set(all_ids)) == total, "DOUBLE-CLAIM: same item handed to two claimers"

        counts = await store.counts(run_id, "default")
        assert counts.in_progress == total
        assert counts.pending == 0

        # Every claim recorded exactly one attempt — a double-claim would
        # have bumped a row to attempts=2.
        from matrx_graph.db._registry import get_model

        rows = (
            await get_model("WfWorkItem")
            .filter(run_id=run_id, set_name="default")
            .values("attempts")
        )
        assert {row["attempts"] for row in rows} == {1}
    finally:
        await def_store.archive(def_row.id)


async def test_claim_orders_fifo_by_seq_and_respects_limit():
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    try:
        for key in ("first", "second", "third"):
            await store.append(run_id, "default", [WorkItemSeed(canonical_key=key)])
        batch = await store.claim(run_id, "default", limit=2, holder="h", lease_seconds=60, wave=1)
        assert [c.canonical_key for c in batch] == ["first", "second"]
        rest = await store.claim(run_id, "default", limit=2, holder="h", lease_seconds=60, wave=2)
        assert [c.canonical_key for c in rest] == ["third"]
        assert rest[0].wave == 2
    finally:
        await def_store.archive(def_row.id)


# ---------------------------------------------------------------------------
# Real wall-clock lease expiry + reclaim_expired
# ---------------------------------------------------------------------------


async def test_lease_expires_in_real_time_and_reclaims_to_pending():
    """A 1-second lease actually expires: claim, sleep past the lease,
    reclaim → the item is pending again and re-claimable with attempts=2.
    Reclaim before expiry must be a no-op — that half proves reclaim reads
    the REAL clock rather than reclaiming everything in_progress."""
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    try:
        await store.append(run_id, "default", [WorkItemSeed(canonical_key="leased")])
        [claim] = await store.claim(
            run_id, "default", limit=1, holder="worker-1", lease_seconds=1, wave=1
        )
        assert claim.attempts == 1

        # Live lease — nothing to reclaim yet.
        assert await store.reclaim_expired(run_id, "default") == 0
        assert (await store.counts(run_id, "default")).in_progress == 1

        await asyncio.sleep(1.3)  # real wall clock — the lease lapses

        assert await store.reclaim_expired(run_id, "default") == 1
        counts = await store.counts(run_id, "default")
        assert counts.pending == 1
        assert counts.in_progress == 0

        [reclaim] = await store.claim(
            run_id, "default", limit=1, holder="worker-2", lease_seconds=60, wave=2
        )
        assert reclaim.id == claim.id
        assert reclaim.attempts == 2
    finally:
        await def_store.archive(def_row.id)


async def test_reclaim_dead_letters_past_max_attempts():
    """max_attempts=2: two claim+expiry cycles exhaust the budget — the
    third reclaim lands the item in dead_letter, never back to pending.
    A neighbouring item with budget left goes back to pending in the SAME
    reclaim call (both UPDATE branches fire)."""
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    try:
        await store.append(
            run_id,
            "default",
            [
                WorkItemSeed(canonical_key="doomed", max_attempts=2),
                WorkItemSeed(canonical_key="survivor", max_attempts=5),
            ],
        )

        # Cycle 1: both claimed, lease lapses, both reclaimed to pending.
        assert (
            len(await store.claim(run_id, "default", limit=10, holder="h", lease_seconds=1, wave=1))
            == 2
        )
        await asyncio.sleep(1.3)
        assert await store.reclaim_expired(run_id, "default") == 2
        assert (await store.counts(run_id, "default")).pending == 2

        # Cycle 2: attempts hit 2 — doomed is exhausted, survivor is not.
        assert (
            len(await store.claim(run_id, "default", limit=10, holder="h", lease_seconds=1, wave=2))
            == 2
        )
        await asyncio.sleep(1.3)
        assert await store.reclaim_expired(run_id, "default") == 2

        counts = await store.counts(run_id, "default")
        assert counts.dead_letter == 1
        assert counts.pending == 1

        # The dead-lettered item is NEVER claimable again.
        remaining = await store.claim(
            run_id, "default", limit=10, holder="h", lease_seconds=60, wave=3
        )
        assert [c.canonical_key for c in remaining] == ["survivor"]
    finally:
        await def_store.archive(def_row.id)


# ---------------------------------------------------------------------------
# Settle idempotency on Postgres
# ---------------------------------------------------------------------------


async def test_settle_idempotent_and_run_scoped():
    """complete/fail are guarded single-row UPDATEs: first settle wins,
    replays return False, a settled item can't flip state, and a wrong
    run_id can never settle another run's item."""
    store = PostgresWorkSetStore()
    def_store, def_row, run_id = await _make_run()
    def_store2, def_row2, run_id2 = await _make_run()
    try:
        await store.append(
            run_id,
            "default",
            [WorkItemSeed(canonical_key="ok"), WorkItemSeed(canonical_key="bad")],
        )
        claims = {
            c.canonical_key: c
            for c in await store.claim(
                run_id, "default", limit=10, holder="h", lease_seconds=60, wave=1
            )
        }

        # Wrong run_id — must not settle (this is the cross-run fence).
        assert await store.complete(claims["ok"].id, run_id=run_id2) is False

        assert await store.complete(claims["ok"].id, run_id=run_id) is True
        assert await store.complete(claims["ok"].id, run_id=run_id) is False
        assert await store.fail(claims["ok"].id, run_id=run_id) is False

        error = {"code": "boom", "message": "it broke"}
        assert await store.fail(claims["bad"].id, run_id=run_id, error=error) is True
        assert await store.fail(claims["bad"].id, run_id=run_id) is False
        assert await store.complete(claims["bad"].id, run_id=run_id) is False

        counts = await store.counts(run_id, "default")
        assert counts.succeeded == 1
        assert counts.failed == 1
        assert counts.drained

        # The failure error landed on the row (operator forensics).
        from matrx_graph.db._registry import get_model

        row = await get_model("WfWorkItem").filter(id=claims["bad"].id).first()
        assert row.error == error

        # A settled item is invisible to reclaim (no lease left to expire).
        assert await store.reclaim_expired(run_id, "default") == 0
    finally:
        await def_store.archive(def_row.id)
        await def_store2.archive(def_row2.id)
