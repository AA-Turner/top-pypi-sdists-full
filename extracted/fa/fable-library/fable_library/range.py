from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import Any

from .big_int import from_zero, op_addition
from .char import char_code_at
from .decimal_ import from_parts
from .decimal_ import op_addition as op_addition_1
from .long import op_addition as op_addition_2
from .seq import delay, unfold
from .types import float64, int32, int64, uint8, uint64
from .util import IEnumerable_1, compare


def make_range_step_function[T](
    step: T, stop: T, zero: T, add: Callable[[T, T], T]
) -> Callable[[T], tuple[T, T] | None]:
    step_compared_with_zero: int32 = compare(step, zero)
    if step_compared_with_zero == int32.ZERO:
        raise Exception("The step of a range cannot be zero")

    step_greater_than_zero: bool = step_compared_with_zero > int32.ZERO

    def _arrow82(
        x: T | None = None, step: Any = step, stop: Any = stop, zero: Any = zero, add: Any = add
    ) -> tuple[T, T] | None:
        compared_with_last: int32 = compare(x, stop)
        return (
            ((x, add(x, step)))
            if (
                True
                if ((compared_with_last <= int32.ZERO) if step_greater_than_zero else False)
                else ((compared_with_last >= int32.ZERO) if (not step_greater_than_zero) else False)
            )
            else None
        )

    return _arrow82


def integral_range_step[T](start: T, step: T, stop: T, zero: T, add: Callable[[T, T], T]) -> IEnumerable_1[T]:
    step_fn: Callable[[T], tuple[T, T] | None] = make_range_step_function(step, stop, zero, add)

    def _arrow83(
        __unit: None = None, start: Any = start, step: Any = step, stop: Any = stop, zero: Any = zero, add: Any = add
    ) -> IEnumerable_1[T]:
        return unfold(step_fn, start)

    return delay(_arrow83)


def range_big_int(start: int, step: int, stop: int) -> IEnumerable_1[int]:
    def _arrow84(x: int, y: int, start: Any = start, step: Any = step, stop: Any = stop) -> int:
        return op_addition(x, y)

    return integral_range_step(start, step, stop, from_zero(), _arrow84)


def range_decimal(start: Decimal, step: Decimal, stop: Decimal) -> IEnumerable_1[Decimal]:
    def _arrow85(x: Decimal, y: Decimal, start: Any = start, step: Any = step, stop: Any = stop) -> Decimal:
        return op_addition_1(x, y)

    return integral_range_step(
        start, step, stop, from_parts(int32.ZERO, int32.ZERO, int32.ZERO, False, uint8.ZERO), _arrow85
    )


def range_double(start: float64, step: float64, stop: float64) -> IEnumerable_1[float64]:
    def _arrow86(x: float64, y: float64, start: Any = start, step: Any = step, stop: Any = stop) -> float64:
        return x + y

    return integral_range_step(start, step, stop, float64(0.0), _arrow86)


def range_int64(start: int64, step: int64, stop: int64) -> IEnumerable_1[int64]:
    def _arrow87(x: int64, y: int64, start: Any = start, step: Any = step, stop: Any = stop) -> int64:
        return op_addition_2(x, y)

    return integral_range_step(start, step, stop, int64.ZERO, _arrow87)


def range_uint64(start: uint64, step: uint64, stop: uint64) -> IEnumerable_1[uint64]:
    def _arrow88(x: uint64, y: uint64, start: Any = start, step: Any = step, stop: Any = stop) -> uint64:
        return op_addition_2(x, y)

    return integral_range_step(start, step, stop, uint64.ZERO, _arrow88)


def range_char(start: str, stop: str) -> IEnumerable_1[str]:
    int_stop: int32 = int32(char_code_at(stop, int32.ZERO))

    def _arrow90(__unit: None = None, start: Any = start, stop: Any = stop) -> IEnumerable_1[str]:
        def step_fn(i: int32) -> tuple[str, int32] | None:
            if i <= int_stop:
                return (chr(int(i)), i + int32.ONE)

            else:
                return None

        return unfold(step_fn, int32(char_code_at(start, int32.ZERO)))

    return delay(_arrow90)


__all__ = [
    "make_range_step_function",
    "integral_range_step",
    "range_big_int",
    "range_decimal",
    "range_double",
    "range_int64",
    "range_uint64",
    "range_char",
]
