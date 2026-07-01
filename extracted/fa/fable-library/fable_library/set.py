from __future__ import annotations

from collections.abc import Callable, Set
from dataclasses import dataclass
from typing import Any, cast

from fable_library.util import to_iterator

from .array_ import Array, zero_create
from .array_ import fold as fold_1
from .array_ import iterate as iterate_2
from .bases import ComparableBase, DisposableBase, EnumerableBase, EnumeratorBase, EquatableBase, StringableBase
from .core import int32
from .list import FSharpList, cons, head, of_array_with_tail, tail
from .list import empty as empty_1
from .list import fold as fold_2
from .list import is_empty as is_empty_1
from .list import singleton as singleton_1
from .mutable_set import (
    HashSet,
    HashSet__Add_2B595,
    HashSet__Contains_2B595,
    HashSet__ctor_Z6150332D,
    HashSet__get_Comparer,
    HashSet__get_Count,
    HashSet__Remove_2B595,
)
from .option import Option, erase, some
from .option import value as value_1
from .protocols import IComparer_1, IEnumerable_1, IEnumerator
from .record import Record
from .reflection import TypeInfo, bool_type, class_type, list_type, option_type, record_type
from .seq import fold as fold_3
from .seq import for_all as for_all_1
from .seq import iterate as iterate_1
from .seq import map as map_1
from .seq import reduce
from .string_ import join
from .system import NotSupportedException__ctor_Z721C83C5
from .util import UNIT, Disposable, Unit, get_enumerator, ignore, nullable, structural_hash


def _expr216(gen0: TypeInfo) -> TypeInfo:
    return class_type("Set.SetTreeLeaf`1", Array([gen0]), SetTreeLeaf_1)


class SetTreeLeaf_1[T]:
    def __init__(self, k: T = UNIT) -> None:
        self.k: Any = k


SetTreeLeaf_1_reflection = _expr216


def SetTreeLeaf_1__ctor_2B595[T](k: T = UNIT) -> SetTreeLeaf_1[T]:
    return SetTreeLeaf_1(k)


def SetTreeLeaf_1__get_Key[T](_: SetTreeLeaf_1[T]) -> T:
    return _.k


def _expr217(gen0: TypeInfo) -> TypeInfo:
    return class_type("Set.SetTreeNode`1", Array([gen0]), SetTreeNode_1, SetTreeLeaf_1_reflection(gen0))


class SetTreeNode_1[T](SetTreeLeaf_1):
    def __init__(self, v: T, left: SetTreeLeaf_1[T] | None, right: SetTreeLeaf_1[T] | None, h: int32) -> None:
        super().__init__(v)
        self.left: SetTreeLeaf_1[Any] | None = left
        self.right: SetTreeLeaf_1[Any] | None = right
        self.h: int32 = h


SetTreeNode_1_reflection = _expr217


def SetTreeNode_1__ctor_5F465FC9[T](
    v: T, left: SetTreeLeaf_1[T] | None, right: SetTreeLeaf_1[T] | None, h: int32
) -> SetTreeNode_1[T]:
    return SetTreeNode_1(v, left, right, h)


def SetTreeNode_1__get_Left[T](_: SetTreeNode_1[T]) -> SetTreeLeaf_1[T] | None:
    return _.left


def SetTreeNode_1__get_Right[T](_: SetTreeNode_1[T]) -> SetTreeLeaf_1[T] | None:
    return _.right


def SetTreeNode_1__get_Height[T](_: SetTreeNode_1[T]) -> int32:
    return _.h


def SetTreeModule_empty[T](__unit: Unit = UNIT) -> SetTreeLeaf_1[T] | None:
    return None


def SetTreeModule_countAux[T](t_mut: SetTreeLeaf_1[T] | None, acc_mut: int32) -> int32:
    while True:
        (t, acc) = (t_mut, acc_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                t_mut = SetTreeNode_1__get_Left(tn)
                acc_mut = SetTreeModule_countAux(SetTreeNode_1__get_Right(tn), acc + int32.ONE)
                continue

            else:
                return acc + int32.ONE

        else:
            return acc

        break


def SetTreeModule_count[_A](s: SetTreeLeaf_1[_A] | None = None) -> int32:
    return SetTreeModule_countAux(s, int32.ZERO)


def SetTreeModule_mk[T](l: SetTreeLeaf_1[T] | None, k: T, r: SetTreeLeaf_1[T] | None = None) -> SetTreeLeaf_1[T] | None:
    hl: int32
    t: SetTreeLeaf_1[Any] | None = l
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        hl = SetTreeNode_1__get_Height(t2) if isinstance(t2, SetTreeNode_1) else int32.ONE

    else:
        hl = int32.ZERO

    hr: int32
    t_1: SetTreeLeaf_1[Any] | None = r
    if t_1 is not None:
        t2_1: SetTreeLeaf_1[Any] = t_1
        hr = SetTreeNode_1__get_Height(t2_1) if isinstance(t2_1, SetTreeNode_1) else int32.ONE

    else:
        hr = int32.ZERO

    m: int32 = hr if (hl < hr) else hl
    if m == int32.ZERO:
        return SetTreeLeaf_1__ctor_2B595(k)

    else:
        return SetTreeNode_1__ctor_5F465FC9(k, l, r, m + int32.ONE)


def SetTreeModule_rebalance[T](
    t1: SetTreeLeaf_1[T] | None, v: T, t2: SetTreeLeaf_1[T] | None = None
) -> SetTreeLeaf_1[T] | None:
    t1h: int32
    t: SetTreeLeaf_1[Any] | None = t1
    if t is not None:
        t2_1: SetTreeLeaf_1[Any] = t
        t1h = SetTreeNode_1__get_Height(t2_1) if isinstance(t2_1, SetTreeNode_1) else int32.ONE

    else:
        t1h = int32.ZERO

    t2h: int32
    t_1: SetTreeLeaf_1[Any] | None = t2
    if t_1 is not None:
        t2_2: SetTreeLeaf_1[Any] = t_1
        t2h = SetTreeNode_1__get_Height(t2_2) if isinstance(t2_2, SetTreeNode_1) else int32.ONE

    else:
        t2h = int32.ZERO

    if t2h > (t1h + int32.TWO):
        match_value: SetTreeLeaf_1[Any] = value_1(t2)
        if isinstance(match_value, SetTreeNode_1):
            t2_0027: SetTreeNode_1[Any] = match_value

            def _arrow218(__unit: Unit = UNIT) -> int32:
                t_2: SetTreeLeaf_1[Any] | None = erase(SetTreeNode_1__get_Left(t2_0027))
                if t_2 is not None:
                    t2_3: SetTreeLeaf_1[Any] = t_2
                    return SetTreeNode_1__get_Height(t2_3) if isinstance(t2_3, SetTreeNode_1) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow218() > (t1h + int32.ONE):
                match_value_1: SetTreeLeaf_1[Any] = value_1(SetTreeNode_1__get_Left(t2_0027))
                if isinstance(match_value_1, SetTreeNode_1):
                    t2l: SetTreeNode_1[Any] = match_value_1
                    return erase(
                        SetTreeModule_mk(
                            SetTreeModule_mk(t1, v, SetTreeNode_1__get_Left(t2l)),
                            SetTreeLeaf_1__get_Key(t2l),
                            SetTreeModule_mk(
                                SetTreeNode_1__get_Right(t2l),
                                SetTreeLeaf_1__get_Key(t2_0027),
                                SetTreeNode_1__get_Right(t2_0027),
                            ),
                        )
                    )

                else:
                    raise Exception("internal error: Set.rebalance")

            else:
                return erase(
                    SetTreeModule_mk(
                        SetTreeModule_mk(t1, v, SetTreeNode_1__get_Left(t2_0027)),
                        SetTreeLeaf_1__get_Key(t2_0027),
                        SetTreeNode_1__get_Right(t2_0027),
                    )
                )

        else:
            raise Exception("internal error: Set.rebalance")

    elif t1h > (t2h + int32.TWO):
        match_value_2: SetTreeLeaf_1[Any] = value_1(t1)
        if isinstance(match_value_2, SetTreeNode_1):
            t1_0027: SetTreeNode_1[Any] = match_value_2

            def _arrow219(__unit: Unit = UNIT) -> int32:
                t_3: SetTreeLeaf_1[Any] | None = erase(SetTreeNode_1__get_Right(t1_0027))
                if t_3 is not None:
                    t2_4: SetTreeLeaf_1[Any] = t_3
                    return SetTreeNode_1__get_Height(t2_4) if isinstance(t2_4, SetTreeNode_1) else int32.ONE

                else:
                    return int32.ZERO

            if _arrow219() > (t2h + int32.ONE):
                match_value_3: SetTreeLeaf_1[Any] = value_1(SetTreeNode_1__get_Right(t1_0027))
                if isinstance(match_value_3, SetTreeNode_1):
                    t1r: SetTreeNode_1[Any] = match_value_3
                    return erase(
                        SetTreeModule_mk(
                            SetTreeModule_mk(
                                SetTreeNode_1__get_Left(t1_0027),
                                SetTreeLeaf_1__get_Key(t1_0027),
                                SetTreeNode_1__get_Left(t1r),
                            ),
                            SetTreeLeaf_1__get_Key(t1r),
                            SetTreeModule_mk(SetTreeNode_1__get_Right(t1r), v, t2),
                        )
                    )

                else:
                    raise Exception("internal error: Set.rebalance")

            else:
                return erase(
                    SetTreeModule_mk(
                        SetTreeNode_1__get_Left(t1_0027),
                        SetTreeLeaf_1__get_Key(t1_0027),
                        SetTreeModule_mk(SetTreeNode_1__get_Right(t1_0027), v, t2),
                    )
                )

        else:
            raise Exception("internal error: Set.rebalance")

    else:
        return erase(SetTreeModule_mk(t1, v, t2))


def SetTreeModule_add[T](comparer: IComparer_1[T], k: T, t: SetTreeLeaf_1[T] | None = None) -> SetTreeLeaf_1[T] | None:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        c: int32 = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2))
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            if c < int32.ZERO:
                return erase(
                    SetTreeModule_rebalance(
                        SetTreeModule_add(comparer, k, SetTreeNode_1__get_Left(tn)),
                        SetTreeLeaf_1__get_Key(tn),
                        SetTreeNode_1__get_Right(tn),
                    )
                )

            elif c == int32.ZERO:
                return t

            else:
                return erase(
                    SetTreeModule_rebalance(
                        SetTreeNode_1__get_Left(tn),
                        SetTreeLeaf_1__get_Key(tn),
                        SetTreeModule_add(comparer, k, SetTreeNode_1__get_Right(tn)),
                    )
                )

        else:
            c_1: int32 = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2))
            if c_1 < int32.ZERO:
                return SetTreeNode_1__ctor_5F465FC9(k, SetTreeModule_empty(), t, int32.TWO)

            elif c_1 == int32.ZERO:
                return t

            else:
                return SetTreeNode_1__ctor_5F465FC9(k, t, SetTreeModule_empty(), int32.TWO)

    else:
        return SetTreeLeaf_1__ctor_2B595(k)


