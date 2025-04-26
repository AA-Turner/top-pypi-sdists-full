r"""Contain shard loader implementations."""

from __future__ import annotations

__all__ = ["ShardDictLoader"]


from iden.shard.base import BaseShard
from iden.shard.dict import ShardDict
from iden.shard.loader.base import BaseShardLoader


class ShardDictLoader(BaseShardLoader[dict[str, BaseShard]]):
    r"""Implement a ``ShardDict`` loader.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard, create_shard_dict
    >>> from iden.shard.loader import ShardDictLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("uri").as_uri()
    ...     shards = {
    ...         "train": create_json_shard(
    ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
    ...         ),
    ...         "val": create_json_shard(
    ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
    ...         ),
    ...     }
    ...     _ = create_shard_dict(shards, uri=uri)
    ...     loader = ShardDictLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    ShardDict(
      (uri): file:///.../uri
      (shards):
        (train): JsonShard(uri=file:///.../shard/uri1)
        (val): JsonShard(uri=file:///.../shard/uri2)
    )

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> ShardDict:
        return ShardDict.from_uri(uri)
