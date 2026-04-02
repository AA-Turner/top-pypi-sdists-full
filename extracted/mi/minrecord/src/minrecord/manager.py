r"""Contain a record manager implementation."""

from __future__ import annotations

__all__ = ["RecordManager"]

import copy
import logging
from typing import Any

from coola.utils.format import repr_indent, repr_mapping, str_indent, str_mapping

from minrecord.base import BaseRecord
from minrecord.functional import get_best_values
from minrecord.generic import Record

logger: logging.Logger = logging.getLogger(__name__)


class RecordManager:
    r"""Implement a simple record manager.

    This class proposes an approach to manage a group of records, but it
    is possible to use other approaches. If this class does not fit your
    needs, feel free to use another approach.

    Args:
        records: The initial records to add to the manager.

    Example:
        ```pycon
        >>> from minrecord import RecordManager, MinScalarRecord
        >>> manager = RecordManager()
        >>> manager.add_record(MinScalarRecord("loss"))
        >>> manager.get_record("loss")
        MinScalarRecord(name=loss, max_size=10, size=0)
        >>> manager.get_record("new_record")
        Record(name=new_record, max_size=10, size=0)

        ```
    """

    def __init__(self, records: dict[str, BaseRecord[Any]] | None = None) -> None:
        self._records = records or {}

    def __len__(self) -> int:
        return len(self._records)

    def __repr__(self) -> str:
        if self._records:
            return (
                f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(self._records))}\n)"
            )
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        if self._records:
            return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self._records))}\n)"
        return f"{self.__class__.__qualname__}()"

    def add_record(
        self, record: BaseRecord[Any], key: str | None = None, exist_ok: bool = False
    ) -> None:
        r"""Add a record to the manager.

        Args:
            record: The record to add to the manager.
            key: The key to store the record. If ``None``, the name
                of the record is used.
            exist_ok: If ``False``, ``RuntimeError`` is raised if the
                key already exists. This parameter should be set
                to ``True`` to overwrite the record for this key.

        Raises:
            RuntimeError: if a record is already registered for the
                key and ``exist_ok=False``.

        Example:
            ```pycon
            >>> from minrecord import RecordManager, MinScalarRecord
            >>> manager = RecordManager()
            >>> manager.add_record(MinScalarRecord("loss"))
            >>> manager
            RecordManager(
              (loss): MinScalarRecord(name=loss, max_size=10, size=0)
            )
            >>> manager.add_record(MinScalarRecord("loss"), "my key")
            >>> manager
            RecordManager(
              (loss): MinScalarRecord(name=loss, max_size=10, size=0)
              (my key): MinScalarRecord(name=loss, max_size=10, size=0)
            )

            ```
        """
        if key is None:
            key = record.name
        if key in self._records and not exist_ok:
            msg = (
                f"A record ({self._records[key]!r}) is already registered for the key "
                f"{key}. Please use `exist_ok=True` if you want to overwrite the "
                "record for this key"
            )
            raise RuntimeError(msg)
        self._records[key] = record

    def get_best_values(self, prefix: str = "", suffix: str = "") -> dict[str, Any]:
        r"""Get the best value of each metric.

        This method ignores the metrics with empty record and the
        non-comparable record.

        Args:
            prefix: The prefix used to create the dict of best values.
                The goal of this prefix is to generate a name which is
                different from the metric name to avoid confusion.
                By default, the returned dict uses the same name as the
                metric.
            suffix: The suffix used to create the dict of best values.
                The goal of this suffix is to generate a name which is
                different from the metric name to avoid confusion.
                By default, the returned dict uses the same name as the
                metric.

        Returns:
            The dict with the best value of each metric.

        Example:
            ```pycon
            >>> from minrecord import RecordManager, MaxScalarRecord
            >>> manager = RecordManager()
            >>> manager.add_record(MaxScalarRecord("accuracy"))
            >>> manager.get_record("accuracy").add_value(42.0)
            >>> manager.get_best_values()
            {'accuracy': 42.0}
            >>> manager.get_best_values(prefix="best/")
            {'best/accuracy': 42.0}
            >>> manager.get_best_values(suffix="/best")
            {'accuracy/best': 42.0}

            ```
        """
        return get_best_values(self._records, prefix=prefix, suffix=suffix)

    def get_record(self, key: str) -> BaseRecord[Any]:
        r"""Get the record associated to a key.

        Args:
            key: The key of the record to retrieve.

        Returns:
            The record if it exists, otherwise it returns an empty
                record. The created empty record is a ``Record``
                object.

        Example:
            ```pycon
            >>> from minrecord import RecordManager, MinScalarRecord
            >>> manager = RecordManager()
            >>> manager.add_record(MinScalarRecord("loss"))
            >>> manager.get_record("loss")
            MinScalarRecord(name=loss, max_size=10, size=0)
            >>> manager.get_record("new_record")
            Record(name=new_record, max_size=10, size=0)

            ```
        """
        if not self.has_record(key):
            self._records[key] = Record(name=key)
        return self._records[key]

    def get_records(self) -> dict[str, BaseRecord[Any]]:
        r"""Get all the records.

        Returns:
            The records with their associated keys.

        Example:
            ```pycon
            >>> from minrecord import RecordManager, MinScalarRecord
            >>> manager = RecordManager()
            >>> manager.add_record(MinScalarRecord("loss"))
            >>> manager.get_records()
            {'loss': MinScalarRecord(name=loss, max_size=10, size=0)}

            ```
        """
        return copy.copy(self._records)

    def has_record(self, key: str) -> bool:
        r"""Indicate if the engine has a record for the given key.

        Args:
            key: The key of the record to check.

        Returns:
            ``True`` if the record exists, ``False`` otherwise

        Example:
            ```pycon
            >>> from minrecord import RecordManager, MinScalarRecord
            >>> manager = RecordManager()
            >>> manager.add_record(MinScalarRecord("loss"))
            >>> manager.has_record("loss")
            True
            >>> manager.has_record("missing")
            False

            ```
        """
        return key in self._records

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Load the state values from a dict.

        Args:
            state_dict: A dict with the new state values.

        Example:
            ```pycon
            >>> from minrecord import RecordManager, Record
            >>> manager = RecordManager()
            >>> manager.add_record(Record("value"))
            >>> manager.load_state_dict({"value": {"state": {"record": ((0, 1), (1, 0.5), (2, 0.25))}}})
            >>> manager.get_record("value").get_last_value()
            0.25

            ```
        """
        for key, state in state_dict.items():
            if self.has_record(key):
                self._records[key].load_state_dict(state["state"])
            else:
                self._records[key] = BaseRecord.from_dict(state)

    def state_dict(self) -> dict[str, Any]:
        r"""Return a dictionary containing state values of all the
        records.

        Returns:
            The dictionary containing state values of all the records.

        Example:
            ```pycon
            >>> from minrecord import RecordManager
            >>> manager = RecordManager()
            >>> manager.state_dict()
            {}

            ```
        """
        return {key: hist.to_dict() for key, hist in self._records.items()}
