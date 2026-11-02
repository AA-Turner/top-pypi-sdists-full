from __future__ import annotations

import asyncio
import contextlib
import contextvars
import logging
import time
import uuid
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, TypeVar

from matrx_connect.lane.buckets import Bucket, DEFAULT_BUCKET_CAPS
from matrx_connect.lane.contextvar import (
    reset_current_lane,
    set_current_lane,
)
from matrx_connect.lane.priorities import TaskPriority, TaskRecord

T = TypeVar("T")

logger = logging.getLogger("matrx_connect.lane")


@dataclass(slots=True, frozen=True)
class FinalizerContext:
    """Outcome flags passed to lane finalizers when the request ends.

    ``failed`` — the main task raised an exception.
    ``soft`` — the main task was canceled (client disconnect / shutdown).
    Both false ⇒ normal stream end.
    """

    failed: bool
    soft: bool

    @property
    def outcome(self) -> str:
        if self.failed:
            return "error"
        if self.soft:
            return "cancelled"
        return "stream_end"


Finalizer = Callable[[FinalizerContext], Awaitable[None]]


@dataclass(slots=True)
class LaneConfig:
    """Per-lane defaults. Override per-process via configure() or per-lane at open()."""

    bucket_caps: dict[str, int] = field(
        default_factory=lambda: dict(DEFAULT_BUCKET_CAPS)
    )
    # Drain timeouts (seconds) applied AFTER the main task ends.
    blocking_drain_timeout: float = 60.0
    normal_drain_timeout: float = 10.0
    deferred_drain_timeout: float = 30.0
    # Retry — only when caller sets retry_safe=True.
    transient_retry_attempts: int = 2
    transient_retry_backoff: tuple[float, ...] = (0.25, 1.0)
    # How many TaskRecords to retain for observability.
    max_task_records: int = 1000


_global_config = LaneConfig()


def configure(**overrides: Any) -> None:
    """Override the process-wide LaneConfig defaults."""
    global _global_config
    import dataclasses
    current = {
        f.name: getattr(_global_config, f.name)
        for f in dataclasses.fields(_global_config)
    }
    current.update(overrides)
    _global_config = LaneConfig(**current)


def get_config() -> LaneConfig:
    return _global_config


# ── Errors ────────────────────────────────────────────────────────────────
class LaneClosedError(RuntimeError):
    """Raised when submitting to a lane that's already in `closed` phase."""


class LaneDrainTimeoutError(RuntimeError):
    """Raised internally when a priority tier exceeds its drain timeout."""


# ── Submission record ─────────────────────────────────────────────────────
@dataclass(slots=True)
class _Submission:
    """One submitted unit of work + its TaskRecord + the future caller awaits."""

    fn: Callable[[], Awaitable[Any]]
    record: TaskRecord
    future: asyncio.Future[Any]
    ctx_snapshot: contextvars.Context


