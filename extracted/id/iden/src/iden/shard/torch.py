r"""Contain PyTorch-based shard implementations."""

from __future__ import annotations

__all__ = ["TorchShard", "create_torch_shard"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola.utils.path import sanitize_path
from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import JsonSaver, TorchLoader, TorchSaver
from iden.shard.file import FileShard

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class TorchShard(FileShard[T]):
    r"""Implement a PyTorch shard for efficient tensor storage.

    This shard stores data in PyTorch's native file format, optimized for
    ``torch.Tensor`` objects and PyTorch state dictionaries. The data are
    stored in a PyTorch file.

    Args:
        uri: The shard's URI.
        path: The path to the PyTorch file.

    Raises:
        RuntimeError: if ``torch`` is not installed.

    Example:
        ```pycon
        >>> import tempfile
        >>> import torch
        >>> from pathlib import Path
        >>> from iden.shard import TorchShard
        >>> from iden.io import TorchSaver
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.pt")
        ...     TorchSaver().save({"key1": torch.ones(2, 3), "key2": torch.arange(5)}, file)
        ...     shard = TorchShard(uri="file:///data/1234456789", path=file)
        ...     shard.get_data()
        ...
        {'key1': tensor([[1., 1., 1.], [1., 1., 1.]]), 'key2': tensor([0, 1, 2, 3, 4])}

        ```
    """

    def __init__(self, uri: str, path: Path | str) -> None:
        super().__init__(uri, path, loader=TorchLoader())

    @classmethod
    def generate_uri_config(cls, path: Path) -> dict[str, Any]:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            path: The path to the pickle file.

        Returns:
            The minimal config to load the shard from its URI.

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.shard import TorchShard
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     file = Path(tmpdir).joinpath("data.pt")
            ...     TorchShard.generate_uri_config(file)
            ...
            {'kwargs': {'path': '.../data.pt'},
             'loader': {'_target_': 'iden.shard.loader.TorchShardLoader'}}

            ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.TorchShardLoader"},
        }


def create_torch_shard(data: T, uri: str, path: Path | None = None) -> TorchShard[T]:
    r"""Create a ``TorchShard`` from data.

    Note:
        It is a utility function to create a ``TorchShard`` from its
            data and URI. It is possible to create a ``TorchShard``
            in other ways.

    Args:
        data: The data to save in the PyTorch file.
        uri: The shard's URI.
        path: The path to the PyTorch file. If ``None``, a path is
            automatically based on the URI.

    Returns:
        The ``TorchShard`` object.

    Raises:
        RuntimeError: if ``torch`` is not installed.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> import torch
        >>> from iden.shard import create_torch_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shard = create_torch_shard(
        ...         data={"key1": torch.ones(2, 3), "key2": torch.arange(5)},
        ...         uri=Path(tmpdir).joinpath("my_uri").as_uri(),
        ...     )
        ...     shard.get_data()
        ...
        {'key1': tensor([[1., 1., 1.], [1., 1., 1.]]), 'key2': tensor([0, 1, 2, 3, 4])}

        ```
    """
    if path is None:
        path = sanitize_path(uri + ".pt")
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(TorchShard.generate_uri_config(path), sanitize_path(uri))
    logger.info(f"Saving data in file {path}")
    TorchSaver().save(data, path)
    return TorchShard(uri, path)
