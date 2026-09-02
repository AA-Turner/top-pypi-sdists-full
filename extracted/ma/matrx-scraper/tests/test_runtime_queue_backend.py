"""RuntimeWorkQueueBackend — the durable crawl frontier, driven exactly as the
SiteCrawler drives a QueueBackend, against the in-memory RML store (no DB).

Proves the adapter upholds the QueueBackend contract on durable storage AND that a
crash mid-crawl (a claimed-but-unsettled item whose lease expires) is recovered with
zero dropped / zero duplicated URLs — the whole point of the swap.
"""

from __future__ import annotations

import pytest

pytest.importorskip("matrx_runtime")

from matrx_runtime import WorkItemState  # noqa: E402
from matrx_runtime.store import InMemoryExecutionStore  # noqa: E402

from matrx_scraper.queue_backend import QueueItem  # noqa: E402
from matrx_scraper.web_crawl.runtime_queue import RuntimeWorkQueueBackend  # noqa: E402

EXEC = "batch-exec-1"


def _backend(store, holder="proc-A", lease=600):
    return RuntimeWorkQueueBackend(store, EXEC, holder=holder, lease_seconds=lease)


def _item(url, depth=0, parent=None, source="link"):
    return QueueItem(url=url, depth=depth, parent_url=parent, source=source)


@pytest.mark.asyncio
async def test_enqueue_dedups_by_canonical_identity() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    assert await q.enqueue(_item("https://x.test/a", source="seed")) is True
    # Same page, trailing slash + fragment — the ONE identity collapses them.
    assert await q.enqueue(_item("https://x.test/a/#frag")) is False
    assert await q.queue_depth() == 1


@pytest.mark.asyncio
async def test_enqueue_many_returns_only_the_newly_landed_items() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    await q.enqueue(_item("https://x.test/a"))
    landed = await q.enqueue_many(
        [_item("https://x.test/a"), _item("https://x.test/b"), _item("https://x.test/b")]
    )
    # 'a' already known, 'b' de-duped within the batch -> only one new 'b'.
    assert [i.url for i in landed] == ["https://x.test/b"]
    assert await q.queue_depth() == 2


@pytest.mark.asyncio
async def test_dequeue_claims_and_preserves_crawl_graph_position() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    await q.enqueue(_item("https://x.test/p", depth=3, parent="https://x.test/", source="link"))
    got = await q.dequeue()
    assert got is not None
    assert got.url == "https://x.test/p" and got.depth == 3
    assert got.parent_url == "https://x.test/" and got.source == "link"
    # Claimed -> in flight, not re-handed out.
    assert await q.dequeue() is None
    assert await q.in_flight_count() == 1


@pytest.mark.asyncio
async def test_mark_done_settles_the_right_item() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    await q.enqueue(_item("https://x.test/p"))
    got = await q.dequeue()
    await q.mark_done(got.url)
    assert await q.in_flight_count() == 0
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.SUCCEEDED] == 1


@pytest.mark.asyncio
async def test_mark_failed_will_retry_requeues_behind_a_gate() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    await q.enqueue(_item("https://x.test/p"))
    got = await q.dequeue()
    await q.mark_failed(got.url, "HTTP 429", will_retry=True)
    # Requeued (pending), but gated by backoff — not immediately re-claimable.
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.PENDING] == 1
    assert await q.dequeue() is None  # not_before gate


@pytest.mark.asyncio
async def test_known_urls_maps_identity_back_to_original_urls() -> None:
    store = InMemoryExecutionStore()
    q = _backend(store)
    await q.enqueue(_item("https://x.test/a"))
    # Ask with alias spellings; the ones whose identity is known come back as-asked.
    known = await q.known_urls(["https://x.test/a/", "https://x.test/a#f", "https://x.test/z"])
    assert known == {"https://x.test/a/", "https://x.test/a#f"}


@pytest.mark.asyncio
async def test_crash_recovery_a_dead_process_frontier_is_resumed_clean() -> None:
    """The reason for the swap: process A claims items and 'dies'; the item reaper
    reclaims them; process B resumes and finishes with zero dropped / zero duplicated."""
    store = InMemoryExecutionStore()
    a = _backend(store, holder="proc-A", lease=600)
    urls = [f"https://x.test/{i}" for i in range(5)]
    await a.enqueue_many([_item(u, source="seed") for u in urls])

    # Process A drains 2, then crashes holding the 3rd (claimed, never settled).
    done: set[str] = set()
    for _ in range(2):
        it = await a.dequeue()
        await a.mark_done(it.url)
        done.add(it.url)
    stuck = await a.dequeue()  # claimed by A, then A "dies" (never settles)
    assert stuck is not None

    # Reaper (host-scheduled) returns A's expired-lease item to pending.
    from datetime import UTC, datetime, timedelta

    future = datetime.now(UTC) + timedelta(seconds=601)
    assert await store.reclaim_expired_work_items(now=future) == 1

    # Process B resumes the SAME batch and drains the rest.
    b = RuntimeWorkQueueBackend(store, EXEC, holder="proc-B", lease_seconds=600)
    while True:
        it = await b.dequeue()
        if it is None:
            break
        await b.mark_done(it.url)
        done.add(it.url)

    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.SUCCEEDED] == 5  # zero dropped
    assert done == set(urls)
    assert sum(counts.values()) == 5  # zero duplicated