# ── The lane ──────────────────────────────────────────────────────────────
class RequestLane:
    """Structured-concurrency primitive — one lane per cx_user_request.

    Owns every async operation spawned for a single user action: reads,
    writes, tool calls, deferred labelers, sub-workflow steps. Tasks are
    submitted via submit_blocking() / submit_normal() / submit_deferred().
    Each declares a bucket (e.g. "db_write") whose per-lane semaphore
    caps fan-out before any global queue/pool gating downstream.

    Lifecycle phases: ``active`` → ``draining`` → ``closed``.

    The lane is bound to a ContextVar on open() so spawned tasks inherit
    it automatically. Don't construct directly — use open() / open_async().
    """

    # ---------------------- construction ----------------------------------
    def __init__(
        self,
        *,
        lane_id: str | None = None,
        scope_kind: str = "request",
        context_snapshot: Mapping[str, Any] | None = None,
        config: LaneConfig | None = None,
        bucket_caps: Mapping[str, int] | None = None,
    ) -> None:
        self.id = lane_id or str(uuid.uuid4())
        self.scope_kind = scope_kind
        self.context_snapshot: dict[str, Any] = dict(context_snapshot or {})
        self.config = config or _global_config
        self.opened_at = time.monotonic()
        self.phase: str = "active"
        self._ctx_token: Any = None

        # Buckets: per-lane named semaphores.
        caps = dict(self.config.bucket_caps)
        if bucket_caps:
            caps.update(bucket_caps)
        self._buckets: dict[str, Bucket] = {
            name: Bucket(name, cap) for name, cap in caps.items()
        }

        # Bookkeeping.
        self._records: dict[str, TaskRecord] = {}
        self._tasks: set[asyncio.Task[Any]] = set()
        # Direct task→record id map so drain/cancel can filter by priority
        # without poking at task internals or relying on name parsing.
        self._task_to_record: dict[asyncio.Task[Any], str] = {}
        # Coalesce map keyed on (priority, coalesce_key) — only DEFERRED uses it.
        self._coalesce: dict[tuple[TaskPriority, str], asyncio.Future[Any]] = {}
        # Finalizers run at the very start of begin_drain — guaranteed end-of-
        # request hooks (persistence flush, metric flush, …). Each is wrapped
        # in asyncio.shield so it survives even soft-cancel drains.
        self._finalizers: list[tuple[str, Finalizer]] = []

    # ---------------------- public submission API -------------------------
    def submit_blocking(
        self,
        fn: Callable[[], Awaitable[T]],
        *,
        name: str,
        bucket: str = "default",
        retries: int = 0,
        retry_safe: bool = False,
        extra: Mapping[str, Any] | None = None,
    ) -> asyncio.Future[T]:
        """Submit a BLOCKING task. Caller is expected to ``await`` the future."""
        return self._submit(
            fn=fn,
            name=name,
            priority=TaskPriority.BLOCKING,
            bucket=bucket,
            retries=retries,
            retry_safe=retry_safe,
            coalesce_key=None,  # forbidden on BLOCKING
            extra=dict(extra or {}),
        )

    def submit_normal(
        self,
        fn: Callable[[], Awaitable[T]],
        *,
        name: str,
        bucket: str = "default",
        retries: int = 0,
        retry_safe: bool = False,
        extra: Mapping[str, Any] | None = None,
    ) -> asyncio.Future[T]:
        """Submit a NORMAL fire-and-forget task. Caller does NOT await."""
        return self._submit(
            fn=fn,
            name=name,
            priority=TaskPriority.NORMAL,
            bucket=bucket,
            retries=retries,
            retry_safe=retry_safe,
            coalesce_key=None,  # forbidden on NORMAL
            extra=dict(extra or {}),
        )

    def submit_deferred(
        self,
        fn: Callable[[], Awaitable[T]],
        *,
        name: str,
        bucket: str = "default",
        retries: int = 0,
        retry_safe: bool = False,
        coalesce_key: str | None = None,
        extra: Mapping[str, Any] | None = None,
    ) -> asyncio.Future[T]:
        """Submit a DEFERRED fire-and-forget task.

        coalesce_key: if another DEFERRED task with the same key is in-flight
        or queued on this lane, return its future instead of starting a new one.
        Solves the two-labelers-racing pattern.
        """
        if coalesce_key is not None:
            cached = self._coalesce.get((TaskPriority.DEFERRED, coalesce_key))
            if cached is not None and not cached.done():
                return cached  # type: ignore[return-value]
        return self._submit(
            fn=fn,
            name=name,
            priority=TaskPriority.DEFERRED,
            bucket=bucket,
            retries=retries,
            retry_safe=retry_safe,
            coalesce_key=coalesce_key,
            extra=dict(extra or {}),
        )

    # ---------------------- internal: actual submission -------------------
    def _submit(
        self,
        *,
        fn: Callable[[], Awaitable[Any]],
        name: str,
        priority: TaskPriority,
        bucket: str,
        retries: int,
        retry_safe: bool,
        coalesce_key: str | None,
        extra: dict[str, Any],
    ) -> asyncio.Future[Any]:
        if self.phase == "closed":
            raise LaneClosedError(
                f"RequestLane {self.id} is closed — cannot accept new tasks"
            )
        if self.phase == "draining" and priority != TaskPriority.DEFERRED:
            # During drain, only DEFERRED submissions are accepted (the
            # main task already ended, but deferred tail work is still
            # legitimately being submitted by post-completion handlers).
            raise LaneClosedError(
                f"RequestLane {self.id} is draining — only DEFERRED tasks accepted"
            )
        # Auto-provision unknown buckets at the default cap so callers don't
        # have to pre-register every bucket name they use.
        if bucket not in self._buckets:
            self._buckets[bucket] = Bucket(
                bucket, self.config.bucket_caps.get("default", 16)
            )

        record = TaskRecord(
            id=str(uuid.uuid4()),
            name=name,
            priority=priority,
            bucket=bucket,
            coalesce_key=coalesce_key,
            retry_safe=retry_safe,
            submitted_at=time.monotonic(),
            extra=extra,
        )
        self._records[record.id] = record
        self._trim_records()

        loop = asyncio.get_event_loop()
        future: asyncio.Future[Any] = loop.create_future()
        ctx_snapshot = contextvars.copy_context()
        submission = _Submission(
            fn=fn, record=record, future=future, ctx_snapshot=ctx_snapshot
        )

        task = loop.create_task(
            self._run_submission(submission, retries=retries),
            name=f"lane:{self.id[:8]}:{name}",
        )
        self._tasks.add(task)
        self._task_to_record[task] = record.id

        def _on_done(t: asyncio.Task[Any]) -> None:
            self._tasks.discard(t)
            self._task_to_record.pop(t, None)

        task.add_done_callback(_on_done)

        if coalesce_key is not None and priority == TaskPriority.DEFERRED:
            self._coalesce[(priority, coalesce_key)] = future
            future.add_done_callback(
                lambda _f, k=coalesce_key: self._coalesce.pop(
                    (TaskPriority.DEFERRED, k), None
                )
            )

        self._log_event("task_submitted", record)
        return future

    # ---------------------- runner ----------------------------------------
    async def _run_submission(self, sub: _Submission, *, retries: int) -> None:
        record = sub.record
        # Sub-task strict-priority gate — BLOCKING never has to wait on a
        # NORMAL/DEFERRED bucket-holder if they share the same bucket.
        # Realized via the bucket semaphore (cooperative — lower-priority
        # tasks release before completion if canceled during drain).
        bucket = self._buckets[record.bucket]
        await bucket.acquire()
        try:
            record.started_at = time.monotonic()
            record.status = "running"
            self._log_event("task_started", record)

            attempt_budget = max(1, retries + 1)
            last_exc: BaseException | None = None
            for attempt in range(1, attempt_budget + 1):
                record.attempts = attempt
                try:
                    # Run in the captured context so the task sees the same
                    # AppContext / lane / etc. as the submit caller.
                    result = await sub.ctx_snapshot.run(_invoke_async, sub.fn)
                except asyncio.CancelledError:
                    record.status = "cancelled"
                    self._log_event("task_cancelled", record)
                    if not sub.future.done():
                        sub.future.cancel()
                    raise
                except Exception as exc:
                    last_exc = exc
                    if attempt < attempt_budget and self._is_transient(exc, record):
                        delay = self._backoff_delay(attempt - 1)
                        self._log_event(
                            "task_retry",
                            record,
                            extra={"attempt": attempt, "delay_s": delay,
                                   "error_class": type(exc).__name__},
                        )
                        await asyncio.sleep(delay)
                        continue
                    record.status = "failed"
                    record.error_class = type(exc).__name__
                    record.error_msg = str(exc) or repr(exc)
                    record.completed_at = time.monotonic()
                    self._log_event("task_failed", record)
                    if not sub.future.done():
                        sub.future.set_exception(exc)
                    return
                else:
                    record.status = "succeeded"
                    record.completed_at = time.monotonic()
                    self._log_event("task_succeeded", record)
                    if not sub.future.done():
                        sub.future.set_result(result)
                    return

            # Shouldn't reach here — loop returns on success or non-retry-able
            # failure. Defensive.
            if last_exc is not None and not sub.future.done():
                sub.future.set_exception(last_exc)
        finally:
            bucket.release()

    @staticmethod
    def _is_transient(exc: BaseException, record: TaskRecord) -> bool:
        """Should this exception be retried?

        Only when caller asserted ``retry_safe=True``. The asyncpg
        exceptions InterfaceError and ConnectionDoesNotExistError are
        at-least-once — retrying a non-idempotent INSERT would double-write.
        """
        if not record.retry_safe:
            return False
        # Cheap module/class check to avoid importing asyncpg here (matrx-connect
        # cannot depend on matrx-orm or asyncpg).
        cls = type(exc)
        qualified = f"{cls.__module__}.{cls.__name__}"
        if qualified.startswith("asyncpg.exceptions."):
            return cls.__name__ in {
                "InterfaceError",
                "ConnectionDoesNotExistError",
                "PoolAcquireTimeoutError",
            }
        if isinstance(exc, OSError):
            return True
        return False

    def _backoff_delay(self, attempt_idx: int) -> float:
        seq = self.config.transient_retry_backoff
        if not seq:
            return 0.0
        if attempt_idx >= len(seq):
            return seq[-1]
        return seq[attempt_idx]

    # ---------------------- finalizers -----------------------------------
    def add_finalizer(self, fn: Finalizer, *, name: str = "anonymous") -> None:
        """Register a coroutine factory to run at the very start of begin_drain.

        Finalizers are the platform-level "guaranteed end-of-request" hook —
        used for writes / metric flushes / cleanups that must run regardless
        of whether the main task succeeded, raised, or was canceled.

        Each finalizer:
          - Is called with a :class:`FinalizerContext` carrying ``failed`` and
            ``soft`` flags so it can pick the right exit semantics.
          - Is awaited inside ``asyncio.shield`` so an outer cancellation of
            the drain task does not interrupt the finalizer's own coroutine.
          - Has its own try/except guard — exceptions are logged but never
            propagate, so one broken finalizer cannot block another.

        Order of execution is insertion order. Register from any code that
        wants its cleanup to happen before priority drains.
        """
        if self.phase == "closed":
            raise LaneClosedError(
                f"RequestLane {self.id} is closed — cannot register finalizer"
            )
        self._finalizers.append((name, fn))

    async def _run_finalizers(self, ctx: FinalizerContext) -> None:
        for name, fn in self._finalizers:
            try:
                await asyncio.shield(fn(ctx))
            except asyncio.CancelledError:
                # Shield should prevent this, but if the inner coroutine
                # itself raises CancelledError, log and continue.
                self._log_event(
                    "finalizer_cancelled",
                    None,
                    extra={"finalizer_name": name, "outcome": ctx.outcome},
                )
            except Exception as exc:
                self._log_event(
                    "finalizer_failed",
                    None,
                    extra={
                        "finalizer_name": name,
                        "outcome": ctx.outcome,
                        "error_class": type(exc).__name__,
                        "error_msg": str(exc) or repr(exc),
                    },
                )

    # ---------------------- drain & cancellation --------------------------
    async def begin_drain(
        self,
        *,
        failed: bool = False,
        soft: bool = False,
    ) -> None:
        """Switch the lane to ``draining`` and wait for pending work.

        - ``failed=True``: the main task raised. We still drain DEFERRED so
          completed-but-not-yet-persisted side-effects (labelers, metrics)
          finish — failures shouldn't silently drop legitimately completed
          work just because the parent crashed.
        - ``soft=True``: client disconnected. Cancel BLOCKING/NORMAL in-flight
          but let DEFERRED finish.
        """
        if self.phase != "active":
            return
        self.phase = "draining"
        self._log_event("lane_drain_begin", None,
                        extra={"failed": failed, "soft": soft})

        # Run finalizers FIRST — guaranteed end-of-request work (persistence
        # flush, metric flush, …). Wrapped in asyncio.shield individually so
        # an outer cancellation can't interrupt them mid-write.
        if self._finalizers:
            await self._run_finalizers(FinalizerContext(failed=failed, soft=soft))

        cfg = self.config
        # Three drain phases. Higher priority gets less drain time because
        # it should already be done — the long tail is DEFERRED.
        # Phase 1: BLOCKING — let it finish.
        await self._await_priority(
            TaskPriority.BLOCKING,
            timeout=cfg.blocking_drain_timeout,
            cancel_on_timeout=True,
        )

        # Phase 2: NORMAL — let it finish; if soft-cancel, kill immediately.
        if soft:
            self._cancel_priority(TaskPriority.NORMAL)
        await self._await_priority(
            TaskPriority.NORMAL,
            timeout=cfg.normal_drain_timeout,
            cancel_on_timeout=True,
        )

        # Phase 3: DEFERRED — fire-and-forget tail. Full drain budget.
        await self._await_priority(
            TaskPriority.DEFERRED,
            timeout=cfg.deferred_drain_timeout,
            cancel_on_timeout=True,
        )

        self._close_phase()

    async def hard_cancel(self) -> None:
        """Cancel everything immediately. Used by /admin/lanes/{id}/kill or shutdown."""
        if self.phase == "closed":
            return
        self.phase = "draining"
        self._log_event("lane_hard_cancel", None)
        for task in list(self._tasks):
            if not task.done():
                task.cancel()
        # Wait briefly for cancellation propagation; don't hang forever.
        await self._await_priority(TaskPriority.BLOCKING, timeout=2.0, cancel_on_timeout=True)
        await self._await_priority(TaskPriority.NORMAL, timeout=2.0, cancel_on_timeout=True)
        await self._await_priority(TaskPriority.DEFERRED, timeout=2.0, cancel_on_timeout=True)
        self._close_phase()

    def _cancel_priority(self, prio: TaskPriority) -> None:
        for task in list(self._tasks):
            if task.done():
                continue
            record_id = self._task_to_record.get(task)
            if record_id is None:
                continue
            record = self._records.get(record_id)
            if record is not None and record.priority == prio:
                task.cancel()

    async def _await_priority(
        self, prio: TaskPriority, *, timeout: float, cancel_on_timeout: bool
    ) -> None:
        relevant: list[asyncio.Task[Any]] = []
        for t in list(self._tasks):
            if t.done():
                continue
            rid = self._task_to_record.get(t)
            if rid is None:
                continue
            rec = self._records.get(rid)
            if rec is not None and rec.priority == prio:
                relevant.append(t)
        if not relevant:
            return
        try:
            await asyncio.wait_for(
                asyncio.gather(*relevant, return_exceptions=True),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            self._log_event(
                "lane_drain_timeout",
                None,
                extra={"priority": prio.name, "stuck_count": len(relevant)},
            )
            if cancel_on_timeout:
                for t in relevant:
                    if not t.done():
                        t.cancel()

    def _close_phase(self) -> None:
        self.phase = "closed"
        self._log_event(
            "lane_closed",
            None,
            extra={
                "duration_s": time.monotonic() - self.opened_at,
                "succeeded": sum(1 for r in self._records.values() if r.status == "succeeded"),
                "failed": sum(1 for r in self._records.values() if r.status == "failed"),
                "cancelled": sum(1 for r in self._records.values() if r.status == "cancelled"),
            },
        )

    # ---------------------- observability ---------------------------------
    def status(self) -> dict[str, Any]:
        """Live snapshot for /admin/lanes."""
        by_phase = {"queued": 0, "running": 0, "succeeded": 0, "failed": 0, "cancelled": 0}
        for r in self._records.values():
            by_phase[r.status] = by_phase.get(r.status, 0) + 1
        return {
            "id": self.id,
            "scope_kind": self.scope_kind,
            "phase": self.phase,
            "age_seconds": time.monotonic() - self.opened_at,
            "context": self.context_snapshot,
            "tasks_by_status": by_phase,
            "buckets": [
                {
                    "name": b.stats().name,
                    "capacity": b.stats().capacity,
                    "in_flight": b.stats().in_flight,
                    "queued": b.stats().queued,
                }
                for b in self._buckets.values()
            ],
        }

    def task_list(self) -> list[dict[str, Any]]:
        return [
            {
                "id": r.id,
                "name": r.name,
                "priority": r.priority.name,
                "bucket": r.bucket,
                "status": r.status,
                "attempts": r.attempts,
                "submitted_at": r.submitted_at,
                "started_at": r.started_at,
                "completed_at": r.completed_at,
                "error_class": r.error_class,
                "error_msg": r.error_msg,
                "coalesce_key": r.coalesce_key,
                "extra": r.extra,
            }
            for r in self._records.values()
        ]

    def _log_event(
        self,
        event: str,
        record: TaskRecord | None,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "event": event,
            "lane_id": self.id,
            "scope_kind": self.scope_kind,
            "phase": self.phase,
        }
        if record is not None:
            payload.update(
                {
                    "task_id": record.id,
                    "task_name": record.name,
                    "priority": record.priority.name,
                    "bucket": record.bucket,
                    "status": record.status,
                    "attempts": record.attempts,
                    "coalesce_key": record.coalesce_key,
                    "error_class": record.error_class,
                    "error_msg": record.error_msg,
                }
            )
        if extra:
            payload.update(extra)
        logger.info("lane_event", extra={"matrx_lane": payload})

    def _trim_records(self) -> None:
        cap = self.config.max_task_records
        if len(self._records) <= cap:
            return
        # Drop oldest terminal records first; never drop queued/running.
        terminal = sorted(
            (r for r in self._records.values() if r.status in {"succeeded", "failed", "cancelled"}),
            key=lambda r: r.submitted_at,
        )
        to_drop = len(self._records) - cap
        for r in terminal[:to_drop]:
            self._records.pop(r.id, None)

    # ---------------------- open / close ----------------------------------
    def __enter__(self) -> "RequestLane":
        self._ctx_token = set_current_lane(self)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Sync exit can't drain (would need an event loop). Best-effort: mark
        # closed; tasks already running will continue but their submitter is gone.
        if self.phase == "active":
            self.phase = "draining"
        if self._ctx_token is not None:
            reset_current_lane(self._ctx_token)
            self._ctx_token = None

    async def __aenter__(self) -> "RequestLane":
        self._ctx_token = set_current_lane(self)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            await self.begin_drain(failed=exc is not None)
        finally:
            if self._ctx_token is not None:
                reset_current_lane(self._ctx_token)
                self._ctx_token = None

    # ---------------------- classmethod factories -------------------------
    @classmethod
    def open(
        cls,
        *,
        lane_id: str | None = None,
        scope_kind: str = "request",
        context_snapshot: Mapping[str, Any] | None = None,
        config: LaneConfig | None = None,
        bucket_caps: Mapping[str, int] | None = None,
    ) -> "RequestLane":
        """Open a new lane and install it as the current ContextVar.

        Use as a context manager:

            async with RequestLane.open(lane_id=request_id, ...) as lane:
                ...  # All async work inside inherits the lane
        """
        return cls(
            lane_id=lane_id,
            scope_kind=scope_kind,
            context_snapshot=context_snapshot,
            config=config,
            bucket_caps=bucket_caps,
        )


async def _invoke_async(fn: Callable[[], Awaitable[Any]]) -> Any:
    """Helper for ctx_snapshot.run — must be a function the snapshot can call."""
    return await fn()
