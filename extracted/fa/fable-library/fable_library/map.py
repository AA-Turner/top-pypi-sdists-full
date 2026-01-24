from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from .array_ import Array, create
from .array_ import map as map_2
from .list import FSharpList, cons, head, of_array_with_tail, singleton, tail
from .list import empty as empty_1
from .list import fold as fold_1
from .list import is_empty as is_empty_1
from .option import some
from .option import value as value_1
from .reflection import TypeInfo, bool_type, class_type, list_type, option_type, record_type
from .seq import compare_with, unfold
from .seq import iterate as iterate_1
from .seq import map as map_1
from .seq import pick as pick_1
from .seq import try_pick as try_pick_1
from .string_ import format, join
from .system import NotSupportedException__ctor_Z721C83C5
from .types import FSharpRef, Record, int32
from .util import (
    ICollection,
    IComparer_1,
    IEnumerable_1,
    IEnumerator,
    compare,
    equals,
    get_enumerator,
    ignore,
    is_array_like,
    range,
    structural_hash,
    to_iterator,
)
from .util import int32 as int32_1


def _expr244(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.MapTreeLeaf`2", [gen0, gen1], MapTreeLeaf_2)


class MapTreeLeaf_2[KEY, VALUE]:
    def __init__(self, k: Any, v: Any) -> None:
        self.k: KEY = k
        self.v: VALUE = v


MapTreeLeaf_2_reflection = _expr244


def MapTreeLeaf_2__ctor_5BDDA1(k: Any, v: Any) -> MapTreeLeaf_2[KEY, VALUE]:
    return MapTreeLeaf_2(k, v)


def MapTreeLeaf_2__get_Key[KEY](_: MapTreeLeaf_2[KEY, Any]) -> KEY:
    return _.k


def MapTreeLeaf_2__get_Value[VALUE](_: MapTreeLeaf_2[Any, VALUE]) -> VALUE:
    return _.v


def _expr245(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.MapTreeNode`2", [gen0, gen1], MapTreeNode_2, MapTreeLeaf_2_reflection(gen0, gen1))


class MapTreeNode_2[KEY, VALUE](MapTreeLeaf_2):
    def __init__(
        self,
        k: KEY,
        v: VALUE,
        left: MapTreeLeaf_2[KEY, VALUE] | None,
        right: MapTreeLeaf_2[KEY, VALUE] | None,
        h: int32,
    ) -> None:
        super().__init__(k, v)
        self.left: MapTreeLeaf_2[KEY, VALUE] | None = left
        self.right: MapTreeLeaf_2[KEY, VALUE] | None = right
        self.h: int32 = h


MapTreeNode_2_reflection = _expr245


def MapTreeNode_2__ctor_Z39DE9543(
    k: KEY, v: VALUE, left: MapTreeLeaf_2[KEY, VALUE] | None, right: MapTreeLeaf_2[KEY, VALUE] | None, h: int32
) -> MapTreeNode_2[KEY, VALUE]:
    return MapTreeNode_2(k, v, left, right, h)


def MapTreeNode_2__get_Left[KEY, VALUE](_: MapTreeNode_2[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return _.left


def MapTreeNode_2__get_Right[KEY, VALUE](_: MapTreeNode_2[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return _.right


def MapTreeNode_2__get_Height(_: MapTreeNode_2[Any, Any]) -> int32:
    return _.h


def MapTreeModule_empty[KEY, VALUE](__unit: None = None) -> MapTreeLeaf_2[Any, Any] | None:
    return None


def MapTreeModule_sizeAux[KEY, VALUE](acc_mut: int32, m_mut: MapTreeLeaf_2[Any, Any] | None) -> int32:
    while True:
        (acc, m) = (acc_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                acc_mut = MapTreeModule_sizeAux(acc + int32.ONE, MapTreeNode_2__get_Left(m2))
                m_mut = MapTreeNode_2__get_Right(m2)
                continue

            else:
                return acc + int32.ONE

        else:
            return acc

        break


def MapTreeModule_size[_A, _B](x: MapTreeLeaf_2[Any, Any] | None = None) -> int32:
    return MapTreeModule_sizeAux(int32.ZERO, x)


def MapTreeModule_mk[KEY, VALUE](
    l: MapTreeLeaf_2[KEY, VALUE] | None, k: KEY, v: VALUE, r: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    hl: int32
    m: MapTreeLeaf_2[KEY, VALUE] | None = l
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        hl = MapTreeNode_2__get_Height(m2) if isinstance(m2, MapTreeNode_2) else int32.ONE

    else:
        hl = int32.ZERO

    hr: int32
    m_1: MapTreeLeaf_2[KEY, VALUE] | None = r
    if m_1 is not None:
        m2_1: MapTreeLeaf_2[KEY, VALUE] = m_1
        hr = MapTreeNode_2__get_Height(m2_1) if isinstance(m2_1, MapTreeNode_2) else int32.ONE

    else:
        hr = int32.ZERO

    m_2: int32 = hr if (hl < hr) else hl
    if m_2 == int32.ZERO:
        return MapTreeLeaf_2__ctor_5BDDA1(k, v)

    else:
        return MapTreeNode_2__ctor_Z39DE9543(k, v, l, r, m_2 + int32.ONE)


def MapTreeModule_rebalance[KEY, VALUE](
    t1: MapTreeLeaf_2[KEY, VALUE] | None, k: KEY, v: VALUE, t2: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    t1h: int32
    m: MapTreeLeaf_2[KEY, VALUE] | None = t1
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        t1h = MapTreeNode_2__get_Height(m2) if isinstance(m2, MapTreeNode_2) else int32.ONE

    else:
        t1h = int32.ZERO

    t2h: int32
    m_1: MapTreeLeaf_2[KEY, VALUE] | None = t2
    if m_1 is not None:
        m2_1: MapTreeLeaf_2[KEY, VALUE] = m_1
        t2h = MapTreeNode_2__get_Height(m2_1) if isinstance(m2_1, MapTreeNode_2) else int32.ONE

    else:
        t2h = int32.ZERO

    if t2h > (t1h + int32.TWO):
        match_value: MapTreeLeaf_2[KEY, VALUE] = value_1(t2)
        if isinstance(match_value, MapTreeNode_2):
            match_value = cast(MapTreeNode_2[KEY, VALUE], match_value)

            def _arrow246(__unit: None = None, t1: Any = t1, k: Any = k, v: Any = v, t2: Any = t2) -> int32:
                m_2: MapTreeLeaf_2[KEY, VALUE] | None = MapTreeNode_2__get_Left(match_value)
                if m_2 is not None:
                    m2_2: MapTreeLeaf_2[KEY, VALUE] = m_2
                    return MapTreeNode_2__get_Height(m2_2) if isinstance(m2_2, MapTreeNode_2) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow246() > (t1h + int32.ONE):
                match_value_1: MapTreeLeaf_2[KEY, VALUE] = value_1(MapTreeNode_2__get_Left(match_value))
                if isinstance(match_value_1, MapTreeNode_2):
                    match_value_1 = cast(MapTreeNode_2[KEY, VALUE], match_value_1)
                    return MapTreeModule_mk(
                        MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(match_value_1)),
                        MapTreeLeaf_2__get_Key(match_value_1),
                        MapTreeLeaf_2__get_Value(match_value_1),
                        MapTreeModule_mk(
                            MapTreeNode_2__get_Right(match_value_1),
                            MapTreeLeaf_2__get_Key(match_value),
                            MapTreeLeaf_2__get_Value(match_value),
                            MapTreeNode_2__get_Right(match_value),
                        ),
                    )

                else:
                    raise Exception("internal error: Map.rebalance")

            else:
                return MapTreeModule_mk(
                    MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(match_value)),
                    MapTreeLeaf_2__get_Key(match_value),
                    MapTreeLeaf_2__get_Value(match_value),
                    MapTreeNode_2__get_Right(match_value),
                )

        else:
            raise Exception("internal error: Map.rebalance")

    elif t1h > (t2h + int32.TWO):
        match_value_2: MapTreeLeaf_2[KEY, VALUE] = value_1(t1)
        if isinstance(match_value_2, MapTreeNode_2):
            match_value_2 = cast(MapTreeNode_2[KEY, VALUE], match_value_2)

            def _arrow247(__unit: None = None, t1: Any = t1, k: Any = k, v: Any = v, t2: Any = t2) -> int32:
                m_3: MapTreeLeaf_2[KEY, VALUE] | None = MapTreeNode_2__get_Right(match_value_2)
                if m_3 is not None:
                    m2_3: MapTreeLeaf_2[KEY, VALUE] = m_3
                    return MapTreeNode_2__get_Height(m2_3) if isinstance(m2_3, MapTreeNode_2) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow247() > (t2h + int32.ONE):
                match_value_3: MapTreeLeaf_2[KEY, VALUE] = value_1(MapTreeNode_2__get_Right(match_value_2))
                if isinstance(match_value_3, MapTreeNode_2):
                    match_value_3 = cast(MapTreeNode_2[KEY, VALUE], match_value_3)
                    return MapTreeModule_mk(
                        MapTreeModule_mk(
                            MapTreeNode_2__get_Left(match_value_2),
                            MapTreeLeaf_2__get_Key(match_value_2),
                            MapTreeLeaf_2__get_Value(match_value_2),
                            MapTreeNode_2__get_Left(match_value_3),
                        ),
                        MapTreeLeaf_2__get_Key(match_value_3),
                        MapTreeLeaf_2__get_Value(match_value_3),
                        MapTreeModule_mk(MapTreeNode_2__get_Right(match_value_3), k, v, t2),
                    )

                else:
                    raise Exception("internal error: Map.rebalance")

            else:
                return MapTreeModule_mk(
                    MapTreeNode_2__get_Left(match_value_2),
                    MapTreeLeaf_2__get_Key(match_value_2),
                    MapTreeLeaf_2__get_Value(match_value_2),
                    MapTreeModule_mk(MapTreeNode_2__get_Right(match_value_2), k, v, t2),
                )

        else:
            raise Exception("internal error: Map.rebalance")

    else:
        return MapTreeModule_mk(t1, k, v, t2)


def MapTreeModule_add[KEY, VALUE](
    comparer: IComparer_1[KEY], k: KEY, v: VALUE, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            if c < int32.ZERO:
                return MapTreeModule_rebalance(
                    MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Left(m2)),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeNode_2__get_Right(m2),
                )

            elif c == int32.ZERO:
                return MapTreeNode_2__ctor_Z39DE9543(
                    k, v, MapTreeNode_2__get_Left(m2), MapTreeNode_2__get_Right(m2), MapTreeNode_2__get_Height(m2)
                )

            else:
                return MapTreeModule_rebalance(
                    MapTreeNode_2__get_Left(m2),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Right(m2)),
                )

        elif c < int32.ZERO:
            return MapTreeNode_2__ctor_Z39DE9543(k, v, MapTreeModule_empty(), m, int32.TWO)

        elif c == int32.ZERO:
            return MapTreeLeaf_2__ctor_5BDDA1(k, v)

        else:
            return MapTreeNode_2__ctor_Z39DE9543(k, v, m, MapTreeModule_empty(), int32.TWO)

    else:
        return MapTreeLeaf_2__ctor_5BDDA1(k, v)


def MapTreeModule_tryFind[KEY, VALUE](
    comparer_mut: IComparer_1[KEY], k_mut: KEY, m_mut: MapTreeLeaf_2[KEY, VALUE] | None
) -> VALUE | None:
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if c == int32.ZERO:
                return some(MapTreeLeaf_2__get_Value(m2))

            elif isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                comparer_mut = comparer
                k_mut = k
                m_mut = MapTreeNode_2__get_Left(m2) if (c < int32.ZERO) else MapTreeNode_2__get_Right(m2)
                continue

            else:
                return None

        else:
            return None

        break


def MapTreeModule_find[KEY, VALUE](
    comparer: IComparer_1[KEY], k: KEY, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> VALUE:
    match_value: VALUE | None = MapTreeModule_tryFind(comparer, k, m)
    if match_value is None:
        raise Exception()

    else:
        return value_1(match_value)


def MapTreeModule_partition1[KEY, _A](
    comparer: IComparer_1[KEY],
    f: Any,
    k: KEY,
    v: _A,
    acc1: MapTreeLeaf_2[KEY, _A] | None = None,
    acc2: MapTreeLeaf_2[KEY, _A] | None = None,
) -> tuple[MapTreeLeaf_2[KEY, _A] | None, MapTreeLeaf_2[KEY, _A] | None]:
    if f(k, v):
        return (MapTreeModule_add(comparer, k, v, acc1), acc2)

    else:
        return (acc1, MapTreeModule_add(comparer, k, v, acc2))


def MapTreeModule_partitionAux[KEY, VALUE](
    comparer_mut: IComparer_1[KEY],
    f_mut: Any,
    m_mut: MapTreeLeaf_2[KEY, VALUE] | None,
    acc__mut: MapTreeLeaf_2[KEY, VALUE] | None,
    acc__1_mut: MapTreeLeaf_2[KEY, VALUE] | None,
) -> tuple[MapTreeLeaf_2[KEY, VALUE] | None, MapTreeLeaf_2[KEY, VALUE] | None]:
    while True:
        (comparer, f, m, acc_, acc__1) = (comparer_mut, f_mut, m_mut, acc__mut, acc__1_mut)
        acc: tuple[MapTreeLeaf_2[KEY, VALUE] | None, MapTreeLeaf_2[KEY, VALUE] | None] = (acc_, acc__1)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                acc_1: tuple[MapTreeLeaf_2[KEY, VALUE] | None, MapTreeLeaf_2[KEY, VALUE] | None] = (
                    MapTreeModule_partitionAux(
                        comparer, f, MapTreeNode_2__get_Right(m2), acc[int32_1(0)], acc[int32_1(1)]
                    )
                )
                acc_4: tuple[MapTreeLeaf_2[KEY, VALUE] | None, MapTreeLeaf_2[KEY, VALUE] | None] = (
                    MapTreeModule_partition1(
                        comparer,
                        f,
                        MapTreeLeaf_2__get_Key(m2),
                        MapTreeLeaf_2__get_Value(m2),
                        acc_1[int32_1(0)],
                        acc_1[int32_1(1)],
                    )
                )
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(m2)
                acc__mut = acc_4[int32_1(0)]
                acc__1_mut = acc_4[int32_1(1)]
                continue

            else:
                return MapTreeModule_partition1(
                    comparer,
                    f,
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    acc[int32_1(0)],
                    acc[int32_1(1)],
                )

        else:
            return acc

        break


def MapTreeModule_partition[KEY, _A](
    comparer: IComparer_1[KEY], f: Callable[[KEY, _A], bool], m: MapTreeLeaf_2[KEY, _A] | None = None
) -> tuple[MapTreeLeaf_2[KEY, _A] | None, MapTreeLeaf_2[KEY, _A] | None]:
    return MapTreeModule_partitionAux(comparer, f, m, MapTreeModule_empty(), MapTreeModule_empty())


def MapTreeModule_filter1[KEY, _A](
    comparer: IComparer_1[KEY], f: Any, k: KEY, v: _A, acc: MapTreeLeaf_2[KEY, _A] | None = None
) -> MapTreeLeaf_2[KEY, _A] | None:
    if f(k, v):
        return MapTreeModule_add(comparer, k, v, acc)

    else:
        return acc


def MapTreeModule_filterAux[KEY, VALUE](
    comparer_mut: IComparer_1[KEY],
    f_mut: Any,
    m_mut: MapTreeLeaf_2[KEY, VALUE] | None,
    acc_mut: MapTreeLeaf_2[KEY, VALUE] | None,
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    while True:
        (comparer, f, m, acc) = (comparer_mut, f_mut, m_mut, acc_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                acc_1: MapTreeLeaf_2[KEY, VALUE] | None = MapTreeModule_filterAux(
                    comparer, f, MapTreeNode_2__get_Left(m2), acc
                )
                acc_2: MapTreeLeaf_2[KEY, VALUE] | None = MapTreeModule_filter1(
                    comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc_1
                )
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(m2)
                acc_mut = acc_2
                continue

            else:
                return MapTreeModule_filter1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc)

        else:
            return acc

        break


def MapTreeModule_filter[KEY, _A](
    comparer: IComparer_1[KEY], f: Callable[[KEY, _A], bool], m: MapTreeLeaf_2[KEY, _A] | None = None
) -> MapTreeLeaf_2[KEY, _A] | None:
    return MapTreeModule_filterAux(comparer, f, m, MapTreeModule_empty())


def MapTreeModule_spliceOutSuccessor[KEY, VALUE](
    m: MapTreeLeaf_2[KEY, VALUE] | None = None,
) -> tuple[KEY, VALUE, MapTreeLeaf_2[KEY, VALUE] | None]:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            if MapTreeNode_2__get_Left(m2) is None:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2))

            else:
                pattern_input: tuple[KEY, VALUE, MapTreeLeaf_2[KEY, VALUE] | None] = MapTreeModule_spliceOutSuccessor(
                    MapTreeNode_2__get_Left(m2)
                )
                return (
                    pattern_input[int32_1(0)],
                    pattern_input[int32_1(1)],
                    MapTreeModule_mk(
                        pattern_input[int32_1(2)],
                        MapTreeLeaf_2__get_Key(m2),
                        MapTreeLeaf_2__get_Value(m2),
                        MapTreeNode_2__get_Right(m2),
                    ),
                )

        else:
            return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeModule_empty())

    else:
        raise Exception("internal error: Map.spliceOutSuccessor")


def MapTreeModule_remove[KEY, VALUE](
    comparer: IComparer_1[KEY], k: KEY, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            if c < int32.ZERO:
                return MapTreeModule_rebalance(
                    MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Left(m2)),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeNode_2__get_Right(m2),
                )

            elif c == int32.ZERO:
                if MapTreeNode_2__get_Left(m2) is None:
                    return MapTreeNode_2__get_Right(m2)

                elif MapTreeNode_2__get_Right(m2) is None:
                    return MapTreeNode_2__get_Left(m2)

                else:
                    pattern_input: tuple[KEY, VALUE, MapTreeLeaf_2[KEY, VALUE] | None] = (
                        MapTreeModule_spliceOutSuccessor(MapTreeNode_2__get_Right(m2))
                    )
                    return MapTreeModule_mk(
                        MapTreeNode_2__get_Left(m2),
                        pattern_input[int32_1(0)],
                        pattern_input[int32_1(1)],
                        pattern_input[int32_1(2)],
                    )

            else:
                return MapTreeModule_rebalance(
                    MapTreeNode_2__get_Left(m2),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Right(m2)),
                )

        elif c == int32.ZERO:
            return MapTreeModule_empty()

        else:
            return m

    else:
        return MapTreeModule_empty()


def MapTreeModule_change[KEY, VALUE](
    comparer: IComparer_1[KEY],
    k: KEY,
    u: Callable[[VALUE | None], VALUE | None],
    m: MapTreeLeaf_2[KEY, VALUE] | None = None,
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if c < int32.ZERO:
                return MapTreeModule_rebalance(
                    MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Left(m2)),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeNode_2__get_Right(m2),
                )

            elif c == int32.ZERO:
                match_value_1: VALUE | None = u(some(MapTreeLeaf_2__get_Value(m2)))
                if match_value_1 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(
                        k,
                        value_1(match_value_1),
                        MapTreeNode_2__get_Left(m2),
                        MapTreeNode_2__get_Right(m2),
                        MapTreeNode_2__get_Height(m2),
                    )

                elif MapTreeNode_2__get_Left(m2) is None:
                    return MapTreeNode_2__get_Right(m2)

                elif MapTreeNode_2__get_Right(m2) is None:
                    return MapTreeNode_2__get_Left(m2)

                else:
                    pattern_input: tuple[KEY, VALUE, MapTreeLeaf_2[KEY, VALUE] | None] = (
                        MapTreeModule_spliceOutSuccessor(MapTreeNode_2__get_Right(m2))
                    )
                    return MapTreeModule_mk(
                        MapTreeNode_2__get_Left(m2),
                        pattern_input[int32_1(0)],
                        pattern_input[int32_1(1)],
                        pattern_input[int32_1(2)],
                    )

            else:
                return MapTreeModule_rebalance(
                    MapTreeNode_2__get_Left(m2),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                    MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Right(m2)),
                )

        else:
            c_1: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if c_1 < int32.ZERO:
                match_value_2: VALUE | None = u(None)
                if match_value_2 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_2), MapTreeModule_empty(), m, int32.TWO)

                else:
                    return m

            elif c_1 == int32.ZERO:
                match_value_3: VALUE | None = u(some(MapTreeLeaf_2__get_Value(m2)))
                if match_value_3 is not None:
                    return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value_3))

                else:
                    return MapTreeModule_empty()

            else:
                match_value_4: VALUE | None = u(None)
                if match_value_4 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_4), m, MapTreeModule_empty(), int32.TWO)

                else:
                    return m

    else:
        match_value: VALUE | None = u(None)
        if match_value is not None:
            return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value))

        else:
            return m


