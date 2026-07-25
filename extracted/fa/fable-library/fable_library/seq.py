from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import cast as cast_1

from fable_library.seq_native import filter, map, map2, map3, map_indexed, unfold

from .array_ import Array, random_shuffle_in_place_by, sort_in_place_with
from .array_ import chunk_by_size as chunk_by_size_1
from .array_ import empty as empty_1
from .array_ import fold_back as fold_back_1
from .array_ import map as map_1
from .array_ import map_fold as map_fold_1
from .array_ import map_fold_back as map_fold_back_1
from .array_ import of_seq as of_seq_1
from .array_ import pairwise as pairwise_1
from .array_ import permute as permute_1
from .array_ import random_choice as random_choice_1
from .array_ import random_choice_by as random_choice_by_1
from .array_ import random_choice_with as random_choice_with_1
from .array_ import random_choices_by as random_choices_by_1
from .array_ import random_sample_by as random_sample_by_1
from .array_ import reduce_back as reduce_back_1
from .array_ import reverse as reverse_1
from .array_ import scan_back as scan_back_1
from .array_ import singleton as singleton_1
from .array_ import split_into as split_into_1
from .array_ import transpose as transpose_1
from .array_ import try_find_back as try_find_back_1
from .array_ import try_find_index_back as try_find_index_back_1
from .array_ import windowed as windowed_1
from .bases import DisposableBase, EnumerableBase, EnumeratorBase, StringableBase
from .core import float64, int32
from .exceptions import to_string
from .fsharp_core import Operators_NullArgCheck
from .global_ import IGenericAdder_1, IGenericAverager_1, SR_indexOutOfBounds
from .list import FSharpList
from .list import is_empty as is_empty_1
from .list import length as length_1
from .list import of_array as of_array_1
from .list import of_seq as of_seq_2
from .list import to_array as to_array_1
from .option import Option, erase, some
from .option import value as value_1
from .protocols import IComparer_1, IDisposable, IEnumerable, IEnumerable_1, IEnumerator, IEqualityComparer_1
from .record import Record
from .reflection import TypeInfo, bool_type, class_type, option_type, record_type
from .system import InvalidOperationException__ctor_Z721C83C5, NotSupportedException__ctor_Z721C83C5
from .types import ExceptionBase
from .util import (
    UNIT,
    Disposable,
    Unit,
    clear,
    compare_primitives,
    create_random,
    equals,
    get_enumerator,
    ignore,
    is_disposable,
    lock,
    nullable,
    random_double,
    range,
    to_enumerable,
)
from .util import dispose as dispose_2
from .util import min as min_1


SR_enumerationAlreadyFinished: str = "Enumeration already finished."

SR_enumerationNotStarted: str = "Enumeration has not started. Call MoveNext."

SR_inputSequenceEmpty: str = "The input sequence was empty."

SR_inputSequenceTooLong: str = "The input sequence contains more than one element."

SR_keyNotFoundAlt: str = "An index satisfying the predicate was not found in the collection."

SR_notEnoughElements: str = "The input sequence has an insufficient number of elements."

SR_resetNotSupported: str = "Reset is not supported on this enumerator."


def Enumerator_noReset[_A](__unit: Unit = UNIT) -> _A:
    raise NotSupportedException__ctor_Z721C83C5(SR_resetNotSupported)


def Enumerator_notStarted[_A](__unit: Unit = UNIT) -> _A:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationNotStarted)


def Enumerator_alreadyFinished[_A](__unit: Unit = UNIT) -> _A:
    raise InvalidOperationException__ctor_Z721C83C5(SR_enumerationAlreadyFinished)


