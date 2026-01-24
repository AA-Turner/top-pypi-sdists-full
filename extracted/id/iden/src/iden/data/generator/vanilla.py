r"""Contain simple data generator implementations."""

from __future__ import annotations

__all__ = ["DataGenerator"]

import copy
from typing import Any, TypeVar

from coola import objects_are_equal

from iden.data.generator.base import BaseDataGenerator

T = TypeVar("T")


class DataGenerator(BaseDataGenerator[T]):
    r"""Implement a simple data generator that wraps existing data.

    This generator provides a straightforward way to create data on demand
    by storing and optionally copying the data when requested.

    Args:
        data: The data to return.
        copy: If ``True``, it returns a copy of the data,
            otherwise it always returns the same data.

    Example:
        ```pycon
        >>> from iden.data.generator import DataGenerator
        >>> generator = DataGenerator([1, 2, 3])
        >>> generator
        DataGenerator(copy=False)
        >>> generator.generate()
        [1, 2, 3]

        ```
    """

    def __init__(self, data: T, copy: bool = False) -> None:
        self._data = data
        self._copy = bool(copy)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(copy={self._copy})"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if type(other) is not type(self):
            return False
        return (
            objects_are_equal(self._data, other._data, equal_nan=equal_nan)
            and self._copy == other._copy
        )

    def generate(self) -> T:
        data = self._data
        if self._copy:
            data = copy.deepcopy(data)
        return data
