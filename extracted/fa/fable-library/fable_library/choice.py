from __future__ import annotations

from typing import Any

from .array_ import Array
from .option import Option, some
from .reflection import TypeInfo, union_type
from .union import Union, tagged_union
from .util import UNIT


def _expr21(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`2",
        Array([gen0, gen1]),
        _FSharpChoice_2,
        lambda: [[("Item", gen0)], [("Item", gen1)]],
        [Choice1Of2, Choice2Of2],
    )


class _FSharpChoice_2[T1, T2](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of2", "Choice2Of2"]


@tagged_union(0)
class Choice1Of2[T1, T2](_FSharpChoice_2[T1, T2]):
    item: T1


@tagged_union(1)
class Choice2Of2[T1, T2](_FSharpChoice_2[T1, T2]):
    item: T2


type FSharpChoice_2[T1, T2] = Choice1Of2[T1, T2] | Choice2Of2[T1, T2]

FSharpChoice_2_reflection = _expr21


def _expr22(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`3",
        Array([gen0, gen1, gen2]),
        _FSharpChoice_3,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)]],
        [Choice1Of3, Choice2Of3, Choice3Of3],
    )


class _FSharpChoice_3[T1, T2, T3](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of3", "Choice2Of3", "Choice3Of3"]


@tagged_union(0)
class Choice1Of3[T1, T2, T3](_FSharpChoice_3[T1, T2, T3]):
    item: T1


@tagged_union(1)
class Choice2Of3[T1, T2, T3](_FSharpChoice_3[T1, T2, T3]):
    item: T2


@tagged_union(2)
class Choice3Of3[T1, T2, T3](_FSharpChoice_3[T1, T2, T3]):
    item: T3


type FSharpChoice_3[T1, T2, T3] = (Choice1Of3[T1, T2, T3] | Choice2Of3[T1, T2, T3]) | Choice3Of3[T1, T2, T3]

FSharpChoice_3_reflection = _expr22


def _expr23(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`4",
        Array([gen0, gen1, gen2, gen3]),
        _FSharpChoice_4,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)], [("Item", gen3)]],
        [Choice1Of4, Choice2Of4, Choice3Of4, Choice4Of4],
    )


class _FSharpChoice_4[T1, T2, T3, T4](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of4", "Choice2Of4", "Choice3Of4", "Choice4Of4"]


@tagged_union(0)
class Choice1Of4[T1, T2, T3, T4](_FSharpChoice_4[T1, T2, T3, T4]):
    item: T1


@tagged_union(1)
class Choice2Of4[T1, T2, T3, T4](_FSharpChoice_4[T1, T2, T3, T4]):
    item: T2


@tagged_union(2)
class Choice3Of4[T1, T2, T3, T4](_FSharpChoice_4[T1, T2, T3, T4]):
    item: T3


@tagged_union(3)
class Choice4Of4[T1, T2, T3, T4](_FSharpChoice_4[T1, T2, T3, T4]):
    item: T4


type FSharpChoice_4[T1, T2, T3, T4] = (
    (Choice1Of4[T1, T2, T3, T4] | Choice2Of4[T1, T2, T3, T4]) | Choice3Of4[T1, T2, T3, T4]
) | Choice4Of4[T1, T2, T3, T4]

FSharpChoice_4_reflection = _expr23


def _expr24(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`5",
        Array([gen0, gen1, gen2, gen3, gen4]),
        _FSharpChoice_5,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)], [("Item", gen3)], [("Item", gen4)]],
        [Choice1Of5, Choice2Of5, Choice3Of5, Choice4Of5, Choice5Of5],
    )


