"""Core logic for simple mq."""

import secrets
import string
from typing import Iterable, List, Optional

from redis import Redis

# TODO: Consider removing the automatic name generation, because not that useful
# TODO: Consider making this private / removing the property


class SimpleMQ:
    """A simple FIFO message queue using Redis."""

    REDIS_KEY_PREFIX = "REDIS_SIMPLE_MQ"
    RANDOM_NAME_LENGTH = 16

    def __init__(self, conn: Redis, name: str = "") -> None:
        """Connect to a queue on Redis with the given name.
        Will create the queue if it does not exist.

        Args:
        - conn: Redis connection object, e.g. conn = Redis()
        - name: Name of this queue. If not defined a random ID will be generated.
        """

        if not isinstance(conn, Redis):
            raise TypeError("conn must be of type Redis")

        self._conn = conn
        if not name:
            self._name = "".join(
                [
                    secrets.choice(string.ascii_lowercase + string.digits)
                    for _ in range(self.RANDOM_NAME_LENGTH)
                ]
            )
        else:
            self._name = str(name)
        self._redis_key = f"{self.REDIS_KEY_PREFIX}_{self.name}"

    @property
    def conn(self) -> Redis:
        """Return redis connection."""
        return self._conn

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    def size(self) -> int:
        """Return current number of messages in the queue."""
        return int(self.conn.llen(self._redis_key))

    def clear(self) -> int:
        """Purge all messages from the queue and return count of cleared messages."""
        total = self.size()
        self.conn.ltrim(self._redis_key, 1, 0)
        return total

    def enqueue(self, message: str) -> int:
        """Enqueue one message into the queue
        and return size of the queue after enqueuing.
        """
        return self.conn.rpush(self._redis_key, str(message))

    def enqueue_bulk(self, messages: Iterable[str]) -> Optional[int]:
        """Enqueue a list of messages into the queue at once.

        Return size of the queue after enqueuing or None if list was empty.
        """
        queue_size = None
        for elem in messages:
            queue_size = self.enqueue(elem)
        return queue_size

    def dequeue(self) -> Optional[str]:
        """Dequeue one message from the queue. Return None if queue was empty."""
        value = self.conn.lpop(self._redis_key)
        if value is not None:
            return value.decode("utf8")
        return None

    def dequeue_bulk(self, max_messages: Optional[int] = None) -> List[str]:
        """Dequeue a list of message from the queue.

        Return no more than max message from queue
        or return all messages if max is not specified.
        Returns an empty list if queue is empty.
        """
        if max_messages is not None and int(max_messages) < 0:
            raise ValueError("max_messages can not be negative")

        messages = []
        i = 0
        while True:
            if max_messages is not None and i == int(max_messages):
                break
            i += 1
            data = self.dequeue()
            if data is None:
                break
            messages.append(data)
        return messages
