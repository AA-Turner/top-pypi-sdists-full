# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Threads and pools that register themselves with omniORB."""

import threading
import weakref

# Since cppTango based on omniThreads, we have to slightly modify ThreadPoolExecutor,
# to use threads with ensured dummy omniORB ID
#
# The `_adjust_thread_count` method below is a slightly modified version of the code from
# https://github.com/python/cpython/blob/3.12/Lib/concurrent/futures/thread.py
# and
# https://github.com/python/cpython/blob/3.14/Lib/concurrent/futures/thread.py
# Copyright (c) Python Software Foundation; All Rights Reserved
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures.thread import _threads_queues, _worker

from tango import EnsureOmniThread


class PyTangoThreadPoolExecutor(ThreadPoolExecutor):
    """
    Based on :class:`concurrent.futures.ThreadPoolExecutor`,
    but additionally ensures every running thread is a dummy omniORB thread.

    The :class:`tango.EnsureOmniThread` context handler is automatically active for
    the lifetime of the all the thread pool's threads.

    .. versionadded:: 10.0.0
    """

    def _adjust_thread_count(self):
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(timeout=0):
            return

        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = f"{self._thread_name_prefix or self}_{num_threads}"
            if hasattr(self, "_initializer"):
                # Python < 3.14
                t = threading.Thread(
                    name=thread_name,
                    target=_thread_pool_executor_worker,
                    args=(
                        weakref.ref(self, weakref_cb),
                        self._work_queue,
                        self._initializer,
                        self._initargs,
                    ),
                )
            else:
                # Python >= 3.14
                t = threading.Thread(
                    name=thread_name,
                    target=_thread_pool_executor_ctx_worker,
                    args=(
                        weakref.ref(self, weakref_cb),
                        self._create_worker_context(),
                        self._work_queue,
                    ),
                )
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue


# Override _worker for Python < 3.14
def _thread_pool_executor_worker(executor_reference, work_queue, initializer, initargs):
    with EnsureOmniThread():
        _worker(executor_reference, work_queue, initializer, initargs)


# Override _worker for Python >= 3.14
def _thread_pool_executor_ctx_worker(executor_reference, ctx, work_queue):
    with EnsureOmniThread():
        _worker(executor_reference, ctx, work_queue)


class PyTangoThread(threading.Thread):
    """
    Based on :class:`threading.Thread`, but additionally ensures it is a dummy omniORB thread.

    The :class:`tango.EnsureOmniThread` handler is automatically active for the lifetime of the
    thread.

    .. versionadded:: 10.3.0
    """

    def _bootstrap_inner(self):
        with EnsureOmniThread():
            super()._bootstrap_inner()
