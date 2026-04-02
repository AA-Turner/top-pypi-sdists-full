from __future__ import annotations

from collections.abc import Callable
from typing import Any
from typing import cast as cast_1

from .array_ import Array, sort_in_place_with
from .array_ import chunk_by_size as chunk_by_size_1
from .array_ import empty as empty_1
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
from .bases import DisposableBase, EnumerableBase, EnumeratorBase, StringableBase
from .core import int32
from .exceptions import to_string
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
from .option import Option, erase, some
from .option import value as value_1
from .protocols import IComparer_1, IDisposable, IEnumerable, IEnumerable_1, IEnumerator, IEqualityComparer_1
from .reflection import TypeInfo, class_type
from .system import InvalidOperationException__ctor_Z721C83C5, NotSupportedException__ctor_Z721C83C5
from .util import (
    UNIT,
    Disposable,
    Unit,
    clear,
    equals,
    get_enumerator,
    ignore,
    is_disposable,
    lock,
    nullable,
    range,
    to_enumerable,
)
from .util import dispose as dispose_2


SR_enumerationAlreadyFinished: str = "Enumeration already finished."

SR_enumerationNotStarted: str = "Enumeration has not started. Call MoveNext."

SR_inputSequenceEmpty: str = "The input sequence was empty."

SR_inputSequenceTooLong: str = "The input sequence contains more than one element."

SR_keyNotFoundAlt: str = "An index satisfying the predicate was not found in the collection."

SR_notEnoughElements: str = "The input sequence has an insufficient number of elements."

SR_resetNotSupported: str = "Reset is not supported on this enumerator."


def Enumerator_noReset[_A](__unit: Unit = UNIT) -> Any:
    raise NotSupportedException__ctor_Z721C83C5(SR_resetNotSupported)


def Enumerator_notStarted[_A](__unit: Unit = UNIT) -> Any:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationNotStarted)


def Enumerator_alreadyFinished[_A](__unit: Unit = UNIT) -> Any:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationAlreadyFinished)


