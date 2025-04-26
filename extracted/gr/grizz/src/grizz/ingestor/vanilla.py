r"""Contain the implementation of a simple ingestor."""

from __future__ import annotations

__all__ = ["Ingestor"]


from typing import TYPE_CHECKING

from grizz.ingestor.base import BaseIngestor

if TYPE_CHECKING:
    import polars as pl


class Ingestor(BaseIngestor):
    r"""Implement a simple DataFrame ingestor.

    Args:
        frame: The DataFrame to ingest.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.ingestor import Ingestor
    >>> ingestor = Ingestor(
    ...     frame=pl.DataFrame(
    ...         {
    ...             "col1": [1, 2, 3, 4, 5],
    ...             "col2": ["1", "2", "3", "4", "5"],
    ...             "col3": ["1", "2", "3", "4", "5"],
    ...             "col4": ["a", "b", "c", "d", "e"],
    ...         }
    ...     )
    ... )
    >>> ingestor
    Ingestor(shape=(5, 4))
    >>> frame = ingestor.ingest()

    ```
    """

    def __init__(self, frame: pl.DataFrame) -> None:
        self._frame = frame

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(shape={self._frame.shape})"

    def ingest(self) -> pl.DataFrame:
        return self._frame
