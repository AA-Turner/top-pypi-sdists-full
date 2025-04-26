r"""Contain the base class to implement a data generator."""

from __future__ import annotations

__all__ = ["BaseDataGenerator", "is_data_generator_config", "setup_data_generator"]

import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from objectory import AbstractFactory
from objectory.utils import is_object_config

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseDataGenerator(Generic[T], ABC, metaclass=AbstractFactory):
    r"""Define the base class to generate data.

    Example usage:

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
    def generate(self) -> T:
        r"""Generate data.

        Returns:
            The generated data.

        Example usage:

        ```pycon
        >>> from iden.data.generator import DataGenerator
        >>> generator = DataGenerator([1, 2, 3])
        >>> generator.generate()
        [1, 2, 3]

        ```
        """


def is_data_generator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseDataGenerator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: Specifies the configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseDataGenerator`` object.

    Example usage:

    ```pycon
    >>> from iden.data.generator import is_data_generator_config
    >>> is_data_generator_config({"_target_": "iden.data.generator.DataGenerator"})
    True

    ```
    """
    return is_object_config(config, BaseDataGenerator)


def setup_data_generator(data_generator: BaseDataGenerator | dict) -> BaseDataGenerator:
    r"""Set up a data generator.

    The data generator is instantiated from its configuration by using the
    ``BaseDataGenerator`` factory function.

    Args:
        data_generator: Specifies the data generator or its configuration.

    Returns:
        The instantiated data generator.

    Example usage:

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
