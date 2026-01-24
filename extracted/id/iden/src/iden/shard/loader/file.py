r"""Contain file-based shard loader implementations."""

from __future__ import annotations

__all__ = ["FileShardLoader"]

from typing import Any, TypeVar

from iden.shard.file import FileShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class FileShardLoader(BaseShardLoader[T]):
    r"""Implement a file-based shard loader.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard
        >>> from iden.shard.loader import FileShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_json_shard([1, 2, 3], uri=uri)
        ...     loader = FileShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        JsonShard(uri=file:///.../my_uri)

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> FileShard[T]:
        return FileShard.from_uri(uri)
