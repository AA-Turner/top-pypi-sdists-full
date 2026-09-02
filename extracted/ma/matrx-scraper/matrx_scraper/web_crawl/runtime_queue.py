"""Durable crawl frontier — a `QueueBackend` backed by the matrx-runtime work queue.

The `SiteCrawler` already drives the tiny `QueueBackend` protocol; this is a durable
implementation of it, so a crawl becomes crash-safe by construction (the platform
standard: common-docs/policies/durable-work-queue-standard.md) with ZERO change to
the crawler's fetch/parse/persist/stream logic. Swap `InMemoryQueueBackend()` for
this and a deploy/OOM/restart mid-crawl is a non-event: the frontier lives in
`runtime.work_item`, a restarted worker resumes claiming, and the item reaper
returns any in-flight items whose worker died.

The batch job is one `global_execution` (created by the host, linked to the crawl
session); its id is the item scope. Runtime stays payload-blind — the crawler's URL
is the opaque `canonical_key` (via the ONE `normalize_url` identity) + a `raw_key`
and a small opaque `payload` (depth/parent/source) runtime never reads.

matrx-runtime is an OPTIONAL dependency (the `durable` extra): importing this module
requires it, but the package crawls standalone on `InMemoryQueueBackend` without it.
"""

from __future__ import annotations

import asyncio
import logging
import os
import socket
import uuid
from collections import defaultdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from collections.abc import Awaitable, Callable

from matrx_runtime import (
    ExecutionError,
    ExecutionStatus,
    ExecutionStore,
    Request,
    WorkItemSeed,
    WorkItemState,
    is_terminal,
)

from matrx_scraper.queue_backend import QueueItem
from matrx_scraper.utils.url import normalize_url

if TYPE_CHECKING:  # avoid a hard import cycle; the host passes a live engine
    from matrx_runtime import ExecutionEngine

# The opaque link between a batch execution and the crawl session it durably backs.
CRAWL_SESSION_LINK_KIND = "web_crawl_session"


class FrontierReadError(RuntimeError):
    """A frontier read could not be trusted, so the crawl stops LOUDLY.

    Raised only when the durable queue reports zero rows for an execution that
    previously had them. Work items are never deleted, so that is a failed READ,
    not a drained queue — and silently believing it is what turns a truncated
    crawl into a recorded success.
    """


# Generous vs a page fetch (seconds); long enough that a slow browser render never
# lets the reaper reclaim a still-live item. A CAPS constant, not config.
DEFAULT_ITEM_LEASE_SECONDS = 600
# Small secondary backoff for a requeued (will_retry) item — the crawler's own
# adaptive host rate-limiter is the real pacer; this just avoids a hot re-claim.
DEFAULT_RETRY_BACKOFF_SECONDS = 5.0
# The store's attempt budget per item. MUST stay comfortably above the
# crawler's own retry policy (initial attempt + MAX_RATE_LIMIT_RETRIES=5
# requeues = 6 claims) plus headroom for lease reclaims, each of which burns
# an attempt. When the two caps were the SAME number (5), the store
# dead-lettered a rate-limited item on the crawler's last requeue while the
# crawler believed it was queued — pages silently vanished under
# `coverage_complete=true` (FOUND_DEFECTS 2026-07-29 F3). The store cap is a
# zombie backstop, never the retry policy — the crawler decides retries.
DEFAULT_ITEM_MAX_ATTEMPTS = 12


logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(UTC)


