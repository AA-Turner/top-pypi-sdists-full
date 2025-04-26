r"""Contain transformers to concatenate columns."""

from __future__ import annotations

__all__ = ["ConcatColumnsTransformer"]

import logging
from typing import TYPE_CHECKING

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class ConcatColumnsTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to concatenate columns into a new column.

    Args:
        columns: The columns to concatenate. The column should have
            the same type or compatible types.
        out_column: The output column.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import ConcatColumns
    >>> transformer = ConcatColumns(columns=["col1", "col2", "col3"], out_column="col")
    >>> transformer
    ConcatColumnsTransformer(columns=('col1', 'col2', 'col3'), out_column=col, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [11, 12, 13, 14, 15],
    ...         "col2": [21, 22, 23, 24, 25],
    ...         "col3": [31, 32, 33, 34, 35],
    ...         "col4": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ i64  ┆ i64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 11   ┆ 21   ┆ 31   ┆ a    │
    │ 12   ┆ 22   ┆ 32   ┆ b    │
    │ 13   ┆ 23   ┆ 33   ┆ c    │
    │ 14   ┆ 24   ┆ 34   ┆ d    │
    │ 15   ┆ 25   ┆ 35   ┆ e    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 5)
    ┌──────┬──────┬──────┬──────┬──────────────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 ┆ col          │
    │ ---  ┆ ---  ┆ ---  ┆ ---  ┆ ---          │
    │ i64  ┆ i64  ┆ i64  ┆ str  ┆ list[i64]    │
    ╞══════╪══════╪══════╪══════╪══════════════╡
    │ 11   ┆ 21   ┆ 31   ┆ a    ┆ [11, 21, 31] │
    │ 12   ┆ 22   ┆ 32   ┆ b    ┆ [12, 22, 32] │
    │ 13   ┆ 23   ┆ 33   ┆ c    ┆ [13, 23, 33] │
    │ 14   ┆ 24   ┆ 34   ┆ d    ┆ [14, 24, 34] │
    │ 15   ┆ 25   ┆ 35   ┆ e    ┆ [15, 25, 35] │
    └──────┴──────┴──────┴──────┴──────────────┘


    ```
    """

    def __init__(
        self,
        columns: Sequence[str],
        out_column: str,
        ignore_missing: bool = False,
    ) -> None:
        super().__init__(columns=columns, ignore_missing=ignore_missing)
        self._out_column = out_column

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"out_column={self._out_column}, ignore_missing={self._ignore_missing})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Concatenating {len(columns):,} columns to {self._out_column}...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select(pl.concat_list(cs.by_name(columns).alias(self._out_column)))
        )
