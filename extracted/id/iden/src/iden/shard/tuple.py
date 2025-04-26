r"""Contain a shard to manage a tuple of shards."""

from __future__ import annotations

__all__ = ["ShardTuple", "create_shard_tuple"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola import objects_are_equal
from coola.utils import (
    repr_indent,
    repr_mapping,
    repr_sequence,
    str_indent,
    str_mapping,
    str_sequence,
)
from objectory import OBJECT_TARGET

from iden.constants import LOADER, SHARDS
from iden.io import JsonSaver, load_json
from iden.shard.base import BaseShard
from iden.shard.utils import get_list_uris
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T")

logger = logging.getLogger(__name__)


class ShardTuple(BaseShard[tuple[BaseShard[T], ...]]):
    r"""Implement a data structure to manage a tuple of shards.

    Args:
        uri: The shard's URI.
        shards: The tuple of shards.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard
    >>> from iden.shard import ShardTuple
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = [
    ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shards/uri1").as_uri()),
    ...         create_json_shard(
    ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shards/uri2").as_uri()
    ...         ),
    ...     ]
    ...     sl = ShardTuple(uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards)
    ...     sl
    ...
    ShardTuple(
      (uri): file:///.../uri
      (shards):
        (0): JsonShard(uri=file:///.../shards/uri1)
        (1): JsonShard(uri=file:///.../shards/uri2)
    )

    ```
    """

    def __init__(self, uri: str, shards: Iterable[BaseShard[T]]) -> None:
        self._uri = uri
        self._shards = tuple(shards)

    def __getitem__(self, index: int) -> BaseShard[T]:
        return self._shards[index]

    def __len__(self) -> int:
        return len(self._shards)

    def __repr__(self) -> str:
        shards = f"\n{repr_sequence(self._shards)}" if self._shards else ""
        args = repr_indent(repr_mapping({"uri": self._uri, "shards": shards}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        shards = f"\n{str_sequence(self._shards)}" if self._shards else ""
        args = str_indent(str_mapping({"uri": self._uri, "shards": shards}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def clear(self) -> None:
        for shard in self._shards:
            shard.clear()

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(
            self.get_uri(), other.get_uri(), equal_nan=equal_nan
        ) and objects_are_equal(self.get_data(), other.get_data(), equal_nan=equal_nan)

    def get(self, index: int) -> BaseShard[T]:
        r"""Get a shard.

        Args:
            index: The shard index to get.

        Returns:
            The shard.

        Raises:
            IndexError: if the index is outside  the tuple range.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard
        >>> from iden.shard import ShardTuple
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     sl = ShardTuple(uri=Path(tmpdir).joinpath("main_uri").as_uri(), shards=shards)
        ...     sl.get(0)
        ...
        JsonShard(uri=file:///.../uri1)

        ```
        """
        return self[index]

    def get_data(self, cache: bool = False) -> tuple[BaseShard[T], ...]:  # noqa: ARG002
        return self._shards

    def get_uri(self) -> str:
        return self._uri

    def is_cached(self) -> bool:
        return any(shard.is_cached() for shard in self._shards)

    def is_sorted_by_uri(self) -> bool:
        r"""Indicate if the shards are sorted by ascending order of URIs
        or not.

        Returns:
            ``True`` if the shards are sorted by ascending order of
                URIs, otherwise ``False``.
        """
        uris = get_list_uris(self._shards)
        return uris == sorted(uris)

    @classmethod
    def from_uri(cls, uri: str) -> ShardTuple[T]:
        r"""Instantiate a shard from its URI.

        Args:
            uri: The URI.

        Returns:
            The instantiated shard.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import ShardTuple, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     uri = Path(tmpdir).joinpath("uri").as_uri()
        ...     create_shard_tuple(shards, uri=uri)
        ...     shard = ShardTuple.from_uri(uri)
        ...     shard
        ...
        ShardTuple(
          (uri): file:///.../uri
          (shards):
            (0): JsonShard(uri=file:///.../shard/uri1)
            (1): JsonShard(uri=file:///.../shard/uri2)
        )

        ```
        """
        # local import to avoid cyclic dependencies
        from iden.shard.loading import load_from_uri

        config = load_json(sanitize_path(uri))
        shards = [load_from_uri(shard) for shard in config[SHARDS]]
        return cls(uri=uri, shards=shards)

    @classmethod
    def generate_uri_config(cls, shards: Iterable[BaseShard[T]]) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            shards: The shards.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import ShardTuple, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     ShardTuple.generate_uri_config(shards)
        ...
        {'shards': ['file:///.../shard/uri1', 'file:///.../shard/uri2'],
         'loader': {'_target_': 'iden.shard.loader.ShardTupleLoader'}}

        ```
        """
        return {
            SHARDS: get_list_uris(shards),
            LOADER: {OBJECT_TARGET: "iden.shard.loader.ShardTupleLoader"},
        }


def create_shard_tuple(shards: Iterable[BaseShard[T]], uri: str) -> ShardTuple[T]:
    r"""Create a ``ShardTuple`` a list of shards.

    Note:
        It is a utility function to create a ``ShardTuple`` from its
            shards and URI. It is possible to create a ``ShardTuple``
            in other ways.

    Args:
        shards: The shards.
        uri: The shard's URI.

    Returns:
        The ``ShardTuple`` object.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import ShardTuple, create_json_shard, create_shard_tuple
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = [
    ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
    ...         create_json_shard(
    ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
    ...         ),
    ...     ]
    ...     shard = create_shard_tuple(shards, uri=Path(tmpdir).joinpath("uri").as_uri())
    ...     shard
    ...
    ShardTuple(
      (uri): file:///.../uri
      (shards):
        (0): JsonShard(uri=file:///.../shard/uri1)
        (1): JsonShard(uri=file:///.../shard/uri2)
    )

    ```
    """
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(ShardTuple.generate_uri_config(shards), sanitize_path(uri))
    return ShardTuple(uri, shards)
