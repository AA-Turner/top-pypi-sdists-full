from __future__ import annotations

import contextlib
import contextvars
import inspect
import logging
import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING

from vercel_runtime import allio
from vercel_runtime.invocation_hooks import attach_due_hooks

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class _PendingAwaitable:
    awaitable: Awaitable[object]
    context: contextvars.Context


class WaitUntilCollector:
    """Invocation-scoped collection of post-response work."""

    def __init__(self) -> None:
        self._pending: dict[int, _PendingAwaitable] = {}
        self._closed = False
        self._lock = threading.Lock()

    def wait_until(self, awaitable: Awaitable[object]) -> None:
        if not inspect.isawaitable(awaitable):
            msg = (
                "wait_until can only be called with an awaitable, "
                f"got {type(awaitable).__name__}"
            )
            raise TypeError(msg)

        with self._lock:
            if self._closed:
                _close_coroutine(awaitable)
                msg = "wait_until cannot be called after the invocation ended"
                raise RuntimeError(msg)
            self._pending.setdefault(
                id(awaitable),
                _PendingAwaitable(
                    awaitable=awaitable,
                    context=contextvars.copy_context(),
                ),
            )

    async def drain(self) -> None:
        while True:
            with self._lock:
                batch = list(self._pending.values())
                self._pending.clear()
                if not batch:
                    self._closed = True
                    return

            errors: list[BaseException] = []
            cancelled_error = allio.get_cancelled_exc_class()
            async with allio.create_task_group() as task_group:
                for pending in batch:
                    pending.context.run(
                        task_group.start_soon,
                        _run_pending,
                        pending,
                        errors,
                    )

            for error in errors:
                if isinstance(error, cancelled_error):
                    logger.error("wait_until task was cancelled")
                else:
                    logger.error(
                        "wait_until task failed",
                        exc_info=(
                            type(error),
                            error,
                            error.__traceback__,
                        ),
                    )


def begin_wait_until() -> WaitUntilCollector:
    collector = WaitUntilCollector()
    _set_public_wait_until(collector.wait_until)
    attach_due_hooks(collector.wait_until)
    return collector


async def finish_wait_until_async(collector: WaitUntilCollector) -> None:
    try:
        await collector.drain()
    finally:
        _set_public_wait_until(None)


def finish_wait_until(collector: WaitUntilCollector) -> None:
    try:
        allio.run(collector.drain)
    finally:
        clear_wait_until_context()


def clear_wait_until_context() -> None:
    _set_public_wait_until(None)


def _set_public_wait_until(
    callback: Callable[[Awaitable[object]], None] | None,
) -> None:
    with contextlib.suppress(ImportError):
        from vercel.cache.context import (  # noqa: PLC0415  # pyright: ignore[reportMissingTypeStubs]
            get_context,
            set_context,
        )

        set_context(wait_until=callback)
        if callback is None and get_context().wait_until is not None:
            # vercel-cache versions before its UNSET sentinel treated None as
            # "leave unchanged". Replace the completed collector with a
            # stateless no-op so a warm worker cannot retain the invocation.
            set_context(wait_until=_discard_wait_until)


async def _run_pending(
    pending: _PendingAwaitable,
    errors: list[BaseException],
) -> None:
    try:
        await pending.awaitable
    except BaseException as error:
        errors.append(error)


def _close_coroutine(awaitable: Awaitable[object]) -> None:
    if inspect.iscoroutine(awaitable):
        awaitable.close()


def _discard_wait_until(awaitable: Awaitable[object]) -> None:
    _close_coroutine(awaitable)
