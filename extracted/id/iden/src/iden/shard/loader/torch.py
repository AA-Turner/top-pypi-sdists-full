r"""Contain PyTorch shard loader implementations."""

from __future__ import annotations

__all__ = ["TorchShardLoader"]

from typing import Any, TypeVar

from coola.utils import check_torch

from iden.shard.loader.base import BaseShardLoader
from iden.shard.torch import TorchShard

T = TypeVar("T")


class TorchShardLoader(BaseShardLoader[T]):
    r"""Implement a PyTorch shard loader for loading shards from PyTorch
    files.

    This loader reads shard configuration from a URI and instantiates a
    PyTorch shard with the specified data file path.

    Raises:
        RuntimeError: if ``torch`` is not installed.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_torch_shard
        >>> from iden.shard.loader import TorchShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     create_torch_shard([1, 2, 3], uri=uri)
        ...     loader = TorchShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        TorchShard(uri=file:///.../my_uri)

        ```
    """

    def __init__(self) -> None:
        check_torch()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, uri: str) -> TorchShard[T]:
        return TorchShard.from_uri(uri)
