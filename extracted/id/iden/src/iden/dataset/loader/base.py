r"""Contain the base class to implement a dataset loader object."""

from __future__ import annotations

__all__ = ["BaseDatasetLoader", "is_dataset_loader_config", "setup_dataset_loader"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    from iden.dataset import BaseDataset

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseDatasetLoader(Generic[T], ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a dataset loader.

    A dataset loader object allows to load a ``BaseDataset`` object from
    its Uniform Resource Identifier (URI).

    Example usage:

    ```pycon
    >>> from iden.dataset.loader import VanillaDatasetLoader
    >>> loader = VanillaDatasetLoader()
    >>> loader
    VanillaDatasetLoader()

    ```
    """

    @abstractmethod
    def load(self, uri: str) -> BaseDataset[T]:
        r"""Load a dataset from its Uniform Resource Identifier (URI).

        Args:
            uri: The URI of the dataset to load.

        Returns:
            The loaded dataset.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.dataset import create_vanilla_dataset
        >>> from iden.dataset.loader import VanillaDatasetLoader
        >>> from iden.shard import create_json_shard, create_shard_dict, create_shard_tuple
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = create_shard_dict(
        ...         shards={
        ...             "train": create_shard_tuple(
        ...                 [
        ...                     create_json_shard(
        ...                         [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...                     ),
        ...                     create_json_shard(
        ...                         [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...                     ),
        ...                 ],
        ...                 uri=Path(tmpdir).joinpath("uri_train").as_uri(),
        ...             ),
        ...             "val": create_shard_tuple(
        ...                 shards=[],
        ...                 uri=Path(tmpdir).joinpath("uri_val").as_uri(),
        ...             ),
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_shards").as_uri(),
        ...     )
        ...     assets = create_shard_dict(
        ...         shards={
        ...             "stats": create_json_shard(
        ...                 [1, 2, 3], uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     uri = Path(tmpdir).joinpath("uri").as_uri()
        ...     _ = create_vanilla_dataset(uri=uri, shards=shards, assets=assets)
        ...     loader = VanillaDatasetLoader()
        ...     dataset = loader.load(uri)
        ...     dataset
        ...
        VanillaDataset(
          (uri): file:///.../uri
          (shards): ShardDict(
              (uri): file:///.../uri_shards
              (shards):
                (train): ShardTuple(
                    (uri): file:///.../uri_train
                    (shards):
                      (0): JsonShard(uri=file:///.../shard/uri1)
                      (1): JsonShard(uri=file:///.../shard/uri2)
                  )
                (val): ShardTuple(
                    (uri): file:///.../uri_val
                    (shards):
                  )
            )
          (assets): ShardDict(
              (uri): file:///.../uri_assets
              (shards):
                (stats): JsonShard(uri=file:///.../uri_stats)
            )
        )

        ```
        """


def is_dataset_loader_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseDatasetLoader``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: Specifies the configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseDatasetLoader`` object.

    Example usage:

    ```pycon
    >>> from iden.dataset.loader import is_dataset_loader_config
    >>> is_dataset_loader_config({"_target_": "iden.dataset.loader.VanillaDatasetLoader"})
    True

    ```
    """
    return is_object_config(config, BaseDatasetLoader)


def setup_dataset_loader(dataset_loader: BaseDatasetLoader | dict) -> BaseDatasetLoader:
    r"""Set up a dataset loader.

    The dataset loader is instantiated from its configuration by using the
    ``BaseDatasetLoader`` factory function.

    Args:
        dataset_loader: Specifies the dataset loader or its configuration.

    Returns:
        The instantiated dataset loader.

    Example usage:

    ```pycon
    >>> from iden.dataset.loader import setup_dataset_loader
    >>> dataset_loader = setup_dataset_loader(
    ...     {"_target_": "iden.dataset.loader.VanillaDatasetLoader"}
    ... )
    >>> dataset_loader
    VanillaDatasetLoader()

    ```
    """
    if isinstance(dataset_loader, dict):
        logger.debug("Initializing a dataset loader from its configuration...")
        dataset_loader = BaseDatasetLoader.factory(**dataset_loader)
    if not isinstance(dataset_loader, BaseDatasetLoader):
        logger.warning(
            f"dataset loader is not a BaseDatasetLoader (received: {type(dataset_loader)})"
        )
    return dataset_loader
