r"""Contain simple data generator implementations."""

from __future__ import annotations

__all__ = ["DataGenerator"]

import copy
from typing import TypeVar

from iden.data.generator.base import BaseDataGenerator

T = TypeVar("T")


class DataGenerator(BaseDataGenerator[T]):
    r"""Implement a simple data generator.

    Args:
        data: The data to return.
        copy: If ``True``, it returns a copy of the data,
            otherwise it always returns the same data.

    Example usage:

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

    def generate(self) -> T:
        data = self._data
        if self._copy:
            data = copy.deepcopy(data)
        return data