def SetTreeModule_balance[T](
    comparer: IComparer_1[T], t1: SetTreeLeaf_1[T] | None, k: T, t2: SetTreeLeaf_1[T] | None = None
) -> SetTreeLeaf_1[T] | None:
    if t1 is not None:
        t1_0027: SetTreeLeaf_1[Any] = t1
        if t2 is not None:
            t2_0027: SetTreeLeaf_1[Any] = t2
            if isinstance(t1_0027, SetTreeNode_1):
                t1n: SetTreeNode_1[Any] = t1_0027
                if isinstance(t2_0027, SetTreeNode_1):
                    t2n: SetTreeNode_1[Any] = t2_0027
                    if (SetTreeNode_1__get_Height(t1n) + int32.TWO) < SetTreeNode_1__get_Height(t2n):
                        return erase(
                            SetTreeModule_rebalance(
                                SetTreeModule_balance(comparer, t1, k, SetTreeNode_1__get_Left(t2n)),
                                SetTreeLeaf_1__get_Key(t2n),
                                SetTreeNode_1__get_Right(t2n),
                            )
                        )

                    elif (SetTreeNode_1__get_Height(t2n) + int32.TWO) < SetTreeNode_1__get_Height(t1n):
                        return erase(
                            SetTreeModule_rebalance(
                                SetTreeNode_1__get_Left(t1n),
                                SetTreeLeaf_1__get_Key(t1n),
                                SetTreeModule_balance(comparer, SetTreeNode_1__get_Right(t1n), k, t2),
                            )
                        )

                    else:
                        return erase(SetTreeModule_mk(t1, k, t2))

                else:
                    return erase(
                        SetTreeModule_add(comparer, k, SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2_0027), t1))
                    )

            else:
                return erase(
                    SetTreeModule_add(comparer, k, SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t1_0027), t2))
                )

        else:
            return erase(SetTreeModule_add(comparer, k, t1))

    else:
        return erase(SetTreeModule_add(comparer, k, t2))


def SetTreeModule_split[T](
    comparer: IComparer_1[T], pivot: T, t: SetTreeLeaf_1[T] | None = None
) -> tuple[SetTreeLeaf_1[T] | None, bool, SetTreeLeaf_1[T] | None]:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            c: int32 = comparer.Compare(pivot, SetTreeLeaf_1__get_Key(tn))
            if c < int32.ZERO:
                pattern_input: tuple[SetTreeLeaf_1[Any] | None, bool, SetTreeLeaf_1[Any] | None] = SetTreeModule_split(
                    comparer, pivot, SetTreeNode_1__get_Left(tn)
                )
                return (
                    pattern_input[0],
                    pattern_input[1],
                    SetTreeModule_balance(
                        comparer, pattern_input[2], SetTreeLeaf_1__get_Key(tn), SetTreeNode_1__get_Right(tn)
                    ),
                )

            elif c == int32.ZERO:
                return (SetTreeNode_1__get_Left(tn), True, SetTreeNode_1__get_Right(tn))

            else:
                pattern_input_1: tuple[SetTreeLeaf_1[Any] | None, bool, SetTreeLeaf_1[Any] | None] = (
                    SetTreeModule_split(comparer, pivot, SetTreeNode_1__get_Right(tn))
                )
                return (
                    SetTreeModule_balance(
                        comparer, SetTreeNode_1__get_Left(tn), SetTreeLeaf_1__get_Key(tn), pattern_input_1[0]
                    ),
                    pattern_input_1[1],
                    pattern_input_1[2],
                )

        else:
            c_1: int32 = comparer.Compare(SetTreeLeaf_1__get_Key(t2), pivot)
            if c_1 < int32.ZERO:
                return (t, False, SetTreeModule_empty())

            elif c_1 == int32.ZERO:
                return (SetTreeModule_empty(), True, SetTreeModule_empty())

            else:
                return (SetTreeModule_empty(), False, t)

    else:
        return (SetTreeModule_empty(), False, SetTreeModule_empty())


def SetTreeModule_spliceOutSuccessor[T](t: SetTreeLeaf_1[T] | None = None) -> tuple[T, SetTreeLeaf_1[T] | None]:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            if SetTreeNode_1__get_Left(tn) is None:
                return (SetTreeLeaf_1__get_Key(tn), SetTreeNode_1__get_Right(tn))

            else:
                pattern_input: tuple[Any, SetTreeLeaf_1[Any] | None] = SetTreeModule_spliceOutSuccessor(
                    SetTreeNode_1__get_Left(tn)
                )
                return (
                    pattern_input[0],
                    SetTreeModule_mk(pattern_input[1], SetTreeLeaf_1__get_Key(tn), SetTreeNode_1__get_Right(tn)),
                )

        else:
            return (SetTreeLeaf_1__get_Key(t2), SetTreeModule_empty())

    else:
        raise Exception("internal error: Set.spliceOutSuccessor")


def SetTreeModule_remove[T](
    comparer: IComparer_1[T], k: T, t: SetTreeLeaf_1[T] | None = None
) -> SetTreeLeaf_1[T] | None:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        c: int32 = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2))
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            if c < int32.ZERO:
                return erase(
                    SetTreeModule_rebalance(
                        SetTreeModule_remove(comparer, k, SetTreeNode_1__get_Left(tn)),
                        SetTreeLeaf_1__get_Key(tn),
                        SetTreeNode_1__get_Right(tn),
                    )
                )

            elif c == int32.ZERO:
                if SetTreeNode_1__get_Left(tn) is None:
                    return erase(SetTreeNode_1__get_Right(tn))

                elif SetTreeNode_1__get_Right(tn) is None:
                    return erase(SetTreeNode_1__get_Left(tn))

                else:
                    pattern_input: tuple[Any, SetTreeLeaf_1[Any] | None] = SetTreeModule_spliceOutSuccessor(
                        SetTreeNode_1__get_Right(tn)
                    )
                    return erase(SetTreeModule_mk(SetTreeNode_1__get_Left(tn), pattern_input[0], pattern_input[1]))

            else:
                return erase(
                    SetTreeModule_rebalance(
                        SetTreeNode_1__get_Left(tn),
                        SetTreeLeaf_1__get_Key(tn),
                        SetTreeModule_remove(comparer, k, SetTreeNode_1__get_Right(tn)),
                    )
                )

        elif c == int32.ZERO:
            return erase(SetTreeModule_empty())

        else:
            return t

    else:
        return t


def SetTreeModule_mem[T](comparer_mut: IComparer_1[T], k_mut: T, t_mut: SetTreeLeaf_1[T] | None) -> bool:
    while True:
        (comparer, k, t) = (comparer_mut, k_mut, t_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            c: int32 = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2))
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                if c < int32.ZERO:
                    comparer_mut = comparer
                    k_mut = k
                    t_mut = SetTreeNode_1__get_Left(tn)
                    continue

                elif c == int32.ZERO:
                    return True

                else:
                    comparer_mut = comparer
                    k_mut = k
                    t_mut = SetTreeNode_1__get_Right(tn)
                    continue

            else:
                return c == int32.ZERO

        else:
            return False

        break


def SetTreeModule_iter[T](f_mut: Callable[[T], None], t_mut: SetTreeLeaf_1[T] | None) -> None:
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                SetTreeModule_iter(f, SetTreeNode_1__get_Left(tn))
                f(SetTreeLeaf_1__get_Key(tn))
                f_mut = f
                t_mut = SetTreeNode_1__get_Right(tn)
                continue

            else:
                f(SetTreeLeaf_1__get_Key(t2))

        break


