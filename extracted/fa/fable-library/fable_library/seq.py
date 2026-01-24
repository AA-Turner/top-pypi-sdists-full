from __future__ import annotations

from collections.abc import Callable
from typing import Any
from typing import cast as cast_1

from .array_ import Array, sort_in_place_with
from .array_ import chunk_by_size as chunk_by_size_1
from .array_ import fold_back as fold_back_1
from .array_ import fold_back2 as fold_back2_1
from .array_ import map as map_1
from .array_ import map_fold as map_fold_1
from .array_ import map_fold_back as map_fold_back_1
from .array_ import of_seq as of_seq_1
from .array_ import pairwise as pairwise_1
from .array_ import permute as permute_1
from .array_ import reduce_back as reduce_back_1
from .array_ import reverse as reverse_1
from .array_ import scan_back as scan_back_1
from .array_ import singleton as singleton_1
from .array_ import split_into as split_into_1
from .array_ import transpose as transpose_1
from .array_ import try_find_back as try_find_back_1
from .array_ import try_find_index_back as try_find_index_back_1
from .array_ import try_head as try_head_1
from .array_ import try_item as try_item_1
from .array_ import windowed as windowed_1
from .fsharp_core import Operators_NullArgCheck
from .global_ import IGenericAdder_1, IGenericAverager_1, SR_indexOutOfBounds
from .list import FSharpList
from .list import is_empty as is_empty_1
from .list import length as length_1
from .list import of_array as of_array_1
from .list import of_seq as of_seq_2
from .list import to_array as to_array_1
from .list import try_head as try_head_2
from .list import try_item as try_item_2
from .option import Option, some
from .option import value as value_1
from .reflection import TypeInfo, class_type
from .system import InvalidOperationException__ctor_Z721C83C5, NotSupportedException__ctor_Z721C83C5
from .types import int32, to_string
from .util import (
    IComparer_1,
    IDisposable,
    IEnumerable_1,
    IEnumerator,
    IEqualityComparer_1,
    clear,
    equals,
    get_enumerator,
    ignore,
    is_array_like,
    is_disposable,
    lock,
    range,
    to_enumerable,
    to_iterator,
)
from .util import dispose as dispose_2
from .util import int32 as int32_1


SR_enumerationAlreadyFinished: str = "Enumeration already finished."

SR_enumerationNotStarted: str = "Enumeration has not started. Call MoveNext."

SR_inputSequenceEmpty: str = "The input sequence was empty."

SR_inputSequenceTooLong: str = "The input sequence contains more than one element."

SR_keyNotFoundAlt: str = "An index satisfying the predicate was not found in the collection."

SR_notEnoughElements: str = "The input sequence has an insufficient number of elements."

SR_resetNotSupported: str = "Reset is not supported on this enumerator."


def Enumerator_noReset[_A](__unit: None = None) -> Any:
    raise NotSupportedException__ctor_Z721C83C5(SR_resetNotSupported)


def Enumerator_notStarted[_A](__unit: None = None) -> Any:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationNotStarted)


def Enumerator_alreadyFinished[_A](__unit: None = None) -> Any:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationAlreadyFinished)