class RuntimeWorkQueueBackend:
    """`QueueBackend` over the matrx-runtime durable work queue (one batch execution).

    One instance is shared by all of a run's `SiteCrawler` workers; they share the
    process `holder`, so if the process dies every in-flight item's lease expires and
    the reaper returns them to pending — the crash-recovery guarantee.
    """

    def __init__(
        self,
        store: ExecutionStore,
        execution_id: str,
        *,
        holder: str,
        lease_seconds: int = DEFAULT_ITEM_LEASE_SECONDS,
        retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
        engine: ExecutionEngine | None = None,
    ) -> None:
        self._store = store
        self._execution_id = execution_id
        self._holder = holder
        self._lease_seconds = lease_seconds
        self._retry_backoff_seconds = retry_backoff_seconds
        # Optional engine handle so the crawl service can settle the batch
        # execution's lifecycle (finalize) when the run ends. The frontier
        # itself only needs the store; the engine is lifecycle-only.
        self._engine = engine
        # url (as handed back from dequeue) -> (claimed item id, per-claim fencing
        # holder), so mark_done/mark_failed (which carry a url, not an id) settle
        # the right row — and ONLY the claim they belong to. The fencing suffix is
        # minted per dequeue: with a plain process-wide holder, worker A's stalled
        # claim could settle worker B's re-claim of the same item after a reclaim
        # (same holder string ⇒ the holder-CAS protected nothing between workers
        # of one process — FOUND_DEFECTS 2026-07-29 F2).
        self._in_flight: dict[str, tuple[str, str]] = {}
        self._lock = asyncio.Lock()
        # Highest total row count this backend has ever observed for the
        # execution. Work items are NEVER deleted — they only change state — so
        # this number can only grow. See `counts()`: it is what makes an
        # all-zero reading provably a LIE rather than an empty frontier.
        self._max_total_seen = 0

    def _seed(self, item: QueueItem) -> WorkItemSeed:
        return WorkItemSeed(
            canonical_key=normalize_url(item.url),
            raw_key=item.url,
            payload={"depth": item.depth, "parent_url": item.parent_url, "source": item.source},
            max_attempts=DEFAULT_ITEM_MAX_ATTEMPTS,
        )

    async def enqueue(self, item: QueueItem) -> bool:
        landed = await self._store.seed_work_items(
            self._execution_id, [self._seed(item)], now=_now()
        )
        return bool(landed)

    async def enqueue_many(self, items: list[QueueItem]) -> list[QueueItem]:
        # De-dupe within the batch by canonical identity (a page links the same URL
        # several times); the caller must not be told the same URL landed twice.
        by_key: dict[str, QueueItem] = {}
        for item in items:
            by_key.setdefault(normalize_url(item.url), item)
        if not by_key:
            return []
        landed = set(
            await self._store.seed_work_items(
                self._execution_id, [self._seed(it) for it in by_key.values()], now=_now()
            )
        )
        return [item for key, item in by_key.items() if key in landed]

    async def dequeue(self) -> QueueItem | None:
        # Per-claim fencing token: process-stable prefix (so a dead process's
        # claims are recognizable) + a unique suffix per claim (so a stale
        # worker's settle can never CAS-match a NEWER claim of the same item).
        claim_holder = f"{self._holder}:{uuid.uuid4().hex[:12]}"
        claimed = await self._store.claim_work_items(
            self._execution_id,
            holder=claim_holder,
            lease_seconds=self._lease_seconds,
            limit=1,
            now=_now(),
        )
        if not claimed:
            return None
        it = claimed[0]
        payload = it.payload or {}
        url = it.raw_key or it.canonical_key
        async with self._lock:
            self._in_flight[url] = (it.id, claim_holder)
        return QueueItem(
            url=url,
            depth=int(payload.get("depth", 0)),
            parent_url=payload.get("parent_url"),
            source=payload.get("source", "link"),
        )

    async def mark_done(self, url: str) -> None:
        async with self._lock:
            entry = self._in_flight.pop(url, None)
        if entry is not None:
            item_id, claim_holder = entry
            try:
                settled = await self._store.complete_work_item(
                    item_id, holder=claim_holder, now=_now()
                )
            except Exception:
                # A store blip must not orphan the claim locally: restore the
                # entry so the caller's failure handler (mark_failed) can still
                # settle this item instead of leaving it to the 600s lease.
                async with self._lock:
                    self._in_flight.setdefault(url, entry)
                raise
            if not settled:
                # The lease expired mid-work and the item was reclaimed (and
                # possibly re-worked) by a newer claim. Losing the CAS is the
                # CORRECT outcome — but it means duplicate work happened, so
                # say it loudly.
                logger.warning(
                    "durable crawl frontier: mark_done(%s) lost the settle CAS — "
                    "the item's lease expired and a newer claim owns it (item %s)",
                    url,
                    item_id,
                )

    async def mark_failed(self, url: str, error: str, will_retry: bool = False) -> None:
        async with self._lock:
            entry = self._in_flight.pop(url, None)
        if entry is not None:
            item_id, claim_holder = entry
            try:
                state = await self._store.fail_work_item(
                    item_id,
                    holder=claim_holder,
                    error=ExecutionError(error_type="crawl_item_failed", message=str(error)[:2000]),
                    retry=will_retry,
                    backoff_seconds=self._retry_backoff_seconds,
                    now=_now(),
                )
            except Exception:
                async with self._lock:
                    self._in_flight.setdefault(url, entry)
                raise
            if state is None:
                # Lost the settle CAS — the lease expired and a newer claim owns
                # the item. Same anomaly the mark_done path warns about.
                logger.warning(
                    "durable crawl frontier: mark_failed(%s) lost the settle CAS — "
                    "the item's lease expired and a newer claim owns it (item %s)",
                    url,
                    item_id,
                )
            elif will_retry and state in (WorkItemState.DEAD_LETTER, WorkItemState.FAILED):
                # The caller asked for a requeue but the store's attempt budget
                # (the zombie backstop) terminally settled the item instead
                # (stores report budget exhaustion as DEAD_LETTER). The budget
                # sits far above the crawler's own retry policy, so this firing
                # means reclaim churn ate the headroom — a real anomaly, never
                # business as usual. SCREAM: the crawler believes this URL is
                # still queued.
                logger.error(
                    "durable crawl frontier: item %s (%s) was DEAD-LETTERED (%s) by "
                    "the store's attempt budget despite a requeue request — the crawl "
                    "will report this URL neither fetched nor failed. Reclaim churn "
                    "exhausted %d attempts; investigate worker health.",
                    item_id,
                    url,
                    state.value,
                    DEFAULT_ITEM_MAX_ATTEMPTS,
                )

    async def is_known(self, url: str) -> bool:
        found = await self._store.existing_work_item_keys(self._execution_id, [normalize_url(url)])
        return bool(found)

    async def known_urls(self, urls: list[str]) -> set[str]:
        # Map canonical identity back to the ORIGINAL urls the caller passed, so the
        # crawler's ledger records the exact anchor it saw.
        key_to_urls: dict[str, list[str]] = defaultdict(list)
        for u in urls:
            key_to_urls[normalize_url(u)].append(u)
        existing = await self._store.existing_work_item_keys(self._execution_id, list(key_to_urls))
        return {u for key in existing for u in key_to_urls[key]}

    async def counts(self) -> tuple[int, int]:
        """(pending, in_flight) — and it REFUSES to report a frontier that vanished.

        The crawler's terminal condition is `pending == 0 and in_flight == 0`, so
        this read decides when a crawl stops. `work_item_counts` builds its result
        from a GROUP BY and fills every missing state with 0 — which means a query
        that returns NO ROWS is indistinguishable from a genuinely drained queue.
        There is no exception and no log; the crawl simply stops and reports
        success.

        A read can return no rows for reasons that have nothing to do with the
        queue. `runtime.work_item` carries an RLS SELECT policy
        (`iam.has_access('work_item', id)`) that currently evaluates FALSE for
        every row, so ANY read of this table as role `authenticated` returns zero
        rows — silently. The durable frontier is worker-owned infrastructure and
        must never be read that way, but "must never" is not a guarantee, and the
        cost of being wrong is a truncated crawl recorded as a success.

        So we make the lie impossible to tell: work items are never deleted, only
        transitioned, so the TOTAL row count for an execution can only ever grow.
        If we have previously seen N > 0 rows and now see zero, the frontier did
        not empty — the read did. Retry once (a transient blip deserves
        reconciliation, per the guard doctrine), then RAISE, because every
        alternative silently abandons the user's crawl.
        """
        pending, in_flight = await self._read_counts()
        return pending, in_flight

    async def _read_counts(self, *, _retrying: bool = False) -> tuple[int, int]:
        c = await self._store.work_item_counts(self._execution_id)
        total = sum(c.values())
        if total == 0 and self._max_total_seen > 0:
            if not _retrying:
                logger.warning(
                    "durable frontier read returned NO rows for execution %s after "
                    "previously seeing %s — re-reading before trusting it.",
                    self._execution_id,
                    self._max_total_seen,
                )
                return await self._read_counts(_retrying=True)
            raise FrontierReadError(
                f"durable frontier for execution {self._execution_id} read as EMPTY "
                f"but {self._max_total_seen} work item(s) were previously visible. "
                "Work items are never deleted, so the queue did not drain — the READ "
                "failed (an RLS-scoped connection returns zero rows for this table "
                "silently). Refusing to report an empty frontier: that is what makes "
                "a truncated crawl look like a successful one."
            )
        self._max_total_seen = max(self._max_total_seen, total)
        return c[WorkItemState.PENDING], c[WorkItemState.IN_PROGRESS]

    async def dead_letter_count(self) -> int:
        """How many of this execution's items the store terminally parked.

        A dead-letter is the zombie backstop firing — the crawler believed the
        URL was still queued (it asked for a requeue) and the store refused.
        The crawler folds this into `coverage_complete`: a run with any
        dead-letters must never claim full coverage, because those URLs were
        neither fetched nor counted as failures.
        """
        c = await self._store.work_item_counts(self._execution_id)
        return c[WorkItemState.DEAD_LETTER]

    async def queue_depth(self) -> int:
        return (await self.counts())[0]

    async def in_flight_count(self) -> int:
        return (await self.counts())[1]

    @property
    def execution_id(self) -> str:
        return self._execution_id

    async def finalize(self, status: str, *, error_message: str | None = None) -> None:
        """Settle the batch execution when the crawl run ends.

        `status` is 'completed' | 'failed' | 'cancelled'. Without this the
        execution stays RUNNING forever and the layer-2 integrity watchdog
        screams about it on every sweep. Best-effort and idempotent from the
        caller's perspective: the engine's terminal-once CAS makes a second
        settle a no-op, and a settle failure is loud-logged, never raised —
        finalization must not mask the crawl's own outcome.
        """
        if self._engine is None:
            return
        error = ExecutionError(
            error_type="web_crawl_run",
            message=(error_message or status)[:2000],
        )
        try:
            if status == "completed":
                await self._engine.complete(self._execution_id)
            elif status == "cancelled":
                await self._engine.cancel(self._execution_id, error=error)
            else:
                await self._engine.fail(self._execution_id, error=error)
        except Exception:
            logger.exception(
                "durable crawl frontier: failed to settle execution %s as %s "
                "(the integrity watchdog will scream about it — that is the backstop)",
                self._execution_id,
                status,
            )


