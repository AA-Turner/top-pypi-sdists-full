r"""Contain DataFrame column utility functions."""

from __future__ import annotations

__all__ = ["drop_null_cols"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


def drop_null_cols(df: pl.DataFrame) -> pl.DataFrame:
    r"""Drop columns whose values are all null.

    A column is dropped if every one of its values is null. Columns
    with at least one non-null value are kept unchanged.

    Args:
        df: The input DataFrame.

    Returns:
        A new DataFrame with all-null columns removed, preserving the
            relative order of the remaining columns. If ``df`` has no
            rows, or no column is entirely null, a DataFrame with the
            same columns as ``df`` is returned (an empty ``df`` has no
            data to judge nullness from, so nothing is dropped).

    Example:
        ```pycon
        >>> import polars as pl
        >>> from zenpyre.utils.dataframe import drop_null_cols
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [None, None, None], "c": [None, 5, None]})
        >>> drop_null_cols(df).columns
        ['a', 'c']

        ```
    """
    if df.height == 0:
        return df
    null_counts = df.null_count().row(0, named=True)
    all_null_cols = [col for col, n in null_counts.items() if n == df.height]
    return df.drop(all_null_cols)
