"""Shared concurrency bounds for the device scan."""

from __future__ import annotations

import contextvars
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import (
    FIRST_COMPLETED,
    FIRST_EXCEPTION,
    Future,
    ThreadPoolExecutor,
    wait,
)
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, TypeVar

from runlayer_cli.scan.resource_governor import default_cpu_cores

if TYPE_CHECKING:
    from runlayer_cli.scan.resource_governor import ResourceGovernor

MAX_SCAN_WORKERS = 4
_Result = TypeVar("_Result")


class ScanThreadPool:
    """Tracked thread pool with ordered fan-in."""

    def __init__(self, executor: ThreadPoolExecutor) -> None:
        self._executor = executor
        self._futures: list[Future[Any]] = []

    def submit(self, work: Callable[[], _Result]) -> Future[_Result]:
        """Submit zero-argument work and track it for failure cleanup.

        Runs *work* in a snapshot of the submitter's ``contextvars.Context`` —
        ``ThreadPoolExecutor`` does not do this itself — so OTel span context
        (e.g. the parent ``cli.scan`` span) and any structlog contextvars stay
        visible inside worker threads.
        """
        context = contextvars.copy_context()

        def run_in_context() -> _Result:
            return context.run(work)

        future = self._executor.submit(run_in_context)
        self._futures.append(future)
        return future

    def gather(self, futures: Sequence[Future[_Result]]) -> list[_Result]:
        """Fail on the first completed error; otherwise return ordered results."""
        done, _ = wait(futures, return_when=FIRST_EXCEPTION)
        self._raise_first_failure(futures, done)
        return [future.result() for future in futures]

    def result(self, target: Future[_Result]) -> _Result:
        """Await *target* while surfacing failures from already-submitted peers."""
        pending = set(self._futures)
        pending.add(target)
        while target in pending:
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            self._raise_first_failure(self._futures, done)
        return target.result()

    def wait_for_all(self) -> None:
        """Wait for tracked work, surfacing the first completed failure."""
        done, _ = wait(self._futures, return_when=FIRST_EXCEPTION)
        self._raise_first_failure(self._futures, done)

    @staticmethod
    def _raise_first_failure(
        futures: Sequence[Future[Any]],
        done: set[Future[Any]],
    ) -> None:
        for future in futures:
            if future in done and (
                future.cancelled() or future.exception() is not None
            ):
                future.result()

    def cancel_pending(self) -> None:
        """Cancel every tracked future that has not started."""
        for future in self._futures:
            future.cancel()


@contextmanager
def bounded_thread_pool(
    *,
    max_workers: int,
    task_count: int | None = None,
    thread_name_prefix: str = "",
) -> Iterator[ScanThreadPool]:
    """Own a bounded executor and cleanly stop siblings on any failure.

    Exceptions raised inside the context cancel pending futures, then wait for
    already-running work to stop before propagating.
    """
    worker_count = max(1, max_workers)
    if task_count is not None:
        worker_count = min(worker_count, max(1, task_count))

    executor = ThreadPoolExecutor(
        max_workers=worker_count,
        thread_name_prefix=thread_name_prefix,
    )
    pool = ScanThreadPool(executor)
    try:
        yield pool
    except BaseException:
        pool.cancel_pending()
        executor.shutdown(wait=True, cancel_futures=True)
        raise
    else:
        executor.shutdown(wait=True)


def scan_worker_count(governor: ResourceGovernor | None = None) -> int:
    """Return the per-pool concurrency ceiling from ``CpuCores``.

    This bounds each pool, not the process: the crawl's shard pool nests inside
    the orchestrator's phase pool (whose phase-2 worker blocks on the shard
    futures — sharing one bounded pool would deadlock), so peak thread count can
    reach twice this ceiling while the crawl runs. ``MaxCpuPercent`` separately
    defines a single-core-equivalent duty target: the governor throttles
    process-wide Python ``process_time`` and, on POSIX, splits that target across
    registered find/PowerShell process groups with SIGSTOP/SIGCONT. Windows
    cannot duty-cycle child groups, so its crawl children use below-normal
    priority as the best-effort fallback.
    """
    cpu_cores = governor.cpu_cores if governor is not None else default_cpu_cores()
    return max(1, min(MAX_SCAN_WORKERS, cpu_cores))
