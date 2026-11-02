"""A project's named queue."""

from __future__ import annotations

import asyncio
import queue
import time
from collections.abc import AsyncIterator, Iterable, Iterator
from typing import ClassVar
from urllib.parse import urlencode

from labqoat._generated.queue_item_page import QueueItemPage
from labqoat._generated.queue_summary import QueueSummary
from labqoat._generated.queue_values import QueueValues
from labqoat.coordination.async_iteration import AsyncIteration
from labqoat.coordination.store_channel import StoreChannel
from labqoat.coordination.store_name import StoreName
from labqoat.coordination.value_batches import ValueBatches
from labqoat.coordination.value_codec import ValueCodec
from labqoat.coordination.wait_deadline import WaitDeadline
from labqoat.json_document import JsonValue


class Queue:
    """First in, first out values shared by a project's runs and the people working on it.

    Get it with ``context.queue(name)`` inside a run and ``client.queue(name)`` on a laptop. Each value goes to
    exactly one taker however many take at once. Partitions are independent queues under one name; a partition
    is cleared ``partition_ttl`` seconds after its last put and holds at most 100,000 values. Waiting calls wake
    as soon as a value lands. Every method has an ``_async`` twin for code running in an event loop.
    """

    DAY: ClassVar[int] = 86_400
    TAKE: ClassVar[int] = 1_000
    POLL: ClassVar[float] = 50.0

    def __init__(self, channel: StoreChannel, name: str) -> None:
        """Name a queue; nothing is contacted until it is used."""
        self.name = StoreName.check(name)
        self._channel = channel
        self._path = f"/queues/{name}"

    def __repr__(self) -> str:
        """Show the name only."""
        return f"Queue({self.name!r})"

    def put(
        self,
        v: object,
        *,
        block: bool = True,
        timeout: float | None = None,
        partition: str | None = None,
        partition_ttl: int = DAY,
    ) -> None:
        """Append one value; when the partition is full, wait for room unless ``block`` is false (``queue.Full``)."""
        self.put_many([v], block=block, timeout=timeout, partition=partition, partition_ttl=partition_ttl)

    def put_many(
        self,
        vs: Iterable[object],
        *,
        block: bool = True,
        timeout: float | None = None,
        partition: str | None = None,
        partition_ttl: int = DAY,
    ) -> None:
        """Append values in order, a thousand per request; ``queue.Full`` when no room came within ``timeout``."""
        deadline = WaitDeadline(timeout)
        encoded = [ValueCodec.encode(v) for v in vs]
        for batch in ValueBatches.split(encoded, ValueCodec.size):
            document: dict[str, JsonValue] = {"values": list(batch), "partition_ttl": partition_ttl}
            self._append(Queue.partitioned(document, partition), block, deadline)

    def get(self, *, block: bool = True, timeout: float | None = None, partition: str | None = None) -> object:
        """Remove and return the oldest value, waiting for one; ``None`` at once when not blocking and empty.

        Waiting ends with ``queue.Empty`` once ``timeout`` seconds pass; without one it waits for as long as it takes.
        """
        values = self._take(1, block, timeout, partition)
        if values:
            return values[0]
        if block:
            raise queue.Empty
        return None

    def get_many(
        self, n_values: int, *, block: bool = True, timeout: float | None = None, partition: str | None = None
    ) -> list[object]:
        """Remove and return up to ``n_values`` (at most 1,000) oldest values once at least one is there.

        Waiting ends with ``queue.Empty`` once ``timeout`` seconds pass; when not blocking an empty queue gives ``[]``.
        """
        if n_values < 1:
            raise ValueError("get_many takes at least one value")
        values = self._take(min(n_values, Queue.TAKE), block, timeout, partition)
        if not values and block:
            raise queue.Empty
        return values

    def len(self, *, partition: str | None = None, total: bool = False) -> int:
        """How many values one partition holds, or all of them together with ``total``."""
        query = urlencode(Queue.partitioned({"total": str(total).lower()}, partition))
        reply = self._channel.send("GET", f"{self._path}?{query}")
        return 0 if reply.missing else QueueSummary.from_dict(reply.document).items

    def clear(self, *, partition: str | None = None, all_partitions: bool = False) -> None:
        """Remove every value of one partition, or of every partition with ``all_partitions``."""
        query = urlencode(Queue.partitioned({"all": str(all_partitions).lower()}, partition))
        self._channel.send("DELETE", f"{self._path}/items?{query}")

    def iterate(self, *, partition: str | None = None, item_poll_timeout: float = 0.0) -> Iterator[object]:
        """Read values in order without removing them, ending once none arrives for ``item_poll_timeout`` seconds."""
        position = 0
        deadline = WaitDeadline(item_poll_timeout)
        while True:
            page = self._read(partition, position, deadline.remaining(Queue.POLL))
            if page.values:
                deadline = WaitDeadline(item_poll_timeout)
                position = page.position
                yield from (ValueCodec.decode(value) for value in page.values)
            elif deadline.expired():
                return

    async def put_async(
        self,
        v: object,
        *,
        block: bool = True,
        timeout: float | None = None,
        partition: str | None = None,
        partition_ttl: int = DAY,
    ) -> None:
        """``put`` for code running in an event loop."""
        await self.put_many_async([v], block=block, timeout=timeout, partition=partition, partition_ttl=partition_ttl)

    async def put_many_async(
        self,
        vs: Iterable[object],
        *,
        block: bool = True,
        timeout: float | None = None,
        partition: str | None = None,
        partition_ttl: int = DAY,
    ) -> None:
        """``put_many`` for code running in an event loop."""
        values = list(vs)
        await asyncio.to_thread(self._put_all, values, (block, timeout, partition, partition_ttl))

    async def get_async(
        self, *, block: bool = True, timeout: float | None = None, partition: str | None = None
    ) -> object:
        """``get`` for code running in an event loop."""
        return await asyncio.to_thread(self._get, (block, timeout, partition))

    async def get_many_async(
        self, n_values: int, *, block: bool = True, timeout: float | None = None, partition: str | None = None
    ) -> list[object]:
        """``get_many`` for code running in an event loop."""
        return await asyncio.to_thread(self._get_many, n_values, (block, timeout, partition))

    async def len_async(self, *, partition: str | None = None, total: bool = False) -> int:
        """``len`` for code running in an event loop."""
        return await asyncio.to_thread(self._len, partition, total)

    async def clear_async(self, *, partition: str | None = None, all_partitions: bool = False) -> None:
        """``clear`` for code running in an event loop."""
        await asyncio.to_thread(self._clear, partition, all_partitions)

    def iterate_async(self, *, partition: str | None = None, item_poll_timeout: float = 0.0) -> AsyncIterator[object]:
        """``iterate`` for code running in an event loop."""
        return AsyncIteration.of(self.iterate(partition=partition, item_poll_timeout=item_poll_timeout))

    def _put_all(self, values: list[object], options: tuple[bool, float | None, str | None, int]) -> None:
        """Run ``put_many`` with its keyword options on a worker thread."""
        block, timeout, partition, partition_ttl = options
        self.put_many(values, block=block, timeout=timeout, partition=partition, partition_ttl=partition_ttl)

    def _get(self, options: tuple[bool, float | None, str | None]) -> object:
        """Run ``get`` with its keyword options on a worker thread."""
        block, timeout, partition = options
        return self.get(block=block, timeout=timeout, partition=partition)

    def _get_many(self, n_values: int, options: tuple[bool, float | None, str | None]) -> list[object]:
        """Run ``get_many`` with its keyword options on a worker thread."""
        block, timeout, partition = options
        return self.get_many(n_values, block=block, timeout=timeout, partition=partition)

    def _len(self, partition: str | None, total: bool) -> int:
        """Run ``len`` with its keyword options on a worker thread."""
        return self.len(partition=partition, total=total)

    def _clear(self, partition: str | None, all_partitions: bool) -> None:
        """Run ``clear`` with its keyword options on a worker thread."""
        self.clear(partition=partition, all_partitions=all_partitions)

    def _append(self, document: dict[str, JsonValue], block: bool, deadline: WaitDeadline) -> None:
        """Put one batch, retrying with growing pauses while the partition is full and the caller may wait."""
        pause = 0.05
        while self._channel.send("POST", self._path + "/items", document).full:
            if not block or deadline.expired():
                raise queue.Full
            time.sleep(deadline.remaining(pause))
            pause = min(pause * 2, 1.0)

    def _take(self, limit: int, block: bool, timeout: float | None, partition: str | None) -> list[object]:
        """Take up to ``limit`` values, holding each request open on the service while the caller may wait."""
        deadline = WaitDeadline(timeout if block else 0.0)
        while True:
            wait = deadline.remaining(Queue.POLL)
            document: dict[str, JsonValue] = {"limit": limit, "timeout": wait}
            reply = self._channel.send("POST", self._path + "/take", Queue.partitioned(document, partition), wait)
            values = [] if reply.missing else QueueValues.from_dict(reply.document).values
            if values or deadline.expired():
                return [ValueCodec.decode(value) for value in values]

    def _read(self, partition: str | None, position: int, wait: float) -> QueueItemPage:
        """One page of values after ``position``, held open for up to ``wait`` seconds while there are none."""
        query = urlencode(Queue.partitioned({"after": position, "limit": 500, "timeout": wait}, partition))
        reply = self._channel.send("GET", f"{self._path}/items?{query}", None, wait)
        return QueueItemPage(values=[], position=position) if reply.missing else QueueItemPage.from_dict(reply.document)

    @staticmethod
    def partitioned(document: dict[str, JsonValue], partition: str | None) -> dict[str, JsonValue]:
        """Name the partition, leaving it out for the default one."""
        return document if partition is None else document | {"partition": partition}
