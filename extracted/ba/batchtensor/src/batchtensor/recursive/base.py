r"""Define the applier base class."""

from __future__ import annotations

__all__ = ["BaseApplier"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from batchtensor.recursive import ApplyState

T = TypeVar("T")


class BaseApplier(ABC, Generic[T]):
    r"""Define the base class to implement a recursive applier."""

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    @abstractmethod
    def apply(self, data: T, func: Callable, state: ApplyState) -> T:
        r"""Recursively apply a function on all the items in a nested
        data.

        Args:
            data: The input data.
            func: The function to apply on each item.
            state: The current state.

        Returns:
            The transformed data.
        """
