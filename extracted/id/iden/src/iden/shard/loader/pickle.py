r"""Contain pickle shard loader implementations."""

from __future__ import annotations

__all__ = ["PickleShardLoader"]

from typing import Any, TypeVar

from iden.shard.loader.base import BaseShardLoader
from iden.shard.pickle import PickleShard

T = TypeVar("T")


class PickleShardLoader(BaseShardLoader[Any]):
    r"""Implement a pickle shard loader.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_pickle_shard
    >>> from iden.shard.loader import PickleShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_pickle_shard([1, 2, 3], uri=uri)
    ...     loader = PickleShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    PickleShard(uri=file:///.../my_uri)

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> PickleShard:
        return PickleShard.from_uri(uri)
