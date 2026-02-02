from collections import deque
from typing import Generic, TypeVar

from theutilitybelt.numeric.bitwise import get_next_highest_power_of_2

TItem = TypeVar("TItem")


class Queue(Generic[TItem]):
    def __init__(self, max_size: int | None = None):
        self._items = deque(maxlen=max_size)

    def put(self, item: TItem):
        self._items.append(item)

    def get(self) -> TItem:
        return self._items.popleft()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def safe_get(self) -> TItem | None:
        if self.is_empty():
            return None

        return self.get()


class BoundedQueue(Generic[TItem]):
    def __init__(self, size: int = 64):
        # Adjust size to the next highest power of 2
        self._size = get_next_highest_power_of_2(size)
        self._mask = self._size - 1  # To use bitwise AND instead of modulus
        self._items: list[TItem | None] = [None] * self._size
        self._head = 0
        self._tail = 0
        self._count = 0

    def put(self, item: TItem):
        if self._count == self._size:
            raise OverflowError("Queue is full")
        self._items[self._tail] = item
        self._tail = (self._tail + 1) & self._mask
        self._count += 1

    def get(self) -> TItem:
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self._items[self._head]
        self._items[self._head] = None  # Clear the slot for GC
        self._head = (self._head + 1) & self._mask
        self._count -= 1
        return item  # type: ignore

    def is_empty(self):
        return self._count == 0

    def safe_get(self) -> TItem | None:
        if self.is_empty():
            return None

        return self.get()

    def __str__(self):
        items = []
        idx = self._head
        for _ in range(self._count):
            items.append(self._items[idx])
            idx = (idx + 1) & self._mask
        return str(items)
