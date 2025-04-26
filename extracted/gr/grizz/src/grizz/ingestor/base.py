r"""Contain the base class to implement an ingestor."""

from __future__ import annotations

__all__ = ["BaseIngestor", "is_ingestor_config", "setup_ingestor"]

import logging
from abc import ABC
from typing import TYPE_CHECKING

from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    import polars as pl

logger = logging.getLogger(__name__)


class BaseIngestor(ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a DataFrame ingestor.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import ParquetIngestor
    >>> ingestor = ParquetIngestor(path="/path/to/frame.parquet")
    >>> ingestor
    ParquetIngestor(path=/path/to/frame.parquet)
    >>> frame = ingestor.ingest()  # doctest: +SKIP

    ```
    """

    def ingest(self) -> pl.DataFrame:
        r"""Ingest a DataFrame.

        Returns:
            The ingested DataFrame.

        Example usage:

        ```pycon

        >>> from grizz.ingestor import ParquetIngestor
        >>> ingestor = ParquetIngestor(path="/path/to/frame.parquet")
        >>> frame = ingestor.ingest()  # doctest: +SKIP

        ```
        """


def is_ingestor_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseIngestor``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseIngestor`` object.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import is_ingestor_config
    >>> is_ingestor_config(
    ...     {"_target_": "grizz.ingestor.CsvIngestor", "path": "/path/to/data.csv"}
    ... )
    True

    ```
    """
    return is_object_config(config, BaseIngestor)


def setup_ingestor(
    ingestor: BaseIngestor | dict,
) -> BaseIngestor:
    r"""Set up an ingestor.

    The ingestor is instantiated from its configuration
    by using the ``BaseIngestor`` factory function.

    Args:
        ingestor: Specifies an ingestor or its configuration.

    Returns:
        An instantiated ingestor.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import setup_ingestor
    >>> ingestor = setup_ingestor(
    ...     {"_target_": "grizz.ingestor.CsvIngestor", "path": "/path/to/data.csv"}
    ... )
    >>> ingestor
    CsvIngestor(path=/path/to/data.csv)

    ```
    """
    if isinstance(ingestor, dict):
        logger.info("Initializing an ingestor from its configuration... ")
        ingestor = BaseIngestor.factory(**ingestor)
    if not isinstance(ingestor, BaseIngestor):
        logger.warning(f"ingestor is not a `BaseIngestor` (received: {type(ingestor)})")
    return ingestor
