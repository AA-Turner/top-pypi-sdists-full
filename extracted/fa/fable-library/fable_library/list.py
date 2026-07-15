from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from .array_ import Array, random_shuffle_in_place_by, sort_in_place_with, zero_create
from .array_ import chunk_by_size as chunk_by_size_1
from .array_ import fold_back as fold_back_1
from .array_ import fold_back2 as fold_back2_1
from .array_ import iterate as iterate_1
from .array_ import map as map_1
from .array_ import of_seq as of_seq_1
from .array_ import pairwise as pairwise_1
from .array_ import permute as permute_1
from .array_ import random_choice_by as random_choice_by_1
from .array_ import random_choices_by as random_choices_by_1
from .array_ import random_sample_by as random_sample_by_1
from .array_ import scan_back as scan_back_1
from .array_ import split_into as split_into_1
from .array_ import transpose as transpose_1
from .array_ import try_find_back as try_find_back_1
from .array_ import try_find_index_back as try_find_index_back_1
from .array_ import windowed as windowed_1
from .bases import DisposableBase, EnumerableBase, EnumeratorBase
from .core import float64, int32
from .exceptions import to_string
from .global_ import (
    IGenericAdder_1,
    IGenericAverager_1,
    SR_differentLengths,
    SR_indexOutOfBounds,
    SR_inputMustBeNonNegative,
    SR_inputSequenceEmpty,
    SR_inputSequenceTooLong,
    SR_inputWasEmpty,
    SR_keyNotFoundAlt,
    SR_notEnoughElements,
)
from .option import Option, default_arg, erase, some
from .option import value as value_1
from .protocols import IComparer_1, IEnumerable_1, IEnumerator, IEqualityComparer_1
from .record import Record
from .reflection import TypeInfo, class_type, option_type, record_type
from .types import ExceptionBase
from .util import (
    UNIT,
    Disposable,
    Unit,
    compare,
    create_random,
    equals,
    get_enumerator,
    ignore,
    nullable,
    random_double,
    range,
    structural_hash,
)


def _expr28(gen0: TypeInfo) -> TypeInfo:
    return record_type(
        "ListModule.FSharpList",
        Array([gen0]),
        FSharpList,
        lambda: [("head_", gen0), ("tail_", option_type(FSharpList_reflection(gen0)))],
    )


