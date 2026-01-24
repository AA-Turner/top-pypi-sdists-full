r"""Contain the base class to implement a data generator."""

from __future__ import annotations

__all__ = ["BaseDataGenerator", "is_data_generator_config", "setup_data_generator"]

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from coola.equality.testers import EqualityTester
from objectory import AbstractFactory
from objectory.utils import is_object_config

from iden.utils.comparator import ObjectEqualityComparator

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class BaseDataGenerator(ABC, Generic[T], metaclass=AbstractFactory):
    r"""Define the base class to generate data.

    Example:
        ```pycon
        >>> from iden.data.generator import DataGenerator
        >>> generator = DataGenerator([1, 2, 3])
        >>> generator
        DataGenerator(copy=False)
        >>> generator.generate()
        [1, 2, 3]

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
            >>> from iden.data.generator import DataGenerator
            >>> DataGenerator([1, 2, 3]).equal(DataGenerator([1, 2, 3]))
            True
            >>> DataGenerator([1, 2, 3]).equal(DataGenerator([]))
            False

            ```
        """

    @abstractmethod
    def generate(self) -> T:
        r"""Generate data.

        Returns:
            The generated data.

        Example:
            ```pycon
            >>> from iden.data.generator import DataGenerator
            >>> generator = DataGenerator([1, 2, 3])
            >>> generator.generate()
            [1, 2, 3]

            ```
        """


def is_data_generator_config(config: dict[Any, Any]) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseDataGenerator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseDataGenerator`` object.

    Example:
        ```pycon
        >>> from iden.data.generator import is_data_generator_config
        >>> is_data_generator_config({"_target_": "iden.data.generator.DataGenerator"})
        True

        ```
    """
    return is_object_config(config, BaseDataGenerator)


def setup_data_generator(
    data_generator: BaseDataGenerator[T] | dict[Any, Any],
) -> BaseDataGenerator[T]:
    r"""Set up a data generator.

    The data generator is instantiated from its configuration by using the
    ``BaseDataGenerator`` factory function.

    Args:
        data_generator: The data generator or its configuration.

    Returns:
        The instantiated data generator.

    Example:
        ```pycon
        >>> from iden.data.generator import is_data_generator_config
        >>> generator = setup_data_generator(
        ...     {"_target_": "iden.data.generator.DataGenerator", "data": [1, 2, 3]}
        ... )
        >>> generator
        DataGenerator(copy=False)

        ```
    """
    if isinstance(data_generator, dict):
        logger.debug("Initializing a data generator from its configuration...")
        data_generator = BaseDataGenerator.factory(**data_generator)
    if not isinstance(data_generator, BaseDataGenerator):
        logger.warning(
            f"data generator is not a BaseDataGenerator (received: {type(data_generator)})"
        )
    return data_generator


if not EqualityTester.has_comparator(BaseDataGenerator):  # pragma: no cover
    EqualityTester.add_comparator(BaseDataGenerator, ObjectEqualityComparator())