class _FSharpChoice_5[T1, T2, T3, T4, T5](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of5", "Choice2Of5", "Choice3Of5", "Choice4Of5", "Choice5Of5"]


@tagged_union(0)
class Choice1Of5[T1, T2, T3, T4, T5](_FSharpChoice_5[T1, T2, T3, T4, T5]):
    item: T1


@tagged_union(1)
class Choice2Of5[T1, T2, T3, T4, T5](_FSharpChoice_5[T1, T2, T3, T4, T5]):
    item: T2


@tagged_union(2)
class Choice3Of5[T1, T2, T3, T4, T5](_FSharpChoice_5[T1, T2, T3, T4, T5]):
    item: T3


@tagged_union(3)
class Choice4Of5[T1, T2, T3, T4, T5](_FSharpChoice_5[T1, T2, T3, T4, T5]):
    item: T4


@tagged_union(4)
class Choice5Of5[T1, T2, T3, T4, T5](_FSharpChoice_5[T1, T2, T3, T4, T5]):
    item: T5


type FSharpChoice_5[T1, T2, T3, T4, T5] = (
    ((Choice1Of5[T1, T2, T3, T4, T5] | Choice2Of5[T1, T2, T3, T4, T5]) | Choice3Of5[T1, T2, T3, T4, T5])
    | Choice4Of5[T1, T2, T3, T4, T5]
) | Choice5Of5[T1, T2, T3, T4, T5]

FSharpChoice_5_reflection = _expr24


def _expr25(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo, gen5: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`6",
        Array([gen0, gen1, gen2, gen3, gen4, gen5]),
        _FSharpChoice_6,
        lambda: [
            [("Item", gen0)],
            [("Item", gen1)],
            [("Item", gen2)],
            [("Item", gen3)],
            [("Item", gen4)],
            [("Item", gen5)],
        ],
        [Choice1Of6, Choice2Of6, Choice3Of6, Choice4Of6, Choice5Of6, Choice6Of6],
    )


class _FSharpChoice_6[T1, T2, T3, T4, T5, T6](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of6", "Choice2Of6", "Choice3Of6", "Choice4Of6", "Choice5Of6", "Choice6Of6"]


@tagged_union(0)
class Choice1Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T1


@tagged_union(1)
class Choice2Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T2


@tagged_union(2)
class Choice3Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T3


@tagged_union(3)
class Choice4Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T4


@tagged_union(4)
class Choice5Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T5


@tagged_union(5)
class Choice6Of6[T1, T2, T3, T4, T5, T6](_FSharpChoice_6[T1, T2, T3, T4, T5, T6]):
    item: T6


type FSharpChoice_6[T1, T2, T3, T4, T5, T6] = (
    (
        ((Choice1Of6[T1, T2, T3, T4, T5, T6] | Choice2Of6[T1, T2, T3, T4, T5, T6]) | Choice3Of6[T1, T2, T3, T4, T5, T6])
        | Choice4Of6[T1, T2, T3, T4, T5, T6]
    )
    | Choice5Of6[T1, T2, T3, T4, T5, T6]
) | Choice6Of6[T1, T2, T3, T4, T5, T6]

FSharpChoice_6_reflection = _expr25


def _expr26(
    gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo, gen5: TypeInfo, gen6: TypeInfo
) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`7",
        Array([gen0, gen1, gen2, gen3, gen4, gen5, gen6]),
        _FSharpChoice_7,
        lambda: [
            [("Item", gen0)],
            [("Item", gen1)],
            [("Item", gen2)],
            [("Item", gen3)],
            [("Item", gen4)],
            [("Item", gen5)],
            [("Item", gen6)],
        ],
        [Choice1Of7, Choice2Of7, Choice3Of7, Choice4Of7, Choice5Of7, Choice6Of7, Choice7Of7],
    )


class _FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7](Union):
    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of7", "Choice2Of7", "Choice3Of7", "Choice4Of7", "Choice5Of7", "Choice6Of7", "Choice7Of7"]


@tagged_union(0)
class Choice1Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T1


@tagged_union(1)
class Choice2Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T2


@tagged_union(2)
class Choice3Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T3


@tagged_union(3)
class Choice4Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T4


@tagged_union(4)
class Choice5Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T5


@tagged_union(5)
class Choice6Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T6


@tagged_union(6)
class Choice7Of7[T1, T2, T3, T4, T5, T6, T7](_FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7]):
    item: T7


type FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7] = (
    (
        (
            (
                (Choice1Of7[T1, T2, T3, T4, T5, T6, T7] | Choice2Of7[T1, T2, T3, T4, T5, T6, T7])
                | Choice3Of7[T1, T2, T3, T4, T5, T6, T7]
            )
            | Choice4Of7[T1, T2, T3, T4, T5, T6, T7]
        )
        | Choice5Of7[T1, T2, T3, T4, T5, T6, T7]
    )
    | Choice6Of7[T1, T2, T3, T4, T5, T6, T7]
) | Choice7Of7[T1, T2, T3, T4, T5, T6, T7]

FSharpChoice_7_reflection = _expr26


def Choice_makeChoice1Of2[T1, A](x: T1 = UNIT) -> FSharpChoice_2[T1, Any]:
    return Choice1Of2(x)


def Choice_makeChoice2Of2[T2, A](x: T2 = UNIT) -> FSharpChoice_2[Any, T2]:
    return Choice2Of2(x)


def Choice_tryValueIfChoice1Of2[T1, T2](x: FSharpChoice_2[T1, Any]) -> Option[T1]:
    match x.tag:
        case 0:
            return some(x.fields[0])

        case _:
            return None


def Choice_tryValueIfChoice2Of2[T1, T2](x: FSharpChoice_2[Any, T2]) -> Option[T2]:
    match x.tag:
        case 1:
            return some(x.fields[0])

        case _:
            return None


__all__ = [
    "Choice1Of2",
    "Choice1Of3",
    "Choice1Of4",
    "Choice1Of5",
    "Choice1Of6",
    "Choice1Of7",
    "Choice2Of2",
    "Choice2Of3",
    "Choice2Of4",
    "Choice2Of5",
    "Choice2Of6",
    "Choice2Of7",
    "Choice3Of3",
    "Choice3Of4",
    "Choice3Of5",
    "Choice3Of6",
    "Choice3Of7",
    "Choice4Of4",
    "Choice4Of5",
    "Choice4Of6",
    "Choice4Of7",
    "Choice5Of5",
    "Choice5Of6",
    "Choice5Of7",
    "Choice6Of6",
    "Choice6Of7",
    "Choice7Of7",
    "Choice_makeChoice1Of2",
    "Choice_makeChoice2Of2",
    "Choice_tryValueIfChoice1Of2",
    "Choice_tryValueIfChoice2Of2",
    "FSharpChoice_2_reflection",
    "FSharpChoice_3_reflection",
    "FSharpChoice_4_reflection",
    "FSharpChoice_5_reflection",
    "FSharpChoice_6_reflection",
    "FSharpChoice_7_reflection",
]
