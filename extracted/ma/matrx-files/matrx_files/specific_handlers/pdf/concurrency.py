"""Executor pools for CPU-bound and OCR PDF work.

PyMuPDF is sync C code and the upstream FAQ explicitly states multi-threaded
use is unsupported (GIL release is "intolerable overhead"). Our discipline:

- Every public ``_async`` method opens its own ``Document`` from bytes inside
  the executor thread. Never share a Document across coroutines or threads.
- General CPU work goes through ``get_cpu_executor`` / ``run_in_cpu_executor``.
- OCR work goes through ``get_ocr_executor`` / ``run_in_ocr_executor`` so
  Tesseract concurrency can be sized independently (it is CPU-saturating
  per-process).

Both pools are lazily initialized on first use and shut down via
``shutdown_executors`` (registered with atexit). Sizing comes from the HOST
through ``configure_worker_counts`` — in aidream the ``media.pdf`` settings
``cpu_workers`` and ``ocr_workers`` (``platform.feature_knob`` rows). This
package never reads the environment for it: ``MATRX_PDF_CPU_WORKERS`` /
``MATRX_PDF_OCR_WORKERS`` were retired 2026-09-11 (USD-5, "Never an env
var"). A standalone install that configures nothing gets one CPU worker per
core and at most four OCR workers.
"""

from __future__ import annotations

import asyncio
import atexit
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, TypeVar

T = TypeVar("T")

# OCR pool size is capped here. PyMuPDF's Tesseract bindings release the GIL,
# so a thread pool is sufficient; we keep the cap conservative because each
# worker can independently saturate a CPU core via Tesseract. The host's
# ``ocr_workers`` setting replaces the cap.
_DEFAULT_OCR_MAX = 4

_cpu_executor: ThreadPoolExecutor | None = None
_ocr_executor: ThreadPoolExecutor | None = None
_init_lock = threading.Lock()

# Host-supplied sizing. Each is a zero-arg callable returning an int; 0 (or a
# value the host cannot read yet) means "the package posture": one CPU worker
# per core, OCR capped at _DEFAULT_OCR_MAX. A callable that raises is
# announced once on stderr — the pool is created either way, because PDF work
# must not fail over a settings read.
_count_sources: dict[str, Callable[[], int]] = {}
_count_announced: set[str] = set()


def configure_worker_counts(
    *,
    cpu: Callable[[], int] | None = None,
    ocr: Callable[[], int] | None = None,
) -> None:
    """Bind pool sizing to the host's settings. Read at pool creation (first
    use); a later change applies to the next process, since a live
    ThreadPoolExecutor is never resized."""
    if cpu is not None:
        _count_sources["cpu"] = cpu
        _count_announced.discard("cpu")
    if ocr is not None:
        _count_sources["ocr"] = ocr
        _count_announced.discard("ocr")


def _host_count(name: str) -> int:
    fn = _count_sources.get(name)
    if fn is None:
        return 0
    try:
        return max(0, int(fn()))
    except Exception as exc:  # noqa: BLE001 — announced, then the package posture
        if name not in _count_announced:
            _count_announced.add(name)
            import sys

            print(
                f"[matrx-files pdf] worker count {name!r} could not be read "
                f"({exc!r}); using the package posture for this process. Fix: "
                f"load the host's settings before the first PDF operation.",
                file=sys.stderr,
            )
        return 0


def _cpu_worker_count() -> int:
    configured = _host_count("cpu")
    if configured > 0:
        return configured
    return max(1, os.cpu_count() or 2)


def _ocr_worker_count() -> int:
    # The host value is a CAP, like the package default: never more OCR
    # workers than cores, since each one saturates a core via Tesseract.
    cap = _host_count("ocr") or _DEFAULT_OCR_MAX
    return max(1, min(cap, os.cpu_count() or 2))


def get_cpu_executor() -> ThreadPoolExecutor:
    global _cpu_executor
    if _cpu_executor is None:
        with _init_lock:
            if _cpu_executor is None:
                _cpu_executor = ThreadPoolExecutor(
                    max_workers=_cpu_worker_count(),
                    thread_name_prefix="matrx-pdf-cpu",
                )
    return _cpu_executor


def get_ocr_executor() -> ThreadPoolExecutor:
    global _ocr_executor
    if _ocr_executor is None:
        with _init_lock:
            if _ocr_executor is None:
                _ocr_executor = ThreadPoolExecutor(
                    max_workers=_ocr_worker_count(),
                    thread_name_prefix="matrx-pdf-ocr",
                )
    return _ocr_executor


async def run_in_cpu_executor(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = asyncio.get_running_loop()
    if kwargs:
        return await loop.run_in_executor(
            get_cpu_executor(), lambda: fn(*args, **kwargs)
        )
    return await loop.run_in_executor(get_cpu_executor(), fn, *args)


async def run_in_ocr_executor(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = asyncio.get_running_loop()
    if kwargs:
        return await loop.run_in_executor(
            get_ocr_executor(), lambda: fn(*args, **kwargs)
        )
    return await loop.run_in_executor(get_ocr_executor(), fn, *args)


def shutdown_executors() -> None:
    global _cpu_executor, _ocr_executor
    with _init_lock:
        if _cpu_executor is not None:
            _cpu_executor.shutdown(wait=False)
            _cpu_executor = None
        if _ocr_executor is not None:
            _ocr_executor.shutdown(wait=False)
            _ocr_executor = None


atexit.register(shutdown_executors)


__all__ = [
    "get_cpu_executor",
    "get_ocr_executor",
    "run_in_cpu_executor",
    "run_in_ocr_executor",
    "shutdown_executors",
]
