r"""Provide the base factory interface for creating zenpyre
BaseProcessor models."""

from __future__ import annotations

__all__ = ["BaseProcessorFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from zenpyre.data_processors.base import BaseProcessor

U = TypeVar("U")
T = TypeVar("T")


class BaseProcessorFactory(ABC, Generic[U, T]):
    """Abstract base class for
    :class:`~zenpyre.data_processors.base.BaseProcessor` factories.

    Subclasses implement :meth:`make_processor` to instantiate and
    return a configured
    :class:`~zenpyre.data_processors.base.BaseProcessor` object.
    This pattern decouples processor creation from the rest of the
    codebase, making it easy to swap processors (e.g. filtering,
    sorting, sequencing) without changing call sites.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import FirstNProcessor
        >>> from zenpyre.data_processors.base import BaseProcessor
        >>> from zenpyre.data_processors.factory import BaseProcessorFactory
        >>> class MyProcessorFactory(BaseProcessorFactory[list[int], list[int]]):
        ...     def make_processor(self) -> BaseProcessor[list[int], list[int]]:
        ...         return FirstNProcessor(n=5)
        ...
        >>> factory = MyProcessorFactory()
        >>> processor = factory.make_processor()

        ```
    """

    @abstractmethod
    def make_processor(self) -> BaseProcessor[U, T]:
        """Create and return a configured BaseProcessor instance.

        Returns:
            A :class:`~zenpyre.data_processors.base.BaseProcessor`
            instance ready for use.
        """
