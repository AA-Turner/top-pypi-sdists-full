r"""Contain JSON-based data loaders and savers."""

from __future__ import annotations

__all__ = ["JsonLoader", "JsonSaver", "load_json", "save_json", "get_loader_mapping"]

import json
from pathlib import Path
from typing import Any, TypeVar

from iden.io.base import BaseFileSaver, BaseLoader

T = TypeVar("T")


class JsonLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_json, JsonLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.json")
    ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = JsonLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, path: Path) -> Any:
        with Path.open(path, mode="rb") as file:
            return json.load(file)


class JsonSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import JsonSaver, JsonLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.json")
    ...     JsonSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = JsonLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: Any, path: Path) -> None:
        with Path.open(path, "w") as file:
            json.dump(to_save, file, sort_keys=False)


def load_json(path: Path) -> Any:
    r"""Load the data from a given JSON file.

    Args:
        path: Specifies the path to the JSON file.

    Returns:
        The data from the JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_json, load_json
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.json")
    ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_json(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    return JsonLoader().load(path)


def save_json(to_save: Any, path: Path, *, exist_ok: bool = False) -> None:
    r"""Save the given data in a JSON file.

    Args:
        to_save: Specifies the data to write in a JSON file.
        path: Specifies the path where to write the JSON file.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.

    Raises:
        FileExistsError: if the file already exists.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_json, load_json
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.json")
    ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_json(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    JsonSaver().save(to_save, path, exist_ok=exist_ok)


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon
    >>> from iden.io.json import get_loader_mapping
    >>> get_loader_mapping()
    {'json': JsonLoader()}

    ```
    """
    return {"json": JsonLoader()}
