r"""Contain some comparators to use ``BaseShard`` objects with
``coola.objects_are_equal``."""

from __future__ import annotations

__all__ = ["ShardEqualityComparator"]

import logging
from typing import TYPE_CHECKING, Any

from coola.equality.comparators import BaseEqualityComparator
from coola.equality.handlers import EqualNanHandler, SameObjectHandler, SameTypeHandler
from coola.equality.testers import EqualityTester

from iden.shard.base import BaseShard

if TYPE_CHECKING:
    import sys

    from coola.equality import EqualityConfig

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

logger = logging.getLogger(__name__)


class ShardEqualityComparator(BaseEqualityComparator[BaseShard]):
    r"""Implement an equality comparator for ``BaseShard`` objects."""

    def __init__(self) -> None:
        self._handler = SameObjectHandler()
        self._handler.chain(SameTypeHandler()).chain(EqualNanHandler())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> Self:
        return self.__class__()

    def equal(self, actual: Any, expected: Any, config: EqualityConfig) -> bool:
        return self._handler.handle(actual, expected, config=config)


if not EqualityTester.has_comparator(BaseShard):  # pragma: no cover
    EqualityTester.add_comparator(BaseShard, ShardEqualityComparator())
