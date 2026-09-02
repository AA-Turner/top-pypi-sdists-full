"""The durable frontier must never report an empty queue it cannot actually see.

`work_item_counts` fills missing states with 0, so a read returning NO ROWS is
indistinguishable from a drained queue — and the crawler's terminal condition is
exactly `pending == 0 and in_flight == 0`. That is how a truncated crawl came to
be recorded as a success with `pages_fetched: 0`.

`runtime.work_item` carries an RLS SELECT policy (`iam.has_access('work_item',
id)`) that evaluates FALSE for every row today, so any read of the table as role
`authenticated` returns zero rows silently. Work items are never deleted, only
transitioned, so a total that goes from N > 0 to 0 is provably a failed READ.
"""

from __future__ import annotations

import pytest

pytest.importorskip("matrx_runtime")

from matrx_scraper.web_crawl.runtime_queue import FrontierReadError  # noqa: E402
from matrx_runtime import WorkItemState  # noqa: E402

from matrx_scraper.web_crawl.runtime_queue import RuntimeWorkQueueBackend  # noqa: E402

EXEC = "exec-honesty"


class _Store:
    """Counts the backend reads; can be told to go blind mid-crawl."""

    def __init__(self, *, pending: int = 0, in_progress: int = 0) -> None:
        self.blind = False
        self.reads = 0
        self._counts = {state: 0 for state in WorkItemState}
        self._counts[WorkItemState.PENDING] = pending
        self._counts[WorkItemState.IN_PROGRESS] = in_progress

    async def work_item_counts(self, execution_id: str):  # noqa: ANN001, ANN201
        self.reads += 1
        if self.blind:
            return {state: 0 for state in WorkItemState}
        return dict(self._counts)


def _backend(store: _Store) -> RuntimeWorkQueueBackend:
    return RuntimeWorkQueueBackend(store, EXEC, holder="h:1")


@pytest.mark.asyncio
async def test_normal_counts_pass_through() -> None:
    backend = _backend(_Store(pending=3, in_progress=1))
    assert await backend.counts() == (3, 1)


@pytest.mark.asyncio
async def test_a_genuinely_empty_frontier_is_fine() -> None:
    """Zero is only a lie if we previously saw rows. A queue that was always
    empty (or drained before this backend ever read it) must not raise."""
    backend = _backend(_Store())
    assert await backend.counts() == (0, 0)


@pytest.mark.asyncio
async def test_draining_to_zero_is_fine() -> None:
    """The real success path: items existed, then reached a terminal state.
    Terminal items still COUNT, so the total never drops to zero."""
    store = _Store(pending=2)
    backend = _backend(store)
    assert await backend.counts() == (2, 0)
    store._counts[WorkItemState.PENDING] = 0
    store._counts[WorkItemState.SUCCEEDED] = 2
    assert await backend.counts() == (0, 0), "a drained queue is still (0, 0) pending/in-flight"


@pytest.mark.asyncio
async def test_frontier_that_vanishes_retries_then_raises() -> None:
    """THE bug: the rows stop being visible mid-crawl. Reconcile first (one
    re-read), then refuse — never report the frontier empty."""
    store = _Store(pending=1, in_progress=1)
    backend = _backend(store)
    assert await backend.counts() == (1, 1)
    reads_before = store.reads

    store.blind = True
    with pytest.raises(FrontierReadError) as exc:
        await backend.counts()

    assert store.reads - reads_before == 2, "must re-read once before giving up"
    message = str(exc.value)
    assert "did not drain" in message
    assert "RLS" in message, "the message must name the known cause, not just fail"


@pytest.mark.asyncio
async def test_a_transient_blind_read_is_reconciled_not_fatal() -> None:
    """A guard that CAN reconcile MUST reconcile — one bad read recovers."""

    class _Flaky(_Store):
        async def work_item_counts(self, execution_id: str):  # noqa: ANN001, ANN201
            self.reads += 1
            if self.reads == 2:  # the first re-read after a good read
                return {state: 0 for state in WorkItemState}
            return dict(self._counts)

    store = _Flaky(pending=1)
    backend = _backend(store)
    assert await backend.counts() == (1, 0)
    # Second call: first read blind, retry succeeds.
    assert await backend.counts() == (1, 0)