def _expr100(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.Seq", Array([gen0]), Enumerator_Seq)


class Enumerator_Seq[T](StringableBase, EnumerableBase[Any]):
    def __init__(self, f: Callable[[], IEnumerator[T]]) -> None:
        self.f: Callable[[], IEnumerator[Any]] = f

    def ToString(self, __unit: Unit = UNIT) -> str:
        xs: Enumerator_Seq[Any] = self
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
        x: Enumerator_Seq[Any] = self
        return x.f()

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        x: Enumerator_Seq[Any] = self
        return x.f()


Enumerator_Seq_reflection = _expr100


def Enumerator_Seq__ctor_673A07F2[T](f: Callable[[], IEnumerator[T]]) -> Enumerator_Seq[T]:
    return Enumerator_Seq(f)


def _expr101(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.Enumerator.FromFunctions`1", Array([gen0]), Enumerator_FromFunctions_1)


class Enumerator_FromFunctions_1[T](EnumeratorBase[Any], DisposableBase):
    def __init__(self, current: Callable[[], T], next_1: Callable[[], bool], dispose: Callable[[], None]) -> None:
        self.current: Callable[[], Any] = current
        self.next: Callable[[], bool] = next_1
        self.dispose: Callable[[], None] = dispose

    def System_Collections_Generic_IEnumerator_1_get_Current(self, __unit: Unit = UNIT) -> T:
        _: Enumerator_FromFunctions_1[Any] = self
        return _.current()

    def System_Collections_IEnumerator_get_Current(self, __unit: Unit = UNIT) -> Any:
        _: Enumerator_FromFunctions_1[Any] = self
        return _.current()

    def System_Collections_IEnumerator_MoveNext(self, __unit: Unit = UNIT) -> bool:
        _: Enumerator_FromFunctions_1[Any] = self
        return _.next()

    def System_Collections_IEnumerator_Reset(self, __unit: Unit = UNIT) -> None:
        Enumerator_noReset()

    def Dispose(self, __unit: Unit = UNIT) -> None:
        _: Enumerator_FromFunctions_1[Any] = self
        _.dispose()


Enumerator_FromFunctions_1_reflection = _expr101


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


def Enumerator_concat[T, U: IEnumerable](sources: IEnumerable_1[U]) -> IEnumerator[T]:
    outer_opt: IEnumerator[Any] | None = cast_1(IEnumerator[Any] | None, None)
    inner_opt: IEnumerator[Any] | None = cast_1(IEnumerator[Any] | None, None)
    started: bool = False
    finished: bool = False
    curr: Option[Any] = cast_1(Option[Any], None)

    def finish(__unit: Unit = UNIT) -> None:
        nonlocal finished, inner_opt, outer_opt
        finished = True
        if inner_opt is not None:
            inner: IEnumerator[Any] = inner_opt
            try:
                dispose_2(inner)

            finally:
                inner_opt = None

        if outer_opt is not None:
            outer: IEnumerator[Any] = outer_opt
            try:
                dispose_2(outer)

            finally:
                outer_opt = None

    def current(__unit: Unit = UNIT) -> T:
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
                outer_opt_1: IEnumerator[Any] | None = outer_opt
                inner_opt_1: IEnumerator[Any] | None = inner_opt
                if outer_opt_1 is not None:
                    if inner_opt_1 is not None:
                        inner_1: IEnumerator[Any] = inner_opt_1
                        if inner_1.System_Collections_IEnumerator_MoveNext():
                            curr = some(inner_1.System_Collections_Generic_IEnumerator_1_get_Current())
                            res = True

                        else:
                            try:
                                dispose_2(inner_1)

                            finally:
                                inner_opt = None

                    else:
                        outer_1: IEnumerator[Any] = outer_opt_1
                        if outer_1.System_Collections_IEnumerator_MoveNext():
                            ie: Any = outer_1.System_Collections_Generic_IEnumerator_1_get_Current()

                            def _arrow102(__unit: Unit = UNIT) -> IEnumerator[T]:
                                copy_of_struct: Any = ie
                                return get_enumerator(copy_of_struct)

                            inner_opt = _arrow102()

                        else:
                            finish()
                            res = False

                else:
                    outer_opt = get_enumerator(sources)

            return value_1(res)

    def dispose(__unit: Unit = UNIT) -> None:
        if not finished:
            finish()

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_enumerateThenFinally[T](f: Callable[[], None], e: IEnumerator[T]) -> IEnumerator[T]:
    def current(e: Any = e) -> T:
        return e.System_Collections_Generic_IEnumerator_1_get_Current()

    def next_1(e: Any = e) -> bool:
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
    curr: Option[Any] = cast_1(Option[Any], None)
    state: Option[Any] = some(openf())

    def dispose(closef: Any = closef) -> None:
        nonlocal state
        if state is not None:
            x_1: Any = value_1(state)
            try:
                closef(x_1)

            finally:
                state = None

    def finish(__unit: Unit = UNIT) -> None:
        nonlocal curr
        try:
            dispose()

        finally:
            curr = None

    def current(__unit: Unit = UNIT) -> U:
        if not started:
            Enumerator_notStarted()

        if curr is not None:
            return value_1(curr)

        else:
            return Enumerator_alreadyFinished()

    def next_1(compute: Any = compute) -> bool:
        nonlocal started, curr
        if not started:
            started = True

        if state is not None:
            s: Any = value_1(state)
            match_value_1: Option[Any]
            try:
                match_value_1 = compute(s)

            except Exception as match_value:
                match_value_: Exception = match_value
                finish()
                raise match_value_

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
    curr: tuple[Any, Any] | None = cast_1(tuple[Any, Any] | None, None)
    acc: Any = state

    def current(__unit: Unit = UNIT) -> T:
        if curr is not None:
            x: Any = curr[0]
            curr[1]
            return x

        else:
            return Enumerator_notStarted()

    def next_1(f: Any = f) -> bool:
        nonlocal curr, acc
        curr = f(acc)
        if curr is not None:
            curr[0]
            st_1: Any = curr[1]
            acc = st_1
            return True

        else:
            return False

    def dispose(__unit: Unit = UNIT) -> None:
        pass

    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def index_not_found[_A](__unit: Unit = UNIT) -> _A:
    raise ExceptionBase(SR_keyNotFoundAlt)


def mk_seq[T](f: Callable[[], IEnumerator[T]]) -> IEnumerable_1[T]:
    return Enumerator_Seq__ctor_673A07F2(f)


def of_seq[T](xs: IEnumerable_1[T]) -> IEnumerator[T]:
    return get_enumerator(Operators_NullArgCheck("source", xs))


def delay[T](generator: Callable[[], IEnumerable_1[T]]) -> IEnumerable_1[T]:
    def _arrow103(generator: Any = generator) -> IEnumerator[T]:
        return get_enumerator(generator())

    return mk_seq(_arrow103)


def concat[COLLECTION: IEnumerable, T](sources: IEnumerable_1[COLLECTION]) -> IEnumerable_1[T]:
    def _arrow104(sources: Any = sources) -> IEnumerator[T]:
        return Enumerator_concat(sources)

    return mk_seq(_arrow104)


def empty[T](__unit: Unit = UNIT) -> IEnumerable_1[T]:
    def _arrow105(__unit: Unit = UNIT) -> IEnumerable_1[T]:
        return empty_1()

    return delay(_arrow105)


def singleton[T](x: T = UNIT) -> IEnumerable_1[T]:
    def _arrow106(x: Any = x) -> IEnumerable_1[T]:
        return singleton_1(x, None)

    return delay(_arrow106)


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
    def _arrow107(create: Any = create, compute: Any = compute, dispose: Any = dispose) -> IEnumerator[_B]:
        return Enumerator_generateWhileSome(create, compute, dispose)

    return mk_seq(_arrow107)


def generate_indexed[_A, _B](
    create: Callable[[], _A], compute: Callable[[int32, _A], Option[_B]], dispose: Callable[[_A], None]
) -> IEnumerable_1[_B]:
    def _arrow109(create: Any = create, compute: Any = compute, dispose: Any = dispose) -> IEnumerator[_B]:
        i: int32 = int32.NEG_ONE

        def _arrow108(x: _A = UNIT) -> Option[_B]:
            nonlocal i
            i = i + int32.ONE
            return compute(i, x)

        return Enumerator_generateWhileSome(create, _arrow108, dispose)

    return mk_seq(_arrow109)


def cast[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow110(xs: Any = xs) -> IEnumerator[T]:
        return Enumerator_cast(get_enumerator(Operators_NullArgCheck("source", xs)))

    return mk_seq(_arrow110)


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
    def _arrow111(x: _A = UNIT, move_next: Any = move_next, current: Any = current) -> Option[_B]:
        return some(current(x)) if move_next(x) else None

    def _arrow112(x_1: _A = UNIT) -> None:
        match_value: Any = x_1
        if is_disposable(match_value):
            dispose_2(match_value)

    return generate(create, _arrow111, _arrow112)


def enumerate_then_finally[T](source: IEnumerable_1[T], compensation: Callable[[], None]) -> IEnumerable_1[T]:
    compensation_1: Callable[[], None] = compensation

    def _arrow113(source: Any = source) -> IEnumerator[T]:
        try:
            return Enumerator_enumerateThenFinally(compensation_1, of_seq(source))

        except Exception as match_value:
            match_value_: Exception = match_value
            compensation_1()
            raise match_value_

    return mk_seq(_arrow113)


def enumerate_using[T: IDisposable, _A: IEnumerable, U](resource: T, source: Callable[[T], _A]) -> IEnumerable_1[U]:
    def compensation(resource: Any = resource) -> None:
        if equals(resource, cast_1(Any, None)):
            pass

        else:
            copy_of_struct: Any = resource
            dispose_2(copy_of_struct)

    def _arrow114(resource: Any = resource, source: Any = source) -> IEnumerator[U]:
        try:
            return Enumerator_enumerateThenFinally(compensation, of_seq(source(resource)))

        except Exception as match_value_1:
            match_value_1_: Exception = match_value_1
            compensation()
            raise match_value_1_

    return mk_seq(_arrow114)


def enumerate_while[T](guard: Callable[[], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow115(i: int32, guard: Any = guard, xs: Any = xs) -> tuple[IEnumerable_1[T], int32] | None:
        return ((xs, i + int32.ONE)) if guard() else None

    return concat(unfold(_arrow115, int32.ZERO))


def _expr116(gen0: TypeInfo) -> TypeInfo:
    return record_type(
        "SeqModule.EnumerateTryWithState`1",
        Array([gen0]),
        EnumerateTryWithState_1,
        lambda: [
            ("source", option_type(class_type("System.Collections.Generic.IEnumerator`1", Array([gen0])))),
            ("caught", bool_type),
        ],
    )


@dataclass(eq=False, repr=False, slots=True)
class EnumerateTryWithState_1[T](Record):
    source: IEnumerator[Any] | None
    caught: bool

    def __hash__(self) -> int:
        return int(self.GetHashCode())


EnumerateTryWithState_1_reflection = _expr116


def enumerate_try_with[T](
    source: IEnumerable_1[T],
    catch_filter: Callable[[Exception], int32],
    catch_handler: Callable[[Exception], IEnumerable_1[T]],
) -> IEnumerable_1[T]:
    def _arrow117(__unit: Unit = UNIT) -> EnumerateTryWithState_1[T]:
        return EnumerateTryWithState_1(None, False)

    def _arrow118(
        state: EnumerateTryWithState_1[T],
        source: Any = source,
        catch_filter: Any = catch_filter,
        catch_handler: Any = catch_handler,
    ) -> Option[T]:
        result: Option[Any] = cast_1(Option[Any], None)
        go: bool = True
        while go:
            try:
                en_2: IEnumerator[Any]
                match_value: IEnumerator[Any] | None = state.source
                if match_value is None:
                    en_1: IEnumerator[Any] = get_enumerator(source)
                    state.source = en_1
                    en_2 = en_1

                else:
                    en_2 = match_value

                if en_2.System_Collections_IEnumerator_MoveNext():
                    result = some(en_2.System_Collections_Generic_IEnumerator_1_get_Current())
                    go = False

                else:
                    go = False

            except Exception as ex:
                ex_: Exception = ex
                if (catch_filter(ex_) != int32.ZERO) if (not state.caught) else False:
                    match_value_1: IEnumerator[Any] | None = state.source
                    if match_value_1 is None:
                        pass

                    else:
                        en_3: IEnumerator[Any] = match_value_1
                        try:
                            dispose_2(en_3)

                        except Exception as match_value_2:
                            pass

                        state.source = cast_1(IEnumerator[Any] | None, None)

                    state.source = get_enumerator(catch_handler(ex_))
                    state.caught = True

                else:
                    raise ex_

        return result

    def _arrow119(state_1: EnumerateTryWithState_1[T]) -> None:
        match_value_3: IEnumerator[Any] | None = state_1.source
        if match_value_3 is None:
            pass

        else:
            en_4: IEnumerator[Any] = match_value_3
            dispose_2(en_4)

    return generate(_arrow117, _arrow118, _arrow119)


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
            v: Any = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                raise Exception(SR_inputSequenceTooLong + " (Parameter 'source')")

            else:
                return v

        else:
            raise Exception(SR_inputSequenceEmpty + " (Parameter 'source')")


def try_exactly_one[T](xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v: Any = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                return None

            else:
                return some(v)

        else:
            return None


def try_find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:
        res: Option[Any] = cast_1(Option[Any], None)
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            c: Any = e.System_Collections_Generic_IEnumerator_1_get_Current()
            if predicate(c):
                res = some(c)

        return res


def find[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: Option[Any] = try_find(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> Option[T]:
    return try_find_back_1(predicate, to_array(xs))


def find_back[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> T:
    match_value: Option[Any] = try_find_back(predicate, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def try_find_index[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> int32 | None:
    with Disposable(of_seq(xs)) as e:

        def loop(i_mut: int32, predicate: Any = predicate) -> int32 | None:
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
        acc: Any = state
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
            acc: Any = state
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
    xs_1: Array[Any] = to_array(xs)
    ys_1: Array[Any] = to_array(ys)
    len_1: int32 = min_1(compare_primitives, int32(len(xs_1)), int32(len(ys_1)))
    acc: Any = state
    for i in range(len_1 - int32.ONE, int32.ZERO, -1):
        acc = folder(xs_1[i], ys_1[i], acc)
    return acc


def for_all[_A](predicate: Callable[[_A], bool], xs: IEnumerable_1[_A]) -> bool:
    def _arrow120(x: _A = UNIT, predicate: Any = predicate) -> bool:
        return not predicate(x)

    return not exists(_arrow120, xs)


def for_all2[_A, _B](predicate: Callable[[_A, _B], bool], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> bool:
    def _arrow121(x: _A, y: _B, predicate: Any = predicate) -> bool:
        return not predicate(x, y)

    return not exists2(_arrow121, xs, ys)


def initialize[_A](count: int32, f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    def _arrow122(i: int32, count: Any = count, f: Any = f) -> tuple[_A, int32] | None:
        return ((f(i), i + int32.ONE)) if (i < count) else None

    return unfold(_arrow122, int32.ZERO)


def initialize_infinite[_A](f: Callable[[int32], _A]) -> IEnumerable_1[_A]:
    return initialize(int32(2147483647), f)


def is_empty[T](xs: IEnumerable_1[T]) -> bool:
    if isinstance(xs, Array):
        return len(xs) == int32.ZERO

    elif isinstance(xs, FSharpList):
        return is_empty_1(xs)

    else:
        with Disposable(of_seq(xs)) as e:
            return not e.System_Collections_IEnumerator_MoveNext()


def iterate[_A](action: Callable[[_A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow123(unit_var: None, x: _A, action: Any = action) -> None:
        action(x)

    fold(_arrow123, None, xs)


def iterate2[_A, _B](action: Callable[[_A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]) -> None:
    def _arrow124(unit_var: None, x: _A, y: _B, action: Any = action) -> None:
        action(x, y)

    fold2(_arrow124, None, xs, ys)


def iterate_indexed[_A](action: Callable[[int32, _A], None], xs: IEnumerable_1[_A]) -> None:
    def _arrow125(i: int32, x: _A, action: Any = action) -> int32:
        action(i, x)
        return i + int32.ONE

    ignore(fold(_arrow125, int32.ZERO, xs))


def iterate_indexed2[_A, _B](
    action: Callable[[int32, _A, _B], None], xs: IEnumerable_1[_A], ys: IEnumerable_1[_B]
) -> None:
    def _arrow126(i: int32, x: _A, y: _B, action: Any = action) -> int32:
        action(i, x, y)
        return i + int32.ONE

    ignore(fold2(_arrow126, int32.ZERO, xs, ys))


def try_last[T](xs: IEnumerable_1[T]) -> Option[T]:
    with Disposable(of_seq(xs)) as e:

        def loop(acc_mut: T = UNIT) -> T:
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
    match_value: Option[Any] = try_last(xs)
    if match_value is None:
        raise Exception(SR_notEnoughElements + " (Parameter 'source')")

    else:
        return value_1(match_value)


def length[T](xs: IEnumerable_1[T]) -> int32:
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


def indexed[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[int32, T]]:
    def mapping(i: int32, x: T) -> tuple[int32, T]:
        return (i, x)

    return map_indexed(mapping, xs)


def read_only[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow127(x: T = UNIT) -> T:
        return x

    return map(_arrow127, Operators_NullArgCheck("source", xs))


def _expr128(gen0: TypeInfo) -> TypeInfo:
    return class_type("SeqModule.CachedSeq`1", Array([gen0]), CachedSeq_1)


class CachedSeq_1[T](EnumerableBase[Any], DisposableBase):
    def __init__(self, cleanup: Callable[[], None], res: IEnumerable_1[T]) -> None:
        self.cleanup: Callable[[], None] = cleanup
        self.res: IEnumerable_1[Any] = res

    def Dispose(self, __unit: Unit = UNIT) -> None:
        _: CachedSeq_1[Any] = self
        _.cleanup()

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        _: CachedSeq_1[Any] = self
        return get_enumerator(_.res)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        _: CachedSeq_1[Any] = self
        return get_enumerator(_.res)


CachedSeq_1_reflection = _expr128


def CachedSeq_1__ctor_Z7A8347D4[T](cleanup: Callable[[], None], res: IEnumerable_1[T]) -> CachedSeq_1[T]:
    return CachedSeq_1(cleanup, res)


def CachedSeq_1__Clear[T](_: CachedSeq_1[T]) -> None:
    _.cleanup()


def cache[T](source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    source_1: IEnumerable_1[Any] = Operators_NullArgCheck("source", source)
    prefix: list[Any] = []
    enumerator_r: Option[IEnumerator[Any] | None] = cast_1(Option[IEnumerator[Any] | None], None)

    def cleanup(__unit: Unit = UNIT) -> None:
        def action_1(__unit: Unit = UNIT) -> None:
            nonlocal enumerator_r
            clear(prefix)
            (pattern_matching_result, e) = nullable[int32, IEnumerator[Any]]()
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

    def _arrow129(i_1: int32) -> tuple[T, int32] | None:
        def action(__unit: Unit = UNIT) -> tuple[T, int32] | None:
            nonlocal enumerator_r
            if i_1 < int32(len(prefix)):
                return (prefix[i_1], i_1 + int32.ONE)

            else:
                if i_1 >= int32(len(prefix)):
                    opt_enumerator_2: IEnumerator[Any] | None
                    if enumerator_r is not None:
                        opt_enumerator_2 = value_1(enumerator_r)

                    else:
                        opt_enumerator: IEnumerator[Any] | None = get_enumerator(source_1)
                        enumerator_r = some(opt_enumerator)
                        opt_enumerator_2 = opt_enumerator

                    if opt_enumerator_2 is None:
                        pass

                    else:
                        enumerator: IEnumerator[Any] = opt_enumerator_2
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

    return CachedSeq_1__ctor_Z7A8347D4(cleanup, unfold(_arrow129, int32.ZERO))


def all_pairs[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    ys_cache: IEnumerable_1[Any] = cache(ys)

    def _arrow130(xs: Any = xs) -> IEnumerable_1[tuple[T1, T2]]:
        def mapping_1(x: T1 = UNIT) -> IEnumerable_1[tuple[T1, T2]]:
            def mapping(y: T2 = UNIT, x: Any = x) -> tuple[T1, T2]:
                return (x, y)

            return map(mapping, ys_cache)

        return concat(map(mapping_1, xs))

    return delay(_arrow130)


def map_fold[STATE, T, RESULT](
    mapping: Callable[[STATE, T], tuple[RESULT, STATE]], state: STATE, xs: IEnumerable_1[T]
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[Any], Any] = map_fold_1(mapping, state, to_array(xs), None)
    return (read_only(pattern_input[0]), pattern_input[1])


def map_fold_back[T, STATE, RESULT](
    mapping: Callable[[T, STATE], tuple[RESULT, STATE]], xs: IEnumerable_1[T], state: STATE
) -> tuple[IEnumerable_1[RESULT], STATE]:
    pattern_input: tuple[Array[Any], Any] = map_fold_back_1(mapping, to_array(xs), state, None)
    return (read_only(pattern_input[0]), pattern_input[1])


def try_pick[T, _A](chooser: Callable[[T], Option[_A]], xs: IEnumerable_1[T]) -> Option[_A]:
    with Disposable(of_seq(xs)) as e:
        res: Option[Any] = cast_1(Option[Any], None)
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else False:
            res = chooser(e.System_Collections_Generic_IEnumerator_1_get_Current())
        return res


def pick[T, _A](chooser: Callable[[T], Option[_A]], xs: IEnumerable_1[T]) -> _A:
    match_value: Option[Any] = try_pick(chooser, xs)
    if match_value is None:
        return index_not_found()

    else:
        return value_1(match_value)


def reduce[T](folder: Callable[[T, T], T], xs: IEnumerable_1[T]) -> T:
    with Disposable(of_seq(xs)) as e:

        def loop(acc_mut: T = UNIT, folder: Any = folder) -> T:
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
    arr: Array[Any] = to_array(xs)
    if int32(len(arr)) > int32.ZERO:
        return reduce_back_1(folder, arr)

    else:
        raise Exception(SR_inputSequenceEmpty)


def replicate[_A](n: int32, x: _A) -> IEnumerable_1[_A]:
    def _arrow131(_arg: int32, x: Any = x) -> _A:
        return x

    return initialize(n, _arrow131)


def reverse[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow132(xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(reverse_1(to_array(xs)))

    return delay(_arrow132)


def scan[STATE, T](folder: Callable[[STATE, T], STATE], state: STATE, xs: IEnumerable_1[T]) -> IEnumerable_1[STATE]:
    def _arrow133(folder: Any = folder, state: Any = state, xs: Any = xs) -> IEnumerable_1[STATE]:
        acc: Any = state

        def mapping(x: T = UNIT) -> STATE:
            nonlocal acc
            acc = folder(acc, x)
            return acc

        return concat(to_enumerable([singleton(state), map(mapping, xs)]))

    return delay(_arrow133)


def scan_back[T, STATE](
    folder: Callable[[T, STATE], STATE], xs: IEnumerable_1[T], state: STATE
) -> IEnumerable_1[STATE]:
    def _arrow134(folder: Any = folder, xs: Any = xs, state: Any = state) -> IEnumerable_1[STATE]:
        return of_array(scan_back_1(folder, to_array(xs), state, None))

    return delay(_arrow134)


def skip[T](count: int32, source: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow135(count: Any = count, source: Any = source) -> IEnumerator[T]:
        e: IEnumerator[Any] = of_seq(source)
        try:
            for _ in range(int32.ONE, count, 1):
                if not e.System_Collections_IEnumerator_MoveNext():
                    raise Exception(SR_notEnoughElements + " (Parameter 'source')")

            def compensation(__unit: Unit = UNIT) -> None:
                pass

            return Enumerator_enumerateThenFinally(compensation, e)

        except Exception as match_value:
            match_value_: Exception = match_value
            dispose_2(e)
            raise match_value_

    return mk_seq(_arrow135)


def skip_while[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow136(predicate: Any = predicate, xs: Any = xs) -> IEnumerable_1[T]:
        skipped: bool = True

        def predicate_1(x: T = UNIT) -> bool:
            nonlocal skipped
            if skipped:
                skipped = predicate(x)

            return not skipped

        return filter(predicate_1, xs)

    return delay(_arrow136)


def tail[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return skip(int32.ONE, xs)


def zip[T1, T2](xs: IEnumerable_1[T1], ys: IEnumerable_1[T2]) -> IEnumerable_1[tuple[T1, T2]]:
    def _arrow137(x: T1, y: T2) -> tuple[T1, T2]:
        return (x, y)

    return map2(_arrow137, xs, ys)


def zip3[T1, T2, T3](
    xs: IEnumerable_1[T1], ys: IEnumerable_1[T2], zs: IEnumerable_1[T3]
) -> IEnumerable_1[tuple[T1, T2, T3]]:
    def _arrow138(x: T1, y: T2, z: T3) -> tuple[T1, T2, T3]:
        return (x, y, z)

    return map3(_arrow138, xs, ys, zs)


def where[T](predicate: Callable[[T], bool], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return filter(predicate, xs)


def pairwise[T](xs: IEnumerable_1[T]) -> IEnumerable_1[tuple[T, T]]:
    def _arrow139(xs: Any = xs) -> IEnumerable_1[tuple[T, T]]:
        return of_array(pairwise_1(to_array(xs)))

    return delay(_arrow139)


def split_into[T](chunks: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow140(chunks: Any = chunks, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(split_into_1(chunks, to_array(xs)))

    return delay(_arrow140)


def windowed[T](window_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow141(window_size: Any = window_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(windowed_1(window_size, to_array(xs)))

    return delay(_arrow141)


def transpose[_A: IEnumerable, T](xss: IEnumerable_1[_A]) -> IEnumerable_1[IEnumerable_1[T]]:
    def _arrow142(xss: Any = xss) -> IEnumerable_1[IEnumerable_1[T]]:
        def mapping(xs_1: _A = UNIT) -> Array[T]:
            return to_array(xs_1)

        return of_array(map_1(of_array, transpose_1(map_1(mapping, to_array(xss), None), None), None))

    return delay(_arrow142)


def sort_with[T](comparer: Callable[[T, T], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow143(comparer: Any = comparer, xs: Any = xs) -> IEnumerable_1[T]:
        arr: Array[Any] = to_array(xs)
        sort_in_place_with(comparer, arr)
        return of_array(arr)

    return delay(_arrow143)


def sort[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow144(x: T, y: T, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y)

    return sort_with(_arrow144, xs)


def sort_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> IEnumerable_1[T]:
    def _arrow145(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y))

    return sort_with(_arrow145, xs)


def sort_descending[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> IEnumerable_1[T]:
    def _arrow146(x: T, y: T, comparer: Any = comparer) -> int32:
        return comparer.Compare(x, y) * int32.NEG_ONE

    return sort_with(_arrow146, xs)


def sort_by_descending[T, U](
    projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]
) -> IEnumerable_1[T]:
    def _arrow147(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> int32:
        return comparer.Compare(projection(x), projection(y)) * int32.NEG_ONE

    return sort_with(_arrow147, xs)


def sum[T](xs: IEnumerable_1[T], adder: IGenericAdder_1[T]) -> T:
    def _arrow148(acc: T, x: T, adder: Any = adder) -> T:
        return adder.Add(acc, x)

    return fold(_arrow148, adder.GetZero(), xs)


def sum_by[T, U](f: Callable[[T], U], xs: IEnumerable_1[T], adder: IGenericAdder_1[U]) -> U:
    def _arrow149(acc: U, x: T, f: Any = f, adder: Any = adder) -> U:
        return adder.Add(acc, f(x))

    return fold(_arrow149, adder.GetZero(), xs)


def max_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow150(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else x

    return reduce(_arrow150, xs)


def max[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow151(x: T, y: T, comparer: Any = comparer) -> T:
        return y if (comparer.Compare(y, x) > int32.ZERO) else x

    return reduce(_arrow151, xs)


def min_by[T, U](projection: Callable[[T], U], xs: IEnumerable_1[T], comparer: IComparer_1[U]) -> T:
    def _arrow152(x: T, y: T, projection: Any = projection, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(projection(y), projection(x)) > int32.ZERO) else y

    return reduce(_arrow152, xs)


def min[T](xs: IEnumerable_1[T], comparer: IComparer_1[T]) -> T:
    def _arrow153(x: T, y: T, comparer: Any = comparer) -> T:
        return x if (comparer.Compare(y, x) > int32.ZERO) else y

    return reduce(_arrow153, xs)


def average[T](xs: IEnumerable_1[T], averager: IGenericAverager_1[T]) -> T:
    count: int32 = int32.ZERO

    def folder(acc: T, x: T, averager: Any = averager) -> T:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, x)

    total: Any = fold(folder, averager.GetZero(), xs)
    if count == int32.ZERO:
        raise Exception(SR_inputSequenceEmpty + " (Parameter 'source')")

    else:
        return averager.DivideByInt(total, count)


def average_by[T, U](f: Callable[[T], U], xs: IEnumerable_1[T], averager: IGenericAverager_1[U]) -> U:
    count: int32 = int32.ZERO

    def _arrow154(acc: U, x: T, f: Any = f, averager: Any = averager) -> U:
        nonlocal count
        count = count + int32.ONE
        return averager.Add(acc, f(x))

    total: Any = fold(_arrow154, averager.GetZero(), xs)
    if count == int32.ZERO:
        raise Exception(SR_inputSequenceEmpty + " (Parameter 'source')")

    else:
        return averager.DivideByInt(total, count)


def permute[T](f: Callable[[int32], int32], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow155(f: Any = f, xs: Any = xs) -> IEnumerable_1[T]:
        return of_array(permute_1(f, to_array(xs)))

    return delay(_arrow155)


def chunk_by_size[T](chunk_size: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[Array[T]]:
    def _arrow156(chunk_size: Any = chunk_size, xs: Any = xs) -> IEnumerable_1[Array[T]]:
        return of_array(chunk_by_size_1(chunk_size, to_array(xs)))

    return delay(_arrow156)


def insert_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    def _arrow157(xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow158(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y) -> Option[T]:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if is_done else (i < index)) else False:
            return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

        elif i == index:
            is_done = True
            return some(y)

        else:
            if not is_done:
                raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

            return None

    def _arrow159(e_1: IEnumerator[T]) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow157, _arrow158, _arrow159)


def insert_many_at[T](index: int32, ys: IEnumerable_1[T], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    status: int32 = int32.NEG_ONE
    if index < int32.ZERO:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    def _arrow160(ys: Any = ys, xs: Any = xs) -> tuple[IEnumerator[T], IEnumerator[T]]:
        return (of_seq(xs), of_seq(ys))

    def _arrow161(i: int32, tupled_arg: tuple[IEnumerator[T], IEnumerator[T]], index: Any = index) -> Option[T]:
        nonlocal status
        e1: IEnumerator[Any] = tupled_arg[0]
        e2: IEnumerator[Any] = tupled_arg[1]
        if i == index:
            status = int32.ZERO

        inserted: Option[Any]
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
                    raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

                return None

        else:
            return some(value_1(inserted))

    def _arrow162(tupled_arg_1: tuple[IEnumerator[T], IEnumerator[T]]) -> None:
        dispose_2(tupled_arg_1[0])
        dispose_2(tupled_arg_1[1])

    return generate_indexed(_arrow160, _arrow161, _arrow162)


def remove_at[T](index: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    def _arrow163(xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow164(i: int32, e: IEnumerator[T], index: Any = index) -> Option[T]:
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
                raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

            return None

    def _arrow165(e_1: IEnumerator[T]) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow163, _arrow164, _arrow165)


def remove_many_at[T](index: int32, count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    if index < int32.ZERO:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    def _arrow166(xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow167(i: int32, e: IEnumerator[T], index: Any = index, count: Any = count) -> Option[T]:
        if i < index:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

            else:
                raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

        else:
            if i == index:
                for _ in range(int32.ONE, count, 1):
                    if not e.System_Collections_IEnumerator_MoveNext():
                        raise Exception(SR_indexOutOfBounds + " (Parameter 'count')")

            return (
                some(e.System_Collections_Generic_IEnumerator_1_get_Current())
                if e.System_Collections_IEnumerator_MoveNext()
                else None
            )

    def _arrow168(e_1: IEnumerator[T]) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow166, _arrow167, _arrow168)


def update_at[T](index: int32, y: T, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    is_done: bool = False
    if index < int32.ZERO:
        raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

    def _arrow169(xs: Any = xs) -> IEnumerator[T]:
        return of_seq(xs)

    def _arrow170(i: int32, e: IEnumerator[T], index: Any = index, y: Any = y) -> Option[T]:
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if is_done else (i < index)) else False:
            return some(e.System_Collections_Generic_IEnumerator_1_get_Current())

        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else False:
            is_done = True
            return some(y)

        else:
            if not is_done:
                raise Exception(SR_indexOutOfBounds + " (Parameter 'index')")

            return None

    def _arrow171(e_1: IEnumerator[T]) -> None:
        dispose_2(e_1)

    return generate_indexed(_arrow169, _arrow170, _arrow171)


def random_shuffle_by[T](randomizer: Callable[[], float64], xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    arr: Array[Any] = to_array(xs)
    random_shuffle_in_place_by(randomizer, arr)
    return of_array(arr)


def random_shuffle_with[T](random: Any, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow172(random: Any = random) -> float64:
        return random_double(random)

    return random_shuffle_by(_arrow172, xs)


def random_shuffle[T](xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return random_shuffle_with(create_random(), xs)


def random_choice_by[T](randomizer: Callable[[], float64], xs: IEnumerable_1[T]) -> T:
    return random_choice_by_1(randomizer, to_array(xs))


def random_choice_with[T](random: Any, xs: IEnumerable_1[T]) -> T:
    return random_choice_with_1(random, to_array(xs))


def random_choice[T](xs: IEnumerable_1[T]) -> T:
    return random_choice_1(to_array(xs))


def random_choices_by[T](randomizer: Callable[[], float64], count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return of_array(random_choices_by_1(randomizer, count, to_array(xs)))


def random_choices_with[T](random: Any, count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow173(random: Any = random) -> float64:
        return random_double(random)

    return random_choices_by(_arrow173, count, xs)


def random_choices[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return random_choices_with(create_random(), count, xs)


def random_sample_by[T](randomizer: Callable[[], float64], count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return of_array(random_sample_by_1(randomizer, count, to_array(xs)))


def random_sample_with[T](random: Any, count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    def _arrow174(random: Any = random) -> float64:
        return random_double(random)

    return random_sample_by(_arrow174, count, xs)


def random_sample[T](count: int32, xs: IEnumerable_1[T]) -> IEnumerable_1[T]:
    return random_sample_with(create_random(), count, xs)


__all__ = [
    "CachedSeq_1__Clear",
    "CachedSeq_1_reflection",
    "EnumerateTryWithState_1_reflection",
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
    "average",
    "average_by",
    "cache",
    "cast",
    "chunk_by_size",
    "compare_with",
    "concat",
    "contains",
    "delay",
    "empty",
    "enumerate_from_functions",
    "enumerate_then_finally",
    "enumerate_try_with",
    "enumerate_using",
    "enumerate_while",
    "exactly_one",
    "exists",
    "exists2",
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
    "index_not_found",
    "indexed",
    "initialize",
    "initialize_infinite",
    "insert_at",
    "insert_many_at",
    "is_empty",
    "iterate",
    "iterate2",
    "iterate_indexed",
    "iterate_indexed2",
    "last",
    "length",
    "map_fold",
    "map_fold_back",
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
    "to_array",
    "to_list",
    "transpose",
    "try_exactly_one",
    "try_find",
    "try_find_back",
    "try_find_index",
    "try_find_index_back",
    "try_last",
    "try_pick",
    "update_at",
    "where",
    "windowed",
    "zip",
    "zip3",
]
