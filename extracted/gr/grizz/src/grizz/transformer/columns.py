r"""Contain ``polars.DataFrame`` transformers to process string
values."""

from __future__ import annotations

__all__ = ["BaseColumnsTransformer"]

import logging
from abc import abstractmethod
from typing import TYPE_CHECKING

from grizz.transformer.base import BaseTransformer
from grizz.utils.column import find_common_columns, find_missing_columns

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl


logger = logging.getLogger(__name__)


class BaseColumnsTransformer(BaseTransformer):
    r"""Define a base class to implement transformers that apply the same
    transformation on multiple columns.

    Args:
        columns: The columns to prepare. If ``None``, it processes all
            the columns of type string.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import StripChars
    >>> transformer = StripChars(columns=["col2", "col3"])
    >>> transformer
    StripCharsTransformer(columns=('col2', 'col3'), ignore_missing=False)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a ", " b", "  c  ", "d", "e"],
    ...         "col4": ["a ", " b", "  c  ", "d", "e"],
    ...     }
    ... )
    >>> frame
    shape: (5, 4)
    ┌──────┬──────┬───────┬───────┐
    │ col1 ┆ col2 ┆ col3  ┆ col4  │
    │ ---  ┆ ---  ┆ ---   ┆ ---   │
    │ i64  ┆ str  ┆ str   ┆ str   │
    ╞══════╪══════╪═══════╪═══════╡
    │ 1    ┆ 1    ┆ a     ┆ a     │
    │ 2    ┆ 2    ┆  b    ┆  b    │
    │ 3    ┆ 3    ┆   c   ┆   c   │
    │ 4    ┆ 4    ┆ d     ┆ d     │
    │ 5    ┆ 5    ┆ e     ┆ e     │
    └──────┴──────┴───────┴───────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (5, 4)
    ┌──────┬──────┬──────┬───────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4  │
    │ ---  ┆ ---  ┆ ---  ┆ ---   │
    │ i64  ┆ str  ┆ str  ┆ str   │
    ╞══════╪══════╪══════╪═══════╡
    │ 1    ┆ 1    ┆ a    ┆ a     │
    │ 2    ┆ 2    ┆ b    ┆  b    │
    │ 3    ┆ 3    ┆ c    ┆   c   │
    │ 4    ┆ 4    ┆ d    ┆ d     │
    │ 5    ┆ 5    ┆ e    ┆ e     │
    └──────┴──────┴──────┴───────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None = None,
        ignore_missing: bool = False,
    ) -> None:
        self._columns = tuple(columns) if columns is not None else None
        self._ignore_missing = bool(ignore_missing)

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        self._pre_transform(frame)
        missing = self.find_missing_columns(frame)
        if missing and not self._ignore_missing:
            msg = f"{len(missing)} columns are missing in the DataFrame: {missing}"
            raise RuntimeError(msg)
        if missing:
            logger.warning(
                f"{len(missing)} columns are missing in the DataFrame and will be ignored: "
                f"{missing}"
            )
        return self._transform(frame=frame)

    def find_columns(self, frame: pl.DataFrame) -> tuple[str, ...]:
        r"""Find the columns to transform.

        Args:
            frame: The input DataFrame. Sometimes the columns to
                transform are found by analyzing the input
                DataFrame.

        Returns:
            The columns to transform.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from grizz.transformer import StripChars
        >>> frame = pl.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["a ", " b", "  c  ", "d", "e"],
        ...         "col4": ["a ", " b", "  c  ", "d", "e"],
        ...     }
        ... )
        >>> transformer = StripChars(columns=["col2", "col3"])
        >>> transformer.find_columns(frame)
        ('col2', 'col3')
        >>> transformer = StripChars()
        >>> transformer.find_columns(frame)
        ('col1', 'col2', 'col3', 'col4')

        ```
        """
        if self._columns is None:
            return tuple(frame.columns)
        return self._columns

    def find_common_columns(self, frame: pl.DataFrame) -> tuple[str, ...]:
        r"""Find the common columns.

        Args:
            frame: The input DataFrame. Sometimes the columns to
                transform are found by analyzing the input
                DataFrame.

        Returns:
            The common columns.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from grizz.transformer import StripChars
        >>> frame = pl.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["a ", " b", "  c  ", "d", "e"],
        ...         "col4": ["a ", " b", "  c  ", "d", "e"],
        ...     }
        ... )
        >>> transformer = StripChars(columns=["col2", "col3", "col5"])
        >>> transformer.find_common_columns(frame)
        ('col2', 'col3')
        >>> transformer = StripChars()
        >>> transformer.find_common_columns(frame)
        ('col1', 'col2', 'col3', 'col4')

        ```
        """
        return find_common_columns(frame, self.find_columns(frame))

    def find_missing_columns(self, frame: pl.DataFrame) -> tuple[str, ...]:
        r"""Find the missing columns.

        Args:
            frame: The input DataFrame. Sometimes the columns to
                transform are found by analyzing the input
                DataFrame.

        Returns:
            The missing columns.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from grizz.transformer import StripChars
        >>> frame = pl.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["a ", " b", "  c  ", "d", "e"],
        ...         "col4": ["a ", " b", "  c  ", "d", "e"],
        ...     }
        ... )
        >>> transformer = StripChars(columns=["col2", "col3", "col5"])
        >>> transformer.find_missing_columns(frame)
        ('col5',)
        >>> transformer = StripChars()
        >>> transformer.find_missing_columns(frame)
        ()

        ```
        """
        return find_missing_columns(frame, self.find_columns(frame))

    @abstractmethod
    def _pre_transform(self, frame: pl.DataFrame) -> None:
        r"""Log information about the transformation.

        Args:
            frame: The DataFrame to transform.
        """

    @abstractmethod
    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        r"""Transform the data in the given column.

        Args:
            frame: The DataFrame to transform.

        Returns:
            The transformed DataFrame.
        """
