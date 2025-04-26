r"""Contain a data loader that automatically find the right loader to
load the data based on the file extension."""

from __future__ import annotations

__all__ = ["AutoFileLoader"]

from typing import TYPE_CHECKING, Any

from coola.utils import str_indent, str_mapping

from iden.io.base import BaseLoader
from iden.io.utils import get_loader_mapping

if TYPE_CHECKING:
    from pathlib import Path


class AutoFileLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data based on the file extension.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_json, AutoFileLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.json")
    ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     loader = AutoFileLoader()
    ...     data = loader.load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    registry: dict[str, BaseLoader] = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self.registry))}\n)"

    def load(self, path: Path) -> Any:
        extension = "".join(path.suffixes)[1:]
        loader = self.find_loader(extension)
        return loader.load(path)

    @classmethod
    def add_loader(cls, extension: str, loader: BaseLoader, exist_ok: bool = False) -> None:
        r"""Add a loader for a given file extension.

        Args:
            extension: The file extension.
            loader: The loader to use for the given file extension.
            exist_ok: If ``False``, ``RuntimeError`` is raised if the
                extension already exists. This parameter should be set
                to ``True`` to overwrite the loader for an extension.

        Raises:
            RuntimeError: if a loader is already registered for the
                extension and ``exist_ok=False``.

        Example usage:

        ```pycon
        >>> from iden.io import AutoFileLoader, TextLoader
        >>> AutoFileLoader.add_loader("text", TextLoader())

        ```
        """
        if extension in cls.registry and not exist_ok:
            msg = (
                f"A loader ({cls.registry[extension]}) is already registered for the file "
                f"extension {extension}. Please use `exist_ok=True` if you want to overwrite the "
                "loader for this extension"
            )
            raise RuntimeError(msg)
        cls.registry[extension] = loader

    @classmethod
    def has_loader(cls, extension: str) -> bool:
        r"""Indicate if a loader is registered for the given file
        extension.

        Args:
            extension: The file extension.

        Returns:
            ``True`` if a loader comparator is registered,
                otherwise ``False``.

        Example usage:

        ```pycon
        >>> from iden.io import AutoFileLoader
        >>> AutoFileLoader.has_loader("txt")
        True
        >>> AutoFileLoader.has_loader("newtxt")
        False

        ```
        """
        return extension in cls.registry

    @classmethod
    def find_loader(cls, extension: str) -> BaseLoader:
        r"""Find the loader associated to the file extension.

        Args:
            extension: The file extension.

        Returns:
            The loader for the given file extension.

        Raises:
            TypeError: if the file extension is not registered.

        Example usage:

        ```pycon
        >>> from iden.io import AutoFileLoader
        >>> AutoFileLoader.find_loader("txt")
        TextLoader()
        >>> AutoFileLoader.find_loader("json")
        JsonLoader()

        ```
        """
        if (loader := cls.registry.get(extension, None)) is not None:
            return loader
        msg = f"Incorrect extension: {extension}"
        raise TypeError(msg)


def register_auto_loaders() -> None:
    r"""Register some loaders for ``AutoFileLoader``."""
    for extension, loader in get_loader_mapping().items():
        if not AutoFileLoader.has_loader(extension):  # pragma: no cover
            AutoFileLoader.add_loader(extension, loader)
