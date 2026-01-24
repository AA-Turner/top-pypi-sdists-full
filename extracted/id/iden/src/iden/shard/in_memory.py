r"""Contain in-memory shard implementations."""

from __future__ import annotations

__all__ = ["InMemoryShard"]

from typing import Any, TypeVar

from coola import objects_are_equal

from iden.shard.base import BaseShard

T = TypeVar("T")


class InMemoryShard(BaseShard[T]):
    r"""Implement an in-memory shard for transient data storage.

    This shard stores data directly in memory without persistence to disk.
    It does not have a valid URI as the data exists only during runtime.

    Example:
        ```pycon
        >>> from iden.shard import InMemoryShard
        >>> shard = InMemoryShard([1, 2, 3])
        >>> shard.get_data()
        [1, 2, 3]

        ```
    """

    def __init__(self, data: T) -> None:
        self._data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def clear(self) -> None:
        r"""Do nothing because it is an in-memory shard."""

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if type(other) is not type(self):
            return False
        return objects_are_equal(self._data, other._data, equal_nan=equal_nan)

    def get_data(self, cache: bool = False) -> T:  # noqa: ARG002
        return self._data

    def get_uri(self) -> str | None:
        return None

    def is_cached(self) -> bool:
        return True
