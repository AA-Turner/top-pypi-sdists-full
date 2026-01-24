r"""Contain YAML shard loader implementations."""

from __future__ import annotations

__all__ = ["YamlShardLoader"]

from typing import Any, TypeVar

from iden.shard.loader.base import BaseShardLoader
from iden.shard.yaml import YamlShard
from iden.utils.imports import check_yaml

T = TypeVar("T")


class YamlShardLoader(BaseShardLoader[T]):
    r"""Implement a YAML shard loader for loading shards from YAML files.

    This loader reads shard configuration from a URI and instantiates a
    YAML shard with the specified data file path.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_yaml_shard
        >>> from iden.shard.loader import YamlShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_yaml_shard([1, 2, 3], uri=uri)
        ...     loader = YamlShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        YamlShard(uri=file:///.../my_uri)

        ```
    """

    def __init__(self) -> None:
        check_yaml()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> YamlShard[T]:
        return YamlShard.from_uri(uri)
