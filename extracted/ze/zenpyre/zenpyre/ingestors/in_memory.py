r"""Define an ingestor that returns pre-loaded in-memory data."""

from __future__ import annotations

__all__ = ["InMemoryIngestor"]

import copy
from typing import Any, TypeVar

from coola.display import InlineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor

T = TypeVar("T")


class InMemoryIngestor(BaseIngestor[T], InlineDisplayMixin):
    r"""Ingestor that returns a pre-loaded in-memory value.

    Wraps an arbitrary value and exposes it through the
    :meth:`ingest` interface, allowing any data already in memory to be
    used wherever a :class:`~zenpyre.ingestors.BaseIngestor` is expected.
    Useful for testing, rapid prototyping, or bypassing the download and
    caching steps of a pipeline.

    By default each call to :meth:`ingest` returns a deep copy of the
    stored value, preventing callers from accidentally mutating the
    ingestor's internal state. Pass ``copy=False`` to return the original
    object directly, which is useful in tests where mock identity must be
    preserved.

    Args:
        data: The value to return when :meth:`ingest` is called.
        copy: If ``True`` (the default), return a deep copy of *data* on
            each :meth:`ingest` call. If ``False``, return the original
            object.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> ingestor = InMemoryIngestor(data="hello\nworld")
        >>> ingestor.ingest()
        hello\nworld

        ```
    """

    def __init__(self, data: T, *, copy: bool = True) -> None:
        self._data = data
        self._copy = copy

    def ingest(self) -> T:
        if self._copy:
            return copy.deepcopy(self._data)
        return self._data

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"copy": self._copy}
