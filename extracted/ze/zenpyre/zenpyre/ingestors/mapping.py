r"""Define an ingestor that aggregates results from a mapping of
ingestors."""

from __future__ import annotations

__all__ = ["MappingIngestor"]

from collections.abc import Hashable
from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from collections.abc import Mapping

T = TypeVar("T")


class MappingIngestor(BaseIngestor[dict[Hashable, BaseIngestor[T]]], MultilineDisplayMixin):
    """Ingestor that calls a mapping of ingestors and returns their
    results as a dict.

    Each inner ingestor is called in order and its return value is
    stored under the corresponding key. The types of the individual
    results are unconstrained — each ingestor may return a different
    type.

    Args:
        sources: A mapping from arbitrary keys to
            :class:`~zenpyre.ingestors.BaseIngestor` instances.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor, MappingIngestor
        >>> ingestor = MappingIngestor(
        ...     sources={
        ...         "10-K": InMemoryIngestor(data="annual report text"),
        ...         "10-Q": InMemoryIngestor(data="quarterly report text"),
        ...     }
        ... )
        >>> ingestor.ingest()
        {'10-K': 'annual report text', '10-Q': 'quarterly report text'}

        ```
    """

    def __init__(self, sources: Mapping[Hashable, BaseIngestor[T]]) -> None:
        self._sources = sources

    def ingest(self) -> dict[Hashable, T]:
        return {key: ingestor.ingest() for key, ingestor in self._sources.items()}

    def _get_repr_kwargs(self) -> dict[Hashable, Any]:
        return self._sources
