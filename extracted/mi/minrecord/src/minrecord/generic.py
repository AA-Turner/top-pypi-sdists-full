r"""Contain the generic record implementation."""

from __future__ import annotations

__all__ = ["Record"]

from collections import deque
from typing import TYPE_CHECKING, Any, TypeVar

from coola.equality import objects_are_equal
from coola.utils.format import str_indent, str_mapping

from minrecord.base import BaseRecord, EmptyRecordError
from minrecord.config import get_max_size

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T")


class Record(BaseRecord[T]):
    r"""Implement a generic record to store the recent values.

    Internally, this class uses a ``deque`` to keep the most recent
    values added in the record. Note that this class does not allow
    to get the best value because it is not possible to define a
    generic rule to know the best object. Please see
    ``ScalarRecord`` that can compute the best value for
    scalars.

    Args:
        name: The name of the record.
        elements: The initial elements in the record. Each element is a
            tuple with the step and its associated value.
        max_size: The maximum size of the record.

    Example:
        ```pycon
        >>> from minrecord import Record
        >>> record = Record(name="value", elements=((None, 64.0), (None, 42.0)))
        >>> record
        Record(name=value, max_size=10, size=2)
        >>> record.get_last_value()
        42.0
        >>> record.get_most_recent()
        ((None, 64.0), (None, 42.0))

        ```
    """

    def __init__(
        self,
        name: str,
        elements: Iterable[tuple[int | None, T]] = (),
        max_size: int = get_max_size(),
    ) -> None:
        super().__init__()
        self._name = name
        if max_size <= 0:
            msg = f"Record size must be greater than 0 (received: {max_size})"
            raise ValueError(msg)
        self._record = deque(elements, maxlen=max_size)

    def __len__(self) -> int:
        return len(self._record)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(name={self.name}, "
            f"max_size={self.max_size:,}, size={len(self):,})"
        )

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {"name": self.name, "max_size": self.max_size, "record": self.get_most_recent()}
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def name(self) -> str:
        return self._name

    @property
    def max_size(self) -> int:
        r"""The maximum size of the record."""
        return self._record.maxlen

    def add_value(self, value: T, step: int | None = None) -> None:
        self._record.append((step, value))

    def clone(self) -> Record[T]:
        return self.__class__(name=self.name, elements=self._record, max_size=self.max_size)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, Record):
            return False
        return objects_are_equal(self.to_dict(), other.to_dict())

    def get_last_value(self) -> Any:
        if self.is_empty():
            msg = f"'{self.name}' record is empty."
            raise EmptyRecordError(msg)
        return self._record[-1][1]

    def get_most_recent(self) -> tuple[tuple[int | None, T], ...]:
        return tuple(self._record)

    def is_comparable(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return not self._record

    def update(self, elements: Iterable[tuple[float | None, T]]) -> None:
        for step, value in elements:
            self.add_value(value, step)

    def config_dict(self) -> dict[str, Any]:
        config = super().config_dict()
        config["max_size"] = self.max_size
        return config

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        self._record = deque(state_dict["record"], maxlen=self.max_size)

    def state_dict(self) -> dict[str, Any]:
        return {"record": self.get_most_recent()}
