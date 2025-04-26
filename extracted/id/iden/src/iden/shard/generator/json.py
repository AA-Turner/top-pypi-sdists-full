r"""Contain JSON shard generator implementations."""

from __future__ import annotations

__all__ = ["JsonShardGenerator"]

from typing import TypeVar

from iden.shard import JsonShard, create_json_shard
from iden.shard.generator.file import BaseFileShardGenerator

T = TypeVar("T")


class JsonShardGenerator(BaseFileShardGenerator[T]):
    r"""Implement a JSON shard generator.

    Args:
        data: The data to save in the shard.
        path_uri: The path where to save the URI file.
        path_shard: The path where to save the shard data.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import JsonShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = JsonShardGenerator(
    ...         data=DataGenerator([1, 2, 3]),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         path_shard=Path(tmpdir).joinpath("data"),
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    JsonShardGenerator(
      (path_uri): PosixPath('/.../uri')
      (path_shard): PosixPath('/.../data')
      (data): DataGenerator(copy=False)
    )
    JsonShard(uri=file:///.../uri/shard1)

    ```
    """

    def _generate(self, data: T, shard_id: str) -> JsonShard[T]:
        return create_json_shard(
            data=data,
            uri=self._path_uri.joinpath(shard_id).as_uri(),
            path=self._path_shard.joinpath(shard_id).with_suffix(".json"),
        )
