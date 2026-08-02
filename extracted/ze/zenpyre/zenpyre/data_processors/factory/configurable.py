r"""Provide a configurable factory for zenpyre BaseProcessor models."""

from __future__ import annotations

__all__ = ["ConfigurableProcessorFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.data_processors.factory.base import BaseProcessorFactory
from zenpyre.data_processors.resolve import resolve_data_processor

if TYPE_CHECKING:
    from zenpyre.data_processors.base import BaseProcessor

U = TypeVar("U")
T = TypeVar("T")


class ConfigurableProcessorFactory(BaseProcessorFactory[U, T], MultilineDisplayMixin):
    """A concrete BaseProcessor factory that accepts either a pre-built
    :class:`~zenpyre.data_processors.base.BaseProcessor` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each :meth:`make_processor`
    call via :func:`~zenpyre.data_processors.resolve.resolve_data_processor`,
    which uses ``objectory`` to instantiate the configured class.  When
    an instance is provided it is returned as-is.

    Args:
        processor: A fully configured
            :class:`~zenpyre.data_processors.base.BaseProcessor`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from zenpyre.data_processors import FirstNProcessor
        >>> from zenpyre.data_processors.factory import ConfigurableProcessorFactory
        >>> factory = ConfigurableProcessorFactory(FirstNProcessor(n=5))
        >>> processor = factory.make_processor()

        ```
    """

    def __init__(self, processor: BaseProcessor[U, T] | dict[str, Any]) -> None:
        self._processor = processor

    def make_processor(self) -> BaseProcessor[U, T]:
        return resolve_data_processor(self._processor)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"processor": self._processor}
