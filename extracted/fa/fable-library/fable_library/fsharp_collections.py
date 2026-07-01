from collections.abc import Callable
from typing import Any, cast

from .core import int32
from .protocols import IComparer_1, IEqualityComparer_1
from .util import UNIT, Unit, compare, physical_hash, structural_hash
from .util import equals as equals_1


def HashIdentity_FromFunctions[T](
    hasher: Callable[[T], int32], equals: Callable[[T, T], bool]
) -> IEqualityComparer_1[Any]:
    class ObjectExpr0(IEqualityComparer_1[Any]):
        def GetHashCode(self, x: T = UNIT, hasher: Any = hasher) -> int32:
            return hasher(x)

        def Equals(self, x_1: T, y: T, equals: Any = equals) -> bool:
            return (
                (True if equals_1(y, cast(Any, None)) else False)
                if equals_1(x_1, cast(Any, None))
                else (False if equals_1(y, cast(Any, None)) else equals(x_1, y))
            )

    return ObjectExpr0()


def HashIdentity_Structural[T](__unit: Unit = UNIT) -> IEqualityComparer_1[Any]:
    class ObjectExpr1(IEqualityComparer_1[Any]):
        def GetHashCode(self, x: T = UNIT) -> int32:
            return structural_hash(x)

        def Equals(self, x_1: T, y: T) -> bool:
            return equals_1(x_1, y)

    return ObjectExpr1()


def HashIdentity_Reference[T](__unit: Unit = UNIT) -> IEqualityComparer_1[Any]:
    class ObjectExpr2(IEqualityComparer_1[Any]):
        def GetHashCode(self, x: T = UNIT) -> int32:
            return physical_hash(x)

        def Equals(self, x_1: T, y: T) -> bool:
            return x_1 is y

    return ObjectExpr2()


def ComparisonIdentity_FromFunction[T](comparer: Callable[[T, T], int32]) -> IComparer_1[T]:
    class ObjectExpr3(IComparer_1[Any]):
        def Compare(self, x: T, y: T, comparer: Any = comparer) -> int32:
            return (
                (int32.ZERO if equals_1(y, cast(Any, None)) else int32.NEG_ONE)
                if equals_1(x, cast(Any, None))
                else (int32.ONE if equals_1(y, cast(Any, None)) else comparer(x, y))
            )

    return ObjectExpr3()


def ComparisonIdentity_Structural[T](__unit: Unit = UNIT) -> IComparer_1[T]:
    class ObjectExpr4(IComparer_1[Any]):
        def Compare(self, x: T, y: T) -> int32:
            return compare(x, y)

    return ObjectExpr4()


__all__ = [
    "ComparisonIdentity_FromFunction",
    "ComparisonIdentity_Structural",
    "HashIdentity_FromFunctions",
    "HashIdentity_Reference",
    "HashIdentity_Structural",
]
