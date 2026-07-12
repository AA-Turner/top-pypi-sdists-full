from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, cast

from fable_library.util import to_iterator

from .array_ import Array, zero_create
from .array_ import map as map_2
from .bases import ComparableBase, DisposableBase, EnumerableBase, EnumeratorBase, EquatableBase, StringableBase
from .core import FSharpRef, int32
from .list import FSharpList, cons, head, of_array_with_tail, singleton, tail
from .list import empty as empty_1
from .list import fold as fold_1
from .list import is_empty as is_empty_1
from .option import Option, erase, some
from .option import value as value_1
from .protocols import ICollection, IComparer_1, IEnumerable_1, IEnumerator
from .record import Record
from .reflection import TypeInfo, bool_type, class_type, list_type, option_type, record_type
from .seq import compare_with
from .seq import pick as pick_1
from .seq import try_pick as try_pick_1
from .seq_native import map as map_1
from .seq_native import unfold
from .string_ import format, join
from .system import NotSupportedException__ctor_Z721C83C5
from .types import ExceptionBase
from .util import UNIT, Disposable, Unit, compare, equals, get_enumerator, ignore, nullable, range, structural_hash


def _expr225(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.MapTreeLeaf`2", Array([gen0, gen1]), MapTreeLeaf_2)


class MapTreeLeaf_2[KEY, VALUE]:
    def __init__(self, k: KEY, v: VALUE) -> None:
        self.k: Any = k
        self.v: Any = v


MapTreeLeaf_2_reflection = _expr225


def MapTreeLeaf_2__ctor_5BDDA1[KEY, VALUE](k: KEY, v: VALUE) -> MapTreeLeaf_2[KEY, VALUE]:
    return MapTreeLeaf_2(k, v)


def MapTreeLeaf_2__get_Key[KEY, VALUE](_: MapTreeLeaf_2[KEY, VALUE]) -> KEY:
    return _.k


def MapTreeLeaf_2__get_Value[KEY, VALUE](_: MapTreeLeaf_2[KEY, VALUE]) -> VALUE:
    return _.v


def _expr226(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.MapTreeNode`2", Array([gen0, gen1]), MapTreeNode_2, MapTreeLeaf_2_reflection(gen0, gen1))


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
        self.left: MapTreeLeaf_2[Any, Any] | None = left
        self.right: MapTreeLeaf_2[Any, Any] | None = right
        self.h: int32 = h


MapTreeNode_2_reflection = _expr226


def MapTreeNode_2__ctor_Z39DE9543[KEY, VALUE](
    k: KEY, v: VALUE, left: MapTreeLeaf_2[KEY, VALUE] | None, right: MapTreeLeaf_2[KEY, VALUE] | None, h: int32
) -> MapTreeNode_2[KEY, VALUE]:
    return MapTreeNode_2(k, v, left, right, h)


def MapTreeNode_2__get_Left[KEY, VALUE](_: MapTreeNode_2[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return _.left


def MapTreeNode_2__get_Right[KEY, VALUE](_: MapTreeNode_2[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return _.right


def MapTreeNode_2__get_Height[KEY, VALUE](_: MapTreeNode_2[KEY, VALUE]) -> int32:
    return _.h


def MapTreeModule_empty[KEY, VALUE](__unit: Unit = UNIT) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return None


def MapTreeModule_sizeAux[KEY, VALUE](acc_mut: int32, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> int32:
    while True:
        (acc, m) = (acc_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                acc_mut = MapTreeModule_sizeAux(acc + int32.ONE, MapTreeNode_2__get_Left(mn))
                m_mut = MapTreeNode_2__get_Right(mn)
                continue

            else:
                return acc + int32.ONE

        else:
            return acc

        break


def MapTreeModule_size[_A, _B](x: MapTreeLeaf_2[_A, _B] | None = None) -> int32:
    return MapTreeModule_sizeAux(int32.ZERO, x)


def MapTreeModule_mk[KEY, VALUE](
    l: MapTreeLeaf_2[KEY, VALUE] | None, k: KEY, v: VALUE, r: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    hl: int32
    m: MapTreeLeaf_2[Any, Any] | None = l
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        hl = MapTreeNode_2__get_Height(m2) if isinstance(m2, MapTreeNode_2) else int32.ONE

    else:
        hl = int32.ZERO

    hr: int32
    m_1: MapTreeLeaf_2[Any, Any] | None = r
    if m_1 is not None:
        m2_1: MapTreeLeaf_2[Any, Any] = m_1
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
    m: MapTreeLeaf_2[Any, Any] | None = t1
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        t1h = MapTreeNode_2__get_Height(m2) if isinstance(m2, MapTreeNode_2) else int32.ONE

    else:
        t1h = int32.ZERO

    t2h: int32
    m_1: MapTreeLeaf_2[Any, Any] | None = t2
    if m_1 is not None:
        m2_1: MapTreeLeaf_2[Any, Any] = m_1
        t2h = MapTreeNode_2__get_Height(m2_1) if isinstance(m2_1, MapTreeNode_2) else int32.ONE

    else:
        t2h = int32.ZERO

    if t2h > (t1h + int32.TWO):
        match_value: MapTreeLeaf_2[Any, Any] = value_1(t2)
        if isinstance(match_value, MapTreeNode_2):
            t2_0027: MapTreeNode_2[Any, Any] = match_value

            def _arrow227(__unit: Unit = UNIT) -> int32:
                m_2: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeNode_2__get_Left(t2_0027))
                if m_2 is not None:
                    m2_2: MapTreeLeaf_2[Any, Any] = m_2
                    return MapTreeNode_2__get_Height(m2_2) if isinstance(m2_2, MapTreeNode_2) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow227() > (t1h + int32.ONE):
                match_value_1: MapTreeLeaf_2[Any, Any] = value_1(MapTreeNode_2__get_Left(t2_0027))
                if isinstance(match_value_1, MapTreeNode_2):
                    t2l: MapTreeNode_2[Any, Any] = match_value_1
                    return erase(
                        MapTreeModule_mk(
                            MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(t2l)),
                            MapTreeLeaf_2__get_Key(t2l),
                            MapTreeLeaf_2__get_Value(t2l),
                            MapTreeModule_mk(
                                MapTreeNode_2__get_Right(t2l),
                                MapTreeLeaf_2__get_Key(t2_0027),
                                MapTreeLeaf_2__get_Value(t2_0027),
                                MapTreeNode_2__get_Right(t2_0027),
                            ),
                        )
                    )

                else:
                    raise Exception("internal error: Map.rebalance")

            else:
                return erase(
                    MapTreeModule_mk(
                        MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(t2_0027)),
                        MapTreeLeaf_2__get_Key(t2_0027),
                        MapTreeLeaf_2__get_Value(t2_0027),
                        MapTreeNode_2__get_Right(t2_0027),
                    )
                )

        else:
            raise Exception("internal error: Map.rebalance")

    elif t1h > (t2h + int32.TWO):
        match_value_2: MapTreeLeaf_2[Any, Any] = value_1(t1)
        if isinstance(match_value_2, MapTreeNode_2):
            t1_0027: MapTreeNode_2[Any, Any] = match_value_2

            def _arrow228(__unit: Unit = UNIT) -> int32:
                m_3: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeNode_2__get_Right(t1_0027))
                if m_3 is not None:
                    m2_3: MapTreeLeaf_2[Any, Any] = m_3
                    return MapTreeNode_2__get_Height(m2_3) if isinstance(m2_3, MapTreeNode_2) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow228() > (t2h + int32.ONE):
                match_value_3: MapTreeLeaf_2[Any, Any] = value_1(MapTreeNode_2__get_Right(t1_0027))
                if isinstance(match_value_3, MapTreeNode_2):
                    t1r: MapTreeNode_2[Any, Any] = match_value_3
                    return erase(
                        MapTreeModule_mk(
                            MapTreeModule_mk(
                                MapTreeNode_2__get_Left(t1_0027),
                                MapTreeLeaf_2__get_Key(t1_0027),
                                MapTreeLeaf_2__get_Value(t1_0027),
                                MapTreeNode_2__get_Left(t1r),
                            ),
                            MapTreeLeaf_2__get_Key(t1r),
                            MapTreeLeaf_2__get_Value(t1r),
                            MapTreeModule_mk(MapTreeNode_2__get_Right(t1r), k, v, t2),
                        )
                    )

                else:
                    raise Exception("internal error: Map.rebalance")

            else:
                return erase(
                    MapTreeModule_mk(
                        MapTreeNode_2__get_Left(t1_0027),
                        MapTreeLeaf_2__get_Key(t1_0027),
                        MapTreeLeaf_2__get_Value(t1_0027),
                        MapTreeModule_mk(MapTreeNode_2__get_Right(t1_0027), k, v, t2),
                    )
                )

        else:
            raise Exception("internal error: Map.rebalance")

    else:
        return erase(MapTreeModule_mk(t1, k, v, t2))


def MapTreeModule_add[KEY, VALUE](
    comparer: IComparer_1[KEY], k: KEY, v: VALUE, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            if c < int32.ZERO:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Left(mn)),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeNode_2__get_Right(mn),
                    )
                )

            elif c == int32.ZERO:
                return MapTreeNode_2__ctor_Z39DE9543(
                    k, v, MapTreeNode_2__get_Left(mn), MapTreeNode_2__get_Right(mn), MapTreeNode_2__get_Height(mn)
                )

            else:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeNode_2__get_Left(mn),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Right(mn)),
                    )
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
) -> Option[VALUE]:
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if c == int32.ZERO:
                return some(MapTreeLeaf_2__get_Value(m2))

            elif isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                comparer_mut = comparer
                k_mut = k
                m_mut = MapTreeNode_2__get_Left(mn) if (c < int32.ZERO) else MapTreeNode_2__get_Right(mn)
                continue

            else:
                return None

        else:
            return None

        break


