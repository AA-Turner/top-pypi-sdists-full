# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

# Imports
import functools
import asyncio
import inspect
import collections
import os
import types
import concurrent.futures
import warnings
import threading

from asyncio import futures, coroutines
from asyncio.tasks import ensure_future
from typing import Callable

# Tango imports
from tango.green import AbstractExecutor
from tango.utils import (
    _get_current_otel_context,
    _get_non_tango_source_location,
    _is_coroutine_function,
    PyTangoThreadPoolExecutor,
)

__all__ = (
    "AsyncioExecutor",
    "get_global_executor",
    "set_global_executor",
    "_switch_global_executor_to_thread",
)

_ALREADY_WARNED_FUNCTIONS = []


# Function removed from Python 3.11
# Taken from https://github.com/python/cpython/blob/3.10/Lib/asyncio/coroutines.py
# (without the _DEBUG part)
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 Python Software Foundation;
# All Rights Reserved
def _coroutine(func):
    """Decorator to mark coroutines.
    If the coroutine is not yielded from before it is destroyed,
    an error message is logged.
    """
    if inspect.iscoroutinefunction(func):
        return func

    if inspect.isgeneratorfunction(func):
        coro = func
    else:

        @functools.wraps(func)
        def coro(*args, **kw):
            res = func(*args, **kw)
            if asyncio.isfuture(res) or inspect.isgenerator(res):
                res = yield from res
            else:
                # If 'res' is an awaitable, run it.
                try:
                    await_meth = res.__await__
                except AttributeError:
                    pass
                else:
                    if isinstance(res, collections.abc.Awaitable):
                        res = yield from await_meth()
            return res

    coro = types.coroutine(coro)
    wrapper = coro
    wrapper._is_coroutine = (
        asyncio.coroutines._is_coroutine
    )  # For iscoroutinefunction().
    return wrapper


# In Python 3.12 the legacy generator-based coroutines are not allowed for execution anymore
# Here we use modified run_coroutine_threadsafe method, which still can execute them
# Taken from https://github.com/python/cpython/blob/3.12/Lib/asyncio/tasks.py
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Python Software Foundation;
# All Rights Reserved
def run_coroutine_threadsafe(coro, loop):
    """Submit a coroutine object to a given event loop.

    Return a concurrent.futures.Future to access the result.
    """
    if not coroutines.iscoroutine(coro) and not types.GeneratorType:
        raise TypeError("A coroutine object is required")

    future = concurrent.futures.Future()

    def callback():
        try:
            futures._chain_future(ensure_future(coro, loop=loop), future)
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            if future.set_running_or_notify_cancel():
                future.set_exception(exc)
            raise

    loop.call_soon_threadsafe(callback)
    return future


_PYTANGOTHREADPOOLEXECUTOR = None


def get_thread_pool_executor():
    global _PYTANGOTHREADPOOLEXECUTOR
    if _PYTANGOTHREADPOOLEXECUTOR is None:
        _PYTANGOTHREADPOOLEXECUTOR = PyTangoThreadPoolExecutor(
            thread_name_prefix="_PyTangoThreadPoolExecutor"
        )
    return _PYTANGOTHREADPOOLEXECUTOR


# Global executor
_MAIN_EXECUTOR = None
_THREAD_EXECUTORS = {}


def _switch_global_executor_to_thread():
    """
    internal PyTango function, use only if you sure, what you are doing!
    Used for correct behavior of TestDeviceContext
    Checks, that global executor belongs to the caller thread, and,
    if not - creates a new one and saves it as a new global
    """
    global _MAIN_EXECUTOR
    if _MAIN_EXECUTOR is not None and not _MAIN_EXECUTOR.in_executor_context():
        # we save current executor in the known subthread executors to be used later
        _THREAD_EXECUTORS[_MAIN_EXECUTOR.get_ident()] = _MAIN_EXECUTOR
        _MAIN_EXECUTOR = AsyncioExecutor()


def get_global_executor():
    global _MAIN_EXECUTOR
    if _MAIN_EXECUTOR is None:
        _MAIN_EXECUTOR = AsyncioExecutor()
    # the following patch is used for correct behavior of TestDeviceContext,
    # which has two different executors for main and device threads
    if not _MAIN_EXECUTOR.in_executor_context():
        ident = threading.get_ident(), os.getpid()
        if ident in _THREAD_EXECUTORS:
            return _THREAD_EXECUTORS[ident]

    return _MAIN_EXECUTOR


def set_global_executor(executor):
    global _MAIN_EXECUTOR
    _MAIN_EXECUTOR = executor


def _get_function_name(fn: Callable) -> str:
    if hasattr(fn, "__qualname__"):
        return fn.__qualname__
    elif hasattr(fn, "__name__"):
        return fn.__name__

    return f"{fn}"


# Asyncio executor
class AsyncioExecutor(AbstractExecutor):
    """Asyncio tango executor"""

    asynchronous = True
    default_wait = False

    def __init__(self, loop=None, subexecutor=None):
        super().__init__()
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        self.loop = loop
        self.subexecutor = (
            subexecutor if subexecutor is not None else get_thread_pool_executor()
        )

    def delegate(self, fn, *args, **kwargs):
        """Return the given operation as an asyncio future."""
        if hasattr(fn, "__trace_kwargs__"):
            kwargs["trace_location"] = _get_non_tango_source_location()
            kwargs["trace_context"] = _get_current_otel_context()
        callback = functools.partial(fn, *args, **kwargs)
        coro = self.loop.run_in_executor(self.subexecutor, callback)
        return asyncio.ensure_future(coro)

    def access(self, accessor, timeout=None):
        """Return a result from an asyncio future."""
        if self.loop.is_running():
            raise RuntimeError("Loop is already running")
        coro = asyncio.wait_for(accessor, timeout)
        return self.loop.run_until_complete(coro)

    def submit(self, fn, *args, **kwargs):
        """Submit an operation"""
        if _is_coroutine_function(fn):
            return run_coroutine_threadsafe(fn(*args, **kwargs), self.loop)
        else:
            # we leave this part of the code to support legacy servers
            name = _get_function_name(fn)
            if name not in _ALREADY_WARNED_FUNCTIONS:
                _ALREADY_WARNED_FUNCTIONS.append(name)
                warnings.warn(
                    f"Sync {name} function called: support of "
                    f"sync functions in PyTango's Asyncio mode is "
                    f"deprecated. Use 'async def' instead of 'def'.",
                    DeprecationWarning,
                )
            corofn = _coroutine(lambda: fn(*args, **kwargs))
            return run_coroutine_threadsafe(corofn(), self.loop)

    def execute(self, fn, *args, **kwargs):
        """Execute an operation and return the result."""
        if self.in_executor_context():
            if _is_coroutine_function(fn):
                return fn(*args, **kwargs)
            else:
                # we leave this part of the code to support legacy servers
                name = _get_function_name(fn)
                if name not in _ALREADY_WARNED_FUNCTIONS:
                    _ALREADY_WARNED_FUNCTIONS.append(name)
                    warnings.warn(
                        f"Sync {name} function called: support of "
                        f"sync functions in PyTango's Asyncio mode is "
                        f"deprecated. Use 'async def' instead of 'def'.",
                        DeprecationWarning,
                    )
                corofn = _coroutine(lambda: fn(*args, **kwargs))
                return corofn()
        future = self.submit(fn, *args, **kwargs)
        return future.result()