def _process_holder(session_id: str) -> str:
    """Process-stable holder shared by all of a run's workers, distinct across a
    restart (pid changes) so a crashed process's items become reclaimable."""
    return f"{session_id}:{socket.gethostname()}:{os.getpid()}"


async def get_or_create_batch_execution(
    engine: ExecutionEngine,
    *,
    execution_type: str,
    link_kind: str,
    link_id: str,
    organization_id: str,
    user_id: str | None,
) -> str:
    """The batch `global_execution` that anchors + scopes ONE durable frontier.

    The generic form of the crawl helper below — the resume semantics are the
    whole point of a durable frontier and must not be re-derived per feature.
    Idempotent per `(link_kind, link_id)`: on RESUME it finds the existing live
    execution by link and reuses it, so a restarted run claims the SAME pending
    frontier instead of a fresh empty one. Otherwise it creates the request +
    root execution. Returns the execution id.
    """
    existing = await engine.find_by_link(link_kind, link_id)
    live = [ex for ex in existing if not is_terminal(ex.status)]
    if live:
        ex = live[0]
        # A resumed pending/paused execution must be RUNNING while the crawl
        # works it — a pending row that is being worked is exactly what the
        # integrity watchdog screams about. Unleased by design: the reaper
        # must never terminate a live long crawl mid-run; a crashed crawl's
        # execution stays RUNNING-unleased and the watchdog is the loud alarm.
        if ex.status in (ExecutionStatus.PENDING, ExecutionStatus.PAUSED):
            await _start_reconciling(engine, ex.id)
        return ex.id
    request = Request(id=str(uuid.uuid4()), organization_id=organization_id, created_by=user_id)
    await engine.store.create_request(request)
    execution = await engine.create_root(
        type=execution_type,
        request_id=request.id,
        link_kind=link_kind,
        link_id=link_id,
    )
    # Created-then-worked in one breath: move PENDING → RUNNING immediately
    # (unleased — see above) so no run ever leaves a pending execution behind.
    await _start_reconciling(engine, execution.id)
    return execution.id


