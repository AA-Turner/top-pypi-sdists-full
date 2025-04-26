r"""Contain text-based data loaders and savers."""

from __future__ import annotations

__all__ = ["TextLoader", "TextSaver", "load_text", "save_text", "get_loader_mapping"]

from pathlib import Path
from typing import Any, TypeVar

from iden.io.base import BaseFileSaver, BaseLoader

T = TypeVar("T")


class TextLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a text file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_text, TextLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.txt")
    ...     save_text("hello", path)
    ...     data = TextLoader().load(path)
    ...     data
    ...
    'hello'

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, path: Path) -> Any:
        with Path.open(path) as file:
            return file.read()


class TextSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a text file.

    Note:
        If the data to save is not a string, it is converted to
            a string before to be saved by using ``str``.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import TextSaver, TextLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.txt")
    ...     TextSaver().save("hello", path)
    ...     data = TextLoader().load(path)
    ...     data
    ...
    'hello'

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: Any, path: Path) -> None:
        with Path.open(path, mode="w") as file:
            file.write(str(to_save))


def load_text(path: Path) -> str:
    r"""Load the data from a given text file.

    Args:
        path: Specifies the path where to the text file.

    Returns:
        The data from the text file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_text, load_text
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.txt")
    ...     save_text("hello", path)
    ...     data = load_text(path)
    ...     data
    ...
    'hello'

    ```
    """
    return TextLoader().load(path)


def save_text(to_save: Any, path: Path, *, exist_ok: bool = False) -> None:
    r"""Save the given data in a text file.

    Args:
        to_save: Specifies the data to write in a text file.
        path: Specifies the path where to write the text file.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.

    Raises:
        FileExistsError: if the file already exists.

    Note:
        If the data to save is not a string, it is converted to
            a string before to be saved by using ``str``.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_text, load_text
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.txt")
    ...     save_text("hello", path)
    ...     data = load_text(path)
    ...     data
    ...
    'hello'

    ```
    """
    TextSaver().save(to_save, path, exist_ok=exist_ok)


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon
    >>> from iden.io.text import get_loader_mapping
    >>> get_loader_mapping()
    {'txt': TextLoader()}

    ```
    """
    return {"txt": TextLoader()}
