import sys
from typing import Any


class _FrozenDict(dict):
    """A JSON object that can be safely shared through ordinary Python APIs."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self._immutable()

    def _immutable(self, *args, **kwargs):
        raise TypeError("Statsig cached evaluation values are immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    __ior__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce_ex__(self, protocol):
        return _restore_frozen_dict, (list(self.items()),)


class _FrozenList(list):
    """A JSON array that can be safely shared through ordinary Python APIs."""

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self._immutable()

    def _immutable(self, *args, **kwargs):
        raise TypeError("Statsig cached evaluation values are immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    __iadd__ = _immutable
    __imul__ = _immutable
    append = _immutable
    clear = _immutable
    extend = _immutable
    insert = _immutable
    pop = _immutable
    remove = _immutable
    reverse = _immutable
    sort = _immutable

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce_ex__(self, protocol):
        return _restore_frozen_list, (list(self),)


def _restore_frozen_dict(items: list[tuple[Any, Any]]) -> _FrozenDict:
    frozen = _FrozenDict()
    for key, value in items:
        dict.__setitem__(frozen, key, value)
    return frozen


def _restore_frozen_list(items: list[Any]) -> _FrozenList:
    frozen = _FrozenList()
    for item in items:
        list.append(frozen, item)
    return frozen


def _deep_freeze_and_measure(value: Any) -> tuple[Any, int]:
    """Copy a JSON tree into read-only containers and measure retained bytes."""

    seen_scalars: set[int] = set()

    def freeze(item: Any) -> tuple[Any, int]:
        if isinstance(item, dict):
            frozen_dict = _FrozenDict()
            size = 0
            for key, child in item.items():
                frozen_child, child_size = freeze(child)
                dict.__setitem__(frozen_dict, key, frozen_child)
                size += child_size

                key_id = id(key)
                if key_id not in seen_scalars:
                    seen_scalars.add(key_id)
                    size += sys.getsizeof(key)
            return frozen_dict, size + sys.getsizeof(frozen_dict)

        if isinstance(item, list):
            frozen_list = _FrozenList()
            size = 0
            for child in item:
                frozen_child, child_size = freeze(child)
                list.append(frozen_list, frozen_child)
                size += child_size
            return frozen_list, size + sys.getsizeof(frozen_list)

        item_id = id(item)
        if item_id in seen_scalars:
            return item, 0
        seen_scalars.add(item_id)
        return item, sys.getsizeof(item)

    return freeze(value)
