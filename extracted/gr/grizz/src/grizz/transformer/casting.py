r"""Contain ``polars.DataFrame`` transformers to convert some columns to
a new data type."""

from __future__ import annotations

__all__ = [
    "CastTransformer",
    "DecimalCastTransformer",
    "FloatCastTransformer",
    "IntegerCastTransformer",
]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_kwargs

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class CastTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to convert some columns to a new data
    type.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        dtype: The target data type.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``cast``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import Cast
    >>> transformer = Cast(columns=["col1", "col3"], dtype=pl.Int32)
    >>> transformer
    CastTransformer(columns=('col1', 'col3'), dtype=Int32, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["1", "2", "3", "4", "5"],
    ...         "col4": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ str  ┆ str  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ 1    ┆ a    │
    │ 2    ┆ 2    ┆ 2    ┆ b    │
    │ 3    ┆ 3    ┆ 3    ┆ c    │
    │ 4    ┆ 4    ┆ 4    ┆ d    │
    │ 5    ┆ 5    ┆ 5    ┆ e    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i32  ┆ str  ┆ i32  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ 1    ┆ a    │
    │ 2    ┆ 2    ┆ 2    ┆ b    │
    │ 3    ┆ 3    ┆ 3    ┆ c    │
    │ 4    ┆ 4    ┆ 4    ┆ d    │
    │ 5    ┆ 5    ┆ 5    ┆ e    │
    └──────┴──────┴──────┴──────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None,
        dtype: type[pl.DataType],
        ignore_missing: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(columns, ignore_missing)
        self._dtype = dtype
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, dtype={self._dtype}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Converting {len(columns):,} columns to {self._dtype}...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select(cs.by_name(columns).cast(self._dtype, **self._kwargs))
        )


class DecimalCastTransformer(CastTransformer):
    r"""Implement a transformer to convert columns of type decimal to a
    new data type.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        dtype: The target data type.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``cast``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import DecimalCast
    >>> transformer = DecimalCast(columns=["col1", "col2"], dtype=pl.Float32)
    >>> transformer
    DecimalCastTransformer(columns=('col1', 'col2'), dtype=Float32, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": [1.0, 2.0, 3.0, 4.0, 5.0],
    ...         "col3": [1.0, 2.0, 3.0, 4.0, 5.0],
    ...         "col4": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={
    ...         "col1": pl.Int64,
    ...         "col2": pl.Decimal,
    ...         "col3": pl.Decimal,
    ...         "col4": pl.String,
    ...     },
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬───────────────┬───────────────┬──────┐
    │ col1 ┆ col2          ┆ col3          ┆ col4 │
    │ ---  ┆ ---           ┆ ---           ┆ ---  │
    │ i64  ┆ decimal[38,0] ┆ decimal[38,0] ┆ str  │
    ╞══════╪═══════════════╪═══════════════╪══════╡
    │ 1    ┆ 1             ┆ 1             ┆ a    │
    │ 2    ┆ 2             ┆ 2             ┆ b    │
    │ 3    ┆ 3             ┆ 3             ┆ c    │
    │ 4    ┆ 4             ┆ 4             ┆ d    │
    │ 5    ┆ 5             ┆ 5             ┆ e    │
    └──────┴───────────────┴───────────────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬───────────────┬──────┐
    │ col1 ┆ col2 ┆ col3          ┆ col4 │
    │ ---  ┆ ---  ┆ ---           ┆ ---  │
    │ i64  ┆ f32  ┆ decimal[38,0] ┆ str  │
    ╞══════╪══════╪═══════════════╪══════╡
    │ 1    ┆ 1.0  ┆ 1             ┆ a    │
    │ 2    ┆ 2.0  ┆ 2             ┆ b    │
    │ 3    ┆ 3.0  ┆ 3             ┆ c    │
    │ 4    ┆ 4.0  ┆ 4             ┆ d    │
    │ 5    ┆ 5.0  ┆ 5             ┆ e    │
    └──────┴──────┴───────────────┴──────┘

    ```
    """

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Converting {len(columns):,} columns to {self._dtype}...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select((cs.by_name(columns) & cs.decimal()).cast(self._dtype, **self._kwargs))
        )


class FloatCastTransformer(CastTransformer):
    r"""Implement a transformer to convert columns of type float to a new
    data type.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        dtype: The target data type.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``cast``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import FloatCast
    >>> transformer = FloatCast(columns=["col1", "col2"], dtype=pl.Int32)
    >>> transformer
    FloatCastTransformer(columns=('col1', 'col2'), dtype=Int32, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": [1.0, 2.0, 3.0, 4.0, 5.0],
    ...         "col3": [1.0, 2.0, 3.0, 4.0, 5.0],
    ...         "col4": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={
    ...         "col1": pl.Int64,
    ...         "col2": pl.Float64,
    ...         "col3": pl.Float64,
    ...         "col4": pl.String,
    ...     },
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1.0  ┆ 1.0  ┆ a    │
    │ 2    ┆ 2.0  ┆ 2.0  ┆ b    │
    │ 3    ┆ 3.0  ┆ 3.0  ┆ c    │
    │ 4    ┆ 4.0  ┆ 4.0  ┆ d    │
    │ 5    ┆ 5.0  ┆ 5.0  ┆ e    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ i32  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ 1.0  ┆ a    │
    │ 2    ┆ 2    ┆ 2.0  ┆ b    │
    │ 3    ┆ 3    ┆ 3.0  ┆ c    │
    │ 4    ┆ 4    ┆ 4.0  ┆ d    │
    │ 5    ┆ 5    ┆ 5.0  ┆ e    │
    └──────┴──────┴──────┴──────┘

    ```
    """

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Converting {len(columns):,} columns to {self._dtype}...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select((cs.by_name(columns) & cs.float()).cast(self._dtype, **self._kwargs))
        )


class IntegerCastTransformer(CastTransformer):
    r"""Implement a transformer to convert columns of type integer to a
    new data type.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        dtype: The target data type.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``cast``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import IntegerCast
    >>> transformer = IntegerCast(columns=["col1", "col2"], dtype=pl.Float32)
    >>> transformer
    IntegerCastTransformer(columns=('col1', 'col2'), dtype=Float32, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": [1.0, 2.0, 3.0, 4.0, 5.0],
    ...         "col3": [1, 2, 3, 4, 5],
    ...         "col4": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={
    ...         "col1": pl.Int64,
    ...         "col2": pl.Float64,
    ...         "col3": pl.Int64,
    ...         "col4": pl.String,
    ...     },
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ f64  ┆ i64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1.0  ┆ 1    ┆ a    │
    │ 2    ┆ 2.0  ┆ 2    ┆ b    │
    │ 3    ┆ 3.0  ┆ 3    ┆ c    │
    │ 4    ┆ 4.0  ┆ 4    ┆ d    │
    │ 5    ┆ 5.0  ┆ 5    ┆ e    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ f32  ┆ f64  ┆ i64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1.0  ┆ 1.0  ┆ 1    ┆ a    │
    │ 2.0  ┆ 2.0  ┆ 2    ┆ b    │
    │ 3.0  ┆ 3.0  ┆ 3    ┆ c    │
    │ 4.0  ┆ 4.0  ┆ 4    ┆ d    │
    │ 5.0  ┆ 5.0  ┆ 5    ┆ e    │
    └──────┴──────┴──────┴──────┘

    ```
    """

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Converting {len(columns):,} columns to {self._dtype}...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select((cs.by_name(columns) & cs.integer()).cast(self._dtype, **self._kwargs))
        )