def SetTreeModule_foldBackOpt[T, _A](f_mut: Any, t_mut: SetTreeLeaf_1[T] | None, x_mut: _A) -> _A:
    while True:
        (f, t, x) = (f_mut, t_mut, x_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(tn)
                x_mut = f(SetTreeLeaf_1__get_Key(tn), SetTreeModule_foldBackOpt(f, SetTreeNode_1__get_Right(tn), x))
                continue

            else:
                return f(SetTreeLeaf_1__get_Key(t2), x)

        else:
            return x

        break


def SetTreeModule_foldBack[_A, _B](f: Callable[[_A, _B], _B], m: SetTreeLeaf_1[_A] | None, x: _B) -> _B:
    return SetTreeModule_foldBackOpt(f, m, x)


def SetTreeModule_foldOpt[_A, T](f_mut: Any, x_mut: _A, t_mut: SetTreeLeaf_1[T] | None) -> _A:
    while True:
        (f, x, t) = (f_mut, x_mut, t_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                f_mut = f
                x_mut = f(SetTreeModule_foldOpt(f, x, SetTreeNode_1__get_Left(tn)), SetTreeLeaf_1__get_Key(tn))
                t_mut = SetTreeNode_1__get_Right(tn)
                continue

            else:
                return f(x, SetTreeLeaf_1__get_Key(t2))

        else:
            return x

        break


def SetTreeModule_fold[_A, _B](f: Callable[[_A, _B], _A], x: _A, m: SetTreeLeaf_1[_B] | None = None) -> _A:
    return SetTreeModule_foldOpt(f, x, m)


def SetTreeModule_forall[T](f_mut: Callable[[T], bool], t_mut: SetTreeLeaf_1[T] | None) -> bool:
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                if SetTreeModule_forall(f, SetTreeNode_1__get_Left(tn)) if f(SetTreeLeaf_1__get_Key(tn)) else False:
                    f_mut = f
                    t_mut = SetTreeNode_1__get_Right(tn)
                    continue

                else:
                    return False

            else:
                return f(SetTreeLeaf_1__get_Key(t2))

        else:
            return True

        break


def SetTreeModule_exists[T](f_mut: Callable[[T], bool], t_mut: SetTreeLeaf_1[T] | None) -> bool:
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                if True if f(SetTreeLeaf_1__get_Key(tn)) else SetTreeModule_exists(f, SetTreeNode_1__get_Left(tn)):
                    return True

                else:
                    f_mut = f
                    t_mut = SetTreeNode_1__get_Right(tn)
                    continue

            else:
                return f(SetTreeLeaf_1__get_Key(t2))

        else:
            return False

        break


def SetTreeModule_subset[_A](
    comparer: IComparer_1[_A], a: SetTreeLeaf_1[_A] | None = None, b: SetTreeLeaf_1[_A] | None = None
) -> bool:
    def _arrow220(x: _A = UNIT, comparer: Any = comparer, b: Any = b) -> bool:
        return SetTreeModule_mem(comparer, x, b)

    return SetTreeModule_forall(_arrow220, a)


def SetTreeModule_properSubset[T](
    comparer: IComparer_1[T], a: SetTreeLeaf_1[T] | None = None, b: SetTreeLeaf_1[T] | None = None
) -> bool:
    def _arrow221(x: T = UNIT, comparer: Any = comparer, b: Any = b) -> bool:
        return SetTreeModule_mem(comparer, x, b)

    if SetTreeModule_forall(_arrow221, a):

        def _arrow222(x_1: T = UNIT, comparer: Any = comparer, a: Any = a) -> bool:
            return not SetTreeModule_mem(comparer, x_1, a)

        return SetTreeModule_exists(_arrow222, b)

    else:
        return False


def SetTreeModule_filterAux[T](
    comparer_mut: IComparer_1[T],
    f_mut: Callable[[T], bool],
    t_mut: SetTreeLeaf_1[T] | None,
    acc_mut: SetTreeLeaf_1[T] | None,
) -> SetTreeLeaf_1[T] | None:
    while True:
        (comparer, f, t, acc) = (comparer_mut, f_mut, t_mut, acc_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                acc_1: SetTreeLeaf_1[Any] | None = (
                    SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(tn), acc)
                    if f(SetTreeLeaf_1__get_Key(tn))
                    else acc
                )
                comparer_mut = comparer
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(tn)
                acc_mut = SetTreeModule_filterAux(comparer, f, SetTreeNode_1__get_Right(tn), acc_1)
                continue

            elif f(SetTreeLeaf_1__get_Key(t2)):
                return erase(SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc))

            else:
                return acc

        else:
            return acc

        break


def SetTreeModule_filter[_A](
    comparer: IComparer_1[_A], f: Callable[[_A], bool], s: SetTreeLeaf_1[_A] | None = None
) -> SetTreeLeaf_1[_A] | None:
    return erase(SetTreeModule_filterAux(comparer, f, s, SetTreeModule_empty()))


def SetTreeModule_diffAux[T](
    comparer_mut: IComparer_1[T], t_mut: SetTreeLeaf_1[T] | None, acc_mut: SetTreeLeaf_1[T] | None
) -> SetTreeLeaf_1[T] | None:
    while True:
        (comparer, t, acc) = (comparer_mut, t_mut, acc_mut)
        if acc is None:
            return acc

        elif t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                comparer_mut = comparer
                t_mut = SetTreeNode_1__get_Left(tn)
                acc_mut = SetTreeModule_diffAux(
                    comparer,
                    SetTreeNode_1__get_Right(tn),
                    SetTreeModule_remove(comparer, SetTreeLeaf_1__get_Key(tn), acc),
                )
                continue

            else:
                return erase(SetTreeModule_remove(comparer, SetTreeLeaf_1__get_Key(t2), acc))

        else:
            return acc

        break


def SetTreeModule_diff[_A](
    comparer: IComparer_1[_A], a: SetTreeLeaf_1[_A] | None = None, b: SetTreeLeaf_1[_A] | None = None
) -> SetTreeLeaf_1[_A] | None:
    return erase(SetTreeModule_diffAux(comparer, b, a))


def SetTreeModule_union[T](
    comparer: IComparer_1[T], t1: SetTreeLeaf_1[T] | None = None, t2: SetTreeLeaf_1[T] | None = None
) -> SetTreeLeaf_1[T] | None:
    if t1 is not None:
        t1_0027: SetTreeLeaf_1[Any] = t1
        if t2 is not None:
            t2_0027: SetTreeLeaf_1[Any] = t2
            if isinstance(t1_0027, SetTreeNode_1):
                t1n: SetTreeNode_1[Any] = t1_0027
                if isinstance(t2_0027, SetTreeNode_1):
                    t2n: SetTreeNode_1[Any] = t2_0027
                    if SetTreeNode_1__get_Height(t1n) > SetTreeNode_1__get_Height(t2n):
                        pattern_input: tuple[SetTreeLeaf_1[Any] | None, bool, SetTreeLeaf_1[Any] | None] = (
                            SetTreeModule_split(comparer, SetTreeLeaf_1__get_Key(t1n), t2)
                        )
                        return erase(
                            SetTreeModule_balance(
                                comparer,
                                SetTreeModule_union(comparer, SetTreeNode_1__get_Left(t1n), pattern_input[0]),
                                SetTreeLeaf_1__get_Key(t1n),
                                SetTreeModule_union(comparer, SetTreeNode_1__get_Right(t1n), pattern_input[2]),
                            )
                        )

                    else:
                        pattern_input_1: tuple[SetTreeLeaf_1[Any] | None, bool, SetTreeLeaf_1[Any] | None] = (
                            SetTreeModule_split(comparer, SetTreeLeaf_1__get_Key(t2n), t1)
                        )
                        return erase(
                            SetTreeModule_balance(
                                comparer,
                                SetTreeModule_union(comparer, SetTreeNode_1__get_Left(t2n), pattern_input_1[0]),
                                SetTreeLeaf_1__get_Key(t2n),
                                SetTreeModule_union(comparer, SetTreeNode_1__get_Right(t2n), pattern_input_1[2]),
                            )
                        )

                else:
                    return erase(SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2_0027), t1))

            else:
                return erase(SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t1_0027), t2))

        else:
            return t1

    else:
        return t2


def SetTreeModule_intersectionAux[T](
    comparer_mut: IComparer_1[T],
    b_mut: SetTreeLeaf_1[T] | None,
    t_mut: SetTreeLeaf_1[T] | None,
    acc_mut: SetTreeLeaf_1[T] | None,
) -> SetTreeLeaf_1[T] | None:
    while True:
        (comparer, b, t, acc) = (comparer_mut, b_mut, t_mut, acc_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                acc_1: SetTreeLeaf_1[Any] | None = erase(
                    SetTreeModule_intersectionAux(comparer, b, SetTreeNode_1__get_Right(tn), acc)
                )
                acc_2: SetTreeLeaf_1[Any] | None = (
                    SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(tn), acc_1)
                    if SetTreeModule_mem(comparer, SetTreeLeaf_1__get_Key(tn), b)
                    else acc_1
                )
                comparer_mut = comparer
                b_mut = b
                t_mut = SetTreeNode_1__get_Left(tn)
                acc_mut = acc_2
                continue

            elif SetTreeModule_mem(comparer, SetTreeLeaf_1__get_Key(t2), b):
                return erase(SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc))

            else:
                return acc

        else:
            return acc

        break


def SetTreeModule_intersection[_A](
    comparer: IComparer_1[_A], a: SetTreeLeaf_1[_A] | None = None, b: SetTreeLeaf_1[_A] | None = None
) -> SetTreeLeaf_1[_A] | None:
    return erase(SetTreeModule_intersectionAux(comparer, b, a, SetTreeModule_empty()))


def SetTreeModule_partition1[_A](
    comparer: IComparer_1[_A],
    f: Callable[[_A], bool],
    k: _A,
    acc1: SetTreeLeaf_1[_A] | None = None,
    acc2: SetTreeLeaf_1[_A] | None = None,
) -> tuple[SetTreeLeaf_1[_A] | None, SetTreeLeaf_1[_A] | None]:
    if f(k):
        return (SetTreeModule_add(comparer, k, acc1), acc2)

    else:
        return (acc1, SetTreeModule_add(comparer, k, acc2))


def SetTreeModule_partitionAux[T](
    comparer_mut: IComparer_1[T],
    f_mut: Callable[[T], bool],
    t_mut: SetTreeLeaf_1[T] | None,
    acc__mut: SetTreeLeaf_1[T] | None,
    acc__1_mut: SetTreeLeaf_1[T] | None,
) -> tuple[SetTreeLeaf_1[T] | None, SetTreeLeaf_1[T] | None]:
    while True:
        (comparer, f, t, acc_, acc__1) = (comparer_mut, f_mut, t_mut, acc__mut, acc__1_mut)
        acc: tuple[SetTreeLeaf_1[Any] | None, SetTreeLeaf_1[Any] | None] = (acc_, acc__1)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                acc_1: tuple[SetTreeLeaf_1[Any] | None, SetTreeLeaf_1[Any] | None] = SetTreeModule_partitionAux(
                    comparer, f, SetTreeNode_1__get_Right(tn), acc[0], acc[1]
                )
                acc_4: tuple[SetTreeLeaf_1[Any] | None, SetTreeLeaf_1[Any] | None] = SetTreeModule_partition1(
                    comparer, f, SetTreeLeaf_1__get_Key(tn), acc_1[0], acc_1[1]
                )
                comparer_mut = comparer
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(tn)
                acc__mut = acc_4[0]
                acc__1_mut = acc_4[1]
                continue

            else:
                return SetTreeModule_partition1(comparer, f, SetTreeLeaf_1__get_Key(t2), acc[0], acc[1])

        else:
            return acc

        break


def SetTreeModule_partition[_A](
    comparer: IComparer_1[_A], f: Callable[[_A], bool], s: SetTreeLeaf_1[_A] | None = None
) -> tuple[SetTreeLeaf_1[_A] | None, SetTreeLeaf_1[_A] | None]:
    return SetTreeModule_partitionAux(comparer, f, s, SetTreeModule_empty(), SetTreeModule_empty())


