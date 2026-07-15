from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from .array_ import Array, copy_to, fill, initialize, of_seq, zero_create
from .bases import EnumerableBase
from .core import FSharpRef, float64, int32
from .global_ import SR_Arg_KeyNotFound
from .protocols import IEnumerable_1, IEnumerator
from .reflection import TypeInfo, class_type
from .seq import delay, empty, enumerate_while, singleton
from .seq_native import append
from .system import ArgumentOutOfRangeException__ctor_Z721C83C5
from .types import ExceptionBase
from .util import UNIT, Disposable, Unit, compare, compare_primitives, get_enumerator, max, structural_hash
from .util import equals as equals_1


def _expr209() -> TypeInfo:
    return class_type(
        "System.Collections.Generic.KeyNotFoundException", None, KeyNotFoundException, class_type("System.Exception")
    )


class KeyNotFoundException(ExceptionBase):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


KeyNotFoundException_reflection = _expr209


def KeyNotFoundException__ctor_Z721C83C5(message: str) -> KeyNotFoundException:
    return KeyNotFoundException(message)


def KeyNotFoundException__ctor(__unit: Unit = UNIT) -> KeyNotFoundException:
    return KeyNotFoundException__ctor_Z721C83C5(SR_Arg_KeyNotFound)


def _expr210(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Comparer`1", Array([gen0]), Comparer_1)


class Comparer_1[T]:
    def __init__(self, comparison: Callable[[T, T], int32]) -> None:
        self.comparison: Callable[[Any, Any], int32] = comparison

    def Compare(self, x: T, y: T) -> int32:
        _: Comparer_1[Any] = self
        return (
            (int32.ZERO if equals_1(y, cast(Any, None)) else int32.NEG_ONE)
            if equals_1(x, cast(Any, None))
            else (int32.ONE if equals_1(y, cast(Any, None)) else _.comparison(x, y))
        )


Comparer_1_reflection = _expr210


def Comparer_1__ctor_47C913C[T](comparison: Callable[[T, T], int32]) -> Comparer_1[T]:
    return Comparer_1(comparison)


def Comparer_1_get_Default[T](__unit: Unit = UNIT) -> Comparer_1[T]:
    return Comparer_1__ctor_47C913C(compare)


def Comparer_1_Create_47C913C[T](comparison: Callable[[T, T], int32]) -> Comparer_1[T]:
    return Comparer_1__ctor_47C913C(comparison)


def Comparer_1__Compare_5BDDA0[T](_: Comparer_1[T], x: T, y: T) -> int32:
    return _.comparison(x, y)


def _expr212(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.EqualityComparer`1", Array([gen0]), EqualityComparer_1)


class EqualityComparer_1[T]:
    def __init__(self, equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]) -> None:
        self.equals: Callable[[Any, Any], bool] = equals
        self.get_hash_code: Callable[[Any], int32] = get_hash_code

    def Equals(self, x: T, y: T) -> bool:
        _: EqualityComparer_1[Any] = self
        return (
            (True if equals_1(y, cast(Any, None)) else False)
            if equals_1(x, cast(Any, None))
            else (False if equals_1(y, cast(Any, None)) else _.equals(x, y))
        )

    def GetHashCode(self, x: T = UNIT) -> int32:
        _: EqualityComparer_1[Any] = self
        return _.get_hash_code(x)


EqualityComparer_1_reflection = _expr212


def EqualityComparer_1__ctor_Z6EE254AB[T](
    equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]
) -> EqualityComparer_1[T]:
    return EqualityComparer_1(equals, get_hash_code)


def EqualityComparer_1_get_Default[T](__unit: Unit = UNIT) -> EqualityComparer_1[T]:
    def _arrow213(obj: T = UNIT) -> int32:
        return structural_hash(obj)

    return EqualityComparer_1__ctor_Z6EE254AB(equals_1, _arrow213)


def EqualityComparer_1_Create_Z6EE254AB[T](
    equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]
) -> EqualityComparer_1[T]:
    return EqualityComparer_1__ctor_Z6EE254AB(equals, get_hash_code)


def EqualityComparer_1__Equals_5BDDA0[T](_: EqualityComparer_1[T], x: T, y: T) -> bool:
    return _.equals(x, y)