def MapTreeModule_find[KEY, VALUE](
    comparer: IComparer_1[KEY], k: KEY, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> VALUE:
    match_value: Option[Any] = MapTreeModule_tryFind(comparer, k, m)
    if match_value is None:
        raise ExceptionBase()

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
        acc: tuple[MapTreeLeaf_2[Any, Any] | None, MapTreeLeaf_2[Any, Any] | None] = (acc_, acc__1)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                acc_1: tuple[MapTreeLeaf_2[Any, Any] | None, MapTreeLeaf_2[Any, Any] | None] = (
                    MapTreeModule_partitionAux(comparer, f, MapTreeNode_2__get_Right(mn), acc[0], acc[1])
                )
                acc_4: tuple[MapTreeLeaf_2[Any, Any] | None, MapTreeLeaf_2[Any, Any] | None] = MapTreeModule_partition1(
                    comparer, f, MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn), acc_1[0], acc_1[1]
                )
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(mn)
                acc__mut = acc_4[0]
                acc__1_mut = acc_4[1]
                continue

            else:
                return MapTreeModule_partition1(
                    comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc[0], acc[1]
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
        return erase(MapTreeModule_add(comparer, k, v, acc))

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
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                acc_1: MapTreeLeaf_2[Any, Any] | None = erase(
                    MapTreeModule_filterAux(comparer, f, MapTreeNode_2__get_Left(mn), acc)
                )
                acc_2: MapTreeLeaf_2[Any, Any] | None = erase(
                    MapTreeModule_filter1(comparer, f, MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn), acc_1)
                )
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(mn)
                acc_mut = acc_2
                continue

            else:
                return erase(
                    MapTreeModule_filter1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc)
                )

        else:
            return acc

        break


def MapTreeModule_filter[KEY, _A](
    comparer: IComparer_1[KEY], f: Callable[[KEY, _A], bool], m: MapTreeLeaf_2[KEY, _A] | None = None
) -> MapTreeLeaf_2[KEY, _A] | None:
    return erase(MapTreeModule_filterAux(comparer, f, m, MapTreeModule_empty()))