def MapTreeModule_mem[KEY, VALUE](
    comparer_mut: IComparer_1[KEY], k_mut: KEY, m_mut: MapTreeLeaf_2[KEY, Any] | None
) -> bool:
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                if c < int32.ZERO:
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Left(m2)
                    continue

                elif c == int32.ZERO:
                    return True

                else:
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue

            else:
                return c == int32.ZERO

        else:
            return False

        break


def MapTreeModule_iterOpt[KEY, VALUE](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> None:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                MapTreeModule_iterOpt(f, MapTreeNode_2__get_Left(m2))
                f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(m2)
                continue

            else:
                f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        break


def MapTreeModule_iter[_A, _B](f: Callable[[_A, _B], None], m: MapTreeLeaf_2[_A, _B] | None = None) -> None:
    MapTreeModule_iterOpt(f, m)


def MapTreeModule_tryPickOpt[KEY, VALUE, _A](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> _A | None:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                match_value: _A | None = MapTreeModule_tryPickOpt(f, MapTreeNode_2__get_Left(m2))
                if match_value is None:
                    match_value_1: _A | None = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                    if match_value_1 is None:
                        f_mut = f
                        m_mut = MapTreeNode_2__get_Right(m2)
                        continue

                    else:
                        return match_value_1

                else:
                    return match_value

            else:
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            return None

        break


def MapTreeModule_tryPick[_A, _B, _C](
    f: Callable[[_A, _B], _C | None], m: MapTreeLeaf_2[_A, _B] | None = None
) -> _C | None:
    return MapTreeModule_tryPickOpt(f, m)


def MapTreeModule_existsOpt[KEY, VALUE](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> bool:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                if (
                    True
                    if MapTreeModule_existsOpt(f, MapTreeNode_2__get_Left(m2))
                    else f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                ):
                    return True

                else:
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue

            else:
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            return False

        break


def MapTreeModule_exists[_A, _B](f: Callable[[_A, _B], bool], m: MapTreeLeaf_2[_A, _B] | None = None) -> bool:
    return MapTreeModule_existsOpt(f, m)


def MapTreeModule_forallOpt[KEY, VALUE](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> bool:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                if (
                    f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                    if MapTreeModule_forallOpt(f, MapTreeNode_2__get_Left(m2))
                    else False
                ):
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue

                else:
                    return False

            else:
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            return True

        break


def MapTreeModule_forall[_A, _B](f: Callable[[_A, _B], bool], m: MapTreeLeaf_2[_A, _B] | None = None) -> bool:
    return MapTreeModule_forallOpt(f, m)


def MapTreeModule_map[KEY, RESULT, VALUE](
    f: Callable[[VALUE], RESULT], m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, RESULT] | None:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            l2: MapTreeLeaf_2[KEY, RESULT] | None = MapTreeModule_map(f, MapTreeNode_2__get_Left(m2))
            v2: RESULT = f(MapTreeLeaf_2__get_Value(m2))
            r2: MapTreeLeaf_2[KEY, RESULT] | None = MapTreeModule_map(f, MapTreeNode_2__get_Right(m2))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(m2), v2, l2, r2, MapTreeNode_2__get_Height(m2))

        else:
            return MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Value(m2)))

    else:
        return MapTreeModule_empty()


def MapTreeModule_mapiOpt[KEY, RESULT, VALUE](
    f: Any, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, RESULT] | None:
    if m is not None:
        m2: MapTreeLeaf_2[KEY, VALUE] = m
        if isinstance(m2, MapTreeNode_2):
            m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
            l2: MapTreeLeaf_2[KEY, RESULT] | None = MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Left(m2))
            v2: RESULT = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            r2: MapTreeLeaf_2[KEY, RESULT] | None = MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Right(m2))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(m2), v2, l2, r2, MapTreeNode_2__get_Height(m2))

        else:
            return MapTreeLeaf_2__ctor_5BDDA1(
                MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            )

    else:
        return MapTreeModule_empty()


