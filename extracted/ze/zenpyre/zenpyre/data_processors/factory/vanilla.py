r"""Provide a concrete default factory for zenpyre BaseProcessor
models."""

from __future__ import annotations

__all__ = ["ProcessorFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.data_processors.factory.base import BaseProcessorFactory

if TYPE_CHECKING:
    from zenpyre.data_processors.base import BaseProcessor

U = TypeVar("U")
T = TypeVar("T")


class ProcessorFactory(BaseProcessorFactory[U, T], MultilineDisplayMixin):
    """A concrete BaseProcessor factory that wraps a pre-built
    :class:`~zenpyre.data_processors.base.BaseProcessor` instance.

    Use this when the processor is already instantiated and you
    simply want to wrap it in the :class:`~BaseProcessorFactory`
    interface — for example, when injecting a fixed processor into a
    component that expects a factory.

    Args:
        processor: A fully configured
            :class:`~zenpyre.data_processors.base.BaseProcessor`
            instance to return from :meth:`make_processor`.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import FirstNProcessor
        >>> from zenpyre.data_processors.factory import ProcessorFactory
        >>> factory = ProcessorFactory(FirstNProcessor(n=5))
        >>> processor = factory.make_processor()

        ```
    """

    def __init__(self, processor: BaseProcessor[U, T]) -> None:
        self._processor = processor

    def make_processor(self) -> BaseProcessor[U, T]:
        return self._processor

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"processor": self._processor}