def SetTreeModule_minimumElementAux[T](t_mut: SetTreeLeaf_1[T] | None, n_mut: T) -> T:
    while True:
        (t, n) = (t_mut, n_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                t_mut = SetTreeNode_1__get_Left(tn)
                n_mut = SetTreeLeaf_1__get_Key(tn)
                continue

            else:
                return SetTreeLeaf_1__get_Key(t2)

        else:
            return n

        break


def SetTreeModule_minimumElementOpt[T](t: SetTreeLeaf_1[T] | None = None) -> Option[T]:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            return some(SetTreeModule_minimumElementAux(SetTreeNode_1__get_Left(tn), SetTreeLeaf_1__get_Key(tn)))

        else:
            return some(SetTreeLeaf_1__get_Key(t2))

    else:
        return None


def SetTreeModule_maximumElementAux[T](t_mut: SetTreeLeaf_1[T] | None, n_mut: T) -> T:
    while True:
        (t, n) = (t_mut, n_mut)
        if t is not None:
            t2: SetTreeLeaf_1[Any] = t
            if isinstance(t2, SetTreeNode_1):
                tn: SetTreeNode_1[Any] = t2
                t_mut = SetTreeNode_1__get_Right(tn)
                n_mut = SetTreeLeaf_1__get_Key(tn)
                continue

            else:
                return SetTreeLeaf_1__get_Key(t2)

        else:
            return n

        break


def SetTreeModule_maximumElementOpt[T](t: SetTreeLeaf_1[T] | None = None) -> Option[T]:
    if t is not None:
        t2: SetTreeLeaf_1[Any] = t
        if isinstance(t2, SetTreeNode_1):
            tn: SetTreeNode_1[Any] = t2
            return some(SetTreeModule_maximumElementAux(SetTreeNode_1__get_Right(tn), SetTreeLeaf_1__get_Key(tn)))

        else:
            return some(SetTreeLeaf_1__get_Key(t2))

    else:
        return None


def SetTreeModule_minimumElement[_A](s: SetTreeLeaf_1[_A] | None = None) -> _A:
    match_value: Option[Any] = SetTreeModule_minimumElementOpt(s)
    if match_value is None:
        raise Exception("Set contains no elements")

    else:
        return value_1(match_value)


def SetTreeModule_maximumElement[_A](s: SetTreeLeaf_1[_A] | None = None) -> _A:
    match_value: Option[Any] = SetTreeModule_maximumElementOpt(s)
    if match_value is None:
        raise Exception("Set contains no elements")

    else:
        return value_1(match_value)


def _expr223(gen0: TypeInfo) -> TypeInfo:
    return record_type(
        "Set.SetTreeModule.SetIterator`1",
        Array([gen0]),
        SetTreeModule_SetIterator_1,
        lambda: [("stack_", list_type(option_type(SetTreeLeaf_1_reflection(gen0)))), ("started_", bool_type)],
    )


@dataclass(eq=False, repr=False, slots=True)
class SetTreeModule_SetIterator_1[T](Record):
    stack_: FSharpList[SetTreeLeaf_1[Any] | None]
    started_: bool

    def __hash__(self) -> int:
        return int(self.GetHashCode())


SetTreeModule_SetIterator_1_reflection = _expr223


def SetTreeModule_collapseLHS[T](stack_mut: FSharpList[SetTreeLeaf_1[T] | None]) -> FSharpList[SetTreeLeaf_1[T] | None]:
    while True:
        (stack,) = (stack_mut,)
        if not is_empty_1(stack):
            x = head(stack)
            rest = tail(stack)
            if x is not None:
                x2: SetTreeLeaf_1[Any] = x
                if isinstance(x2, SetTreeNode_1):
                    xn: SetTreeNode_1[Any] = x2
                    stack_mut = of_array_with_tail(
                        Array[Any](
                            [
                                SetTreeNode_1__get_Left(xn),
                                SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(xn)),
                                SetTreeNode_1__get_Right(xn),
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


def SetTreeModule_mkIterator[_A](s: SetTreeLeaf_1[_A] | None = None) -> SetTreeModule_SetIterator_1[_A]:
    return SetTreeModule_SetIterator_1(SetTreeModule_collapseLHS(singleton_1(s)), False)


def SetTreeModule_notStarted[_A](__unit: Unit = UNIT) -> _A:
    raise Exception("Enumeration not started")


def SetTreeModule_alreadyFinished[_A](__unit: Unit = UNIT) -> _A:
    raise Exception("Enumeration already started")


def SetTreeModule_current[_A](i: SetTreeModule_SetIterator_1[_A]) -> _A:
    if i.started_:
        match_value: FSharpList[SetTreeLeaf_1[Any] | None] = i.stack_
        if is_empty_1(match_value):
            return SetTreeModule_alreadyFinished()

        elif head(match_value) is not None:
            t: SetTreeLeaf_1[Any] = value_1(head(match_value))
            return SetTreeLeaf_1__get_Key(t)

        else:
            raise Exception("Please report error: Set iterator, unexpected stack for current")

    else:
        return SetTreeModule_notStarted()


def SetTreeModule_moveNext[T](i: SetTreeModule_SetIterator_1[T]) -> bool:
    if i.started_:
        match_value: FSharpList[SetTreeLeaf_1[Any] | None] = i.stack_
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                t: SetTreeLeaf_1[Any] = value_1(head(match_value))
                if isinstance(t, SetTreeNode_1):
                    raise Exception("Please report error: Set iterator, unexpected stack for moveNext")

                else:
                    i.stack_ = SetTreeModule_collapseLHS(tail(match_value))
                    return not is_empty_1(i.stack_)

            else:
                raise Exception("Please report error: Set iterator, unexpected stack for moveNext")

        else:
            return False

    else:
        i.started_ = True
        return not is_empty_1(i.stack_)


def SetTreeModule_mkIEnumerator[A](s: SetTreeLeaf_1[A] | None = None) -> IEnumerator[A]:
    i: SetTreeModule_SetIterator_1[Any] = SetTreeModule_mkIterator(s)

    class ObjectExpr224(EnumeratorBase[Any], DisposableBase):
        def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: Unit = UNIT) -> A:
            return SetTreeModule_current(i)

        def System_Collections_IEnumerator_get_Current(self, __unit: Unit = UNIT) -> Any:
            return SetTreeModule_current(i)

        def System_Collections_IEnumerator_MoveNext(self, __unit: Unit = UNIT) -> bool:
            return SetTreeModule_moveNext(i)

        def System_Collections_IEnumerator_Reset(self, s: Any = s) -> None:
            nonlocal i
            i = SetTreeModule_mkIterator(s)

        def Dispose(self, __unit: Unit = UNIT) -> None:
            pass

    return ObjectExpr224()


def SetTreeModule_compareStacks[T](
    comparer_mut: IComparer_1[T],
    l1_mut: FSharpList[SetTreeLeaf_1[T] | None],
    l2_mut: FSharpList[SetTreeLeaf_1[T] | None],
) -> int32:
    """Set comparison.  Note this can be expensive."""
    while True:
        (comparer, l1, l2) = (comparer_mut, l1_mut, l2_mut)
        if not is_empty_1(l1):
            if not is_empty_1(l2):
                if head(l2) is not None:
                    if head(l1) is not None:
                        t1_5 = tail(l1)
                        t2_5 = tail(l2)
                        x1_3: SetTreeLeaf_1[Any] = value_1(head(l1))
                        x2_3: SetTreeLeaf_1[Any] = value_1(head(l2))
                        if isinstance(x1_3, SetTreeNode_1):
                            x1n_2: SetTreeNode_1[Any] = x1_3
                            if SetTreeNode_1__get_Left(x1n_2) is None:
                                if isinstance(x2_3, SetTreeNode_1):
                                    x2n_2: SetTreeNode_1[Any] = x2_3
                                    if SetTreeNode_1__get_Left(x2n_2) is None:
                                        c: int32 = comparer.Compare(
                                            SetTreeLeaf_1__get_Key(x1n_2), SetTreeLeaf_1__get_Key(x2n_2)
                                        )
                                        if c != int32.ZERO:
                                            return c

                                        else:
                                            comparer_mut = comparer
                                            l1_mut = cons(SetTreeNode_1__get_Right(x1n_2), t1_5)
                                            l2_mut = cons(SetTreeNode_1__get_Right(x2n_2), t2_5)
                                            continue

                                    else:
                                        (pattern_matching_result, t1_6, x1_4, t2_6, x2_4) = nullable[
                                            int32,
                                            FSharpList[SetTreeLeaf_1[Any] | None],
                                            SetTreeLeaf_1[Any],
                                            FSharpList[SetTreeLeaf_1[Any] | None],
                                            SetTreeLeaf_1[Any],
                                        ]()
                                        if not is_empty_1(l1):
                                            if head(l1) is not None:
                                                pattern_matching_result = int32(0)
                                                t1_6 = tail(l1)
                                                x1_4 = value_1(head(l1))

                                            elif not is_empty_1(l2):
                                                if head(l2) is not None:
                                                    pattern_matching_result = int32(1)
                                                    t2_6 = tail(l2)
                                                    x2_4 = value_1(head(l2))

                                                else:
                                                    pattern_matching_result = int32(2)

                                            else:
                                                pattern_matching_result = int32(2)

                                        elif not is_empty_1(l2):
                                            if head(l2) is not None:
                                                pattern_matching_result = int32(1)
                                                t2_6 = tail(l2)
                                                x2_4 = value_1(head(l2))

                                            else:
                                                pattern_matching_result = int32(2)

                                        else:
                                            pattern_matching_result = int32(2)

                                        if pattern_matching_result == int32.ZERO:
                                            if isinstance(x1_4, SetTreeNode_1):
                                                x1n_3: SetTreeNode_1[Any] = x1_4
                                                comparer_mut = comparer
                                                l1_mut = of_array_with_tail(
                                                    Array[Any](
                                                        [
                                                            SetTreeNode_1__get_Left(x1n_3),
                                                            SetTreeNode_1__ctor_5F465FC9(
                                                                SetTreeLeaf_1__get_Key(x1n_3),
                                                                SetTreeModule_empty(),
                                                                SetTreeNode_1__get_Right(x1n_3),
                                                                int32.ZERO,
                                                            ),
                                                        ]
                                                    ),
                                                    t1_6,
                                                )
                                                l2_mut = l2
                                                continue

                                            else:
                                                comparer_mut = comparer
                                                l1_mut = of_array_with_tail(
                                                    Array[Any](
                                                        [
                                                            SetTreeModule_empty(),
                                                            SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_4)),
                                                        ]
                                                    ),
                                                    t1_6,
                                                )
                                                l2_mut = l2
                                                continue

                                        elif pattern_matching_result == int32.ONE:
                                            if isinstance(x2_4, SetTreeNode_1):
                                                x2n_3: SetTreeNode_1[Any] = x2_4
                                                comparer_mut = comparer
                                                l1_mut = l1
                                                l2_mut = of_array_with_tail(
                                                    Array[Any](
                                                        [
                                                            SetTreeNode_1__get_Left(x2n_3),
                                                            SetTreeNode_1__ctor_5F465FC9(
                                                                SetTreeLeaf_1__get_Key(x2n_3),
                                                                SetTreeModule_empty(),
                                                                SetTreeNode_1__get_Right(x2n_3),
                                                                int32.ZERO,
                                                            ),
                                                        ]
                                                    ),
                                                    t2_6,
                                                )
                                                continue

                                            else:
                                                comparer_mut = comparer
                                                l1_mut = l1
                                                l2_mut = of_array_with_tail(
                                                    Array[Any](
                                                        [
                                                            SetTreeModule_empty(),
                                                            SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_4)),
                                                        ]
                                                    ),
                                                    t2_6,
                                                )
                                                continue

                                        else:
                                            raise Exception("unexpected state in SetTree.compareStacks")

                                else:
                                    c_1: int32 = comparer.Compare(
                                        SetTreeLeaf_1__get_Key(x1n_2), SetTreeLeaf_1__get_Key(x2_3)
                                    )
                                    if c_1 != int32.ZERO:
                                        return c_1

                                    else:
                                        comparer_mut = comparer
                                        l1_mut = cons(SetTreeNode_1__get_Right(x1n_2), t1_5)
                                        l2_mut = cons(SetTreeModule_empty(), t2_5)
                                        continue

                            else:
                                (pattern_matching_result_1, t1_7, x1_5, t2_7, x2_5) = nullable[
                                    int32,
                                    FSharpList[SetTreeLeaf_1[Any] | None],
                                    SetTreeLeaf_1[Any],
                                    FSharpList[SetTreeLeaf_1[Any] | None],
                                    SetTreeLeaf_1[Any],
                                ]()
                                if not is_empty_1(l1):
                                    if head(l1) is not None:
                                        pattern_matching_result_1 = int32(0)
                                        t1_7 = tail(l1)
                                        x1_5 = value_1(head(l1))

                                    elif not is_empty_1(l2):
                                        if head(l2) is not None:
                                            pattern_matching_result_1 = int32(1)
                                            t2_7 = tail(l2)
                                            x2_5 = value_1(head(l2))

                                        else:
                                            pattern_matching_result_1 = int32(2)

                                    else:
                                        pattern_matching_result_1 = int32(2)

                                elif not is_empty_1(l2):
                                    if head(l2) is not None:
                                        pattern_matching_result_1 = int32(1)
                                        t2_7 = tail(l2)
                                        x2_5 = value_1(head(l2))

                                    else:
                                        pattern_matching_result_1 = int32(2)

                                else:
                                    pattern_matching_result_1 = int32(2)

                                if pattern_matching_result_1 == int32.ZERO:
                                    if isinstance(x1_5, SetTreeNode_1):
                                        x1n_4: SetTreeNode_1[Any] = x1_5
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeNode_1__get_Left(x1n_4),
                                                    SetTreeNode_1__ctor_5F465FC9(
                                                        SetTreeLeaf_1__get_Key(x1n_4),
                                                        SetTreeModule_empty(),
                                                        SetTreeNode_1__get_Right(x1n_4),
                                                        int32.ZERO,
                                                    ),
                                                ]
                                            ),
                                            t1_7,
                                        )
                                        l2_mut = l2
                                        continue

                                    else:
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeModule_empty(),
                                                    SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_5)),
                                                ]
                                            ),
                                            t1_7,
                                        )
                                        l2_mut = l2
                                        continue

                                elif pattern_matching_result_1 == int32.ONE:
                                    if isinstance(x2_5, SetTreeNode_1):
                                        x2n_4: SetTreeNode_1[Any] = x2_5
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeNode_1__get_Left(x2n_4),
                                                    SetTreeNode_1__ctor_5F465FC9(
                                                        SetTreeLeaf_1__get_Key(x2n_4),
                                                        SetTreeModule_empty(),
                                                        SetTreeNode_1__get_Right(x2n_4),
                                                        int32.ZERO,
                                                    ),
                                                ]
                                            ),
                                            t2_7,
                                        )
                                        continue

                                    else:
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeModule_empty(),
                                                    SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_5)),
                                                ]
                                            ),
                                            t2_7,
                                        )
                                        continue

                                else:
                                    raise Exception("unexpected state in SetTree.compareStacks")

                        elif isinstance(x2_3, SetTreeNode_1):
                            x2n_5: SetTreeNode_1[Any] = x2_3
                            if SetTreeNode_1__get_Left(x2n_5) is None:
                                c_2: int32 = comparer.Compare(
                                    SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2n_5)
                                )
                                if c_2 != int32.ZERO:
                                    return c_2

                                else:
                                    comparer_mut = comparer
                                    l1_mut = cons(SetTreeModule_empty(), t1_5)
                                    l2_mut = cons(SetTreeNode_1__get_Right(x2n_5), t2_5)
                                    continue

                            else:
                                (pattern_matching_result_2, t1_8, x1_6, t2_8, x2_6) = nullable[
                                    int32,
                                    FSharpList[SetTreeLeaf_1[Any] | None],
                                    SetTreeLeaf_1[Any],
                                    FSharpList[SetTreeLeaf_1[Any] | None],
                                    SetTreeLeaf_1[Any],
                                ]()
                                if not is_empty_1(l1):
                                    if head(l1) is not None:
                                        pattern_matching_result_2 = int32(0)
                                        t1_8 = tail(l1)
                                        x1_6 = value_1(head(l1))

                                    elif not is_empty_1(l2):
                                        if head(l2) is not None:
                                            pattern_matching_result_2 = int32(1)
                                            t2_8 = tail(l2)
                                            x2_6 = value_1(head(l2))

                                        else:
                                            pattern_matching_result_2 = int32(2)

                                    else:
                                        pattern_matching_result_2 = int32(2)

                                elif not is_empty_1(l2):
                                    if head(l2) is not None:
                                        pattern_matching_result_2 = int32(1)
                                        t2_8 = tail(l2)
                                        x2_6 = value_1(head(l2))

                                    else:
                                        pattern_matching_result_2 = int32(2)

                                else:
                                    pattern_matching_result_2 = int32(2)

                                if pattern_matching_result_2 == int32.ZERO:
                                    if isinstance(x1_6, SetTreeNode_1):
                                        x1n_5: SetTreeNode_1[Any] = x1_6
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeNode_1__get_Left(x1n_5),
                                                    SetTreeNode_1__ctor_5F465FC9(
                                                        SetTreeLeaf_1__get_Key(x1n_5),
                                                        SetTreeModule_empty(),
                                                        SetTreeNode_1__get_Right(x1n_5),
                                                        int32.ZERO,
                                                    ),
                                                ]
                                            ),
                                            t1_8,
                                        )
                                        l2_mut = l2
                                        continue

                                    else:
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeModule_empty(),
                                                    SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_6)),
                                                ]
                                            ),
                                            t1_8,
                                        )
                                        l2_mut = l2
                                        continue

                                elif pattern_matching_result_2 == int32.ONE:
                                    if isinstance(x2_6, SetTreeNode_1):
                                        x2n_6: SetTreeNode_1[Any] = x2_6
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeNode_1__get_Left(x2n_6),
                                                    SetTreeNode_1__ctor_5F465FC9(
                                                        SetTreeLeaf_1__get_Key(x2n_6),
                                                        SetTreeModule_empty(),
                                                        SetTreeNode_1__get_Right(x2n_6),
                                                        int32.ZERO,
                                                    ),
                                                ]
                                            ),
                                            t2_8,
                                        )
                                        continue

                                    else:
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail(
                                            Array[Any](
                                                [
                                                    SetTreeModule_empty(),
                                                    SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_6)),
                                                ]
                                            ),
                                            t2_8,
                                        )
                                        continue

                                else:
                                    raise Exception("unexpected state in SetTree.compareStacks")

                        else:
                            c_3: int32 = comparer.Compare(SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2_3))
                            if c_3 != int32.ZERO:
                                return c_3

                            else:
                                comparer_mut = comparer
                                l1_mut = t1_5
                                l2_mut = t2_5
                                continue

                    else:
                        x2: SetTreeLeaf_1[Any] = value_1(head(l2))
                        (pattern_matching_result_3, t1_2, x1, t2_2, x2_1) = nullable[
                            int32,
                            FSharpList[SetTreeLeaf_1[Any] | None],
                            SetTreeLeaf_1[Any],
                            FSharpList[SetTreeLeaf_1[Any] | None],
                            SetTreeLeaf_1[Any],
                        ]()
                        if not is_empty_1(l1):
                            if head(l1) is not None:
                                pattern_matching_result_3 = int32(0)
                                t1_2 = tail(l1)
                                x1 = value_1(head(l1))

                            elif not is_empty_1(l2):
                                if head(l2) is not None:
                                    pattern_matching_result_3 = int32(1)
                                    t2_2 = tail(l2)
                                    x2_1 = value_1(head(l2))

                                else:
                                    pattern_matching_result_3 = int32(2)

                            else:
                                pattern_matching_result_3 = int32(2)

                        elif not is_empty_1(l2):
                            if head(l2) is not None:
                                pattern_matching_result_3 = int32(1)
                                t2_2 = tail(l2)
                                x2_1 = value_1(head(l2))

                            else:
                                pattern_matching_result_3 = int32(2)

                        else:
                            pattern_matching_result_3 = int32(2)

                        if pattern_matching_result_3 == int32.ZERO:
                            if isinstance(x1, SetTreeNode_1):
                                x1n: SetTreeNode_1[Any] = x1
                                comparer_mut = comparer
                                l1_mut = of_array_with_tail(
                                    Array[Any](
                                        [
                                            SetTreeNode_1__get_Left(x1n),
                                            SetTreeNode_1__ctor_5F465FC9(
                                                SetTreeLeaf_1__get_Key(x1n),
                                                SetTreeModule_empty(),
                                                SetTreeNode_1__get_Right(x1n),
                                                int32.ZERO,
                                            ),
                                        ]
                                    ),
                                    t1_2,
                                )
                                l2_mut = l2
                                continue

                            else:
                                comparer_mut = comparer
                                l1_mut = of_array_with_tail(
                                    Array[Any](
                                        [SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1))]
                                    ),
                                    t1_2,
                                )
                                l2_mut = l2
                                continue

                        elif pattern_matching_result_3 == int32.ONE:
                            if isinstance(x2_1, SetTreeNode_1):
                                x2n: SetTreeNode_1[Any] = x2_1
                                comparer_mut = comparer
                                l1_mut = l1
                                l2_mut = of_array_with_tail(
                                    Array[Any](
                                        [
                                            SetTreeNode_1__get_Left(x2n),
                                            SetTreeNode_1__ctor_5F465FC9(
                                                SetTreeLeaf_1__get_Key(x2n),
                                                SetTreeModule_empty(),
                                                SetTreeNode_1__get_Right(x2n),
                                                int32.ZERO,
                                            ),
                                        ]
                                    ),
                                    t2_2,
                                )
                                continue

                            else:
                                comparer_mut = comparer
                                l1_mut = l1
                                l2_mut = of_array_with_tail(
                                    Array[Any](
                                        [SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_1))]
                                    ),
                                    t2_2,
                                )
                                continue

                        else:
                            raise Exception("unexpected state in SetTree.compareStacks")

                elif head(l1) is not None:
                    x1_1: SetTreeLeaf_1[Any] = value_1(head(l1))
                    (pattern_matching_result_4, t1_4, x1_2, t2_4, x2_2) = nullable[
                        int32,
                        FSharpList[SetTreeLeaf_1[Any] | None],
                        SetTreeLeaf_1[Any],
                        FSharpList[SetTreeLeaf_1[Any] | None],
                        SetTreeLeaf_1[Any],
                    ]()
                    if not is_empty_1(l1):
                        if head(l1) is not None:
                            pattern_matching_result_4 = int32(0)
                            t1_4 = tail(l1)
                            x1_2 = value_1(head(l1))

                        elif not is_empty_1(l2):
                            if head(l2) is not None:
                                pattern_matching_result_4 = int32(1)
                                t2_4 = tail(l2)
                                x2_2 = value_1(head(l2))

                            else:
                                pattern_matching_result_4 = int32(2)

                        else:
                            pattern_matching_result_4 = int32(2)

                    elif not is_empty_1(l2):
                        if head(l2) is not None:
                            pattern_matching_result_4 = int32(1)
                            t2_4 = tail(l2)
                            x2_2 = value_1(head(l2))

                        else:
                            pattern_matching_result_4 = int32(2)

                    else:
                        pattern_matching_result_4 = int32(2)

                    if pattern_matching_result_4 == int32.ZERO:
                        if isinstance(x1_2, SetTreeNode_1):
                            x1n_1: SetTreeNode_1[Any] = x1_2
                            comparer_mut = comparer
                            l1_mut = of_array_with_tail(
                                Array[Any](
                                    [
                                        SetTreeNode_1__get_Left(x1n_1),
                                        SetTreeNode_1__ctor_5F465FC9(
                                            SetTreeLeaf_1__get_Key(x1n_1),
                                            SetTreeModule_empty(),
                                            SetTreeNode_1__get_Right(x1n_1),
                                            int32.ZERO,
                                        ),
                                    ]
                                ),
                                t1_4,
                            )
                            l2_mut = l2
                            continue

                        else:
                            comparer_mut = comparer
                            l1_mut = of_array_with_tail(
                                Array[Any](
                                    [SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_2))]
                                ),
                                t1_4,
                            )
                            l2_mut = l2
                            continue

                    elif pattern_matching_result_4 == int32.ONE:
                        if isinstance(x2_2, SetTreeNode_1):
                            x2n_1: SetTreeNode_1[Any] = x2_2
                            comparer_mut = comparer
                            l1_mut = l1
                            l2_mut = of_array_with_tail(
                                Array[Any](
                                    [
                                        SetTreeNode_1__get_Left(x2n_1),
                                        SetTreeNode_1__ctor_5F465FC9(
                                            SetTreeLeaf_1__get_Key(x2n_1),
                                            SetTreeModule_empty(),
                                            SetTreeNode_1__get_Right(x2n_1),
                                            int32.ZERO,
                                        ),
                                    ]
                                ),
                                t2_4,
                            )
                            continue

                        else:
                            comparer_mut = comparer
                            l1_mut = l1
                            l2_mut = of_array_with_tail(
                                Array[Any](
                                    [SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_2))]
                                ),
                                t2_4,
                            )
                            continue

                    else:
                        raise Exception("unexpected state in SetTree.compareStacks")

                else:
                    comparer_mut = comparer
                    l1_mut = tail(l1)
                    l2_mut = tail(l2)
                    continue

            else:
                return int32.ONE

        elif is_empty_1(l2):
            return int32.ZERO

        else:
            return int32.NEG_ONE

        break