def MapTreeModule_spliceOutSuccessor[KEY, VALUE](
    m: MapTreeLeaf_2[KEY, VALUE] | None = None,
) -> tuple[KEY, VALUE, MapTreeLeaf_2[KEY, VALUE] | None]:
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            if MapTreeNode_2__get_Left(mn) is None:
                return (MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn), MapTreeNode_2__get_Right(mn))

            else:
                pattern_input: tuple[Any, Any, MapTreeLeaf_2[Any, Any] | None] = MapTreeModule_spliceOutSuccessor(
                    MapTreeNode_2__get_Left(mn)
                )
                return (
                    pattern_input[0],
                    pattern_input[1],
                    MapTreeModule_mk(
                        pattern_input[2],
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeNode_2__get_Right(mn),
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
        m2: MapTreeLeaf_2[Any, Any] = m
        c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            if c < int32.ZERO:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Left(mn)),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeNode_2__get_Right(mn),
                    )
                )

            elif c == int32.ZERO:
                if MapTreeNode_2__get_Left(mn) is None:
                    return erase(MapTreeNode_2__get_Right(mn))

                elif MapTreeNode_2__get_Right(mn) is None:
                    return erase(MapTreeNode_2__get_Left(mn))

                else:
                    pattern_input: tuple[Any, Any, MapTreeLeaf_2[Any, Any] | None] = MapTreeModule_spliceOutSuccessor(
                        MapTreeNode_2__get_Right(mn)
                    )
                    return erase(
                        MapTreeModule_mk(
                            MapTreeNode_2__get_Left(mn), pattern_input[0], pattern_input[1], pattern_input[2]
                        )
                    )

            else:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeNode_2__get_Left(mn),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Right(mn)),
                    )
                )

        elif c == int32.ZERO:
            return erase(MapTreeModule_empty())

        else:
            return m

    else:
        return erase(MapTreeModule_empty())


def MapTreeModule_change[KEY, VALUE](
    comparer: IComparer_1[KEY],
    k: KEY,
    u: Callable[[Option[VALUE]], Option[VALUE]],
    m: MapTreeLeaf_2[KEY, VALUE] | None = None,
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(mn))
            if c < int32.ZERO:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Left(mn)),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeNode_2__get_Right(mn),
                    )
                )

            elif c == int32.ZERO:
                match_value_1: Option[Any] = u(some(MapTreeLeaf_2__get_Value(mn)))
                if match_value_1 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(
                        k,
                        value_1(match_value_1),
                        MapTreeNode_2__get_Left(mn),
                        MapTreeNode_2__get_Right(mn),
                        MapTreeNode_2__get_Height(mn),
                    )

                elif MapTreeNode_2__get_Left(mn) is None:
                    return erase(MapTreeNode_2__get_Right(mn))

                elif MapTreeNode_2__get_Right(mn) is None:
                    return erase(MapTreeNode_2__get_Left(mn))

                else:
                    pattern_input: tuple[Any, Any, MapTreeLeaf_2[Any, Any] | None] = MapTreeModule_spliceOutSuccessor(
                        MapTreeNode_2__get_Right(mn)
                    )
                    return erase(
                        MapTreeModule_mk(
                            MapTreeNode_2__get_Left(mn), pattern_input[0], pattern_input[1], pattern_input[2]
                        )
                    )

            else:
                return erase(
                    MapTreeModule_rebalance(
                        MapTreeNode_2__get_Left(mn),
                        MapTreeLeaf_2__get_Key(mn),
                        MapTreeLeaf_2__get_Value(mn),
                        MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Right(mn)),
                    )
                )

        else:
            c_1: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if c_1 < int32.ZERO:
                match_value_2: Option[Any] = u(None)
                if match_value_2 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_2), MapTreeModule_empty(), m, int32.TWO)

                else:
                    return m

            elif c_1 == int32.ZERO:
                match_value_3: Option[Any] = u(some(MapTreeLeaf_2__get_Value(m2)))
                if match_value_3 is not None:
                    return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value_3))

                else:
                    return erase(MapTreeModule_empty())

            else:
                match_value_4: Option[Any] = u(None)
                if match_value_4 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_4), m, MapTreeModule_empty(), int32.TWO)

                else:
                    return m

    else:
        match_value: Option[Any] = u(None)
        if match_value is not None:
            return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value))

        else:
            return m


def MapTreeModule_mem[KEY, VALUE](
    comparer_mut: IComparer_1[KEY], k_mut: KEY, m_mut: MapTreeLeaf_2[KEY, VALUE] | None
) -> bool:
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            c: int32 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2))
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                if c < int32.ZERO:
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Left(mn)
                    continue

                elif c == int32.ZERO:
                    return True

                else:
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Right(mn)
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
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                MapTreeModule_iterOpt(f, MapTreeNode_2__get_Left(mn))
                f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn))
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(mn)
                continue

            else:
                f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        break


def MapTreeModule_iter[_A, _B](f: Callable[[_A, _B], None], m: MapTreeLeaf_2[_A, _B] | None = None) -> None:
    MapTreeModule_iterOpt(f, m)


def MapTreeModule_tryPickOpt[KEY, VALUE, _A](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> Option[_A]:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                match_value: Option[Any] = MapTreeModule_tryPickOpt(f, MapTreeNode_2__get_Left(mn))
                if match_value is None:
                    match_value_1: Option[Any] = f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn))
                    if match_value_1 is None:
                        f_mut = f
                        m_mut = MapTreeNode_2__get_Right(mn)
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
    f: Callable[[_A, _B], Option[_C]], m: MapTreeLeaf_2[_A, _B] | None = None
) -> Option[_C]:
    return MapTreeModule_tryPickOpt(f, m)


def MapTreeModule_existsOpt[KEY, VALUE](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> bool:
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                if (
                    True
                    if MapTreeModule_existsOpt(f, MapTreeNode_2__get_Left(mn))
                    else f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn))
                ):
                    return True

                else:
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(mn)
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
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                if (
                    f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn))
                    if MapTreeModule_forallOpt(f, MapTreeNode_2__get_Left(mn))
                    else False
                ):
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(mn)
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


def MapTreeModule_map[VALUE, RESULT, KEY](
    f: Callable[[VALUE], RESULT], m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, RESULT] | None:
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            l2: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeModule_map(f, MapTreeNode_2__get_Left(mn)))
            v2: Any = f(MapTreeLeaf_2__get_Value(mn))
            r2: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeModule_map(f, MapTreeNode_2__get_Right(mn)))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(mn), v2, l2, r2, MapTreeNode_2__get_Height(mn))

        else:
            return MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Value(m2)))

    else:
        return erase(MapTreeModule_empty())


def MapTreeModule_mapiOpt[KEY, VALUE, RESULT](
    f: Any, m: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> MapTreeLeaf_2[KEY, RESULT] | None:
    if m is not None:
        m2: MapTreeLeaf_2[Any, Any] = m
        if isinstance(m2, MapTreeNode_2):
            mn: MapTreeNode_2[Any, Any] = m2
            l2: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Left(mn)))
            v2: Any = f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn))
            r2: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Right(mn)))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(mn), v2, l2, r2, MapTreeNode_2__get_Height(mn))

        else:
            return MapTreeLeaf_2__ctor_5BDDA1(
                MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            )

    else:
        return erase(MapTreeModule_empty())


