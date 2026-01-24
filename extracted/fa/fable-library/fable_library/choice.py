from __future__ import annotations

from typing import Any

from .array_ import Array
from .option import some
from .reflection import TypeInfo, union_type
from .types import Union, int32
from .util import int32 as int32_1


def _expr21(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`2", [gen0, gen1], FSharpChoice_2, lambda: [[("Item", gen0)], [("Item", gen1)]]
    )


class FSharpChoice_2[T1, T2](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of2", "Choice2Of2"]


FSharpChoice_2_reflection = _expr21


def _expr22(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`3",
        [gen0, gen1, gen2],
        FSharpChoice_3,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)]],
    )


class FSharpChoice_3[T1, T2, T3](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of3", "Choice2Of3", "Choice3Of3"]


FSharpChoice_3_reflection = _expr22


def _expr23(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`4",
        [gen0, gen1, gen2, gen3],
        FSharpChoice_4,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)], [("Item", gen3)]],
    )


class FSharpChoice_4[T1, T2, T3, T4](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of4", "Choice2Of4", "Choice3Of4", "Choice4Of4"]


FSharpChoice_4_reflection = _expr23


def _expr24(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`5",
        [gen0, gen1, gen2, gen3, gen4],
        FSharpChoice_5,
        lambda: [[("Item", gen0)], [("Item", gen1)], [("Item", gen2)], [("Item", gen3)], [("Item", gen4)]],
    )


class FSharpChoice_5[T1, T2, T3, T4, T5](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of5", "Choice2Of5", "Choice3Of5", "Choice4Of5", "Choice5Of5"]


FSharpChoice_5_reflection = _expr24


def _expr25(gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo, gen5: TypeInfo) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`6",
        [gen0, gen1, gen2, gen3, gen4, gen5],
        FSharpChoice_6,
        lambda: [
            [("Item", gen0)],
            [("Item", gen1)],
            [("Item", gen2)],
            [("Item", gen3)],
            [("Item", gen4)],
            [("Item", gen5)],
        ],
    )


class FSharpChoice_6[T1, T2, T3, T4, T5, T6](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of6", "Choice2Of6", "Choice3Of6", "Choice4Of6", "Choice5Of6", "Choice6Of6"]


FSharpChoice_6_reflection = _expr25


def _expr26(
    gen0: TypeInfo, gen1: TypeInfo, gen2: TypeInfo, gen3: TypeInfo, gen4: TypeInfo, gen5: TypeInfo, gen6: TypeInfo
) -> TypeInfo:
    return union_type(
        "FSharp.Core.FSharpChoice`7",
        [gen0, gen1, gen2, gen3, gen4, gen5, gen6],
        FSharpChoice_7,
        lambda: [
            [("Item", gen0)],
            [("Item", gen1)],
            [("Item", gen2)],
            [("Item", gen3)],
            [("Item", gen4)],
            [("Item", gen5)],
            [("Item", gen6)],
        ],
    )


class FSharpChoice_7[T1, T2, T3, T4, T5, T6, T7](Union):
    def __init__(self, tag: int32, *fields: Any) -> None:
        super().__init__()
        self.tag: int32 = tag
        self.fields: Array[Any] = Array[Any](fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Choice1Of7", "Choice2Of7", "Choice3Of7", "Choice4Of7", "Choice5Of7", "Choice6Of7", "Choice7Of7"]


FSharpChoice_7_reflection = _expr26


def Choice_makeChoice1Of2[A, T1](x: T1 | None = None) -> FSharpChoice_2[T1, Any]:
    return FSharpChoice_2(int32_1(0), x)


def Choice_makeChoice2Of2[A, T2](x: T2 | None = None) -> FSharpChoice_2[Any, T2]:
    return FSharpChoice_2(int32_1(1), x)


def Choice_tryValueIfChoice1Of2[T1, T2](x: FSharpChoice_2[T1, Any]) -> T1 | None:
    if x.tag == int32_1(0):
        return some(x.fields[int32_1(0)])

    else:
        return None


def Choice_tryValueIfChoice2Of2[T1, T2](x: FSharpChoice_2[Any, T2]) -> T2 | None:
    if x.tag == int32_1(1):
        return some(x.fields[int32_1(0)])

    else:
        return None


__all__ = [
    "FSharpChoice_2_reflection",
    "FSharpChoice_3_reflection",
    "FSharpChoice_4_reflection",
    "FSharpChoice_5_reflection",
    "FSharpChoice_6_reflection",
    "FSharpChoice_7_reflection",
    "Choice_makeChoice1Of2",
    "Choice_makeChoice2Of2",
    "Choice_tryValueIfChoice1Of2",
    "Choice_tryValueIfChoice2Of2",
]
