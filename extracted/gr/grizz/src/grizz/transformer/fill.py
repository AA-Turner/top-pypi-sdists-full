r"""Contain transformers to fill values."""

from __future__ import annotations

__all__ = ["FillNanTransformer", "FillNullTransformer"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_kwargs

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class FillNanTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to fill NaN values.

    Args:
        columns: The columns to prepare. If ``None``, it processes all
            the columns of type string.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``fill_nan``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import FillNan
    >>> transformer = FillNan(columns=["col1", "col4"], value=100)
    >>> transformer
    FillNanTransformer(columns=('col1', 'col4'), ignore_missing=False, value=100)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, None],
    ...         "col2": [1.2, 2.2, 3.2, 4.2, float("nan")],
    ...         "col3": ["a", "b", "c", "d", None],
    ...         "col4": [1.2, float("nan"), 3.2, None, 5.2],
    ...     }
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ str  ┆ f64  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1.2  ┆ a    ┆ 1.2  │
    │ 2    ┆ 2.2  ┆ b    ┆ NaN  │
    │ 3    ┆ 3.2  ┆ c    ┆ 3.2  │
    │ 4    ┆ 4.2  ┆ d    ┆ null │
    │ null ┆ NaN  ┆ null ┆ 5.2  │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬───────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4  │
    │ ---  ┆ ---  ┆ ---  ┆ ---   │
    │ i64  ┆ f64  ┆ str  ┆ f64   │
    ╞══════╪══════╪══════╪═══════╡
    │ 1    ┆ 1.2  ┆ a    ┆ 1.2   │
    │ 2    ┆ 2.2  ┆ b    ┆ 100.0 │
    │ 3    ┆ 3.2  ┆ c    ┆ 3.2   │
    │ 4    ┆ 4.2  ┆ d    ┆ null  │
    │ null ┆ NaN  ┆ null ┆ 5.2   │
    └──────┴──────┴──────┴───────┘

    ```
    """

    def __init__(
        self, columns: Sequence[str] | None = None, ignore_missing: bool = False, **kwargs: Any
    ) -> None:
        super().__init__(columns=columns, ignore_missing=ignore_missing)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Filling NaN values of {len(columns):,} columns...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select((cs.by_name(columns) & cs.float()).fill_nan(**self._kwargs))
        )


class FillNullTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to fill null values.

    Args:
        columns: The columns to prepare. If ``None``, it processes all
            the columns of type string.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``fill_null``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import FillNull
    >>> transformer = FillNull(columns=["col1", "col4"], value=100)
    >>> transformer
    FillNullTransformer(columns=('col1', 'col4'), ignore_missing=False, value=100)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, None],
    ...         "col2": [1.2, 2.2, 3.2, 4.2, None],
    ...         "col3": ["a", "b", "c", "d", None],
    ...         "col4": [1.2, float("nan"), 3.2, None, 5.2],
    ...     }
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ str  ┆ f64  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1.2  ┆ a    ┆ 1.2  │
    │ 2    ┆ 2.2  ┆ b    ┆ NaN  │
    │ 3    ┆ 3.2  ┆ c    ┆ 3.2  │
    │ 4    ┆ 4.2  ┆ d    ┆ null │
    │ null ┆ null ┆ null ┆ 5.2  │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬───────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4  │
    │ ---  ┆ ---  ┆ ---  ┆ ---   │
    │ i64  ┆ f64  ┆ str  ┆ f64   │
    ╞══════╪══════╪══════╪═══════╡
    │ 1    ┆ 1.2  ┆ a    ┆ 1.2   │
    │ 2    ┆ 2.2  ┆ b    ┆ NaN   │
    │ 3    ┆ 3.2  ┆ c    ┆ 3.2   │
    │ 4    ┆ 4.2  ┆ d    ┆ 100.0 │
    │ 100  ┆ null ┆ null ┆ 5.2   │
    └──────┴──────┴──────┴───────┘

    ```
    """

    def __init__(
        self, columns: Sequence[str] | None = None, ignore_missing: bool = False, **kwargs: Any
    ) -> None:
        super().__init__(columns=columns, ignore_missing=ignore_missing)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Filling NaN values of {len(columns):,} columns...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(frame.select(cs.by_name(columns).fill_null(**self._kwargs)))
