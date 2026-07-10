from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array
from .core import int32
from .list import FSharpList, empty, singleton
from .option import Option, some
from .reflection import TypeInfo, union_type
from .union import Union, narrow, tagged_union
from .util import equals


def _expr8(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpResult`2",
        Array([gen0, gen1]),
        _FSharpResult_2,
        lambda: [[("ResultValue", gen0)], [("ErrorValue", gen1)]],
        [Ok, Error],
    )


class _FSharpResult_2[T, TERROR](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Ok", "Error"]


@tagged_union(0)
class Ok[T, TERROR](_FSharpResult_2[T, TERROR]):
    result_value: Any


@tagged_union(1)
class Error[T, TERROR](_FSharpResult_2[T, TERROR]):
    error_value: Any


type FSharpResult_2[T, TERROR] = Ok[T, TERROR] | Error[T, TERROR]

FSharpResult_2_reflection = _expr8


def Result_Map[A, B, C](mapping: Callable[[A], B], result: FSharpResult_2[A, C]) -> FSharpResult_2[B, C]:
    match result.tag:
        case 0:
            return Ok(mapping(narrow(Ok, result).result_value))

        case _:
            return Error(narrow(Error, result).error_value)


def Result_MapError[A, B, C](mapping: Callable[[A], B], result: FSharpResult_2[C, A]) -> FSharpResult_2[C, B]:
    match result.tag:
        case 0:
            return Ok(narrow(Ok, result).result_value)

        case _:
            return Error(mapping(narrow(Error, result).error_value))


def Result_Bind[A, B, C](
    binder: Callable[[A], FSharpResult_2[B, C]], result: FSharpResult_2[A, C]
) -> FSharpResult_2[B, C]:
    match result.tag:
        case 0:
            return binder(narrow(Ok, result).result_value)

        case _:
            return Error(narrow(Error, result).error_value)


def Result_IsOk[A, B](result: FSharpResult_2[A, B]) -> bool:
    match result.tag:
        case 0:
            return True

        case _:
            return False


def Result_IsError[A, B](result: FSharpResult_2[A, B]) -> bool:
    match result.tag:
        case 0:
            return False

        case _:
            return True


def Result_Contains[A, B](value: A, result: FSharpResult_2[A, B]) -> bool:
    match result.tag:
        case 0:
            return equals(narrow(Ok, result).result_value, value)

        case _:
            return False


def Result_Count[A, B](result: FSharpResult_2[A, B]) -> int32:
    match result.tag:
        case 0:
            return int32.ONE

        case _:
            return int32.ZERO


def Result_DefaultValue[A, B](default_value: A, result: FSharpResult_2[A, B]) -> A:
    match result.tag:
        case 0:
            return narrow(Ok, result).result_value

        case _:
            return default_value


def Result_DefaultWith[B, A](def_thunk: Callable[[B], A], result: FSharpResult_2[A, B]) -> A:
    match result.tag:
        case 0:
            return narrow(Ok, result).result_value

        case _:
            return def_thunk(narrow(Error, result).error_value)


def Result_Exists[A, B](predicate: Callable[[A], bool], result: FSharpResult_2[A, B]) -> bool:
    match result.tag:
        case 0:
            return predicate(narrow(Ok, result).result_value)

        case _:
            return False


def Result_Fold[A, B, S](folder: Callable[[S, A], S], state: S, result: FSharpResult_2[A, B]) -> S:
    match result.tag:
        case 0:
            return folder(state, narrow(Ok, result).result_value)

        case _:
            return state


def Result_FoldBack[A, B, S](folder: Callable[[A, S], S], result: FSharpResult_2[A, B], state: S) -> S:
    match result.tag:
        case 0:
            return folder(narrow(Ok, result).result_value, state)

        case _:
            return state


def Result_ForAll[A, B](predicate: Callable[[A], bool], result: FSharpResult_2[A, B]) -> bool:
    match result.tag:
        case 0:
            return predicate(narrow(Ok, result).result_value)

        case _:
            return True


def Result_Iterate[A, B](action: Callable[[A], None], result: FSharpResult_2[A, B]) -> None:
    match result.tag:
        case 0:
            action(narrow(Ok, result).result_value)

        case _:
            pass


def Result_ToArray[A, B](result: FSharpResult_2[A, B]) -> Array[A]:
    match result.tag:
        case 0:
            return Array[Any]([narrow(Ok, result).result_value])

        case _:
            return Array[Any]([])


def Result_ToList[A, B](result: FSharpResult_2[A, B]) -> FSharpList[A]:
    match result.tag:
        case 0:
            return singleton(narrow(Ok, result).result_value)

        case _:
            return empty()


def Result_ToOption[A, B](result: FSharpResult_2[A, B]) -> Option[A]:
    match result.tag:
        case 0:
            return some(narrow(Ok, result).result_value)

        case _:
            return None


def Result_ToValueOption[A, B](result: FSharpResult_2[A, B]) -> Option[A]:
    match result.tag:
        case 0:
            return some(narrow(Ok, result).result_value)

        case _:
            return None


__all__ = [
    "Error",
    "FSharpResult_2_reflection",
    "Ok",
    "Result_Bind",
    "Result_Contains",
    "Result_Count",
    "Result_DefaultValue",
    "Result_DefaultWith",
    "Result_Exists",
    "Result_Fold",
    "Result_FoldBack",
    "Result_ForAll",
    "Result_IsError",
    "Result_IsOk",
    "Result_Iterate",
    "Result_Map",
    "Result_MapError",
    "Result_ToArray",
    "Result_ToList",
    "Result_ToOption",
    "Result_ToValueOption",
]
