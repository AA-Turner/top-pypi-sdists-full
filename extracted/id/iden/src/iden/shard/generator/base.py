r"""Contain the base class to implement a shard generator."""

from __future__ import annotations

__all__ = ["BaseShardGenerator", "is_shard_generator_config", "setup_shard_generator"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from coola.equality.testers import EqualityTester
from objectory import AbstractFactory
from objectory.utils import is_object_config

from iden.utils.comparator import ObjectEqualityComparator

if TYPE_CHECKING:
    from iden.shard import BaseShard

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class BaseShardGenerator(ABC, Generic[T], metaclass=AbstractFactory):
    r"""Define the base class to create a shard.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.data.generator import DataGenerator
        >>> from iden.shard.generator import JsonShardGenerator
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     generator = JsonShardGenerator(
        ...         data=DataGenerator([1, 2, 3]),
        ...         path_uri=Path(tmpdir).joinpath("uri"),
        ...         path_shard=Path(tmpdir).joinpath("data"),
        ...     )
        ...     generator
        ...     shard = generator.generate("shard1")
        ...     shard
        ...
        JsonShardGenerator(
          (path_uri): PosixPath('/.../uri')
          (path_shard): PosixPath('/.../data')
          (data): DataGenerator(copy=False)
        )
        JsonShard(uri=file:///.../uri/shard1)

        ```
    """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two objects are equal or not.

        Args:
            other: The object to compare with.
            equal_nan: If ``True``, then two ``NaN``s will be
                considered equal.

        Returns:
            ``True`` if the two objects are equal, otherwise ``False``.

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.data.generator import DataGenerator
            >>> from iden.shard.generator import JsonShardGenerator
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     generator1 = JsonShardGenerator(
            ...         data=DataGenerator([1, 2, 3]),
            ...         path_uri=Path(tmpdir).joinpath("uri"),
            ...         path_shard=Path(tmpdir).joinpath("data"),
            ...     )
            ...     generator2 = JsonShardGenerator(
            ...         data=DataGenerator([1, 2, 3]),
            ...         path_uri=Path(tmpdir).joinpath("uri"),
            ...         path_shard=Path(tmpdir).joinpath("data"),
            ...     )
            ...     generator3 = JsonShardGenerator(
            ...         data=DataGenerator([]),
            ...         path_uri=Path(tmpdir).joinpath("uri"),
            ...         path_shard=Path(tmpdir).joinpath("data"),
            ...     )
            ...     generator1.equal(generator2)
            ...     generator1.equal(generator3)
            ...
            True
            False

            ```
        """

    @abstractmethod
    def generate(self, shard_id: str) -> BaseShard[T]:
        r"""Generate a shard.

        Args:
            shard_id: The shard IDI.

        Returns:
            The generated shard.

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.data.generator import DataGenerator
            >>> from iden.shard.generator import JsonShardGenerator
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     generator = JsonShardGenerator(
            ...         data=DataGenerator([1, 2, 3]),
            ...         path_uri=Path(tmpdir).joinpath("uri"),
            ...         path_shard=Path(tmpdir).joinpath("data"),
            ...     )
            ...     shard = generator.generate("shard1")
            ...     shard
            ...
            JsonShard(uri=file:///.../uri/shard1)

            ```
        """


def is_shard_generator_config(config: dict[Any, Any]) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseShardGenerator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseShardGenerator`` object.

    Example:
        ```pycon
        >>> from iden.shard.generator import is_shard_generator_config
        >>> is_shard_generator_config({"_target_": "iden.shard.generator.JsonShardGenerator"})
        True

        ```
    """
    return is_object_config(config, BaseShardGenerator)


def setup_shard_generator(
    shard_generator: BaseShardGenerator[T] | dict[Any, Any],
) -> BaseShardGenerator[T]:
    r"""Set up a shard generator.

    The shard generator is instantiated from its configuration by using the
    ``BaseShardGenerator`` factory function.

    Args:
        shard_generator: The shard generator or its configuration.

    Returns:
        The instantiated shard generator.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard.generator import setup_shard_generator
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     generator = setup_shard_generator(
        ...         {
        ...             "_target_": "iden.shard.generator.JsonShardGenerator",
        ...             "data": [1, 2, 3],
        ...             "path_uri": Path(tmpdir).joinpath("uri"),
        ...             "path_shard": Path(tmpdir).joinpath("data"),
        ...         }
        ...     )
        ...     generator
        ...
        JsonShardGenerator(
          (path_uri): PosixPath('/.../uri')
          (path_shard): PosixPath('/.../data')
          (data): [1, 2, 3]
        )

        ```
    """
    if isinstance(shard_generator, dict):
        logger.debug("Initializing a shard generator from its configuration...")
        shard_generator = BaseShardGenerator.factory(**shard_generator)
    if not isinstance(shard_generator, BaseShardGenerator):
        logger.warning(
            f"shard generator is not a BaseShardGenerator (received: {type(shard_generator)})"
        )
    return shard_generator


if not EqualityTester.has_comparator(BaseShardGenerator):  # pragma: no cover
    EqualityTester.add_comparator(BaseShardGenerator, ObjectEqualityComparator())