def _expr97(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.Seq", Array([gen0]), Enumerator_Seq)


class Enumerator_Seq[T](StringableBase, EnumerableBase[T]):
    def __init__(self, f: Callable[[], IEnumerator[T]]) -> None:
        self.f: Callable[[], IEnumerator[T]] = f

    def ToString(self, __unit: Unit = UNIT) -> str:
        xs: Enumerator_Seq[T] = self
        i: int32 = int32.ZERO
        str_1: str = "seq ["
        with Disposable(get_enumerator(xs)) as e:
            while e.System_Collections_IEnumerator_MoveNext() if (i < int32.FOUR) else False:
                if i > int32.ZERO:
                    str_1 = str_1 + "; "

                str_1 = str_1 + to_string(e.System_Collections_Generic_IEnumerator_1_get_Current())
                i = i + int32.ONE
            if i == int32.FOUR:
                str_1 = str_1 + "; ..."

            return str_1 + "]"

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        x: Enumerator_Seq[T] = self
        return x.f()

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        x: Enumerator_Seq[T] = self
        return x.f()


Enumerator_Seq_reflection = _expr97


def Enumerator_Seq__ctor_673A07F2[T](f: Callable[[], IEnumerator[T]]) -> Enumerator_Seq[T]:
    return Enumerator_Seq(f)


def _expr98(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.FromFunctions`1", Array([gen0]), Enumerator_FromFunctions_1)


class Enumerator_FromFunctions_1[T](EnumeratorBase[T], DisposableBase):
    def __init__(self, current: Callable[[], T], next_1: Callable[[], bool], dispose: Callable[[], None]) -> None:
        self.current: Callable[[], T] = current
        self.next: Callable[[], bool] = next_1
        self.dispose: Callable[[], None] = dispose

    def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: Unit = UNIT) -> T:
        _: Enumerator_FromFunctions_1[T] = self
        return _.current()

    def System_Collections_IEnumerator_get_Current(self, __unit: Unit = UNIT) -> Any:
        _: Enumerator_FromFunctions_1[T] = self
        return _.current()

    def System_Collections_IEnumerator_MoveNext(self, __unit: Unit = UNIT) -> bool:
        _: Enumerator_FromFunctions_1[T] = self
        return _.next()

    def System_Collections_IEnumerator_Reset(self, __unit: Unit = UNIT) -> None:
        Enumerator_noReset()

    def Dispose(self, __unit: Unit = UNIT) -> None:
        _: Enumerator_FromFunctions_1[T] = self
        _.dispose()


Enumerator_FromFunctions_1_reflection = _expr98


def Enumerator_FromFunctions_1__ctor_58C54629[T](
    current: Callable[[], T], next_1: Callable[[], bool], dispose: Callable[[], None]
) -> Enumerator_FromFunctions_1[T]:
    return Enumerator_FromFunctions_1(current, next_1, dispose)


def Enumerator_cast[T](e: IEnumerator[T]) -> IEnumerator[T]:
    def current(e: Any = e) -> T:
        return e.System_Collections_Generic_IEnumerator_1_get_Current()

    def next_1(e: Any = e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()

    def dispose(e: Any = e) -> None:
        dispose_2(e)

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_concat[T, U: IEnumerable](sources: IEnumerable_1[Any]) -> IEnumerator[Any]:
    outer_opt: IEnumerator[U] | None = cast_1(IEnumerator[U] | None, None)
    inner_opt: IEnumerator[T] | None = cast_1(IEnumerator[T] | None, None)
    started: bool = False
    finished: bool = False
    curr: Option[T] = cast_1(Option[T], None)

    def finish(sources: Any = sources) -> None:
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

    def current(sources: Any = sources) -> T:
        if not started:
            Enumerator_notStarted()

        elif finished:
            Enumerator_alreadyFinished()

        if curr is not None:
            return value_1(curr)

        else:
            return Enumerator_alreadyFinished()

    def next_1(sources: Any = sources) -> bool:
        nonlocal started
        if not started:
            started = True

        if finished:
            return False

        else:
            res: bool | None = cast_1(bool | None, None)
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

                            def _arrow99(__unit: Unit = UNIT) -> IEnumerator[T]:
                                copy_of_struct: U = ie
                                return get_enumerator(copy_of_struct)

                            inner_opt = _arrow99()

                        else:
                            finish()
                            res = False

                else:
                    outer_opt = get_enumerator(sources)

            return value_1(res)

    def dispose(sources: Any = sources) -> None:
        if not finished:
            finish()

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_enumerateThenFinally[T](f: Callable[[], None], e: IEnumerator[T]) -> IEnumerator[T]:
    def current(f: Any = f, e: Any = e) -> T:
        return e.System_Collections_Generic_IEnumerator_1_get_Current()

    def next_1(f: Any = f, e: Any = e) -> bool:
        return e.System_Collections_IEnumerator_MoveNext()

    def dispose(f: Any = f, e: Any = e) -> None:
        try:
            dispose_2(e)

        finally:
            f()

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_generateWhileSome[T, U](
    openf: Callable[[], T], compute: Callable[[T], Option[U]], closef: Callable[[T], None]
) -> IEnumerator[U]:
    started: bool = False
    curr: Option[U] = cast_1(Option[U], None)
    state: Option[T] = some(openf())

    def dispose(openf: Any = openf, compute: Any = compute, closef: Any = closef) -> None:
        nonlocal state
        if state is not None:
            x_1: T = value_1(state)
            try:
                closef(x_1)

            finally:
                state = None

    def finish(openf: Any = openf, compute: Any = compute, closef: Any = closef) -> None:
        nonlocal curr
        try:
            dispose()

        finally:
            curr = None

    def current(openf: Any = openf, compute: Any = compute, closef: Any = closef) -> U:
        if not started:
            Enumerator_notStarted()

        if curr is not None:
            return value_1(curr)

        else:
            return Enumerator_alreadyFinished()

    def next_1(openf: Any = openf, compute: Any = compute, closef: Any = closef) -> bool:
        nonlocal started, curr
        if not started:
            started = True

        if state is not None:
            s: T = value_1(state)
            match_value_1: Option[U]
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
    curr: tuple[T, STATE] | None = cast_1(tuple[T, STATE] | None, None)
    acc: STATE = state

    def current(f: Any = f, state: Any = state) -> T:
        if curr is not None:
            x: T = curr[0]
            st: STATE = curr[1]
            return x

        else:
            return Enumerator_notStarted()

    def next_1(f: Any = f, state: Any = state) -> bool:
        nonlocal curr, acc
        curr = f(acc)
        if curr is not None:
            x_1: T = curr[0]
            st_1: STATE = curr[1]
            acc = st_1
            return True

        else:
            return False

    def dispose(f: Any = f, state: Any = state) -> None:
        pass

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def index_not_found[_A](__unit: Unit = UNIT) -> Any:
    raise Exception(SR_keyNotFoundAlt)


def mk_seq[T](f: Callable[[], IEnumerator[T]]) -> IEnumerable_1[T]:
    return Enumerator_Seq__ctor_673A07F2(f)


def of_seq[T](xs: IEnumerable_1[T]) -> IEnumerator[T]:
    return get_enumerator(Operators_NullArgCheck("source", xs))


def delay[T](generator: Callable[[], IEnumerable_1[T]]) -> IEnumerable_1[T]:
    def _arrow100(generator: Any = generator) -> IEnumerator[T]:
        return get_enumerator(generator())

    return mk_seq(_arrow100)


def concat[COLLECTION: IEnumerable, T](sources: IEnumerable_1[Any]) -> IEnumerable_1[Any]:
    def _arrow101(sources: Any = sources) -> IEnumerator[T]:
        return Enumerator_concat(sources)

    return mk_seq(_arrow101)


def unfold[STATE, T](generator: Callable[[STATE], tuple[T, STATE] | None], state: STATE) -> IEnumerable_1[T]:
    def _arrow102(generator: Any = generator, state: Any = state) -> IEnumerator[T]:
        return Enumerator_unfold(generator, state)

    return mk_seq(_arrow102)


def empty[T](__unit: Unit = UNIT) -> IEnumerable_1[Any]:
    def _arrow103(__unit: Unit = UNIT) -> IEnumerable_1[T]:
        return empty_1()

    return delay(_arrow103)


def singleton[T](x: T = UNIT) -> IEnumerable_1[T]:
    def _arrow104(x: Any = x) -> IEnumerable_1[T]:
        return singleton_1(x, None)

    return delay(_arrow104)


def of_array[T](arr: Array[T]) -> IEnumerable_1[T]:
    return arr


def to_array[T](xs: IEnumerable_1[T]) -> Array[T]:
    if isinstance(xs, FSharpList):
        return to_array_1(xs)

    else:
        return of_seq_1(xs)


def of_list[T](xs: FSharpList[T]) -> IEnumerable_1[T]:
    return xs


def to_list[T](xs: IEnumerable_1[T]) -> FSharpList[T]:
    if isinstance(xs, Array):
        return of_array_1(xs)

    elif isinstance(xs, FSharpList):
        return xs

    else:
        return of_seq_2(xs)


def generate[_A, _B](
    create: Callable[[], _A], compute: Callable[[_A], Option[_B]], dispose: Callable[[_A], None]
) -> IEnumerable_1[_B]:
    def _arrow105(create: Any = create, compute: Any = compute, dispose: Any = dispose) -> IEnumerator[_B]:
        return Enumerator_generateWhileSome(create, compute, dispose)

    return mk_seq(_arrow105)


def generate_indexed[_A, _B](
    create: Callable[[], _A], compute: Callable[[int32, _A], Option[_B]], dispose: Callable[[_A], None]
) -> IEnumerable_1[_B]:
    def _arrow107(create: Any = create, compute: Any = compute, dispose: Any = dispose) -> IEnumerator[_B]:
        i: int32 = int32.NEG_ONE

        def _arrow106(x: _A = UNIT) -> Option[_B]:
            nonlocal i
            i = i + int32.ONE
            return compute(i, x)

        return Enumerator_generateWhileSome(create, _arrow106, dispose)

    return mk_seq(_arrow107)


def append[T](xs: IEnumerable_1[T], ys: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return concat(to_enumerable([xs, ys]))


def cast[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow108(xs: Any = xs) -> IEnumerator[T]:
        return Enumerator_cast(get_enumerator(Operators_NullArgCheck("source", xs)))

    return mk_seq(_arrow108)


def choose[T, U](chooser: Callable[[T], Option[U]], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow109(chooser: Any = chooser, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow110(e: IEnumerator[T], chooser: Any = chooser, xs: Any = xs) -> Option[U]:
        curr: Option[U] = cast_1(Option[U], None)
        while e.System_Collections_IEnumerator_MoveNext() if (curr is None) else False:
            curr = chooser(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return curr

    def _arrow111(e_1: IEnumerator[T], chooser: Any = chooser, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow109, _arrow110, _arrow111)


def compare_with[T](comparer: Callable[[T, T], int32], xs: IEnumerable_1[T], ys: IEnumerable_1[T]) -> int32:
    with Disposable(of_seq(xs)) as e1:
        with Disposable(of_seq(ys)) as e2:
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
    with Disposable(of_seq(xs)) as e:
        found: bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else False:
            found = comparer.Equals(value, e.System_Collections_Generic_IEnumerator_1_get_Current())
        return found


def enumerate_from_functions[_A, _B](
    create: Callable[[], _A], move_next: Callable[[_A], bool], current: Callable[[_A], _B]
) -> IEnumerable_1[_B]:
    def _arrow112(x: _A = UNIT, create: Any = create, move_next: Any = move_next, current: Any = current) -> Option[_B]:
        return some(current(x)) if move_next(x) else None

    def _arrow113(x_1: _A = UNIT, create: Any = create, move_next: Any = move_next, current: Any = current) -> None:
        match_value: Any = x_1
        if is_disposable(match_value):
            dispose_2(match_value)

    return generate(create, _arrow112, _arrow113)


def enumerate_then_finally[T](source: IEnumerable_1[T], compensation: Callable[[], None]) -> IEnumerable_1[T]:
    compensation_1: Callable[[], None] = compensation

    def _arrow114(source: Any = source, compensation: Any = compensation) -> IEnumerator[T]:
        try:
            return Enumerator_enumerateThenFinally(compensation_1, of_seq(source))

        except Exception as match_value:
            compensation_1()
            raise match_value

    return mk_seq(_arrow114)


def enumerate_using[T: IDisposable, _A: IEnumerable, U](resource: T, source: Callable[[T], Any]) -> IEnumerable_1[Any]:
    def compensation(resource: Any = resource, source: Any = source) -> None:
        if equals(resource, cast_1(Any, None)):
            pass

        else:
            copy_of_struct: T = resource
            dispose_2(copy_of_struct)

    def _arrow115(resource: Any = resource, source: Any = source) -> IEnumerator[U]:
        try:
            return Enumerator_enumerateThenFinally(compensation, of_seq(source(resource)))

        except Exception as match_value_1:
            compensation()
            raise match_value_1

    return mk_seq(_arrow115)


def enumerate_while[T](guard: Callable[[], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow116(i: int32, guard: Any = guard, xs: Any = xs) -> tuple[IEnumerable_1[T], int32] | None:
        return ((xs, i + int32.ONE)) if guard() else None

    return concat(unfold(_arrow116, int32.ZERO))


def filter[T](f: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def chooser(x: T = UNIT, f: Any = f, xs: Any = xs) -> Option[T]:
        if f(x):
            return some(x)

        else:
            return None

    return choose(chooser, xs)


def exists[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> bool:
    with Disposable(of_seq(xs)) as e:
        found: bool = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else False:
            found = predicate(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return found


def exists2[T1, T2](predicate: Callable[[T1, T2], bool], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> bool:
    with Disposable(of_seq(xs)) as e1:
        with Disposable(of_seq(ys)) as e2:
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
    with Disposable(of_seq(xs)) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                raise Exception((SR_inputSequenceTooLong + "\\nParameter name: ") + "source")

            else:
                return v

        else:
            raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")


def try_exactly_one[T](xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                return None

            else:
                return some(v)

        else:
            return None


def try_find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:
        res: Option[T] = cast_1(Option[T], None)
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            c: T = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if predicate(c):
                res = some(c)

        return res


def find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: Option[T] = try_find(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> Option[T]:
    return try_find_back_1(predicate, to_array(xs))


def find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: Option[T] = try_find_back(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_index[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32 | None:
    with Disposable(of_seq(xs)) as e:

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
    match_value: int32 | None = erase(try_find_index(predicate, xs))
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def try_find_index_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32 | None:
    return erase(try_find_index_back_1(predicate, to_array(xs)))


def find_index_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32:
    match_value: int32 | None = erase(try_find_index_back(predicate, xs))
    if match_value is None:
        index_not_found()
        return int32.NEG_ONE

    else:
        return match_value


def fold[T, STATE](folder: Callable[[STATE, T], STATE], state: STATE, xs: IEnumerable_1[T]) -> STATE:
    with Disposable(of_seq(xs)) as e:
        acc: STATE = state
        while e.System_Collections_IEnumerator_MoveNext():
            acc = folder(acc, e.System_Collections_Generic_IEnumerator_1_get_Current())
        return acc


def fold_back[T, STATE](folder: Callable[[T, Any], Any], xs: IEnumerable_1[T], state: Any = None) -> Any:
    return fold_back_1(folder, to_array(xs), state)


def fold2[T1, T2, STATE](
    folder: Callable[[STATE, T1, T2], STATE], state: STATE, xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]
) -> STATE:
    with Disposable(of_seq(xs)) as e1:
        with Disposable(of_seq(ys)) as e2:
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


def fold_back2[T1, T2, STATE](
    folder: Callable[[T1, T2, STATE], STATE], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], state: STATE
) -> STATE:
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def for_all[_A](predicate: Callable[[_A], bool], xs: IEnumerable_1[_A]) -> bool:
    def _arrow117(x: _A = UNIT, predicate: Any = predicate, xs: Any = xs) -> bool:
        return not predicate(x)

    return not exists(_arrow117, xs)


def for_all2[_A, _B](predicate: Callable[[_A, _B], bool], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> bool:
    def _arrow118(x: _A, y: _B, predicate: Any = predicate, xs: Any = xs, ys: Any = ys) -> bool:
        return not predicate(x, y)

    return not exists2(_arrow118, xs, ys)


def try_head[T](xs: IEnumerable_1[T]) -> Option[T]:
    if isinstance(xs, Array):
        return try_head_1(xs)

    elif isinstance(xs, FSharpList):
        return try_head_2(xs)

    else:
        with Disposable(of_seq(xs)) as e:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                return None


def head[T](xs: IEnumerable_1[T]) -> T:
    match_value: Option[T] = try_head(xs)
    if match_value is None:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")

    else:
        return value_1(match_value)


def initialize[_A](count: int32, f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    def _arrow119(i: int32, count: Any = count, f: Any = f) -> tuple[_A, int32] | None:
        return ((f(i), i + int32.ONE)) if (i < count) else None

    return unfold(_arrow119, int32.ZERO)


def initialize_infinite[_A](f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    return initialize(int32(2147483647), f)


def is_empty[T](xs: IEnumerable_1[Any]) -> bool:
    if isinstance(xs, Array):
        return len(xs) == int32.ZERO

    elif isinstance(xs, FSharpList):
        return is_empty_1(xs)

    else:
        with Disposable(of_seq(xs)) as e:
            return not e.System_Collections_IEnumerator_MoveNext()


def try_item[T](index: int32, xs: IEnumerable_1[T]) -> Option[T]:
    if isinstance(xs, Array):
        return try_item_1(index, xs)

    elif isinstance(xs, FSharpList):
        return try_item_2(index, xs)

    else:
        with Disposable(of_seq(xs)) as e:

            def loop(index_1_mut: int32, index: Any = index, xs: Any = xs) -> Option[T]:
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
    match_value: Option[T] = try_item(index, xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "index")

    else:
        return value_1(match_value)


def iterate[_A](action: Callable[[_A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow120(unit_var: None, x: _A, action: Any = action, xs: Any = xs) -> None:
        action(x)

    fold(_arrow120, None, xs)


def iterate2[_A, _B](action: Callable[[_A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> None:
    def _arrow121(unit_var: None, x: _A, y: _B, action: Any = action, xs: Any = xs, ys: Any = ys) -> None:
        action(x, y)

    fold2(_arrow121, None, xs, ys)


def iterate_indexed[_A](action: Callable[[int32, _A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow122(i: int32, x: _A, action: Any = action, xs: Any = xs) -> int32:
        action(i, x)
        return i + int32.ONE

    ignore(fold(_arrow122, int32.ZERO, xs))


def iterate_indexed2[_A, _B](
    action: Callable[[int32, _A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]
) -> None:
    def _arrow123(i: int32, x: _A, y: _B, action: Any = action, xs: Any = xs, ys: Any = ys) -> int32:
        action(i, x, y)
        return i + int32.ONE

    ignore(fold2(_arrow123, int32.ZERO, xs, ys))


def try_last[T](xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:

        def loop(acc_mut: T = UNIT, xs: Any = xs) -> T:
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
    match_value: Option[T] = try_last(xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

    else:
        return value_1(match_value)


def length[T](xs: IEnumerable_1[Any]) -> int32:
    if isinstance(xs, Array):
        return int32(len(xs))

    elif isinstance(xs, FSharpList):
        return length_1(xs)

    else:
        with Disposable(of_seq(xs)) as e:
            count: int32 = int32.ZERO
            while e.System_Collections_IEnumerator_MoveNext():
                count = count + int32.ONE
            return count


def map[T, U](mapping: Callable[[T], U], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow124(mapping: Any = mapping, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow125(e: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> Option[U]:
        return (
            some(mapping(e.System_Collections_Generic_IEnumerator_1_get_Current()))
            if e.System_Collections_IEnumerator_MoveNext()
            else None
        )

    def _arrow126(e_1: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow124, _arrow125, _arrow126)


def map_indexed[T, U](mapping: Callable[[int32, T], U], xs: IEnumerable_1[T]) -> IEnumerable_1[U]:
    def _arrow127(mapping: Any = mapping, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow128(i: int32, e: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> Option[U]:
        return (
            some(mapping(i, e.System_Collections_Generic_IEnumerator_1_get_Current()))
            if e.System_Collections_IEnumerator_MoveNext()
            else None
        )

    def _arrow129(e_1: IEnumerator[T], mapping: Any = mapping, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow127, _arrow128, _arrow129)


def indexed[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[int32, T]]:
    def mapping(i: int32, x: T, xs: Any = xs) -> tuple[int32, T]:
        return (i, x)

    return map_indexed(mapping, xs)


def map2[T1, T2, U](mapping: Callable[[T1, T2], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[U]:
    def _arrow130(mapping: Any = mapping, xs: Any = xs, ys: Any = ys) -> tuple[IEnumerator[T1], IEnumerator[T2]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow131(
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> Option[U]:
        e1: IEnumerator[T1] = tupled_arg[0]
        e2: IEnumerator[T2] = tupled_arg[1]
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

    def _arrow132(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> None:
        try:
            dispose_2(tupled_arg_1[0])

        finally:
            dispose_2(tupled_arg_1[1])

    return generate(_arrow130, _arrow131, _arrow132)


def map_indexed2[T1, T2, U](
    mapping: Callable[[int32, T1, T2], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]
) -> IEnumerable_1[U]:
    def _arrow133(mapping: Any = mapping, xs: Any = xs, ys: Any = ys) -> tuple[IEnumerator[T1], IEnumerator[T2]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow134(
        i: int32,
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
    ) -> Option[U]:
        e1: IEnumerator[T1] = tupled_arg[0]
        e2: IEnumerator[T2] = tupled_arg[1]
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

    def _arrow135(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2]], mapping: Any = mapping, xs: Any = xs, ys: Any = ys
    ) -> None:
        try:
            dispose_2(tupled_arg_1[0])

        finally:
            dispose_2(tupled_arg_1[1])

    return generate_indexed(_arrow133, _arrow134, _arrow135)


def map3[T1, T2, T3, U](
    mapping: Callable[[T1, T2, T3], U], xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], zs: IEnumerable_1[T3]
) -> IEnumerable_1[U]:
    def _arrow136(
        mapping: Any = mapping, xs: Any = xs, ys: Any = ys, zs: Any = zs
    ) -> tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]]:
        return (of_seq(xs), of_seq(ys), of_seq(zs))

    def _arrow137(
        tupled_arg: tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
        zs: Any = zs,
    ) -> Option[U]:
        e1: IEnumerator[T1] = tupled_arg[0]
        e2: IEnumerator[T2] = tupled_arg[1]
        e3: IEnumerator[T3] = tupled_arg[2]
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

    def _arrow138(
        tupled_arg_1: tuple[IEnumerator[T1], IEnumerator[T2], IEnumerator[T3]],
        mapping: Any = mapping,
        xs: Any = xs,
        ys: Any = ys,
        zs: Any = zs,
    ) -> None:
        try:
            dispose_2(tupled_arg_1[0])

        finally:
            try:
                dispose_2(tupled_arg_1[1])

            finally:
                dispose_2(tupled_arg_1[2])

    return generate(_arrow136, _arrow137, _arrow138)


def read_only[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow139(x: T = UNIT, xs: Any = xs) -> T:
        return x

    return map(_arrow139, Operators_NullArgCheck("source", xs))


def _expr140(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.CachedSeq`1", Array([gen0]), CachedSeq_1)


class CachedSeq_1[T](EnumerableBase[T], DisposableBase):
    def __init__(self, cleanup: Callable[[], None], res: IEnumerable_1[T]) -> None:
        self.cleanup: Callable[[], None] = cleanup
        self.res: IEnumerable_1[T] = res

    def Dispose(self, __unit: Unit = UNIT) -> None:
        _: CachedSeq_1[T] = self
        _.cleanup()

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        _: CachedSeq_1[T] = self
        return get_enumerator(_.res)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        _: CachedSeq_1[T] = self
        return get_enumerator(_.res)


CachedSeq_1_reflection = _expr140


def CachedSeq_1__ctor_Z7A8347D4[T](cleanup: Callable[[], None], res: IEnumerable_1[T]) -> CachedSeq_1[T]:
    return CachedSeq_1(cleanup, res)


def CachedSeq_1__Clear[T](_: CachedSeq_1[Any]) -> None:
    _.cleanup()


def cache[T](source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    source_1: IEnumerable_1[T] = Operators_NullArgCheck("source", source)
    prefix: list[T] = []
    enumerator_r: Option[IEnumerator[T] | None] = cast_1(Option[IEnumerator[T] | None], None)

    def cleanup(source: Any = source) -> None:
        def action_1(__unit: Unit = UNIT) -> None:
            nonlocal enumerator_r
            clear(prefix)
            (pattern_matching_result, e) = nullable[int32, IEnumerator[T]]()
            if enumerator_r is not None:
                if value_1(enumerator_r) is not None:
                    pattern_matching_result = int32(0)
                    e = value_1(value_1(enumerator_r))

                else:
                    pattern_matching_result = int32(1)

            else:
                pattern_matching_result = int32(1)

            if pattern_matching_result == int32.ZERO:
                dispose_2(e)

            enumerator_r = None

        lock(prefix, action_1)

    def _arrow141(i_1: int32, source: Any = source) -> tuple[T, int32] | None:
        def action(__unit: Unit = UNIT) -> tuple[T, int32] | None:
            nonlocal enumerator_r
            if i_1 < int32(len(prefix)):
                return (prefix[i_1], i_1 + int32.ONE)

            else:
                if i_1 >= int32(len(prefix)):
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

                if i_1 < int32(len(prefix)):
                    return (prefix[i_1], i_1 + int32.ONE)

                else:
                    return None

        return erase(lock(prefix, action))

    return CachedSeq_1__ctor_Z7A8347D4(cleanup, unfold(_arrow141, int32.ZERO))


def all_pairs[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    ys_cache: IEnumerable_1[T2] = cache(ys)

    def _arrow142(xs: Any = xs, ys: Any = ys) -> IEnumerable_1[tuple[T1, T2]]:
        def mapping_1(x: T1 = UNIT) -> IEnumerable_1[tuple[T1, T2]]:
            def mapping(y: T2 = UNIT, x: Any = x) -> tuple[T1, T2]:
                return (x, y)

            return map(mapping, ys_cache)

        return concat(map(mapping_1, xs))

    return delay(_arrow142)


def map_fold[STATE, T, RESULT](
    mapping: Callable[[STATE, T], tuple[RESULT, STATE]], state: STATE, xs: IEnumerable_1[T]
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[RESULT], STATE] = map_fold_1(mapping, state, to_array(xs), None)
    return (read_only(pattern_input[0]), pattern_input[1])


def map_fold_back[T, STATE, RESULT](
    mapping: Callable[[T, STATE], tuple[RESULT, STATE]], xs: IEnumerable_1[T], state: STATE
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[RESULT], STATE] = map_fold_back_1(mapping, to_array(xs), state, None)
    return (read_only(pattern_input[0]), pattern_input[1])


def try_pick[T, _A](chooser: Callable[[T], Option[_A]], xs: IEnumerable_1[T]) -> Option[_A]:
    with Disposable(of_seq(xs)) as e:
        res: Option[_A] = cast_1(Option[_A], None)
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            res = chooser(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return res


def pick[T, _A](chooser: Callable[[T], Option[_A]], xs: IEnumerable_1[T]) -> _A:
    match_value: Option[_A] = try_pick(chooser, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def reduce[T](folder: Callable[[T, T], T], xs: IEnumerable_1[T]) -> T:
    with Disposable(of_seq(xs)) as e:

        def loop(acc_mut: T = UNIT, folder: Any = folder, xs: Any = xs) -> T:
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
    if int32(len(arr)) > int32.ZERO:
        return reduce_back_1(folder, arr)

    else:
        raise Exception(SR_inputSequenceEmpty)


def replicate[_A](n: int32, x: _A) -> IEnumerable_1[_A]:
    def _arrow143(_arg: int32, n: Any = n, x: Any = x) -> _A:
        return x

    return initialize(n, _arrow143)


def reverse[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow144(xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(reverse_1(to_array(xs)))

    return delay(_arrow144)


def scan[STATE, T](folder: Callable[[STATE, T], STATE], state: STATE, xs: IEnumerable_1[T]) -> IEnumerable_1[STATE]:
    def _arrow145(folder: Any = folder, state: Any = state, xs: Any = xs) -> IEnumerable_1[STATE]:
        acc: STATE = state

        def mapping(x: T = UNIT) -> STATE:
            nonlocal acc
            acc = folder(acc, x)
            return acc

        return concat(to_enumerable([singleton(state), map(mapping, xs)]))

    return delay(_arrow145)


def scan_back[T, STATE](
    folder: Callable[[T, STATE], STATE], xs: IEnumerable_1[T], state: STATE
) -> IEnumerable_1[STATE]:
    def _arrow146(folder: Any = folder, xs: Any = xs, state: Any = state) -> IEnumerable_1[STATE]:
        return of_array(scan_back_1(folder, to_array(xs), state, None))

    return delay(_arrow146)


def skip[T](count: int32, source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow147(count: Any = count, source: Any = source) -> IEnumerator[T]:
        e: IEnumerator[T] = of_seq(source)
        try:
            for _ in range(int32.ONE, count, 1):
                if not e.System_Collections_IEnumerator_MoveNext():
                    raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

            def compensation(__unit: Unit = UNIT) -> None:
                pass

            return Enumerator_enumerateThenFinally(compensation, e)

        except Exception as match_value:
            dispose_2(e)
            raise match_value

    return mk_seq(_arrow147)


def skip_while[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow148(predicate: Any = predicate, xs: Any = xs) -> IEnumerable_1[T]:
        skipped: bool = True

        def f(x: T = UNIT) -> bool:
            nonlocal skipped
            if skipped:
                skipped = predicate(x)

            return not skipped

        return filter(f, xs)

    return delay(_arrow148)


def tail[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return skip(int32.ONE, xs)


def take[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow149(count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow150(i: int32, e: IEnumerator[T], count: Any = count, xs: Any = xs) -> Option[T]:
        if i < count:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")

        else:
            return None

    def _arrow151(e_1: IEnumerator[T], count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow149, _arrow150, _arrow151)


def take_while[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow152(predicate: Any = predicate, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow153(e: IEnumerator[T], predicate: Any = predicate, xs: Any = xs) -> Option[T]:
        return (
            some(e.System_Collections_Generic_IEnumerator_1_get_Current())
            if (
                predicate(e.System_Collections_Generic_IEnumerator_1_get_Current())
                if e.System_Collections_IEnumerator_MoveNext()
                else False
            )
            else None
        )

    def _arrow154(e_1: IEnumerator[T], predicate: Any = predicate, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate(_arrow152, _arrow153, _arrow154)


def truncate[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow155(count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow156(i: int32, e: IEnumerator[T], count: Any = count, xs: Any = xs) -> Option[T]:
        return (
            some(e.System_Collections_Generic_IEnumerator_1_get_Current())
            if (e.System_Collections_IEnumerator_MoveNext() if (i < count) else False)
            else None
        )

    def _arrow157(e_1: IEnumerator[T], count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow155, _arrow156, _arrow157)


def zip[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    def _arrow158(x: T1, y: T2, xs: Any = xs, ys: Any = ys) -> tuple[T1, T2]:
        return (x, y)

    return map2(_arrow158, xs, ys)


def zip3[T1, T2, T3](
    xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], zs: IEnumerable_1[T3]
) -> IEnumerable_1[tuple[T1, T2, T3]]:
    def _arrow159(x: T1, y: T2, z: T3, xs: Any = xs, ys: Any = ys, zs: Any = zs) -> tuple[T1, T2, T3]:
        return (x, y, z)

    return map3(_arrow159, xs, ys, zs)


def collect[T, COLLECTION: IEnumerable, U](mapping: Callable[[T], Any], xs: IEnumerable_1[T]) -> IEnumerable_1[Any]:
    def _arrow160(mapping: Any = mapping, xs: Any = xs) -> IEnumerable_1[U]:
        return concat(map(mapping, xs))

    return delay(_arrow160)


def where[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return filter(predicate, xs)


def pairwise[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[T, T]]:
    def _arrow161(xs: Any = xs) -> IEnumerable_1[tuple[T, T]]:
        return of_array(pairwise_1(to_array(xs)))

    return delay(_arrow161)


def split_into[T](chunks: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow162(chunks: Any = chunks, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(split_into_1(chunks, to_array(xs)))

    return delay(_arrow162)


def windowed[T](window_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow163(window_size: Any = window_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(windowed_1(window_size, to_array(xs)))

    return delay(_arrow163)


def transpose[_A: IEnumerable, T](xss: IEnumerable_1[Any]) -> IEnumerable_1[IEnumerable_1[Any]]:
    def _arrow164(xss: Any = xss) -> IEnumerable_1[IEnumerable_1[T]]:
        def mapping(xs_1: _A = UNIT) -> Array[T]:
            return to_array(xs_1)

        return of_array(map_1(of_array, transpose_1(map_1(mapping, to_array(xss), None), None), None))

    return delay(_arrow164)


def sort_with[T](comparer: Callable[[T, T], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow165(comparer: Any = comparer, xs: Any = xs) -> IEnumerable_1[T]:
        arr: Array[T] = to_array(xs)
        sort_in_place_with(comparer, arr)
        return of_array(arr)

    return delay(_arrow165)


def sort[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow166(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y)

    return sort_with(_arrow166, xs)


def sort_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> IEnumerable_1[T]:
    def _arrow167(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y))

    return sort_with(_arrow167, xs)


def sort_descending[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow168(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y) * int32.NEG_ONE

    return sort_with(_arrow168, xs)


def sort_by_descending[T, U](
    projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]
) -> IEnumerable_1[T]:
    def _arrow169(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y)) * int32.NEG_ONE

    return sort_with(_arrow169, xs)


def sum[T](xs: IEnumerable_1[T], adder: IGenericAdder_1[T]) -> T:
    def _arrow170(acc: T, x: T, xs: Any = xs, adder: Any = adder) -> T:
        return adder.Add(acc, x)

    return fold(_arrow170, adder.GetZero(), xs)


def sum_by[T, U](f: Callable[[T], U], xs: IEnumerable_1[T], adder: IGenericAdder_1[U]) -> U:
    def _arrow171(acc: U, x: T, f: Any = f, xs: Any = xs, adder: Any = adder) -> U:
        return adder.Add(acc, f(x))

    return fold(_arrow171, adder.GetZero(), xs)


def max_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow172(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else x

    return reduce(_arrow172, xs)


def max[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow173(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(y, x) > int32.ZERO) else x

    return reduce(_arrow173, xs)


def min_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow174(x: T, y: T, projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else y

    return reduce(_arrow174, xs)


def min[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow175(x: T, y: T, xs: Any = xs, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(y, x) > int32.ZERO) else y

    return reduce(_arrow175, xs)


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

    def _arrow176(acc: U, x: T, f: Any = f, xs: Any = xs, averager: Any = averager) -> U:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, f(x))

    total: U = fold(_arrow176, averager.GetZero(), xs)
    if count == int32.ZERO:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")

    else:
        return averager.DivideByInt(total, count)


def permute[T](f: Callable[[int32], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow177(f: Any = f, xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(permute_1(f, to_array(xs)))

    return delay(_arrow177)


def chunk_by_size[T](chunk_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow178(chunk_size: Any = chunk_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(chunk_by_size_1(chunk_size, to_array(xs)))

    return delay(_arrow178)


def insert_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow179(index: Any = index, y: Any = y, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow180(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> Option[T]:
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

    def _arrow181(e_1: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow179, _arrow180, _arrow181)


def insert_many_at[T](index: int32, ys: IEnumerable_1[T], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    status: int32 = int32.NEG_ONE
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow182(index: Any = index, ys: Any = ys, xs: Any = xs) -> tuple[IEnumerator[T], IEnumerator[T]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow183(
        i: int32, tupled_arg: tuple[IEnumerator[T], IEnumerator[T]], index: Any = index, ys: Any = ys, xs: Any = xs
    ) -> Option[T]:
        nonlocal status
        e1: IEnumerator[T] = tupled_arg[0]
        e2: IEnumerator[T] = tupled_arg[1]
        if i == index:
            status = int32.ZERO

        inserted: Option[T]
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

    def _arrow184(
        tupled_arg_1: tuple[IEnumerator[T], IEnumerator[T]], index: Any = index, ys: Any = ys, xs: Any = xs
    ) -> None:
        dispose_2(tupled_arg_1[0])
        dispose_2(tupled_arg_1[1])

    return generate_indexed(_arrow182, _arrow183, _arrow184)


def remove_at[T](index: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow185(index: Any = index, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow186(i: int32, e: IEnumerator[T], index: Any = index, xs: Any = xs) -> Option[T]:
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

    def _arrow187(e_1: IEnumerator[T], index: Any = index, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow185, _arrow186, _arrow187)


def remove_many_at[T](index: int32, count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow188(index: Any = index, count: Any = count, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow189(i: int32, e: IEnumerator[T], index: Any = index, count: Any = count, xs: Any = xs) -> Option[T]:
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

    def _arrow190(e_1: IEnumerator[T], index: Any = index, count: Any = count, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow188, _arrow189, _arrow190)


def update_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")

    def _arrow191(index: Any = index, y: Any = y, xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow192(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> Option[T]:
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

    def _arrow193(e_1: IEnumerator[T], index: Any = index, y: Any = y, xs: Any = xs) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow191, _arrow192, _arrow193)


__all__ = [
    "CachedSeq_1__Clear",
    "CachedSeq_1_reflection",
    "Enumerator_FromFunctions_1_reflection",
    "Enumerator_Seq_reflection",
    "Enumerator_alreadyFinished",
    "Enumerator_cast",
    "Enumerator_concat",
    "Enumerator_enumerateThenFinally",
    "Enumerator_generateWhileSome",
    "Enumerator_noReset",
    "Enumerator_notStarted",
    "Enumerator_unfold",
    "SR_enumerationAlreadyFinished",
    "SR_enumerationNotStarted",
    "SR_inputSequenceEmpty",
    "SR_inputSequenceTooLong",
    "SR_keyNotFoundAlt",
    "SR_notEnoughElements",
    "SR_resetNotSupported",
    "all_pairs",
    "append",
    "average",
    "average_by",
    "cache",
    "cast",
    "choose",
    "chunk_by_size",
    "collect",
    "compare_with",
    "concat",
    "contains",
    "delay",
    "empty",
    "enumerate_from_functions",
    "enumerate_then_finally",
    "enumerate_using",
    "enumerate_while",
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
    "for_all",
    "for_all2",
    "generate",
    "generate_indexed",
    "head",
    "index_not_found",
    "indexed",
    "initialize",
    "initialize_infinite",
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
    "mk_seq",
    "of_array",
    "of_list",
    "of_seq",
    "pairwise",
    "permute",
    "pick",
    "read_only",
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
    "split_into",
    "sum",
    "sum_by",
    "tail",
    "take",
    "take_while",
    "to_array",
    "to_list",
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
    "update_at",
    "where",
    "windowed",
    "zip",
    "zip3",
]
