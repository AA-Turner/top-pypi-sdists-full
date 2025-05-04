r"""Contain joblib shard generator implementations."""

from __future__ import annotations

__all__ = ["JoblibShardGenerator"]

from typing import TypeVar

from iden.shard import JoblibShard, create_joblib_shard
from iden.shard.generator.file import BaseFileShardGenerator

T = TypeVar("T")


class JoblibShardGenerator(BaseFileShardGenerator[T]):
    r"""Implement a joblib shard generator.

    Args:
        data: The data to save in the shard.
        path_uri: The path where to save the URI file.
        path_shard: The path where to save the shard data.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import JoblibShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = JoblibShardGenerator(
    ...         data=DataGenerator([1, 2, 3]),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         path_shard=Path(tmpdir).joinpath("data"),
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    JoblibShardGenerator(
      (path_uri): PosixPath('/.../uri')
      (path_shard): PosixPath('/.../data')
      (data): DataGenerator(copy=False)
    )
    JoblibShard(uri=file:///.../uri/shard1)

    ```
    """

    def _generate(self, data: T, shard_id: str) -> JoblibShard[T]:
        return create_joblib_shard(
            data=data,
            uri=self._path_uri.joinpath(shard_id).as_uri(),
            path=self._path_shard.joinpath(shard_id).with_suffix(".joblib"),
        )