def MapTreeModule_mapi[_A, _B, _C](
    f: Callable[[_A, _B], _C], m: MapTreeLeaf_2[_A, _B] | None = None
) -> MapTreeLeaf_2[_A, _C] | None:
    return MapTreeModule_mapiOpt(f, m)


def MapTreeModule_foldBackOpt[KEY, VALUE, _A](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None, x_mut: _A) -> _A:
    while True:
        (f, m, x) = (f_mut, m_mut, x_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                x_1: _A = MapTreeModule_foldBackOpt(f, MapTreeNode_2__get_Right(m2), x)
                x_2: _A = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_1)
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(m2)
                x_mut = x_2
                continue

            else:
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x)

        else:
            return x

        break


def MapTreeModule_foldBack[_A, _B, _C](f: Callable[[_A, _B, _C], _C], m: MapTreeLeaf_2[_A, _B] | None, x: _C) -> _C:
    return MapTreeModule_foldBackOpt(f, m, x)


def MapTreeModule_foldOpt[KEY, VALUE, _A](f_mut: Any, x_mut: _A, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> _A:
    while True:
        (f, x, m) = (f_mut, x_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                f_mut = f
                x_mut = f(
                    MapTreeModule_foldOpt(f, x, MapTreeNode_2__get_Left(m2)),
                    MapTreeLeaf_2__get_Key(m2),
                    MapTreeLeaf_2__get_Value(m2),
                )
                m_mut = MapTreeNode_2__get_Right(m2)
                continue

            else:
                return f(x, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            return x

        break


def MapTreeModule_fold[_A, _B, _C](f: Callable[[_A, _B, _C], _A], x: _A, m: MapTreeLeaf_2[_B, _C] | None = None) -> _A:
    return MapTreeModule_foldOpt(f, x, m)


def MapTreeModule_foldSectionOpt[A, KEY, VALUE](
    comparer: IComparer_1[KEY], lo: KEY, hi: KEY, f: Any, m: MapTreeLeaf_2[KEY, VALUE] | None, x: A
) -> A:
    def fold_from_to(
        f_1_mut: Any,
        m_1_mut: MapTreeLeaf_2[KEY, VALUE] | None,
        x_1_mut: A,
        comparer: Any = comparer,
        lo: Any = lo,
        hi: Any = hi,
        f: Any = f,
        m: Any = m,
        x: Any = x,
    ) -> A:
        while True:
            (f_1, m_1, x_1) = (f_1_mut, m_1_mut, x_1_mut)
            if m_1 is not None:
                m2: MapTreeLeaf_2[KEY, VALUE] = m_1
                if isinstance(m2, MapTreeNode_2):
                    m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                    c_lo_key: int32 = comparer.Compare(lo, MapTreeLeaf_2__get_Key(m2))
                    c_key_hi: int32 = comparer.Compare(MapTreeLeaf_2__get_Key(m2), hi)
                    x_2: A = fold_from_to(f_1, MapTreeNode_2__get_Left(m2), x_1) if (c_lo_key < int32.ZERO) else x_1
                    x_3: A = (
                        f_1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_2)
                        if ((c_key_hi <= int32.ZERO) if (c_lo_key <= int32.ZERO) else False)
                        else x_2
                    )
                    if c_key_hi < int32.ZERO:
                        f_1_mut = f_1
                        m_1_mut = MapTreeNode_2__get_Right(m2)
                        x_1_mut = x_3
                        continue

                    else:
                        return x_3

                elif (
                    (comparer.Compare(MapTreeLeaf_2__get_Key(m2), hi) <= int32.ZERO)
                    if (comparer.Compare(lo, MapTreeLeaf_2__get_Key(m2)) <= int32.ZERO)
                    else False
                ):
                    return f_1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_1)

                else:
                    return x_1

            else:
                return x_1

            break

    if comparer.Compare(lo, hi) == int32.ONE:
        return x

    else:
        return fold_from_to(f, m, x)


def MapTreeModule_foldSection[_A, _B, _C](
    comparer: IComparer_1[_A], lo: _A, hi: _A, f: Callable[[_A, _B, _C], _C], m: MapTreeLeaf_2[_A, _B] | None, x: _C
) -> _C:
    return MapTreeModule_foldSectionOpt(comparer, lo, hi, f, m, x)


def MapTreeModule_toList[KEY, VALUE](m: MapTreeLeaf_2[KEY, VALUE] | None = None) -> FSharpList[tuple[KEY, VALUE]]:
    def loop(
        m_1_mut: MapTreeLeaf_2[KEY, VALUE] | None, acc_mut: FSharpList[tuple[KEY, VALUE]], m: Any = m
    ) -> FSharpList[tuple[KEY, VALUE]]:
        while True:
            (m_1, acc) = (m_1_mut, acc_mut)
            if m_1 is not None:
                m2: MapTreeLeaf_2[KEY, VALUE] = m_1
                if isinstance(m2, MapTreeNode_2):
                    m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                    m_1_mut = MapTreeNode_2__get_Left(m2)
                    acc_mut = cons(
                        (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)),
                        loop(MapTreeNode_2__get_Right(m2), acc),
                    )
                    continue

                else:
                    return cons((MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)), acc)

            else:
                return acc

            break

    return loop(m, empty_1())


