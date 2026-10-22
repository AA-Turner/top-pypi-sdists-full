"""A settled crawl leaves no work behind — and a resume still carries what it closed.

Census 2026-10-21: 389 terminal crawl executions still held 50,461 `pending` work
items, because `finalize` settled the batch execution and never closed its queue
(the shared `WorkQueueDrainer` rule never reached the crawl's own loop). `finalize`
now closes every pending item to `failed`, `execution_<state>`; those items were
never fetched, so a resume carries them like pending ones.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

pytest.importorskip("matrx_runtime")

from matrx_runtime import ExecutionEngine, WorkItemState  # noqa: E402
from matrx_runtime.store import InMemoryExecutionStore  # noqa: E402

from matrx_scraper.queue_backend import QueueItem  # noqa: E402
from matrx_scraper.web_crawl.runtime_queue import make_work_queue_factory  # noqa: E402

SITE = "https://x.test/"
URLS = [f"{SITE}{p}" for p in ("", "a", "b", "c")]


def _prepared(session_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        session_id=session_id,
        state=SimpleNamespace(organization_id="org-1", user_id="user-1"),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["completed", "failed", "cancelled"])
async def test_finalize_closes_every_pending_item_naming_the_state(status: str) -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    q = await make_work_queue_factory(engine)(_prepared(f"sess-{status}"))
    await q.enqueue_many([QueueItem(url=u, depth=1, parent_url=SITE, source="link") for u in URLS])
    first = await q.dequeue()
    await q.mark_done(first.url)

    await q.finalize(status, error_message="run ended")

    counts = await engine.store.work_item_counts(q.execution_id)
    assert counts.get(WorkItemState.PENDING, 0) == 0
    closed = await engine.store.list_work_items(q.execution_id, states=[WorkItemState.FAILED], limit=10)
    assert len(closed) == len(URLS) - 1
    assert {it.error.error_type for it in closed} == {f"execution_{status}"}


@pytest.mark.asyncio
async def test_a_resume_carries_the_items_its_settled_execution_closed() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    q1 = await make_work_queue_factory(engine)(_prepared("sess-carry"))
    await q1.enqueue_many([QueueItem(url=u, depth=1, parent_url=SITE, source="link") for u in URLS])
    done = await q1.dequeue()
    await q1.mark_done(done.url)
    gone = await q1.dequeue()
    await q1.mark_failed(gone.url, "http 404", will_retry=False)
    await q1.finalize("cancelled", error_message="stopped")
    assert (await engine.store.work_item_counts(q1.execution_id)).get(WorkItemState.PENDING, 0) == 0

    q2 = await make_work_queue_factory(engine)(_prepared("sess-carry"))

    # The two never-fetched pages come forward; the fetched one and the real 404 do not.
    assert await q2.queue_depth() == 2
    assert not await q2.enqueue(QueueItem(url=done.url, depth=1, parent_url=SITE, source="link"))
    assert not await q2.enqueue(QueueItem(url=gone.url, depth=1, parent_url=SITE, source="link"))
