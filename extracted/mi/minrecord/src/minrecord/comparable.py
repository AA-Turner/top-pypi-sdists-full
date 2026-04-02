r"""Contain the comparable record implementations."""

from __future__ import annotations

__all__ = ["ComparableRecord", "MaxScalarRecord", "MinScalarRecord"]

from numbers import Number
from typing import TYPE_CHECKING, Any, TypeVar

from coola.utils.format import str_indent, str_mapping

from minrecord.base import EmptyRecordError
from minrecord.comparator import (
    BaseComparator,
    MaxScalarComparator,
    MinScalarComparator,
)
from minrecord.generic import Record

if TYPE_CHECKING:
    import sys
    from collections.abc import Iterable

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

T = TypeVar("T")


class ComparableRecord(Record[T]):
    r"""Implement a record of comparable values.

    Args:
        name: The name of the record.
        comparator: The comparator to use to find the best value.
        elements: The initial elements. Each element is a tuple with
            the step and its associated value.
        max_size: The maximum number of elements to store in the record.
        best_value: The initial best value. If ``None``, the initial
            best value of the ``comparator`` is used.
        improved: Indicate if the last value is the best value or not.

    Example:
        ```pycon
        >>> from minrecord import ComparableRecord
        >>> from minrecord.comparator import MaxScalarComparator
        >>> record = ComparableRecord("value", MaxScalarComparator())
        >>> record.add_value(64.0)
        >>> record.add_value(42.0)
        >>> record.get_last_value()
        42.0
        >>> record.get_most_recent()
        ((None, 64.0), (None, 42.0))
        >>> record.get_best_value()
        64.0

        ```
    """

    def __init__(
        self,
        name: str,
        comparator: BaseComparator[T],
        elements: Iterable[tuple[int | None, T]] = (),
        max_size: int = 10,
        best_value: T | None = None,
        improved: bool = False,
    ) -> None:
        super().__init__(name=name, elements=elements, max_size=max_size)
        self._comparator = comparator
        self._best_value = best_value or self._comparator.get_initial_best_value()
        self._improved = bool(improved)

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "name": self.name,
                    "max_size": self.max_size,
                    "comparator": self._comparator,
                    "best_value": self._best_value,
                    "improved": self._improved,
                    "record": self.get_most_recent(),
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def add_value(self, value: T, step: int | None = None) -> None:
        self._improved = self.is_better(new_value=value, old_value=self._best_value)
        if self._improved:
            self._best_value = value
        super().add_value(value, step)

    def clone(self) -> ComparableRecord[T]:
        return self.__class__(
            name=self.name,
            elements=self._record,
            max_size=self.max_size,
            comparator=self._comparator,
            best_value=self._best_value,
            improved=self._improved,
        )

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
            >>> from minrecord import ComparableRecord
            >>> from minrecord.comparator import MaxScalarComparator
            >>> record = ComparableRecord("accuracy", MaxScalarComparator())
            >>> record.is_better(new_value=1, old_value=0)
            True
            >>> record.is_better(new_value=0, old_value=1)
            False

            ```
        """
        return self._comparator.is_better(new_value=new_value, old_value=old_value)

    def _get_best_value(self) -> T:
        if self.is_empty():
            msg = "The record is empty so it is not possible to get the best value."
            raise EmptyRecordError(msg)
        return self._best_value

    def _has_improved(self) -> bool:
        if self.is_empty():
            msg = "The record is empty."
            raise EmptyRecordError(msg)
        return self._improved

    def is_comparable(self) -> bool:
        return True

    def config_dict(self) -> dict[str, Any]:
        config = super().config_dict()
        config["max_size"] = self.max_size
        config["comparator"] = self._comparator
        return config

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        super().load_state_dict(state_dict)
        self._improved = state_dict["improved"]
        self._best_value = state_dict["best_value"]

    def state_dict(self) -> dict[str, Any]:
        state = super().state_dict()
        state.update({"improved": self._improved, "best_value": self._best_value})
        return state

    @classmethod
    def from_elements(
        cls, name: str, comparator: BaseComparator[T], elements: Iterable[tuple[float | None, T]]
    ) -> Self:
        record = cls(name=name, comparator=comparator)
        record.update(elements)
        return record


class MaxScalarRecord(ComparableRecord[Number]):
    r"""A specific implementation to track the max value of a scalar
    record.

    This record uses the ``MaxScalarComparator`` to find the
    best value of the record.

    Args:
        name: The name of the record.
        elements: The initial elements. Each element is a tuple with
            the step and its associated value.
        max_size: The maximum number of elements to store inthe record.
        best_value: The initial best value. If ``None``, the initial
            best value of the ``comparator`` is used.
        improved: Indicate if the last value is the best value or not.

    Example:
        ```pycon
        >>> from minrecord import MaxScalarRecord
        >>> record = MaxScalarRecord("value")
        >>> record.add_value(64.0)
        >>> record.add_value(42.0)
        >>> record.get_most_recent()
        ((None, 64.0), (None, 42.0))
        >>> record.get_last_value()
        42.0
        >>> record.get_best_value()
        64.0

        ```
    """

    def __init__(
        self,
        name: str,
        elements: Iterable[tuple[int | None, T]] = (),
        max_size: int = 10,
        best_value: T | None = None,
        improved: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            comparator=MaxScalarComparator(),
            elements=elements,
            max_size=max_size,
            best_value=best_value,
            improved=improved,
        )

    def config_dict(self) -> dict[str, Any]:
        config = super().config_dict()
        del config["comparator"]
        return config

    @classmethod
    def from_elements(cls, name: str, elements: Iterable[tuple[float | None, T]]) -> Self:
        r"""Instantiate a ``MaxScalarRecord`` object from the elements.

        Args:
            name: The name of the record.
            elements: The initial elements. Each element is a tuple with
                the step and its associated value.

        Returns:
            The instantiated record.

        Example:
            ```pycon
            >>> from minrecord import MaxScalarRecord
            >>> record = MaxScalarRecord.from_elements("value", ((None, 64.0), (None, 42.0)))
            >>> record.get_most_recent()
            ((None, 64.0), (None, 42.0))
            >>> record.get_last_value()
            42.0
            >>> record.get_best_value()
            64.0

            ```
        """
        record = cls(name)
        record.update(elements)
        return record


class MinScalarRecord(ComparableRecord[Number]):
    r"""A specific implementation to track the min value of a scalar
    record.

    This record uses the ``MinScalarComparator`` to find the
    best value of the record.

    Args:
        name: The name of the record.
        elements: The initial elements. Each element is a tuple with
            the step and its associated value.
        max_size: The maximum number of elements to store inthe record.
        best_value: The initial best value. If ``None``, the initial
            best  value of the ``comparator`` is used.
        improved: Indicate if the last value is the best value or not.

    Example:
        ```pycon
        >>> from minrecord import MinScalarRecord
        >>> record = MinScalarRecord("value")
        >>> record.add_value(64.0)
        >>> record.add_value(42.0)
        >>> record.get_most_recent()
        ((None, 64.0), (None, 42.0))
        >>> record.get_last_value()
        42.0
        >>> record.get_best_value()
        42.0

        ```
    """

    def __init__(
        self,
        name: str,
        elements: Iterable[tuple[int | None, T]] = (),
        max_size: int = 10,
        best_value: T | None = None,
        improved: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            comparator=MinScalarComparator(),
            elements=elements,
            max_size=max_size,
            best_value=best_value,
            improved=improved,
        )

    def config_dict(self) -> dict[str, Any]:
        config = super().config_dict()
        del config["comparator"]
        return config

    @classmethod
    def from_elements(cls, name: str, elements: Iterable[tuple[float | None, T]]) -> Self:
        r"""Instantiate a ``MaxScalarRecord`` object from the elements.

        Args:
            name: The name of the record.
            elements: The initial elements. Each element is a tuple with
                the step and its associated value.

        Returns:
            The instantiated record.

        Example:
            ```pycon
            >>> from minrecord import MinScalarRecord
            >>> record = MinScalarRecord.from_elements("value", ((None, 64.0), (None, 42.0)))
            >>> record.get_most_recent()
            ((None, 64.0), (None, 42.0))
            >>> record.get_last_value()
            42.0
            >>> record.get_best_value()
            42.0

            ```
        """
        record = cls(name)
        record.update(elements)
        return record