def MapTreeModule_copyToArray[_A, _B](m: MapTreeLeaf_2[_A, _B] | None, arr: Array[Any], i: int32) -> None:
    j: int32 = i

    def _arrow248(x: _A, y: _B, m: Any = m, arr: Any = arr, i: Any = i) -> None:
        nonlocal j
        arr[j] = (x, y)
        j = j + int32.ONE

    MapTreeModule_iter(_arrow248, m)


def MapTreeModule_toArray[_A, _B](m: MapTreeLeaf_2[_A, _B] | None = None) -> Array[Any]:
    res: Array[Any] = create(MapTreeModule_size(m), (None, None))
    MapTreeModule_copyToArray(m, res, int32.ZERO)
    return res


def MapTreeModule_ofList[_A, _B](
    comparer: IComparer_1[_A], l: FSharpList[tuple[_A, _B]]
) -> MapTreeLeaf_2[_A, _B] | None:
    def _arrow249(
        acc: MapTreeLeaf_2[_A, _B] | None, tupled_arg: tuple[_A, _B], comparer: Any = comparer, l: Any = l
    ) -> MapTreeLeaf_2[_A, _B] | None:
        return MapTreeModule_add(comparer, tupled_arg[int32_1(0)], tupled_arg[int32_1(1)], acc)

    return fold_1(_arrow249, MapTreeModule_empty(), l)