def SetTreeModule_compare[T](
    comparer: IComparer_1[T], t1: SetTreeLeaf_1[T] | None = None, t2: SetTreeLeaf_1[T] | None = None
) -> int32:
    if t1 is None:
        if t2 is None:
            return int32.ZERO

        else:
            return int32.NEG_ONE

    elif t2 is None:
        return int32.ONE

    else:
        return SetTreeModule_compareStacks(comparer, singleton_1(t1), singleton_1(t2))


def SetTreeModule_choose[_A](s: SetTreeLeaf_1[_A] | None = None) -> _A:
    return SetTreeModule_minimumElement(s)


def SetTreeModule_toList[T](t: SetTreeLeaf_1[T] | None = None) -> FSharpList[T]:
    def loop(t_0027_mut: SetTreeLeaf_1[T] | None, acc_mut: FSharpList[T]) -> FSharpList[T]:
        while True:
            (t_0027, acc) = (t_0027_mut, acc_mut)
            if t_0027 is not None:
                t2: SetTreeLeaf_1[Any] = t_0027
                if isinstance(t2, SetTreeNode_1):
                    tn: SetTreeNode_1[Any] = t2
                    t_0027_mut = SetTreeNode_1__get_Left(tn)
                    acc_mut = cons(SetTreeLeaf_1__get_Key(tn), loop(SetTreeNode_1__get_Right(tn), acc))
                    continue

                else:
                    return cons(SetTreeLeaf_1__get_Key(t2), acc)

            else:
                return acc

            break

    return loop(t, empty_1())


