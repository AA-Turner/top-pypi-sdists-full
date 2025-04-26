r"""Contain ``polars.DataFrame`` transformers to select columns in
DataFrames."""

from __future__ import annotations

__all__ = ["ColumnSelectionTransformer"]

import logging
from typing import TYPE_CHECKING

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.column import find_common_columns
from grizz.utils.format import str_col_diff

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl


logger = logging.getLogger(__name__)


class ColumnSelectionTransformer(BaseColumnsTransformer):
    r"""Implement a ``polars.DataFrame`` transformer to select a subset
    of columns.

    Args:
        columns: The columns to keep.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise a warning message is shown.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import ColumnSelection
    >>> transformer = ColumnSelection(columns=["col1", "col2"])
    >>> transformer
    ColumnSelectionTransformer(columns=('col1', 'col2'), ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": ["2020-1-1", "2020-1-2", "2020-1-31", "2020-12-31", None],
    ...         "col2": [1, 2, 3, 4, 5],
    ...         "col3": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> out = transformer.transform(frame)
    >>> out
        shape: (5, 2)
    ┌────────────┬──────┐
    │ col1       ┆ col2 │
    │ ---        ┆ ---  │
    │ str        ┆ i64  │
    ╞════════════╪══════╡
    │ 2020-1-1   ┆ 1    │
    │ 2020-1-2   ┆ 2    │
    │ 2020-1-31  ┆ 3    │
    │ 2020-12-31 ┆ 4    │
    │ null       ┆ 5    │
    └────────────┴──────┘

    ```
    """

    def __init__(self, columns: Sequence[str], ignore_missing: bool = False) -> None:
        super().__init__(columns, ignore_missing)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"ignore_missing={self._ignore_missing})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Selecting {len(columns):,} columns...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = find_common_columns(frame, self._columns)
        initial_shape = frame.shape
        out = frame.select(columns)
        logger.info(
            f"DataFrame shape: {initial_shape} -> {out.shape} | "
            f"{str_col_diff(orig=initial_shape[1], final=out.shape[1])}"
        )
        return out
