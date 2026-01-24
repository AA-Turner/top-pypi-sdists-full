from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array
from .list import FSharpList, empty, singleton
from .option import some
from .reflection import TypeInfo, union_type
from .types import Union, int32
from .util import equals
from .util import int32 as int32_1


def _expr20(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpResult`2",
        [gen0, gen1],
        FSharpResult_2,
        lambda: [[("ResultValue", gen0)], [("ErrorValue", gen1)]],
    )


class FSharpResult_2[T, TERROR](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Ok", "Error"]


FSharpResult_2_reflection = _expr20


def Result_Map[A, B, C](mapping: Callable[[A], B], result: FSharpResult_2[A, C]) -> FSharpResult_2[B, C]:
    if result.tag == int32_1(0):
        return FSharpResult_2(int32_1(0), mapping(result.fields[int32_1(0)]))

    else:
        return FSharpResult_2(int32_1(1), result.fields[int32_1(0)])


def Result_MapError[A, B, C](mapping: Callable[[A], B], result: FSharpResult_2[C, A]) -> FSharpResult_2[C, B]:
    if result.tag == int32_1(0):
        return FSharpResult_2(int32_1(0), result.fields[int32_1(0)])

    else:
        return FSharpResult_2(int32_1(1), mapping(result.fields[int32_1(0)]))


def Result_Bind[A, B, C](
    binder: Callable[[A], FSharpResult_2[B, C]], result: FSharpResult_2[A, C]
) -> FSharpResult_2[B, C]:
    if result.tag == int32_1(0):
        return binder(result.fields[int32_1(0)])

    else:
        return FSharpResult_2(int32_1(1), result.fields[int32_1(0)])


def Result_IsOk[A, B](result: FSharpResult_2[Any, Any]) -> bool:
    if result.tag == int32_1(0):
        return True

    else:
        return False


def Result_IsError[A, B](result: FSharpResult_2[Any, Any]) -> bool:
    if result.tag == int32_1(0):
        return False

    else:
        return True


def Result_Contains[A, B](value: A, result: FSharpResult_2[A, Any]) -> bool:
    if result.tag == int32_1(0):
        return equals(result.fields[int32_1(0)], value)

    else:
        return False


def Result_Count[A, B](result: FSharpResult_2[Any, Any]) -> int32:
    if result.tag == int32_1(0):
        return int32.ONE

    else:
        return int32.ZERO


def Result_DefaultValue[A, B](default_value: A, result: FSharpResult_2[A, Any]) -> A:
    if result.tag == int32_1(0):
        return result.fields[int32_1(0)]

    else:
        return default_value


def Result_DefaultWith[A, B](def_thunk: Callable[[B], A], result: FSharpResult_2[A, B]) -> A:
    if result.tag == int32_1(0):
        return result.fields[int32_1(0)]

    else:
        return def_thunk(result.fields[int32_1(0)])


def Result_Exists[A, B](predicate: Callable[[A], bool], result: FSharpResult_2[A, Any]) -> bool:
    if result.tag == int32_1(0):
        return predicate(result.fields[int32_1(0)])

    else:
        return False


def Result_Fold[A, B, S](folder: Callable[[S, A], S], state: S, result: FSharpResult_2[A, Any]) -> S:
    if result.tag == int32_1(0):
        return folder(state, result.fields[int32_1(0)])

    else:
        return state


def Result_FoldBack[A, B, S](folder: Callable[[A, S], S], result: FSharpResult_2[A, Any], state: S) -> S:
    if result.tag == int32_1(0):
        return folder(result.fields[int32_1(0)], state)

    else:
        return state


def Result_ForAll[A, B](predicate: Callable[[A], bool], result: FSharpResult_2[A, Any]) -> bool:
    if result.tag == int32_1(0):
        return predicate(result.fields[int32_1(0)])

    else:
        return True


def Result_Iterate[A, B](action: Callable[[A], None], result: FSharpResult_2[A, Any]) -> None:
    if result.tag == int32_1(0):
        action(result.fields[int32_1(0)])


def Result_ToArray[A, B](result: FSharpResult_2[A, Any]) -> Array[A]:
    if result.tag == int32_1(0):
        return Array[Any]([result.fields[int32_1(0)]])

    else:
        return Array[Any]([])


def Result_ToList[A, B](result: FSharpResult_2[A, Any]) -> FSharpList[A]:
    if result.tag == int32_1(0):
        return singleton(result.fields[int32_1(0)])

    else:
        return empty()


def Result_ToOption[A, B](result: FSharpResult_2[A, Any]) -> A | None:
    if result.tag == int32_1(0):
        return some(result.fields[int32_1(0)])

    else:
        return None


def Result_ToValueOption[A, B](result: FSharpResult_2[A, Any]) -> A | None:
    if result.tag == int32_1(0):
        return some(result.fields[int32_1(0)])

    else:
        return None


__all__ = [
    "FSharpResult_2_reflection",
    "Result_Map",
    "Result_MapError",
    "Result_Bind",
    "Result_IsOk",
    "Result_IsError",
    "Result_Contains",
    "Result_Count",
    "Result_DefaultValue",
    "Result_DefaultWith",
    "Result_Exists",
    "Result_Fold",
    "Result_FoldBack",
    "Result_ForAll",
    "Result_Iterate",
    "Result_ToArray",
    "Result_ToList",
    "Result_ToOption",
    "Result_ToValueOption",
]