def MapTreeModule_mkFromEnumerator[_A, _B](
    comparer_mut: IComparer_1[_A], acc_mut: MapTreeLeaf_2[_A, _B] | None, e_mut: IEnumerator[tuple[_A, _B]]
) -> MapTreeLeaf_2[_A, _B] | None:
    while True:
        (comparer, acc, e) = (comparer_mut, acc_mut, e_mut)
        if e.System_Collections_IEnumerator_MoveNext():
            pattern_input: tuple[_A, _B] = e.System_Collections_Generic_IEnumerator_1_get_Current()
            comparer_mut = comparer
            acc_mut = MapTreeModule_add(comparer, pattern_input[int32_1(0)], pattern_input[int32_1(1)], acc)
            e_mut = e
            continue

        else:
            return acc

        break


def MapTreeModule_ofArray[KEY, VALUE](
    comparer: IComparer_1[KEY], arr: Array[tuple[KEY, VALUE]]
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    res: MapTreeLeaf_2[KEY, VALUE] | None = MapTreeModule_empty()
    for idx in range(int32.ZERO, len(arr) - int32.ONE, 1):
        for_loop_var: tuple[KEY, VALUE] = arr[idx]
        res = MapTreeModule_add(comparer, for_loop_var[int32_1(0)], for_loop_var[int32_1(1)], res)
    return res


def MapTreeModule_ofSeq[KEY, VALUE](
    comparer: IComparer_1[KEY], c: IEnumerable_1[tuple[KEY, VALUE]]
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if is_array_like(c):
        c = cast(Array[tuple[KEY, VALUE]], c)
        return MapTreeModule_ofArray(comparer, c)

    elif isinstance(c, FSharpList):
        c = cast(FSharpList[tuple[KEY, VALUE]], c)
        return MapTreeModule_ofList(comparer, c)

    else:
        with get_enumerator(c) as ie:
            return MapTreeModule_mkFromEnumerator(comparer, MapTreeModule_empty(), ie)


def _expr250(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return record_type(
        "Map.MapTreeModule.MapIterator`2",
        [gen0, gen1],
        MapTreeModule_MapIterator_2,
        lambda: [("stack_", list_type(option_type(MapTreeLeaf_2_reflection(gen0, gen1)))), ("started_", bool_type)],
    )


@dataclass(eq=False, repr=False, slots=True)
class MapTreeModule_MapIterator_2[KEY, VALUE](Record):
    stack_: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None]
    started_: bool

    def __hash__(self) -> int:
        return int(self.GetHashCode())


MapTreeModule_MapIterator_2_reflection = _expr250


def MapTreeModule_collapseLHS[KEY, VALUE](
    stack_mut: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None],
) -> FSharpList[MapTreeLeaf_2[KEY, VALUE] | None]:
    while True:
        (stack,) = (stack_mut,)
        if not is_empty_1(stack):
            rest: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None] = tail(stack)
            m: MapTreeLeaf_2[KEY, VALUE] | None = head(stack)
            if m is not None:
                m2: MapTreeLeaf_2[KEY, VALUE] = m
                if isinstance(m2, MapTreeNode_2):
                    m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                    stack_mut = of_array_with_tail(
                        Array[Any](
                            [
                                MapTreeNode_2__get_Left(m2),
                                MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)),
                                MapTreeNode_2__get_Right(m2),
                            ]
                        ),
                        rest,
                    )
                    continue

                else:
                    return stack

            else:
                stack_mut = rest
                continue

        else:
            return empty_1()

        break


def MapTreeModule_mkIterator[_A, _B](m: MapTreeLeaf_2[_A, _B] | None = None) -> MapTreeModule_MapIterator_2[_A, _B]:
    return MapTreeModule_MapIterator_2(MapTreeModule_collapseLHS(singleton(m)), False)


def MapTreeModule_notStarted[_A](__unit: None = None) -> Any:
    raise Exception("enumeration not started")


def MapTreeModule_alreadyFinished[_A](__unit: None = None) -> Any:
    raise Exception("enumeration already finished")


def MapTreeModule_current[KEY, VALUE](i: MapTreeModule_MapIterator_2[KEY, VALUE]) -> Any:
    if i.started_:
        match_value: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None] = i.stack_
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m: MapTreeLeaf_2[KEY, VALUE] = head(match_value)
                if isinstance(m, MapTreeNode_2):
                    m = cast(MapTreeNode_2[KEY, VALUE], m)
                    raise Exception("Please report error: Map iterator, unexpected stack for current")

                else:
                    return (MapTreeLeaf_2__get_Key(m), MapTreeLeaf_2__get_Value(m))

            else:
                raise Exception("Please report error: Map iterator, unexpected stack for current")

        else:
            return MapTreeModule_alreadyFinished()

    else:
        return MapTreeModule_notStarted()


def MapTreeModule_moveNext[KEY, VALUE](i: MapTreeModule_MapIterator_2[Any, Any]) -> bool:
    if i.started_:
        match_value: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None] = i.stack_
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m: MapTreeLeaf_2[KEY, VALUE] = head(match_value)
                if isinstance(m, MapTreeNode_2):
                    m = cast(MapTreeNode_2[KEY, VALUE], m)
                    raise Exception("Please report error: Map iterator, unexpected stack for moveNext")

                else:
                    i.stack_ = MapTreeModule_collapseLHS(tail(match_value))
                    return not is_empty_1(i.stack_)

            else:
                raise Exception("Please report error: Map iterator, unexpected stack for moveNext")

        else:
            return False

    else:
        i.started_ = True
        return not is_empty_1(i.stack_)


def MapTreeModule_mkIEnumerator[A, B](m: MapTreeLeaf_2[A, B] | None = None) -> IEnumerator[Any]:
    i: MapTreeModule_MapIterator_2[A, B] = MapTreeModule_mkIterator(m)

    class ObjectExpr251(IEnumerator[Any]):
        def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: None = None, m: Any = m) -> Any:
            return MapTreeModule_current(i)

        def System_Collections_IEnumerator_get_Current(self, __unit: None = None, m: Any = m) -> Any:
            return MapTreeModule_current(i)

        def System_Collections_IEnumerator_MoveNext(self, __unit: None = None, m: Any = m) -> bool:
            return MapTreeModule_moveNext(i)

        def System_Collections_IEnumerator_Reset(self, __unit: None = None, m: Any = m) -> None:
            nonlocal i
            i = MapTreeModule_mkIterator(m)

        def Dispose(self, __unit: None = None, m: Any = m) -> None:
            pass

    return ObjectExpr251()