@dataclass(eq=False, repr=False, slots=True)
class FSharpList[T](Record, EnumerableBase[Any]):
    head_: Any
    tail_: FSharpList[Any] | None

    def ToString(self, __unit: Unit = UNIT) -> str:
        xs: FSharpList[Any] = self
        result: str = "["
        first: bool = True
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x_1: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()

                def _arrow27(__unit: Unit = UNIT) -> str:
                    x: Any = x_1
                    match_value: Any = x
                    return (('"' + match_value) + '"') if (str(type(match_value)) == "<class 'str'>") else to_string(x)

                result = (result if first else (result + "; ")) + _arrow27()
                first = False
        return result + "]"

    def Equals(self, other: Any = None) -> bool:
        xs: FSharpList[Any] = self
        if xs is other:
            return True

        else:

            def loop(xs_1_mut: FSharpList[T], ys_1_mut: FSharpList[T]) -> bool:
                while True:
                    (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
                    match_value: FSharpList[Any] | None = xs_1.tail_
                    match_value_1: FSharpList[Any] | None = ys_1.tail_
                    if match_value is not None:
                        if match_value_1 is not None:
                            xt: FSharpList[Any] = match_value
                            yt: FSharpList[Any] = match_value_1
                            if equals(xs_1.head_, ys_1.head_):
                                xs_1_mut = xt
                                ys_1_mut = yt
                                continue

                            else:
                                return False

                        else:
                            return False

                    elif match_value_1 is not None:
                        return False

                    else:
                        return True

                    break

            return loop(xs, other)

    def GetHashCode(self, __unit: Unit = UNIT) -> int32:
        xs: FSharpList[Any] = self

        def loop(i_mut: int32, h_mut: int32, xs_1_mut: FSharpList[T]) -> int32:
            while True:
                (i, h, xs_1) = (i_mut, h_mut, xs_1_mut)
                match_value: FSharpList[Any] | None = xs_1.tail_
                if match_value is not None:
                    t: FSharpList[Any] = match_value
                    if i > int32(18):
                        return h

                    else:
                        i_mut = i + int32.ONE
                        h_mut = ((h << int32.ONE) + structural_hash(xs_1.head_)) + (int32(631) * i)
                        xs_1_mut = t
                        continue

                else:
                    return h

                break

        return loop(int32.ZERO, int32.ZERO, xs)

    def CompareTo(self, other: Any = None) -> int32:
        xs: FSharpList[Any] = self

        def loop(xs_1_mut: FSharpList[T], ys_1_mut: FSharpList[T]) -> int32:
            while True:
                (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
                match_value: FSharpList[Any] | None = xs_1.tail_
                match_value_1: FSharpList[Any] | None = ys_1.tail_
                if match_value is not None:
                    if match_value_1 is not None:
                        xt: FSharpList[Any] = match_value
                        yt: FSharpList[Any] = match_value_1
                        c: int32 = compare(xs_1.head_, ys_1.head_)
                        if c == int32.ZERO:
                            xs_1_mut = xt
                            ys_1_mut = yt
                            continue

                        else:
                            return c

                    else:
                        return int32.ONE

                elif match_value_1 is not None:
                    return int32.NEG_ONE

                else:
                    return int32.ZERO

                break

        return loop(xs, other)

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        xs: FSharpList[Any] = self
        return ListEnumerator_1__ctor_3002E699(xs)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        xs: FSharpList[Any] = self
        return get_enumerator(xs)

    def __hash__(self) -> int:
        return int(self.GetHashCode())


FSharpList_reflection = _expr28


def _expr29(gen0: TypeInfo) -> TypeInfo:
    return class_type("ListModule.ListEnumerator`1", Array([gen0]), ListEnumerator_1)


class ListEnumerator_1[T](EnumeratorBase[Any], DisposableBase):
    def __init__(self, xs: FSharpList[T]) -> None:
        self.xs: FSharpList[Any] = xs
        self.it: FSharpList[Any] = self.xs
        self.current: Any = cast(Any, None)

    def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: Unit = UNIT) -> T:
        _: ListEnumerator_1[Any] = self
        return _.current

    def System_Collections_IEnumerator_get_Current(self, __unit: Unit = UNIT) -> Any:
        _: ListEnumerator_1[Any] = self
        return _.current

    def System_Collections_IEnumerator_MoveNext(self, __unit: Unit = UNIT) -> bool:
        _: ListEnumerator_1[Any] = self
        match_value: FSharpList[Any] | None = _.it.tail_
        if match_value is not None:
            t: FSharpList[Any] = match_value
            _.current = _.it.head_
            _.it = t
            return True

        else:
            return False

    def System_Collections_IEnumerator_Reset(self, __unit: Unit = UNIT) -> None:
        _: ListEnumerator_1[Any] = self
        _.it = _.xs
        _.current = cast(Any, None)

    def Dispose(self, __unit: Unit = UNIT) -> None:
        pass


ListEnumerator_1_reflection = _expr29


def ListEnumerator_1__ctor_3002E699[T](xs: FSharpList[T]) -> ListEnumerator_1[T]:
    return ListEnumerator_1(xs)


def FSharpList_get_Empty[T](__unit: Unit = UNIT) -> FSharpList[T]:
    return FSharpList(cast(Any, None), None)


def FSharpList_Cons_305B8EAC[T](x: T, xs: FSharpList[T]) -> FSharpList[T]:
    return FSharpList(x, xs)


def FSharpList__get_IsEmpty[T](xs: FSharpList[T]) -> bool:
    return xs.tail_ is None


def FSharpList__get_Length[T](xs: FSharpList[T]) -> int32:
    def loop(i_mut: int32, xs_1_mut: FSharpList[T]) -> int32:
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            match_value: FSharpList[Any] | None = xs_1.tail_
            if match_value is not None:
                i_mut = i + int32.ONE
                xs_1_mut = match_value
                continue

            else:
                return i

            break

    return loop(int32.ZERO, xs)


def FSharpList__get_Head[T](xs: FSharpList[T]) -> T:
    match_value: FSharpList[Any] | None = xs.tail_
    if match_value is not None:
        return xs.head_

    else:
        raise Exception(SR_inputWasEmpty + " (Parameter 'list')")


def FSharpList__get_Tail[T](xs: FSharpList[T]) -> FSharpList[T]:
    match_value: FSharpList[Any] | None = xs.tail_
    if match_value is not None:
        return match_value

    else:
        raise Exception(SR_inputWasEmpty + " (Parameter 'list')")


def FSharpList__get_Item_Z524259A4[T](xs: FSharpList[T], index: int32) -> T:
    def loop(i_mut: int32, xs_1_mut: FSharpList[T], index: Any = index) -> T:
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            match_value: FSharpList[Any] | None = xs_1.tail_
            if match_value is not None:
                if i == index:
                    return xs_1.head_

                else:
                    i_mut = i + int32.ONE
                    xs_1_mut = match_value
                    continue

            else:
                raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

            break

    return loop(int32.ZERO, xs)


def index_not_found[_A](__unit: Unit = UNIT) -> _A:
    raise ExceptionBase(SR_keyNotFoundAlt)


def empty[_A](__unit: Unit = UNIT) -> FSharpList[_A]:
    return FSharpList_get_Empty()


def cons[T](x: T, xs: FSharpList[T]) -> FSharpList[T]:
    return FSharpList_Cons_305B8EAC(x, xs)


def singleton[_A](x: _A = UNIT) -> FSharpList[_A]:
    return FSharpList_Cons_305B8EAC(x, FSharpList_get_Empty())


def is_empty[T](xs: FSharpList[T]) -> bool:
    return FSharpList__get_IsEmpty(xs)


def length[T](xs: FSharpList[T]) -> int32:
    return FSharpList__get_Length(xs)


def head[T](xs: FSharpList[T]) -> T:
    return FSharpList__get_Head(xs)


def try_head[T](xs: FSharpList[T]) -> Option[T]:
    if FSharpList__get_IsEmpty(xs):
        return None

    else:
        return some(FSharpList__get_Head(xs))


def tail[T](xs: FSharpList[T]) -> FSharpList[T]:
    return FSharpList__get_Tail(xs)


def try_last[T](xs_mut: FSharpList[T]) -> Option[T]:
    while True:
        (xs,) = (xs_mut,)
        if FSharpList__get_IsEmpty(xs):
            return None

        else:
            t: FSharpList[Any] = FSharpList__get_Tail(xs)
            if FSharpList__get_IsEmpty(t):
                return some(FSharpList__get_Head(xs))

            else:
                xs_mut = t
                continue

        break


def last[T](xs: FSharpList[T]) -> T:
    match_value: Option[Any] = try_last(xs)
    if match_value is None:
        raise Exception(SR_inputWasEmpty)

    else:
        return value_1(match_value)


def compare_with[T](comparer: Callable[[T, T], int32], xs: FSharpList[T], ys: FSharpList[T]) -> int32:
    def loop(xs_1_mut: FSharpList[T], ys_1_mut: FSharpList[T], comparer: Any = comparer) -> int32:
        while True:
            (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
            match_value: bool = FSharpList__get_IsEmpty(xs_1)
            match_value_1: bool = FSharpList__get_IsEmpty(ys_1)
            if match_value:
                if match_value_1:
                    return int32.ZERO

                else:
                    return int32.NEG_ONE

            elif match_value_1:
                return int32.ONE

            else:
                c: int32 = comparer(FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1))
                if c == int32.ZERO:
                    xs_1_mut = FSharpList__get_Tail(xs_1)
                    ys_1_mut = FSharpList__get_Tail(ys_1)
                    continue

                else:
                    return c

            break

    return loop(xs, ys)


def to_array[T](xs: FSharpList[T]) -> Array[T]:
    res: Array[Any] = zero_create(FSharpList__get_Length(xs), cast(Any, None))

    def loop(i_mut: int32, xs_1_mut: FSharpList[T]) -> None:
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if not FSharpList__get_IsEmpty(xs_1):
                res[i] = FSharpList__get_Head(xs_1)
                i_mut = i + int32.ONE
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    loop(int32.ZERO, xs)
    return res


def fold[T, STATE](folder: Callable[[STATE, T], STATE], state: STATE, xs: FSharpList[T]) -> STATE:
    acc: Any = state
    xs_1: FSharpList[Any] = xs
    while not FSharpList__get_IsEmpty(xs_1):
        acc = folder(acc, head(xs_1))
        xs_1 = FSharpList__get_Tail(xs_1)
    return acc


def reverse[T](xs: FSharpList[T]) -> FSharpList[T]:
    def _arrow30(acc: FSharpList[T], x: T) -> FSharpList[T]:
        return FSharpList_Cons_305B8EAC(x, acc)

    return fold(_arrow30, FSharpList_get_Empty(), xs)


def fold_back[T, STATE](folder: Callable[[T, STATE], STATE], xs: FSharpList[T], state: STATE) -> STATE:
    return fold_back_1(folder, to_array(xs), state)


def fold_indexed[STATE, T](folder: Callable[[int32, STATE, T], STATE], state: STATE, xs: FSharpList[T]) -> STATE:
    def loop(i_mut: int32, acc_mut: STATE, xs_1_mut: FSharpList[T], folder: Any = folder) -> STATE:
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return acc

            else:
                i_mut = i + int32.ONE
                acc_mut = folder(i, acc, FSharpList__get_Head(xs_1))
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    return loop(int32.ZERO, state, xs)


def fold2[T1, T2, STATE](
    folder: Callable[[STATE, T1, T2], STATE], state: STATE, xs: FSharpList[T1], ys: FSharpList[T2]
) -> STATE:
    acc: Any = state
    xs_1: FSharpList[Any] = xs
    ys_1: FSharpList[Any] = ys
    while (not FSharpList__get_IsEmpty(ys_1)) if (not FSharpList__get_IsEmpty(xs_1)) else False:
        acc = folder(acc, FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1))
        xs_1 = FSharpList__get_Tail(xs_1)
        ys_1 = FSharpList__get_Tail(ys_1)
    return acc


