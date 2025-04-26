r"""Contain the implementation of a CSV ingestor."""

from __future__ import annotations

__all__ = ["CsvIngestor"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl

from grizz.ingestor.base import BaseIngestor
from grizz.utils.format import str_kwargs
from grizz.utils.path import human_file_size, sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class CsvIngestor(BaseIngestor):
    r"""Implement a CSV DataFrame ingestor.

    Args:
        path: The path to the CSV file to ingest.
        **kwargs: Additional keyword arguments for
            ``polars.read_csv``.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import CsvIngestor
    >>> ingestor = CsvIngestor(path="/path/to/frame.csv")
    >>> ingestor
    CsvIngestor(path=/path/to/frame.csv)
    >>> frame = ingestor.ingest()  # doctest: +SKIP

    ```
    """

    def __init__(self, path: Path | str, **kwargs: Any) -> None:
        self._path = sanitize_path(path)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(path={self._path}{str_kwargs(self._kwargs)})"

    def ingest(self) -> pl.DataFrame:
        logger.info(f"Ingesting CSV data from {self._path} | size={human_file_size(self._path)}...")
        frame = pl.read_csv(self._path, **self._kwargs)
        logger.info(f"Data ingested | shape: {frame.shape}")
        return frame
