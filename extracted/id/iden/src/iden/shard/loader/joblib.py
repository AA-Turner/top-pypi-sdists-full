r"""Contain joblib shard loader implementations."""

from __future__ import annotations

__all__ = ["JoblibShardLoader"]

from typing import Any, TypeVar

from iden.shard.joblib import JoblibShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class JoblibShardLoader(BaseShardLoader[Any]):
    r"""Implement a joblib shard loader.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_joblib_shard
    >>> from iden.shard.loader import JoblibShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_joblib_shard([1, 2, 3], uri=uri)
    ...     loader = JoblibShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    JoblibShard(uri=file:///.../my_uri)

    ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> JoblibShard:
        return JoblibShard.from_uri(uri)