def SetTreeModule_copyToArray[_A](s: SetTreeLeaf_1[_A] | None, arr: Array[_A], i: int32) -> None:
    j: int32 = i

    def _arrow225(x: _A = UNIT, arr: Any = arr) -> None:
        nonlocal j
        arr[j] = x
        j = j + int32.ONE

    SetTreeModule_iter(_arrow225, s)


def SetTreeModule_toArray[_A](s: SetTreeLeaf_1[_A] | None = None) -> Array[_A]:
    res: Array[Any] = zero_create(SetTreeModule_count(s), cast(Any, None))
    SetTreeModule_copyToArray(s, res, int32.ZERO)
    return res


def SetTreeModule_mkFromEnumerator[_A](
    comparer_mut: IComparer_1[_A], acc_mut: SetTreeLeaf_1[_A] | None, e_mut: IEnumerator[_A]
) -> SetTreeLeaf_1[_A] | None:
    while True:
        (comparer, acc, e) = (comparer_mut, acc_mut, e_mut)
        if e.System_Collections_IEnumerator_MoveNext():
            comparer_mut = comparer
            acc_mut = SetTreeModule_add(comparer, e.System_Collections_Generic_IEnumerator_1_get_Current(), acc)
            e_mut = e
            continue

        else:
            return acc

        break


def SetTreeModule_ofArray[_A](comparer: IComparer_1[_A], l: Array[_A]) -> SetTreeLeaf_1[_A] | None:
    def _arrow226(acc: SetTreeLeaf_1[_A] | None, k: _A, comparer: Any = comparer) -> SetTreeLeaf_1[_A] | None:
        return erase(SetTreeModule_add(comparer, k, acc))

    return erase(fold_1(_arrow226, SetTreeModule_empty(), l))


def SetTreeModule_ofList[_A](comparer: IComparer_1[_A], l: FSharpList[_A]) -> SetTreeLeaf_1[_A] | None:
    def _arrow227(acc: SetTreeLeaf_1[_A] | None, k: _A, comparer: Any = comparer) -> SetTreeLeaf_1[_A] | None:
        return erase(SetTreeModule_add(comparer, k, acc))

    return erase(fold_2(_arrow227, SetTreeModule_empty(), l))


def SetTreeModule_ofSeq[T](comparer: IComparer_1[T], c: IEnumerable_1[T]) -> SetTreeLeaf_1[T] | None:
    if isinstance(c, Array):
        return erase(SetTreeModule_ofArray(comparer, c))

    elif isinstance(c, FSharpList):
        return erase(SetTreeModule_ofList(comparer, c))

    else:
        with Disposable(get_enumerator(c)) as ie:
            return erase(SetTreeModule_mkFromEnumerator(comparer, SetTreeModule_empty(), ie))


def _expr229(gen0: TypeInfo) -> TypeInfo:
    return class_type("Set.FSharpSet", Array([gen0]), FSharpSet)


