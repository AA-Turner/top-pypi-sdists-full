"""Task-scoped in-memory cache + write queue for Layer 1 micro-compaction.

Layer 1 (``XPanderContextOptimizer.maybe_offload_content``) used to write the
encrypted blob to the agent's workspace synchronously and only return the
preview + retrieval pointer to the LLM after the HTTP round-trip resolved.
Cold-start workspace boots are seconds, so the agent blocked on each large
tool result even though the encrypted bytes were already in process.

This cache splits the two:

* ``put(context_id, encrypted, ...)`` stores the bytes in memory immediately
  and spawns an asyncio.Task that POSTs to the workspace in the background.
* ``get(context_id)`` returns the in-memory entry — used by the agno tool
  hook to short-circuit ``xpworkspace-context-retrieve`` without paying for
  the round-trip.
* ``aflush()`` is the barrier — every workspace op that is NOT a cached
  context-optimization read awaits this so the sandbox is consistent before
  bash/exec/etc. observe it.
* ``aclose()`` drains pending writes at task end.

The cache is task-scoped: instantiated once per ``XPanderContextOptimizer``,
GC'd when the optimizer is. Cross-task leakage is impossible because the
encryption key is derived from ``org_id + agent_id + task_id`` — even if a
context_id collided, the decrypt would fail.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Dict, List, Optional

from loguru import logger


@dataclass
class WorkspaceCacheEntry:
    """A single offloaded blob held in memory while its workspace write
    is in flight (or after it has flushed — entries persist until the
    cache is closed at task end).
    """

    encrypted: str
    """The base64-encoded ciphertext that was POSTed (or is about to be)
    to ``CONTEXT_OPTIMIZATION/<context_id>.xp``. Stored verbatim so a cache
    hit on retrieve can decrypt with the same routine the workspace path
    uses, with no second source of truth."""

    size: int
    """Original (plaintext) char count, kept for stats reporting only."""

    workspace_path: str
    """The full ``CONTEXT_OPTIMIZATION/<id>.xp`` path the preview points
    at. Convenient for log lines and the rare codepath that wants the
    canonical path for an entry."""

    created_at: float = field(default_factory=time.monotonic)
    """Wall-clock time the entry was put — useful for debug telemetry."""


CacheStats = Dict[str, float]


class WorkspaceCache:
    """In-memory cache + async write queue for L1 offloaded blobs.

    Not threadsafe — agno tool hooks run serially per turn on a single
    asyncio loop, which is the only writer. If that ever changes, wrap
    ``_entries`` / ``_pending`` mutations in an ``asyncio.Lock``.
    """

    def __init__(self) -> None:
        self._entries: Dict[str, WorkspaceCacheEntry] = {}
        self._pending: Dict[str, asyncio.Task] = {}
        self._errors: List[BaseException] = []
        self._stats: CacheStats = {
            "mem_hits": 0,
            "mem_misses": 0,
            "puts": 0,
            "pending_writes_peak": 0,
            "barrier_count": 0,
            "barrier_wait_ms_total": 0.0,
            "write_failures": 0,
        }

    # ------------------------------------------------------------------ #
    #  Mutation
    # ------------------------------------------------------------------ #

    def put(
        self,
        context_id: str,
        encrypted: str,
        size: int,
        workspace_path: str,
        do_write_async: Callable[[], Awaitable[None]],
    ) -> None:
        """Store *encrypted* in memory and spawn an async workspace write.

        Returns immediately — the caller can build the preview + pointer and
        hand control back to the LLM without waiting for the network.

        Args:
            context_id: UUID identifying the blob (the ``<uuid>`` part of
                ``CONTEXT_OPTIMIZATION/<uuid>.xp``).
            encrypted: Base64-encoded ciphertext.
            size: Plaintext char count, for stats.
            workspace_path: Full workspace path the preview will reference.
            do_write_async: Zero-arg coroutine factory that performs the
                actual workspace POST. The cache wraps it in an
                ``asyncio.create_task`` so the caller does not block.
        """
        self._entries[context_id] = WorkspaceCacheEntry(
            encrypted=encrypted,
            size=size,
            workspace_path=workspace_path,
        )
        self._stats["puts"] += 1

        task = asyncio.create_task(
            self._run_write(context_id, do_write_async),
            name=f"wcache-write:{context_id}",
        )
        self._pending[context_id] = task
        self._stats["pending_writes_peak"] = max(
            self._stats["pending_writes_peak"], len(self._pending)
        )
        logger.debug(
            f"[wcache] put ctx={context_id} size={size:,} "
            f"queue_depth={len(self._pending)}"
        )

    def enqueue_writeback(
        self,
        name: str,
        do_write_async: Callable[[], Awaitable[None]],
    ) -> None:
        """Queue a background workspace write WITHOUT storing an entry.

        Same barrier-flush semantics as ``put`` (the queued task lives in
        ``_pending`` and is awaited by ``aflush``), but no in-memory
        cache entry is created — used for append-mode writes (e.g. the
        action ledger appending one encrypted line per tool call) where
        the path is shared across many writes and the cache's
        ``context_id → blob`` model doesn't apply.

        The internal pending-key is uniquified per call so a caller
        passing a duplicate ``name`` (or letting the default suffix
        recycle once queue depth drops) cannot evict an in-flight task
        from ``_pending``. ``aflush`` only awaits tasks still keyed in
        the dict — overwriting a key would make the earlier write
        invisible to the barrier.
        """
        base_name = name or "wcache-writeback"
        pending_key = base_name
        suffix = 1
        while pending_key in self._pending:
            suffix += 1
            pending_key = f"{base_name}:{suffix}"
        task = asyncio.create_task(
            self._run_write(pending_key, do_write_async),
            name=pending_key,
        )
        self._pending[pending_key] = task
        self._stats["pending_writes_peak"] = max(
            self._stats["pending_writes_peak"], len(self._pending)
        )

    async def _run_write(
        self,
        context_id: str,
        do_write_async: Callable[[], Awaitable[None]],
    ) -> None:
        """Background write coroutine.

        Failures are captured into ``_errors`` for the next barrier flush
        to observe. We deliberately do NOT re-raise here: the spawned task
        is fire-and-forget from the optimizer's perspective and a re-raise
        would leave the task in a "task exception was never retrieved"
        state (asyncio logs that at GC time, polluting the user's logs).
        Errors are surfaced exactly once, on the next ``aflush()`` call.
        """
        try:
            await do_write_async()
        except BaseException as exc:
            self._stats["write_failures"] += 1
            self._errors.append(exc)
            logger.warning(f"[wcache] queued write failed ctx={context_id}: {exc}")
        finally:
            self._pending.pop(context_id, None)

    # ------------------------------------------------------------------ #
    #  Read
    # ------------------------------------------------------------------ #

    def get(self, context_id: str) -> Optional[WorkspaceCacheEntry]:
        """Return the cached entry for *context_id*, or ``None`` on miss.

        Updates ``mem_hits`` / ``mem_misses`` stats so callers don't have to.
        """
        entry = self._entries.get(context_id)
        if entry is not None:
            self._stats["mem_hits"] += 1
        else:
            self._stats["mem_misses"] += 1
        return entry

    def has_pending(self) -> bool:
        return bool(self._pending)

    # ------------------------------------------------------------------ #
    #  Barrier / drain
    # ------------------------------------------------------------------ #

    async def aflush(self) -> None:
        """Wait for every queued write to complete, then surface any errors.

        Called from the agno tool hook before any non-context-optimization
        ``xpworkspace-*`` tool runs. Any single queued-write failure is
        re-raised so the barrier op observes it loudly (the spec requires
        failures not be silently dropped).
        """
        t0 = time.monotonic()
        self._stats["barrier_count"] += 1

        if self._pending:
            tasks = list(self._pending.values())
            await asyncio.gather(*tasks, return_exceptions=True)

        # Surface the first queued error, then clear the buffer so the next
        # barrier doesn't re-raise the same error.
        if self._errors:
            err = self._errors.pop(0)
            self._errors.clear()
            self._stats["barrier_wait_ms_total"] += (time.monotonic() - t0) * 1000
            raise err

        self._stats["barrier_wait_ms_total"] += (time.monotonic() - t0) * 1000

    async def aclose(self) -> None:
        """Drain pending writes and clear the in-memory store.

        Called from ``XPanderContextOptimizer.aclose()`` at task end. Errors
        are logged but not raised — the task is finishing and the caller
        can't do anything productive with the exception at that point.
        """
        if self._pending:
            logger.info(
                f"[wcache] draining {len(self._pending)} pending write(s) at close"
            )
            tasks = list(self._pending.values())
            await asyncio.gather(*tasks, return_exceptions=True)

        if self._errors:
            for err in self._errors:
                logger.warning(f"[wcache] queued write error at close: {err}")
            self._errors.clear()

        self._entries.clear()
        self._pending.clear()

    # ------------------------------------------------------------------ #
    #  Stats
    # ------------------------------------------------------------------ #

    @property
    def stats(self) -> CacheStats:
        return self._stats
