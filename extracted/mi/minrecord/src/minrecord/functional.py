r"""Contain functions to manipulate records."""

from __future__ import annotations

__all__ = ["get_best_values", "get_last_values"]

import contextlib
from typing import TYPE_CHECKING, Any

from minrecord.base import BaseRecord, EmptyRecordError

if TYPE_CHECKING:
    from collections.abc import Mapping


def get_best_values(
    records: Mapping[str, BaseRecord[Any]], prefix: str = "", suffix: str = ""
) -> dict[str, Any]:
    r"""Get the best value of each record.

    This function ignores the empty and non-comparable records.

    Args:
        records: The records and their associated keys.
        prefix: The prefix used to create the dict of best values.
            The goal of this prefix is to generate a name which is
            different from the record name to avoid confusion.
            By default, the returned dict uses the same name as the
            record.
        suffix: The suffix used to create the dict of best values.
            The goal of this suffix is to generate a name which is
            different from the record name to avoid confusion.
            By default, the returned dict uses the same name as the
            record.

    Returns:
        The dict with the best value of each record.

    Example:
        ```pycon
        >>> from minrecord import (
        ...     MinScalarRecord,
        ...     MaxScalarRecord,
        ...     get_best_values,
        ... )
        >>> record1 = MinScalarRecord.from_elements("loss", elements=[(None, 1.9), (None, 1.2)])
        >>> record2 = MaxScalarRecord.from_elements("accuracy", elements=[(None, 42), (None, 35)])
        >>> get_best_values({"loss": record1, "accuracy": record2})
        {'loss': 1.2, 'accuracy': 42}
        >>> get_best_values({"loss": record1, "accuracy": record2}, prefix="best/")
        {'best/loss': 1.2, 'best/accuracy': 42}
        >>> get_best_values({"loss": record1, "accuracy": record2}, suffix="/best")
        {'loss/best': 1.2, 'accuracy/best': 42}

        ```
    """
    values = {}
    for key, record in records.items():
        if record.is_comparable():
            with contextlib.suppress(EmptyRecordError):
                values[f"{prefix}{key}{suffix}"] = record.get_best_value()
    return values


def get_last_values(
    records: Mapping[str, BaseRecord[Any]], prefix: str = "", suffix: str = ""
) -> dict[str, Any]:
    r"""Get the last value of each record.

    This function ignores the empty records.

    Args:
        records: The records and their associated keys.
        prefix: The prefix used to create the dict of best values.
            The goal of this prefix is to generate a name which is
            different from the record name to avoid confusion.
            By default, the returned dict uses the same name as the
            record.
        suffix: The suffix used to create the dict of best values.
            The goal of this suffix is to generate a name which is
            different from the record name to avoid confusion.
            By default, the returned dict uses the same name as the
            record.

    Returns:
        The dict with the best value of each record.

    Example:
        ```pycon
        >>> from minrecord import (
        ...     MinScalarRecord,
        ...     MaxScalarRecord,
        ...     get_last_values,
        ... )
        >>> record1 = MinScalarRecord.from_elements("loss", elements=[(None, 1.9), (None, 1.2)])
        >>> record2 = MaxScalarRecord.from_elements("accuracy", elements=[(None, 42), (None, 35)])
        >>> get_last_values({"loss": record1, "accuracy": record2})
        {'loss': 1.2, 'accuracy': 35}
        >>> get_last_values({"loss": record1, "accuracy": record2}, prefix="last/")
        {'last/loss': 1.2, 'last/accuracy': 35}
        >>> get_last_values({"loss": record1, "accuracy": record2}, suffix="/last")
        {'loss/last': 1.2, 'accuracy/last': 35}

        ```
    """
    values = {}
    for key, record in records.items():
        with contextlib.suppress(EmptyRecordError):
            values[f"{prefix}{key}{suffix}"] = record.get_last_value()
    return values
