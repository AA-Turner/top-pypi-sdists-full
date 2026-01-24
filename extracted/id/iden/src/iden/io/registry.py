r"""Define the data loader registry for automatically loading data based
on file extension.

This module provides a registry system that manages and dispatches
loaders based on file extensions.
"""

from __future__ import annotations

__all__ = ["LoaderRegistry"]

from typing import TYPE_CHECKING, Any

from coola.utils.format import repr_indent, repr_mapping, str_indent, str_mapping

from iden.io.base import BaseLoader

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path


class LoaderRegistry(BaseLoader[Any]):
    r"""Registry that manages and dispatches loaders based on file
    extension.

    This registry maps file extensions (e.g., "json", "txt") to loader instances
    that handle loading files with those extensions. It provides automatic
    dispatching to the appropriate loader based on a file's extension.

    Args:
        registry: Optional initial mapping of extensions to loaders. If provided,
            the registry is copied to prevent external mutations.

    Attributes:
        _registry: Internal mapping of registered extensions to loaders

    Example:
        Basic usage with JSON and text loaders:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json, LoaderRegistry, JsonLoader, TextLoader
        >>> registry = LoaderRegistry({"json": JsonLoader(), "txt": TextLoader()})
        >>> registry
        LoaderRegistry(
          (json): JsonLoader()
          (txt): TextLoader()
        )
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = registry.load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """

    def __init__(self, registry: dict[str, BaseLoader[Any]] | None = None) -> None:
        self._registry: dict[str, BaseLoader[Any]] = registry.copy() if registry else {}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(self._registry))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self._registry))}\n)"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, path: Path) -> Any:
        extension = "".join(path.suffixes)[1:]
        loader = self.find_loader(extension)
        return loader.load(path)

    def register(
        self,
        extension: str,
        loader: BaseLoader[Any],
        exist_ok: bool = False,
    ) -> None:
        r"""Register a loader for a given file extension.

        This method associates a loader instance with a specific file extension.
        When loading files with this extension, the registered loader will be used.

        Args:
            extension: The file extension to register (e.g., "json", "txt")
            loader: The loader instance that handles files with this extension
            exist_ok: If False (default), raises an error if the extension is already
                registered. If True, overwrites the existing registration silently.

        Raises:
            RuntimeError: If the extension is already registered and exist_ok is False

        Example:
            ```pycon
            >>> from iden.io import LoaderRegistry, JsonLoader
            >>> registry = LoaderRegistry()
            >>> registry.register("json", JsonLoader())
            >>> registry
            LoaderRegistry(
              (json): JsonLoader()
            )

            ```
        """
        if extension in self._registry and not exist_ok:
            msg = (
                f"Loader {self._registry[extension]} already registered "
                f"for extension '{extension}'. Use exist_ok=True to overwrite."
            )
            raise RuntimeError(msg)
        self._registry[extension] = loader

    def register_many(
        self,
        mapping: Mapping[str, BaseLoader[Any]],
        exist_ok: bool = False,
    ) -> None:
        r"""Register multiple loaders at once.

        This is a convenience method for bulk registration that internally calls
        register() for each extension-loader pair.

        Args:
            mapping: Dictionary mapping file extensions to loader instances
            exist_ok: If False (default), raises an error if any extension is already
                registered. If True, overwrites existing registrations silently.

        Raises:
            RuntimeError: If any extension is already registered and exist_ok is False

        Example:
            ```pycon
            >>> from iden.io import LoaderRegistry, JsonLoader, TextLoader
            >>> registry = LoaderRegistry()
            >>> registry.register_many({"json": JsonLoader(), "txt": TextLoader()})
            >>> registry
            LoaderRegistry(
              (json): JsonLoader()
              (txt): TextLoader()
            )

            ```
        """
        for ext, loader in mapping.items():
            self.register(ext, loader, exist_ok=exist_ok)

    def has_loader(self, extension: str) -> bool:
        r"""Check if a loader is registered for the given extension.

        Args:
            extension: The file extension to check (e.g., "json", "txt")

        Returns:
            True if a loader is registered for this extension, False otherwise

        Example:
            ```pycon
            >>> from iden.io import LoaderRegistry, JsonLoader
            >>> registry = LoaderRegistry()
            >>> registry.register("json", JsonLoader())
            >>> registry.has_loader("json")
            True
            >>> registry.has_loader("txt")
            False

            ```
        """
        return extension in self._registry

    def find_loader(self, extension: str) -> BaseLoader[Any]:
        r"""Find the appropriate loader for a given file extension.

        Args:
            extension: The file extension to find a loader for (e.g., "json", "txt")

        Returns:
            The loader registered for the given file extension

        Raises:
            ValueError: If no loader is registered for the extension

        Example:
            ```pycon
            >>> from iden.io import LoaderRegistry, JsonLoader
            >>> registry = LoaderRegistry()
            >>> registry.register("json", JsonLoader())
            >>> loader = registry.find_loader("json")
            >>> loader
            JsonLoader()

            ```
        """
        if (loader := self._registry.get(extension, None)) is not None:
            return loader
        msg = f"Incorrect extension: {extension}"
        raise ValueError(msg)