def MapTreeModule_mapi[_A, _B, _C](
    f: Callable[[_A, _B], _C], m: MapTreeLeaf_2[_A, _B] | None = None
) -> MapTreeLeaf_2[_A, _C] | None:
    return erase(MapTreeModule_mapiOpt(f, m))


def MapTreeModule_foldBackOpt[KEY, VALUE, _A](f_mut: Any, m_mut: MapTreeLeaf_2[KEY, VALUE] | None, x_mut: _A) -> _A:
    while True:
        (f, m, x) = (f_mut, m_mut, x_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                x_1: Any = MapTreeModule_foldBackOpt(f, MapTreeNode_2__get_Right(mn), x)
                x_2: Any = f(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn), x_1)
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(mn)
                x_mut = x_2
                continue

            else:
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x)

        else:
            return x

        break


def MapTreeModule_foldBack[_A, _B, _C](f: Callable[[_A, _B, _C], _C], m: MapTreeLeaf_2[_A, _B] | None, x: _C) -> _C:
    return MapTreeModule_foldBackOpt(f, m, x)


def MapTreeModule_foldOpt[_A, KEY, VALUE](f_mut: Any, x_mut: _A, m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> _A:
    while True:
        (f, x, m) = (f_mut, x_mut, m_mut)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            if isinstance(m2, MapTreeNode_2):
                mn: MapTreeNode_2[Any, Any] = m2
                f_mut = f
                x_mut = f(
                    MapTreeModule_foldOpt(f, x, MapTreeNode_2__get_Left(mn)),
                    MapTreeLeaf_2__get_Key(mn),
                    MapTreeLeaf_2__get_Value(mn),
                )
                m_mut = MapTreeNode_2__get_Right(mn)
                continue

            else:
                return f(x, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            return x

        break


def MapTreeModule_fold[_A, _B, _C](f: Callable[[_A, _B, _C], _A], x: _A, m: MapTreeLeaf_2[_B, _C] | None = None) -> _A:
    return MapTreeModule_foldOpt(f, x, m)


def MapTreeModule_foldSectionOpt[KEY, VALUE, A](
    comparer: IComparer_1[KEY], lo: KEY, hi: KEY, f: Any, m: MapTreeLeaf_2[KEY, VALUE] | None, x: A
) -> A:
    def fold_from_to(
        f_1_mut: Any,
        m_1_mut: MapTreeLeaf_2[KEY, VALUE] | None,
        x_1_mut: A,
        comparer: Any = comparer,
        lo: Any = lo,
        hi: Any = hi,
    ) -> A:
        while True:
            (f_1, m_1, x_1) = (f_1_mut, m_1_mut, x_1_mut)
            if m_1 is not None:
                m2: MapTreeLeaf_2[Any, Any] = m_1
                if isinstance(m2, MapTreeNode_2):
                    mn: MapTreeNode_2[Any, Any] = m2
                    c_lo_key: int32 = comparer.Compare(lo, MapTreeLeaf_2__get_Key(mn))
                    c_key_hi: int32 = comparer.Compare(MapTreeLeaf_2__get_Key(mn), hi)
                    x_2: Any = fold_from_to(f_1, MapTreeNode_2__get_Left(mn), x_1) if (c_lo_key < int32.ZERO) else x_1
                    x_3: Any = (
                        f_1(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn), x_2)
                        if ((c_key_hi <= int32.ZERO) if (c_lo_key <= int32.ZERO) else False)
                        else x_2
                    )
                    if c_key_hi < int32.ZERO:
                        f_1_mut = f_1
                        m_1_mut = MapTreeNode_2__get_Right(mn)
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
        m_1_mut: MapTreeLeaf_2[KEY, VALUE] | None, acc_mut: FSharpList[tuple[KEY, VALUE]]
    ) -> FSharpList[tuple[KEY, VALUE]]:
        while True:
            (m_1, acc) = (m_1_mut, acc_mut)
            if m_1 is not None:
                m2: MapTreeLeaf_2[Any, Any] = m_1
                if isinstance(m2, MapTreeNode_2):
                    mn: MapTreeNode_2[Any, Any] = m2
                    m_1_mut = MapTreeNode_2__get_Left(mn)
                    acc_mut = cons(
                        (MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn)),
                        loop(MapTreeNode_2__get_Right(mn), acc),
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

    def _arrow230(x: _A, y: _B, arr: Any = arr) -> None:
        nonlocal j
        arr[j] = (x, y)
        j = j + int32.ONE

    MapTreeModule_iter(_arrow230, m)


def MapTreeModule_toArray[_A, _B](m: MapTreeLeaf_2[_A, _B] | None = None) -> Array[Any]:
    res: Array[Any] = zero_create(MapTreeModule_size(m), (cast(Any, None), cast(Any, None)))
    MapTreeModule_copyToArray(m, res, int32.ZERO)
    return res


def MapTreeModule_ofList[_A, _B](
    comparer: IComparer_1[_A], l: FSharpList[tuple[_A, _B]]
) -> MapTreeLeaf_2[_A, _B] | None:
    def _arrow231(
        acc: MapTreeLeaf_2[_A, _B] | None, tupled_arg: tuple[_A, _B], comparer: Any = comparer
    ) -> MapTreeLeaf_2[_A, _B] | None:
        return erase(MapTreeModule_add(comparer, tupled_arg[0], tupled_arg[1], acc))

    return erase(fold_1(_arrow231, MapTreeModule_empty(), l))


def MapTreeModule_mkFromEnumerator[_A, _B](
    comparer_mut: IComparer_1[_A], acc_mut: MapTreeLeaf_2[_A, _B] | None, e_mut: IEnumerator[tuple[_A, _B]]
) -> MapTreeLeaf_2[_A, _B] | None:
    while True:
        (comparer, acc, e) = (comparer_mut, acc_mut, e_mut)
        if e.System_Collections_IEnumerator_MoveNext():
            pattern_input: tuple[Any, Any] = e.System_Collections_Generic_IEnumerator_1_get_Current()
            comparer_mut = comparer
            acc_mut = MapTreeModule_add(comparer, pattern_input[0], pattern_input[1], acc)
            e_mut = e
            continue

        else:
            return acc

        break


