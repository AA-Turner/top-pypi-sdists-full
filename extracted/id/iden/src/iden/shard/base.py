r"""Contain the base class to implement a shard object."""

from __future__ import annotations

__all__ = ["BaseShard"]

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseShard(Generic[T], ABC):
    r"""Define the base class to implement a shard.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_json
    >>> from iden.shard import JsonShard
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("uri/0001").as_uri()
    ...     file = Path(tmpdir).joinpath("data.json")
    ...     save_json([1, 2, 3], file)
    ...     shard = JsonShard(uri=uri, path=file)
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    @abstractmethod
    def clear(self) -> None:
        r"""Clear the current shard cache i.e. remove from memory the
        data if possible.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json
        >>> from iden.shard import JsonShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("uri/0001").as_uri()
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     save_json([1, 2, 3], file)
        ...     shard = JsonShard(uri=uri, path=file)
        ...     data = shard.get_data(cache=True)
        ...     data
        ...     data.append(4)  # in-place modification
        ...     data = shard.get_data()
        ...     data
        ...     shard.clear()
        ...     data = shard.get_data()
        ...     data
        ...
        [1, 2, 3]
        [1, 2, 3, 4]
        [1, 2, 3]

        ```
        """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two shards are equal or not.

        Args:
            other: The object to compare with.
            equal_nan: If ``True``, then two ``NaN``s will be
                considered equal.

        Returns:
            ``True`` if the two shards are equal, otherwise ``False``.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import JsonShard, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri1 = Path(tmpdir).joinpath("my_uri1").as_uri()
        ...     uri2 = Path(tmpdir).joinpath("my_uri2").as_uri()
        ...     shard1 = create_json_shard([1, 2, 3], uri=uri1)
        ...     shard2 = create_json_shard([4, 5, 6], uri=uri2)
        ...     shard3 = JsonShard.from_uri(uri=uri1)
        ...     shard1.equal(shard2)
        ...     shard1.equal(shard3)
        ...
        False
        True

        ```
        """

    @abstractmethod
    def get_data(self, cache: bool = False) -> T:
        r"""Get the data in the shard.

        Args:
            cache: If ``True``, the shard will cache the data when the
                data are loaded the first time.

        Returns:
            The data in the shard.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json
        >>> from iden.shard import JsonShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("uri/0001").as_uri()
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     save_json([1, 2, 3], file)
        ...     shard = JsonShard(uri=uri, path=file)
        ...     shard.get_data()
        ...
        [1, 2, 3]

        ```
        """

    @abstractmethod
    def get_uri(self) -> str | None:
        r"""Get the Uniform Resource Identifier (URI) of the shard.

        Returns:
            The Uniform Resource Identifier (URI).

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json
        >>> from iden.shard import JsonShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("uri/0001").as_uri()
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     save_json([1, 2, 3], file)
        ...     shard = JsonShard(uri=uri, path=file)
        ...     shard.get_uri()
        ...
        'file:///.../uri/0001'

        ```
        """

    @abstractmethod
    def is_cached(self) -> bool:
        r"""Indicate if the data in the shard are cached or not.

        Returns:
            ``True`` if the data are cached, otherwise ``False``.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json
        >>> from iden.shard import JsonShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("uri/0001").as_uri()
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     save_json([1, 2, 3], file)
        ...     shard = JsonShard(uri=uri, path=file)
        ...     shard.is_cached()
        ...     data = shard.get_data(cache=True)
        ...     shard.is_cached()
        ...     shard.clear()
        ...     shard.is_cached()
        ...
        False
        True
        False

        ```
        """
