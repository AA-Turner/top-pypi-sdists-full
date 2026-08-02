r"""Provide a generic resolution utility for creating objects from an
existing instance or an objectory configuration dictionary."""

from __future__ import annotations

__all__ = ["resolve_object"]

import logging
from typing import Any, TypeVar

from objectory import factory

from zenpyre.utils.config import BaseConfig

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")


def resolve_object(obj: T | dict[str, Any] | BaseConfig, cls: type[T] = object) -> T:
    """Resolve an instance of ``cls`` from an existing object or a
    configuration dictionary.

    If ``obj`` is already an instance of ``cls`` it is returned
    as-is.  If it is a :class:`dict`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`.

    Args:
        obj: Either a fully configured instance of ``cls``, or a
            :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).
        cls: The expected type. Used to validate the resolved object,
            whether ``obj`` was already an instance or was built from
            a configuration dictionary. Defaults to :class:`object`,
            which accepts any resolved value without validation.

    Returns:
        A configured instance of ``cls``.

    Raises:
        TypeError: If the resolved object is not an instance of
            ``cls``.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> from zenpyre.ingestors.base import BaseIngestor
        >>> from zenpyre.utils.resolve import resolve_object
        >>> # From an existing instance:
        >>> ingestor = resolve_object(InMemoryIngestor([1, 2, 3]), cls=BaseIngestor)
        >>> # From a configuration dictionary:
        >>> ingestor = resolve_object(
        ...     {"_target_": "zenpyre.ingestors.InMemoryIngestor", "data": [1, 2, 3]},
        ...     cls=BaseIngestor,
        ... )
        >>> # From a BaseConfig, whose to_kwargs() includes a "_target_" key:
        >>> from zenpyre.utils.config import MISSING, BaseConfig
        >>> class IngestorConfig(BaseConfig):
        ...     def __init__(self, data: list[int]):
        ...         self.data = data
        ...     def get_value(self, name, default=MISSING):
        ...         return self.to_kwargs()[name]
        ...     def to_kwargs(self):
        ...         return {"_target_": "zenpyre.ingestors.InMemoryIngestor", "data": self.data}
        ...
        >>> ingestor = resolve_object(IngestorConfig(data=[1, 2, 3]), cls=BaseIngestor)

        ```
    """
    if isinstance(obj, BaseConfig):
        obj = obj.to_kwargs()
    if isinstance(obj, dict):
        logger.info("Initializing a %s instance from its configuration...", cls.__qualname__)
        obj = factory(**obj)
    if not isinstance(obj, cls):
        msg = f"Received object is not a {cls.__name__} instance (received: {type(obj)})"
        raise TypeError(msg)
    return obj
