import logging
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Generic, TypeVar

_LOG = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass(order=True)
class _QueueItem(Generic[T]):
    position: int
    size: int
    item: T = field(compare=False)


class SequenceQueue(Generic[T]):
    """A queue that maintains order based on sequence positions.

    Items can be inserted with their position and size, and the queue will maintain
    them in order. The pop() method will only return an item if the next
    expected position is available. When an item is popped, the next position
    advances to the end of the item's span (``position + size``).

    This only works if the sequence covers the entire range of positions
    without any gaps.  If there are gaps then the queue will never emit an
    item and just fill up.

    Overlap semantics (GEN-744): producers may enqueue items whose spans
    overlap ones already popped (e.g. checkpoint recovery re-enqueues a
    range at a clipped offset). An item whose span is *fully* behind the
    cursor (``position + size <= next_position``) contributes nothing and
    is silently dropped on read. An item that *partially* overlaps
    (``position < next_position < position + size``) is still returned by
    ``pop()``; the consumer is responsible for skipping the
    already-covered prefix. This keeps ``is_empty()`` and ``pop()``
    coherent — whenever ``is_empty()`` is False, ``pop()`` returns an
    item — so a ``while not is_empty(): pop()`` consumer can never spin.

    Examples
    --------
        >>> q = SequenceQueue[str]()
        >>> q.put(1, 2, "second")  # position 2, size 2
        >>> q.put(0, 1, "first")   # position 0, size 2
        >>> q.put(3, 1, "third")   # position 3, size 1
        >>> q.pop()  # Returns "first" (advances position by 1)
        >>> q.pop()  # Returns "second" (advances position by 2)
        >>> q.pop()  # Returns "third" (advances position by 1)
    """

    def __init__(self) -> None:
        self._heap = []
        self._next_position = 0

    def _drop_fully_stale(self) -> None:
        """Discard heap items whose span is entirely behind the cursor.

        Such items exist when a producer enqueues a span overlapping ones
        already popped. They have nothing left to contribute, and keeping
        them would stall ``pop()`` (position mismatch) without emptying
        the heap — an infinite loop in any ``while not is_empty(): pop()``
        consumer.
        """
        while (
            self._heap
            and self._heap[0].position + self._heap[0].size <= self._next_position
        ):
            dropped = heappop(self._heap)
            _LOG.warning(
                "Dropping fully-covered stale item at position %d (size %d, "
                "next_position %d); producer enqueued rows already emitted",
                dropped.position,
                dropped.size,
                self._next_position,
            )

    def put(self, position: int, size: int, item: T) -> None:
        """Insert an item with its position and size into the queue.

        Parameters
        ----------
            position
                The sequence position of the item
            size
                The size of the item (how much to advance next_position)
            item
                The item to insert
        """
        heappush(self._heap, _QueueItem(position, size, item))

    def pop(self) -> T | None:
        """Pop the next item in sequence if available.

        Returns
        -------
            The next item in sequence if available, None otherwise.
            An item is returned when its span reaches the next expected
            position; a partially overlapping item (position behind the
            cursor but span extending past it) is returned as-is and the
            caller must skip the already-covered prefix. On pop,
            next_position advances to ``position + size``. Items fully
            behind the cursor are silently discarded.
        """
        self._drop_fully_stale()
        if not self._heap:
            return None

        next_item = self._heap[0]
        if next_item.position <= self._next_position:
            heappop(self._heap)
            self._next_position = next_item.position + next_item.size
            return next_item.item
        return None

    def peek(self) -> T | None:
        """Peek at the next item in sequence without removing it.

        Returns
        -------
            The next item in sequence if available and ready, None otherwise.
        """
        self._drop_fully_stale()
        if not self._heap:
            return None

        next_item = self._heap[0]
        if next_item.position <= self._next_position:
            return next_item.item
        return None

    def is_empty(self) -> bool:
        """Check if the queue holds anything poppable right now.

        Returns
        -------
            True if the heap is empty (after reaping fully-stale items) or
            the next buffered item starts past the expected position (a
            gap). Guaranteed coherent with pop(): False means pop()
            returns an item.
        """
        self._drop_fully_stale()
        return len(self._heap) == 0 or self._heap[0].position > self._next_position

    def next_position(self) -> int:
        """Get the next expected position.

        Returns
        -------
            The next position that will be returned by pop()
        """
        return self._next_position

    def next_buffered_position(self) -> int | None:
        """Return the smallest buffered position (if any).

        This is useful for detecting gaps: when the queue is empty for the next
        expected position, the next buffered position indicates where coverage
        resumes.
        """
        self._drop_fully_stale()
        if not self._heap:
            return None
        return self._heap[0].position
