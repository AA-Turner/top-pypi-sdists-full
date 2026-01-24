# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later


import os

# Concurrent imports
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# Tango imports
from tango.green import AbstractExecutor, get_ident
from tango.utils import _get_current_otel_context, _get_non_tango_source_location

__all__ = (
    "FuturesExecutor",
    "get_global_executor",
    "set_global_executor",
    "_switch_global_executor_to_thread",
)

# Global executor

_MAIN_EXECUTOR = None
_THREAD_EXECUTORS = {}


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
        cls = ProcessPoolExecutor if process else ThreadPoolExecutor
        self.subexecutor = cls(max_workers=max_workers)

    def delegate(self, fn, *args, **kwargs):
        """Return the given operation as a concurrent future."""
        if hasattr(fn, "__trace_kwargs__"):
            kwargs["trace_location"] = _get_non_tango_source_location()
            kwargs["trace_context"] = _get_current_otel_context()
        return self.subexecutor.submit(fn, *args, **kwargs)

    def access(self, accessor, timeout=None):
        """Return a result from a single callable."""
        return accessor.result(timeout=timeout)

    def submit(self, fn, *args, **kwargs):
        """Submit an operation"""
        return fn(*args, **kwargs)

    def execute(self, fn, *args, **kwargs):
        """Execute an operation and return the result."""
        return fn(*args, **kwargs)
