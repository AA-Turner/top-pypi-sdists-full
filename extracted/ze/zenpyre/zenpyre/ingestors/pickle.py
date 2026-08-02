r"""Define an ingestor that loads data from a pickle file."""

from __future__ import annotations

__all__ = ["PickleIngestor"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import InlineDisplayMixin
from coola.utils.path import sanitize_path
from iden.io import load_pickle

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class PickleIngestor(BaseIngestor[T], InlineDisplayMixin):
    """Ingestor that loads data from a pickle file.

    Args:
        path: Path to the pickle file to load.

    Raises:
        FileNotFoundError: If ``path`` does not exist when
            :meth:`ingest` is called.

    Example:
        ```pycon
        >>> ingestor = PickleIngestor(path="data.pkl")
        >>> data = ingestor.ingest()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str) -> None:
        self._path = sanitize_path(path)

    def ingest(self) -> T:
        """Load and return data from the pickle file.

        Returns:
            The Python object stored in the pickle file.

        Raises:
            FileNotFoundError: If the pickle file does not exist at the
                configured path.
        """
        logger.info(f"Ingesting data from pickle file: {self._path}")
        if not self._path.is_file():
            msg = (
                f"Pickle file not found: '{self._path}'. "
                "Ensure the file has been created before calling ingest()"
            )
            raise FileNotFoundError(msg)
        return load_pickle(self._path)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        """Return a display-friendly dict of constructor arguments.

        Returns:
            A dict with a ``"path"`` key.
        """
        return {"path": self._path}
