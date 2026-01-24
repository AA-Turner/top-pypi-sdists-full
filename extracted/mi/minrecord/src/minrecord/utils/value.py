r"""Contain utility functions to manage objects."""

from __future__ import annotations

__all__ = ["MutableValue"]

from typing import Generic, TypeVar

T = TypeVar("T")


class MutableValue(Generic[T]):
    r"""Implement a simple class to build a mutable object.

    Args:
        value: The initial value.

    Example:
        ```pycon
        >>> from minrecord.utils.value import MutableValue
        >>> value = MutableValue(10)
        >>> value.get_value()
        10
        >>> value.set_value(42)
        >>> value.get_value()
        42

        ```
    """

    def __init__(self, value: T) -> None:
        self._value = value

    def get_value(self) -> T:
        r"""Get the current value.

        Returns:
            The current value.
        """
        return self._value

    def set_value(self, value: T) -> None:
        r"""Set a new value.

        Args:
            value: The new value.
        """
        self._value = value
