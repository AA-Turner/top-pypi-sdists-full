"""A resume after a crash, error or stop continues the frontier — it never re-crawls.

Live 2026-10-12, session 8beb27cd: the scraper redeploy killed the run, the
integrity reconciler marked its batch execution `failed`, and the resume found
no LIVE execution for the session, so it created a fresh, empty one and fetched
every page again. A terminal execution can never reopen; the resume now carries
its frontier forward: finished keys are never fetched again, unfinished ones
(pending, a dead process's claims, dead-letters) are seeded into the new queue.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

pytest.importorskip("matrx_runtime")

from matrx_runtime import ExecutionEngine  # noqa: E402
from matrx_runtime.store import InMemoryExecutionStore  # noqa: E402

from matrx_scraper.crawler import SiteCrawler, SiteCrawlerConfig  # noqa: E402
from matrx_scraper.queue_backend import QueueItem  # noqa: E402
from matrx_scraper.web_crawl.runtime_queue import make_work_queue_factory  # noqa: E402

from test_crawler import CapturingSink  # noqa: E402

SITE = "https://x.test/"
A, B, C, D, E = (f"{SITE}{p}" for p in ("", "b", "c", "d", "e"))


def _prepared(session_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        session_id=session_id,
        state=SimpleNamespace(organization_id="org-1", user_id="user-1"),
    )


def _item(url: str) -> QueueItem:
    return QueueItem(url=url, depth=1, parent_url=SITE, source="link")


async def _first_life(engine: ExecutionEngine) -> str:
    """A: fetched. B: failed for good. C: claimed when the process died. D: pending."""
    q1 = await make_work_queue_factory(engine)(_prepared("sess-r"))
    await q1.enqueue_many([_item(u) for u in (A, B, C, D)])
    claimed = {}
    for _ in range(3):
        it = await q1.dequeue()
        claimed[it.url] = it
    await q1.mark_done(A)
    await q1.mark_failed(B, "http 404", will_retry=False)
    # C stays claimed: the process dies here. The reconciler closes the execution.
    await q1.finalize("failed", error_message="producer settled as failed")
    return q1.execution_id


@pytest.mark.asyncio
async def test_a_resume_after_the_queue_was_closed_carries_its_frontier() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    first = await _first_life(engine)

    q2 = await make_work_queue_factory(engine)(_prepared("sess-r"))

    assert q2.execution_id != first  # a terminal execution cannot reopen
    assert await q2.queue_depth() == 2  # C and D, nothing else
    assert await q2.enqueue(_item(A)) is False  # fetched last life
    assert await q2.enqueue(_item(B)) is False  # recorded failed last life
    assert await q2.known_urls([A, B, E]) == {A, B}
    assert await q2.enqueue(_item(E)) is True  # genuinely new


@pytest.mark.asyncio
async def test_the_resumed_crawl_fetches_only_what_the_last_life_left() -> None:
    engine = ExecutionEngine(InMemoryExecutionStore())
    await _first_life(engine)
    q2 = await make_work_queue_factory(engine)(_prepared("sess-r"))
    crawler = SiteCrawler(
        run_id="sess-r",
        config=SiteCrawlerConfig(
            base_url=SITE,
            seed_from_sitemap=False,
            respect_robots=False,
            concurrency=1,
            max_pages=50,
            adaptive_pacing=False,
            host_rps=1000.0,
            host_burst=1000.0,
        ),
        event_sink=CapturingSink(),
        queue_backend=q2,
    )
    fetched: list[str] = []

    async def page_work(item: QueueItem) -> None:
        fetched.append(item.url)
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process_page = page_work  # type: ignore[method-assign]
    await crawler.run()

    assert sorted(fetched) == [C, D]


@pytest.mark.asyncio
async def test_a_frontier_larger_than_any_batch_or_old_cap_carries_completely(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Nothing is lost silently: 20,005 unfinished items (past the old 20,000
    cap) all come forward, seeded across many batches, and every one is
    verified present before the resume starts."""
    from matrx_runtime import WorkItemSeed

    from matrx_scraper.web_crawl import runtime_queue

    engine = ExecutionEngine(InMemoryExecutionStore())
    q1 = await make_work_queue_factory(engine)(_prepared("sess-big"))
    total = 20_005
    seeds = [WorkItemSeed(canonical_key=f"{SITE}p{i}", raw_key=f"{SITE}p{i}") for i in range(total)]
    await engine.store.seed_work_items(q1.execution_id, seeds, now=runtime_queue._now())
    await q1.finalize("failed", error_message="crashed")

    batches: list[int] = []
    real_seed = engine.store.seed_work_items

    async def counting_seed(execution_id, items, *, now):  # noqa: ANN001
        batches.append(len(items))
        return await real_seed(execution_id, items, now=now)

    monkeypatch.setattr(engine.store, "seed_work_items", counting_seed)
    q2 = await make_work_queue_factory(engine)(_prepared("sess-big"))

    assert await q2.queue_depth() == total
    assert sum(batches) == total
    assert len(batches) == -(-total // runtime_queue.PRIOR_CARRY_BATCH)
    assert max(batches) <= runtime_queue.PRIOR_CARRY_BATCH


@pytest.mark.asyncio
async def test_a_carry_that_does_not_land_refuses_the_resume_loudly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.web_crawl.runtime_queue import FrontierCarryError

    engine = ExecutionEngine(InMemoryExecutionStore())
    await _first_life(engine)

    async def lossy_seed(execution_id, items, *, now):  # noqa: ANN001, ARG001
        return []  # the store dropped them

    monkeypatch.setattr(engine.store, "seed_work_items", lossy_seed)
    with pytest.raises(FrontierCarryError, match="2 of 2 unfinished"):
        await make_work_queue_factory(engine)(_prepared("sess-r"))


@pytest.mark.asyncio
async def test_a_refused_resume_closes_the_execution_it_created(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_runtime import is_terminal

    from matrx_scraper.web_crawl.runtime_queue import CRAWL_SESSION_LINK_KIND, FrontierCarryError

    engine = ExecutionEngine(InMemoryExecutionStore())
    await _first_life(engine)

    async def lossy_seed(execution_id, items, *, now):  # noqa: ANN001, ARG001
        return []

    monkeypatch.setattr(engine.store, "seed_work_items", lossy_seed)
    with pytest.raises(FrontierCarryError):
        await make_work_queue_factory(engine)(_prepared("sess-r"))

    executions = await engine.find_by_link(CRAWL_SESSION_LINK_KIND, "sess-r")
    assert len(executions) == 2
    assert all(is_terminal(ex.status) for ex in executions)


def test_the_run_lease_beats_before_the_frontier_is_resolved() -> None:
    """A resume's carry happens inside `_resolve_durable_queue`; the lease must
    already be beating then, or a large carry reads as a dead run."""
    from matrx_utils.source_guard import stable_source

    from matrx_scraper.web_crawl.service import WebCrawlService

    source = stable_source(WebCrawlService._run_prepared)
    beat = source.index("self._heartbeat_run_lease(")
    resolve = source.index("self._resolve_durable_queue(prepared)")
    watcher = source.index("self._watch_for_cancel(")
    assert beat < resolve < watcher


@pytest.mark.asyncio
async def test_the_early_heartbeat_beats_the_lease_until_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio
    from datetime import timedelta

    from matrx_scraper.web_crawl import service as service_module

    monkeypatch.setattr(service_module, "RUN_LEASE_HEARTBEAT_EVERY", timedelta(seconds=0.01))
    beats: list[str] = []

    async def heartbeat_run_lease(session_id: str, token: str) -> bool:
        beats.append(token)
        return True

    repository = SimpleNamespace(heartbeat_run_lease=heartbeat_run_lease)
    task = asyncio.create_task(
        service_module.WebCrawlService._heartbeat_run_lease("s", repository, lease_token="lease-1")  # type: ignore[arg-type]
    )
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert len(beats) >= 3
