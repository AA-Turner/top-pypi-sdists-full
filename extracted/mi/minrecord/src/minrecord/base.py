r"""Contain the base class to record values."""

from __future__ import annotations

__all__ = [
    "BaseRecord",
    "EmptyRecordError",
    "NotAComparableRecordError",
]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from coola.equality.tester import EqualEqualityTester, get_default_registry
from coola.utils.introspection import get_fully_qualified_name

from minrecord.utils.imports import check_objectory, is_objectory_available

if is_objectory_available():
    from objectory import OBJECT_TARGET, AbstractFactory
else:  # pragma: no cover
    from minrecord.utils.fallback.objectory import OBJECT_TARGET, AbstractFactory


if TYPE_CHECKING:
    from collections.abc import Iterable


T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class BaseRecord(ABC, Generic[T], metaclass=AbstractFactory):
    r"""Define the base class to implement a record.

    The record tracks the value added as well as the step
    when the value is added. The goal of this class is to track the
    recent record because the loggers (e.g. MLFlow or Tensorboard)
    do not allow to get the last value or the best value. The record
    keeps in memory a recent record of pairs (step, value)
    where step is the index of the step when the value was added. The
    length of the recent record depends on the concrete
    implementation.

    To implement your own record, you will need to define the
    following methods:

        - ``add_value``
        - ``get_last_value``
        - ``get_most_recent``
        - ``is_comparable``
        - ``is_empty``
        - ``update``
        - ``load_state_dict``
        - ``state_dict``

    If it is a comparable record, you will need to implement
    the following methods too:

        - ``_get_best_value``
        - ``_has_improved``

    You may also need to extend the ``config_dict`` method.

    Example:
        ```pycon
        >>> from minrecord import Record
        >>> record = Record("loss")
        >>> record.add_value(value=2, step=0)
        >>> record.add_value(value=1.2, step=1)
        >>> record.get_last_value()
        1.2

        ```
    """

    @property
    @abstractmethod
    def name(self) -> str:
        r"""The name of the record."""

    @abstractmethod
    def add_value(self, value: T, step: float | None = None) -> None:
        r"""Add a new value to the record.

        Args:
            value: The value to add to the record.
            step: The step value to record. ``None`` means there is no
                step to track.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.add_value(value=2)
            >>> record.add_value(value=42, step=1)
            >>> record
            Record(name=loss, max_size=10, size=2)

            ```
        """

    @abstractmethod
    def clone(self) -> BaseRecord[T]:
        r"""Clone the current record.

        Returns:
            A copy of the current record.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record_cloned = record.clone()
            >>> record_cloned
            Record(name=loss, max_size=10, size=0)

            ```
        """

    @abstractmethod
    def equal(self, other: Any) -> bool:
        r"""Indicate if two records are equal or not.

        Args:
            other: The object to compare.

        Returns:
            ``True`` if the records are equal, ``False`` otherwise.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record1 = Record("loss")
            >>> record2 = Record("accuracy")
            >>> record3 = Record("loss")
            >>> record1.equal(record2)
            False
            >>> record1.equal(record1)
            True

            ```
        """

    def get_best_value(self) -> T:
        r"""Get the best value of this record.

        It is possible to get the best value only if it is a
        comparable record i.e. it is possible to compare the
        values in the record.

        Returns:
            The best value of this record.

        Raises:
            NotAComparableRecord: if it is not a comparable record.
            EmptyRecordError: if the record is empty

        Example:
            ```pycon
            >>> from minrecord import MaxScalarRecord
            >>> record = MaxScalarRecord("accuracy")
            >>> record.add_value(value=2, step=0)
            >>> record.add_value(value=4, step=1)
            >>> record.get_best_value()
            4

            ```
        """
        if not self.is_comparable():
            msg = (
                "It is not possible to get the best value because it is not possible to compare "
                f"the values in {self.name} record"
            )
            raise NotAComparableRecordError(msg)
        return self._get_best_value()

    def _get_best_value(self) -> T:
        r"""Get the best value of this record.

        You need to implement this method for a comparable record.

        Returns:
            The best value of this record.

        Raises:
            NotImplementedError: if this method is not implemented.
        """
        msg = "_get_best_value method is not implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def get_last_value(self) -> T:
        r"""Get the last value.

        Returns:
            The last value added in the record.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.add_value(value=2, step=0)
            >>> record.add_value(value=1.2, step=1)
            >>> record.get_last_value()
            1.2
            >>> record.add_value(value=0.8, step=1)
            >>> record.get_last_value()
            0.8

            ```
        """

    @abstractmethod
    def get_most_recent(self) -> tuple[tuple[float | None, T], ...]:
        r"""Get the tuple of recent values and their associated steps.

        The last value in the tuple is the last value added to the
        record. The length of the recent record depends on the
        concrete implementation.

        Returns:
            A tuple of the recent values in the record.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.add_value(value=2)
            >>> record.add_value(value=1.2, step=1)
            >>> record.add_value(value=0.8, step=2)
            >>> record.get_most_recent()
            ((None, 2), (1, 1.2), (2, 0.8))

            ```
        """

    def has_improved(self) -> bool:
        r"""Indicate if the last value is the best value.

        It is possible to use this method only if it is a comparable
        record i.e. it is possible to compare the values in
        the record.

        Returns:
            ``True`` if the last value is the best value,
                otherwise ``False``.

        Raises:
            NotAComparableRecord: if it is not a comparable record.
            EmptyRecordError: if the record is empty

        Example:
            ```pycon
            >>> from minrecord import MaxScalarRecord
            >>> record = MaxScalarRecord("accuracy")
            >>> record.add_value(value=2, step=0)
            >>> record.add_value(value=4, step=1)
            >>> record.has_improved()
            True

            ```
        """
        if not self.is_comparable():
            msg = (
                "It is not possible to indicate if the last value is the best value because it "
                f"is not possible to compare the values in {self.name} record"
            )
            raise NotAComparableRecordError(msg)
        return self._has_improved()

    def _has_improved(self) -> bool:
        r"""Indicate if the last value is the best value.

        You need to implement this method for a comparable record.

        Returns:
            ``True`` if the last value is the best value,
                otherwise ``False``.

        Raises:
            NotImplementedError: if this method is not implemented
        """
        msg = "_has_improved method is not implemented"
        raise NotImplementedError(msg)

    @abstractmethod
    def is_comparable(self) -> bool:
        r"""Indicate if it is possible to compare the values in the
        record.

        Note that it is possible to compute the best value only for
        records that are comparable.

        Returns:
            ``True`` if it is possible to compare the values in
                the record, otherwise ``False``.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.is_comparable()
            False

            ```
        """

    @abstractmethod
    def is_empty(self) -> bool:
        r"""Indicate if the record is empty or not.

        Returns:
            ``True`` if the record is empty, otherwise ``False``.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.is_empty()
            True

            ```
        """

    @abstractmethod
    def update(self, elements: Iterable[tuple[float | None, T]]) -> None:
        r"""Update the record by adding the elements.

        Args:
            elements: The elements to add to the record.  Each tuple
                has the following structure ``(step, value)``.
                The step can be ``None`` if there is no step.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.update([(0, 42), (1, 45)])
            >>> record
            Record(name=loss, max_size=10, size=2)

            ```
        """

    def config_dict(self) -> dict[str, Any]:
        r"""Get the config of the record.

        The config dictionary should contain all the values necessary
        to instantiate a record with the same parameters
        with the  ``factory`` method. It is expected to contain values
        like the full name of the class and the arguments of the
        constructor. This dictionary should not contain the state
        values. It is possible to get the state values with the
        ``state_dict`` method.

        Returns:
            The config of the record.

        Example:
            ```pycon
            >>> from minrecord import BaseRecord, Record
            >>> config = Record("loss").config_dict()
            >>> record = BaseRecord.factory(**config)  # Note that the state is not copied.
            >>> record
            Record(name=loss, max_size=10, size=0)

            ```
        """
        return {OBJECT_TARGET: get_fully_qualified_name(self.__class__), "name": self.name}

    @abstractmethod
    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Set up the record from a dictionary containing the state
        values.

        Args:
            state_dict: A dictionary containing state keys with values.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.load_state_dict({"record": ((0, 42.0),)})
            >>> record.get_last_value()
            42.0

            ```
        """

    @abstractmethod
    def state_dict(self) -> dict[str, Any]:
        r"""Get a dictionary containing the state values of the record.

        Returns:
            The state values in a dict.

        Example:
            ```pycon
            >>> from minrecord import Record
            >>> record = Record("loss")
            >>> record.add_value(42.0, step=0)
            >>> state = record.state_dict()
            >>> state
            {'record': ((0, 42.0),)}

            ```
        """

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BaseRecord[T]:
        r"""Instantiate a record from a dictionary.

        Args:
            data: The dictionary that is used to instantiate the
                record. The dictionary is expected to contain the
                parameters to create instantiate the record and the
                state of the record.

        Returns:
            The instantiated record.

        Example:
            ```pycon
            >>> from minrecord import BaseRecord
            >>> from objectory import OBJECT_TARGET
            >>> record = BaseRecord.from_dict(
            ...     {
            ...         "config": {
            ...             OBJECT_TARGET: "minrecord.Record",
            ...             "name": "loss",
            ...             "max_size": 7,
            ...         },
            ...         "state": {"record": ((0, 1), (1, 5))},
            ...     }
            ... )
            >>> record
            Record(name=loss, max_size=7, size=2)

            ```
        """
        check_objectory()
        obj = cls.factory(**data["config"])
        obj.load_state_dict(data["state"])
        return obj

    def to_dict(self) -> dict[str, Any]:
        r"""Export the current record to a dictionary.

        This method exports all the information to re-create the
        record with the same state. The returned dictionary
        can be used as input of the ``from_dict`` method to resume the
        record.

        Returns:
            A dictionary with the config and the state of the
                record.

        Example:
            ```pycon
            >>> from minrecord import BaseRecord, Record
            >>> record_dict = Record("loss").to_dict()
            >>> record = BaseRecord.from_dict(record_dict)
            >>> record
            Record(name=loss, max_size=10, size=0)

            ```
        """
        return {"config": self.config_dict(), "state": self.state_dict()}


class EmptyRecordError(Exception):
    r"""Raise an error if the record is empty."""


class NotAComparableRecordError(Exception):
    r"""Raise an error if it is not possible to compare the values in
    the record."""


get_default_registry().register(BaseRecord, EqualEqualityTester(), exist_ok=True)
