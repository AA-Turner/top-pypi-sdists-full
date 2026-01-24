r"""Contain shard loader implementations."""

from __future__ import annotations

__all__ = ["ShardTupleLoader"]

from typing import Any, TypeVar

from iden.shard.base import BaseShard
from iden.shard.loader.base import BaseShardLoader
from iden.shard.tuple import ShardTuple

T = TypeVar("T")


class ShardTupleLoader(BaseShardLoader[tuple[BaseShard[T], ...]]):
    r"""Implement a shard tuple loader for loading sequence-structured
    shards.

    This loader reads shard configuration from a URI and instantiates a
    ShardTuple containing an ordered sequence of shards.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, create_shard_tuple
        >>> from iden.shard.loader import ShardTupleLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("uri").as_uri()
        ...     shards = [
        ...         create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()),
        ...         create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     ]
        ...     create_shard_tuple(shards, uri=uri)
        ...     loader = ShardTupleLoader()
        ...     shard = loader.load(uri)
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

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> ShardTuple[T]:
        return ShardTuple.from_uri(uri)
