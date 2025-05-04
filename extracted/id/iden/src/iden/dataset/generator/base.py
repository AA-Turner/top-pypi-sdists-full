r"""Contain the base class to implement a dataset generator."""

from __future__ import annotations

__all__ = ["BaseDatasetGenerator", "is_dataset_generator_config", "setup_dataset_generator"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    from iden.dataset import BaseDataset

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseDatasetGenerator(Generic[T], ABC, metaclass=AbstractFactory):
    r"""Define the base class to create a dataset.

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset.generator import VanillaDatasetGenerator
    >>> from iden.shard.generator import ShardDictGenerator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = VanillaDatasetGenerator(
    ...         path_uri=Path(tmpdir).joinpath("uri"),
    ...         shards=ShardDictGenerator(
    ...             path_uri=Path(tmpdir).joinpath("uri/shards"), shards={}
    ...         ),
    ...         assets=ShardDictGenerator(
    ...             path_uri=Path(tmpdir).joinpath("uri/assets"), shards={}
    ...         ),
    ...     )
    ...     generator
    ...     dataset = generator.generate("dataset1")
    ...     dataset
    ...
    VanillaDatasetGenerator(
      (path_uri): PosixPath('/.../uri')
      (shards): ShardDictGenerator(
          (path_uri): PosixPath('/.../uri/shards')
          (shards):
        )
      (assets): ShardDictGenerator(
          (path_uri): PosixPath('/.../uri/assets')
          (shards):
        )
    )
    VanillaDataset(
      (uri): file:///.../uri/dataset1
      (shards): ShardDict(
          (uri): file:///.../uri/shards/shards
          (shards):
        )
      (assets): ShardDict(
          (uri): file:///.../uri/assets/assets
          (shards):
        )
    )

    ```
    """

    @abstractmethod
    def generate(self, dataset_id: str) -> BaseDataset[T]:
        r"""Generate a dataset.

        Args:
            dataset_id: The dataset IDI.

        Returns:
            The generated dataset.

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.dataset.generator import VanillaDatasetGenerator
        >>> from iden.shard.generator import ShardDictGenerator
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     generator = VanillaDatasetGenerator(
        ...         path_uri=Path(tmpdir).joinpath("uri"),
        ...         shards=ShardDictGenerator(
        ...             path_uri=Path(tmpdir).joinpath("uri/shards"), shards={}
        ...         ),
        ...         assets=ShardDictGenerator(
        ...             path_uri=Path(tmpdir).joinpath("uri/assets"), shards={}
        ...         ),
        ...     )
        ...     dataset = generator.generate("dataset1")
        ...     dataset
        ...
        VanillaDataset(
          (uri): file:///.../uri/dataset1
          (shards): ShardDict(
              (uri): file:///.../uri/shards/shards
              (shards):
            )
          (assets): ShardDict(
              (uri): file:///.../uri/assets/assets
              (shards):
            )
        )

        ```
        """


def is_dataset_generator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseDatasetGenerator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseDatasetGenerator`` object.

    Example usage:

    ```pycon

    >>> from iden.dataset.generator import is_dataset_generator_config
    >>> is_dataset_generator_config(
    ...     {"_target_": "iden.dataset.generator.VanillaDatasetGenerator"}
    ... )
    True

    ```
    """
    return is_object_config(config, BaseDatasetGenerator)


def setup_dataset_generator(
    dataset_generator: BaseDatasetGenerator[T] | dict,
) -> BaseDatasetGenerator[T]:
    r"""Set up a dataset generator.

    The dataset generator is instantiated from its configuration by using the
    ``BaseDatasetGenerator`` factory function.

    Args:
        dataset_generator: The dataset generator or its configuration.

    Returns:
        The instantiated dataset generator.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset.generator import setup_dataset_generator
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     generator = setup_dataset_generator(
    ...         {
    ...             "_target_": "iden.dataset.generator.VanillaDatasetGenerator",
    ...             "path_uri": Path(tmpdir).joinpath("uri"),
    ...             "shards": {
    ...                 "_target_": "iden.shard.generator.ShardDictGenerator",
    ...                 "path_uri": Path(tmpdir).joinpath("uri/shards"),
    ...                 "shards": {},
    ...             },
    ...             "assets": {
    ...                 "_target_": "iden.shard.generator.ShardDictGenerator",
    ...                 "path_uri": Path(tmpdir).joinpath("uri/assets"),
    ...                 "shards": {},
    ...             },
    ...         }
    ...     )
    ...     generator
    ...
    VanillaDatasetGenerator(
      (path_uri): PosixPath('/.../uri')
      (shards): ShardDictGenerator(
          (path_uri): PosixPath('/.../uri/shards')
          (shards):
        )
      (assets): ShardDictGenerator(
          (path_uri): PosixPath('/.../uri/assets')
          (shards):
        )
    )

    ```
    """
    if isinstance(dataset_generator, dict):
        logger.debug("Initializing a dataset generator from its configuration...")
        dataset_generator = BaseDatasetGenerator.factory(**dataset_generator)
    if not isinstance(dataset_generator, BaseDatasetGenerator):
        logger.warning(
            f"dataset generator is not a BaseDatasetGenerator (received: {type(dataset_generator)})"
        )
    return dataset_generator
