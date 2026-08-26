from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import Any

from .big_int import from_zero, op_addition
from .char import char_code_at
from .core import int32, int64, uint8, uint32, uint64
from .decimal_ import from_parts
from .decimal_ import op_addition as op_addition_1
from .option import erase
from .protocols import IEnumerable_1
from .seq import delay
from .seq_native import unfold
from .util import UNIT, compare


def make_range_step_function[T](
    step: T, stop: T, zero: T, add: Callable[[T, T], T]
) -> Callable[[T], tuple[T, T] | None]:
    step_compared_with_zero: int = compare(step, zero)
    if step_compared_with_zero == 0:
        raise Exception("The step of a range cannot be zero")

    step_greater_than_zero: bool = step_compared_with_zero > 0

    def _arrow66(x: T = UNIT, step: Any = step, stop: Any = stop, add: Any = add) -> tuple[T, T] | None:
        compared_with_last: int = compare(x, stop)
        return (
            ((x, add(x, step)))
            if (
                True
                if ((compared_with_last <= 0) if step_greater_than_zero else False)
                else ((compared_with_last >= 0) if (not step_greater_than_zero) else False)
            )
            else None
        )

    return _arrow66


def integral_range_step[T](start: T, step: T, stop: T, zero: T, add: Callable[[T, T], T]) -> IEnumerable_1[T]:
    step_fn: Callable[[Any], tuple[Any, Any] | None] = erase(make_range_step_function(step, stop, zero, add))

    def _arrow67(start: Any = start) -> IEnumerable_1[T]:
        return unfold(step_fn, start)

    return delay(_arrow67)


def range_big_int(start: int, step: int, stop: int) -> IEnumerable_1[int]:
    return integral_range_step(start, step, stop, from_zero(), op_addition)


def range_decimal(start: Decimal, step: Decimal, stop: Decimal) -> IEnumerable_1[Decimal]:
    return integral_range_step(start, step, stop, from_parts(0, 0, 0, False, uint8.ZERO), op_addition_1)


def range_double(start: float, step: float, stop: float) -> IEnumerable_1[float]:
    def _arrow71(x: float, y: float) -> float:
        return x + y

    return integral_range_step(start, step, stop, 0.0, _arrow71)


def range_int32(start: int, step: int, stop: int) -> IEnumerable_1[int]:
    def _arrow72(x: int, y: int) -> int:
        return tmp if (-2147483648 <= (tmp := x + y) <= 2147483647) else int32(tmp)

    return integral_range_step(start, step, stop, 0, _arrow72)


def range_uint32(start: uint32, step: uint32, stop: uint32) -> IEnumerable_1[uint32]:
    def _arrow73(x: uint32, y: uint32) -> uint32:
        return x + y

    return integral_range_step(start, step, stop, uint32.ZERO, _arrow73)


def range_int64(start: int64, step: int64, stop: int64) -> IEnumerable_1[int64]:
    def _arrow74(x: int64, y: int64) -> int64:
        return x + y

    return integral_range_step(start, step, stop, int64.ZERO, _arrow74)


def range_uint64(start: uint64, step: uint64, stop: uint64) -> IEnumerable_1[uint64]:
    def _arrow75(x: uint64, y: uint64) -> uint64:
        return x + y

    return integral_range_step(start, step, stop, uint64.ZERO, _arrow75)


def range_char(start: str, stop: str) -> IEnumerable_1[str]:
    int_stop: int = int32(char_code_at(stop, 0))

    def _arrow76(start: Any = start) -> IEnumerable_1[str]:
        def step_fn(i: int) -> tuple[str, int] | None:
            if i <= int_stop:
                return (chr(int(i)), (i + 1) if (i <= 2147483646) else int32(i + 1))

            else:
                return None

        return unfold(step_fn, int32(char_code_at(start, 0)))

    return delay(_arrow76)


__all__ = [
    "integral_range_step",
    "make_range_step_function",
    "range_big_int",
    "range_char",
    "range_decimal",
    "range_double",
    "range_int32",
    "range_int64",
    "range_uint32",
    "range_uint64",
]