def fold_back2[T1, T2, STATE](
    folder: Callable[[T1, T2, STATE], STATE], xs: FSharpList[T1], ys: FSharpList[T2], state: STATE
) -> STATE:
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def unfold[STATE, T](generator: Callable[[STATE], tuple[T, STATE] | None], state: STATE) -> FSharpList[T]:
    def loop(acc_mut: STATE, node_mut: FSharpList[T], generator: Any = generator) -> FSharpList[T]:
        while True:
            (acc, node) = (acc_mut, node_mut)
            match_value: tuple[Any, Any] | None = erase(generator(acc))
            if match_value is not None:
                acc_mut = match_value[1]

                def _arrow31(match_value: tuple[T, STATE], node: Any = node) -> FSharpList[T]:
                    t: FSharpList[Any] = FSharpList(match_value[0], None)
                    node.tail_ = t
                    return t

                node_mut = _arrow31(match_value)
                continue

            else:
                return node

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node_1: FSharpList[Any] = loop(state, root)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node_1.tail_ = t_2
    return FSharpList__get_Tail(root)


def iterate[_A](action: Callable[[_A], None], xs: FSharpList[_A]) -> None:
    def _arrow32(unit_var: None, x: _A, action: Any = action) -> None:
        action(x)

    fold(_arrow32, None, xs)


def iterate2[_A, _B](action: Callable[[_A, _B], None], xs: FSharpList[_A], ys: FSharpList[_B]) -> None:
    def _arrow33(unit_var: None, x: _A, y: _B, action: Any = action) -> None:
        action(x, y)

    fold2(_arrow33, None, xs, ys)


def iterate_indexed[_A](action: Callable[[int32, _A], None], xs: FSharpList[_A]) -> None:
    def _arrow34(i: int32, x: _A, action: Any = action) -> int32:
        action(i, x)
        return i + int32.ONE

    ignore(fold(_arrow34, int32.ZERO, xs))


def iterate_indexed2[_A, _B](action: Callable[[int32, _A, _B], None], xs: FSharpList[_A], ys: FSharpList[_B]) -> None:
    def _arrow35(i: int32, x: _A, y: _B, action: Any = action) -> int32:
        action(i, x, y)
        return i + int32.ONE

    ignore(fold2(_arrow35, int32.ZERO, xs, ys))


def to_seq[T](xs: FSharpList[T]) -> IEnumerable_1[T]:
    return xs


def of_array_with_tail[T](xs: Array[T], tail_1: FSharpList[T]) -> FSharpList[T]:
    res: FSharpList[Any] = tail_1
    for i in range(int32(len(xs)) - int32.ONE, int32.ZERO, -1):
        res = FSharpList_Cons_305B8EAC(xs[i], res)
    return res


def of_array[T](xs: Array[T]) -> FSharpList[T]:
    return of_array_with_tail(xs, FSharpList_get_Empty())


def of_seq[T](xs: IEnumerable_1[T]) -> FSharpList[T]:
    if isinstance(xs, Array):
        return of_array(xs)

    elif isinstance(xs, FSharpList):
        return xs

    else:
        root: FSharpList[Any] = FSharpList_get_Empty()
        node: FSharpList[Any] = root
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()

                def _arrow36(__unit: Unit = UNIT) -> FSharpList[T]:
                    xs_3: FSharpList[Any] = node
                    t: FSharpList[Any] = FSharpList(x, None)
                    xs_3.tail_ = t
                    return t

                node = _arrow36()
        xs_5: FSharpList[Any] = node
        t_2: FSharpList[Any] = FSharpList_get_Empty()
        xs_5.tail_ = t_2
        return FSharpList__get_Tail(root)


def concat[T](lists: IEnumerable_1[FSharpList[T]]) -> FSharpList[T]:
    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = root

    def action(xs: FSharpList[T]) -> None:
        nonlocal node

        def _arrow37(acc: FSharpList[T], x: T) -> FSharpList[T]:
            t: FSharpList[Any] = FSharpList(x, None)
            acc.tail_ = t
            return t

        node = fold(_arrow37, node, xs)

    if isinstance(lists, Array):
        iterate_1(action, lists)

    elif isinstance(lists, FSharpList):
        iterate(action, lists)

    else:
        with Disposable(get_enumerator(lists)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                action(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())

    xs_6: FSharpList[Any] = node
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    xs_6.tail_ = t_2
    return FSharpList__get_Tail(root)


def scan[STATE, T](folder: Callable[[STATE, T], STATE], state: STATE, xs: FSharpList[T]) -> FSharpList[STATE]:
    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any]
    t: FSharpList[Any] = FSharpList(state, None)
    root.tail_ = t
    node = t
    acc: Any = state
    xs_3: FSharpList[Any] = xs
    while not FSharpList__get_IsEmpty(xs_3):
        acc = folder(acc, FSharpList__get_Head(xs_3))

        def _arrow38(__unit: Unit = UNIT) -> FSharpList[STATE]:
            xs_4: FSharpList[Any] = node
            t_2: FSharpList[Any] = FSharpList(acc, None)
            xs_4.tail_ = t_2
            return t_2

        node = _arrow38()
        xs_3 = FSharpList__get_Tail(xs_3)
    xs_6: FSharpList[Any] = node
    t_4: FSharpList[Any] = FSharpList_get_Empty()
    xs_6.tail_ = t_4
    return FSharpList__get_Tail(root)


def scan_back[T, STATE](folder: Callable[[T, STATE], STATE], xs: FSharpList[T], state: STATE) -> FSharpList[STATE]:
    return of_array(scan_back_1(folder, to_array(xs), state, None))


def append[T](xs: FSharpList[T], ys: FSharpList[T]) -> FSharpList[T]:
    def _arrow39(acc: FSharpList[T], x: T) -> FSharpList[T]:
        return FSharpList_Cons_305B8EAC(x, acc)

    return fold(_arrow39, ys, reverse(xs))


def collect[T, U](mapping: Callable[[T], FSharpList[U]], xs: FSharpList[T]) -> FSharpList[U]:
    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = root
    ys: FSharpList[Any] = xs
    while not FSharpList__get_IsEmpty(ys):
        zs: FSharpList[Any] = mapping(FSharpList__get_Head(ys))
        while not FSharpList__get_IsEmpty(zs):

            def _arrow40(__unit: Unit = UNIT) -> FSharpList[U]:
                xs_1: FSharpList[Any] = node
                t: FSharpList[Any] = FSharpList(FSharpList__get_Head(zs), None)
                xs_1.tail_ = t
                return t

            node = _arrow40()
            zs = FSharpList__get_Tail(zs)
        ys = FSharpList__get_Tail(ys)
    xs_3: FSharpList[Any] = node
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    xs_3.tail_ = t_2
    return FSharpList__get_Tail(root)


