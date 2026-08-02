r"""Provide the base factory interface for creating zenpyre BaseIngestor
models."""

from __future__ import annotations

__all__ = ["BaseIngestorFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from zenpyre.ingestors.base import BaseIngestor

T = TypeVar("T")


class BaseIngestorFactory(ABC, Generic[T]):
    """Abstract base class for
    :class:`~zenpyre.ingestors.base.BaseIngestor` factories.

    Subclasses implement :meth:`make_ingestor` to instantiate and
    return a configured
    :class:`~zenpyre.ingestors.base.BaseIngestor` object.  This
    pattern decouples ingestor creation from the rest of the
    codebase, making it easy to swap ingestors (e.g. file, web,
    database) without changing call sites.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> from zenpyre.ingestors.base import BaseIngestor
        >>> from zenpyre.ingestors.factory import BaseIngestorFactory
        >>> class MyIngestorFactory(BaseIngestorFactory[list[int]]):
        ...     def make_ingestor(self) -> BaseIngestor[list[int]]:
        ...         return InMemoryIngestor([1, 2, 3])
        ...
        >>> factory = MyIngestorFactory()
        >>> ingestor = factory.make_ingestor()

        ```
    """

    @abstractmethod
    def make_ingestor(self) -> BaseIngestor[T]:
        """Create and return a configured BaseIngestor instance.

        Returns:
            A :class:`~zenpyre.ingestors.base.BaseIngestor`
            instance ready for use.
        """
