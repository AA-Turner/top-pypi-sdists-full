# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later


import functools
import os
import threading

# Concurrent imports
from concurrent.futures import ProcessPoolExecutor

from tango._instrumentation import _get_non_tango_source_location
from tango._telemetry import _telemetry_runtime

# Tango imports
from tango.green import AbstractExecutor, get_ident, get_thread_pool_executor

__all__ = (
    "FuturesExecutor",
    "_switch_global_executor_to_thread",
    "get_global_executor",
    "set_global_executor",
)

# Global executor

_MAIN_EXECUTOR = None
_THREAD_EXECUTORS = {}

# Thread-local storage to track which FuturesExecutor owns the current thread's work.
# Set by FuturesExecutor.delegate() so that nested Tango calls from pool threads
# (which have a different ident than the asyncio loop thread) can find the right executor.
_delegate_thread_local = threading.local()


def _switch_global_executor_to_thread():
    """
    internal PyTango function, use only if you sure, what you are doing!
    Used for correct behavior of TestDeviceContext
    checks, that global executor belongs to the caller thread, and,
    if not - creates a new one and saves it as a new global
    """
    global _MAIN_EXECUTOR
    if _MAIN_EXECUTOR is not None and not _MAIN_EXECUTOR.in_executor_context():
        # we save current executor in the known subthread executors to be used later
        _THREAD_EXECUTORS[_MAIN_EXECUTOR.get_ident()] = _MAIN_EXECUTOR
        _MAIN_EXECUTOR = FuturesExecutor()


def get_global_executor():
    global _MAIN_EXECUTOR
    if _MAIN_EXECUTOR is None:
        _MAIN_EXECUTOR = FuturesExecutor()

    # the following patch is used for correct behavior of TestDeviceContext,
    # which has two different executors for main and device threads
    if not _MAIN_EXECUTOR.in_executor_context():
        ident = get_ident(), os.getpid()
        if ident in _THREAD_EXECUTORS:
            return _THREAD_EXECUTORS[ident]
        # If running in a pool thread spawned by an FuturesExecutor's delegate(),
        # recover the owning executor from the thread-local set by that delegate().
        thread_executor = getattr(_delegate_thread_local, "executor", None)
        if thread_executor is not None:
            return thread_executor

    return _MAIN_EXECUTOR


def set_global_executor(executor):
    global _MAIN_EXECUTOR
    _MAIN_EXECUTOR = executor


# Futures executor


class FuturesExecutor(AbstractExecutor):
    """Futures tango executor"""

    asynchronous = True
    default_wait = True

    def __init__(self, process=False, max_workers=20):
        super().__init__()
        if process:
            self.subexecutor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.subexecutor = get_thread_pool_executor(max_workers=max_workers)

    def delegate(self, fn, *args, **kwargs):
        """Return the given operation as a concurrent future."""
        if hasattr(fn, "__trace_kwargs__"):
            kwargs["trace_location"] = _get_non_tango_source_location()
            kwargs["trace_context"] = _telemetry_runtime.get_current_otel_context()

        callback = functools.partial(fn, *args, **kwargs)
        executor_ref = self

        def _callback_with_executor():
            _delegate_thread_local.executor = executor_ref
            return callback()

        return self.subexecutor.submit(_callback_with_executor)

    def access(self, accessor, timeout=None):
        """Return a result from a single callable."""
        return accessor.result(timeout=timeout)

    def submit(self, fn, *args, **kwargs):
        """Submit an operation"""
        return fn(*args, **kwargs)

    def execute(self, fn, *args, **kwargs):
        """Execute an operation and return the result."""
        return fn(*args, **kwargs)
