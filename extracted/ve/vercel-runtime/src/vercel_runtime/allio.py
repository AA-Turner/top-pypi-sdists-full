"""Lightweight compat library for asyncio/trio.

We want to support both asyncio and trio, but don't want to depend on
anyio, and we don't want to vendor it, because it contains state that
we don't want to deal with.

So instead we just expose the different stuff we need, which is pretty
minimal.
"""

from __future__ import annotations

import asyncio
import contextlib
import functools
import importlib
import sys
from typing import TYPE_CHECKING, Any, Protocol, Self

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from types import TracebackType

__all__ = [
    "create_task_group",
    "current_async_library",
    "current_rt",
    "get_cancelled_exc_class",
    "run",
    "to_thread",
]


class _TaskGroupProtocol(Protocol):
    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
        /,
    ) -> None: ...

    def start_soon[T, *Args](
        self,
        func: Callable[[*Args], Coroutine[Any, Any, T]],
        /,
        *args: *Args,
    ) -> None: ...


class _Runtime(Protocol):
    @staticmethod
    def create_task_group() -> _TaskGroupProtocol: ...

    @staticmethod
    def get_cancelled_exc_class() -> type[BaseException]: ...

    @staticmethod
    def run[T, *Args](
        func: Callable[[*Args], Coroutine[Any, Any, T]],
        /,
        *args: *Args,
    ) -> T: ...

    @staticmethod
    async def to_thread[T, *Args](
        func: Callable[[*Args], T],
        /,
        *args: *Args,
    ) -> T: ...


class _AsyncioTaskGroup(asyncio.TaskGroup):
    def start_soon[T, *Args](
        self,
        func: Callable[[*Args], Coroutine[Any, Any, T]],
        /,
        *args: *Args,
    ) -> None:
        self.create_task(func(*args))


class _AsyncioRuntime:
    @staticmethod
    def create_task_group() -> _TaskGroupProtocol:
        return _AsyncioTaskGroup()

    @staticmethod
    def get_cancelled_exc_class() -> type[BaseException]:
        return asyncio.CancelledError

    @staticmethod
    def run[T, *Args](
        func: Callable[[*Args], Coroutine[Any, Any, T]],
        /,
        *args: *Args,
    ) -> T:
        return asyncio.run(func(*args))

    @staticmethod
    async def to_thread[T, *Args](
        func: Callable[[*Args], T],
        /,
        *args: *Args,
    ) -> T:
        return await asyncio.to_thread(func, *args)


def _create_trio_runtime(trio: Any) -> type[_Runtime]:
    class _TrioRuntime:
        @staticmethod
        def create_task_group() -> _TaskGroupProtocol:
            return trio.open_nursery()  # type: ignore[no-any-return]

        @staticmethod
        def get_cancelled_exc_class() -> type[BaseException]:
            return trio.Cancelled  # type: ignore[no-any-return]

        @staticmethod
        def run[T, *Args](
            func: Callable[[*Args], Coroutine[Any, Any, T]],
            /,
            *args: *Args,
        ) -> T:
            return trio.run(func, *args)  # type: ignore[no-any-return]

        @staticmethod
        async def to_thread[T, *Args](
            func: Callable[[*Args], T],
            /,
            *args: *Args,
        ) -> T:
            return await trio.to_thread.run_sync(  # type: ignore[no-any-return]
                func, *args
            )

    return _TrioRuntime


# Look up trio and sniffio only when they are needed: the runtime may add
# the application's dependencies to `sys.path` after importing this module.
@functools.cache
def _trio_runtime() -> type[_Runtime]:
    return _create_trio_runtime(importlib.import_module("trio"))


def current_async_library() -> str:
    # trio imports sniffio, so if nothing has imported sniffio, trio is not
    # running.
    sniffio: Any = sys.modules.get("sniffio")
    if sniffio is not None:
        return sniffio.current_async_library()  # type: ignore[no-any-return]

    asyncio.get_running_loop()
    return "asyncio"


def current_rt() -> type[_Runtime]:
    return _get_runtime(current_async_library())


def _get_runtime(backend: str) -> type[_Runtime]:
    if backend == "asyncio":
        return _AsyncioRuntime
    if backend == "trio":
        with contextlib.suppress(ImportError):
            return _trio_runtime()
    msg = f'async backend "{backend}" is not available'
    raise RuntimeError(msg)


def create_task_group() -> _TaskGroupProtocol:
    return current_rt().create_task_group()


def get_cancelled_exc_class() -> type[BaseException]:
    return current_rt().get_cancelled_exc_class()


def run[T, *Args](
    func: Callable[[*Args], Coroutine[Any, Any, T]],
    /,
    *args: *Args,
    backend: str = "asyncio",
) -> T:
    return _get_runtime(backend).run(func, *args)


async def to_thread[T, *Args](
    func: Callable[[*Args], T],
    /,
    *args: *Args,
) -> T:
    return await current_rt().to_thread(func, *args)
