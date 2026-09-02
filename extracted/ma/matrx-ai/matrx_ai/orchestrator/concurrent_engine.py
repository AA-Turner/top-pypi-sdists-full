from __future__ import annotations

import asyncio
import random
import time
import traceback
from collections import deque
from collections.abc import Awaitable, Callable
from enum import StrEnum
from typing import Any, TypeVar

from matrx_utils import vcprint
from pydantic import BaseModel, Field, model_validator

from matrx_ai.providers.errors import RetryableError, _extract_status_code, classify_provider_error

T = TypeVar("T")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Warmup strategy
# ---------------------------------------------------------------------------


class WarmupStrategy(StrEnum):
    NONE = "none"
    STAGED = "staged"


# ---------------------------------------------------------------------------
# Public configuration
# ---------------------------------------------------------------------------


class EngineConfig(BaseModel):
    initial_concurrency: int = 10
    max_concurrency: int | None = None
    min_concurrency: int = 1
    max_retries: int = 3
    base_backoff: float = 2.0
    max_backoff: float = 60.0
    jitter: float = 1.0
    rate_limit_cooldown: float = 30.0
    window_size: int = 20
    error_rate_threshold: float = 0.3
    recovery_streak: int = 10
    warmup: WarmupStrategy = WarmupStrategy.NONE
    retry_sweep: bool = True
    retry_sweep_concurrency: int = 2
    retry_sweep_delay: float = 3.0

    @model_validator(mode="after")
    def _set_defaults(self) -> EngineConfig:
        if self.max_concurrency is None:
            self.max_concurrency = max(self.initial_concurrency * 2, 20)
        if self.min_concurrency < 1:
            self.min_concurrency = 1
        if self.max_concurrency < self.initial_concurrency:
            self.max_concurrency = self.initial_concurrency
        return self


# ---------------------------------------------------------------------------
# Public result types
# ---------------------------------------------------------------------------


