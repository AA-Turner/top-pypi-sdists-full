from __future__ import annotations

import weakref
from typing import Generic, TypeVar

T = TypeVar("T")


class WeakSetByIdentity(Generic[T]):
    def __init__(self):
        super().__init__()
        self._items: dict[int, weakref.ReferenceType[T]] = {}

    def add(self, item: T):
        """
        Adds the item to this weak set. It will not be kept alive.
        """
        item_id = id(item)

        def remove_item(ref: weakref.ReferenceType[T]):
            if item_id in self._items and self._items[item_id] is ref:
                # We need to confirm that this ref hasn't been replaced by another one,
                # which could happen if the id() was reused by Python right after the `item` was collected.
                del self._items[item_id]

        self._items[item_id] = weakref.ref(item, remove_item)

    def __contains__(self, item: T) -> bool:
        return id(item) in self._items and self._items[id(item)]() is item
