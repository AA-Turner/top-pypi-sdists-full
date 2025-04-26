r"""Contain the base class to implement a shard loader object."""

from __future__ import annotations

__all__ = ["BaseShardLoader", "is_shard_loader_config", "setup_shard_loader"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    from iden.shard import BaseShard

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseShardLoader(Generic[T], ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a shard loader.

    A shard loader object allows to load a ``BaseShard`` object from
    its Uniform Resource Identifier (URI).

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard
    >>> from iden.shard.loader import JsonShardLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_json_shard([1, 2, 3], uri=uri)
    ...     loader = JsonShardLoader()
    ...     loader
    ...
    JsonShardLoader()

    ```
    """

    @abstractmethod
    def load(self, uri: str) -> BaseShard[T]:
        r"""Load a shard from its Uniform Resource Identifier (URI).

        Args:
            uri: The URI of the shard to load.

        Returns:
            The loaded shard.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard
        >>> from iden.shard.loader import JsonShardLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
        ...     _ = create_json_shard([1, 2, 3], uri=uri)
        ...     loader = JsonShardLoader()
        ...     shard = loader.load(uri)
        ...     shard
        ...
        JsonShard(uri=file:///.../my_uri)

        ```
        """


def is_shard_loader_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseShardLoader``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: Specifies the configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseShardLoader`` object.

    Example usage:

    ```pycon
    >>> from iden.shard.loader import is_shard_loader_config
    >>> is_shard_loader_config({"_target_": "iden.shard.loader.JsonShardLoader"})
    True

    ```
    """
    return is_object_config(config, BaseShardLoader)


def setup_shard_loader(shard_loader: BaseShardLoader | dict) -> BaseShardLoader:
    r"""Set up a shard loader.

    The shard loader is instantiated from its configuration by using the
    ``BaseShardLoader`` factory function.

    Args:
        shard_loader: Specifies the shard loader or its configuration.

    Returns:
        The instantiated shard loader.

    Example usage:

    ```pycon
    >>> from iden.shard.loader import setup_shard_loader
    >>> shard_loader = setup_shard_loader({"_target_": "iden.shard.loader.JsonShardLoader"})
    >>> shard_loader
    JsonShardLoader()

    ```
    """
    if isinstance(shard_loader, dict):
        logger.debug("Initializing a shard loader from its configuration...")
        shard_loader = BaseShardLoader.factory(**shard_loader)
    if not isinstance(shard_loader, BaseShardLoader):
        logger.warning(f"shard loader is not a BaseShardLoader (received: {type(shard_loader)})")
    return shard_loader