class ItemOutcome[T, R](BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    item: Any
    result: Any | None = None
    error: str | None = None
    attempts: int = 1
    elapsed: float = 0.0

    @property
    def success(self) -> bool:
        return self.error is None


class BatchResult[T, R](BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    succeeded: list[ItemOutcome[T, R]] = Field(default_factory=list)
    failed: list[ItemOutcome[T, R]] = Field(default_factory=list)
    total: int = 0
    elapsed_seconds: float = 0.0
    total_retries: int = 0
    rate_limit_events: int = 0
    concurrency_changes: list[tuple[float, int]] = Field(default_factory=list)
    was_cancelled: bool = False
    retry_sweep_recovered: int = 0

    @property
    def succeeded_count(self) -> int:
        return len(self.succeeded)

    @property
    def failed_count(self) -> int:
        return len(self.failed)

    def failure_summary(self) -> list[dict[str, Any]]:
        return [
            {
                "item": o.item,
                "error": o.error,
                "attempts": o.attempts,
                "elapsed": o.elapsed,
            }
            for o in self.failed
        ]

    def print_report(self, *, label: str = "Batch Engine Report") -> None:
        lines = [
            f"\n{'=' * 64}",
            f"  {label}",
            f"{'=' * 64}",
            f"  Total items:        {self.total}",
            f"  Succeeded:          {self.succeeded_count}",
            f"  Failed:             {self.failed_count}",
            f"  Total retries:      {self.total_retries}",
            f"  Rate limit events:  {self.rate_limit_events}",
            f"  Elapsed:            {self.elapsed_seconds:.1f}s",
            f"  Cancelled:          {self.was_cancelled}",
        ]
        if self.retry_sweep_recovered:
            lines.append(f"  Recovered by sweep: {self.retry_sweep_recovered}")
        if self.concurrency_changes:
            lines.append(f"  Concurrency changes: {self.concurrency_changes}")

        if self.failed:
            lines.append(f"\n  {'─' * 60}")
            lines.append(f"  Failed items ({self.failed_count}):")
            lines.append(f"  {'─' * 60}")
            for i, o in enumerate(self.failed, 1):
                lines.append(f"  [{i}] item={o.item}")
                lines.append(f"      error:    {o.error}")
                lines.append(f"      attempts: {o.attempts}  elapsed: {o.elapsed:.1f}s")

        lines.append(f"{'=' * 64}\n")
        vcprint("\n".join(lines), color="yellow" if self.failed else "green")


# ---------------------------------------------------------------------------
# Progress callback protocol
# ---------------------------------------------------------------------------

OnProgress = Callable[[int, int, "ItemOutcome[Any, Any]"], Awaitable[None]]


# ---------------------------------------------------------------------------
# AIMD adaptive concurrency controller
# ---------------------------------------------------------------------------


class _AIMDController:
    def __init__(self, config: EngineConfig, start_time: float) -> None:
        self._config = config
        self._start_time = start_time
        self.current: int = config.initial_concurrency
        self._window: deque[bool] = deque(maxlen=config.window_size)
        self._consecutive_successes: int = 0
        self.rate_limit_events: int = 0
        self.changes: list[tuple[float, int]] = []

    def _record_change(self, new_level: int) -> None:
        if new_level != self.current:
            self.current = new_level
            offset = time.monotonic() - self._start_time
            self.changes.append((round(offset, 2), new_level))
            vcprint(
                f"[ConcurrentEngine] Concurrency adjusted to {new_level}",
                color="yellow",
            )

    def on_success(self) -> None:
        self._window.append(True)
        self._consecutive_successes += 1
        cfg = self._config
        if self._consecutive_successes >= cfg.recovery_streak:
            new = min(cfg.max_concurrency, self.current + 1)  # type: ignore[operator]
            self._consecutive_successes = 0
            self._record_change(new)

    def on_retryable_failure(self) -> None:
        self._window.append(False)
        self._consecutive_successes = 0
        cfg = self._config
        if len(self._window) >= cfg.window_size // 2:
            failure_rate = self._window.count(False) / len(self._window)
            if failure_rate > cfg.error_rate_threshold:
                new = max(cfg.min_concurrency, int(self.current * 0.7))
                self._record_change(new)

    def on_rate_limit(self) -> None:
        self.rate_limit_events += 1
        self._window.append(False)
        self._consecutive_successes = 0
        cfg = self._config
        new = max(cfg.min_concurrency, self.current // 2)
        self._record_change(new)


# ---------------------------------------------------------------------------
# Internal pending item wrapper
# ---------------------------------------------------------------------------


class _PendingItem[T]:
    __slots__ = ("item", "attempt")

    def __init__(self, item: T, attempt: int = 0) -> None:
        self.item = item
        self.attempt = attempt


# ---------------------------------------------------------------------------
# Application-level failure exception
# ---------------------------------------------------------------------------


class WorkerResultError(Exception):
    """Raised internally when a worker returns without throwing but the
    ``is_result_success`` check indicates a logical failure.  Carries the
    original result so downstream handlers can inspect it."""

    def __init__(self, message: str, *, result: Any = None) -> None:
        super().__init__(message)
        self.result = result


# ---------------------------------------------------------------------------
# Default error classification helpers
# ---------------------------------------------------------------------------


def _default_is_retryable(exc: Exception) -> bool:
    if isinstance(exc, WorkerResultError):
        error_str = str(exc).lower()
        retryable_keywords = ("database", "db ", "connection", "timeout", "timed out", "pool", "network")
        non_retryable_keywords = ("parse", "invalid", "not found", "validation")
        if any(kw in error_str for kw in non_retryable_keywords):
            return False
        if any(kw in error_str for kw in retryable_keywords):
            return True
        return True

    attached: RetryableError | None = getattr(exc, "error_info", None)
    if attached is not None:
        return attached.is_retryable

    status_code = _extract_status_code(exc)
    if status_code is not None:
        info = classify_provider_error("unknown", exc)
        return info.is_retryable

    error_str = str(exc).lower()
    if any(kw in error_str for kw in ("429", "rate limit", "quota", "timeout", "timed out", "connection")):
        return True
    if any(kw in error_str for kw in ("401", "403", "invalid api key", "400", "invalid request")):
        return False

    return True


def _is_rate_limit(exc: Exception) -> bool:
    attached: RetryableError | None = getattr(exc, "error_info", None)
    if attached is not None:
        return attached.error_type == "rate_limit"
    status_code = _extract_status_code(exc)
    if status_code == 429:
        return True
    error_str = str(exc).lower()
    return any(kw in error_str for kw in ("429", "rate limit", "quota"))


# ---------------------------------------------------------------------------
# Worker result (internal, carries the exception object for classification)
# ---------------------------------------------------------------------------


class _WorkerResult[T, R]:
    __slots__ = ("item", "result", "exception", "elapsed", "attempt")

    def __init__(
        self,
        item: T,
        *,
        result: R | None = None,
        exception: Exception | None = None,
        elapsed: float = 0.0,
        attempt: int = 0,
    ) -> None:
        self.item = item
        self.result = result
        self.exception = exception
        self.elapsed = elapsed
        self.attempt = attempt

    @property
    def success(self) -> bool:
        return self.exception is None

    def to_outcome(self) -> ItemOutcome[T, R]:
        return ItemOutcome(
            item=self.item,
            result=self.result,
            error=str(self.exception) if self.exception else None,
            attempts=self.attempt + 1,
            elapsed=round(self.elapsed, 2),
        )


# ---------------------------------------------------------------------------
# ConcurrentEngine
# ---------------------------------------------------------------------------


class ConcurrentEngine:
    def __init__(
        self,
        config: EngineConfig | None = None,
        on_progress: OnProgress | None = None,
        is_retryable: Callable[[Exception], bool] | None = None,
        is_result_success: Callable[[Any], bool] | None = None,
    ) -> None:
        self.config = config or EngineConfig()
        self._on_progress = on_progress
        self._is_retryable = is_retryable or _default_is_retryable
        self._is_result_success = is_result_success

    async def run(
        self,
        items: list[T],
        worker: Callable[[T], Awaitable[R]],
        cancel_event: asyncio.Event | None = None,
    ) -> BatchResult[T, R]:
        if not items:
            return BatchResult(total=0)

        start_time = time.monotonic()
        total = len(items)
        controller = _AIMDController(self.config, start_time)

        succeeded: list[ItemOutcome[T, R]] = []
        failed: list[ItemOutcome[T, R]] = []
        total_retries = 0
        completed_count = 0
        was_cancelled = False

        def _build_result() -> BatchResult[T, R]:
            return BatchResult(
                succeeded=succeeded,
                failed=failed,
                total=total,
                elapsed_seconds=round(time.monotonic() - start_time, 2),
                total_retries=total_retries,
                rate_limit_events=controller.rate_limit_events,
                concurrency_changes=controller.changes,
                was_cancelled=was_cancelled,
            )

        async def _notify_progress(outcome: ItemOutcome[T, R]) -> None:
            if self._on_progress:
                try:
                    await self._on_progress(completed_count, total, outcome)
                except Exception:
                    pass

        try:
            # --- Staged warmup ---
            # Stage 1: one item sequentially — validates the worker itself.
            # Stage 2: small concurrent burst — validates the concurrency plumbing.
            # If both pass, proceed to full-force concurrent execution.
            # Any failure in either stage aborts the batch immediately.
            cursor = 0
            if self.config.warmup == WarmupStrategy.STAGED and total >= 1:
                # Stage 1: single sequential call
                if cancel_event and cancel_event.is_set():
                    was_cancelled = True
                    return _build_result()

                vcprint(
                    "[ConcurrentEngine] Warmup stage 1: single sequential call",
                    color="blue",
                )
                wr = await self._call_worker(items[0], worker, attempt=0)
                outcome = wr.to_outcome()
                completed_count += 1
                cursor = 1

                if wr.success:
                    succeeded.append(outcome)
                    controller.on_success()
                    await _notify_progress(outcome)
                else:
                    failed.append(outcome)
                    vcprint(
                        f"[ConcurrentEngine] Warmup stage 1 failed. "
                        f"Worker is not functional. Aborting. Error: {outcome.error}",
                        color="red",
                    )
                    await _notify_progress(outcome)
                    return _build_result()

                # Stage 2: small concurrent burst (2 items, or whatever remains)
                stage2_count = min(2, total - cursor)
                if stage2_count > 0:
                    if cancel_event and cancel_event.is_set():
                        was_cancelled = True
                        return _build_result()

                    vcprint(
                        f"[ConcurrentEngine] Warmup stage 2: {stage2_count} concurrent calls",
                        color="blue",
                    )
                    stage2_items = items[cursor : cursor + stage2_count]
                    stage2_tasks = [
                        asyncio.create_task(self._call_worker(item, worker, attempt=0))
                        for item in stage2_items
                    ]
                    stage2_results: list[_WorkerResult[T, R]] = await asyncio.gather(*stage2_tasks)

                    stage2_failures = 0
                    for wr in stage2_results:
                        outcome = wr.to_outcome()
                        completed_count += 1
                        cursor += 1
                        if wr.success:
                            succeeded.append(outcome)
                            controller.on_success()
                        else:
                            failed.append(outcome)
                            controller.on_retryable_failure()
                            stage2_failures += 1
                        await _notify_progress(outcome)

                    if stage2_failures > 0:
                        vcprint(
                            f"[ConcurrentEngine] Warmup stage 2 had {stage2_failures} failure(s). "
                            f"Concurrency is unreliable. Aborting.",
                            color="red",
                        )
                        return _build_result()

                vcprint(
                    "[ConcurrentEngine] Warmup passed. Proceeding to full concurrent execution.",
                    color="green",
                )

            # --- Full concurrent phase ---
            remaining_items = items[cursor:]
            if not remaining_items:
                return _build_result()

            vcprint(
                f"[ConcurrentEngine] Dispatching all {len(remaining_items)} items; "
                "central provider admission owns pacing",
                color="blue",
            )

            queue: asyncio.Queue[_PendingItem[T]] = asyncio.Queue()
            for item in remaining_items:
                queue.put_nowait(_PendingItem(item))

            async def _worker_loop() -> None:
                nonlocal completed_count, total_retries, was_cancelled

                while True:
                    if cancel_event and cancel_event.is_set():
                        was_cancelled = True
                        return

                    try:
                        pending = queue.get_nowait()
                    except asyncio.QueueEmpty:
                        return

                    wr = await self._call_worker(
                        pending.item, worker, attempt=pending.attempt
                    )

                    if wr.success:
                        outcome = wr.to_outcome()
                        succeeded.append(outcome)
                        completed_count += 1
                        await _notify_progress(outcome)
                    else:
                        exc = wr.exception
                        retryable = exc is not None and self._is_retryable(exc)
                        rate_limited = exc is not None and _is_rate_limit(exc)
                        can_retry = retryable and pending.attempt < self.config.max_retries

                        if rate_limited:
                            controller.rate_limit_events += 1
                            vcprint(
                                "[ConcurrentEngine] Rate limit surfaced after central provider "
                                "admission; retrying under that same admission gate.",
                                color="red",
                            )

                        if can_retry:
                            total_retries += 1
                            delay = min(
                                self.config.base_backoff * (2 ** pending.attempt)
                                + random.uniform(0, self.config.jitter),
                                self.config.max_backoff,
                            )
                            vcprint(
                                f"[ConcurrentEngine] Retrying item (attempt {pending.attempt + 1}/{self.config.max_retries}) "
                                f"after {delay:.1f}s — {wr.exception}",
                                color="yellow",
                            )
                            await asyncio.sleep(delay)
                            queue.put_nowait(_PendingItem(pending.item, pending.attempt + 1))
                        else:
                            outcome = wr.to_outcome()
                            failed.append(outcome)
                            completed_count += 1
                            await _notify_progress(outcome)

            num_workers = len(remaining_items)
            tasks: list[asyncio.Task[None]] = []
            for _ in range(num_workers):
                tasks.append(asyncio.create_task(_worker_loop()))

            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as exc:
            vcprint(
                f"[ConcurrentEngine] Unexpected engine error: {exc}\n{traceback.format_exc()}",
                color="red",
            )

        # --- Retry sweep for recoverable failures ---
        if (
            self.config.retry_sweep
            and failed
            and not was_cancelled
            and not (cancel_event and cancel_event.is_set())
        ):
            sweep_candidates = []
            permanent_failures: list[ItemOutcome[T, R]] = []
            for outcome in failed:
                err_str = (outcome.error or "").lower()
                is_deterministic = any(
                    kw in err_str for kw in ("parse", "invalid", "not found", "validation")
                )
                if is_deterministic:
                    permanent_failures.append(outcome)
                else:
                    sweep_candidates.append(outcome)

            if sweep_candidates:
                vcprint(
                    f"\n[ConcurrentEngine] Retry sweep: {len(sweep_candidates)} recoverable "
                    "failure(s), dispatching all under central provider admission",
                    color="blue",
                )
                await asyncio.sleep(self.config.retry_sweep_delay)

                recovered: list[ItemOutcome[T, R]] = []
                still_failed: list[ItemOutcome[T, R]] = []

                async def _sweep_one(candidate: ItemOutcome[T, R]) -> None:
                    wr = await self._call_worker(
                        candidate.item, worker, attempt=candidate.attempts
                    )
                    sweep_outcome = wr.to_outcome()
                    if wr.success:
                        recovered.append(sweep_outcome)
                        vcprint(
                            f"[ConcurrentEngine] Sweep recovered item={candidate.item}",
                            color="green",
                        )
                    else:
                        still_failed.append(sweep_outcome)
                        vcprint(
                            f"[ConcurrentEngine] Sweep retry failed for item={candidate.item}: "
                            f"{sweep_outcome.error}",
                            color="red",
                        )

                sweep_tasks = [
                    asyncio.create_task(_sweep_one(c)) for c in sweep_candidates
                ]
                await asyncio.gather(*sweep_tasks, return_exceptions=True)

                succeeded.extend(recovered)
                failed.clear()
                failed.extend(permanent_failures)
                failed.extend(still_failed)

                sweep_recovered_count = len(recovered)
                vcprint(
                    f"[ConcurrentEngine] Sweep complete: {sweep_recovered_count} recovered, "
                    f"{len(still_failed)} still failed, "
                    f"{len(permanent_failures)} permanent failure(s)",
                    color="green" if not still_failed else "yellow",
                )

                return BatchResult(
                    succeeded=succeeded,
                    failed=failed,
                    total=total,
                    elapsed_seconds=round(time.monotonic() - start_time, 2),
                    total_retries=total_retries,
                    rate_limit_events=controller.rate_limit_events,
                    concurrency_changes=controller.changes,
                    was_cancelled=was_cancelled,
                    retry_sweep_recovered=sweep_recovered_count,
                )

        return _build_result()

    async def _call_worker(
        self,
        item: T,
        worker: Callable[[T], Awaitable[R]],
        *,
        attempt: int,
    ) -> _WorkerResult[T, R]:
        t0 = time.monotonic()
        try:
            result = await worker(item)
            elapsed = time.monotonic() - t0

            if self._is_result_success is not None and not self._is_result_success(result):
                error_detail = getattr(result, "error", None) or "Worker returned a failed result"
                exc = WorkerResultError(str(error_detail), result=result)
                return _WorkerResult(item, result=result, exception=exc, elapsed=elapsed, attempt=attempt)

            return _WorkerResult(item, result=result, elapsed=elapsed, attempt=attempt)
        except Exception as exc:
            elapsed = time.monotonic() - t0
            return _WorkerResult(item, exception=exc, elapsed=elapsed, attempt=attempt)
