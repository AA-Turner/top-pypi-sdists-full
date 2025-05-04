r"""Contain pickle-based data loaders and savers."""

from __future__ import annotations

__all__ = ["PickleLoader", "PickleSaver", "get_loader_mapping", "load_pickle", "save_pickle"]

import pickle
from pathlib import Path
from typing import Any, TypeVar

from coola import objects_are_equal
from coola.utils.format import repr_mapping_line

from iden.io.base import BaseFileSaver, BaseLoader

T = TypeVar("T")


class PickleLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a pickle file.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_pickle, PickleLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pkl")
    ...     save_pickle({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = PickleLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return isinstance(other, self.__class__)

    def load(self, path: Path) -> Any:
        with Path.open(path, mode="rb") as file:
            return pickle.load(file)  # noqa: S301


class PickleSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a pickle file.

    Args:
        **kwargs: Additional arguments passed to ``pickle.dump``.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import PickleSaver, PickleLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pkl")
    ...     PickleSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = PickleLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __init__(self, **kwargs: Any) -> None:
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({repr_mapping_line(self._kwargs)})"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._kwargs, other._kwargs, equal_nan=equal_nan)

    def _save_file(self, to_save: Any, path: Path) -> None:
        with Path.open(path, mode="wb") as file:
            pickle.dump(to_save, file, **self._kwargs)


def load_pickle(path: Path) -> Any:
    r"""Load the data from a given pickle file.

    Args:
        path: The path to the pickle file.

    Returns:
        The data from the pickle file.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_pickle, load_pickle
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pkl")
    ...     save_pickle({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_pickle(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    return PickleLoader().load(path)


def save_pickle(to_save: Any, path: Path, *, exist_ok: bool = False, **kwargs: Any) -> None:
    r"""Save the given data in a pickle file.

    Args:
        to_save: The data to write in a pickle file.
        path: The path where to write the pickle file.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.
        **kwargs: Additional arguments passed to ``pickle.dump``.

    Raises:
        FileExistsError: if the file already exists.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_pickle, load_pickle
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pkl")
    ...     save_pickle({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_pickle(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    PickleSaver(**kwargs).save(to_save, path, exist_ok=exist_ok)


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon

    >>> from iden.io.pickle import get_loader_mapping
    >>> get_loader_mapping()
    {'pkl': PickleLoader(), 'pickle': PickleLoader()}

    ```
    """
    loader = PickleLoader()
    return {"pkl": loader, "pickle": loader}