def MapTreeModule_ofArray[KEY, VALUE](
    comparer: IComparer_1[KEY], arr: Array[tuple[KEY, VALUE]]
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    res: MapTreeLeaf_2[Any, Any] | None = erase(MapTreeModule_empty())
    for idx in range(int32.ZERO, int32(len(arr)) - int32.ONE, 1):
        for_loop_var: tuple[Any, Any] = arr[idx]
        res = MapTreeModule_add(comparer, for_loop_var[0], for_loop_var[1], res)
    return res


def MapTreeModule_ofSeq[KEY, VALUE](
    comparer: IComparer_1[KEY], c: IEnumerable_1[tuple[KEY, VALUE]]
) -> MapTreeLeaf_2[KEY, VALUE] | None:
    if isinstance(c, Array):
        return erase(MapTreeModule_ofArray(comparer, c))

    elif isinstance(c, FSharpList):
        return erase(MapTreeModule_ofList(comparer, c))

    else:
        with Disposable(get_enumerator(c)) as ie:
            return erase(MapTreeModule_mkFromEnumerator(comparer, MapTreeModule_empty(), ie))


def _expr232(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return record_type(
        "Map.MapTreeModule.MapIterator`2",
        Array([gen0, gen1]),
        MapTreeModule_MapIterator_2,
        lambda: [("stack_", list_type(option_type(MapTreeLeaf_2_reflection(gen0, gen1)))), ("started_", bool_type)],
    )


@dataclass(eq=False, repr=False, slots=True)
class MapTreeModule_MapIterator_2[KEY, VALUE](Record):
    stack_: FSharpList[MapTreeLeaf_2[Any, Any] | None]
    started_: bool

    def __hash__(self) -> int:
        return int(self.GetHashCode())


MapTreeModule_MapIterator_2_reflection = _expr232


def MapTreeModule_collapseLHS[KEY, VALUE](
    stack_mut: FSharpList[MapTreeLeaf_2[KEY, VALUE] | None],
) -> FSharpList[MapTreeLeaf_2[KEY, VALUE] | None]:
    while True:
        (stack,) = (stack_mut,)
        if not is_empty_1(stack):
            rest = tail(stack)
            m = head(stack)
            if m is not None:
                m2: MapTreeLeaf_2[Any, Any] = m
                if isinstance(m2, MapTreeNode_2):
                    mn: MapTreeNode_2[Any, Any] = m2
                    stack_mut = of_array_with_tail(
                        Array[Any](
                            [
                                MapTreeNode_2__get_Left(mn),
                                MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(mn), MapTreeLeaf_2__get_Value(mn)),
                                MapTreeNode_2__get_Right(mn),
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


def MapTreeModule_notStarted[_A](__unit: Unit = UNIT) -> _A:
    raise Exception("enumeration not started")


def MapTreeModule_alreadyFinished[_A](__unit: Unit = UNIT) -> _A:
    raise Exception("enumeration already finished")


def MapTreeModule_current[KEY, VALUE](i: MapTreeModule_MapIterator_2[KEY, VALUE]) -> Any:
    if i.started_:
        match_value: FSharpList[MapTreeLeaf_2[Any, Any] | None] = i.stack_
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m: MapTreeLeaf_2[Any, Any] = value_1(head(match_value))
                if isinstance(m, MapTreeNode_2):
                    raise Exception("Please report error: Map iterator, unexpected stack for current")

                else:
                    return (MapTreeLeaf_2__get_Key(m), MapTreeLeaf_2__get_Value(m))

            else:
                raise Exception("Please report error: Map iterator, unexpected stack for current")

        else:
            return MapTreeModule_alreadyFinished()

    else:
        return MapTreeModule_notStarted()


def MapTreeModule_moveNext[KEY, VALUE](i: MapTreeModule_MapIterator_2[KEY, VALUE]) -> bool:
    if i.started_:
        match_value: FSharpList[MapTreeLeaf_2[Any, Any] | None] = i.stack_
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m: MapTreeLeaf_2[Any, Any] = value_1(head(match_value))
                if isinstance(m, MapTreeNode_2):
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
    i: MapTreeModule_MapIterator_2[Any, Any] = MapTreeModule_mkIterator(m)

    class ObjectExpr233(EnumeratorBase[Any], DisposableBase):
        def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: Unit = UNIT) -> Any:
            return MapTreeModule_current(i)

        def System_Collections_IEnumerator_get_Current(self, __unit: Unit = UNIT) -> Any:
            return MapTreeModule_current(i)

        def System_Collections_IEnumerator_MoveNext(self, __unit: Unit = UNIT) -> bool:
            return MapTreeModule_moveNext(i)

        def System_Collections_IEnumerator_Reset(self, m: Any = m) -> None:
            nonlocal i
            i = MapTreeModule_mkIterator(m)

        def Dispose(self, __unit: Unit = UNIT) -> None:
            pass

    return ObjectExpr233()


def MapTreeModule_toSeq[_A, _B](s: MapTreeLeaf_2[_A, _B] | None = None) -> IEnumerable_1[Any]:
    def generator(en_1: IEnumerator[Any]) -> tuple[Any, IEnumerator[Any]] | None:
        if en_1.System_Collections_IEnumerator_MoveNext():
            return (en_1.System_Collections_Generic_IEnumerator_1_get_Current(), en_1)

        else:
            return None

    return unfold(generator, MapTreeModule_mkIEnumerator(s))


def MapTreeModule_leftmost[KEY, VALUE](m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> tuple[KEY, VALUE]:
    while True:
        (m,) = (m_mut,)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            (pattern_matching_result, nd_1) = nullable[int32, MapTreeNode_2[Any, Any]]()
            if isinstance(m2, MapTreeNode_2):
                if MapTreeNode_2__get_Height(m2) > int32.ONE:
                    pattern_matching_result = int32(0)
                    nd_1 = m2

                else:
                    pattern_matching_result = int32(1)

            else:
                pattern_matching_result = int32(1)

            if pattern_matching_result == int32.ZERO:
                if MapTreeNode_2__get_Left(nd_1) is None:
                    return (MapTreeLeaf_2__get_Key(nd_1), MapTreeLeaf_2__get_Value(nd_1))

                else:
                    m_mut = MapTreeNode_2__get_Left(nd_1)
                    continue

            else:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            raise ExceptionBase()

        break


def MapTreeModule_rightmost[KEY, VALUE](m_mut: MapTreeLeaf_2[KEY, VALUE] | None) -> tuple[KEY, VALUE]:
    while True:
        (m,) = (m_mut,)
        if m is not None:
            m2: MapTreeLeaf_2[Any, Any] = m
            (pattern_matching_result, nd_1) = nullable[int32, MapTreeNode_2[Any, Any]]()
            if isinstance(m2, MapTreeNode_2):
                if MapTreeNode_2__get_Height(m2) > int32.ONE:
                    pattern_matching_result = int32(0)
                    nd_1 = m2

                else:
                    pattern_matching_result = int32(1)

            else:
                pattern_matching_result = int32(1)

            if pattern_matching_result == int32.ZERO:
                if MapTreeNode_2__get_Right(nd_1) is None:
                    return (MapTreeLeaf_2__get_Key(nd_1), MapTreeLeaf_2__get_Value(nd_1))

                else:
                    m_mut = MapTreeNode_2__get_Right(nd_1)
                    continue

            else:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))

        else:
            raise ExceptionBase()

        break


def _expr236(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Map.FSharpMap", Array([gen0, gen1]), FSharpMap)


class FSharpMap[KEY, VALUE](Mapping[Any, Any], StringableBase, ComparableBase, EquatableBase, EnumerableBase[Any]):
    def __init__(self, comparer: IComparer_1[KEY], tree: MapTreeLeaf_2[KEY, VALUE] | None = None) -> None:
        self.comparer: IComparer_1[Any] = comparer
        self.tree: MapTreeLeaf_2[Any, Any] | None = tree

    def GetHashCode(self, __unit: Unit = UNIT) -> int32:
        this: FSharpMap[Any, Any] = self
        return FSharpMap__ComputeHashCode(this)

    def Equals(self, other: Any = None) -> bool:
        this: FSharpMap[Any, Any] = self
        if isinstance(other, FSharpMap):
            with Disposable(get_enumerator(this)) as e1:
                with Disposable(get_enumerator(other)) as e2:

                    def loop(__unit: Unit = UNIT) -> bool:
                        m1: bool = e1.System_Collections_IEnumerator_MoveNext()
                        if m1 == e2.System_Collections_IEnumerator_MoveNext():
                            if not m1:
                                return True

                            else:
                                e1c: Any = e1.System_Collections_Generic_IEnumerator_1_get_Current()
                                e2c: Any = e2.System_Collections_Generic_IEnumerator_1_get_Current()
                                if equals(e1c[1], e2c[1]) if equals(e1c[0], e2c[0]) else False:
                                    return loop()

                                else:
                                    return False

                        else:
                            return False

                    return loop()

        else:
            return False

    def ToString(self, __unit: Unit = UNIT) -> str:
        this: FSharpMap[Any, Any] = self

        def _arrow234(kv: Any) -> str:
            return format("({0}, {1})", kv[0], kv[1])

        return ("map [" + join("; ", map_1(_arrow234, this))) + "]"

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        _: FSharpMap[Any, Any] = self
        return MapTreeModule_mkIEnumerator(_.tree)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        _: FSharpMap[Any, Any] = self
        return MapTreeModule_mkIEnumerator(_.tree)

    def CompareTo(self, other: Any = None) -> int32:
        this: FSharpMap[Any, Any] = self

        def _arrow235(kvp1: Any, kvp2: Any) -> int32:
            c: int32 = this.comparer.Compare(kvp1[0], kvp2[0])
            return c if (c != int32.ZERO) else compare(kvp1[1], kvp2[1])

        return compare_with(_arrow235, this, other) if isinstance(other, FSharpMap) else int32.ONE

    def System_Collections_Generic_ICollection_1_Add2B595(self, x: Any = UNIT) -> None:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: Unit = UNIT) -> None:
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Remove2B595(self, x: Any = UNIT) -> bool:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("Map cannot be mutated")

    def System_Collections_Generic_ICollection_1_Contains2B595(self, x: Any = UNIT) -> bool:
        m: FSharpMap[Any, Any] = self
        return equals(FSharpMap__get_Item(m, x[0]), x[1]) if FSharpMap__ContainsKey(m, x[0]) else False

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, arr: Array[Any], i: int32) -> None:
        m: FSharpMap[Any, Any] = self
        MapTreeModule_copyToArray(m.tree, arr, i)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: Unit = UNIT) -> bool:
        return True

    def System_Collections_Generic_ICollection_1_get_Count(self, __unit: Unit = UNIT) -> int32:
        m: FSharpMap[Any, Any] = self
        return FSharpMap__get_Count(m)

    def System_Collections_Generic_IReadOnlyCollection_1_get_Count(self, __unit: Unit = UNIT) -> int32:
        m: FSharpMap[Any, Any] = self
        return FSharpMap__get_Count(m)

    def get_item(self, key: KEY = UNIT) -> VALUE:
        this: FSharpMap[Any, Any] = self
        return FSharpMap__get_Item(this, key)

    def ContainsKey(self, key: KEY = UNIT) -> bool:
        this: FSharpMap[Any, Any] = self
        return FSharpMap__ContainsKey(this, key)

    @property
    def Count(self, __unit: Unit = UNIT) -> int32:
        this: FSharpMap[Any, Any] = self
        return FSharpMap__get_Count(this)

    def __getitem__(self, key):
        return self.get_item(key)

    def __contains__(self, key):
        return self.ContainsKey(key)

    def __len__(self):
        return self.Count

    def __iter__(self):
        for kv in to_iterator(self.GetEnumerator()):
            yield kv[0]


