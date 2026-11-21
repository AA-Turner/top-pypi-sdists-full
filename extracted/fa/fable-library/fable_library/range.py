from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import Any

from .big_int import from_zero, op_addition
from .char import char_code_at
from .core import byte, float32, int8, int16, int32, int64, op_division_float64, sbyte, uint8, uint16, uint32, uint64
from .decimal_ import from_parts
from .decimal_ import op_addition as op_addition_1
from .double import floor
from .fsharp_core import Operators_InvalidArg
from .option import erase
from .protocols import IEnumerable_1
from .seq import delay, empty, singleton
from .seq_native import map, unfold
from .util import UNIT, Unit, compare


def make_range_step_function[T](
    step: T, stop: T, zero: T, add: Callable[[T, T], T]
) -> Callable[[T], tuple[T, T] | None]:
    step_compared_with_zero: int = compare(step, zero)
    if step_compared_with_zero == 0:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    step_greater_than_zero: bool = step_compared_with_zero > 0

    def _arrow55(x: T = UNIT, step: Any = step, stop: Any = stop, add: Any = add) -> tuple[T, T] | None:
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

    return _arrow55


def integral_range_step[T](start: T, step: T, stop: T, zero: T, add: Callable[[T, T], T]) -> IEnumerable_1[T]:
    step_fn: Callable[[Any], tuple[Any, Any] | None] = erase(make_range_step_function(step, stop, zero, add))

    def _arrow56(__unit: Unit = UNIT, start: Any = start) -> IEnumerable_1[T]:
        return unfold(step_fn, start)

    return delay(_arrow56)


def range_big_int(start: int, step: int, stop: int) -> IEnumerable_1[int]:
    return integral_range_step(start, step, stop, from_zero(), op_addition)


def range_decimal(start: Decimal, step: Decimal, stop: Decimal) -> IEnumerable_1[Decimal]:
    return integral_range_step(start, step, stop, from_parts(0, 0, 0, False, uint8.ZERO), op_addition_1)


def range_double(start: float, step: float, stop: float) -> IEnumerable_1[float]:
    def _arrow57(x: float, y: float) -> float:
        return x + y

    return integral_range_step(start, step, stop, 0.0, _arrow57)


def floating_range_step(
    round: Callable[[float], float], start: float, step: float, stop: float
) -> IEnumerable_1[float]:
    if start != start:
        Operators_InvalidArg("n", "The start of a range cannot be NaN.")

    if step != step:
        Operators_InvalidArg("step", "The step of a range cannot be NaN.")

    if stop != stop:
        Operators_InvalidArg("m", "The end of a range cannot be NaN.")

    if start == stop:
        return singleton(start)

    else:
        up: bool = start < stop
        if True if ((step < 0.0) if up else False) else ((step > 0.0) if (not up) else False):
            return empty()

        else:

            def before(a: float, b: float) -> bool:
                if up:
                    return a < b

                else:
                    return a > b

            def step_fn(
                x: float | None = None, round: Any = round, step: Any = step, stop: Any = stop
            ) -> tuple[float, float | None] | None:
                if x is not None:
                    x_1: float = x
                    next_1: float = round(x_1 + step)
                    if (
                        (True if (before(next_1, stop) if before(x_1, next_1) else False) else (next_1 == stop))
                        if (next_1 != x_1)
                        else False
                    ):
                        return (x_1, next_1)

                    else:
                        return (x_1, None)

                else:
                    return None

            return unfold(step_fn, start)


def floating_range(round: Callable[[float], float], start: float, step: float, stop: float) -> IEnumerable_1[float]:
    def _arrow58(
        __unit: Unit = UNIT, round: Any = round, start: Any = start, step: Any = step, stop: Any = stop
    ) -> IEnumerable_1[float]:
        if step == 0.0:
            Operators_InvalidArg("step", "The step of a range cannot be zero.")

        num_steps: float = round(op_division_float64(round(stop - start), step))

        def step_fn(i: float) -> tuple[float, float] | None:
            if i <= num_steps:
                return (round(start + round(round(i) * step)), i + 1.0)

            else:
                return None

        return (
            unfold(step_fn, 0.0)
            if (
                (floor(num_steps) == num_steps)
                if ((num_steps <= 2147483647.0) if (-2147483648.0 <= num_steps) else False)
                else False
            )
            else floating_range_step(round, start, step, stop)
        )

    return delay(_arrow58)


def range_float(start: float, step: float, stop: float) -> IEnumerable_1[float]:
    def _arrow59(x: float) -> float:
        return x

    return floating_range(_arrow59, start, step, stop)


def range_single(start: float32, step: float32, stop: float32) -> IEnumerable_1[float32]:
    def _arrow60(x: float) -> float:
        return float(float32(x))

    return map(float32, floating_range(_arrow60, float(start), float(step), float(stop)))


