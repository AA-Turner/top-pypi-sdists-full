r"""Contain cloudpickle shard loader implementations."""

from __future__ import annotations

__all__ = ["CloudpickleShardLoader"]

from typing import Any, TypeVar

from iden.shard.cloudpickle import CloudpickleShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class CloudpickleShardLoader(BaseShardLoader[Any]):
    r"""Implement a cloudpickle shard loader.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_cloudpickle_shard
    >>> from iden.shard.loader import CloudpickleShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_cloudpickle_shard([1, 2, 3], uri=uri)
    ...     loader = CloudpickleShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    CloudpickleShard(uri=file:///.../my_uri)

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> CloudpickleShard:
        return CloudpickleShard.from_uri(uri)