# ---------------------------------------------------------------------------
# The host factory: create/reuse the batch execution + build the backend.
# Driven through a REAL ExecutionEngine over the in-memory store (no DB).
# ---------------------------------------------------------------------------

from types import SimpleNamespace  # noqa: E402

from matrx_runtime import ExecutionEngine  # noqa: E402
from matrx_scraper.web_crawl.runtime_queue import (  # noqa: E402
    CRAWL_SESSION_LINK_KIND,
    get_or_create_crawl_execution,
    make_work_queue_factory,
)


def _prepared(session_id, org="org-1", user="user-1"):
    return SimpleNamespace(
        session_id=session_id,
        state=SimpleNamespace(organization_id=org, user_id=user),
    )


@pytest.mark.asyncio
async def test_factory_creates_a_batch_execution_linked_to_the_session() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    exec_id = await get_or_create_crawl_execution(
        engine, session_id="sess-1", organization_id="org-1", user_id="user-1"
    )
    linked = await engine.find_by_link(CRAWL_SESSION_LINK_KIND, "sess-1")
    assert [e.id for e in linked] == [exec_id]
    assert linked[0].type == "crawl"


@pytest.mark.asyncio
async def test_resume_reuses_the_same_execution_and_frontier() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    factory = make_work_queue_factory(engine)

    # First run seeds a frontier, drains one, then "crashes".
    q1 = await factory(_prepared("sess-1"))
    await q1.enqueue_many([_item(f"https://x.test/{i}") for i in range(3)])
    first = await q1.dequeue()
    await q1.mark_done(first.url)

    # Resume: a NEW backend for the SAME session must reuse the SAME batch execution
    # and see the SAME remaining pending frontier — not a fresh empty one.
    q2 = await factory(_prepared("sess-1"))
    assert q2._execution_id == q1._execution_id
    assert await q2.queue_depth() == 2  # the two never-drained items

    # Exactly one batch execution exists for the session.
    linked = await engine.find_by_link(CRAWL_SESSION_LINK_KIND, "sess-1")
    assert len(linked) == 1


# ---------------------------------------------------------------------------
# Execution lifecycle: a worked frontier's execution is RUNNING while worked,
# terminal when the run ends — never a pending row the integrity watchdog
# screams about forever, never a RUNNING row after the crawl finished.
# ---------------------------------------------------------------------------

from matrx_runtime import ExecutionStatus  # noqa: E402


@pytest.mark.asyncio
async def test_factory_execution_is_running_not_pending() -> None:
    """A created-and-being-worked execution must be RUNNING (unleased). A
    pending execution that is actively worked is exactly what the layer-2
    integrity watchdog exists to scream about."""
    engine = ExecutionEngine(InMemoryExecutionStore())
    factory = make_work_queue_factory(engine)
    q = await factory(_prepared("sess-lc-1"))
    ex = await engine.store.get_execution(q.execution_id)
    assert ex.status is ExecutionStatus.RUNNING
    assert ex.lease_holder is None  # unleased by design: the reaper must not
    assert ex.lease_expires_at is None  # kill a live long crawl mid-run


@pytest.mark.asyncio
async def test_finalize_settles_the_execution_terminal() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    factory = make_work_queue_factory(engine)

    q = await factory(_prepared("sess-lc-2"))
    await q.finalize("completed")
    ex = await engine.store.get_execution(q.execution_id)
    assert ex.status is ExecutionStatus.COMPLETED

    q2 = await factory(_prepared("sess-lc-3"))
    await q2.finalize("failed", error_message="boom")
    ex2 = await engine.store.get_execution(q2.execution_id)
    assert ex2.status is ExecutionStatus.FAILED

    q3 = await factory(_prepared("sess-lc-4"))
    await q3.finalize("cancelled")
    ex3 = await engine.store.get_execution(q3.execution_id)
    assert ex3.status is ExecutionStatus.CANCELLED


