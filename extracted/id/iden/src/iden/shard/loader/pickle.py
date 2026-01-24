r"""Contain pickle shard loader implementations."""

from __future__ import annotations

__all__ = ["PickleShardLoader"]

from typing import Any, TypeVar

from iden.shard.loader.base import BaseShardLoader
from iden.shard.pickle import PickleShard

T = TypeVar("T")


class PickleShardLoader(BaseShardLoader[T]):
    r"""Implement a pickle shard loader for loading shards from pickle
    files.

    This loader reads shard configuration from a URI and instantiates a
    pickle shard with the specified data file path.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_pickle_shard
        >>> from iden.shard.loader import PickleShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_pickle_shard([1, 2, 3], uri=uri)
        ...     loader = PickleShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        PickleShard(uri=file:///.../my_uri)

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> PickleShard[T]:
        return PickleShard.from_uri(uri)
