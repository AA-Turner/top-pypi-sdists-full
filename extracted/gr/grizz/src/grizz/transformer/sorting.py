r"""Contain ``polars.DataFrame`` transformers to sort the DataFrame."""

from __future__ import annotations

__all__ = ["SortColumnsTransformer", "SortTransformer"]

import logging
from typing import TYPE_CHECKING, Any

from grizz.transformer.base import BaseTransformer

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl


class SortTransformer(BaseTransformer):
    r"""Implement a transformer to sort the DataFrame by the given
    columns.

    Args:
        columns: The columns to convert.
        *args: The positional arguments to pass to ``sort``.
        **kwargs: The keyword arguments to pass to ``sort``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import Sort
    >>> transformer = Sort(columns=["col3", "col1"])
    >>> transformer
    SortTransformer(columns=('col3', 'col1'))
    >>> frame = pl.DataFrame(
    ...     {"col1": [1, 2, None], "col2": [6.0, 5.0, 4.0], "col3": ["a", "c", "b"]}
    ... )
    >>> frame
    shape: (3, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ 6.0  ┆ a    │
    │ 2    ┆ 5.0  ┆ c    │
    │ null ┆ 4.0  ┆ b    │
    └──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (3, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ 6.0  ┆ a    │
    │ null ┆ 4.0  ┆ b    │
    │ 2    ┆ 5.0  ┆ c    │
    └──────┴──────┴──────┘

    ```
    """

    def __init__(self, columns: Sequence[str], *args: Any, **kwargs: Any) -> None:
        self._columns = tuple(columns)
        self._args = args
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(columns={self._columns})"

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        logger.info(f"Sorting rows based on the columns: {self._columns}")
        return frame.sort(self._columns, *self._args, **self._kwargs)


class SortColumnsTransformer(BaseTransformer):
    r"""Implement a transformer to sort the DataFrame columns by name.

    Args:
        reverse: If set to ``False``, then the columns are sorted by
            alphabetical order.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import SortColumns
    >>> transformer = SortColumns()
    >>> transformer
    SortColumnsTransformer(reverse=False)
    >>> frame = pl.DataFrame(
    ...     {"col2": [1, 2, None], "col3": [6.0, 5.0, 4.0], "col1": ["a", "c", "b"]}
    ... )
    >>> frame
    shape: (3, 3)
    ┌──────┬──────┬──────┐
    │ col2 ┆ col3 ┆ col1 │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ 6.0  ┆ a    │
    │ 2    ┆ 5.0  ┆ c    │
    │ null ┆ 4.0  ┆ b    │
    └──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (3, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ str  ┆ i64  ┆ f64  │
    ╞══════╪══════╪══════╡
    │ a    ┆ 1    ┆ 6.0  │
    │ c    ┆ 2    ┆ 5.0  │
    │ b    ┆ null ┆ 4.0  │
    └──────┴──────┴──────┘

    ```
    """

    def __init__(self, reverse: bool = False) -> None:
        self._reverse = reverse

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(reverse={self._reverse})"

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        logger.info("Sorting columns")
        return frame.select(sorted(frame.columns, reverse=self._reverse))
