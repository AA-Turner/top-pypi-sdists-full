r"""Contain safetensors shard generator implementations."""

from __future__ import annotations

__all__ = ["NumpySafetensorsShardGenerator", "TorchSafetensorsShardGenerator"]

from typing import TYPE_CHECKING, TypeVar
from unittest.mock import Mock

from coola.utils.imports import (
    check_numpy,
    check_torch,
    is_numpy_available,
    is_torch_available,
)

from iden.shard import (
    NumpySafetensorsShard,
    TorchSafetensorsShard,
    create_numpy_safetensors_shard,
    create_torch_safetensors_shard,
)
from iden.shard.generator.file import BaseFileShardGenerator
from iden.utils.imports import check_safetensors

if is_numpy_available():
    import numpy as np
else:  # pragma: no cover
    np = Mock()

if is_torch_available():
    import torch
else:  # pragma: no cover
    torch = Mock()

if TYPE_CHECKING:
    from pathlib import Path

    from iden.data.generator import BaseDataGenerator

T = TypeVar("T")


class NumpySafetensorsShardGenerator(BaseFileShardGenerator[dict[str, np.ndarray]]):
    r"""Implement a safetensors shard generator.

    Args:
        data: The data to save in the shard.
        path_uri: The path where to save the URI file.
        path_shard: The path where to save the shard data.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> import numpy as np
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import NumpySafetensorsShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = NumpySafetensorsShardGenerator(
    ...         data=DataGenerator({"key1": np.ones((2, 3)), "key2": np.arange(5)}),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         path_shard=Path(tmpdir).joinpath("data"),
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    NumpySafetensorsShardGenerator(
      (path_uri): PosixPath('/.../uri')
      (path_shard): PosixPath('/.../data')
      (data): DataGenerator(copy=False)
    )
    NumpySafetensorsShard(uri=file:///.../uri/shard1)

    ```
    """

    def __init__(
        self,
        path_uri: Path,
        path_shard: Path,
        data: BaseDataGenerator[dict[str, np.ndarray]] | dict,
    ) -> None:
        check_safetensors()
        check_numpy()
        super().__init__(path_uri=path_uri, path_shard=path_shard, data=data)

    def _generate(self, data: dict[str, np.ndarray], shard_id: str) -> NumpySafetensorsShard:
        return create_numpy_safetensors_shard(
            data=data,
            uri=self._path_uri.joinpath(shard_id).as_uri(),
            path=self._path_shard.joinpath(shard_id).with_suffix(".safetensors"),
        )


class TorchSafetensorsShardGenerator(BaseFileShardGenerator[dict[str, torch.Tensor]]):
    r"""Implement a safetensors shard generator.

    Args:
        data: The data to save in the shard.
        path_uri: The path where to save the URI file.
        path_shard: The path where to save the shard data.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> import torch
    >>> from pathlib import Path
    >>> from iden.data.generator import DataGenerator
    >>> from iden.shard.generator import TorchSafetensorsShardGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = TorchSafetensorsShardGenerator(
    ...         data=DataGenerator({"key1": torch.ones(2, 3), "key2": torch.arange(5)}),
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         path_shard=Path(tmpdir).joinpath("data"),
    ...     )
    ...     generator
    ...     shard = generator.generate("shard1")
    ...     shard
    ...
    TorchSafetensorsShardGenerator(
      (path_uri): PosixPath('/.../uri')
      (path_shard): PosixPath('/.../data')
      (data): DataGenerator(copy=False)
    )
    TorchSafetensorsShard(uri=file:///.../uri/shard1)

    ```
    """

    def __init__(
        self,
        path_uri: Path,
        path_shard: Path,
        data: BaseDataGenerator[dict[str, torch.Tensor]] | dict,
    ) -> None:
        check_safetensors()
        check_torch()
        super().__init__(path_uri=path_uri, path_shard=path_shard, data=data)

    def _generate(self, data: dict[str, torch.Tensor], shard_id: str) -> TorchSafetensorsShard:
        return create_torch_safetensors_shard(
            data=data,
            uri=self._path_uri.joinpath(shard_id).as_uri(),
            path=self._path_shard.joinpath(shard_id).with_suffix(".safetensors"),
        )