async def get_or_create_crawl_execution(
    engine: ExecutionEngine,
    *,
    session_id: str,
    organization_id: str,
    user_id: str | None,
) -> str:
    """The batch `global_execution` that anchors + scopes a crawl's work items."""
    return await get_or_create_batch_execution(
        engine,
        execution_type="crawl",
        link_kind=CRAWL_SESSION_LINK_KIND,
        link_id=session_id,
        organization_id=organization_id,
        user_id=user_id,
    )


async def _start_reconciling(engine: ExecutionEngine, execution_id: str) -> None:
    """`engine.start()` that RECONCILES a lost transition race instead of killing
    the request. Two crawls of one session can race PENDING → RUNNING; the loser's
    CAS raises — but "already RUNNING" is exactly the state we wanted, so a raise
    that resolves to an active execution is reconciled + logged, never propagated
    (the platform guard rule: a guard that CAN reconcile MUST reconcile)."""
    try:
        await engine.start(execution_id)
    except Exception:
        ex = await engine.store.get_execution(execution_id)
        if ex is not None and ex.status is ExecutionStatus.RUNNING:
            logger.warning(
                "durable crawl frontier: lost the start() race for execution %s — "
                "another runner moved it to RUNNING first; reconciled (COERCED).",
                execution_id,
            )
            return
        raise


