r"""Contain the base class to implement a ``polars.DataFrame``
transformer."""

from __future__ import annotations

__all__ = [
    "BaseTransformer",
    "is_transformer_config",
    "setup_transformer",
]

import logging
from abc import ABC
from typing import TYPE_CHECKING

from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    import polars as pl

logger = logging.getLogger(__name__)


class BaseTransformer(ABC, metaclass=AbstractFactory):
    r"""Define the base class to transform a ``polars.DataFrame``.

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

    def transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        r"""Transform the data in the ``polars.DataFrame``.

        Args:
            frame: The ``polars.DataFrame`` to transform.

        Returns:
            The transformed DataFrame.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from grizz.transformer import Cast
        >>> transformer = Cast(columns=["col1", "col3"], dtype=pl.Int32)
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


def is_transformer_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseTransformer``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseTransformer`` object.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import is_transformer_config
    >>> is_transformer_config(
    ...     {
    ...         "_target_": "grizz.transformer.Cast",
    ...         "columns": ("col1", "col3"),
    ...         "dtype": pl.Int32,
    ...     }
    ... )
    True

    ```
    """
    return is_object_config(config, BaseTransformer)


def setup_transformer(
    transformer: BaseTransformer | dict,
) -> BaseTransformer:
    r"""Set up a ``polars.DataFrame`` transformer.

    The transformer is instantiated from its configuration
    by using the ``BaseTransformer`` factory function.

    Args:
        transformer: Specifies a ``polars.DataFrame`` transformer or
            its configuration.

    Returns:
        An instantiated transformer.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import setup_transformer
    >>> transformer = setup_transformer(
    ...     {
    ...         "_target_": "grizz.transformer.Cast",
    ...         "columns": ("col1", "col3"),
    ...         "dtype": pl.Int32,
    ...     }
    ... )
    >>> transformer
    CastTransformer(columns=('col1', 'col3'), dtype=Int32, ignore_missing=False)

    ```
    """
    if isinstance(transformer, dict):
        logger.info("Initializing a DataFrame transformer from its configuration... ")
        transformer = BaseTransformer.factory(**transformer)
    if not isinstance(transformer, BaseTransformer):
        logger.warning(f"transformer is not a `BaseTransformer` (received: {type(transformer)})")
    return transformer