def EqualityComparer_1__GetHashCode_2B595[T](_: EqualityComparer_1[T], x: T) -> int32:
    return _.get_hash_code(x)


def _expr218(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Stack`1", Array([gen0]), Stack_1)


class Stack_1[T](EnumerableBase[Any]):
    def __init__(self, initial_contents: Array[T], initial_count: int32) -> None:
        self.contents: Array[Any] = initial_contents
        self.count: int32 = initial_count

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        _: Stack_1[Any] = self

        def _arrow217(__unit: Unit = UNIT) -> IEnumerable_1[T]:
            index: int32 = _.count - int32.ONE

            def _arrow214(__unit: Unit = UNIT) -> bool:
                return index >= int32.ZERO

            def _arrow216(__unit: Unit = UNIT) -> IEnumerable_1[T]:
                def _arrow215(__unit: Unit = UNIT) -> IEnumerable_1[T]:
                    nonlocal index
                    index = index - int32.ONE
                    return empty()

                return append(singleton(_.contents[index]), delay(_arrow215))

            return enumerate_while(_arrow214, delay(_arrow216))

        return get_enumerator(delay(_arrow217))

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        this: Stack_1[Any] = self
        return get_enumerator(this)


Stack_1_reflection = _expr218


def Stack_1__ctor_Z3B4C077E[T](initial_contents: Array[T], initial_count: int32) -> Stack_1[T]:
    return Stack_1(initial_contents, initial_count)


def Stack_1__ctor_Z524259A4[T](initial_capacity: int32) -> Stack_1[T]:
    return Stack_1__ctor_Z3B4C077E(zero_create(initial_capacity, cast(Any, None)), int32.ZERO)


def Stack_1__ctor[T](__unit: Unit = UNIT) -> Stack_1[T]:
    return Stack_1__ctor_Z524259A4(int32.FOUR)


def Stack_1__ctor_BB573A[T](xs: IEnumerable_1[T]) -> Stack_1[T]:
    arr: Array[Any] = of_seq(xs)
    return Stack_1__ctor_Z3B4C077E(arr, int32(len(arr)))


def Stack_1__Ensure_Z524259A4[T](_: Stack_1[T], new_size: int32) -> None:
    old_size: int32 = int32(len(_.contents))
    if new_size > old_size:
        old: Array[Any] = _.contents
        _.contents = zero_create(max(compare_primitives, new_size, old_size * int32.TWO), cast(Any, None))
        copy_to(old, int32.ZERO, _.contents, int32.ZERO, _.count)


def Stack_1__get_Count[T](_: Stack_1[T]) -> int32:
    return _.count


def Stack_1__Pop[T](_: Stack_1[T]) -> T:
    _.count = _.count - int32.ONE
    return _.contents[_.count]


def Stack_1__Peek[T](_: Stack_1[T]) -> T:
    return _.contents[_.count - int32.ONE]


def Stack_1__Contains_2B595[T](_: Stack_1[T], x: T) -> bool:
    found: bool = False
    i: int32 = int32.ZERO
    while (not found) if (i < _.count) else False:
        if equals_1(x, _.contents[i]):
            found = True

        else:
            i = i + int32.ONE

    return found


def Stack_1__TryPeek_1F3DB691[T](this: Stack_1[T], result: FSharpRef[T]) -> bool:
    if this.count > int32.ZERO:
        result.contents = Stack_1__Peek(this)
        return True

    else:
        return False


def Stack_1__TryPop_1F3DB691[T](this: Stack_1[T], result: FSharpRef[T]) -> bool:
    if this.count > int32.ZERO:
        result.contents = Stack_1__Pop(this)
        return True

    else:
        return False


def Stack_1__Push_2B595[T](this: Stack_1[T], x: T) -> None:
    Stack_1__Ensure_Z524259A4(this, this.count + int32.ONE)
    this.contents[this.count] = x
    this.count = this.count + int32.ONE


def Stack_1__Clear[T](_: Stack_1[T]) -> None:
    _.count = int32.ZERO
    fill(_.contents, int32.ZERO, int32(len(_.contents)), cast(Any, None))


def Stack_1__TrimExcess[T](this: Stack_1[T]) -> None:
    if (float64(this.count) / float64(int32(len(this.contents)))) > float64(0.9):
        Stack_1__Ensure_Z524259A4(this, this.count)


def Stack_1__ToArray[T](_: Stack_1[T]) -> Array[T]:
    def _arrow219(i: int32, _: Any = _) -> T:
        return _.contents[(_.count - int32.ONE) - i]

    return initialize(_.count, _arrow219, None)


def _expr220(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Queue`1", Array([gen0]), Queue_1)


class Queue_1[T](EnumerableBase[Any]):
    def __init__(self, initial_contents: Array[T], initial_count: int32) -> None:
        self.contents: Array[Any] = initial_contents
        self.count: int32 = initial_count
        self.head: int32 = int32.ZERO
        self.tail: int32 = int32.ZERO if (initial_count == int32(len(self.contents))) else initial_count

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        _: Queue_1[Any] = self
        return get_enumerator(Queue_1__toSeq(_))

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        this: Queue_1[Any] = self
        return get_enumerator(this)


Queue_1_reflection = _expr220


def Queue_1__ctor_Z3B4C077E[T](initial_contents: Array[T], initial_count: int32) -> Queue_1[T]:
    return Queue_1(initial_contents, initial_count)


def Queue_1__ctor_Z524259A4[T](initial_capacity: int32) -> Queue_1[T]:
    if initial_capacity < int32.ZERO:
        raise ArgumentOutOfRangeException__ctor_Z721C83C5("capacity is less than 0")

    return Queue_1__ctor_Z3B4C077E(zero_create(initial_capacity, cast(Any, None)), int32.ZERO)


def Queue_1__ctor[T](__unit: Unit = UNIT) -> Queue_1[T]:
    return Queue_1__ctor_Z524259A4(int32.FOUR)


def Queue_1__ctor_BB573A[T](xs: IEnumerable_1[T]) -> Queue_1[T]:
    arr: Array[Any] = of_seq(xs)
    return Queue_1__ctor_Z3B4C077E(arr, int32(len(arr)))


def Queue_1__get_Count[T](_: Queue_1[T]) -> int32:
    return _.count


def Queue_1__Enqueue_2B595[T](_: Queue_1[T], value: T) -> None:
    if _.count == Queue_1__size(_):
        Queue_1__ensure_Z524259A4(_, _.count + int32.ONE)

    _.contents[_.tail] = value
    _.tail = (_.tail + int32.ONE) % Queue_1__size(_)
    _.count = _.count + int32.ONE


def Queue_1__Dequeue[T](_: Queue_1[T]) -> T:
    if _.count == int32.ZERO:
        raise Exception("Queue is empty")

    value: Any = _.contents[_.head]
    _.head = (_.head + int32.ONE) % Queue_1__size(_)
    _.count = _.count - int32.ONE
    return value


def Queue_1__Peek[T](_: Queue_1[T]) -> T:
    if _.count == int32.ZERO:
        raise Exception("Queue is empty")

    return _.contents[_.head]


def Queue_1__TryDequeue_1F3DB691[T](this: Queue_1[T], result: FSharpRef[T]) -> bool:
    if this.count == int32.ZERO:
        return False

    else:
        result.contents = Queue_1__Dequeue(this)
        return True


def Queue_1__TryPeek_1F3DB691[T](this: Queue_1[T], result: FSharpRef[T]) -> bool:
    if this.count == int32.ZERO:
        return False

    else:
        result.contents = Queue_1__Peek(this)
        return True


def Queue_1__Contains_2B595[T](_: Queue_1[T], x: T) -> bool:
    found: bool = False
    i: int32 = int32.ZERO
    while (not found) if (i < _.count) else False:
        if equals_1(x, _.contents[Queue_1__toIndex_Z524259A4(_, i)]):
            found = True

        else:
            i = i + int32.ONE

    return found


def Queue_1__Clear[T](_: Queue_1[T]) -> None:
    _.count = int32.ZERO
    _.head = int32.ZERO
    _.tail = int32.ZERO
    fill(_.contents, int32.ZERO, Queue_1__size(_), cast(Any, None))


def Queue_1__TrimExcess[T](_: Queue_1[T]) -> None:
    if (float64(_.count) / float64(int32(len(_.contents)))) > float64(0.9):
        Queue_1__ensure_Z524259A4(_, _.count)


def Queue_1__ToArray[T](_: Queue_1[T]) -> Array[T]:
    return Array[Any](Queue_1__toSeq(_))


def Queue_1__CopyTo_Z3B4C077E[T](_: Queue_1[T], target: Array[T], start: int32) -> None:
    i: int32 = start
    with Disposable(get_enumerator(Queue_1__toSeq(_))) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            item: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            target[i] = item
            i = i + int32.ONE


def Queue_1__size[T](this: Queue_1[T]) -> int32:
    return int32(len(this.contents))


def Queue_1__toIndex_Z524259A4[T](this: Queue_1[T], i: int32) -> int32:
    return (this.head + i) % Queue_1__size(this)


def Queue_1__ensure_Z524259A4[T](this: Queue_1[T], required_size: int32) -> None:
    new_buffer: Array[Any] = zero_create(required_size, cast(Any, None))
    if this.head < this.tail:
        copy_to(this.contents, this.head, new_buffer, int32.ZERO, this.count)

    else:
        copy_to(this.contents, this.head, new_buffer, int32.ZERO, Queue_1__size(this) - this.head)
        copy_to(this.contents, int32.ZERO, new_buffer, Queue_1__size(this) - this.head, this.tail)

    this.head = int32.ZERO
    this.contents = new_buffer
    this.tail = int32.ZERO if (this.count == Queue_1__size(this)) else this.count


def Queue_1__toSeq[T](this: Queue_1[T]) -> IEnumerable_1[T]:
    def _arrow224(this: Any = this) -> IEnumerable_1[T]:
        i: int32 = int32.ZERO

        def _arrow221(__unit: Unit = UNIT) -> bool:
            return i < this.count

        def _arrow223(__unit: Unit = UNIT) -> IEnumerable_1[T]:
            def _arrow222(__unit: Unit = UNIT) -> IEnumerable_1[T]:
                nonlocal i
                i = i + int32.ONE
                return empty()

            return append(singleton(this.contents[Queue_1__toIndex_Z524259A4(this, i)]), delay(_arrow222))

        return enumerate_while(_arrow221, delay(_arrow223))

    return delay(_arrow224)


__all__ = [
    "Comparer_1_Create_47C913C",
    "Comparer_1__Compare_5BDDA0",
    "Comparer_1_get_Default",
    "Comparer_1_reflection",
    "EqualityComparer_1_Create_Z6EE254AB",
    "EqualityComparer_1__Equals_5BDDA0",
    "EqualityComparer_1__GetHashCode_2B595",
    "EqualityComparer_1_get_Default",
    "EqualityComparer_1_reflection",
    "KeyNotFoundException__ctor",
    "KeyNotFoundException_reflection",
    "Queue_1__Clear",
    "Queue_1__Contains_2B595",
    "Queue_1__CopyTo_Z3B4C077E",
    "Queue_1__Dequeue",
    "Queue_1__Enqueue_2B595",
    "Queue_1__Peek",
    "Queue_1__ToArray",
    "Queue_1__TrimExcess",
    "Queue_1__TryDequeue_1F3DB691",
    "Queue_1__TryPeek_1F3DB691",
    "Queue_1__ctor",
    "Queue_1__ctor_BB573A",
    "Queue_1__ctor_Z524259A4",
    "Queue_1__ensure_Z524259A4",
    "Queue_1__get_Count",
    "Queue_1__size",
    "Queue_1__toIndex_Z524259A4",
    "Queue_1__toSeq",
    "Queue_1_reflection",
    "Stack_1__Clear",
    "Stack_1__Contains_2B595",
    "Stack_1__Ensure_Z524259A4",
    "Stack_1__Peek",
    "Stack_1__Pop",
    "Stack_1__Push_2B595",
    "Stack_1__ToArray",
    "Stack_1__TrimExcess",
    "Stack_1__TryPeek_1F3DB691",
    "Stack_1__TryPop_1F3DB691",
    "Stack_1__ctor",
    "Stack_1__ctor_BB573A",
    "Stack_1__ctor_Z524259A4",
    "Stack_1__get_Count",
    "Stack_1_reflection",
]