class FSharpSet[T](Set[Any], StringableBase, ComparableBase, EquatableBase, EnumerableBase[Any]):
    def __init__(self, comparer: IComparer_1[T], tree: SetTreeLeaf_1[T] | None = None) -> None:
        self.comparer: IComparer_1[Any] = comparer
        self.tree: SetTreeLeaf_1[Any] | None = tree

    def GetHashCode(self, __unit: Unit = UNIT) -> int32:
        this: FSharpSet[Any] = self
        return FSharpSet__ComputeHashCode(this)

    def Equals(self, other: Any = None) -> bool:
        this: FSharpSet[Any] = self
        return (
            (
                SetTreeModule_compare(
                    FSharpSet__get_Comparer(this), FSharpSet__get_Tree(this), FSharpSet__get_Tree(other)
                )
                == int32.ZERO
            )
            if isinstance(other, FSharpSet)
            else False
        )

    def ToString(self, __unit: Unit = UNIT) -> str:
        this: FSharpSet[Any] = self
        return ("set [" + join("; ", this)) + "]"

    def CompareTo(self, other: Any = None) -> int32:
        this: FSharpSet[Any] = self
        return (
            SetTreeModule_compare(FSharpSet__get_Comparer(this), FSharpSet__get_Tree(this), FSharpSet__get_Tree(other))
            if isinstance(other, FSharpSet)
            else int32.ONE
        )

    def System_Collections_Generic_ICollection_1_Add2B595(self, x: T = UNIT) -> None:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("ReadOnlyCollection")

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: Unit = UNIT) -> None:
        raise NotSupportedException__ctor_Z721C83C5("ReadOnlyCollection")

    def System_Collections_Generic_ICollection_1_Remove2B595(self, x: T = UNIT) -> bool:
        ignore(x)
        raise NotSupportedException__ctor_Z721C83C5("ReadOnlyCollection")

    def System_Collections_Generic_ICollection_1_Contains2B595(self, x: T = UNIT) -> bool:
        s: FSharpSet[Any] = self
        return SetTreeModule_mem(FSharpSet__get_Comparer(s), x, FSharpSet__get_Tree(s))

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, arr: Array[T], i: int32) -> None:
        s: FSharpSet[Any] = self
        SetTreeModule_copyToArray(FSharpSet__get_Tree(s), arr, i)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: Unit = UNIT) -> bool:
        return True

    def System_Collections_Generic_ICollection_1_get_Count(self, __unit: Unit = UNIT) -> int32:
        s: FSharpSet[Any] = self
        return FSharpSet__get_Count(s)

    def System_Collections_Generic_IReadOnlyCollection_1_get_Count(self, __unit: Unit = UNIT) -> int32:
        s: FSharpSet[Any] = self
        return FSharpSet__get_Count(s)

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        s: FSharpSet[Any] = self
        return SetTreeModule_mkIEnumerator(FSharpSet__get_Tree(s))

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        s: FSharpSet[Any] = self
        return SetTreeModule_mkIEnumerator(FSharpSet__get_Tree(s))

    def Contains(self, value: T = UNIT) -> bool:
        this: FSharpSet[Any] = self
        return FSharpSet__Contains(this, value)

    @property
    def Count(self, __unit: Unit = UNIT) -> int32:
        this: FSharpSet[Any] = self
        return FSharpSet__get_Count(this)

    def __contains__(self, item):
        return self.Contains(item)

    def __len__(self):
        return self.Count

    def __iter__(self):
        return to_iterator(self.GetEnumerator())


FSharpSet_reflection = _expr229


def FSharpSet__ctor[T](comparer: IComparer_1[T], tree: SetTreeLeaf_1[T] | None = None) -> FSharpSet[T]:
    return FSharpSet(comparer, tree)


def FSharpSet__get_Comparer[T](set_1: FSharpSet[T]) -> IComparer_1[T]:
    return set_1.comparer


def FSharpSet__get_Tree[T](set_1: FSharpSet[T]) -> SetTreeLeaf_1[T] | None:
    return set_1.tree


def FSharpSet_Empty[T](comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet__ctor(comparer, SetTreeModule_empty())


def FSharpSet__Add[T](s: FSharpSet[T], value: T) -> FSharpSet[T]:
    return FSharpSet__ctor(
        FSharpSet__get_Comparer(s), SetTreeModule_add(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s))
    )


def FSharpSet__Remove[T](s: FSharpSet[T], value: T) -> FSharpSet[T]:
    return FSharpSet__ctor(
        FSharpSet__get_Comparer(s), SetTreeModule_remove(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s))
    )


def FSharpSet__get_Count[T](s: FSharpSet[T]) -> int32:
    return SetTreeModule_count(FSharpSet__get_Tree(s))


def FSharpSet__Contains[T](s: FSharpSet[T], value: T) -> bool:
    return SetTreeModule_mem(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s))


def FSharpSet__Iterate[T](s: FSharpSet[T], x: Callable[[T], None]) -> None:
    SetTreeModule_iter(x, FSharpSet__get_Tree(s))


def FSharpSet__Fold[_A, T](s: FSharpSet[T], f: Callable[[T, _A], _A], z: _A) -> _A:
    f_1: Any = f

    def _arrow237(x: _A, z_1: T) -> _A:
        return f_1(z_1, x)

    return SetTreeModule_fold(_arrow237, z, FSharpSet__get_Tree(s))


def FSharpSet__get_IsEmpty[T](s: FSharpSet[T]) -> bool:
    return FSharpSet__get_Tree(s) is None


def FSharpSet__Partition[T](s: FSharpSet[T], f: Callable[[T], bool]) -> tuple[FSharpSet[T], FSharpSet[T]]:
    if FSharpSet__get_Tree(s) is None:
        return (s, s)

    else:
        pattern_input: tuple[SetTreeLeaf_1[Any] | None, SetTreeLeaf_1[Any] | None] = SetTreeModule_partition(
            FSharpSet__get_Comparer(s), f, FSharpSet__get_Tree(s)
        )
        return (
            FSharpSet__ctor(FSharpSet__get_Comparer(s), pattern_input[0]),
            FSharpSet__ctor(FSharpSet__get_Comparer(s), pattern_input[1]),
        )


def FSharpSet__Filter[T](s: FSharpSet[T], f: Callable[[T], bool]) -> FSharpSet[T]:
    if FSharpSet__get_Tree(s) is None:
        return s

    else:
        return FSharpSet__ctor(
            FSharpSet__get_Comparer(s), SetTreeModule_filter(FSharpSet__get_Comparer(s), f, FSharpSet__get_Tree(s))
        )


def FSharpSet__Map[U, T](s: FSharpSet[T], f: Callable[[T], U], comparer: IComparer_1[U]) -> FSharpSet[U]:
    def _arrow240(acc: SetTreeLeaf_1[U] | None, k: T, f: Any = f, comparer: Any = comparer) -> SetTreeLeaf_1[U] | None:
        return erase(SetTreeModule_add(comparer, f(k), acc))

    return FSharpSet__ctor(comparer, SetTreeModule_fold(_arrow240, SetTreeModule_empty(), FSharpSet__get_Tree(s)))


def FSharpSet__Exists[T](s: FSharpSet[T], f: Callable[[T], bool]) -> bool:
    return SetTreeModule_exists(f, FSharpSet__get_Tree(s))


def FSharpSet__ForAll[T](s: FSharpSet[T], f: Callable[[T], bool]) -> bool:
    return SetTreeModule_forall(f, FSharpSet__get_Tree(s))


def FSharpSet_op_Subtraction[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> FSharpSet[T]:
    if FSharpSet__get_Tree(set1) is None:
        return set1

    elif FSharpSet__get_Tree(set2) is None:
        return set1

    else:
        return FSharpSet__ctor(
            FSharpSet__get_Comparer(set1),
            SetTreeModule_diff(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2)),
        )


def FSharpSet_op_Addition[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> FSharpSet[T]:
    if FSharpSet__get_Tree(set2) is None:
        return set1

    elif FSharpSet__get_Tree(set1) is None:
        return set2

    else:
        return FSharpSet__ctor(
            FSharpSet__get_Comparer(set1),
            SetTreeModule_union(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2)),
        )


def FSharpSet_Intersection[T](a: FSharpSet[T], b: FSharpSet[T]) -> FSharpSet[T]:
    if FSharpSet__get_Tree(b) is None:
        return b

    elif FSharpSet__get_Tree(a) is None:
        return a

    else:
        return FSharpSet__ctor(
            FSharpSet__get_Comparer(a),
            SetTreeModule_intersection(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b)),
        )


def FSharpSet_IntersectionMany[T](sets: IEnumerable_1[FSharpSet[T]]) -> FSharpSet[T]:
    return reduce(FSharpSet_Intersection, sets)


def FSharpSet_Equality[T](a: FSharpSet[T], b: FSharpSet[T]) -> bool:
    return (
        SetTreeModule_compare(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b)) == int32.ZERO
    )


def FSharpSet_Compare[T](a: FSharpSet[T], b: FSharpSet[T]) -> int32:
    return SetTreeModule_compare(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b))


def FSharpSet__get_Choose[T](x: FSharpSet[T]) -> T:
    return SetTreeModule_choose(FSharpSet__get_Tree(x))


def FSharpSet__get_MinimumElement[T](x: FSharpSet[T]) -> T:
    return SetTreeModule_minimumElement(FSharpSet__get_Tree(x))


def FSharpSet__get_MaximumElement[T](x: FSharpSet[T]) -> T:
    return SetTreeModule_maximumElement(FSharpSet__get_Tree(x))


def FSharpSet__IsSubsetOf[T](x: FSharpSet[T], other_set: FSharpSet[T]) -> bool:
    return SetTreeModule_subset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(x), FSharpSet__get_Tree(other_set))


def FSharpSet__IsSupersetOf[T](x: FSharpSet[T], other_set: FSharpSet[T]) -> bool:
    return SetTreeModule_subset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(other_set), FSharpSet__get_Tree(x))


def FSharpSet__IsProperSubsetOf[T](x: FSharpSet[T], other_set: FSharpSet[T]) -> bool:
    return SetTreeModule_properSubset(
        FSharpSet__get_Comparer(x), FSharpSet__get_Tree(x), FSharpSet__get_Tree(other_set)
    )


def FSharpSet__IsProperSupersetOf[T](x: FSharpSet[T], other_set: FSharpSet[T]) -> bool:
    return SetTreeModule_properSubset(
        FSharpSet__get_Comparer(x), FSharpSet__get_Tree(other_set), FSharpSet__get_Tree(x)
    )


def FSharpSet__ToList[T](x: FSharpSet[T]) -> FSharpList[T]:
    return SetTreeModule_toList(FSharpSet__get_Tree(x))


def FSharpSet__ToArray[T](x: FSharpSet[T]) -> Array[T]:
    return SetTreeModule_toArray(FSharpSet__get_Tree(x))