def make_work_queue_factory(
    engine: ExecutionEngine,
) -> Callable[[object], Awaitable[RuntimeWorkQueueBackend]]:
    """Build the `work_queue_factory` a host wires via `configure_ext` — turns a crawl
    `PreparedCrawl` into a durable backend. The host owns the engine; this closes over
    it so the package's `run_prepared` can stay engine-agnostic.

        configure_ext(work_queue_factory=make_work_queue_factory(engine))
    """

    async def factory(prepared: object) -> RuntimeWorkQueueBackend:
        session_id = prepared.session_id  # type: ignore[attr-defined]
        state = prepared.state  # type: ignore[attr-defined]
        execution_id = await get_or_create_crawl_execution(
            engine,
            session_id=session_id,
            organization_id=state.organization_id,
            user_id=state.user_id,
        )
        return RuntimeWorkQueueBackend(
            engine.store,
            execution_id,
            holder=_process_holder(session_id),
            engine=engine,
        )

    return factory


__all__ = [
    "RuntimeWorkQueueBackend",
    "DEFAULT_ITEM_LEASE_SECONDS",
    "DEFAULT_ITEM_MAX_ATTEMPTS",
    "CRAWL_SESSION_LINK_KIND",
    "get_or_create_batch_execution",
    "get_or_create_crawl_execution",
    "make_work_queue_factory",
    "process_holder",
]


#: Public alias — a frontier other than the crawler's needs the same
#: process-stable-but-restart-distinct holder, and must not re-derive it.
process_holder = _process_holder