def map_indexed[T, U](mapping: Callable[[int32, T], U], xs: FSharpList[T]) -> FSharpList[U]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(i: int32, acc: FSharpList[U], x: T, mapping: Any = mapping) -> FSharpList[U]:
        t: FSharpList[Any] = FSharpList(mapping(i, x), None)
        acc.tail_ = t
        return t

    node: FSharpList[Any] = fold_indexed(folder, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def map[T, U](mapping: Callable[[T], U], xs: FSharpList[T]) -> FSharpList[U]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(acc: FSharpList[U], x: T, mapping: Any = mapping) -> FSharpList[U]:
        t: FSharpList[Any] = FSharpList(mapping(x), None)
        acc.tail_ = t
        return t

    node: FSharpList[Any] = fold(folder, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def indexed[_A](xs: FSharpList[_A]) -> FSharpList[tuple[int32, _A]]:
    def _arrow41(i: int32, x: _A) -> tuple[int32, _A]:
        return (i, x)

    return map_indexed(_arrow41, xs)


def map2[T1, T2, U](mapping: Callable[[T1, T2], U], xs: FSharpList[T1], ys: FSharpList[T2]) -> FSharpList[U]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(acc: FSharpList[U], x: T1, y: T2, mapping: Any = mapping) -> FSharpList[U]:
        t: FSharpList[Any] = FSharpList(mapping(x, y), None)
        acc.tail_ = t
        return t

    node: FSharpList[Any] = fold2(folder, root, xs, ys)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def map_indexed2[T1, T2, U](
    mapping: Callable[[int32, T1, T2], U], xs: FSharpList[T1], ys: FSharpList[T2]
) -> FSharpList[U]:
    def loop(
        i_mut: int32, acc_mut: FSharpList[U], xs_1_mut: FSharpList[T1], ys_1_mut: FSharpList[T2], mapping: Any = mapping
    ) -> FSharpList[U]:
        while True:
            (i, acc, xs_1, ys_1) = (i_mut, acc_mut, xs_1_mut, ys_1_mut)
            if True if FSharpList__get_IsEmpty(xs_1) else FSharpList__get_IsEmpty(ys_1):
                return acc

            else:
                i_mut = i + int32.ONE

                def _arrow42(i: Any = i, acc: Any = acc, xs_1: Any = xs_1, ys_1: Any = ys_1) -> FSharpList[U]:
                    t: FSharpList[Any] = FSharpList(
                        mapping(i, FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1)), None
                    )
                    acc.tail_ = t
                    return t

                acc_mut = _arrow42()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                ys_1_mut = FSharpList__get_Tail(ys_1)
                continue

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node_1: FSharpList[Any] = loop(int32.ZERO, root, xs, ys)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node_1.tail_ = t_2
    return FSharpList__get_Tail(root)


def map3[T1, T2, T3, U](
    mapping: Callable[[T1, T2, T3], U], xs: FSharpList[T1], ys: FSharpList[T2], zs: FSharpList[T3]
) -> FSharpList[U]:
    def loop(
        acc_mut: FSharpList[U],
        xs_1_mut: FSharpList[T1],
        ys_1_mut: FSharpList[T2],
        zs_1_mut: FSharpList[T3],
        mapping: Any = mapping,
    ) -> FSharpList[U]:
        while True:
            (acc, xs_1, ys_1, zs_1) = (acc_mut, xs_1_mut, ys_1_mut, zs_1_mut)
            if (
                True
                if (True if FSharpList__get_IsEmpty(xs_1) else FSharpList__get_IsEmpty(ys_1))
                else FSharpList__get_IsEmpty(zs_1)
            ):
                return acc

            else:

                def _arrow54(acc: Any = acc, xs_1: Any = xs_1, ys_1: Any = ys_1, zs_1: Any = zs_1) -> FSharpList[U]:
                    t: FSharpList[Any] = FSharpList(
                        mapping(FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1), FSharpList__get_Head(zs_1)),
                        None,
                    )
                    acc.tail_ = t
                    return t

                acc_mut = _arrow54()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                ys_1_mut = FSharpList__get_Tail(ys_1)
                zs_1_mut = FSharpList__get_Tail(zs_1)
                continue

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node_1: FSharpList[Any] = loop(root, xs, ys, zs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node_1.tail_ = t_2
    return FSharpList__get_Tail(root)


def map_fold[STATE, T, RESULT](
    mapping: Callable[[STATE, T], tuple[RESULT, STATE]], state: STATE, xs: FSharpList[T]
) -> tuple[FSharpList[RESULT], STATE]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(
        tupled_arg: tuple[FSharpList[RESULT], STATE], x: T, mapping: Any = mapping
    ) -> tuple[FSharpList[RESULT], STATE]:
        pattern_input: tuple[Any, Any] = mapping(tupled_arg[1], x)

        def _arrow55(tupled_arg: Any = tupled_arg) -> FSharpList[RESULT]:
            t: FSharpList[Any] = FSharpList(pattern_input[0], None)
            tupled_arg[0].tail_ = t
            return t

        return (_arrow55(), pattern_input[1])

    pattern_input_1: tuple[FSharpList[Any], Any] = fold(folder, (root, state), xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    pattern_input_1[0].tail_ = t_2
    return (FSharpList__get_Tail(root), pattern_input_1[1])


def map_fold_back[T, STATE, RESULT](
    mapping: Callable[[T, STATE], tuple[RESULT, STATE]], xs: FSharpList[T], state: STATE
) -> tuple[FSharpList[RESULT], STATE]:
    def _arrow56(acc: STATE, x: T, mapping: Any = mapping) -> tuple[RESULT, STATE]:
        return mapping(x, acc)

    return map_fold(_arrow56, state, reverse(xs))


def try_pick[T, _A](f: Callable[[T], Option[_A]], xs: FSharpList[T]) -> Option[_A]:
    def loop(xs_1_mut: FSharpList[T], f: Any = f) -> Option[_A]:
        while True:
            (xs_1,) = (xs_1_mut,)
            if FSharpList__get_IsEmpty(xs_1):
                return None

            else:
                match_value: Option[Any] = f(FSharpList__get_Head(xs_1))
                if match_value is None:
                    xs_1_mut = FSharpList__get_Tail(xs_1)
                    continue

                else:
                    return match_value

            break

    return loop(xs)


def pick[_A, _B](f: Callable[[_A], Option[_B]], xs: FSharpList[_A]) -> _B:
    match_value: Option[Any] = try_pick(f, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> Option[_A]:
    def _arrow57(x: _A = UNIT, f: Any = f) -> Option[_A]:
        return some(x) if f(x) else None

    return try_pick(_arrow57, xs)


def find[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> _A:
    match_value: Option[Any] = try_find(f, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_back[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> Option[_A]:
    return try_find_back_1(f, to_array(xs))


def find_back[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> _A:
    match_value: Option[Any] = try_find_back(f, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_index[T](f: Callable[[T], bool], xs: FSharpList[T]) -> int32 | None:
    def loop(i_mut: int32, xs_1_mut: FSharpList[T], f: Any = f) -> int32 | None:
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return None

            elif f(FSharpList__get_Head(xs_1)):
                return i

            else:
                i_mut = i + int32.ONE
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    return erase(loop(int32.ZERO, xs))


def find_index[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> int32:
    match_value: int32 | None = erase(try_find_index(f, xs))
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def try_find_index_back[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> int32 | None:
    return erase(try_find_index_back_1(f, to_array(xs)))


def find_index_back[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> int32:
    match_value: int32 | None = erase(try_find_index_back(f, xs))
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def try_item[T](n: int32, xs: FSharpList[T]) -> Option[T]:
    def loop(i_mut: int32, xs_1_mut: FSharpList[T], n: Any = n) -> Option[T]:
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return None

            elif i == n:
                return some(FSharpList__get_Head(xs_1))

            else:
                i_mut = i + int32.ONE
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    return loop(int32.ZERO, xs)


def item[T](n: int32, xs: FSharpList[T]) -> T:
    return FSharpList__get_Item_Z524259A4(xs, n)


def filter[T](f: Callable[[T], bool], xs: FSharpList[T]) -> FSharpList[T]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(acc: FSharpList[T], x: T, f: Any = f) -> FSharpList[T]:
        if f(x):
            t: FSharpList[Any] = FSharpList(x, None)
            acc.tail_ = t
            return t

        else:
            return acc

    node: FSharpList[Any] = fold(folder, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def partition[T](f: Callable[[T], bool], xs: FSharpList[T]) -> tuple[FSharpList[T], FSharpList[T]]:
    match_value: FSharpList[Any] = FSharpList_get_Empty()
    root2: FSharpList[Any] = FSharpList_get_Empty()
    root1: FSharpList[Any] = match_value

    def folder(
        tupled_arg: tuple[FSharpList[T], FSharpList[T]], x: T, f: Any = f
    ) -> tuple[FSharpList[T], FSharpList[T]]:
        lacc: FSharpList[Any] = tupled_arg[0]
        racc: FSharpList[Any] = tupled_arg[1]
        if f(x):

            def _arrow58(x: Any = x) -> FSharpList[T]:
                t: FSharpList[Any] = FSharpList(x, None)
                lacc.tail_ = t
                return t

            return (_arrow58(), racc)

        else:

            def _arrow59(x: Any = x) -> FSharpList[T]:
                t_2: FSharpList[Any] = FSharpList(x, None)
                racc.tail_ = t_2
                return t_2

            return (lacc, _arrow59())

    pattern_input_1: tuple[FSharpList[Any], FSharpList[Any]] = fold(folder, (root1, root2), xs)
    t_4: FSharpList[Any] = FSharpList_get_Empty()
    pattern_input_1[0].tail_ = t_4
    t_5: FSharpList[Any] = FSharpList_get_Empty()
    pattern_input_1[1].tail_ = t_5
    return (FSharpList__get_Tail(root1), FSharpList__get_Tail(root2))


def choose[T, U](f: Callable[[T], Option[U]], xs: FSharpList[T]) -> FSharpList[U]:
    root: FSharpList[Any] = FSharpList_get_Empty()

    def folder(acc: FSharpList[U], x: T, f: Any = f) -> FSharpList[U]:
        match_value: Option[Any] = f(x)
        if match_value is None:
            return acc

        else:
            t: FSharpList[Any] = FSharpList(value_1(match_value), None)
            acc.tail_ = t
            return t

    node: FSharpList[Any] = fold(folder, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def contains[T](value: T, xs: FSharpList[T], eq: IEqualityComparer_1[Any]) -> bool:
    def _arrow60(v: T = UNIT, value: Any = value, eq: Any = eq) -> bool:
        return eq.Equals(value, v)

    return try_find_index(_arrow60, xs) is not None


def initialize[T](n: int32, f: Callable[[int32], T]) -> FSharpList[T]:
    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = root
    for i in range(int32.ZERO, n - int32.ONE, 1):

        def _arrow61(f: Any = f) -> FSharpList[T]:
            xs: FSharpList[Any] = node
            t: FSharpList[Any] = FSharpList(f(i), None)
            xs.tail_ = t
            return t

        node = _arrow61()
    xs_2: FSharpList[Any] = node
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    xs_2.tail_ = t_2
    return FSharpList__get_Tail(root)


def replicate[_A](n: int32, x: _A) -> FSharpList[_A]:
    def _arrow62(_arg: int32, x: Any = x) -> _A:
        return x

    return initialize(n, _arrow62)


def reduce[T](f: Callable[[T, T], T], xs: FSharpList[T]) -> T:
    if FSharpList__get_IsEmpty(xs):
        raise Exception(SR_inputWasEmpty)

    else:
        return fold(f, head(xs), tail(xs))


def reduce_back[T](f: Callable[[T, T], T], xs: FSharpList[T]) -> T:
    if FSharpList__get_IsEmpty(xs):
        raise Exception(SR_inputWasEmpty)

    else:
        return fold_back(f, tail(xs), head(xs))


def for_all[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> bool:
    def _arrow63(acc: bool, x: _A, f: Any = f) -> bool:
        return f(x) if acc else False

    return fold(_arrow63, True, xs)


def for_all2[_A, _B](f: Callable[[_A, _B], bool], xs: FSharpList[_A], ys: FSharpList[_B]) -> bool:
    def _arrow64(acc: bool, x: _A, y: _B, f: Any = f) -> bool:
        return f(x, y) if acc else False

    return fold2(_arrow64, True, xs, ys)


def exists[_A](f: Callable[[_A], bool], xs: FSharpList[_A]) -> bool:
    return try_find_index(f, xs) is not None


def exists2[T1, T2](f_mut: Callable[[T1, T2], bool], xs_mut: FSharpList[T1], ys_mut: FSharpList[T2]) -> bool:
    while True:
        (f, xs, ys) = (f_mut, xs_mut, ys_mut)
        match_value: bool = FSharpList__get_IsEmpty(xs)
        match_value_1: bool = FSharpList__get_IsEmpty(ys)
        (pattern_matching_result,) = nullable[int32]()
        if match_value:
            if match_value_1:
                pattern_matching_result = int32(0)

            else:
                pattern_matching_result = int32(2)

        elif match_value_1:
            pattern_matching_result = int32(2)

        else:
            pattern_matching_result = int32(1)

        if pattern_matching_result == int32.ZERO:
            return False

        elif pattern_matching_result == int32.ONE:
            if f(FSharpList__get_Head(xs), FSharpList__get_Head(ys)):
                return True

            else:
                f_mut = f
                xs_mut = FSharpList__get_Tail(xs)
                ys_mut = FSharpList__get_Tail(ys)
                continue

        else:
            raise Exception(SR_differentLengths + " (Parameter 'list2')")

        break


def unzip[_A, _B](xs: FSharpList[tuple[_A, _B]]) -> tuple[FSharpList[_A], FSharpList[_B]]:
    def _arrow65(
        tupled_arg: tuple[_A, _B], tupled_arg_1: tuple[FSharpList[_A], FSharpList[_B]]
    ) -> tuple[FSharpList[_A], FSharpList[_B]]:
        return (
            FSharpList_Cons_305B8EAC(tupled_arg[0], tupled_arg_1[0]),
            FSharpList_Cons_305B8EAC(tupled_arg[1], tupled_arg_1[1]),
        )

    return fold_back(_arrow65, xs, (FSharpList_get_Empty(), FSharpList_get_Empty()))


def unzip3[_A, _B, _C](xs: FSharpList[tuple[_A, _B, _C]]) -> tuple[FSharpList[_A], FSharpList[_B], FSharpList[_C]]:
    def _arrow66(
        tupled_arg: tuple[_A, _B, _C], tupled_arg_1: tuple[FSharpList[_A], FSharpList[_B], FSharpList[_C]]
    ) -> tuple[FSharpList[_A], FSharpList[_B], FSharpList[_C]]:
        return (
            FSharpList_Cons_305B8EAC(tupled_arg[0], tupled_arg_1[0]),
            FSharpList_Cons_305B8EAC(tupled_arg[1], tupled_arg_1[1]),
            FSharpList_Cons_305B8EAC(tupled_arg[2], tupled_arg_1[2]),
        )

    return fold_back(_arrow66, xs, (FSharpList_get_Empty(), FSharpList_get_Empty(), FSharpList_get_Empty()))


def zip[_A, _B](xs: FSharpList[_A], ys: FSharpList[_B]) -> FSharpList[tuple[_A, _B]]:
    def _arrow67(x: _A, y: _B) -> tuple[_A, _B]:
        return (x, y)

    return map2(_arrow67, xs, ys)


def zip3[_A, _B, _C](xs: FSharpList[_A], ys: FSharpList[_B], zs: FSharpList[_C]) -> FSharpList[tuple[_A, _B, _C]]:
    def _arrow68(x: _A, y: _B, z: _C) -> tuple[_A, _B, _C]:
        return (x, y, z)

    return map3(_arrow68, xs, ys, zs)


def sort_with[T](comparer: Callable[[T, T], int32], xs: FSharpList[T]) -> FSharpList[T]:
    arr: Array[Any] = to_array(xs)
    sort_in_place_with(comparer, arr)
    return of_array(arr)


def sort[T](xs: FSharpList[T], comparer: IComparer_1[T]) -> FSharpList[T]:
    def _arrow69(x: T, y: T, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y)

    return sort_with(_arrow69, xs)


def sort_by[T, U](projection: Callable[[T], U], xs: FSharpList[T], comparer: IComparer_1[U]) -> FSharpList[T]:
    def _arrow70(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y))

    return sort_with(_arrow70, xs)


def sort_descending[T](xs: FSharpList[T], comparer: IComparer_1[T]) -> FSharpList[T]:
    def _arrow71(x: T, y: T, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y) * int32.NEG_ONE

    return sort_with(_arrow71, xs)


def sort_by_descending[T, U](
    projection: Callable[[T], U], xs: FSharpList[T], comparer: IComparer_1[U]
) -> FSharpList[T]:
    def _arrow72(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y)) * int32.NEG_ONE

    return sort_with(_arrow72, xs)


def sum[T](xs: FSharpList[T], adder: IGenericAdder_1[T]) -> T:
    def _arrow73(acc: T, x: T, adder: Any = adder) -> T:
        return adder.Add(acc, x)

    return fold(_arrow73, adder.GetZero(), xs)


def sum_by[T, U](f: Callable[[T], U], xs: FSharpList[T], adder: IGenericAdder_1[U]) -> U:
    def _arrow74(acc: U, x: T, f: Any = f, adder: Any = adder) -> U:
        return adder.Add(acc, f(x))

    return fold(_arrow74, adder.GetZero(), xs)


def max_by[T, U](projection: Callable[[T], U], xs: FSharpList[T], comparer: IComparer_1[U]) -> T:
    def _arrow75(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else x

    return reduce(_arrow75, xs)


def max[T](xs: FSharpList[T], comparer: IComparer_1[T]) -> T:
    def _arrow76(x: T, y: T, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(y, x) > int32.ZERO) else x

    return reduce(_arrow76, xs)


def min_by[T, U](projection: Callable[[T], U], xs: FSharpList[T], comparer: IComparer_1[U]) -> T:
    def _arrow77(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else y

    return reduce(_arrow77, xs)


def min[T](xs: FSharpList[T], comparer: IComparer_1[T]) -> T:
    def _arrow78(x: T, y: T, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(y, x) > int32.ZERO) else y

    return reduce(_arrow78, xs)


def average[T](xs: FSharpList[T], averager: IGenericAverager_1[T]) -> T:
    count: int32 = int32.ZERO

    def folder(acc: T, x: T, averager: Any = averager) -> T:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, x)

    total: Any = fold(folder, averager.GetZero(), xs)
    return averager.DivideByInt(total, count)


def average_by[T, U](f: Callable[[T], U], xs: FSharpList[T], averager: IGenericAverager_1[U]) -> U:
    count: int32 = int32.ZERO

    def _arrow79(acc: U, x: T, f: Any = f, averager: Any = averager) -> U:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, f(x))

    total: Any = fold(_arrow79, averager.GetZero(), xs)
    return averager.DivideByInt(total, count)


def permute[T](f: Callable[[int32], int32], xs: FSharpList[T]) -> FSharpList[T]:
    return of_array(permute_1(f, to_array(xs)))


def chunk_by_size[T](chunk_size: int32, xs: FSharpList[T]) -> FSharpList[FSharpList[T]]:
    return of_array(map_1(of_array, chunk_by_size_1(chunk_size, to_array(xs)), None))


def all_pairs[T1, T2](xs: FSharpList[T1], ys: FSharpList[T2]) -> FSharpList[tuple[T1, T2]]:
    root: FSharpList[tuple[Any, Any]] = FSharpList_get_Empty()
    node: FSharpList[tuple[Any, Any]] = root

    def _arrow82(x: T1 = UNIT, ys: Any = ys) -> None:
        def _arrow81(y: T2 = UNIT) -> None:
            nonlocal node

            def _arrow80(__unit: Unit = UNIT) -> FSharpList[tuple[T1, T2]]:
                xs_1: FSharpList[tuple[Any, Any]] = node
                t: FSharpList[tuple[Any, Any]] = FSharpList((x, y), None)
                xs_1.tail_ = t
                return t

            node = _arrow80()

        iterate(_arrow81, ys)

    iterate(_arrow82, xs)
    xs_3: FSharpList[tuple[Any, Any]] = node
    t_2: FSharpList[tuple[Any, Any]] = FSharpList_get_Empty()
    xs_3.tail_ = t_2
    return FSharpList__get_Tail(root)


def skip[T](count_mut: int32, xs_mut: FSharpList[T]) -> FSharpList[T]:
    while True:
        (count, xs) = (count_mut, xs_mut)
        if count <= int32.ZERO:
            return xs

        elif FSharpList__get_IsEmpty(xs):
            raise Exception(SR_notEnoughElements + " (Parameter 'list')")

        else:
            count_mut = count - int32.ONE
            xs_mut = FSharpList__get_Tail(xs)
            continue

        break


def skip_while[T](predicate_mut: Callable[[T], bool], xs_mut: FSharpList[T]) -> FSharpList[T]:
    while True:
        (predicate, xs) = (predicate_mut, xs_mut)
        if FSharpList__get_IsEmpty(xs):
            return xs

        elif not predicate(FSharpList__get_Head(xs)):
            return xs

        else:
            predicate_mut = predicate
            xs_mut = FSharpList__get_Tail(xs)
            continue

        break


def take[T](count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    if count < int32.ZERO:
        raise Exception(SR_inputMustBeNonNegative + " (Parameter 'count')")

    def loop(i_mut: int32, acc_mut: FSharpList[T], xs_1_mut: FSharpList[T]) -> FSharpList[T]:
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if i <= int32.ZERO:
                return acc

            elif FSharpList__get_IsEmpty(xs_1):
                raise Exception(SR_notEnoughElements + " (Parameter 'list')")

            else:
                i_mut = i - int32.ONE

                def _arrow90(acc: Any = acc, xs_1: Any = xs_1) -> FSharpList[T]:
                    t: FSharpList[Any] = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail_ = t
                    return t

                acc_mut = _arrow90()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = loop(count, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def take_while[T](predicate: Callable[[T], bool], xs: FSharpList[T]) -> FSharpList[T]:
    def loop(acc_mut: FSharpList[T], xs_1_mut: FSharpList[T], predicate: Any = predicate) -> FSharpList[T]:
        while True:
            (acc, xs_1) = (acc_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return acc

            elif not predicate(FSharpList__get_Head(xs_1)):
                return acc

            else:

                def _arrow92(acc: Any = acc, xs_1: Any = xs_1) -> FSharpList[T]:
                    t: FSharpList[Any] = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail_ = t
                    return t

                acc_mut = _arrow92()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = loop(root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def truncate[T](count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    def loop(i_mut: int32, acc_mut: FSharpList[T], xs_1_mut: FSharpList[T]) -> FSharpList[T]:
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if i <= int32.ZERO:
                return acc

            elif FSharpList__get_IsEmpty(xs_1):
                return acc

            else:
                i_mut = i - int32.ONE

                def _arrow93(acc: Any = acc, xs_1: Any = xs_1) -> FSharpList[T]:
                    t: FSharpList[Any] = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail_ = t
                    return t

                acc_mut = _arrow93()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue

            break

    root: FSharpList[Any] = FSharpList_get_Empty()
    node: FSharpList[Any] = loop(count, root, xs)
    t_2: FSharpList[Any] = FSharpList_get_Empty()
    node.tail_ = t_2
    return FSharpList__get_Tail(root)


def get_slice[T](start_index: int32 | None, end_index: int32 | None, xs: FSharpList[T]) -> FSharpList[T]:
    len_1: int32 = length(xs)
    start_index_1: int32
    index: int32 = default_arg(start_index, int32.ZERO)
    start_index_1 = int32.ZERO if (index < int32.ZERO) else index
    end_index_1: int32
    index_1: int32 = default_arg(end_index, len_1 - int32.ONE)
    end_index_1 = (len_1 - int32.ONE) if (index_1 >= len_1) else index_1
    if end_index_1 < start_index_1:
        return FSharpList_get_Empty()

    else:
        return take((end_index_1 - start_index_1) + int32.ONE, skip(start_index_1, xs))


def split_at[T](index: int32, xs: FSharpList[T]) -> tuple[FSharpList[T], FSharpList[T]]:
    if index < int32.ZERO:
        raise Exception(SR_inputMustBeNonNegative + " (Parameter 'index')")

    if index > FSharpList__get_Length(xs):
        raise Exception(SR_notEnoughElements + " (Parameter 'index')")

    return (take(index, xs), skip(index, xs))


def exactly_one[T](xs: FSharpList[T]) -> T:
    if FSharpList__get_IsEmpty(xs):
        raise Exception(SR_inputSequenceEmpty + " (Parameter 'list')")

    elif FSharpList__get_IsEmpty(FSharpList__get_Tail(xs)):
        return FSharpList__get_Head(xs)

    else:
        raise Exception(SR_inputSequenceTooLong + " (Parameter 'list')")


def try_exactly_one[T](xs: FSharpList[T]) -> Option[T]:
    if FSharpList__get_IsEmpty(FSharpList__get_Tail(xs)) if (not FSharpList__get_IsEmpty(xs)) else False:
        return some(FSharpList__get_Head(xs))

    else:
        return None


def where[T](predicate: Callable[[T], bool], xs: FSharpList[T]) -> FSharpList[T]:
    return filter(predicate, xs)


def pairwise[T](xs: FSharpList[T]) -> FSharpList[tuple[T, T]]:
    return of_array(pairwise_1(to_array(xs)))


def windowed[T](window_size: int32, xs: FSharpList[T]) -> FSharpList[FSharpList[T]]:
    return of_array(map_1(of_array, windowed_1(window_size, to_array(xs)), None))


def split_into[T](chunks: int32, xs: FSharpList[T]) -> FSharpList[FSharpList[T]]:
    return of_array(map_1(of_array, split_into_1(chunks, to_array(xs)), None))


def transpose[T](lists: IEnumerable_1[FSharpList[T]]) -> FSharpList[FSharpList[T]]:
    return of_array(map_1(of_array, transpose_1(map_1(to_array, of_seq_1(lists), None), None), None))


def insert_at[T](index: int32, y: T, xs: FSharpList[T]) -> FSharpList[T]:
    i: int32 = int32.NEG_ONE
    is_done: bool = False

    def folder(acc: FSharpList[T], x: T, index: Any = index, y: Any = y) -> FSharpList[T]:
        nonlocal i, is_done
        i = i + int32.ONE
        if i == index:
            is_done = True
            return FSharpList_Cons_305B8EAC(x, FSharpList_Cons_305B8EAC(y, acc))

        else:
            return FSharpList_Cons_305B8EAC(x, acc)

    result: FSharpList[Any] = fold(folder, FSharpList_get_Empty(), xs)

    def _arrow94(__unit: Unit = UNIT) -> FSharpList[T]:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    return reverse(
        result if is_done else (FSharpList_Cons_305B8EAC(y, result) if ((i + int32.ONE) == index) else _arrow94())
    )


def insert_many_at[T](index: int32, ys: IEnumerable_1[T], xs: FSharpList[T]) -> FSharpList[T]:
    i: int32 = int32.NEG_ONE
    is_done: bool = False
    ys_1: FSharpList[Any] = of_seq(ys)

    def folder(acc: FSharpList[T], x: T, index: Any = index) -> FSharpList[T]:
        nonlocal i, is_done
        i = i + int32.ONE
        if i == index:
            is_done = True
            return FSharpList_Cons_305B8EAC(x, append(ys_1, acc))

        else:
            return FSharpList_Cons_305B8EAC(x, acc)

    result: FSharpList[Any] = fold(folder, FSharpList_get_Empty(), xs)

    def _arrow95(__unit: Unit = UNIT) -> FSharpList[T]:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    return reverse(result if is_done else (append(ys_1, result) if ((i + int32.ONE) == index) else _arrow95()))


def remove_at[T](index: int32, xs: FSharpList[T]) -> FSharpList[T]:
    i: int32 = int32.NEG_ONE
    is_done: bool = False

    def f(_arg: T = UNIT, index: Any = index) -> bool:
        nonlocal i, is_done
        i = i + int32.ONE
        if i == index:
            is_done = True
            return False

        else:
            return True

    ys: FSharpList[Any] = filter(f, xs)
    if not is_done:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    return ys


def remove_many_at[T](index: int32, count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    i: int32 = int32.NEG_ONE
    status: int32 = int32.NEG_ONE

    def f(_arg: T = UNIT, index: Any = index, count: Any = count) -> bool:
        nonlocal i, status
        i = i + int32.ONE
        if i == index:
            status = int32.ZERO
            return False

        elif i > index:
            if i < (index + count):
                return False

            else:
                status = int32.ONE
                return True

        else:
            return True

    ys: FSharpList[Any] = filter(f, xs)
    status_1: int32 = (
        int32.ONE if (((i + int32.ONE) == (index + count)) if (status == int32.ZERO) else False) else status
    )
    if status_1 < int32.ONE:
        raise Exception(
            SR_indexOutOfBounds + ((" (Parameter '" + ("index" if (status_1 < int32.ZERO) else "count")) + "')")
        )

    return ys


def update_at[T](index: int32, y: T, xs: FSharpList[T]) -> FSharpList[T]:
    is_done: bool = False

    def mapping(i: int32, x: T, index: Any = index, y: Any = y) -> T:
        nonlocal is_done
        if i == index:
            is_done = True
            return y

        else:
            return x

    ys: FSharpList[Any] = map_indexed(mapping, xs)
    if not is_done:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    return ys


def random_shuffle_by[T](randomizer: Callable[[], float64], xs: FSharpList[T]) -> FSharpList[T]:
    arr: Array[Any] = to_array(xs)
    random_shuffle_in_place_by(randomizer, arr)
    return of_array(arr)


def random_shuffle_with[T](random: Any, xs: FSharpList[T]) -> FSharpList[T]:
    def _arrow96(random: Any = random) -> float64:
        return random_double(random)

    return random_shuffle_by(_arrow96, xs)


def random_shuffle[T](xs: FSharpList[T]) -> FSharpList[T]:
    return random_shuffle_with(create_random(), xs)


def random_choice_by[T](randomizer: Callable[[], float64], xs: FSharpList[T]) -> T:
    return random_choice_by_1(randomizer, to_array(xs))


def random_choice_with[T](random: Any, xs: FSharpList[T]) -> T:
    def _arrow97(random: Any = random) -> float64:
        return random_double(random)

    return random_choice_by(_arrow97, xs)


def random_choice[T](xs: FSharpList[T]) -> T:
    return random_choice_with(create_random(), xs)


def random_choices_by[T](randomizer: Callable[[], float64], count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    return of_array(random_choices_by_1(randomizer, count, to_array(xs)))


def random_choices_with[T](random: Any, count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    def _arrow98(random: Any = random) -> float64:
        return random_double(random)

    return random_choices_by(_arrow98, count, xs)


def random_choices[T](count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    return random_choices_with(create_random(), count, xs)


def random_sample_by[T](randomizer: Callable[[], float64], count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    return of_array(random_sample_by_1(randomizer, count, to_array(xs)))


def random_sample_with[T](random: Any, count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    def _arrow99(random: Any = random) -> float64:
        return random_double(random)

    return random_sample_by(_arrow99, count, xs)


def random_sample[T](count: int32, xs: FSharpList[T]) -> FSharpList[T]:
    return random_sample_with(create_random(), count, xs)


__all__ = [
    "FSharpList_Cons_305B8EAC",
    "FSharpList__get_Head",
    "FSharpList__get_IsEmpty",
    "FSharpList__get_Item_Z524259A4",
    "FSharpList__get_Length",
    "FSharpList__get_Tail",
    "FSharpList_get_Empty",
    "FSharpList_reflection",
    "ListEnumerator_1_reflection",
    "all_pairs",
    "append",
    "average",
    "average_by",
    "choose",
    "chunk_by_size",
    "collect",
    "compare_with",
    "concat",
    "cons",
    "contains",
    "empty",
    "exactly_one",
    "exists",
    "exists2",
    "filter",
    "find",
    "find_back",
    "find_index",
    "find_index_back",
    "fold",
    "fold2",
    "fold_back",
    "fold_back2",
    "fold_indexed",
    "for_all",
    "for_all2",
    "get_slice",
    "head",
    "index_not_found",
    "indexed",
    "initialize",
    "insert_at",
    "insert_many_at",
    "is_empty",
    "item",
    "iterate",
    "iterate2",
    "iterate_indexed",
    "iterate_indexed2",
    "last",
    "length",
    "map",
    "map2",
    "map3",
    "map_fold",
    "map_fold_back",
    "map_indexed",
    "map_indexed2",
    "max",
    "max_by",
    "min",
    "min_by",
    "of_array",
    "of_array_with_tail",
    "of_seq",
    "pairwise",
    "partition",
    "permute",
    "pick",
    "random_choice",
    "random_choice_by",
    "random_choice_with",
    "random_choices",
    "random_choices_by",
    "random_choices_with",
    "random_sample",
    "random_sample_by",
    "random_sample_with",
    "random_shuffle",
    "random_shuffle_by",
    "random_shuffle_with",
    "reduce",
    "reduce_back",
    "remove_at",
    "remove_many_at",
    "replicate",
    "reverse",
    "scan",
    "scan_back",
    "singleton",
    "skip",
    "skip_while",
    "sort",
    "sort_by",
    "sort_by_descending",
    "sort_descending",
    "sort_with",
    "split_at",
    "split_into",
    "sum",
    "sum_by",
    "tail",
    "take",
    "take_while",
    "to_array",
    "to_seq",
    "transpose",
    "truncate",
    "try_exactly_one",
    "try_find",
    "try_find_back",
    "try_find_index",
    "try_find_index_back",
    "try_head",
    "try_item",
    "try_last",
    "try_pick",
    "unfold",
    "unzip",
    "unzip3",
    "update_at",
    "where",
    "windowed",
    "zip",
    "zip3",
]