def MapTreeModule_toSeq[_A, _B](s: MapTreeLeaf_2[_A, _B] | None = None) -> IEnumerable_1[Any]:
    def generator(en_1: IEnumerator[Any], s: Any = s) -> tuple[Any, IEnumerator[Any]] | None:
        if en_1.System_Collections_IEnumerator_MoveNext():
            return (en_1.System_Collections_Generic_IEnumerator_1_get_Current(), en_1)

        else:
            return None

    return unfold(generator, MapTreeModule_mkIEnumerator(s))


def MapTreeModule_leftmost[KEY, VALUE](m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> tuple[KEY, VALUE]:
    while True:
        (m,) = (m_mut,)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            (pattern_matching_result, nd_1) = (None, None)
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                if MapTreeNode_2__get_Height(m2) > int32.ONE:
                    pattern_matching_result = int32_1(0)
                    nd_1 = m2

                else:
                    pattern_matching_result = int32_1(1)

            else:
                pattern_matching_result = int32_1(1)

            if pattern_matching_result == int32.ZERO:
                if MapTreeNode_2__get_Left(nd_1) is None:
                    return (MapTreeLeaf_2__get_Key(nd_1), MapTreeLeaf_2__get_Value(nd_1))

                else:
                    m_mut = MapTreeNode_2__get_Left(nd_1)
                    continue

            elif pattern_matching_result == int32.ONE:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            raise Exception()

        break


def MapTreeModule_rightmost[KEY, VALUE](m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> tuple[KEY, VALUE]:
    while True:
        (m,) = (m_mut,)
        if m is not None:
            m2: MapTreeLeaf_2[KEY, VALUE] = m
            (pattern_matching_result, nd_1) = (None, None)
            if isinstance(m2, MapTreeNode_2):
                m2 = cast(MapTreeNode_2[KEY, VALUE], m2)
                if MapTreeNode_2__get_Height(m2) > int32.ONE:
                    pattern_matching_result = int32_1(0)
                    nd_1 = m2

                else:
                    pattern_matching_result = int32_1(1)

            else:
                pattern_matching_result = int32_1(1)

            if pattern_matching_result == int32.ZERO:
                if MapTreeNode_2__get_Right(nd_1) is None:
                    return (MapTreeLeaf_2__get_Key(nd_1), MapTreeLeaf_2__get_Value(nd_1))

                else:
                    m_mut = MapTreeNode_2__get_Right(nd_1)
                    continue

            elif pattern_matching_result == int32.ONE:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            raise Exception()

        break


def _expr254(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.FSharpMap", [gen0, gen1], FSharpMap)


class FSharpMap[KEY, VALUE]:
    def __init__(self, comparer: IComparer_1[KEY], tree: MapTreeLeaf_2[KEY, Any] | None = None) -> None:
        self.comparer: IComparer_1[KEY] = comparer
        self.tree: MapTreeLeaf_2[KEY, VALUE] | None = tree

    def GetHashCode(self, __unit: None = None) -> int32:
        this: FSharpMap[KEY, VALUE] = self
        return FSharpMap__ComputeHashCode(this)

    def __eq__(self, other: Any = None) -> bool:
        this: FSharpMap[KEY, VALUE] = self
        if isinstance(other, FSharpMap):
            other = cast(FSharpMap[KEY, VALUE], other)
            with get_enumerator(this) as e1:
                with get_enumerator(other) as e2:

                    def loop(__unit: None = None) -> bool:
                        m1: bool = e1.System_Collections_IEnumerator_MoveNext()
                        if m1 == e2.System_Collections_IEnumerator_MoveNext():
                            if not m1:
                                return True

                            else:
                                e1c: Any = e1.System_Collections_Generic_IEnumerator_1_get_Current()
                                e2c: Any = e2.System_Collections_Generic_IEnumerator_1_get_Current()
                                if (
                                    equals(e1c[int32_1(1)], e2c[int32_1(1)])
                                    if equals(e1c[int32_1(0)], e2c[int32_1(0)])
                                    else False
                                ):
                                    return loop()

                                else:
                                    return False

                        else:
                            return False

                    return loop()

        else:
            return False

    def __str__(self, __unit: None = None) -> str:
        this: FSharpMap[KEY, VALUE] = self

        def _arrow252(kv: Any) -> str:
            return format("({0}, {1})", kv[int32_1(0)], kv[int32_1(1)])

        return ("map [" + join("; ", map_1(_arrow252, this))) + "]"

    @property
    def Symbol_toStringTag(self, __unit: None = None) -> str:
        return "FSharpMap"

    def to_json(self, __unit: None = None) -> Any:
        this: FSharpMap[KEY, VALUE] = self
        return Array.from_(this)

    def GetEnumerator[KEY, VALUE](self, __unit: None = None) -> IEnumerator[Any]:
        _: FSharpMap[KEY, VALUE] = self
        return MapTreeModule_mkIEnumerator(_.tree)

    def __iter__[KEY, VALUE](self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        _: FSharpMap[KEY, VALUE] = self
        return MapTreeModule_mkIEnumerator(_.tree)

    def __cmp__(self, other: Any = None) -> int32:
        this: FSharpMap[KEY, VALUE] = self

        def _arrow253(kvp1: Any, kvp2: Any) -> int32:
            c: int32 = this.comparer.Compare(kvp1[int32_1(0)], kvp2[int32_1(0)])
            return c if (c != int32.ZERO) else compare(kvp1[int32_1(1)], kvp2[int32_1(1)])

        return compare_with(_arrow253, this, other) if isinstance(other, FSharpMap) else int32.ONE

    def System_Collections_Generic_ICollection_1_Add2B595(self, x: Any) -> None:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: None = None) -> None:
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Remove2B595(self, x: Any) -> bool:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Contains2B595(self, x: Any) -> bool:
        m: FSharpMap[KEY, VALUE] = self
        return (
            equals(FSharpMap__get_Item(m, x[int32_1(0)]), x[int32_1(1)])
            if FSharpMap__ContainsKey(m, x[int32_1(0)])
            else False
        )

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, arr: Array[Any], i: int32) -> None:
        m: FSharpMap[KEY, VALUE] = self
        MapTreeModule_copyToArray(m.tree, arr, i)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: None = None) -> bool:
        return True

    def __len__(self, __unit: None = None) -> int32:
        m: FSharpMap[KEY, VALUE] = self
        return FSharpMap__get_Count(m)

    def __len__(self, __unit: None = None) -> int32:
        m: FSharpMap[KEY, VALUE] = self
        return FSharpMap__get_Count(m)

    @property
    def size(self, __unit: None = None) -> int32:
        m: FSharpMap[KEY, VALUE] = self
        return FSharpMap__get_Count(m)

    def clear(self, __unit: None = None) -> None:
        raise Exception("Map cannot be mutated")

    def __delitem__(self, _arg: KEY | None = None) -> bool:
        raise Exception("Map cannot be mutated")
        return False

    def entries[KEY, VALUE](self, __unit: None = None) -> IEnumerable_1[tuple[KEY, VALUE]]:
        m: FSharpMap[KEY, VALUE] = self

        def mapping(p: Any) -> tuple[KEY, VALUE]:
            return (p[int32_1(0)], p[int32_1(1)])

        return map_1(mapping, m)

    def __getitem__[VALUE](self, k: KEY | None = None) -> VALUE:
        m: FSharpMap[KEY, VALUE] = self
        return FSharpMap__get_Item(m, k)

    def __contains__(self, k: KEY | None = None) -> bool:
        m: FSharpMap[KEY, VALUE] = self
        return FSharpMap__ContainsKey(m, k)

    def keys[KEY](self, __unit: None = None) -> IEnumerable_1[KEY]:
        m: FSharpMap[KEY, VALUE] = self

        def mapping(p: Any) -> KEY:
            return p[int32_1(0)]

        return map_1(mapping, m)

    def __setitem__[KEY, VALUE](self, k: KEY, v: VALUE) -> Map_2[KEY, VALUE]:
        m: FSharpMap[KEY, VALUE] = self
        raise Exception("Map cannot be mutated")
        return m

    def values[VALUE](self, __unit: None = None) -> IEnumerable_1[VALUE]:
        m: FSharpMap[KEY, VALUE] = self

        def mapping(p: Any) -> VALUE:
            return p[int32_1(1)]

        return map_1(mapping, m)

    def for_each(self, f: Callable[[VALUE, KEY, Map_2[KEY, VALUE]], None], this_arg: Any | None = None) -> None:
        m: FSharpMap[KEY, VALUE] = self

        def action(p: Any) -> None:
            f(p[int32_1(1)], p[int32_1(0)], m)

        iterate_1(action, m)


FSharpMap_reflection = _expr254


def FSharpMap__ctor(comparer: IComparer_1[KEY], tree: MapTreeLeaf_2[KEY, Any] | None = None) -> FSharpMap[KEY, VALUE]:
    return FSharpMap(comparer, tree)


def FSharpMap_Empty[KEY, VALUE](comparer: IComparer_1[KEY]) -> FSharpMap[KEY, Any]:
    return FSharpMap__ctor(comparer, MapTreeModule_empty())


def FSharpMap__get_Comparer[KEY](m: FSharpMap[KEY, Any]) -> IComparer_1[KEY]:
    return m.comparer


def FSharpMap__get_Tree[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return m.tree


def FSharpMap__Add[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY, value: VALUE) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_add(m.comparer, key, value, m.tree))


def FSharpMap__Change[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], key: KEY, f: Callable[[VALUE | None], VALUE | None]
) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_change(m.comparer, key, f, m.tree))


