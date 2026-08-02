r"""Provide generic JSON persistence utilities for lists of dataclass
instances."""

from __future__ import annotations

__all__ = ["load_dataclasses", "save_dataclasses"]

import logging
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any, TypeVar

from coola.utils.path import sanitize_path
from iden.io import load_json, save_json

if TYPE_CHECKING:
    from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")


def load_dataclasses(path: Path | str, cls: type[T]) -> list[T]:
    """Load a list of dataclass instances from a JSON file.

    Reads a JSON array of objects from ``path`` and converts each one
    into an instance of ``cls`` by unpacking its keys as keyword
    arguments.

    Args:
        path: The source file path, as previously written by
            :func:`save_dataclasses`.
        cls: The dataclass type to reconstruct each entry as.

    Returns:
        A list of ``cls`` instances loaded from ``path``.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        TypeError: If the JSON content is not a list.
        ValueError: If an entry in the list is missing a required field
            or has an unexpected field for ``cls``.

    Example:
        ```pycon
        >>> from dataclasses import dataclass
        >>> from zenpyre.utils.dataclass import load_dataclasses
        >>> @dataclass(frozen=True)
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> points = load_dataclasses("points.json", Point)  # doctest: +SKIP

        ```
    """
    if not is_dataclass(cls):
        msg = f"cls must be a dataclass type, got {cls}"
        raise TypeError(msg)

    path = sanitize_path(path)
    logger.debug("Loading %s items from %s...", cls.__name__, path)
    data = load_json(path)

    if not isinstance(data, list):
        msg = f"Expected a JSON array of {cls.__name__} objects in {path}, got {type(data)}"
        raise TypeError(msg)

    try:
        items = [cls(**entry) for entry in data]
    except TypeError as e:
        msg = f"Could not parse {cls.__name__} entries from {path}: {e}"
        raise ValueError(msg) from e

    logger.debug("Loaded %s items from %s", f"{len(items):,}", path)
    return items


def save_dataclasses(items: list[Any], path: Path | str, *, exist_ok: bool = False) -> None:
    """Save a list of dataclass instances to a JSON file.

    Serialises each item to a dict via :func:`dataclasses.asdict` and
    writes the resulting list to ``path`` as a JSON array. Works with any
    dataclass type, including frozen dataclasses, as long as all field
    values are JSON-serialisable.

    Args:
        items: The list of dataclass instances to save.
        path: The destination file path.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.

    Raises:
        TypeError: If any item in ``items`` is not a dataclass
            instance.
        FileExistsError: If ``path`` already exists and
            ``exist_ok=False``.
        OSError: If ``path`` cannot be written to, or if ``path``
            exists as a directory (regardless of ``exist_ok``).

    Example:
        ```pycon
        >>> from dataclasses import dataclass
        >>> from zenpyre.utils.dataclass import save_dataclasses
        >>> @dataclass(frozen=True)
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> points = save_dataclasses([Point(1, 2), Point(3, 4)])  # doctest: +SKIP

        ```
    """
    for item in items:
        if not is_dataclass(item):
            msg = f"All items must be dataclass instances, got {type(item)}"
            raise TypeError(msg)

    path = sanitize_path(path)
    logger.debug("Saving %s items to %s...", f"{len(items):,}", path)
    data = [asdict(item) for item in items]
    save_json(data, path, exist_ok=exist_ok)
    logger.debug("Saved %s items to %s", f"{len(items):,}", path)
