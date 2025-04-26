r"""Contain safetensors shard loader implementations."""

from __future__ import annotations

__all__ = ["NumpySafetensorsShardLoader", "TorchSafetensorsShardLoader"]

from unittest.mock import Mock

from coola.utils import check_numpy, check_torch, is_numpy_available, is_torch_available

from iden.shard.loader.base import BaseShardLoader
from iden.shard.safetensors import NumpySafetensorsShard, TorchSafetensorsShard
from iden.utils.imports import check_safetensors

if is_numpy_available():
    import numpy as np
else:  # pragma: no cover
    np = Mock()

if is_torch_available():
    import torch
else:  # pragma: no cover
    torch = Mock()


class NumpySafetensorsShardLoader(BaseShardLoader[dict[str, np.ndarray]]):
    r"""Implement a safetensors shard loader for ``numpy.ndarray``s.

    Raises:
        RuntimeError: if ``safetensors`` or ``numpy`` is not installed.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> import numpy as np
    >>> from pathlib import Path
    >>> from iden.shard import create_numpy_safetensors_shard
    >>> from iden.shard.loader import NumpySafetensorsShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_numpy_safetensors_shard(
    ...         {"key1": np.ones((2, 3)), "key2": np.arange(5)}, uri=uri
    ...     )
    ...     loader = NumpySafetensorsShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    NumpySafetensorsShard(uri=file:///.../my_uri)

    ```
    """

    def __init__(self) -> None:
        check_safetensors()
        check_numpy()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> NumpySafetensorsShard:
        return NumpySafetensorsShard.from_uri(uri)


class TorchSafetensorsShardLoader(BaseShardLoader[dict[str, torch.Tensor]]):
    r"""Implement a safetensors shard loader for ``torch.Tensor``s.

    Raises:
        RuntimeError: if ``safetensors`` or ``torch`` is not installed.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> import torch
    >>> from pathlib import Path
    >>> from iden.shard import create_torch_safetensors_shard
    >>> from iden.shard.loader import TorchSafetensorsShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_torch_safetensors_shard(
    ...         {"key1": torch.ones(2, 3), "key2": torch.arange(5)}, uri=uri
    ...     )
    ...     loader = TorchSafetensorsShardLoader()
    ...     shard = loader.load(uri)
    ...     shard
    ...
    TorchSafetensorsShard(uri=file:///.../my_uri)

    ```
    """

    def __init__(self) -> None:
        check_safetensors()
        check_torch()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> TorchSafetensorsShard:
        return TorchSafetensorsShard.from_uri(uri)
