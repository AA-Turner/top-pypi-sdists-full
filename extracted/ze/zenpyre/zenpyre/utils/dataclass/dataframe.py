r"""Provide a generic utility to convert a list of dataclass instances
into a Polars DataFrame."""

from __future__ import annotations

__all__ = ["dataclasses_to_dataframe"]

import logging
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any

from coola.utils.imports import is_polars_available

if TYPE_CHECKING or is_polars_available():
    import polars as pl
else:  # pragma: no cover
    from coola.utils.fallback.polars import polars as pl

logger: logging.Logger = logging.getLogger(__name__)


def dataclasses_to_dataframe(items: list[Any]) -> pl.DataFrame:
    """Convert a list of dataclass instances into a Polars DataFrame.

    Serialises each item to a dict via :func:`dataclasses.asdict` and
    builds a :class:`polars.DataFrame` from the resulting list of
    dicts. Works with any dataclass type, including frozen
    dataclasses, as long as all field values are compatible with
    Polars' type inference.

    Args:
        items: The list of dataclass instances to convert.

    Returns:
        A ``polars.DataFrame`` with one row per item and one column
        per field.

    Raises:
        TypeError: If any item in ``items`` is not a dataclass
            instance.

    Example:
        ```pycon
        >>> from dataclasses import dataclass
        >>> from zenpyre.utils.dataclass import dataclasses_to_dataframe
        >>> @dataclass(frozen=True)
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> frame = dataclasses_to_dataframe([Point(1, 2), Point(3, 4)])
        >>> frame
        shape: (2, 2)
        ┌─────┬─────┐
        │ x   ┆ y   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 2   │
        │ 3   ┆ 4   │
        └─────┴─────┘

        ```
    """
    for item in items:
        if not is_dataclass(item):
            msg = f"All items must be dataclass instances, got {type(item)}"
            raise TypeError(msg)

    logger.debug("Converting %s items to a DataFrame...", f"{len(items):,}")
    data = [asdict(item) for item in items]
    frame = pl.DataFrame(data)
    logger.debug("Converted %s items to a DataFrame with shape %s", f"{len(items):,}", frame.shape)
    return frame
