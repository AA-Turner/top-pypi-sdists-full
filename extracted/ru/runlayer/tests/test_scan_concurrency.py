"""Tests for scan-wide concurrency bounds."""

import contextvars
import threading
from types import SimpleNamespace
from unittest import mock

import pytest

from runlayer_cli.scan.concurrency import (
    MAX_SCAN_WORKERS,
    bounded_thread_pool,
    scan_worker_count,
)


@pytest.mark.parametrize(
    ("cpu_cores", "expected"),
    [
        (1, 1),
        (2, 2),
        (MAX_SCAN_WORKERS, MAX_SCAN_WORKERS),
        (MAX_SCAN_WORKERS + 8, MAX_SCAN_WORKERS),
    ],
)
def test_worker_count_respects_cpu_core_cap(cpu_cores, expected):
    governor = SimpleNamespace(cpu_cores=cpu_cores)

    assert scan_worker_count(governor) == expected


def test_bounded_pool_clamps_workers_to_task_count():
    with mock.patch(
        "runlayer_cli.scan.concurrency.ThreadPoolExecutor"
    ) as executor_type:
        with bounded_thread_pool(max_workers=8, task_count=3):
            pass

    executor_type.assert_called_once_with(
        max_workers=3,
        thread_name_prefix="",
    )
    executor_type.return_value.shutdown.assert_called_once_with(wait=True)


def test_gather_preserves_submission_order():
    second_finished = threading.Event()

    def first():
        assert second_finished.wait(timeout=1)
        return "first"

    def second():
        second_finished.set()
        return "second"

    with bounded_thread_pool(max_workers=2, task_count=2) as pool:
        futures = [pool.submit(first), pool.submit(second)]
        results = pool.gather(futures)

    assert results == ["first", "second"]


_test_context_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "test_scan_concurrency_var", default=None
)


def test_submit_propagates_submitter_context_to_worker():
    """OTel span context / structlog contextvars must reach worker threads."""
    token = _test_context_var.set("parent-scan-span")
    try:
        with bounded_thread_pool(max_workers=2) as pool:
            future = pool.submit(_test_context_var.get)
        assert future.result() == "parent-scan-span"
    finally:
        _test_context_var.reset(token)


def test_submit_captures_context_at_submit_time():
    """Each submit snapshots the caller's context; later mutations don't leak."""
    token = _test_context_var.set("first")
    try:
        with bounded_thread_pool(max_workers=1) as pool:
            first = pool.submit(_test_context_var.get)
            _test_context_var.set("second")
            second = pool.submit(_test_context_var.get)
        assert first.result() == "first"
        assert second.result() == "second"
    finally:
        _test_context_var.reset(token)


def test_submit_propagates_otel_span_context_to_worker():
    """A span started in a worker must nest under the submitter's active span."""
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider

    tracer = TracerProvider().get_tracer("test")

    def child_span_context() -> trace.SpanContext:
        with tracer.start_as_current_span("scan.phase") as span:
            return span.get_span_context()

    with tracer.start_as_current_span("cli.scan") as parent:
        with bounded_thread_pool(max_workers=1) as pool:
            child_context = pool.submit(child_span_context).result()

    assert child_context.trace_id == parent.get_span_context().trace_id


def test_worker_context_mutations_do_not_leak_to_submitter():
    def mutate() -> None:
        _test_context_var.set("worker-only")

    with bounded_thread_pool(max_workers=1) as pool:
        pool.submit(mutate).result()

    assert _test_context_var.get() is None


class _ScanAbort(BaseException):
    pass


def test_gather_surfaces_failure_before_earlier_running_result_finishes():
    running_started = threading.Event()
    running_finished = threading.Event()
    release_running = threading.Event()

    def running():
        running_started.set()
        assert release_running.wait(timeout=2)
        running_finished.set()

    def fail():
        assert running_started.wait(timeout=1)
        raise _ScanAbort

    release_timer = threading.Timer(1.0, release_running.set)
    try:
        with bounded_thread_pool(max_workers=2) as pool:
            futures = [pool.submit(running), pool.submit(fail)]
            release_timer.start()
            with pytest.raises(_ScanAbort):
                pool.gather(futures)
            assert not running_finished.is_set()
            release_running.set()
    finally:
        release_timer.cancel()
        release_running.set()


def test_failure_cancels_pending_and_waits_for_running_work():
    running_started = threading.Event()
    allow_failure = threading.Event()
    release_running = threading.Event()
    running_finished = threading.Event()

    def running():
        running_started.set()
        assert release_running.wait(timeout=1)
        running_finished.set()

    def fail():
        assert allow_failure.wait(timeout=1)
        raise _ScanAbort

    def pending():
        assert release_running.wait(timeout=1)

    release_timer = threading.Timer(0.2, release_running.set)
    pending_futures = []
    try:
        with pytest.raises(_ScanAbort):
            with bounded_thread_pool(max_workers=2) as pool:
                pool.submit(running)
                failed_future = pool.submit(fail)
                pending_futures = [pool.submit(pending) for _ in range(5)]
                assert running_started.wait(timeout=1)
                release_timer.start()
                allow_failure.set()
                failed_future.result()
    finally:
        release_timer.cancel()

    assert running_finished.is_set()
    assert any(future.cancelled() for future in pending_futures)
