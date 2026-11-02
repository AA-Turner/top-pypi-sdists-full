"""A project's queues as a collection."""

import secrets
from collections.abc import Iterator
from contextlib import contextmanager

from labqoat._generated.queue_list import QueueList
from labqoat._generated.queue_summary import QueueSummary
from labqoat.coordination.queue import Queue
from labqoat.coordination.store_channel import StoreChannel
from labqoat.coordination.store_name import StoreName


class QueuesClient:
    """List the project's queues, delete one, or hold a throwaway one for the length of a block."""

    def __init__(self, channel: StoreChannel) -> None:
        """Share the channel of the client or run that asked."""
        self._channel = channel

    def list(self) -> list[QueueSummary]:
        """Every queue of the project by name, with the values of all its partitions."""
        return QueueList.from_dict(self._channel.send("GET", "/queues").document).items

    def delete(self, name: str) -> None:
        """Delete a queue with all its partitions; ``KeyError`` when there is no such queue."""
        if self._channel.send("DELETE", "/queues/" + StoreName.check(name)).missing:
            raise KeyError(name)

    @contextmanager
    def ephemeral(self) -> Iterator[Queue]:
        """A queue under a fresh name, deleted when the block ends; hand ``.name`` to the runs that share it."""
        store = Queue(self._channel, "ephemeral-" + secrets.token_hex(8))
        try:
            yield store
        finally:
            self._channel.send("DELETE", "/queues/" + store.name)
