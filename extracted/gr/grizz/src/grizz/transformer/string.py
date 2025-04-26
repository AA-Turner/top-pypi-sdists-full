r"""Contain ``polars.DataFrame`` transformers to process string
values."""

from __future__ import annotations

__all__ = ["StripCharsTransformer"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_kwargs

if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class StripCharsTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to remove leading and trailing
    characters.

    Args:
        columns: The columns to prepare. If ``None``, it processes all
            the columns of type string.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``strip_chars``.

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
        logger.info(f"Stripping characters of {len(columns):,} columns...")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        return frame.with_columns(
            frame.select((cs.by_name(columns) & cs.string()).str.strip_chars(**self._kwargs))
        )
