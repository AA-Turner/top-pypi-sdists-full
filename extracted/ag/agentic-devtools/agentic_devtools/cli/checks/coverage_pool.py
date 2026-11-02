"""Bounded concurrent execution for per-file coverage checks."""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Mapping
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

CoverageCheck = Callable[[str], tuple[bool, str]]
CoverageResult = tuple[str, bool, str, float]
_COVERAGE_WORKERS_ENV = "AGDT_CHECKS_COVERAGE_WORKERS"
_DEFAULT_MAX_WORKERS = 4


def get_coverage_worker_count(
    source_count: int,
    *,
    env: Mapping[str, str] | None = None,
    cpu_count: int | None = None,
) -> int:
    """Return a positive worker budget capped by the number of source files."""
    if source_count < 0:
        raise ValueError("source_count must be non-negative")
    environment = os.environ if env is None else env
    raw_workers = environment.get(_COVERAGE_WORKERS_ENV)
    configured_workers: int | None = None
    if raw_workers is not None:
        try:
            configured_workers = int(raw_workers)
        except ValueError as exc:
            raise ValueError(f"{_COVERAGE_WORKERS_ENV} must be a positive integer") from exc
        if configured_workers <= 0:
            raise ValueError(f"{_COVERAGE_WORKERS_ENV} must be a positive integer")
    if source_count == 0:
        return 0

    available_cpus = cpu_count if cpu_count is not None else os.cpu_count()
    cpu_budget = max(available_cpus or 1, 1)
    if configured_workers is None:
        configured_workers = min(cpu_budget, _DEFAULT_MAX_WORKERS)
    else:
        configured_workers = min(configured_workers, cpu_budget)

    return min(configured_workers, source_count)


def run_coverage_pool(
    source_files: list[str],
    check: CoverageCheck,
    *,
    max_workers: int,
    on_start: Callable[[str], None] | None = None,
    on_complete: Callable[[CoverageResult], None] | None = None,
) -> list[CoverageResult]:
    """Run coverage jobs concurrently and return results in submission order."""
    if not source_files:
        return []
    if max_workers <= 0:
        raise ValueError("max_workers must be a positive integer")

    with ThreadPoolExecutor(max_workers=min(max_workers, len(source_files))) as pool:
        future_indexes: dict[Future[tuple[bool, str, float]], int] = {}
        for index, source_file in enumerate(source_files):
            future = pool.submit(_run_coverage_check, check, source_file, on_start)
            future_indexes[future] = index

        results: dict[int, CoverageResult] = {}
        for future in as_completed(future_indexes):
            index = future_indexes[future]
            source_file = source_files[index]
            try:
                passed, output, duration = future.result()
            except Exception as exc:  # noqa: BLE001
                result = (source_file, False, f"Unexpected exception: {exc!r}", 0.0)
            else:
                result = (source_file, passed, output, duration)
            results[index] = result
            if on_complete is not None:
                on_complete(result)
    return [results[index] for index in range(len(source_files))]


def _run_coverage_check(
    check: CoverageCheck,
    source_file: str,
    on_start: Callable[[str], None] | None,
) -> tuple[bool, str, float]:
    """Run one callback and retain its duration for the gate's result summary."""
    if on_start is not None:
        on_start(source_file)
    started = time.monotonic()
    passed, output = check(source_file)
    return passed, output, time.monotonic() - started
