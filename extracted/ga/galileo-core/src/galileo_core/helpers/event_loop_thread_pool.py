"""
EventLoopThreadPool provides a mechanism for running asyncio coroutines from synchronous code.

This module contains implementations for:
1. EventLoopThreadInterface - An abstract interface for event loop thread implementations
2. EventLoopThread - A single thread with its own event loop for executing coroutines
3. EventLoopThreadPool - A pool of EventLoopThread instances that are initialized lazily

The EventLoopThreadPool is particularly useful in scenarios where:
- You need to execute async code from a synchronous context
- You want to parallelize async operations across multiple event loops
- You need to maintain a pool of reusable event loops for performance reasons

Examples:
    Basic usage with waiting for results:
    ```python
    # Create a thread pool
    pool = EventLoopThreadPool(name="MyThreadPool", num_threads=4)

    # Define an async function
    async def fetch_data(url):
        # ... async code here
        return result

    # Execute the async function and wait for results
    result = pool.submit(lambda: fetch_data("https://example.com"))
    ```

    Fire-and-forget usage:
    ```python
    # Submit without waiting for result
    future = pool.submit(lambda: process_data_async(data), wait_for_result=False)

    # Optionally check the result later
    result = future.result()  # This will block until complete
    ```

    Direct coroutine submission:
    ```python
    # Create and submit a coroutine directly
    coroutine = fetch_data("https://example.com")
    result = pool.submit(coroutine)
    ```

The module handles gevent integration automatically and will adapt its behavior
when running in a gevent-patched environment.
"""

import asyncio
import os
import random
import threading
from abc import abstractmethod
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from logging import getLogger
from typing import Any, Callable, Coroutine, List, Union

logger = getLogger(__name__)


# EventLoopThread doesn't play nice with gevent because gevent patches threading.
# So if we are in gevent patched environment, we have different control flow.
_GEVENT_PATCHED = False
try:
    import gevent  # type: ignore[import-not-found]
    import gevent.monkey  # type: ignore[import-not-found]

    # Check if threading specifically is patched
    _GEVENT_PATCHED = gevent.monkey.is_module_patched("threading")
except ImportError:
    pass  # gevent not installed or not used


class EventLoopThreadInterface:
    def submit(
        self,
        async_fn: Union[Callable[[], Coroutine[Any, Any, Any]], Coroutine[Any, Any, Any]],
        wait_for_result: bool = True,
    ) -> Any:
        """
        Submit an async function or coroutine.

        If `wait_for_result` is True, this method will block until the async function
        completes and returns its result (or raises an exception). Otherwise, it returns
        a concurrent.futures.Future immediately.
        """
        pass

    @abstractmethod
    def stop(self, timeout_sec: int = 2) -> None:
        """
        For testing only.
        :param timeout_sec:
        :return:
        """
        pass


class EventLoopThread(EventLoopThreadInterface, threading.Thread):
    """
    A thread that runs its own event loop so you can submit coroutines to be executed
    on it and wait for results from synchronous code.
    """

    def __init__(self, name: str = "EventLoopThread", daemon: bool = True) -> None:
        super().__init__(name=name)
        self.daemon = daemon
        self.loop: AbstractEventLoop
        if not _GEVENT_PATCHED:
            try:
                import uvloop  # type: ignore[import-not-found]

                self.loop = uvloop.new_event_loop()
            except ImportError:
                self.loop = asyncio.new_event_loop()
        else:
            self.loop = asyncio.new_event_loop()

    def run(self) -> None:
        # Set the event loop for this thread.
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def submit(
        self,
        async_fn: Union[Callable[[], Coroutine[Any, Any, Any]], Coroutine[Any, Any, Any]],
        wait_for_result: bool = True,
    ) -> Any:
        coro: Coroutine[Any, Any, Any] = async_fn if isinstance(async_fn, Coroutine) else async_fn()
        future: Future[Any] = asyncio.run_coroutine_threadsafe(coro, self.loop)

        if wait_for_result:
            # Block until the result is ready (or an exception is raised).
            result = future.result()
            return result
        else:
            return future

    def stop(self, timeout_sec: int = 2) -> None:
        """Stop the event loop."""
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join(timeout=timeout_sec)


class EventLoopThreadPool(EventLoopThreadInterface):
    """
    Manage collection of EventLoopThread instances and also initailize them lazily.

    Lazy initialization is important when running in forked processes.
    """

    def __init__(self, name: str = "EventLoopThreadPool", num_threads: int = 16) -> None:
        self.name = name
        self.num_threads = num_threads
        self.threads: List[EventLoopThread] = []
        self.init_pid = os.getpid()  # Store the PID when the pool is initialized

        self.init_lock = threading.Lock()

    def submit(
        self,
        async_fn: Union[Callable[[], Coroutine[Any, Any, Any]], Coroutine[Any, Any, Any]],
        wait_for_result: bool = True,
    ) -> Any:
        if _GEVENT_PATCHED:
            import gevent
            from gevent.event import AsyncResult  # type: ignore[import-not-found]

            async_result: AsyncResult[Any] = AsyncResult()

            def run_coro_in_temp_loop() -> None:
                try:
                    coro = async_fn if asyncio.iscoroutine(async_fn) else async_fn()
                    result: Any = asyncio.run(coro)  # type: ignore[arg-type]
                    async_result.set(result)
                except Exception as e:
                    async_result.set_exception(e)

            gevent.spawn(run_coro_in_temp_loop)

            if wait_for_result:
                return async_result.get()
            return async_result
        else:
            # If threads list is empty or we're in a different process (forked), initialize new threads
            if len(self.threads) == 0 or os.getpid() != self.init_pid:
                with self.init_lock:
                    if len(self.threads) == 0 or os.getpid() != self.init_pid:
                        self.threads = [EventLoopThread(f"{self.name}-{i}") for i in range(self.num_threads)]
                        self.init_pid = os.getpid()  # Update the PID
                        for thread in self.threads:
                            thread.start()
                        logger.debug(f"Initialized EventLoopThreadPool {self.name} in PID {self.init_pid}")
            return random.choice(self.threads).submit(async_fn, wait_for_result)

    def stop(self, timeout_sec: int = 2) -> None:
        if self.threads:
            for thread in self.threads:
                thread.stop(timeout_sec)
