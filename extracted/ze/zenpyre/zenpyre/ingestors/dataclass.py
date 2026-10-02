r"""Provide an ingestor that loads a list of dataclass instances from a
JSON file."""

from __future__ import annotations

__all__ = ["DataclassIngestor"]

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from coola.display import InlineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor
from zenpyre.utils.dataclass.io import load_dataclasses

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T")


class DataclassIngestor(BaseIngestor[list[T]], InlineDisplayMixin, Generic[T]):
    """An ingestor that loads a list of dataclass instances from a JSON
    file.

    Reads a JSON file previously written by
    :func:`~zenpyre.utils.dataclass_io.save_dataclasses` and
    reconstructs each entry as an instance of ``cls``.

    Args:
        path: The path to the JSON file to load.
        cls: The dataclass type to reconstruct each entry as.

    Example:
        ```pycon
        >>> from dataclasses import dataclass
        >>> from zenpyre.ingestors import DataclassIngestor
        >>> @dataclass(frozen=True)
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> ingestor = DataclassIngestor(path="points.json", cls=Point)
        >>> points = ingestor.ingest()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, cls: type[T]) -> None:
        self._path = path
        self._cls = cls

    def ingest(self) -> list[T]:
        return load_dataclasses(self._path, self._cls)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path, "cls": self._cls}
