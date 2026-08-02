r"""Define an ingestor that loads plain-text content from disk."""

from __future__ import annotations

__all__ = ["TextIngestor"]

import logging
from typing import TYPE_CHECKING, Any

from coola.display import InlineDisplayMixin
from coola.utils.path import sanitize_path
from iden.io import load_text

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


class TextIngestor(BaseIngestor[str], InlineDisplayMixin):
    """Ingestor that loads data from a text file.

    Reads the full content of a text file and returns it as a single
    string. Intended for loading Markdown filings or other plain-text
    documents for downstream processing by an agent.

    Args:
        path: Path to the text file to load.
        encoding: The file encoding to use when reading the file.
            Defaults to ``"utf-8"``.

    Raises:
        FileNotFoundError: If ``path`` does not exist when
            :meth:`ingest` is called.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import TextIngestor
        >>> ingestor = TextIngestor(path="filing.md")
        >>> text = ingestor.ingest()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, encoding: str = "utf-8") -> None:
        self._path = sanitize_path(path)
        self._encoding = encoding

    def ingest(self) -> str:
        """Load and return the content of the text file.

        Returns:
            The full file content as a string.

        Raises:
            FileNotFoundError: If the text file does not exist at the
                configured path.
        """
        logger.info(f"Ingesting data from text file: {self._path}")
        if not self._path.is_file():
            msg = (
                f"Text file not found: '{self._path}'. "
                "Ensure the file exists before calling ingest()"
            )
            raise FileNotFoundError(msg)
        return load_text(self._path, encoding=self._encoding)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        """Return a display-friendly dict of constructor arguments.

        Returns:
            A dict with ``"path"`` and ``"encoding"`` keys.
        """
        return {"path": self._path, "encoding": self._encoding}
