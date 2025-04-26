r"""Contain shard loader implementations."""

from __future__ import annotations

__all__ = ["ShardTupleLoader"]


from iden.shard.base import BaseShard
from iden.shard.loader.base import BaseShardLoader
from iden.shard.tuple import ShardTuple


class ShardTupleLoader(BaseShardLoader[tuple[BaseShard, ...]]):
    r"""Implement a ``ShardTuple`` loader.

    Example usage:

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
    ...     _ = create_shard_tuple(shards, uri=uri)
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

    def load(self, uri: str) -> ShardTuple:
        return ShardTuple.from_uri(uri)
