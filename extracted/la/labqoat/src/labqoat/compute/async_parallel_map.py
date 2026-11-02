"""Async bounded fan-out whose observers can be closed independently of accepted Runs."""

import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable, Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class AsyncParallelMap(Generic[T, R]):
    """Maintain a bounded task window without materializing the complete input iterable."""

    def __init__(self, operation: Callable[[T], Awaitable[R]], limit: int, ordered: bool) -> None:
        """Validate configuration before starting authored dispatch operations."""
        if type(limit) is not int or not 1 <= limit <= 256:
            raise ValueError("max_in_flight must be an integer between 1 and 256")
        self.operation = operation
        self.limit = limit
        self.ordered = ordered

    async def iterate(self, inputs: Iterable[T]) -> AsyncGenerator[R, None]:
        """Cancel observation tasks on close while leaving durable accepted work owned by the service."""
        source = iter(inputs)
        pending: dict[asyncio.Future[R], None] = {}
        try:
            self._fill(source, pending)
            while pending:
                task = await self._next(pending)
                del pending[task]
                yield await task
                self._fill(source, pending)
        finally:
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

    def _fill(self, source: Iterator[T], pending: dict[asyncio.Future[R], None]) -> None:
        """Start only enough operations to fill the current delivery window."""
        while len(pending) < self.limit:
            try:
                item = next(source)
            except StopIteration:
                return
            pending[asyncio.ensure_future(self.operation(item))] = None

    async def _next(self, pending: dict[asyncio.Future[R], None]) -> asyncio.Future[R]:
        """Choose the oldest input or wait for the earliest completed result."""
        if self.ordered:
            return next(iter(pending))
        completed, _remaining = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        return next(iter(completed))