FSharpMap_reflection = _expr236


def FSharpMap__ctor[KEY, VALUE](
    comparer: IComparer_1[KEY], tree: MapTreeLeaf_2[KEY, VALUE] | None = None
) -> FSharpMap[KEY, VALUE]:
    return FSharpMap(comparer, tree)


def FSharpMap_Empty[KEY, VALUE](comparer: IComparer_1[KEY]) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(comparer, MapTreeModule_empty())


def FSharpMap__get_Comparer[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> IComparer_1[KEY]:
    return m.comparer


def FSharpMap__get_Tree[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> MapTreeLeaf_2[KEY, VALUE] | None:
    return m.tree


def FSharpMap__Add[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY, value: VALUE) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_add(m.comparer, key, value, m.tree))


def FSharpMap__Change[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], key: KEY, f: Callable[[Option[VALUE]], Option[VALUE]]
) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_change(m.comparer, key, f, m.tree))


def FSharpMap__get_IsEmpty[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> bool:
    return m.tree is None


def FSharpMap__get_Item[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> VALUE:
    return MapTreeModule_find(m.comparer, key, m.tree)


def FSharpMap__TryPick[_A, KEY, VALUE](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], Option[_A]]) -> Option[_A]:
    return MapTreeModule_tryPick(f, m.tree)


