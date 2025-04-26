r"""Contain DataFrame columns utility functions."""

from __future__ import annotations

__all__ = ["find_common_columns", "find_missing_columns"]


from typing import TYPE_CHECKING

import polars as pl

if TYPE_CHECKING:
    from collections.abc import Sequence


def find_common_columns(
    frame_or_cols: pl.DataFrame | Sequence, columns: Sequence[str]
) -> tuple[str, ...]:
    r"""Find the common columns that are both in the DataFrame and the
    given columns.

    Args:
        frame_or_cols: The DataFrame or its columns.
        columns: The columns to check.

    Returns:
        The columns i.e. the columns that are both in
            ``columns`` and ``frame_or_cols``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.utils.column import find_common_columns
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a ", " b", "  c  ", "d", "e"],
    ...     }
    ... )
    >>> cols = find_common_columns(frame, columns=["col1", "col2", "col3", "col4"])
    >>> cols
    ('col1', 'col2', 'col3')

    ```
    """
    cols = set(frame_or_cols.columns if isinstance(frame_or_cols, pl.DataFrame) else frame_or_cols)
    columns = set(columns)
    return tuple(sorted(columns.intersection(cols)))


def find_missing_columns(
    frame_or_cols: pl.DataFrame | Sequence, columns: Sequence[str]
) -> tuple[str, ...]:
    r"""Find the columns that are in the given columns but not in the
    DataFrame.

    Args:
        frame_or_cols: The DataFrame or its columns.
        columns: The columns to check.

    Returns:
        The list of missing columns i.e. the columns that are in
            ``columns`` but not in ``frame_or_cols``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.utils.column import find_missing_columns
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a ", " b", "  c  ", "d", "e"],
    ...     }
    ... )
    >>> cols = find_missing_columns(frame, columns=["col1", "col2", "col3", "col4"])
    >>> cols
    ('col4',)

    ```
    """
    cols = set(frame_or_cols.columns if isinstance(frame_or_cols, pl.DataFrame) else frame_or_cols)
    columns = set(columns)
    return tuple(sorted(columns.difference(cols).intersection(columns)))
