r"""Contain joblib shard loader implementations."""

from __future__ import annotations

__all__ = ["JoblibShardLoader"]

from typing import Any, TypeVar

from iden.shard.joblib import JoblibShard
from iden.shard.loader.base import BaseShardLoader

T = TypeVar("T")


class JoblibShardLoader(BaseShardLoader[T]):
    r"""Implement a joblib shard loader for loading shards from joblib
    files.

    This loader reads shard configuration from a URI and instantiates a
    joblib shard with the specified data file path.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_joblib_shard
        >>> from iden.shard.loader import JoblibShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_joblib_shard([1, 2, 3], uri=uri)
        ...     loader = JoblibShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        JoblibShard(uri=file:///.../my_uri)

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> JoblibShard[T]:
        return JoblibShard.from_uri(uri)
