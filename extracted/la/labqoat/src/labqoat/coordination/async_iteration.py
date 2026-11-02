"""Blocking iterators consumed from an event loop."""

import asyncio
import itertools
from collections.abc import AsyncIterator, Iterator
from typing import TypeVar

ItemT = TypeVar("ItemT")


class AsyncIteration:
    """Advance a blocking iterator on a worker thread so the event loop keeps running while it waits."""

    @staticmethod
    async def of(iterator: Iterator[ItemT]) -> AsyncIterator[ItemT]:
        """Yield what the iterator yields, one step per thread hop."""
        while True:
            step = await asyncio.to_thread(AsyncIteration.step, iterator)
            if not step:
                return
            yield step[0]

    @staticmethod
    def step(iterator: Iterator[ItemT]) -> list[ItemT]:
        """The next item in a list of one, or an empty list once the iterator ends."""
        return list(itertools.islice(iterator, 1))