def FSharpMap__get_IsEmpty(m: FSharpMap[Any, Any]) -> bool:
    return m.tree is None


def FSharpMap__get_Item[VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> VALUE:
    return MapTreeModule_find(m.comparer, key, m.tree)


def FSharpMap__TryPick[_A](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], _A | None]) -> _A | None:
    return MapTreeModule_tryPick(f, m.tree)


def FSharpMap__Exists(m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]) -> bool:
    return MapTreeModule_exists(predicate, m.tree)


def FSharpMap__Filter[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]
) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_filter(m.comparer, predicate, m.tree))


def FSharpMap__ForAll(m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]) -> bool:
    return MapTreeModule_forall(predicate, m.tree)


def FSharpMap__Fold[_A](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE, _A], _A], acc: _A) -> _A:
    return MapTreeModule_foldBack(f, m.tree, acc)


def FSharpMap__FoldSection[_A](
    m: FSharpMap[KEY, VALUE], lo: KEY, hi: KEY, f: Callable[[KEY, VALUE, _A], _A], acc: _A
) -> _A:
    return MapTreeModule_foldSection(m.comparer, lo, hi, f, m.tree, acc)


def FSharpMap__Iterate(m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], None]) -> None:
    MapTreeModule_iter(f, m.tree)


def FSharpMap__MapRange[KEY, RESULT](m: FSharpMap[KEY, VALUE], f: Callable[[VALUE], RESULT]) -> FSharpMap[KEY, RESULT]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_map(f, m.tree))


def FSharpMap__Map[B, KEY](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], B]) -> FSharpMap[KEY, B]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_mapi(f, m.tree))


def FSharpMap__Partition[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]
) -> tuple[FSharpMap[KEY, VALUE], FSharpMap[KEY, VALUE]]:
    pattern_input: tuple[MapTreeLeaf_2[KEY, VALUE] | None, MapTreeLeaf_2[KEY, VALUE] | None] = MapTreeModule_partition(
        m.comparer, predicate, m.tree
    )
    return (
        FSharpMap__ctor(m.comparer, pattern_input[int32_1(0)]),
        FSharpMap__ctor(m.comparer, pattern_input[int32_1(1)]),
    )


def FSharpMap__get_Count(m: FSharpMap[Any, Any]) -> int32:
    return MapTreeModule_size(m.tree)


def FSharpMap__ContainsKey(m: FSharpMap[KEY, Any], key: KEY) -> bool:
    return MapTreeModule_mem(m.comparer, key, m.tree)


def FSharpMap__Remove[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_remove(m.comparer, key, m.tree))


def FSharpMap__TryGetValue(_: FSharpMap[KEY, VALUE], key: KEY, value: FSharpRef[VALUE]) -> bool:
    match_value: VALUE | None = MapTreeModule_tryFind(_.comparer, key, _.tree)
    if match_value is None:
        return False

    else:
        v: VALUE = value_1(match_value)
        value.contents = v
        return True


def FSharpMap__get_Keys[KEY](_: FSharpMap[KEY, Any]) -> ICollection[KEY]:
    def mapping(kvp: Any, _: Any = _) -> KEY:
        return kvp[int32_1(0)]

    return map_2(mapping, MapTreeModule_toArray(_.tree), None)


def FSharpMap__get_Values[VALUE](_: FSharpMap[Any, VALUE]) -> ICollection[VALUE]:
    def mapping(kvp: Any, _: Any = _) -> VALUE:
        return kvp[int32_1(1)]

    return map_2(mapping, MapTreeModule_toArray(_.tree), None)


