r"""Contain transformers to drop columns or rows with null values."""

from __future__ import annotations

__all__ = ["DropNullColumnTransformer", "DropNullRowTransformer"]

import logging
from itertools import compress
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_col_diff, str_kwargs, str_row_diff

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class DropNullColumnTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to remove the columns that have too many
    null values.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        threshold: The maximum percentage of null values to keep
            columns. If the proportion of null vallues is greater
            or equal to this threshold value, the column is removed.
            If set to ``1.0``, it removes all the columns that have
            only null values.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``cast``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import DropNullColumn
    >>> transformer = DropNullColumn()
    >>> transformer
    DropNullColumnTransformer(columns=None, threshold=1.0, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": ["2020-1-1", "2020-1-2", "2020-1-31", "2020-12-31", None],
    ...         "col2": [1, None, 3, None, 5],
    ...         "col3": [None, None, None, None, None],
    ...     }
    ... )
    >>> frame
    shape: (5, 3)
    ┌────────────┬──────┬──────┐
    │ col1       ┆ col2 ┆ col3 │
    │ ---        ┆ ---  ┆ ---  │
    │ str        ┆ i64  ┆ null │
    ╞════════════╪══════╪══════╡
    │ 2020-1-1   ┆ 1    ┆ null │
    │ 2020-1-2   ┆ null ┆ null │
    │ 2020-1-31  ┆ 3    ┆ null │
    │ 2020-12-31 ┆ null ┆ null │
    │ null       ┆ 5    ┆ null │
    └────────────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 2)
    ┌────────────┬──────┐
    │ col1       ┆ col2 │
    │ ---        ┆ ---  │
    │ str        ┆ i64  │
    ╞════════════╪══════╡
    │ 2020-1-1   ┆ 1    │
    │ 2020-1-2   ┆ null │
    │ 2020-1-31  ┆ 3    │
    │ 2020-12-31 ┆ null │
    │ null       ┆ 5    │
    └────────────┴──────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None = None,
        threshold: float = 1.0,
        ignore_missing: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(columns, ignore_missing)
        self._threshold = threshold
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, threshold={self._threshold}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:  # noqa: ARG002
        logger.info(
            f"Checking columns and dropping the columns that have too "
            f"many null values (threshold={self._threshold})..."
        )

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        if frame.is_empty():
            return frame
        columns = self.find_common_columns(frame)
        initial_shape = frame.shape
        pct = frame.select(columns).null_count() / frame.shape[0]
        cols = list(compress(pct.columns, (pct >= self._threshold).row(0)))
        logger.info(
            f"Dropping {len(cols):,} columns that have too "
            f"many null values (threshold={self._threshold})..."
        )
        logger.info(f"dropped columns: {cols}")
        out = frame.drop(cols)
        logger.info(
            f"DataFrame shape: {initial_shape} -> {out.shape} | "
            f"{str_col_diff(orig=initial_shape[1], final=out.shape[1])}"
        )
        return out


class DropNullRowTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to drop all rows that contain null
    values.

    Note that all the values in the row need to be null to drop the
    row.

    Args:
        columns: The columns to check. If set to ``None`` (default),
            use all columns.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import DropNullRow
    >>> transformer = DropNullRow()
    >>> transformer
    DropNullRowTransformer(columns=None, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": ["2020-1-1", "2020-1-2", "2020-1-31", "2020-12-31", None],
    ...         "col2": [1, None, 3, None, None],
    ...         "col3": [None, None, None, None, None],
    ...     }
    ... )
    >>> frame
    shape: (5, 3)
    ┌────────────┬──────┬──────┐
    │ col1       ┆ col2 ┆ col3 │
    │ ---        ┆ ---  ┆ ---  │
    │ str        ┆ i64  ┆ null │
    ╞════════════╪══════╪══════╡
    │ 2020-1-1   ┆ 1    ┆ null │
    │ 2020-1-2   ┆ null ┆ null │
    │ 2020-1-31  ┆ 3    ┆ null │
    │ 2020-12-31 ┆ null ┆ null │
    │ null       ┆ null ┆ null │
    └────────────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (4, 3)
    ┌────────────┬──────┬──────┐
    │ col1       ┆ col2 ┆ col3 │
    │ ---        ┆ ---  ┆ ---  │
    │ str        ┆ i64  ┆ null │
    ╞════════════╪══════╪══════╡
    │ 2020-1-1   ┆ 1    ┆ null │
    │ 2020-1-2   ┆ null ┆ null │
    │ 2020-1-31  ┆ 3    ┆ null │
    │ 2020-12-31 ┆ null ┆ null │
    └────────────┴──────┴──────┘

    ```
    """

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"ignore_missing={self._ignore_missing})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:  # noqa: ARG002
        logger.info("Dropping all rows that contain null values....")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        initial_shape = frame.shape
        out = frame.filter(~pl.all_horizontal(cs.by_name(columns).is_null()))
        logger.info(
            f"DataFrame shape: {initial_shape} -> {out.shape} | "
            f"{str_row_diff(orig=initial_shape[0], final=out.shape[0])}"
        )
        return out
