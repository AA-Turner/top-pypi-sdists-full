r"""Contain the comparator base class and some implementations."""

from __future__ import annotations

__all__ = [
    "BaseComparator",
    "MaxScalarComparator",
    "MinScalarComparator",
]

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from coola.equality.tester import EqualEqualityTester, get_default_registry

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class BaseComparator(ABC, Generic[T]):
    r"""Define the base comparator class to implement a comparator.

    Example:
        ```pycon
        >>> from minrecord import MinScalarComparator
        >>> comparator = MinScalarComparator()
        >>> comparator.is_better(old_value=0.4, new_value=0.6)
        False
        >>> comparator.get_initial_best_value()
        inf

        ```
    """

    @abstractmethod
    def equal(self, other: Any) -> bool:
        r"""Indicate if two comparators are equal or not.

        Args:
            other: The other object to compare with.

        Returns:
            ``True`` if the comparators are equal, ``False`` otherwise.

        Example:
            ```pycon
            >>> from minrecord import MinScalarComparator, MaxScalarComparator
            >>> comparator = MinScalarComparator()
            >>> comparator.equal(MinScalarComparator())
            True
            >>> comparator.equal(MaxScalarComparator())
            False

            ```
        """

    @abstractmethod
    def get_initial_best_value(self) -> T:
        r"""Get the initial best value.

        Returns:
            The initial best value.

        Example:
            ```pycon
            >>> from minrecord import MinScalarComparator
            >>> comparator = MinScalarComparator()
            >>> comparator.get_initial_best_value()
            inf

            ```
        """

    @abstractmethod
    def is_better(self, old_value: T, new_value: T) -> bool:
        r"""Indicate if the new value is better than the old value.

        Args:
            old_value: The old value to compare.
            new_value: The new value to compare.

        Returns:
            ``True`` if the new value is better than the old value,
                otherwise ``False``.

        Example:
            ```pycon
            >>> from minrecord import MinScalarComparator
            >>> comparator = MinScalarComparator()
            >>> comparator.is_better(old_value=0.4, new_value=0.6)
            False

            ```
        """


class MaxScalarComparator(BaseComparator[float]):
    r"""Implement a max comparator for scalar value.

    This comparator can be used to find the maximum value between two
    scalar values.

    Example:
        ```pycon
        >>> from minrecord import MaxScalarComparator
        >>> comparator = MaxScalarComparator()
        >>> comparator.is_better(old_value=0.4, new_value=0.6)
        True
        >>> comparator.get_initial_best_value()
        -inf

        ```
    """

    def equal(self, other: Any) -> bool:
        return isinstance(other, MaxScalarComparator)

    def get_initial_best_value(self) -> float:
        return -float("inf")

    def is_better(self, old_value: float, new_value: float) -> bool:
        return old_value <= new_value


class MinScalarComparator(BaseComparator[float]):
    r"""Implementation of a min comparator for scalar value.

    This comparator can be used to find the minimum value between two
    scalar values.

    Example:
        ```pycon
        >>> from minrecord import MinScalarComparator
        >>> comparator = MinScalarComparator()
        >>> comparator.is_better(old_value=0.4, new_value=0.6)
        False
        >>> comparator.get_initial_best_value()
        inf

        ```
    """

    def equal(self, other: Any) -> bool:
        return isinstance(other, MinScalarComparator)

    def get_initial_best_value(self) -> float:
        return float("inf")

    def is_better(self, old_value: float, new_value: float) -> bool:
        return new_value <= old_value


get_default_registry().register(BaseComparator, EqualEqualityTester(), exist_ok=True)