def range_sbyte(start: sbyte, step: sbyte, stop: sbyte) -> IEnumerable_1[sbyte]:
    start_1: sbyte = start
    step_1: sbyte = step
    stop_1: sbyte = stop
    if step_1 == int8.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > int8.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: sbyte | None = None) -> tuple[sbyte, sbyte | None] | None:
            if x_1 is not None:
                x_2: sbyte = x_1

                def _arrow61(__unit: Unit = UNIT) -> bool:
                    x: sbyte = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= int8.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= int8.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow61():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_byte(start: byte, step: byte, stop: byte) -> IEnumerable_1[byte]:
    start_1: byte = start
    step_1: byte = step
    stop_1: byte = stop
    if step_1 == uint8.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > uint8.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: byte | None = None) -> tuple[byte, byte | None] | None:
            if x_1 is not None:
                x_2: byte = x_1

                def _arrow62(__unit: Unit = UNIT) -> bool:
                    x: byte = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= uint8.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= uint8.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow62():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_int16(start: int16, step: int16, stop: int16) -> IEnumerable_1[int16]:
    start_1: int16 = start
    step_1: int16 = step
    stop_1: int16 = stop
    if step_1 == int16.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > int16.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: int16 | None = None) -> tuple[int16, int16 | None] | None:
            if x_1 is not None:
                x_2: int16 = x_1

                def _arrow63(__unit: Unit = UNIT) -> bool:
                    x: int16 = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= int16.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= int16.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow63():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_uint16(start: uint16, step: uint16, stop: uint16) -> IEnumerable_1[uint16]:
    start_1: uint16 = start
    step_1: uint16 = step
    stop_1: uint16 = stop
    if step_1 == uint16.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > uint16.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: uint16 | None = None) -> tuple[uint16, uint16 | None] | None:
            if x_1 is not None:
                x_2: uint16 = x_1

                def _arrow64(__unit: Unit = UNIT) -> bool:
                    x: uint16 = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= uint16.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= uint16.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow64():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_int32(start: int, step: int, stop: int) -> IEnumerable_1[int]:
    start_1: int = start
    step_1: int = step
    stop_1: int = stop
    if step_1 == 0:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > 0
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: int | None = None) -> tuple[int, int | None] | None:
            if x_1 is not None:
                x_2: int = x_1

                def _arrow65(__unit: Unit = UNIT) -> bool:
                    x: int = x_2
                    return (
                        (
                            ((tmp if (-2147483648 <= (tmp := stop_1 - x) <= 2147483647) else int32(tmp)) >= step_1)
                            if (x >= 0)
                            else (
                                (tmp_1 if (-2147483648 <= (tmp_1 := x + step_1) <= 2147483647) else int32(tmp_1))
                                <= stop_1
                            )
                        )
                        if up
                        else (
                            (
                                (tmp_2 if (-2147483648 <= (tmp_2 := stop_1 - x) <= 2147483647) else int32(tmp_2))
                                <= step_1
                            )
                            if (x <= 0)
                            else (
                                (tmp_3 if (-2147483648 <= (tmp_3 := x + step_1) <= 2147483647) else int32(tmp_3))
                                >= stop_1
                            )
                        )
                    )

                if _arrow65():
                    return (x_2, tmp_4 if (-2147483648 <= (tmp_4 := x_2 + step_1) <= 2147483647) else int32(tmp_4))

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_uint32(start: uint32, step: uint32, stop: uint32) -> IEnumerable_1[uint32]:
    start_1: uint32 = start
    step_1: uint32 = step
    stop_1: uint32 = stop
    if step_1 == uint32.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > uint32.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: uint32 | None = None) -> tuple[uint32, uint32 | None] | None:
            if x_1 is not None:
                x_2: uint32 = x_1

                def _arrow66(__unit: Unit = UNIT) -> bool:
                    x: uint32 = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= uint32.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= uint32.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow66():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_int64(start: int64, step: int64, stop: int64) -> IEnumerable_1[int64]:
    start_1: int64 = start
    step_1: int64 = step
    stop_1: int64 = stop
    if step_1 == int64.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > int64.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: int64 | None = None) -> tuple[int64, int64 | None] | None:
            if x_1 is not None:
                x_2: int64 = x_1

                def _arrow67(__unit: Unit = UNIT) -> bool:
                    x: int64 = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= int64.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= int64.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow67():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_uint64(start: uint64, step: uint64, stop: uint64) -> IEnumerable_1[uint64]:
    start_1: uint64 = start
    step_1: uint64 = step
    stop_1: uint64 = stop
    if step_1 == uint64.ZERO:
        Operators_InvalidArg("step", "The step of a range cannot be zero.")

    up: bool = step_1 > uint64.ZERO
    if True if ((start_1 <= stop_1) if up else False) else ((start_1 >= stop_1) if (not up) else False):

        def step_fn(x_1: uint64 | None = None) -> tuple[uint64, uint64 | None] | None:
            if x_1 is not None:
                x_2: uint64 = x_1

                def _arrow68(__unit: Unit = UNIT) -> bool:
                    x: uint64 = x_2
                    return (
                        (((stop_1 - x) >= step_1) if (x >= uint64.ZERO) else ((x + step_1) <= stop_1))
                        if up
                        else (((stop_1 - x) <= step_1) if (x <= uint64.ZERO) else ((x + step_1) >= stop_1))
                    )

                if _arrow68():
                    return (x_2, x_2 + step_1)

                else:
                    return (x_2, None)

            else:
                return None

        return unfold(step_fn, start_1)

    else:
        return empty()


def range_char(start: str, stop: str) -> IEnumerable_1[str]:
    int_stop: int = int32(char_code_at(stop, 0))

    def _arrow69(__unit: Unit = UNIT, start: Any = start) -> IEnumerable_1[str]:
        def step_fn(i: int) -> tuple[str, int] | None:
            if i <= int_stop:
                return (chr(int(i)), (i + 1) if (i <= 2147483646) else int32(i + 1))

            else:
                return None

        return unfold(step_fn, int32(char_code_at(start, 0)))

    return delay(_arrow69)


__all__ = [
    "floating_range",
    "floating_range_step",
    "integral_range_step",
    "make_range_step_function",
    "range_big_int",
    "range_byte",
    "range_char",
    "range_decimal",
    "range_double",
    "range_float",
    "range_int16",
    "range_int32",
    "range_int64",
    "range_sbyte",
    "range_single",
    "range_uint16",
    "range_uint32",
    "range_uint64",
]
