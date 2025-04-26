r"""Contain a wrapper around an ingestor to transform the data after
ingestion."""

from __future__ import annotations

__all__ = ["TransformIngestor"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_mapping

from grizz.ingestor.base import BaseIngestor, setup_ingestor
from grizz.transformer.base import BaseTransformer, setup_transformer

if TYPE_CHECKING:
    import polars as pl

logger = logging.getLogger(__name__)


class TransformIngestor(BaseIngestor):
    r"""Implement an ingestor that also transforms the DataFrame.

    Args:
        ingestor: The base ingestor.
        transformer: The ``polars.DataFrame`` transformer or
            its configuration.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.ingestor import TransformIngestor, Ingestor
    >>> from grizz.transformer import Cast
    >>> ingestor = TransformIngestor(
    ...     ingestor=Ingestor(
    ...         pl.DataFrame(
    ...             {
    ...                 "col1": ["1", "2", "3", "4", "5"],
    ...                 "col2": ["a", "b", "c", "d", "e"],
    ...                 "col3": [1.2, 2.2, 3.2, 4.2, 5.2],
    ...             }
    ...         )
    ...     ),
    ...     transformer=Cast(columns=["col1", "col3"], dtype=pl.Float32),
    ... )
    >>> ingestor
    TransformIngestor(
      (ingestor): Ingestor(shape=(5, 3))
      (transformer): CastTransformer(columns=('col1', 'col3'), dtype=Float32, ignore_missing=False)
    )
    >>> frame = ingestor.ingest()
    >>> frame
    shape: (5, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ f32  ┆ str  ┆ f32  │
    ╞══════╪══════╪══════╡
    │ 1.0  ┆ a    ┆ 1.2  │
    │ 2.0  ┆ b    ┆ 2.2  │
    │ 3.0  ┆ c    ┆ 3.2  │
    │ 4.0  ┆ d    ┆ 4.2  │
    │ 5.0  ┆ e    ┆ 5.2  │
    └──────┴──────┴──────┘

    ```
    """

    def __init__(self, ingestor: BaseIngestor | dict, transformer: BaseTransformer | dict) -> None:
        self._ingestor = setup_ingestor(ingestor)
        self._transformer = setup_transformer(transformer)

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping({"ingestor": self._ingestor, "transformer": self._transformer})
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def ingest(self) -> pl.DataFrame:
        frame = self._ingestor.ingest()
        return self._transformer.transform(frame)
