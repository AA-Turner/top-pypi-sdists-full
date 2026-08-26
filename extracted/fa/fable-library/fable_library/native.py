from __future__ import annotations

from typing import Any, cast

from .array_ import Array, FSharpCons, create, of_seq
from .core import int32
from .fsharp_core import Operators_IsNull
from .protocols import IEnumerable_1
from .util import range


def Helpers_arrayFrom[T](xs: IEnumerable_1[T]) -> Array[T]:
    return of_seq(xs)


def Helpers_allocateArray[T](len_1: int) -> Array[T]:
    return create(len_1, cast(Any, None))


def Helpers_allocateArrayFromCons[T](cons: FSharpCons[T], len_1: int) -> Array[T]:
    if Operators_IsNull(cons):
        return create(len_1, cast(Any, None))

    else:
        return cons.allocate(len_1)


def Helpers_fillImpl[T](array: Array[T], value: T, start: int, count: int) -> Array[T]:
    for i in range(0, (count - 1) if (count >= -2147483647) else int32(count - 1), 1):
        array[tmp if (-2147483648 <= (tmp := i + start) <= 2147483647) else int32(tmp)] = value
    return array


def Helpers_spliceImpl[T](array: Array[T], start: int, delete_count: int) -> Array[T]:
    for _ in range(1, delete_count, 1):
        array.pop(start)
    return array


def Helpers_indexOfImpl[T](array: Array[T], item: T, start: int) -> Any:
    try:
        return array.index(item, start)

    except Exception as ex:
        return -1


__all__ = [
    "Helpers_allocateArray",
    "Helpers_allocateArrayFromCons",
    "Helpers_arrayFrom",
    "Helpers_fillImpl",
    "Helpers_indexOfImpl",
    "Helpers_spliceImpl",
]