def FSharpMap__Exists[KEY, VALUE](m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]) -> bool:
    return MapTreeModule_exists(predicate, m.tree)


def FSharpMap__Filter[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]
) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_filter(m.comparer, predicate, m.tree))


def FSharpMap__ForAll[KEY, VALUE](m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]) -> bool:
    return MapTreeModule_forall(predicate, m.tree)


def FSharpMap__Fold[_A, KEY, VALUE](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE, _A], _A], acc: _A) -> _A:
    return MapTreeModule_foldBack(f, m.tree, acc)


def FSharpMap__FoldSection[_A, KEY, VALUE](
    m: FSharpMap[KEY, VALUE], lo: KEY, hi: KEY, f: Callable[[KEY, VALUE, _A], _A], acc: _A
) -> _A:
    return MapTreeModule_foldSection(m.comparer, lo, hi, f, m.tree, acc)


def FSharpMap__Iterate[KEY, VALUE](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], None]) -> None:
    MapTreeModule_iter(f, m.tree)


def FSharpMap__MapRange[RESULT, KEY, VALUE](
    m: FSharpMap[KEY, VALUE], f: Callable[[VALUE], RESULT]
) -> FSharpMap[KEY, RESULT]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_map(f, m.tree))


def FSharpMap__Map[B, KEY, VALUE](m: FSharpMap[KEY, VALUE], f: Callable[[KEY, VALUE], B]) -> FSharpMap[KEY, B]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_mapi(f, m.tree))


def FSharpMap__Partition[KEY, VALUE](
    m: FSharpMap[KEY, VALUE], predicate: Callable[[KEY, VALUE], bool]
) -> tuple[FSharpMap[KEY, VALUE], FSharpMap[KEY, VALUE]]:
    pattern_input: tuple[MapTreeLeaf_2[Any, Any] | None, MapTreeLeaf_2[Any, Any] | None] = MapTreeModule_partition(
        m.comparer, predicate, m.tree
    )
    return (FSharpMap__ctor(m.comparer, pattern_input[0]), FSharpMap__ctor(m.comparer, pattern_input[1]))