@pytest.mark.asyncio
async def test_finalize_after_finalize_is_a_loud_noop_not_a_crash() -> None:
    """The engine's terminal-once CAS makes a double settle raise internally;
    finalize must swallow it loudly — a finalize race must never mask the
    crawl's own outcome."""
    engine = ExecutionEngine(InMemoryExecutionStore())
    factory = make_work_queue_factory(engine)
    q = await factory(_prepared("sess-lc-5"))
    await q.finalize("completed")
    await q.finalize("failed", error_message="late loser")  # must not raise
    ex = await engine.store.get_execution(q.execution_id)
    assert ex.status is ExecutionStatus.COMPLETED  # first settle wins


@pytest.mark.asyncio
async def test_rerun_after_terminal_execution_gets_a_fresh_execution() -> None:
    """Re-crawling a session whose previous batch execution already settled
    must NOT resurrect or reuse the terminal execution — it gets a fresh one
    (terminal is forever; the old record stays as history)."""
    engine = ExecutionEngine(InMemoryExecutionStore())
    factory = make_work_queue_factory(engine)
    q1 = await factory(_prepared("sess-lc-6"))
    await q1.finalize("completed")
    q2 = await factory(_prepared("sess-lc-6"))
    assert q2.execution_id != q1.execution_id
    ex = await engine.store.get_execution(q2.execution_id)
    assert ex.status is ExecutionStatus.RUNNING


# ---------------------------------------------------------------------------
# Per-claim fencing (F2) + attempt-budget alignment (F3).
# ---------------------------------------------------------------------------

from datetime import UTC, datetime, timedelta  # noqa: E402

from matrx_scraper.web_crawl.runtime_queue import DEFAULT_ITEM_MAX_ATTEMPTS  # noqa: E402


@pytest.mark.asyncio
async def test_stale_claim_cannot_settle_a_newer_claim_of_the_same_item() -> None:
    """F2 regression: worker A's claim stalls past its lease, the reaper returns
    the item, worker B (SAME process holder prefix) re-claims and finishes it.
    A's late mark_done must LOSE the settle CAS — before per-claim fencing, A's
    settle matched B's claim (identical process-wide holder) and silently
    completed B's in-flight work, so B's own settle no-opped and the page was
    double-processed with corrupted accounting."""
    store = InMemoryExecutionStore()
    a = _backend(store, holder="proc-A")
    await a.enqueue(_item("https://x.test/slow"))

    got_a = await a.dequeue()
    assert got_a is not None

    # A stalls; the reaper returns the item; B (same backend/process) re-claims.
    future = datetime.now(UTC) + timedelta(seconds=601)
    assert await store.reclaim_expired_work_items(now=future) == 1
    b_view = RuntimeWorkQueueBackend(store, EXEC, holder="proc-A")
    got_b = await b_view.dequeue()
    assert got_b is not None and got_b.url == got_a.url

    # A's zombie settle must not touch B's claim.
    await a.mark_done(got_a.url)
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.IN_PROGRESS] == 1  # B still owns it
    assert counts[WorkItemState.SUCCEEDED] == 0

    # B's settle is the one that lands.
    await b_view.mark_done(got_b.url)
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.SUCCEEDED] == 1


@pytest.mark.asyncio
async def test_store_attempt_budget_outlasts_the_crawler_retry_policy() -> None:
    """F3 regression: the crawler's rate-limit policy is initial attempt + 5
    requeues. The store's per-item budget must survive ALL of them — when both
    caps were 5, the store dead-lettered the crawler's final requeue while the
    crawler believed the URL was still queued (silent page loss under
    coverage_complete=true)."""
    assert DEFAULT_ITEM_MAX_ATTEMPTS >= 8  # 6 legitimate claims + reclaim headroom

    store = InMemoryExecutionStore()
    # Zero retry backoff so the test can re-claim immediately — production's
    # 5s backoff only delays claimability, it never changes the budget.
    q = RuntimeWorkQueueBackend(store, EXEC, holder="proc-A", retry_backoff_seconds=0.0)
    await q.enqueue(_item("https://x.test/throttled"))

    # initial attempt + 5 rate-limit requeues, exactly the crawler's policy.
    for attempt in range(6):
        got = await q.dequeue()
        assert got is not None, f"item was dead-lettered at claim {attempt + 1}"
        if attempt < 5:
            await q.mark_failed(got.url, "http_429", will_retry=True)

    # After the 6th claim the crawler gives up terminally — its own decision.
    await q.mark_failed(got.url, "http_429: retries exhausted", will_retry=False)
    counts = await store.work_item_counts(EXEC)
    assert counts[WorkItemState.FAILED] == 1
    assert counts[WorkItemState.PENDING] == 0
