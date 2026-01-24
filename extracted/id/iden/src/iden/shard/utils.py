r"""Contain utility functions and classes for working with shards."""

from __future__ import annotations

__all__ = ["ShardIterable", "get_dict_uris", "get_list_uris", "sort_by_uri"]

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from iden.shard import BaseShard

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from iden.shard.base import BaseShard

T = TypeVar("T")


class ShardIterable(Generic[T]):
    r"""Implement a shard iterable that loads and clears the data
    automatically.

    Args:
        iterable: The shard iterable.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard
        >>> from iden.shard.utils import ShardIterable
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     data = list(ShardIterable(shards))
        ...     data
        ...
        [[1, 2, 3], [4, 5, 6, 7]]

        ```
    """

    def __init__(self, iterable: Iterable[BaseShard[T]]) -> None:
        self._iterable = iterable

    def __iter__(self) -> Iterator[T]:
        for shard in self._iterable:
            yield shard.get_data()
            shard.clear()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"


def get_dict_uris(shards: dict[str, BaseShard[Any]]) -> dict[str, str]:
    r"""Get the dictionary of shard URIs.

    Args:
        shards: The dictionary of shards.

    Returns:
        The dictionary of shard URIs.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, get_dict_uris
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     get_dict_uris(shards)
        ...
        {'train': 'file:///.../shard/uri1', 'val': 'file:///.../shard/uri2'}

        ```
    """
    return {key: shard.get_uri() for key, shard in shards.items()}


def get_list_uris(shards: Iterable[BaseShard[Any]]) -> list[str]:
    r"""Get the list of shard URIs.

    Args:
        shards: The iterable of shards from which to extract URIs.

    Returns:
        The list of shard URIs.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import get_list_uris, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     get_list_uris(shards)
        ...
        ['file:///.../shard/uri1', 'file:///.../shard/uri2']

        ```
    """
    return [shard.get_uri() for shard in shards]


def sort_by_uri(
    shards: Iterable[BaseShard[Any]], /, *, reverse: bool = False
) -> list[BaseShard[Any]]:
    r"""Sort a sequence of shards by their URIs.

    Args:
        shards: The shards to sort.
        reverse: If set to ``True``, then the list elements are sorted
            as if each comparison were reversed.

    Returns:
        The sorted shards.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, sort_by_uri
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = sort_by_uri(
        ...         [
        ...             create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("uri2").as_uri()),
        ...             create_json_shard([4, 5, 6, 7], uri=Path(tmpdir).joinpath("uri3").as_uri()),
        ...             create_json_shard([4, 5, 6, 7], uri=Path(tmpdir).joinpath("uri1").as_uri()),
        ...         ]
        ...     )
        ...     shards
        ...
        [JsonShard(uri=file:///.../uri1), JsonShard(uri=file:///.../uri2), JsonShard(uri=file:///.../uri3)]

        ```
    """
    return sorted(shards, key=lambda item: item.get_uri(), reverse=reverse)
