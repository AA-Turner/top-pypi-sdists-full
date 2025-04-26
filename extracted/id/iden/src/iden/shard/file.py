r"""Contain file-based shard implementations."""

from __future__ import annotations

__all__ = ["FileShard"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola import objects_are_equal
from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import AutoFileLoader, BaseLoader, load_json, setup_loader
from iden.shard.base import BaseShard
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T")


class FileShard(BaseShard[T]):
    r"""Implement a generic shard where the data are stored in a single
    file.

    Args:
        uri: The shard's URI.
        path: Specifies the path to the pickle file.
        loader: The data loader or its configuration.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import FileShard
    >>> from iden.io import save_json, JsonLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     file = Path(tmpdir).joinpath("data.json")
    ...     save_json([1, 2, 3], file)
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     shard = FileShard(uri=uri, path=file, loader=JsonLoader())
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    def __init__(
        self, uri: str, path: Path | str, loader: BaseLoader[T] | dict | None = None
    ) -> None:
        self._uri = uri
        self._path = sanitize_path(path)
        self._loader = setup_loader(loader or AutoFileLoader())

        self._is_cached = False
        self._data = None

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(uri={self.get_uri()})"

    @property
    def path(self) -> Path:
        r"""The path to the file with data."""
        return self._path

    def clear(self) -> None:
        self._is_cached = False
        self._data = None

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(
            self.get_uri(), other.get_uri(), equal_nan=equal_nan
        ) and objects_are_equal(self.path, other.path, equal_nan=equal_nan)

    def get_data(self, cache: bool = False) -> T:
        if not self._is_cached:
            data = self._loader.load(self._path)
            if cache:
                self._data = data
                self._is_cached = True
        else:
            data = self._data
        return data

    def get_uri(self) -> str:
        return self._uri

    def is_cached(self) -> bool:
        return self._is_cached

    @classmethod
    def from_uri(cls, uri: str) -> FileShard:
        r"""Instantiate a shard from its URI.

        Args:
            uri: The URI.

        Returns:
            The instantiated shard.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import FileShard, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     _ = create_json_shard([1, 2, 3], uri=uri)
        ...     shard = FileShard.from_uri(uri)
        ...     shard
        ...
        FileShard(uri=file:///.../my_uri)

        ```
        """
        config = load_json(sanitize_path(uri))
        return cls(uri=uri, **config[KWARGS])

    @classmethod
    def generate_uri_config(cls, path: Path) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            path: The path to the json file.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import FileShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     FileShard.generate_uri_config(file)
        ...
        {'kwargs': {'path': '.../data.json'},
         'loader': {'_target_': 'iden.shard.loader.FileShardLoader'}}

        ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.FileShardLoader"},
        }