def FSharpMap__get_Count[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> int32:
    return MapTreeModule_size(m.tree)


def FSharpMap__ContainsKey[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> bool:
    return MapTreeModule_mem(m.comparer, key, m.tree)


def FSharpMap__Remove[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> FSharpMap[KEY, VALUE]:
    return FSharpMap__ctor(m.comparer, MapTreeModule_remove(m.comparer, key, m.tree))


def FSharpMap__TryGetValue[KEY, VALUE](_: FSharpMap[KEY, VALUE], key: KEY, value: FSharpRef[VALUE]) -> bool:
    match_value: Option[Any] = MapTreeModule_tryFind(_.comparer, key, _.tree)
    if match_value is None:
        return False

    else:
        v: Any = value_1(match_value)
        value.contents = v
        return True


def FSharpMap__get_Keys[KEY, VALUE](_: FSharpMap[KEY, VALUE]) -> ICollection[KEY]:
    def mapping(kvp: Any) -> KEY:
        return kvp[0]

    return map_2(mapping, MapTreeModule_toArray(_.tree), None)


def FSharpMap__get_Values[KEY, VALUE](_: FSharpMap[KEY, VALUE]) -> ICollection[VALUE]:
    def mapping(kvp: Any) -> VALUE:
        return kvp[1]

    return map_2(mapping, MapTreeModule_toArray(_.tree), None)


def FSharpMap__get_MinKeyValue[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> tuple[KEY, VALUE]:
    return MapTreeModule_leftmost(m.tree)


def FSharpMap__get_MaxKeyValue[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> tuple[KEY, VALUE]:
    return MapTreeModule_rightmost(m.tree)


def FSharpMap__TryFind[KEY, VALUE](m: FSharpMap[KEY, VALUE], key: KEY) -> Option[VALUE]:
    return MapTreeModule_tryFind(m.comparer, key, m.tree)


def FSharpMap__ToList[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> FSharpList[tuple[KEY, VALUE]]:
    return MapTreeModule_toList(m.tree)


def FSharpMap__ToArray[KEY, VALUE](m: FSharpMap[KEY, VALUE]) -> Array[Any]:
    return MapTreeModule_toArray(m.tree)


def FSharpMap__ComputeHashCode[KEY, VALUE](this: FSharpMap[KEY, VALUE]) -> int32:
    def combine_hash(x: int32, y: int32) -> int32:
        return ((x << int32.ONE) + y) + int32(631)

    res: int32 = int32.ZERO
    with Disposable(get_enumerator(this)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            active_pattern_result: tuple[Any, Any] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            res = combine_hash(res, structural_hash(active_pattern_result[0]))
            res = combine_hash(res, structural_hash(active_pattern_result[1]))
    return res


def is_empty[_A, _B](table: FSharpMap[_A, _B]) -> bool:
    return FSharpMap__get_IsEmpty(table)


def add[_A, _B](key: _A, value: _B, table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Add(table, key, value)


def change[_A, _B](key: _A, f: Callable[[Option[_B]], Option[_B]], table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Change(table, key, f)


def find[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> _B:
    return FSharpMap__get_Item(table, key)


def try_find[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> Option[_B]:
    return FSharpMap__TryFind(table, key)


def remove[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> FSharpMap[_A, _B]:
    return FSharpMap__Remove(table, key)


def contains_key[_A, _B](key: _A, table: FSharpMap[_A, _B]) -> bool:
    return FSharpMap__ContainsKey(table, key)


def iterate[_A, _B](action: Callable[[_A, _B], None], table: FSharpMap[_A, _B]) -> None:
    FSharpMap__Iterate(table, action)


def try_pick[_A, _B, _C](chooser: Callable[[_A, _B], Option[_C]], table: FSharpMap[_A, _B]) -> Option[_C]:
    return FSharpMap__TryPick(table, chooser)


def pick[_A, _B, _C](chooser: Callable[[_A, _B], Option[_C]], table: FSharpMap[_A, _B]) -> _C:
    match_value: Option[Any] = try_pick(chooser, table)
    if match_value is not None:
        return value_1(match_value)

    else:
        raise ExceptionBase()


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


def fold[KEY, T, STATE](folder: Callable[[STATE, KEY, T], STATE], state: STATE, table: FSharpMap[KEY, T]) -> STATE:
    return MapTreeModule_fold(folder, state, FSharpMap__get_Tree(table))


def fold_back[KEY, T, STATE](folder: Callable[[KEY, T, STATE], STATE], table: FSharpMap[KEY, T], state: STATE) -> STATE:
    return MapTreeModule_foldBack(folder, FSharpMap__get_Tree(table), state)


def to_seq[_A, _B](table: FSharpMap[_A, _B]) -> IEnumerable_1[tuple[_A, _B]]:
    def mapping(kvp: Any) -> tuple[_A, _B]:
        return (kvp[0], kvp[1])

    return map_1(mapping, table)


def find_key[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> _A:
    def chooser(kvp: Any, predicate: Any = predicate) -> Option[_A]:
        k: Any = kvp[0]
        if predicate(k, kvp[1]):
            return some(k)

        else:
            return None

    return pick_1(chooser, table)


def try_find_key[_A, _B](predicate: Callable[[_A, _B], bool], table: FSharpMap[_A, _B]) -> Option[_A]:
    def chooser(kvp: Any, predicate: Any = predicate) -> Option[_A]:
        k: Any = kvp[0]
        if predicate(k, kvp[1]):
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


def keys[K, V](table: FSharpMap[K, V]) -> ICollection[K]:
    return FSharpMap__get_Keys(table)


def values[K, V](table: FSharpMap[K, V]) -> ICollection[V]:
    return FSharpMap__get_Values(table)


def min_key_value[_A, _B](table: FSharpMap[_A, _B]) -> tuple[_A, _B]:
    return FSharpMap__get_MinKeyValue(table)


def max_key_value[_A, _B](table: FSharpMap[_A, _B]) -> tuple[_A, _B]:
    return FSharpMap__get_MaxKeyValue(table)


def empty[KEY, VALUE](comparer: IComparer_1[KEY]) -> FSharpMap[KEY, VALUE]:
    return FSharpMap_Empty(comparer)


def count[_A, _B](table: FSharpMap[_A, _B]) -> int32:
    return FSharpMap__get_Count(table)


__all__ = [
    "FSharpMap_Empty",
    "FSharpMap__Add",
    "FSharpMap__Change",
    "FSharpMap__ComputeHashCode",
    "FSharpMap__ContainsKey",
    "FSharpMap__Exists",
    "FSharpMap__Filter",
    "FSharpMap__Fold",
    "FSharpMap__FoldSection",
    "FSharpMap__ForAll",
    "FSharpMap__Iterate",
    "FSharpMap__Map",
    "FSharpMap__MapRange",
    "FSharpMap__Partition",
    "FSharpMap__Remove",
    "FSharpMap__ToArray",
    "FSharpMap__ToList",
    "FSharpMap__TryFind",
    "FSharpMap__TryGetValue",
    "FSharpMap__TryPick",
    "FSharpMap__get_Comparer",
    "FSharpMap__get_Count",
    "FSharpMap__get_IsEmpty",
    "FSharpMap__get_Item",
    "FSharpMap__get_Keys",
    "FSharpMap__get_MaxKeyValue",
    "FSharpMap__get_MinKeyValue",
    "FSharpMap__get_Tree",
    "FSharpMap__get_Values",
    "FSharpMap_reflection",
    "MapTreeLeaf_2__get_Key",
    "MapTreeLeaf_2__get_Value",
    "MapTreeLeaf_2_reflection",
    "MapTreeModule_MapIterator_2_reflection",
    "MapTreeModule_add",
    "MapTreeModule_alreadyFinished",
    "MapTreeModule_change",
    "MapTreeModule_collapseLHS",
    "MapTreeModule_copyToArray",
    "MapTreeModule_current",
    "MapTreeModule_empty",
    "MapTreeModule_exists",
    "MapTreeModule_existsOpt",
    "MapTreeModule_filter",
    "MapTreeModule_filter1",
    "MapTreeModule_filterAux",
    "MapTreeModule_find",
    "MapTreeModule_fold",
    "MapTreeModule_foldBack",
    "MapTreeModule_foldBackOpt",
    "MapTreeModule_foldOpt",
    "MapTreeModule_foldSection",
    "MapTreeModule_foldSectionOpt",
    "MapTreeModule_forall",
    "MapTreeModule_forallOpt",
    "MapTreeModule_iter",
    "MapTreeModule_iterOpt",
    "MapTreeModule_leftmost",
    "MapTreeModule_map",
    "MapTreeModule_mapi",
    "MapTreeModule_mapiOpt",
    "MapTreeModule_mem",
    "MapTreeModule_mk",
    "MapTreeModule_mkFromEnumerator",
    "MapTreeModule_mkIEnumerator",
    "MapTreeModule_mkIterator",
    "MapTreeModule_moveNext",
    "MapTreeModule_notStarted",
    "MapTreeModule_ofArray",
    "MapTreeModule_ofList",
    "MapTreeModule_ofSeq",
    "MapTreeModule_partition",
    "MapTreeModule_partition1",
    "MapTreeModule_partitionAux",
    "MapTreeModule_rebalance",
    "MapTreeModule_remove",
    "MapTreeModule_rightmost",
    "MapTreeModule_size",
    "MapTreeModule_sizeAux",
    "MapTreeModule_spliceOutSuccessor",
    "MapTreeModule_toArray",
    "MapTreeModule_toList",
    "MapTreeModule_toSeq",
    "MapTreeModule_tryFind",
    "MapTreeModule_tryPick",
    "MapTreeModule_tryPickOpt",
    "MapTreeNode_2__get_Height",
    "MapTreeNode_2__get_Left",
    "MapTreeNode_2__get_Right",
    "MapTreeNode_2_reflection",
    "add",
    "change",
    "contains_key",
    "count",
    "empty",
    "exists",
    "filter",
    "find",
    "find_key",
    "fold",
    "fold_back",
    "for_all",
    "is_empty",
    "iterate",
    "keys",
    "map",
    "max_key_value",
    "min_key_value",
    "of_array",
    "of_list",
    "of_seq",
    "partition",
    "pick",
    "remove",
    "to_array",
    "to_list",
    "to_seq",
    "try_find",
    "try_find_key",
    "try_pick",
    "values",
]
