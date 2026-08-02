r"""Provide a resolution utility for creating zenpyre BaseProcessor
models."""

from __future__ import annotations

__all__ = ["resolve_data_processor"]

from typing import TYPE_CHECKING, Any, TypeVar

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


T = TypeVar("T")
U = TypeVar("U")


def resolve_data_processor(
    processor: BaseProcessor[U, T] | dict[str, Any] | BaseConfig,
) -> BaseProcessor[U, T]:
    """Resolve a :class:`~zenpyre.data_processors.base.BaseProcessor`
    instance from an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``processor`` is already a
    :class:`~zenpyre.data_processors.base.BaseProcessor` instance
    it is returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        processor: Either a fully configured
            :class:`~zenpyre.data_processors.base.BaseProcessor`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured
        :class:`~zenpyre.data_processors.base.BaseProcessor`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~zenpyre.data_processors.base.BaseProcessor`
            instance.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import resolve_data_processor, FirstNProcessor
        >>> # From an existing instance:
        >>> processor = resolve_data_processor(FirstNProcessor(n=5))
        >>> # From a configuration dictionary:
        >>> processor = resolve_data_processor(  # doctest: +SKIP
        ...     {"_target_": "zenpyre.data_processors.FirstNProcessor", "n": 5}
        ... )

        ```
    """
    return resolve_object(processor, cls=BaseProcessor)
