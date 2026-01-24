# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

# Imports
import sys
import os
import functools
from collections import namedtuple

# Gevent imports
import gevent.event
import gevent.queue
import gevent.monkey
import gevent.threadpool

# Bypass gevent monkey patching
ThreadSafeEvent = gevent.monkey.get_original("threading", "Event")

# Tango imports
from tango.green import AbstractExecutor, get_ident
from tango.utils import _get_current_otel_context, _get_non_tango_source_location

__all__ = (
    "GeventExecutor",
    "get_global_executor",
    "set_global_executor",
    "_switch_global_executor_to_thread",
)

# Global executor

_MAIN_EXECUTOR = None
_THREAD_POOL = None
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
        _MAIN_EXECUTOR = GeventExecutor(subexecutor=ThreadPool(maxsize=100))


def get_global_executor():
    global _MAIN_EXECUTOR
    if _MAIN_EXECUTOR is None:
        _MAIN_EXECUTOR = GeventExecutor()

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


def get_global_threadpool():
    global _THREAD_POOL
    if _THREAD_POOL is None:
        _THREAD_POOL = ThreadPool(maxsize=10**4)
    return _THREAD_POOL


ExceptionInfo = namedtuple("ExceptionInfo", "type value traceback")


def wrap_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return ExceptionInfo(*sys.exc_info())

    return wrapper


def unwrap_error(source):
    destination = gevent.event.AsyncResult()

    def link(source):
        if isinstance(source.value, ExceptionInfo):
            try:
                destination.set_exception(source.value.value, exc_info=source.value)
            # Gevent 1.0 compatibility
            except TypeError:
                destination.set_exception(source.value.value)
            return
        destination(source)

    source.rawlink(link)
    return destination


class ThreadPool(gevent.threadpool.ThreadPool):
    def spawn(self, fn, *args, **kwargs):
        wrapped = wrap_error(fn)
        raw = super().spawn(wrapped, *args, **kwargs)
        return unwrap_error(raw)


# Gevent task and event loop


class GeventTask:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.value = None
        self.exception = None
        self.done = ThreadSafeEvent()
        self.started = ThreadSafeEvent()

    def run(self):
        self.started.set()
        try:
            self.value = self.func(*self.args, **self.kwargs)
        except Exception:
            self.exception = sys.exc_info()
        finally:
            self.done.set()

    def spawn(self):
        return gevent.spawn(self.run)

    def result(self):
        self.done.wait()
        if self.exception:
            raise self.exception[1]
        return self.value


# Gevent executor


class GeventExecutor(AbstractExecutor):
    """Gevent tango executor"""

    asynchronous = True
    default_wait = True

    def __init__(self, loop=None, subexecutor=None):
        super().__init__()
        if loop is None:
            loop = gevent.get_hub().loop
        if subexecutor is None:
            subexecutor = get_global_threadpool()
        self.loop = loop
        self.subexecutor = subexecutor

    def delegate(self, fn, *args, **kwargs):
        """Return the given operation as a gevent future."""
        if hasattr(fn, "__trace_kwargs__"):
            kwargs["trace_location"] = _get_non_tango_source_location()
            kwargs["trace_context"] = _get_current_otel_context()
        return self.subexecutor.spawn(fn, *args, **kwargs)

    def access(self, accessor, timeout=None):
        """Return a result from an gevent future."""
        return accessor.get(timeout=timeout)

    def create_watcher(self):
        try:
            return self.loop.async_()
        except AttributeError:
            return getattr(self.loop, "async")()

    def submit(self, fn, *args, **kwargs):
        task = GeventTask(fn, *args, **kwargs)
        watcher = self.create_watcher()
        watcher.start(task.spawn)
        watcher.send()
        task.started.wait()
        # The watcher has to be stopped in order to be garbage-collected.
        # This step is crucial since the watcher holds a reference to the
        # `task.spawn` method which itself holds a reference to the task.
        # It's also important to wait for the task to be spawned before
        # stopping the watcher, otherwise the task won't run.
        watcher.stop()
        return task

    def execute(self, fn, *args, **kwargs):
        """Execute an operation and return the result."""
        if self.in_executor_context():
            return fn(*args, **kwargs)
        task = self.submit(fn, *args, **kwargs)
        return task.result()