def _expr95(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.Seq", [gen0], Enumerator_Seq)


class Enumerator_Seq[T]:
    def __init__(self, f: Callable[[], IEnumerator[T]]) -> None:
        self.f: Callable[[], IEnumerator[T]] = f

    def __str__(self, __unit: None = None) -> str:
        xs: Enumerator_Seq[T] = self
        i: int32 = int32.ZERO
        str_1: str = "seq ["
        with get_enumerator(xs) as e:
            while e.System_Collections_IEnumerator_MoveNext() if (i < int32.FOUR) else False:
                if i > int32.ZERO:
                    str_1 = str_1 + "; "

                str_1 = str_1 + to_string(e.System_Collections_Generic_IEnumerator_1_get_Current())
                i = i + int32.ONE
            if i == int32.FOUR:
                str_1 = str_1 + "; ..."

            return str_1 + "]"

    def GetEnumerator[T](self, __unit: None = None) -> IEnumerator[T]:
        x: Enumerator_Seq[T] = self
        return x.f()

    def __iter__[T](self) -> IEnumerator[T]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        x: Enumerator_Seq[T] = self
        return x.f()


Enumerator_Seq_reflection = _expr95


def Enumerator_Seq__ctor_673A07F2(f: Callable[[], IEnumerator[T]]) -> Enumerator_Seq[T]:
    return Enumerator_Seq(f)


def _expr96(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.FromFunctions`1", [gen0], Enumerator_FromFunctions_1)


class Enumerator_FromFunctions_1[T](IDisposable):
    def __init__(self, current: Callable[[], T], next_1: Callable[[], bool], dispose: Callable[[], None]) -> None:
        self.current: Callable[[], T] = current
        self.next: Callable[[], bool] = next_1
        self.dispose: Callable[[], None] = dispose

    def System_Collections_Generic_IEnumerator_1_get_Current[T](self, __unit: None = None) -> T:
        _: Enumerator_FromFunctions_1[T] = self
        return _.current()

    def System_Collections_IEnumerator_get_Current(self, __unit: None = None) -> Any:
        _: Enumerator_FromFunctions_1[T] = self
        return _.current()

    def System_Collections_IEnumerator_MoveNext(self, __unit: None = None) -> bool:
        _: Enumerator_FromFunctions_1[T] = self
        return _.next()

    def System_Collections_IEnumerator_Reset(self, __unit: None = None) -> None:
        Enumerator_noReset()

    def Dispose(self, __unit: None = None) -> None:
        _: Enumerator_FromFunctions_1[T] = self
        _.dispose()


Enumerator_FromFunctions_1_reflection = _expr96


def Enumerator_FromFunctions_1__ctor_58C54629(
    current: Callable[[], T], next_1: Callable[[], bool], dispose: Callable[[], None]
) -> Enumerator_FromFunctions_1[T]:
    return Enumerator_FromFunctions_1(current, next_1, dispose)


def Enumerator_cast[T](e: IEnumerator[T]) -> IEnumerator[T]:
    def current(__unit: None = None, e: Any = e) -> T:
        return e.System_Collections_Generic_IEnumerator_1_get_Current()

    def next_1(__unit: None = None, e: Any = e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()

    def dispose(__unit: None = None, e: Any = e) -> None:
        dispose_2(e)

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_concat[T, U](sources: IEnumerable_1[Any]) -> IEnumerator[Any]:
    outer_opt: IEnumerator[U] | None = None
    inner_opt: IEnumerator[T] | None = None
    started: bool = False
    finished: bool = False
    curr: T | None = None

    def finish(__unit: None = None, sources: Any = sources) -> None:
        nonlocal finished, inner_opt, outer_opt
        finished = True
        if inner_opt is not None:
            inner: IEnumerator[T] = inner_opt
            try:
                dispose_2(inner)

            finally:
                inner_opt = None

        if outer_opt is not None:
            outer: IEnumerator[U] = outer_opt
            try:
                dispose_2(outer)

            finally:
                outer_opt = None

    def current(__unit: None = None, sources: Any = sources) -> T:
        if not started:
            Enumerator_notStarted()

        elif finished:
            Enumerator_alreadyFinished()

        if curr is not None:
            return value_1(curr)

        else:
            return Enumerator_alreadyFinished()

    def next_1(__unit: None = None, sources: Any = sources) -> bool:
        nonlocal started
        if not started:
            started = True

        if finished:
            return False

        else:
            res: bool | None = None
            while res is None:
                nonlocal curr, inner_opt, outer_opt
                outer_opt_1: IEnumerator[U] | None = outer_opt
                inner_opt_1: IEnumerator[T] | None = inner_opt
                if outer_opt_1 is not None:
                    if inner_opt_1 is not None:
                        inner_1: IEnumerator[T] = inner_opt_1
                        if inner_1.System_Collections_IEnumerator_MoveNext():
                            curr = some(inner_1.System_Collections_Generic_IEnumerator_1_get_Current())
                            res = True

                        else:
                            try:
                                dispose_2(inner_1)

                            finally:
                                inner_opt = None

                    else:
                        outer_1: IEnumerator[U] = outer_opt_1
                        if outer_1.System_Collections_IEnumerator_MoveNext():
                            ie: U = outer_1.System_Collections_Generic_IEnumerator_1_get_Current()

                            def _arrow97(__unit: None = None) -> IEnumerator[T]:
                                copy_of_struct: U = ie
                                return get_enumerator(copy_of_struct)

                            inner_opt = _arrow97()

                        else:
                            finish()
                            res = False

                else:
                    outer_opt = get_enumerator(sources)

            return value_1(res)

    def dispose(__unit: None = None, sources: Any = sources) -> None:
        if not finished:
            finish()

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_enumerateThenFinally[T](f: Callable[[], None], e: IEnumerator[T]) -> IEnumerator[T]:
    def current(__unit: None = None, f: Any = f, e: Any = e) -> T:
        return e.System_Collections_Generic_IEnumerator_1_get_Current()

    def next_1(__unit: None = None, f: Any = f, e: Any = e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()

    def dispose(__unit: None = None, f: Any = f, e: Any = e) -> None:
        try:
            dispose_2(e)

        finally:
            f()

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_generateWhileSome[T, U](
    openf: Callable[[], T], compute: Callable[[T], U | None], closef: Callable[[T], None]
) -> IEnumerator[U]:
    started: bool = False
    curr: U | None = None
    state: T | None = some(openf())

    def dispose(__unit: None = None, openf: Any = openf, compute: Any = compute, closef: Any = closef) -> None:
        nonlocal state
        if state is not None:
            x_1: T = value_1(state)
            try:
                closef(x_1)

            finally:
                state = None

    def finish(__unit: None = None, openf: Any = openf, compute: Any = compute, closef: Any = closef) -> None:
        nonlocal curr
        try:
            dispose()

        finally:
            curr = None

    def current(__unit: None = None, openf: Any = openf, compute: Any = compute, closef: Any = closef) -> U:
        if not started:
            Enumerator_notStarted()

        if curr is not None:
            return value_1(curr)

        else:
            return Enumerator_alreadyFinished()

    def next_1(__unit: None = None, openf: Any = openf, compute: Any = compute, closef: Any = closef) -> bool:
        nonlocal started, curr
        if not started:
            started = True

        if state is not None:
            s: T = value_1(state)
            match_value_1: U | None
            try:
                match_value_1 = compute(s)

            except Exception as match_value:
                finish()
                raise match_value

            if match_value_1 is not None:
                curr = match_value_1
                return True

            else:
                finish()
                return False

        else:
            return False

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_unfold[STATE, T](f: Callable[[STATE], tuple[T, STATE] | None], state: STATE) -> IEnumerator[T]:
    curr: tuple[T, STATE] | None = None
    acc: STATE = state

    def current(__unit: None = None, f: Any = f, state: Any = state) -> T:
        if curr is not None:
            x: T = curr[int32_1(0)]
            st: STATE = curr[int32_1(1)]
            return x

        else:
            return Enumerator_notStarted()

    def next_1(__unit: None = None, f: Any = f, state: Any = state) -> bool:
        nonlocal curr, acc
        curr = f(acc)
        if curr is not None:
            x_1: T = curr[int32_1(0)]
            st_1: STATE = curr[int32_1(1)]
            acc = st_1
            return True

        else:
            return False

    def dispose(__unit: None = None, f: Any = f, state: Any = state) -> None:
        pass

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def index_not_found[_A](__unit: None = None) -> Any:
    raise Exception(SR_keyNotFoundAlt)


def mk_seq[T](f: Callable[[], IEnumerator[T]]) -> IEnumerable_1[T]:
    return Enumerator_Seq__ctor_673A07F2(f)


def of_seq[T](xs: IEnumerable_1[T]) -> IEnumerator[T]:
    return get_enumerator(Operators_NullArgCheck("source", xs))


def delay[T](generator: Callable[[], IEnumerable_1[T]]) -> IEnumerable_1[T]:
    def _arrow98(__unit: None = None, generator: Any = generator) -> IEnumerator[T]:
        return get_enumerator(generator())

    return mk_seq(_arrow98)


def concat[COLLECTION, T](sources: IEnumerable_1[Any]) -> IEnumerable_1[Any]:
    def _arrow99(__unit: None = None, sources: Any = sources) -> IEnumerator[T]:
        return Enumerator_concat(sources)

    return mk_seq(_arrow99)


def unfold[STATE, T](generator: Callable[[STATE], tuple[T, STATE] | None], state: STATE) -> IEnumerable_1[T]:
    def _arrow100(__unit: None = None, generator: Any = generator, state: Any = state) -> IEnumerator[T]:
        return Enumerator_unfold(generator, state)

    return mk_seq(_arrow100)


def empty[T](__unit: None = None) -> IEnumerable_1[Any]:
    def _arrow101(__unit: None = None) -> IEnumerable_1[T]:
        return [0] * int32.ZERO

    return delay(_arrow101)


def singleton[T](x: T | None = None) -> IEnumerable_1[T]:
    def _arrow102(__unit: None = None, x: Any = x) -> IEnumerable_1[T]:
        return singleton_1(x, None)

    return delay(_arrow102)


def of_array[T](arr: Array[T]) -> IEnumerable_1[T]:
    return arr


def to_array[T](xs: IEnumerable_1[T]) -> Array[T]:
    if isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return to_array_1(xs)

    else:
        return of_seq_1(xs)


def of_list[T](xs: FSharpList[T]) -> IEnumerable_1[T]:
    return xs


def to_list[T](xs: IEnumerable_1[T]) -> FSharpList[T]:
    if is_array_like(xs):
        xs = cast_1(Array[T], xs)
        return of_array_1(xs)

    elif isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return xs

    else:
        return of_seq_2(xs)


def generate[_A, _B](
    create: Callable[[], _A], compute: Callable[[_A], _B | None], dispose: Callable[[_A], None]
) -> IEnumerable_1[_B]:
    def _arrow103(
        __unit: None = None, create: Any = create, compute: Any = compute, dispose: Any = dispose
    ) -> IEnumerator[_B]:
        return Enumerator_generateWhileSome(create, compute, dispose)

    return mk_seq(_arrow103)


def generate_indexed[_A, _B](
    create: Callable[[], _A], compute: Callable[[int32, _A], _B | None], dispose: Callable[[_A], None]
) -> IEnumerable_1[_B]:
    def _arrow105(
        __unit: None = None, create: Any = create, compute: Any = compute, dispose: Any = dispose
    ) -> IEnumerator[_B]:
        i: int32 = int32.NEG_ONE

        def _arrow104(x: _A | None = None) -> _B | None:
            nonlocal i
            i = i + int32.ONE
            return compute(i, x)

        return Enumerator_generateWhileSome(create, _arrow104, dispose)

    return mk_seq(_arrow105)


def append[T](xs: IEnumerable_1[T], ys: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return concat(to_enumerable([xs, ys]))


def cast[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow106(__unit: None = None, xs: Any = xs) -> IEnumerator[T]:
        return Enumerator_cast(get_enumerator(Operators_NullArgCheck("source", xs)))

    return mk_seq(_arrow106)


def choose[T, U](chooser: Callable[[T], U | None], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow107(__unit: None = None, chooser: Any = chooser, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow108(e: IEnumerator[T], chooser: Any = chooser, xs: Any = xs) -> U | None:
        curr: U | None = None
        while e.System_Collections_IEnumerator_MoveNext() if (curr is None) else False:
            curr = chooser(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return curr

    def _arrow109(e_1: IEnumerator[T], chooser: Any = chooser, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow107, _arrow108, _arrow109)


def compare_with[T](comparer: Callable[[T, T], int32], xs: IEnumerable_1[T], ys: IEnumerable_1[T]) -> int32:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            c: int32 = int32.ZERO
            b1: bool = e1.System_Collections_IEnumerator_MoveNext()
            b2: bool = e2.System_Collections_IEnumerator_MoveNext()
            while b2 if (b1 if (c == int32.ZERO) else False) else False:
                c = comparer(
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
                if c == int32.ZERO:
                    b1 = e1.System_Collections_IEnumerator_MoveNext()
                    b2 = e2.System_Collections_IEnumerator_MoveNext()

            if c != int32.ZERO:
                return c

            elif b1:
                return int32.ONE

            elif b2:
                return int32.NEG_ONE

            else:
                return int32.ZERO


def contains[T](value: T, xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> bool:
    with of_seq(xs) as e:
        found: bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else False:
            found = comparer.Equals(value, e.System_Collections_Generic_IEnumerator_1_get_Current())
        return found


def enumerate_from_functions[_A, _B](
    create: Callable[[], _A], move_next: Callable[[_A], bool], current: Callable[[_A], _B]
) -> IEnumerable_1[_B]:
    def _arrow110(
        x: _A | None = None, create: Any = create, move_next: Any = move_next, current: Any = current
    ) -> _B | None:
        return some(current(x)) if move_next(x) else None

    def _arrow111(
        x_1: _A | None = None, create: Any = create, move_next: Any = move_next, current: Any = current
    ) -> None:
        match_value: Any = x_1
        if is_disposable(match_value):
            dispose_2(match_value)

    return generate(create, _arrow110, _arrow111)


def enumerate_then_finally[T](source: IEnumerable_1[T], compensation: Callable[[], None]) -> IEnumerable_1[T]:
    compensation_1: Callable[[], None] = compensation

    def _arrow112(__unit: None = None, source: Any = source, compensation: Any = compensation) -> IEnumerator[T]:
        try:
            return Enumerator_enumerateThenFinally(compensation_1, of_seq(source))

        except Exception as match_value:
            compensation_1()
            raise match_value

    return mk_seq(_arrow112)


def enumerate_using[T, U, _A](resource: T, source: Callable[[T], _A]) -> IEnumerable_1[Any]:
    def compensation(__unit: None = None, resource: Any = resource, source: Any = source) -> None:
        if equals(resource, None):
            pass

        else:
            copy_of_struct: T = resource
            dispose_2(copy_of_struct)

    def _arrow113(__unit: None = None, resource: Any = resource, source: Any = source) -> IEnumerator[U]:
        try:
            return Enumerator_enumerateThenFinally(compensation, of_seq(source(resource)))

        except Exception as match_value_1:
            compensation()
            raise match_value_1

    return mk_seq(_arrow113)


def enumerate_while[T](guard: Callable[[], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow114(i: int32, guard: Any = guard, xs: Any = xs) -> tuple[IEnumerable_1[T], int32] | None:
        return ((xs, i + int32.ONE)) if guard() else None

    return concat(unfold(_arrow114, int32.ZERO))


def filter[T](f: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def chooser(x: T | None = None, f: Any = f, xs: Any = xs) -> T | None:
        if f(x):
            return some(x)

        else:
            return None

    return choose(chooser, xs)


def exists[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> bool:
    with of_seq(xs) as e:
        found: bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else False:
            found = predicate(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return found


def exists2[T1, T2](predicate: Callable[[T1, T2], bool], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> bool:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            found: bool = False
            while (
                e2.System_Collections_IEnumerator_MoveNext()
                if (e1.System_Collections_IEnumerator_MoveNext() if (not found) else False)
                else False
            ):
                found = predicate(
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
            return found


def exactly_one[T](xs: IEnumerable_1[T]) -> T:
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                raise Exception((SR_inputSequenceTooLong + "\\nParameter name: ") + "source")

            else:
                return v

        else:
            raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")


def try_exactly_one[T](xs: IEnumerable_1[T]) -> T | None:
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                return None

            else:
                return some(v)

        else:
            return None


def try_find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T | None:
    with of_seq(xs) as e:
        res: T | None = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            c: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if predicate(c):
                res = some(c)

        return res


def find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: T | None = try_find(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T | None:
    return try_find_back_1(predicate, to_array(xs))


def find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: T | None = try_find_back(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_index[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32 | None:
    with of_seq(xs) as e:

        def loop(i_mut: int32, predicate: Any = predicate, xs: Any = xs) -> int32 | None:
            while True:
                (i,) = (i_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    if predicate(e.System_Collections_Generic_IEnumerator_1_get_Current()):
                        return i

                    else:
                        i_mut = i + int32.ONE
                        continue

                else:
                    return None

                break

        return loop(int32.ZERO)


def find_index[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32:
    match_value: int32 | None = try_find_index(predicate, xs)
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def try_find_index_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32 | None:
    return try_find_index_back_1(predicate, to_array(xs))


def find_index_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32:
    match_value: int32 | None = try_find_index_back(predicate, xs)
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def fold[STATE, T](folder: Callable[[STATE, T], STATE], state: STATE, xs: IEnumerable_1[T]) -> STATE:
    with of_seq(xs) as e:
        acc: STATE = state
        while e.System_Collections_IEnumerator_MoveNext():
            acc = folder(acc, e.System_Collections_Generic_IEnumerator_1_get_Current())
        return acc


def fold_back[STATE, T](folder: Callable[[T, Any], Any], xs: IEnumerable_1[T], state: Any = None) -> Any:
    return fold_back_1(folder, to_array(xs), state)


def fold2[STATE, T1, T2](
    folder: Callable[[STATE, T1, T2], STATE], state: STATE, xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]
) -> STATE:
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            acc: STATE = state
            while (
                e2.System_Collections_IEnumerator_MoveNext() if e1.System_Collections_IEnumerator_MoveNext() else False
            ):
                acc = folder(
                    acc,
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
            return acc


def fold_back2[STATE, T1, T2](
    folder: Callable[[T1, T2, STATE], STATE], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], state: STATE
) -> STATE:
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def for_all[_A](predicate: Callable[[_A], bool], xs: IEnumerable_1[_A]) -> bool:
    def _arrow115(x: _A | None = None, predicate: Any = predicate, xs: Any = xs) -> bool:
        return not predicate(x)

    return not exists(_arrow115, xs)


def for_all2[_A, _B](predicate: Callable[[_A, _B], bool], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> bool:
    def _arrow116(x: _A, y: _B, predicate: Any = predicate, xs: Any = xs, ys: Any = ys) -> bool:
        return not predicate(x, y)

    return not exists2(_arrow116, xs, ys)


def try_head[T](xs: IEnumerable_1[T]) -> T | None:
    if is_array_like(xs):
        xs = cast_1(Array[T], xs)
        return try_head_1(xs)

    elif isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return try_head_2(xs)

    else:
        with of_seq(xs) as e:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                return None


def head[T](xs: IEnumerable_1[T]) -> T:
    match_value: T | None = try_head(xs)
    if match_value is None:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")

    else:
        return value_1(match_value)


def initialize[_A](count: int32, f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    def _arrow117(i: int32, count: Any = count, f: Any = f) -> tuple[_A, int32] | None:
        return ((f(i), i + int32.ONE)) if (i < count) else None

    return unfold(_arrow117, int32.ZERO)


def initialize_infinite[_A](f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    return initialize(int32(2147483647), f)


def is_empty[T](xs: IEnumerable_1[Any]) -> bool:
    if is_array_like(xs):
        xs = cast_1(Array[T], xs)
        return len(xs) == int32.ZERO

    elif isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return is_empty_1(xs)

    else:
        with of_seq(xs) as e:
            return not e.System_Collections_IEnumerator_MoveNext()


def try_item[T](index: int32, xs: IEnumerable_1[T]) -> T | None:
    if is_array_like(xs):
        xs = cast_1(Array[T], xs)
        return try_item_1(index, xs)

    elif isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return try_item_2(index, xs)

    else:
        with of_seq(xs) as e:

            def loop(index_1_mut: int32, index: Any = index, xs: Any = xs) -> T | None:
                while True:
                    (index_1,) = (index_1_mut,)
                    if not e.System_Collections_IEnumerator_MoveNext():
                        return None

                    elif index_1 == int32.ZERO:
                        return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

                    else:
                        index_1_mut = index_1 - int32.ONE
                        continue

                    break

            return loop(index)


def item[T](index: int32, xs: IEnumerable_1[T]) -> T:
    match_value: T | None = try_item(index, xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "index")

    else:
        return value_1(match_value)


def iterate[_A](action: Callable[[_A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow118(unit_var: None, x: _A, action: Any = action, xs: Any = xs) -> None:
        action(x)

    fold(_arrow118, None, xs)


def iterate2[_A, _B](action: Callable[[_A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> None:
    def _arrow119(unit_var: None, x: _A, y: _B, action: Any = action, xs: Any = xs, ys: Any = ys) -> None:
        action(x, y)

    fold2(_arrow119, None, xs, ys)


def iterate_indexed[_A](action: Callable[[int32, _A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow120(i: int32, x: _A, action: Any = action, xs: Any = xs) -> int32:
        action(i, x)
        return i + int32.ONE

    ignore(fold(_arrow120, int32.ZERO, xs))


def iterate_indexed2[_A, _B](
    action: Callable[[int32, _A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]
) -> None:
    def _arrow121(i: int32, x: _A, y: _B, action: Any = action, xs: Any = xs, ys: Any = ys) -> int32:
        action(i, x, y)
        return i + int32.ONE

    ignore(fold2(_arrow121, int32.ZERO, xs, ys))


def try_last[T](xs: IEnumerable_1[T]) -> T | None:
    with of_seq(xs) as e:

        def loop(acc_mut: T | None = None, xs: Any = xs) -> T | None:
            while True:
                (acc,) = (acc_mut,)
                if not e.System_Collections_IEnumerator_MoveNext():
                    return acc

                else:
                    acc_mut = e.System_Collections_Generic_IEnumerator_1_get_Current()
                    continue

                break

        if e.System_Collections_IEnumerator_MoveNext():
            return some(loop(e.System_Collections_Generic_IEnumerator_1_get_Current()))

        else:
            return None


def last[T](xs: IEnumerable_1[T]) -> T:
    match_value: T | None = try_last(xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

    else:
        return value_1(match_value)


def length[T](xs: IEnumerable_1[Any]) -> int32:
    if is_array_like(xs):
        xs = cast_1(Array[T], xs)
        return len(xs)

    elif isinstance(xs, FSharpList):
        xs = cast_1(FSharpList[T], xs)
        return length_1(xs)

    else:
        with of_seq(xs) as e:
            count: int32 = int32.ZERO
            while e.System_Collections_IEnumerator_MoveNext():
                count = count + int32.ONE
            return count


def map[T, U](mapping: Callable[[T], U], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow122(__unit: None = None, mapping: Any = mapping, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow123(e: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> U | None:
        return (
            some(mapping(e.System_Collections_Generic_IEnumerator_1_get_Current()))
            if e.System_Collections_IEnumerator_MoveNext()
            else None
        )

    def _arrow124(e_1: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow122, _arrow123, _arrow124)


def map_indexed[T, U](mapping: Callable[[int32, T], U], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow125(__unit: None = None, mapping: Any = mapping, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow126(i: int32, e: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> U | None:
        return (
            some(mapping(i, e.System_Collections_Generic_IEnumerator_1_get_Current()))
            if e.System_Collections_IEnumerator_MoveNext()
            else None
        )

    def _arrow127(e_1: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow125, _arrow126, _arrow127)


def indexed[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[int32, T]]:
    def mapping(i: int32, x: T, xs: Any = xs) -> tuple[int32, T]:
        return (i, x)

    return map_indexed(mapping, xs)


def map2[T1, T2, U](mapping: Callable[[T1, T2], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[U]:
    def _arrow128(
        __unit: None = None, mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> tuple[IEnumerator[T1], IEnumerator[T2]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow129(
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> U | None:
        e1: IEnumerator[T1] = tupled_arg[int32_1(0)]
        e2: IEnumerator[T2] = tupled_arg[int32_1(1)]
        return (
            some(
                mapping(
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
            )
            if (e2.System_Collections_IEnumerator_MoveNext() if e1.System_Collections_IEnumerator_MoveNext() else False)
            else None
        )

    def _arrow130(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> None:
        try:
            dispose_2(tupled_arg_1[int32_1(0)])

        finally:
            dispose_2(tupled_arg_1[int32_1(1)])

    return generate(_arrow128, _arrow129, _arrow130)


def map_indexed2[T1, T2, U](
    mapping: Callable[[int32, T1, T2], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]
) -> IEnumerable_1[U]:
    def _arrow131(
        __unit: None = None, mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> tuple[IEnumerator[T1], IEnumerator[T2]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow132(
        i: int32,
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
    ) -> U | None:
        e1: IEnumerator[T1] = tupled_arg[int32_1(0)]
        e2: IEnumerator[T2] = tupled_arg[int32_1(1)]
        return (
            some(
                mapping(
                    i,
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
            )
            if (e2.System_Collections_IEnumerator_MoveNext() if e1.System_Collections_IEnumerator_MoveNext() else False)
            else None
        )

    def _arrow133(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> None:
        try:
            dispose_2(tupled_arg_1[int32_1(0)])

        finally:
            dispose_2(tupled_arg_1[int32_1(1)])

    return generate_indexed(_arrow131, _arrow132, _arrow133)


def map3[T1, T2, T3, U](
    mapping: Callable[[T1, T2, T3], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], zs: IEnumerable_1[T3]
) -> IEnumerable_1[U]:
    def _arrow134(
        __unit: None = None, mapping: Any = mapping, xs: Any = xs, ys: Any = ys, zs: Any = zs
    ) -> tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]]:
        return (of_seq(xs), of_seq(ys), of_seq(zs))

    def _arrow135(
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
        zs: Any = zs,
    ) -> U | None:
        e1: IEnumerator[T1] = tupled_arg[int32_1(0)]
        e2: IEnumerator[T2] = tupled_arg[int32_1(1)]
        e3: IEnumerator[T3] = tupled_arg[int32_1(2)]
        return (
            some(
                mapping(
                    e1.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e2.System_Collections_Generic_IEnumerator_1_get_Current(),
                    e3.System_Collections_Generic_IEnumerator_1_get_Current(),
                )
            )
            if (
                e3.System_Collections_IEnumerator_MoveNext()
                if (
                    e2.System_Collections_IEnumerator_MoveNext()
                    if e1.System_Collections_IEnumerator_MoveNext()
                    else False
                )
                else False
            )
            else None
        )

    def _arrow136(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
        zs: Any = zs,
    ) -> None:
        try:
            dispose_2(tupled_arg_1[int32_1(0)])

        finally:
            try:
                dispose_2(tupled_arg_1[int32_1(1)])

            finally:
                dispose_2(tupled_arg_1[int32_1(2)])

    return generate(_arrow134, _arrow135, _arrow136)


def read_only[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow137(x: T | None = None, xs: Any = xs) -> T | None:
        return x

    return map(_arrow137, Operators_NullArgCheck("source", xs))


def _expr138(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.CachedSeq`1", [gen0], CachedSeq_1)


class CachedSeq_1[T](IDisposable):
    def __init__(self, cleanup: Callable[[], None], res: IEnumerable_1[Any]) -> None:
        self.cleanup: Callable[[], None] = cleanup
        self.res: IEnumerable_1[T] = res

    def Dispose(self, __unit: None = None) -> None:
        _: CachedSeq_1[T] = self
        _.cleanup()

    def GetEnumerator[T](self, __unit: None = None) -> IEnumerator[T]:
        _: CachedSeq_1[T] = self
        return get_enumerator(_.res)

    def __iter__[T](self) -> IEnumerator[T]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        _: CachedSeq_1[T] = self
        return get_enumerator(_.res)


CachedSeq_1_reflection = _expr138


def CachedSeq_1__ctor_Z7A8347D4(cleanup: Callable[[], None], res: IEnumerable_1[Any]) -> CachedSeq_1[T]:
    return CachedSeq_1(cleanup, res)


def CachedSeq_1__Clear(_: CachedSeq_1[Any]) -> None:
    _.cleanup()


def cache[T](source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    source_1: IEnumerable_1[T] = Operators_NullArgCheck("source", source)
    prefix: list[T] = []
    enumerator_r: Option[IEnumerator[T] | None] = None

    def cleanup(__unit: None = None, source: Any = source) -> None:
        def action_1(__unit: None = None) -> None:
            nonlocal enumerator_r
            clear(prefix)
            (pattern_matching_result, e) = (None, None)
            if enumerator_r is not None:
                if value_1(enumerator_r) is not None:
                    pattern_matching_result = int32_1(0)
                    e = value_1(enumerator_r)

                else:
                    pattern_matching_result = int32_1(1)

            else:
                pattern_matching_result = int32_1(1)

            if pattern_matching_result == int32.ZERO:
                dispose_2(e)

            enumerator_r = None

        lock(prefix, action_1)

    def _arrow139(i_1: int32, source: Any = source) -> tuple[T, int32] | None:
        def action(__unit: None = None) -> tuple[T, int32] | None:
            nonlocal enumerator_r
            if i_1 < len(prefix):
                return (prefix[i_1], i_1 + int32.ONE)

            else:
                if i_1 >= len(prefix):
                    opt_enumerator_2: IEnumerator[T] | None
                    if enumerator_r is not None:
                        opt_enumerator_2 = value_1(enumerator_r)

                    else:
                        opt_enumerator: IEnumerator[T] | None = get_enumerator(source_1)
                        enumerator_r = some(opt_enumerator)
                        opt_enumerator_2 = opt_enumerator

                    if opt_enumerator_2 is None:
                        pass

                    else:
                        enumerator: IEnumerator[T] = opt_enumerator_2
                        if enumerator.System_Collections_IEnumerator_MoveNext():
                            (prefix.append(enumerator.System_Collections_Generic_IEnumerator_1_get_Current()))

                        else:
                            dispose_2(enumerator)
                            enumerator_r = some(None)

                if i_1 < len(prefix):
                    return (prefix[i_1], i_1 + int32.ONE)

                else:
                    return None

        return lock(prefix, action)

    return CachedSeq_1__ctor_Z7A8347D4(cleanup, unfold(_arrow139, int32.ZERO))


def all_pairs[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    ys_cache: IEnumerable_1[T2] = cache(ys)

    def _arrow140(__unit: None = None, xs: Any = xs, ys: Any = ys) -> IEnumerable_1[tuple[T1, T2]]:
        def mapping_1(x: T1 | None = None) -> IEnumerable_1[tuple[T1, T2]]:
            def mapping(y: T2 | None = None, x: Any = x) -> tuple[T1, T2]:
                return (x, y)

            return map(mapping, ys_cache)

        return concat(map(mapping_1, xs))

    return delay(_arrow140)


def map_fold[RESULT, STATE, T](
    mapping: Callable[[STATE, T], tuple[RESULT, STATE]], state: STATE, xs: IEnumerable_1[T]
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[RESULT], STATE] = map_fold_1(mapping, state, to_array(xs), None)
    return (read_only(pattern_input[int32_1(0)]), pattern_input[int32_1(1)])


def map_fold_back[RESULT, STATE, T](
    mapping: Callable[[T, STATE], tuple[RESULT, STATE]], xs: IEnumerable_1[T], state: STATE
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[RESULT], STATE] = map_fold_back_1(mapping, to_array(xs), state, None)
    return (read_only(pattern_input[int32_1(0)]), pattern_input[int32_1(1)])


def try_pick[T, _A](chooser: Callable[[T], _A | None], xs: IEnumerable_1[T]) -> _A | None:
    with of_seq(xs) as e:
        res: _A | None = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            res = chooser(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return res


def pick[T, _A](chooser: Callable[[T], _A | None], xs: IEnumerable_1[T]) -> _A:
    match_value: _A | None = try_pick(chooser, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def reduce[T](folder: Callable[[T, T], T], xs: IEnumerable_1[T]) -> T:
    with of_seq(xs) as e:

        def loop(acc_mut: T | None = None, folder: Any = folder, xs: Any = xs) -> T | None:
            while True:
                (acc,) = (acc_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    acc_mut = folder(acc, e.System_Collections_Generic_IEnumerator_1_get_Current())
                    continue

                else:
                    return acc

                break

        if e.System_Collections_IEnumerator_MoveNext():
            return loop(e.System_Collections_Generic_IEnumerator_1_get_Current())

        else:
            raise Exception(SR_inputSequenceEmpty)


def reduce_back[T](folder: Callable[[T, T], T], xs: IEnumerable_1[T]) -> T:
    arr: Array[T] = to_array(xs)
    if len(arr) > int32.ZERO:
        return reduce_back_1(folder, arr)

    else:
        raise Exception(SR_inputSequenceEmpty)


def replicate[_A](n: int32, x: _A) -> IEnumerable_1[_A]:
    def _arrow141(_arg: int32, n: Any = n, x: Any = x) -> _A:
        return x

    return initialize(n, _arrow141)


def reverse[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow142(__unit: None = None, xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(reverse_1(to_array(xs)))

    return delay(_arrow142)


def scan[STATE, T](folder: Callable[[STATE, T], STATE], state: STATE, xs: IEnumerable_1[T]) -> IEnumerable_1[STATE]:
    def _arrow143(__unit: None = None, folder: Any = folder, state: Any = state, xs: Any = xs) -> IEnumerable_1[STATE]:
        acc: STATE = state

        def mapping(x: T | None = None) -> STATE:
            nonlocal acc
            acc = folder(acc, x)
            return acc

        return concat(to_enumerable([singleton(state), map(mapping, xs)]))

    return delay(_arrow143)


def scan_back[STATE, T](
    folder: Callable[[T, STATE], STATE], xs: IEnumerable_1[T], state: STATE
) -> IEnumerable_1[STATE]:
    def _arrow144(__unit: None = None, folder: Any = folder, xs: Any = xs, state: Any = state) -> IEnumerable_1[STATE]:
        return of_array(scan_back_1(folder, to_array(xs), state, None))

    return delay(_arrow144)


def skip[T](count: int32, source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow145(__unit: None = None, count: Any = count, source: Any = source) -> IEnumerator[T]:
        e: IEnumerator[T] = of_seq(source)
        try:
            for _ in range(int32.ONE, count, 1):
                if not e.System_Collections_IEnumerator_MoveNext():
                    raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

            def compensation(__unit: None = None) -> None:
                pass

            return Enumerator_enumerateThenFinally(compensation, e)

        except Exception as match_value:
            dispose_2(e)
            raise match_value

    return mk_seq(_arrow145)


def skip_while[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow146(__unit: None = None, predicate: Any = predicate, xs: Any = xs) -> IEnumerable_1[T]:
        skipped: bool = True

        def f(x: T | None = None) -> bool:
            nonlocal skipped
            if skipped:
                skipped = predicate(x)

            return not skipped

        return filter(f, xs)

    return delay(_arrow146)


def tail[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return skip(int32.ONE, xs)


def take[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow147(__unit: None = None, count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow148(i: int32, e: IEnumerator[T], count: Any = count, xs: Any = xs) -> T | None:
        if i < count:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

        else:
            return None

    def _arrow149(e_1: IEnumerator[T], count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow147, _arrow148, _arrow149)


def take_while[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow150(__unit: None = None, predicate: Any = predicate, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow151(e: IEnumerator[T], predicate: Any = predicate, xs: Any = xs) -> T | None:
        return (
            some(e.System_Collections_Generic_IEnumerator_1_get_Current())
            if (
                predicate(e.System_Collections_Generic_IEnumerator_1_get_Current())
                if e.System_Collections_IEnumerator_MoveNext()
                else False
            )
            else None
        )

    def _arrow152(e_1: IEnumerator[T], predicate: Any = predicate, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow150, _arrow151, _arrow152)


def truncate[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow153(__unit: None = None, count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow154(i: int32, e: IEnumerator[T], count: Any = count, xs: Any = xs) -> T | None:
        return (
            some(e.System_Collections_Generic_IEnumerator_1_get_Current())
            if (e.System_Collections_IEnumerator_MoveNext() if (i < count) else False)
            else None
        )

    def _arrow155(e_1: IEnumerator[T], count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow153, _arrow154, _arrow155)


def zip[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    def _arrow156(x: T1, y: T2, xs: Any = xs, ys: Any = ys) -> tuple[T1, T2]:
        return (x, y)

    return map2(_arrow156, xs, ys)


def zip3[T1, T2, T3](
    xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], zs: IEnumerable_1[T3]
) -> IEnumerable_1[tuple[T1, T2, T3]]:
    def _arrow157(x: T1, y: T2, z: T3, xs: Any = xs, ys: Any = ys, zs: Any = zs) -> tuple[T1, T2, T3]:
        return (x, y, z)

    return map3(_arrow157, xs, ys, zs)


def collect[COLLECTION, T, U](mapping: Callable[[T], COLLECTION], xs: IEnumerable_1[T]) -> IEnumerable_1[Any]:
    def _arrow158(__unit: None = None, mapping: Any = mapping, xs: Any = xs) -> IEnumerable_1[U]:
        return concat(map(mapping, xs))

    return delay(_arrow158)


def where[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return filter(predicate, xs)


def pairwise[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[T, T]]:
    def _arrow159(__unit: None = None, xs: Any = xs) -> IEnumerable_1[tuple[T, T]]:
        return of_array(pairwise_1(to_array(xs)))

    return delay(_arrow159)


def split_into[T](chunks: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow160(__unit: None = None, chunks: Any = chunks, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(split_into_1(chunks, to_array(xs)))

    return delay(_arrow160)


def windowed[T](window_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow161(__unit: None = None, window_size: Any = window_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(windowed_1(window_size, to_array(xs)))

    return delay(_arrow161)


def transpose[T, _A](xss: IEnumerable_1[Any]) -> IEnumerable_1[IEnumerable_1[Any]]:
    def _arrow162(__unit: None = None, xss: Any = xss) -> IEnumerable_1[IEnumerable_1[T]]:
        return of_array(map_1(of_array, transpose_1(map_1(to_array, to_array(xss), None), None), None))

    return delay(_arrow162)


def sort_with[T](comparer: Callable[[T, T], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow163(__unit: None = None, comparer: Any = comparer, xs: Any = xs) -> IEnumerable_1[T]:
        arr: Array[T] = to_array(xs)
        sort_in_place_with(comparer, arr)
        return of_array(arr)

    return delay(_arrow163)


def sort[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow164(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y)

    return sort_with(_arrow164, xs)


def sort_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> IEnumerable_1[T]:
    def _arrow165(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y))

    return sort_with(_arrow165, xs)


def sort_descending[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow166(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y) * int32.NEG_ONE

    return sort_with(_arrow166, xs)


def sort_by_descending[T, U](
    projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]
) -> IEnumerable_1[T]:
    def _arrow167(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y)) * int32.NEG_ONE

    return sort_with(_arrow167, xs)


def sum[T](xs: IEnumerable_1[T], adder: IGenericAdder_1[T]) -> T:
    def _arrow168(acc: T, x: T, xs: Any = xs, adder: Any = adder) -> T:
        return adder.Add(acc, x)

    return fold(_arrow168, adder.GetZero(), xs)


def sum_by[T, U](f: Callable[[T], U], xs: IEnumerable_1[T], adder: IGenericAdder_1[U]) -> U:
    def _arrow169(acc: U, x: T, f: Any = f, xs: Any = xs, adder: Any = adder) -> U:
        return adder.Add(acc, f(x))

    return fold(_arrow169, adder.GetZero(), xs)


def max_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow170(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else x

    return reduce(_arrow170, xs)


def max[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow171(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(y, x) > int32.ZERO) else x

    return reduce(_arrow171, xs)


def min_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow172(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else y

    return reduce(_arrow172, xs)


def min[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow173(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(y, x) > int32.ZERO) else y

    return reduce(_arrow173, xs)


def average[T](xs: IEnumerable_1[T], averager: IGenericAverager_1[T]) -> T:
    count: int32 = int32.ZERO

    def folder(acc: T, x: T, xs: Any = xs, averager: Any = averager) -> T:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, x)

    total: T = fold(folder, averager.GetZero(), xs)
    if count == int32.ZERO:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")

    else:
        return averager.DivideByInt(total, count)


def average_by[T, U](f: Callable[[T], U], xs: IEnumerable_1[T], averager: IGenericAverager_1[U]) -> U:
    count: int32 = int32.ZERO

    def _arrow174(acc: U, x: T, f: Any = f, xs: Any = xs, averager: Any = averager) -> U:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, f(x))

    total: U = fold(_arrow174, averager.GetZero(), xs)
    if count == int32.ZERO:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")

    else:
        return averager.DivideByInt(total, count)


def permute[T](f: Callable[[int32], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow175(__unit: None = None, f: Any = f, xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(permute_1(f, to_array(xs)))

    return delay(_arrow175)


def chunk_by_size[T](chunk_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow176(__unit: None = None, chunk_size: Any = chunk_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(chunk_by_size_1(chunk_size, to_array(xs)))

    return delay(_arrow176)


def insert_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow177(__unit: None = None, index: Any = index, y: Any = y, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow178(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> T | None:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if is_done else (i < index)) else False:
            return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

        elif i == index:
            is_done = True
            return some(y)

        else:
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

            return None

    def _arrow179(e_1: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow177, _arrow178, _arrow179)


def insert_many_at[T](index: int32, ys: IEnumerable_1[T], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    status: int32 = int32.NEG_ONE
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow180(
        __unit: None = None, index: Any = index, ys: Any = ys, xs: Any = xs
    ) -> tuple[IEnumerator[T], IEnumerator[T]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow181(
        i: int32, tupled_arg: tuple[IEnumerator[T], IEnumerator[T]], index: Any = index, ys: Any = ys, xs: Any = xs
    ) -> T | None:
        nonlocal status
        e1: IEnumerator[T] = tupled_arg[int32_1(0)]
        e2: IEnumerator[T] = tupled_arg[int32_1(1)]
        if i == index:
            status = int32.ZERO

        inserted: T | None
        if status == int32.ZERO:
            if e2.System_Collections_IEnumerator_MoveNext():
                inserted = some(e2.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                status = int32.ONE
                inserted = None

        else:
            inserted = None

        if inserted is None:
            if e1.System_Collections_IEnumerator_MoveNext():
                return some(e1.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                if status < int32.ONE:
                    raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

                return None

        else:
            return some(value_1(inserted))

    def _arrow182(
        tupled_arg_1: tuple[IEnumerator[T], IEnumerator[T]], index: Any = index, ys: Any = ys, xs: Any = xs
    ) -> None:
        dispose_2(tupled_arg_1[int32_1(0)])
        dispose_2(tupled_arg_1[int32_1(1)])

    return generate_indexed(_arrow180, _arrow181, _arrow182)


def remove_at[T](index: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow183(__unit: None = None, index: Any = index, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow184(i: int32, e: IEnumerator[T], index: Any = index, xs: Any = xs) -> T | None:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if is_done else (i < index)) else False:
            return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else False:
            is_done = True
            return (
                some(e.System_Collections_Generic_IEnumerator_1_get_Current())
                if e.System_Collections_IEnumerator_MoveNext()
                else None
            )

        else:
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

            return None

    def _arrow185(e_1: IEnumerator[T], index: Any = index, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow183, _arrow184, _arrow185)


def remove_many_at[T](index: int32, count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow186(__unit: None = None, index: Any = index, count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow187(i: int32, e: IEnumerator[T], index: Any = index, count: Any = count, xs: Any = xs) -> T | None:
        if i < index:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

        else:
            if i == index:
                for _ in range(int32.ONE, count, 1):
                    if not e.System_Collections_IEnumerator_MoveNext():
                        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "count")

            return (
                some(e.System_Collections_Generic_IEnumerator_1_get_Current())
                if e.System_Collections_IEnumerator_MoveNext()
                else None
            )

    def _arrow188(e_1: IEnumerator[T], index: Any = index, count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow186, _arrow187, _arrow188)


def update_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow189(__unit: None = None, index: Any = index, y: Any = y, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow190(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> T | None:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if is_done else (i < index)) else False:
            return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else False:
            is_done = True
            return some(y)

        else:
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

            return None

    def _arrow191(e_1: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow189, _arrow190, _arrow191)


__all__ = [
    "SR_enumerationAlreadyFinished",
    "SR_enumerationNotStarted",
    "SR_inputSequenceEmpty",
    "SR_inputSequenceTooLong",
    "SR_keyNotFoundAlt",
    "SR_notEnoughElements",
    "SR_resetNotSupported",
    "Enumerator_noReset",
    "Enumerator_notStarted",
    "Enumerator_alreadyFinished",
    "Enumerator_Seq_reflection",
    "Enumerator_FromFunctions_1_reflection",
    "Enumerator_cast",
    "Enumerator_concat",
    "Enumerator_enumerateThenFinally",
    "Enumerator_generateWhileSome",
    "Enumerator_unfold",
    "index_not_found",
    "mk_seq",
    "of_seq",
    "delay",
    "concat",
    "unfold",
    "empty",
    "singleton",
    "of_array",
    "to_array",
    "of_list",
    "to_list",
    "generate",
    "generate_indexed",
    "append",
    "cast",
    "choose",
    "compare_with",
    "contains",
    "enumerate_from_functions",
    "enumerate_then_finally",
    "enumerate_using",
    "enumerate_while",
    "filter",
    "exists",
    "exists2",
    "exactly_one",
    "try_exactly_one",
    "try_find",
    "find",
    "try_find_back",
    "find_back",
    "try_find_index",
    "find_index",
    "try_find_index_back",
    "find_index_back",
    "fold",
    "fold_back",
    "fold2",
    "fold_back2",
    "for_all",
    "for_all2",
    "try_head",
    "head",
    "initialize",
    "initialize_infinite",
    "is_empty",
    "try_item",
    "item",
    "iterate",
    "iterate2",
    "iterate_indexed",
    "iterate_indexed2",
    "try_last",
    "last",
    "length",
    "map",
    "map_indexed",
    "indexed",
    "map2",
    "map_indexed2",
    "map3",
    "read_only",
    "CachedSeq_1_reflection",
    "CachedSeq_1__Clear",
    "cache",
    "all_pairs",
    "map_fold",
    "map_fold_back",
    "try_pick",
    "pick",
    "reduce",
    "reduce_back",
    "replicate",
    "reverse",
    "scan",
    "scan_back",
    "skip",
    "skip_while",
    "tail",
    "take",
    "take_while",
    "truncate",
    "zip",
    "zip3",
    "collect",
    "where",
    "pairwise",
    "split_into",
    "windowed",
    "transpose",
    "sort_with",
    "sort",
    "sort_by",
    "sort_descending",
    "sort_by_descending",
    "sum",
    "sum_by",
    "max_by",
    "max",
    "min_by",
    "min",
    "average",
    "average_by",
    "permute",
    "chunk_by_size",
    "insert_at",
    "insert_many_at",
    "remove_at",
    "remove_many_at",
    "update_at",
]