def FSharpMap__get_MinKeyValue[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> tuple[KEY, VALUE]:
    return MapTreeModule_leftmost(m.tree)


def FSharpMap__get_MaxKeyValue[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> tuple[KEY, VALUE]:
    return MapTreeModule_rightmost(m.tree)


def FSharpMap__TryFind[VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> VALUE | None:
    return MapTreeModule_tryFind(m.comparer, key, m.tree)


def FSharpMap__ToList[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> FSharpList[tuple[KEY, VALUE]]:
    return MapTreeModule_toList(m.tree)


def FSharpMap__ToArray[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> Array[Any]:
    return MapTreeModule_toArray(m.tree)


def FSharpMap__ComputeHashCode(this: FSharpMap[Any, Any]) -> int32:
    def combine_hash(x: int32, y: int32, this: Any = this) -> int32:
        return ((x << int32.ONE) + y) + int32(631)

    res: int32 = int32.ZERO
    with get_enumerator(this) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            active_pattern_result: tuple[KEY, VALUE] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            res = combine_hash(res, structural_hash(active_pattern_result[int32_1(0)]))
            res = combine_hash(res, structural_hash(active_pattern_result[int32_1(1)]))
    return res


def is_empty[_A, _B](table: FSharpMap[Any, Any]) -> bool:
    return FSharpMap__get_IsEmpty(table)


def add[_A, _B](key: _A, value: _B, table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Add(table, key, value)


def change[_A, _B](key: _A, f: Callable[[_B | None], _B | None], table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Change(table, key, f)


def find[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> _B:
    return FSharpMap__get_Item(table, key)


def try_find[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> _B | None:
    return FSharpMap__TryFind(table, key)


def remove[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Remove(table, key)


def contains_key[_A, _B](key: _A, table: FSharpMap[_A, Any]) -> bool:
    return FSharpMap__ContainsKey(table, key)


def iterate[_A, _B](action: Callable[[_A, _B], None], table: FSharpMap[_A, _B]) -> None:
    FSharpMap__Iterate(table, action)


def try_pick[_A, _B, _C](chooser: Callable[[_A, _B], _C | None], table: FSharpMap[_A, _B]) -> _C | None:
    return FSharpMap__TryPick(table, chooser)


def pick[_A, _B, _C](chooser: Callable[[_A, _B], _C | None], table: FSharpMap[_A, _B]) -> _C:
    match_value: _C | None = try_pick(chooser, table)
    if match_value is not None:
        return value_1(match_value)

    else:
        raise Exception()


def exists[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> bool:
    return FSharpMap__Exists(table, predicate)


def filter[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Filter(table, predicate)


def partition[_A, _B](
    predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]
) -> tuple[FSharpMap[_A, _B], FSharpMap[_A, _B]]:
    return FSharpMap__Partition(table, predicate)


def for_all[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> bool:
    return FSharpMap__ForAll(table, predicate)


def map[_A, _B, _C](mapping: Callable[[_A, _B], _C], table: FSharpMap[_A, _B]) -> FSharpMap[_A, _C]:
    return FSharpMap__Map(table, mapping)


def fold[KEY, STATE, T](folder: Callable[[STATE, KEY, T], STATE], state: STATE, table: FSharpMap[KEY, T]) -> STATE:
    return MapTreeModule_fold(folder, state, FSharpMap__get_Tree(table))


def fold_back[KEY, STATE, T](folder: Callable[[KEY, T, STATE], STATE], table: FSharpMap[KEY, T], state: STATE) -> STATE:
    return MapTreeModule_foldBack(folder, FSharpMap__get_Tree(table), state)


def to_seq[_A, _B](table: FSharpMap[_A, _B]) -> IEnumerable_1[tuple[_A, _B]]:
    def mapping(kvp: Any, table: Any = table) -> tuple[_A, _B]:
        return (kvp[int32_1(0)], kvp[int32_1(1)])

    return map_1(mapping, table)


def find_key[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> _A:
    def chooser(kvp: Any, predicate: Any = predicate, table: Any = table) -> _A | None:
        k: _A = kvp[int32_1(0)]
        if predicate(k, kvp[int32_1(1)]):
            return some(k)

        else:
            return None

    return pick_1(chooser, table)


def try_find_key[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> _A | None:
    def chooser(kvp: Any, predicate: Any = predicate, table: Any = table) -> _A | None:
        k: _A = kvp[int32_1(0)]
        if predicate(k, kvp[int32_1(1)]):
            return some(k)

        else:
            return None

    return try_pick_1(chooser, table)


def of_list[KEY, VALUE](elements: FSharpList[tuple[KEY, VALUE]], comparer: IComparer_1[KEY]) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def of_seq[T, _A](elements: IEnumerable_1[tuple[T, _A]], comparer: IComparer_1[T]) -> FSharpMap[T, _A]:
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def of_array[KEY, VALUE](elements: Array[tuple[KEY, VALUE]], comparer: IComparer_1[KEY]) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def to_list[_A, _B](table: FSharpMap[_A, _B]) -> FSharpList[tuple[_A, _B]]:
    return FSharpMap__ToList(table)


def to_array[_A, _B](table: FSharpMap[_A, _B]) -> Array[Any]:
    return FSharpMap__ToArray(table)


def keys[K, V](table: FSharpMap[K, Any]) -> ICollection[K]:
    return FSharpMap__get_Keys(table)


def values[K, V](table: FSharpMap[Any, V]) -> ICollection[V]:
    return FSharpMap__get_Values(table)


def min_key_value[_A, _B](table: FSharpMap[_A, _B]) -> tuple[_A, _B]:
    return FSharpMap__get_MinKeyValue(table)


def max_key_value[_A, _B](table: FSharpMap[_A, _B]) -> tuple[_A, _B]:
    return FSharpMap__get_MaxKeyValue(table)


def empty[KEY, VALUE](comparer: IComparer_1[KEY]) -> FSharpMap[KEY, Any]:
    return FSharpMap_Empty(comparer)


def count[_A, _B](table: FSharpMap[Any, Any]) -> int32:
    return FSharpMap__get_Count(table)


__all__ = [
    "MapTreeLeaf_2_reflection",
    "MapTreeLeaf_2__get_Key",
    "MapTreeLeaf_2__get_Value",
    "MapTreeNode_2_reflection",
    "MapTreeNode_2__get_Left",
    "MapTreeNode_2__get_Right",
    "MapTreeNode_2__get_Height",
    "MapTreeModule_empty",
    "MapTreeModule_sizeAux",
    "MapTreeModule_size",
    "MapTreeModule_mk",
    "MapTreeModule_rebalance",
    "MapTreeModule_add",
    "MapTreeModule_tryFind",
    "MapTreeModule_find",
    "MapTreeModule_partition1",
    "MapTreeModule_partitionAux",
    "MapTreeModule_partition",
    "MapTreeModule_filter1",
    "MapTreeModule_filterAux",
    "MapTreeModule_filter",
    "MapTreeModule_spliceOutSuccessor",
    "MapTreeModule_remove",
    "MapTreeModule_change",
    "MapTreeModule_mem",
    "MapTreeModule_iterOpt",
    "MapTreeModule_iter",
    "MapTreeModule_tryPickOpt",
    "MapTreeModule_tryPick",
    "MapTreeModule_existsOpt",
    "MapTreeModule_exists",
    "MapTreeModule_forallOpt",
    "MapTreeModule_forall",
    "MapTreeModule_map",
    "MapTreeModule_mapiOpt",
    "MapTreeModule_mapi",
    "MapTreeModule_foldBackOpt",
    "MapTreeModule_foldBack",
    "MapTreeModule_foldOpt",
    "MapTreeModule_fold",
    "MapTreeModule_foldSectionOpt",
    "MapTreeModule_foldSection",
    "MapTreeModule_toList",
    "MapTreeModule_copyToArray",
    "MapTreeModule_toArray",
    "MapTreeModule_ofList",
    "MapTreeModule_mkFromEnumerator",
    "MapTreeModule_ofArray",
    "MapTreeModule_ofSeq",
    "MapTreeModule_MapIterator_2_reflection",
    "MapTreeModule_collapseLHS",
    "MapTreeModule_mkIterator",
    "MapTreeModule_notStarted",
    "MapTreeModule_alreadyFinished",
    "MapTreeModule_current",
    "MapTreeModule_moveNext",
    "MapTreeModule_mkIEnumerator",
    "MapTreeModule_toSeq",
    "MapTreeModule_leftmost",
    "MapTreeModule_rightmost",
    "FSharpMap_reflection",
    "FSharpMap_Empty",
    "FSharpMap__get_Comparer",
    "FSharpMap__get_Tree",
    "FSharpMap__Add",
    "FSharpMap__Change",
    "FSharpMap__get_IsEmpty",
    "FSharpMap__get_Item",
    "FSharpMap__TryPick",
    "FSharpMap__Exists",
    "FSharpMap__Filter",
    "FSharpMap__ForAll",
    "FSharpMap__Fold",
    "FSharpMap__FoldSection",
    "FSharpMap__Iterate",
    "FSharpMap__MapRange",
    "FSharpMap__Map",
    "FSharpMap__Partition",
    "FSharpMap__get_Count",
    "FSharpMap__ContainsKey",
    "FSharpMap__Remove",
    "FSharpMap__TryGetValue",
    "FSharpMap__get_Keys",
    "FSharpMap__get_Values",
    "FSharpMap__get_MinKeyValue",
    "FSharpMap__get_MaxKeyValue",
    "FSharpMap__TryFind",
    "FSharpMap__ToList",
    "FSharpMap__ToArray",
    "FSharpMap__ComputeHashCode",
    "is_empty",
    "add",
    "change",
    "find",
    "try_find",
    "remove",
    "contains_key",
    "iterate",
    "try_pick",
    "pick",
    "exists",
    "filter",
    "partition",
    "for_all",
    "map",
    "fold",
    "fold_back",
    "to_seq",
    "find_key",
    "try_find_key",
    "of_list",
    "of_seq",
    "of_array",
    "to_list",
    "to_array",
    "keys",
    "values",
    "min_key_value",
    "max_key_value",
    "empty",
    "count",
]
