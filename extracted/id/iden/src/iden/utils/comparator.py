r"""Contain a generic comparator for iden objects to be used with
``coola.objects_are_equal``."""

from __future__ import annotations

__all__ = ["ObjectEqualityComparator"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.equality.comparators import BaseEqualityComparator
from coola.equality.handlers import EqualNanHandler, SameObjectHandler, SameTypeHandler

if TYPE_CHECKING:
    from coola.equality import EqualityConfig


T = TypeVar("T")
S = TypeVar("S", bound="ObjectEqualityComparator")


class ObjectEqualityComparator(BaseEqualityComparator[T]):  # noqa: PLW1641
    r"""Implement an equality comparator for ``BaseLoader`` objects."""

    def __init__(self) -> None:
        self._handler = SameObjectHandler()
        self._handler.chain(SameTypeHandler()).chain(EqualNanHandler())

    def __eq__(self, other: object) -> bool:
        return type(other) is type(self)

    def clone(self) -> S:
        return self.__class__()

    def equal(self, actual: T, expected: Any, config: EqualityConfig) -> bool:
        return self._handler.handle(actual, expected, config=config)
