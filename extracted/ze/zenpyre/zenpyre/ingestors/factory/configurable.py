r"""Provide a configurable factory for zenpyre BaseIngestor models."""

from __future__ import annotations

__all__ = ["ConfigurableIngestorFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.factory.base import BaseIngestorFactory
from zenpyre.ingestors.resolve import resolve_ingestor

if TYPE_CHECKING:
    from zenpyre.ingestors.base import BaseIngestor

T = TypeVar("T")


class ConfigurableIngestorFactory(BaseIngestorFactory[T], MultilineDisplayMixin):
    """A concrete BaseIngestor factory that accepts either a pre-built
    :class:`~zenpyre.ingestors.base.BaseIngestor` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each :meth:`make_ingestor`
    call via :func:`~zenpyre.ingestors.resolve.resolve_ingestor`, which
    uses ``objectory`` to instantiate the configured class.  When an
    instance is provided it is returned as-is.

    Args:
        ingestor: A fully configured
            :class:`~zenpyre.ingestors.base.BaseIngestor`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> from zenpyre.ingestors.factory import ConfigurableIngestorFactory
        >>> factory = ConfigurableIngestorFactory(InMemoryIngestor([1, 2, 3]))
        >>> ingestor = factory.make_ingestor()

        ```
    """

    def __init__(self, ingestor: BaseIngestor[T] | dict[str, Any]) -> None:
        self._ingestor = ingestor

    def make_ingestor(self) -> BaseIngestor[T]:
        return resolve_ingestor(self._ingestor)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"ingestor": self._ingestor}
