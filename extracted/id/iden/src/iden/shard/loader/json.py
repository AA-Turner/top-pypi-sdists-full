r"""Contain JSON shard loader implementations."""

from __future__ import annotations

__all__ = ["JsonShardLoader"]

from typing import Any, TypeVar

from iden.shard.json import JsonShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class JsonShardLoader(BaseShardLoader[Any]):
    r"""Implement a JSON shard loader.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard
    >>> from iden.shard.loader import JsonShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_json_shard([1, 2, 3], uri=uri)
    ...     loader = JsonShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    JsonShard(uri=file:///.../my_uri)

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> JsonShard:
        return JsonShard.from_uri(uri)
