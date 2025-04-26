r"""Contain PyTorch shard loader implementations."""

from __future__ import annotations

__all__ = ["TorchShardLoader"]

from typing import Any

from coola.utils import check_torch

from iden.shard.loader.base import BaseShardLoader
from iden.shard.torch import TorchShard


class TorchShardLoader(BaseShardLoader[Any]):
    r"""Implement a PyTorch shard loader.

    Raises:
        RuntimeError: if ``torch`` is not installed.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_torch_shard
    >>> from iden.shard.loader import TorchShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_torch_shard([1, 2, 3], uri=uri)
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

    def load(self, uri: str) -> TorchShard:
        return TorchShard.from_uri(uri)
