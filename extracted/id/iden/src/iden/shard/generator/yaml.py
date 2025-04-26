r"""Contain YAML shard generator implementations."""

from __future__ import annotations

__all__ = ["YamlShardGenerator"]

from typing import TYPE_CHECKING, TypeVar

from iden.shard import YamlShard, create_yaml_shard
from iden.shard.generator.file import BaseFileShardGenerator
from iden.utils.imports import check_yaml

if TYPE_CHECKING:
    from pathlib import Path

    from iden.data.generator import BaseDataGenerator

T = TypeVar("T")


class YamlShardGenerator(BaseFileShardGenerator[T]):
    r"""Implement a YAML shard generator.

    Args:
        data: The data to save in the shard.
        path_uri: The path where to save the URI file.
        path_shard: The path where to save the shard data.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import YamlShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = YamlShardGenerator(
    ...         data=DataGenerator([1, 2, 3]),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         path_shard=Path(tmpdir).joinpath("data"),
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    YamlShardGenerator(
      (path_uri): PosixPath('/.../uri')
      (path_shard): PosixPath('/.../data')
      (data): DataGenerator(copy=False)
    )
    YamlShard(uri=file:///.../uri/shard1)

    ```
    """

    def __init__(self, data: BaseDataGenerator[T] | dict, path_uri: Path, path_shard: Path) -> None:
        check_yaml()
        super().__init__(data=data, path_uri=path_uri, path_shard=path_shard)

    def _generate(self, data: T, shard_id: str) -> YamlShard[T]:
        return create_yaml_shard(
            data=data,
            uri=self._path_uri.joinpath(shard_id).as_uri(),
            path=self._path_shard.joinpath(shard_id).with_suffix(".yaml"),
        )
