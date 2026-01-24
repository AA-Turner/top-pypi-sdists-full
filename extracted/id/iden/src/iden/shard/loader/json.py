r"""Contain JSON shard loader implementations."""

from __future__ import annotations

__all__ = ["JsonShardLoader"]

from typing import Any, TypeVar

from iden.shard.json import JsonShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class JsonShardLoader(BaseShardLoader[T]):
    r"""Implement a JSON shard loader for loading shards from JSON files.

    This loader reads shard configuration from a URI and instantiates a
    JSON shard with the specified data file path.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard
        >>> from iden.shard.loader import JsonShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_json_shard([1, 2, 3], uri=uri)
        ...     loader = JsonShardLoader()
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

    def load(self, uri: str) -> JsonShard[T]:
        return JsonShard.from_uri(uri)