def FSharpSet__ComputeHashCode[T](this: FSharpSet[T]) -> int32:
    res: int32 = int32.ZERO
    with Disposable(get_enumerator(this)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            x_1: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            res = ((res << int32.ONE) + structural_hash(x_1)) + int32(631)
    return abs(res)


def is_empty[T](set_1: FSharpSet[T]) -> bool:
    return FSharpSet__get_IsEmpty(set_1)


def contains[T](element: T, set_1: FSharpSet[T]) -> bool:
    return FSharpSet__Contains(set_1, element)


def add[T](value: T, set_1: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet__Add(set_1, value)


def singleton[T](value: T, comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet__Add(FSharpSet_Empty(comparer), value)


def remove[T](value: T, set_1: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet__Remove(set_1, value)


def union[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet_op_Addition(set1, set2)


def union_many[T](sets: IEnumerable_1[FSharpSet[T]], comparer: IComparer_1[T]) -> FSharpSet[T]:
    return fold_3(FSharpSet_op_Addition, FSharpSet_Empty(comparer), sets)


def intersect[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet_Intersection(set1, set2)


def intersect_many[T](sets: IEnumerable_1[FSharpSet[T]]) -> FSharpSet[T]:
    return FSharpSet_IntersectionMany(sets)


def iterate[T](action: Callable[[T], None], set_1: FSharpSet[T]) -> None:
    FSharpSet__Iterate(set_1, action)


def empty[T](comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet_Empty(comparer)


def for_all[T](predicate: Callable[[T], bool], set_1: FSharpSet[T]) -> bool:
    return FSharpSet__ForAll(set_1, predicate)


def exists[T](predicate: Callable[[T], bool], set_1: FSharpSet[T]) -> bool:
    return FSharpSet__Exists(set_1, predicate)


def filter[T](predicate: Callable[[T], bool], set_1: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet__Filter(set_1, predicate)


def partition[T](predicate: Callable[[T], bool], set_1: FSharpSet[T]) -> tuple[FSharpSet[T], FSharpSet[T]]:
    return FSharpSet__Partition(set_1, predicate)


def fold[T, STATE](folder: Callable[[STATE, T], STATE], state: STATE, set_1: FSharpSet[T]) -> STATE:
    return SetTreeModule_fold(folder, state, FSharpSet__get_Tree(set_1))


def fold_back[T, STATE](folder: Callable[[T, STATE], STATE], set_1: FSharpSet[T], state: STATE) -> STATE:
    return SetTreeModule_foldBack(folder, FSharpSet__get_Tree(set_1), state)


def map[T, U](mapping: Callable[[T], U], set_1: FSharpSet[T], comparer: IComparer_1[U]) -> FSharpSet[U]:
    return FSharpSet__Map(set_1, mapping, comparer)


def count[T](set_1: FSharpSet[T]) -> int32:
    return FSharpSet__get_Count(set_1)


def of_list[T](elements: IEnumerable_1[T], comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet__ctor(comparer, SetTreeModule_ofSeq(comparer, elements))


def of_array[T](array: Array[T], comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet__ctor(comparer, SetTreeModule_ofArray(comparer, array))


def to_list[T](set_1: FSharpSet[T]) -> FSharpList[T]:
    return FSharpSet__ToList(set_1)


def to_array[T](set_1: FSharpSet[T]) -> Array[T]:
    return FSharpSet__ToArray(set_1)


def to_seq[T](set_1: FSharpSet[T]) -> IEnumerable_1[T]:
    def mapping(x: T = UNIT) -> T:
        return x

    return map_1(mapping, set_1)


def of_seq[T](elements: IEnumerable_1[T], comparer: IComparer_1[T]) -> FSharpSet[T]:
    return FSharpSet__ctor(comparer, SetTreeModule_ofSeq(comparer, elements))


def difference[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> FSharpSet[T]:
    return FSharpSet_op_Subtraction(set1, set2)


def is_subset[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> bool:
    return SetTreeModule_subset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2))


def is_superset[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> bool:
    return SetTreeModule_subset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set2), FSharpSet__get_Tree(set1))


def is_proper_subset[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> bool:
    return SetTreeModule_properSubset(
        FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2)
    )


def is_proper_superset[T](set1: FSharpSet[T], set2: FSharpSet[T]) -> bool:
    return SetTreeModule_properSubset(
        FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set2), FSharpSet__get_Tree(set1)
    )


def min_element[T](set_1: FSharpSet[T]) -> T:
    return FSharpSet__get_MinimumElement(set_1)


def max_element[T](set_1: FSharpSet[T]) -> T:
    return FSharpSet__get_MaximumElement(set_1)


def union_with[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> HashSet[T]:
    def action(x: T = UNIT, s1: Any = s1) -> None:
        ignore(HashSet__Add_2B595(s1, x))

    iterate_1(action, s2)
    return s1


def new_mutable_set_with[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> HashSet[T]:
    return HashSet__ctor_Z6150332D(s2, HashSet__get_Comparer(s1))


def intersect_with[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> None:
    s2_1: HashSet[Any] = new_mutable_set_with(s1, s2)

    def action(x: T = UNIT, s1: Any = s1) -> None:
        if not HashSet__Contains_2B595(s2_1, x):
            ignore(HashSet__Remove_2B595(s1, x))

    iterate_2(action, Array[Any](s1))


def except_with[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> None:
    def action(x: T = UNIT, s1: Any = s1) -> None:
        ignore(HashSet__Remove_2B595(s1, x))

    iterate_1(action, s2)


def is_subset_of[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> bool:
    s2_1: HashSet[Any] = new_mutable_set_with(s1, s2)

    def predicate(k: T = UNIT) -> bool:
        return HashSet__Contains_2B595(s2_1, k)

    return for_all_1(predicate, s1)


def is_superset_of[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> bool:
    def predicate(k: T = UNIT, s1: Any = s1) -> bool:
        return HashSet__Contains_2B595(s1, k)

    return for_all_1(predicate, s2)


def is_proper_subset_of[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> bool:
    s2_1: HashSet[Any] = new_mutable_set_with(s1, s2)
    if HashSet__get_Count(s2_1) > HashSet__get_Count(s1):

        def predicate(k: T = UNIT) -> bool:
            return HashSet__Contains_2B595(s2_1, k)

        return for_all_1(predicate, s1)

    else:
        return False


def is_proper_superset_of[T](s1: HashSet[T], s2: IEnumerable_1[T]) -> bool:
    s2_1: HashSet[Any] = new_mutable_set_with(s1, s2)
    if HashSet__get_Count(s1) > HashSet__get_Count(s2_1):

        def predicate(k: T = UNIT, s1: Any = s1) -> bool:
            return HashSet__Contains_2B595(s1, k)

        return for_all_1(predicate, s2_1)

    else:
        return False


__all__ = [
    "FSharpSet_Compare",
    "FSharpSet_Empty",
    "FSharpSet_Equality",
    "FSharpSet_Intersection",
    "FSharpSet_IntersectionMany",
    "FSharpSet__Add",
    "FSharpSet__ComputeHashCode",
    "FSharpSet__Contains",
    "FSharpSet__Exists",
    "FSharpSet__Filter",
    "FSharpSet__Fold",
    "FSharpSet__ForAll",
    "FSharpSet__IsProperSubsetOf",
    "FSharpSet__IsProperSupersetOf",
    "FSharpSet__IsSubsetOf",
    "FSharpSet__IsSupersetOf",
    "FSharpSet__Iterate",
    "FSharpSet__Map",
    "FSharpSet__Partition",
    "FSharpSet__Remove",
    "FSharpSet__ToArray",
    "FSharpSet__ToList",
    "FSharpSet__get_Choose",
    "FSharpSet__get_Comparer",
    "FSharpSet__get_Count",
    "FSharpSet__get_IsEmpty",
    "FSharpSet__get_MaximumElement",
    "FSharpSet__get_MinimumElement",
    "FSharpSet__get_Tree",
    "FSharpSet_op_Addition",
    "FSharpSet_op_Subtraction",
    "FSharpSet_reflection",
    "SetTreeLeaf_1__get_Key",
    "SetTreeLeaf_1_reflection",
    "SetTreeModule_SetIterator_1_reflection",
    "SetTreeModule_add",
    "SetTreeModule_alreadyFinished",
    "SetTreeModule_balance",
    "SetTreeModule_choose",
    "SetTreeModule_collapseLHS",
    "SetTreeModule_compare",
    "SetTreeModule_compareStacks",
    "SetTreeModule_copyToArray",
    "SetTreeModule_count",
    "SetTreeModule_countAux",
    "SetTreeModule_current",
    "SetTreeModule_diff",
    "SetTreeModule_diffAux",
    "SetTreeModule_empty",
    "SetTreeModule_exists",
    "SetTreeModule_filter",
    "SetTreeModule_filterAux",
    "SetTreeModule_fold",
    "SetTreeModule_foldBack",
    "SetTreeModule_foldBackOpt",
    "SetTreeModule_foldOpt",
    "SetTreeModule_forall",
    "SetTreeModule_intersection",
    "SetTreeModule_intersectionAux",
    "SetTreeModule_iter",
    "SetTreeModule_maximumElement",
    "SetTreeModule_maximumElementAux",
    "SetTreeModule_maximumElementOpt",
    "SetTreeModule_mem",
    "SetTreeModule_minimumElement",
    "SetTreeModule_minimumElementAux",
    "SetTreeModule_minimumElementOpt",
    "SetTreeModule_mk",
    "SetTreeModule_mkFromEnumerator",
    "SetTreeModule_mkIEnumerator",
    "SetTreeModule_mkIterator",
    "SetTreeModule_moveNext",
    "SetTreeModule_notStarted",
    "SetTreeModule_ofArray",
    "SetTreeModule_ofList",
    "SetTreeModule_ofSeq",
    "SetTreeModule_partition",
    "SetTreeModule_partition1",
    "SetTreeModule_partitionAux",
    "SetTreeModule_properSubset",
    "SetTreeModule_rebalance",
    "SetTreeModule_remove",
    "SetTreeModule_spliceOutSuccessor",
    "SetTreeModule_split",
    "SetTreeModule_subset",
    "SetTreeModule_toArray",
    "SetTreeModule_toList",
    "SetTreeModule_union",
    "SetTreeNode_1__get_Height",
    "SetTreeNode_1__get_Left",
    "SetTreeNode_1__get_Right",
    "SetTreeNode_1_reflection",
    "add",
    "contains",
    "count",
    "difference",
    "empty",
    "except_with",
    "exists",
    "filter",
    "fold",
    "fold_back",
    "for_all",
    "intersect",
    "intersect_many",
    "intersect_with",
    "is_empty",
    "is_proper_subset",
    "is_proper_subset_of",
    "is_proper_superset",
    "is_proper_superset_of",
    "is_subset",
    "is_subset_of",
    "is_superset",
    "is_superset_of",
    "iterate",
    "map",
    "max_element",
    "min_element",
    "new_mutable_set_with",
    "of_array",
    "of_list",
    "of_seq",
    "partition",
    "remove",
    "singleton",
    "to_array",
    "to_list",
    "to_seq",
    "union",
    "union_many",
    "union_with",
]
