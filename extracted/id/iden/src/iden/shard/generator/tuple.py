r"""Contain tuple-based shard generator implementations."""

from __future__ import annotations

__all__ = ["ShardTupleGenerator"]

from typing import TYPE_CHECKING, TypeVar

from coola.utils import repr_indent, repr_mapping

from iden.shard import BaseShard, ShardTuple, create_shard_tuple
from iden.shard.generator.base import BaseShardGenerator, setup_shard_generator

T = TypeVar("T")

if TYPE_CHECKING:
    from pathlib import Path


class ShardTupleGenerator(BaseShardGenerator[tuple[BaseShard[T], ...]]):
    r"""Implement a ``ShardTuple`` generator.

    Args:
        shard: The shard generator or its configuration.
        num_shards: The number of shards to generate in the
            ``ShardTuple``.
        path_uri: The path where to save the URI file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> import torch
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import ShardTupleGenerator, JsonShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = ShardTupleGenerator(
    ...         shard=JsonShardGenerator(
    ...             data=DataGenerator([1, 2, 3]),
    ...             path_uri=Path(tmpdir).joinpath("uri"),
    ...             path_shard=Path(tmpdir).joinpath("data"),
    ...         ),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         num_shards=5,
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    ShardTupleGenerator(
      (path_uri): PosixPath('/.../uri')
      (num_shards): 5
      (shard): JsonShardGenerator(
          (path_uri): PosixPath('/.../uri')
          (path_shard): PosixPath('/.../data')
          (data): DataGenerator(copy=False)
        )
    )
    ShardTuple(
      (uri): file:///.../uri/shard1
      (shards):
        (0): JsonShard(uri=file:///.../uri/000000001)
        (1): JsonShard(uri=file:///.../uri/000000002)
        (2): JsonShard(uri=file:///.../uri/000000003)
        (3): JsonShard(uri=file:///.../uri/000000004)
        (4): JsonShard(uri=file:///.../uri/000000005)
    )

    ```
    """

    def __init__(
        self, shard: BaseShardGenerator[T] | dict, num_shards: int, path_uri: Path
    ) -> None:
        self._shard = setup_shard_generator(shard)
        self._num_shards = num_shards
        self._path_uri = path_uri

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "path_uri": self._path_uri,
                    "num_shards": self._num_shards,
                    "shard": self._shard,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def generate(self, shard_id: str) -> ShardTuple[T]:
        shards = [self._shard.generate(f"{i + 1:09}") for i in range(self._num_shards)]
        return create_shard_tuple(uri=self._path_uri.joinpath(shard_id).as_uri(), shards=shards)
