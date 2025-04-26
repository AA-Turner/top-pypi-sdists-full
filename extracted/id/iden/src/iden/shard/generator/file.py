r"""Contain file-based shard generator implementations."""

from __future__ import annotations

__all__ = ["BaseFileShardGenerator"]

from abc import abstractmethod
from typing import TYPE_CHECKING, TypeVar

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from iden.data.generator import BaseDataGenerator, setup_data_generator
from iden.shard.generator.base import BaseShardGenerator

if TYPE_CHECKING:
    from pathlib import Path

    from iden.shard import BaseShard, JsonShard

T = TypeVar("T")


class BaseFileShardGenerator(BaseShardGenerator[T]):
    r"""Implement a JSON shard generator.

    Args:
        data: The data generator or its configuration.
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

    def __init__(self, path_uri: Path, path_shard: Path, data: BaseDataGenerator[T] | dict) -> None:
        self._data = setup_data_generator(data)
        self._path_uri = path_uri
        self._path_shard = path_shard

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {"path_uri": self._path_uri, "path_shard": self._path_shard, "data": self._data}
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {"path_uri": self._path_uri, "path_shard": self._path_shard, "data": self._data}
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def generate(self, shard_id: str) -> BaseShard[T]:
        data = self._data.generate()
        return self._generate(data=data, shard_id=shard_id)

    @abstractmethod
    def _generate(self, data: T, shard_id: str) -> JsonShard[T]:
        r"""Generate a shard based on the data and shard ID.

        Args:
            data: The data to save in the shard.
            shard_id: The shard IDI.

        Returns:
            The generated shard.
        """
