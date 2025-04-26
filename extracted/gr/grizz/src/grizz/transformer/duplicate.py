r"""Contain transformers to drop columns or rows with null values."""

from __future__ import annotations

__all__ = ["DropDuplicateTransformer"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
import polars.selectors as cs

from grizz.transformer.columns import BaseColumnsTransformer
from grizz.utils.format import str_kwargs, str_row_diff

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class DropDuplicateTransformer(BaseColumnsTransformer):
    r"""Implement a transformer to drop duplicate rows.

    Args:
        columns: The columns to check. If set to ``None`` (default),
            use all columns.
        ignore_missing: If ``False``, an exception is raised if a
            column is missing, otherwise just a warning message is
            shown.
        **kwargs: The keyword arguments for ``unique``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import DropDuplicate
    >>> transformer = DropDuplicate(keep="first", maintain_order=True)
    >>> transformer
    DropDuplicateTransformer(columns=None, ignore_missing=False, keep=first, maintain_order=True)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 1],
    ...         "col2": ["1", "2", "3", "4", "1"],
    ...         "col3": ["1", "2", "3", "1", "1"],
    ...         "col4": ["a", "a", "a", "a", "a"],
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
    │ 2    ┆ 2    ┆ 2    ┆ a    │
    │ 3    ┆ 3    ┆ 3    ┆ a    │
    │ 4    ┆ 4    ┆ 1    ┆ a    │
    │ 1    ┆ 1    ┆ 1    ┆ a    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.transform(frame)
    >>> out
    shape: (4, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ str  ┆ str  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ 1    ┆ a    │
    │ 2    ┆ 2    ┆ 2    ┆ a    │
    │ 3    ┆ 3    ┆ 3    ┆ a    │
    │ 4    ┆ 4    ┆ 1    ┆ a    │
    └──────┴──────┴──────┴──────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None = None,
        ignore_missing: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(columns, ignore_missing)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(columns={self._columns}, "
            f"ignore_missing={self._ignore_missing}{str_kwargs(self._kwargs)})"
        )

    def _pre_transform(self, frame: pl.DataFrame) -> None:
        columns = self.find_common_columns(frame)
        logger.info(f"Dropping duplicate rows by checking {len(columns):,} columns....")

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        columns = self.find_common_columns(frame)
        initial_shape = frame.shape
        out = frame.unique(subset=cs.by_name(columns), **self._kwargs)
        logger.info(
            f"DataFrame shape: {initial_shape} -> {out.shape} | "
            f"{str_row_diff(orig=initial_shape[0], final=out.shape[0])}"
        )
        return out
