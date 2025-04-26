r"""Contain ``polars.DataFrame`` transformers to compute difference."""

from __future__ import annotations

__all__ = ["DiffTransformer", "TimeDiffTransformer"]


from typing import TYPE_CHECKING

import polars as pl

from grizz.transformer import BaseTransformer

if TYPE_CHECKING:
    from collections.abc import Sequence


class DiffTransformer(BaseTransformer):
    r"""Implement a transformer to compute the first discrete difference
    between shifted items.

    Args:
        in_col: The input column name.
        out_col: The output column name.
        shift: The number of slots to shift.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import Diff
    >>> transformer = Diff(in_col="col1", out_col="diff")
    >>> transformer
    DiffTransformer(in_col=col1, out_col=diff, shift=1)
    >>> frame = pl.DataFrame({"col1": [1, 2, 3, 4, 5], "col2": ["a", "b", "c", "d", "e"]})
    >>> frame
    shape: (5, 2)
    ┌──────┬──────┐
    │ col1 ┆ col2 │
    │ ---  ┆ ---  │
    │ i64  ┆ str  │
    ╞══════╪══════╡
    │ 1    ┆ a    │
    │ 2    ┆ b    │
    │ 3    ┆ c    │
    │ 4    ┆ d    │
    │ 5    ┆ e    │
    └──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ diff │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ str  ┆ i64  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ a    ┆ null │
    │ 2    ┆ b    ┆ 1    │
    │ 3    ┆ c    ┆ 1    │
    │ 4    ┆ d    ┆ 1    │
    │ 5    ┆ e    ┆ 1    │
    └──────┴──────┴──────┘

    ```
    """

    def __init__(self, in_col: str, out_col: str, shift: int = 1) -> None:
        self._in_col = in_col
        self._out_col = out_col
        self._shift = shift

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(in_col={self._in_col}, "
            f"out_col={self._out_col}, shift={self._shift})"
        )

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        return frame.with_columns(
            frame.select(pl.col(self._in_col).diff(n=self._shift).alias(self._out_col))
        )


class TimeDiffTransformer(BaseTransformer):
    r"""Implement a transformer to compute the time difference between
    consecutive time steps.

    Args:
        group_cols: The columns used to generate the group for each
            sequence.
        time_col: The input time column name.
        time_diff_col: The output time difference column name.
        shift: The number of slots to shift.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import TimeDiff
    >>> transformer = TimeDiff(group_cols=["col"], time_col="time", time_diff_col="diff")
    >>> transformer
    TimeDiffTransformer(group_cols=['col'], time_col=time, time_diff_col=diff, shift=1)
    >>> frame = pl.DataFrame({"col": ["a", "b", "a", "a", "b"], "time": [1, 2, 3, 4, 5]})
    >>> frame
    shape: (5, 2)
    ┌─────┬──────┐
    │ col ┆ time │
    │ --- ┆ ---  │
    │ str ┆ i64  │
    ╞═════╪══════╡
    │ a   ┆ 1    │
    │ b   ┆ 2    │
    │ a   ┆ 3    │
    │ a   ┆ 4    │
    │ b   ┆ 5    │
    └─────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 3)
    ┌─────┬──────┬──────┐
    │ col ┆ time ┆ diff │
    │ --- ┆ ---  ┆ ---  │
    │ str ┆ i64  ┆ i64  │
    ╞═════╪══════╪══════╡
    │ a   ┆ 1    ┆ 0    │
    │ a   ┆ 3    ┆ 2    │
    │ a   ┆ 4    ┆ 1    │
    │ b   ┆ 2    ┆ 0    │
    │ b   ┆ 5    ┆ 3    │
    └─────┴──────┴──────┘

    ```
    """

    def __init__(
        self, group_cols: Sequence[str], time_col: str, time_diff_col: str, shift: int = 1
    ) -> None:
        self._group_cols = list(group_cols)
        self._time_col = time_col
        self._time_diff_col = time_diff_col
        self._shift = shift

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(group_cols={self._group_cols}, "
            f"time_col={self._time_col}, time_diff_col={self._time_diff_col}, "
            f"shift={self._shift})"
        )

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        frame = frame.sort(by=[*self._group_cols, self._time_col])
        return frame.with_columns(
            frame.group_by(self._group_cols)
            .agg(pl.col(self._time_col).diff(n=1).replace({None: 0}).alias(self._time_diff_col))
            .sort(by=self._group_cols)
            .select(pl.col(self._time_diff_col).explode())
        )
