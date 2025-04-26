r"""Contain ``polars.DataFrame`` transformers to process columns with
time values."""

from __future__ import annotations

__all__ = ["TimeToSecondTransformer", "ToTimeTransformer"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.base import BaseTransformer
from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_kwargs

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class TimeToSecondTransformer(BaseTransformer):
    r"""Implement a transformer to convert a column with time values to
    seconds.

    Args:
        in_col: The input column with the time value to convert.
        out_col: The output column with the time in seconds.

    Example usage:

    ```pycon

    >>> import datetime
    >>> import polars as pl
    >>> from grizz.transformer import TimeToSecond
    >>> transformer = TimeToSecond(in_col="time", out_col="second")
    >>> transformer
    TimeToSecondTransformer(in_col=time, out_col=second)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "time": [
    ...             datetime.time(0, 0, 1, 890000),
    ...             datetime.time(0, 1, 1, 890000),
    ...             datetime.time(1, 1, 1, 890000),
    ...             datetime.time(0, 19, 19, 890000),
    ...             datetime.time(19, 19, 19, 890000),
    ...         ],
    ...         "col": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={"time": pl.Time, "col": pl.String},
    ... )
    >>> frame
    shape: (5, 2)
    ┌──────────────┬─────┐
    │ time         ┆ col │
    │ ---          ┆ --- │
    │ time         ┆ str │
    ╞══════════════╪═════╡
    │ 00:00:01.890 ┆ a   │
    │ 00:01:01.890 ┆ b   │
    │ 01:01:01.890 ┆ c   │
    │ 00:19:19.890 ┆ d   │
    │ 19:19:19.890 ┆ e   │
    └──────────────┴─────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 3)
    ┌──────────────┬─────┬──────────┐
    │ time         ┆ col ┆ second   │
    │ ---          ┆ --- ┆ ---      │
    │ time         ┆ str ┆ f64      │
    ╞══════════════╪═════╪══════════╡
    │ 00:00:01.890 ┆ a   ┆ 1.89     │
    │ 00:01:01.890 ┆ b   ┆ 61.89    │
    │ 01:01:01.890 ┆ c   ┆ 3661.89  │
    │ 00:19:19.890 ┆ d   ┆ 1159.89  │
    │ 19:19:19.890 ┆ e   ┆ 69559.89 │
    └──────────────┴─────┴──────────┘

    ```
    """

    def __init__(self, in_col: str, out_col: str) -> None:
        self._in_col = in_col
        self._out_col = out_col

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(in_col={self._in_col}, out_col={self._out_col})"

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        logger.info(f"Converting time column ({self._in_col}) to seconds ({self._out_col})...")
        return frame.with_columns(
            frame.select(
                pl.col(self._in_col)
                .cast(pl.Duration)
                .dt.total_microseconds()
                .truediv(1e6)
                .alias(self._out_col)
            )
        )


class ToTimeTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to convert some columns to a
    ``polars.Time`` type.

    Args:
        columns: The columns to convert. ``None`` means all the
            columns.
        format: Format to use for conversion. Refer to the
            [chrono crate documentation](https://docs.rs/chrono/latest/chrono/format/strftime/index.html)
            for the full specification. Example: ``"%H:%M:%S"``.
            If set to ``None`` (default), the format is inferred from
            the data.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``to_time``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import ToTime
    >>> transformer = ToTime(columns=["col1"], format="%H:%M:%S")
    >>> transformer
    ToTimeTransformer(columns=('col1',), format=%H:%M:%S, ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": ["01:01:01", "02:02:02", "12:00:01", "18:18:18", "23:59:59"],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["01:01:01", "02:02:02", "12:00:01", "18:18:18", "23:59:59"],
    ...     }
    ... )
    >>> frame
    shape: (5, 3)
    ┌──────────┬──────┬──────────┐
    │ col1     ┆ col2 ┆ col3     │
    │ ---      ┆ ---  ┆ ---      │
    │ str      ┆ str  ┆ str      │
    ╞══════════╪══════╪══════════╡
    │ 01:01:01 ┆ 1    ┆ 01:01:01 │
    │ 02:02:02 ┆ 2    ┆ 02:02:02 │
    │ 12:00:01 ┆ 3    ┆ 12:00:01 │
    │ 18:18:18 ┆ 4    ┆ 18:18:18 │
    │ 23:59:59 ┆ 5    ┆ 23:59:59 │
    └──────────┴──────┴──────────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 3)
    ┌──────────┬──────┬──────────┐
    │ col1     ┆ col2 ┆ col3     │
    │ ---      ┆ ---  ┆ ---      │
    │ time     ┆ str  ┆ str      │
    ╞══════════╪══════╪══════════╡
    │ 01:01:01 ┆ 1    ┆ 01:01:01 │
    │ 02:02:02 ┆ 2    ┆ 02:02:02 │
    │ 12:00:01 ┆ 3    ┆ 12:00:01 │
    │ 18:18:18 ┆ 4    ┆ 18:18:18 │
    │ 23:59:59 ┆ 5    ┆ 23:59:59 │
    └──────────┴──────┴──────────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None,
        format: str | None = None,  # noqa: A002
        ignore_missing: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(columns, ignore_missing)
        self._format = format
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, format={self._format}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_columns(frame)
        logger.info(f"Converting {len(columns):,} columns to time ({self._format})...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select(
                (cs.by_name(columns) & cs.string()).str.to_time(self._format, **self._kwargs)
            )
        )
