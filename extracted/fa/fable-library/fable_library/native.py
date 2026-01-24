from __future__ import annotations

from typing import Any

from .array_ import Array, FSharpCons, create, of_seq
from .fsharp_core import Operators_IsNull
from .types import int32
from .util import IEnumerable_1, range


def Helpers_arrayFrom[T](xs: IEnumerable_1[T]) -> Array[T]:
    return of_seq(xs)


def Helpers_allocateArray[T](len_1: int32) -> Array[Any]:
    return create(len_1, None)


def Helpers_allocateArrayFromCons[T](cons: FSharpCons[T], len_1: int32) -> Array[T]:
    if Operators_IsNull(cons):
        return FSharpCons().allocate(len_1)

    else:
        return cons.allocate(len_1)


def Helpers_fillImpl[T](array: Array[T], value: T, start: int32, count: int32) -> Array[T]:
    for i in range(int32.ZERO, count - int32.ONE, 1):
        array[i + start] = value
    return array


def Helpers_spliceImpl[T](array: Array[T], start: int32, delete_count: int32) -> Array[T]:
    for _ in range(int32.ONE, delete_count, 1):
        array.pop(start)
    return array


def Helpers_indexOfImpl[T](array: Array[T], item: T, start: int32) -> Any:
    try:
        return array.index(item, start)

    except Exception as ex:
        return int32.NEG_ONE


__all__ = [
    "Helpers_arrayFrom",
    "Helpers_allocateArray",
    "Helpers_allocateArrayFromCons",
    "Helpers_fillImpl",
    "Helpers_spliceImpl",
    "Helpers_indexOfImpl",
]
