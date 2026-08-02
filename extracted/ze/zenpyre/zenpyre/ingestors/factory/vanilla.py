r"""Provide a concrete default factory for zenpyre BaseIngestor
models."""

from __future__ import annotations

__all__ = ["IngestorFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.factory.base import BaseIngestorFactory

if TYPE_CHECKING:
    from zenpyre.ingestors.base import BaseIngestor

T = TypeVar("T")


class IngestorFactory(BaseIngestorFactory[T], MultilineDisplayMixin):
    """A concrete BaseIngestor factory that wraps a pre-built
    :class:`~zenpyre.ingestors.base.BaseIngestor` instance.

    Use this when the ingestor is already instantiated and you
    simply want to wrap it in the :class:`~BaseIngestorFactory`
    interface — for example, when injecting a fixed ingestor into a
    component that expects a factory.

    Args:
        ingestor: A fully configured
            :class:`~zenpyre.ingestors.base.BaseIngestor`
            instance to return from :meth:`make_ingestor`.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> from zenpyre.ingestors.factory import IngestorFactory
        >>> factory = IngestorFactory(InMemoryIngestor([1, 2, 3]))
        >>> ingestor = factory.make_ingestor()

        ```
    """

    def __init__(self, ingestor: BaseIngestor[T]) -> None:
        self._ingestor = ingestor

    def make_ingestor(self) -> BaseIngestor[T]:
        return self._ingestor

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"ingestor": self._ingestor}
