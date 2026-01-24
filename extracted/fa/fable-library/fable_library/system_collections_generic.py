from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array, copy_to, create, fill, initialize, of_seq
from .global_ import SR_Arg_KeyNotFound
from .reflection import TypeInfo, class_type
from .seq import append, delay, empty, enumerate_while, singleton
from .system import ArgumentOutOfRangeException__ctor_Z721C83C5
from .types import FSharpRef, float64, int32
from .util import (
    IEnumerable_1,
    IEnumerator,
    compare,
    compare_primitives,
    get_enumerator,
    max,
    structural_hash,
    to_iterator,
)
from .util import equals as equals_1


def _expr228() -> TypeInfo:
    return class_type(
        "System.Collections.Generic.KeyNotFoundException", None, KeyNotFoundException, class_type("System.Exception")
    )


class KeyNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        pass


KeyNotFoundException_reflection = _expr228


def KeyNotFoundException__ctor_Z721C83C5(message: str) -> KeyNotFoundException:
    return KeyNotFoundException(message)


def KeyNotFoundException__ctor(__unit: None = None) -> KeyNotFoundException:
    return KeyNotFoundException__ctor_Z721C83C5(SR_Arg_KeyNotFound)


def _expr229(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Comparer`1", [gen0], Comparer_1)


class Comparer_1[T]:
    def __init__(self, comparison: Callable[[T, T], int32]) -> None:
        self.comparison: Callable[[T, T], int32] = comparison

    def Compare[T](self, x: T, y: T) -> int32:
        _: Comparer_1[T] = self
        return (
            (int32.ZERO if equals_1(y, None) else int32.NEG_ONE)
            if equals_1(x, None)
            else (int32.ONE if equals_1(y, None) else _.comparison(x, y))
        )


Comparer_1_reflection = _expr229


def Comparer_1__ctor_47C913C(comparison: Callable[[T, T], int32]) -> Comparer_1[T]:
    return Comparer_1(comparison)


def Comparer_1_get_Default[T](__unit: None = None) -> Comparer_1[Any]:
    return Comparer_1__ctor_47C913C(compare)


def Comparer_1_Create_47C913C[T](comparison: Callable[[T, T], int32]) -> Comparer_1[T]:
    return Comparer_1__ctor_47C913C(comparison)


def Comparer_1__Compare_5BDDA0[T](_: Comparer_1[T], x: T, y: T) -> int32:
    return _.comparison(x, y)


def _expr230(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.EqualityComparer`1", [gen0], EqualityComparer_1)


class EqualityComparer_1[T]:
    def __init__(self, equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]) -> None:
        self.equals: Callable[[T, T], bool] = equals
        self.get_hash_code: Callable[[T], int32] = get_hash_code

    def __eq__[T](self, x: T, y: T) -> bool:
        _: EqualityComparer_1[T] = self
        return (
            (True if equals_1(y, None) else False)
            if equals_1(x, None)
            else (False if equals_1(y, None) else _.equals(x, y))
        )

    def GetHashCode[T](self, x: T | None = None) -> int32:
        _: EqualityComparer_1[T] = self
        return _.get_hash_code(x)


EqualityComparer_1_reflection = _expr230


def EqualityComparer_1__ctor_Z6EE254AB(
    equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]
) -> EqualityComparer_1[T]:
    return EqualityComparer_1(equals, get_hash_code)


def EqualityComparer_1_get_Default[T](__unit: None = None) -> EqualityComparer_1[Any]:
    return EqualityComparer_1__ctor_Z6EE254AB(equals_1, structural_hash)


def EqualityComparer_1_Create_Z6EE254AB[T](
    equals: Callable[[T, T], bool], get_hash_code: Callable[[T], int32]
) -> EqualityComparer_1[T]:
    return EqualityComparer_1__ctor_Z6EE254AB(equals, get_hash_code)


def EqualityComparer_1__Equals_5BDDA0[T](_: EqualityComparer_1[T], x: T, y: T) -> bool:
    return _.equals(x, y)


def EqualityComparer_1__GetHashCode_2B595[T](_: EqualityComparer_1[T], x: T) -> int32:
    return _.get_hash_code(x)


def _expr235(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Stack`1", [gen0], Stack_1)


class Stack_1[T]:
    def __init__(self, initial_contents: Array[Any], initial_count: int32) -> None:
        self.contents: Array[T] = initial_contents
        self.count: int32 = initial_count

    def GetEnumerator[T](self, __unit: None = None) -> IEnumerator[T]:
        _: Stack_1[T] = self

        def _arrow234(__unit: None = None) -> IEnumerable_1[T]:
            index: int32 = _.count - int32.ONE

            def _arrow231(__unit: None = None) -> bool:
                return index >= int32.ZERO

            def _arrow233(__unit: None = None) -> IEnumerable_1[T]:
                def _arrow232(__unit: None = None) -> IEnumerable_1[T]:
                    nonlocal index
                    index = index - int32.ONE
                    return empty()

                return append(singleton(_.contents[index]), delay(_arrow232))

            return enumerate_while(_arrow231, delay(_arrow233))

        return get_enumerator(delay(_arrow234))

    def __iter__[T](self) -> IEnumerator[T]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        this: Stack_1[T] = self
        return get_enumerator(this)


Stack_1_reflection = _expr235


def Stack_1__ctor_Z3B4C077E(initial_contents: Array[Any], initial_count: int32) -> Stack_1[T]:
    return Stack_1(initial_contents, initial_count)


def Stack_1__ctor_Z524259A4[T](initial_capacity: int32) -> Stack_1[Any]:
    return Stack_1__ctor_Z3B4C077E(create(initial_capacity, None), int32.ZERO)


def Stack_1__ctor[T](__unit: None = None) -> Stack_1[Any]:
    return Stack_1__ctor_Z524259A4(int32.FOUR)


def Stack_1__ctor_BB573A[T](xs: IEnumerable_1[T]) -> Stack_1[T]:
    arr: Array[T] = of_seq(xs)
    return Stack_1__ctor_Z3B4C077E(arr, len(arr))


def Stack_1__Ensure_Z524259A4(_: Stack_1[Any], new_size: int32) -> None:
    old_size: int32 = len(_.contents)
    if new_size > old_size:
        old: Array[T] = _.contents

        def _arrow236(x: int32, y: int32, _: Any = _, new_size: Any = new_size) -> int32:
            return compare_primitives(x, y)

        _.contents = create(max(_arrow236, new_size, old_size * int32.TWO), None)
        copy_to(old, int32.ZERO, _.contents, int32.ZERO, _.count)


def Stack_1__get_Count(_: Stack_1[Any]) -> int32:
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


def Stack_1__Clear(_: Stack_1[Any]) -> None:
    _.count = int32.ZERO
    fill(_.contents, int32.ZERO, len(_.contents), None)


def Stack_1__TrimExcess(this: Stack_1[Any]) -> None:
    if (float64(this.count) / float64(len(this.contents))) > float64(0.9):
        Stack_1__Ensure_Z524259A4(this, this.count)


def Stack_1__ToArray[T](_: Stack_1[T]) -> Array[T]:
    def _arrow237(i: int32, _: Any = _) -> T:
        return _.contents[(_.count - int32.ONE) - i]

    return initialize(_.count, _arrow237, None)


def _expr238(gen0: TypeInfo) -> TypeInfo:
    return class_type("System.Collections.Generic.Queue`1", [gen0], Queue_1)


class Queue_1[T]:
    def __init__(self, initial_contents: Array[Any], initial_count: int32) -> None:
        self.contents: Array[T] = initial_contents
        self.count: int32 = initial_count
        self.head: int32 = int32.ZERO
        self.tail: int32 = int32.ZERO if (initial_count == len(self.contents)) else initial_count

    def GetEnumerator[T](self, __unit: None = None) -> IEnumerator[T]:
        _: Queue_1[T] = self
        return get_enumerator(Queue_1__toSeq(_))

    def __iter__[T](self) -> IEnumerator[T]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        this: Queue_1[T] = self
        return get_enumerator(this)


Queue_1_reflection = _expr238


def Queue_1__ctor_Z3B4C077E(initial_contents: Array[Any], initial_count: int32) -> Queue_1[T]:
    return Queue_1(initial_contents, initial_count)


def Queue_1__ctor_Z524259A4[T](initial_capacity: int32) -> Queue_1[Any]:
    if initial_capacity < int32.ZERO:
        raise ArgumentOutOfRangeException__ctor_Z721C83C5("capacity is less than 0")

    return Queue_1__ctor_Z3B4C077E(create(initial_capacity, None), int32.ZERO)


def Queue_1__ctor[T](__unit: None = None) -> Queue_1[Any]:
    return Queue_1__ctor_Z524259A4(int32.FOUR)


def Queue_1__ctor_BB573A[T](xs: IEnumerable_1[T]) -> Queue_1[T]:
    arr: Array[T] = of_seq(xs)
    return Queue_1__ctor_Z3B4C077E(arr, len(arr))


def Queue_1__get_Count(_: Queue_1[Any]) -> int32:
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

    value: T = _.contents[_.head]
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


def Queue_1__Clear(_: Queue_1[Any]) -> None:
    _.count = int32.ZERO
    _.head = int32.ZERO
    _.tail = int32.ZERO
    fill(_.contents, int32.ZERO, Queue_1__size(_), None)


def Queue_1__TrimExcess(_: Queue_1[Any]) -> None:
    if (float64(_.count) / float64(len(_.contents))) > float64(0.9):
        Queue_1__ensure_Z524259A4(_, _.count)


def Queue_1__ToArray[T](_: Queue_1[T]) -> Array[T]:
    return Array[Any](Queue_1__toSeq(_))


def Queue_1__CopyTo_Z3B4C077E[T](_: Queue_1[T], target: Array[T], start: int32) -> None:
    i: int32 = start
    with get_enumerator(Queue_1__toSeq(_)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            item: T = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            target[i] = item
            i = i + int32.ONE


def Queue_1__size(this: Queue_1[Any]) -> int32:
    return len(this.contents)


def Queue_1__toIndex_Z524259A4(this: Queue_1[Any], i: int32) -> int32:
    return (this.head + i) % Queue_1__size(this)


def Queue_1__ensure_Z524259A4(this: Queue_1[Any], required_size: int32) -> None:
    new_buffer: Array[T] = create(required_size, None)
    if this.head < this.tail:
        copy_to(this.contents, this.head, new_buffer, int32.ZERO, this.count)

    else:
        copy_to(this.contents, this.head, new_buffer, int32.ZERO, Queue_1__size(this) - this.head)
        copy_to(this.contents, int32.ZERO, new_buffer, Queue_1__size(this) - this.head, this.tail)

    this.head = int32.ZERO
    this.contents = new_buffer
    this.tail = int32.ZERO if (this.count == Queue_1__size(this)) else this.count


def Queue_1__toSeq[T](this: Queue_1[T]) -> IEnumerable_1[T]:
    def _arrow242(__unit: None = None, this: Any = this) -> IEnumerable_1[T]:
        i: int32 = int32.ZERO

        def _arrow239(__unit: None = None) -> bool:
            return i < this.count

        def _arrow241(__unit: None = None) -> IEnumerable_1[T]:
            def _arrow240(__unit: None = None) -> IEnumerable_1[T]:
                nonlocal i
                i = i + int32.ONE
                return empty()

            return append(singleton(this.contents[Queue_1__toIndex_Z524259A4(this, i)]), delay(_arrow240))

        return enumerate_while(_arrow239, delay(_arrow241))

    return delay(_arrow242)


__all__ = [
    "KeyNotFoundException_reflection",
    "KeyNotFoundException__ctor",
    "Comparer_1_reflection",
    "Comparer_1_get_Default",
    "Comparer_1_Create_47C913C",
    "Comparer_1__Compare_5BDDA0",
    "EqualityComparer_1_reflection",
    "EqualityComparer_1_get_Default",
    "EqualityComparer_1_Create_Z6EE254AB",
    "EqualityComparer_1__Equals_5BDDA0",
    "EqualityComparer_1__GetHashCode_2B595",
    "Stack_1_reflection",
    "Stack_1__ctor_Z524259A4",
    "Stack_1__ctor",
    "Stack_1__ctor_BB573A",
    "Stack_1__Ensure_Z524259A4",
    "Stack_1__get_Count",
    "Stack_1__Pop",
    "Stack_1__Peek",
    "Stack_1__Contains_2B595",
    "Stack_1__TryPeek_1F3DB691",
    "Stack_1__TryPop_1F3DB691",
    "Stack_1__Push_2B595",
    "Stack_1__Clear",
    "Stack_1__TrimExcess",
    "Stack_1__ToArray",
    "Queue_1_reflection",
    "Queue_1__ctor_Z524259A4",
    "Queue_1__ctor",
    "Queue_1__ctor_BB573A",
    "Queue_1__get_Count",
    "Queue_1__Enqueue_2B595",
    "Queue_1__Dequeue",
    "Queue_1__Peek",
    "Queue_1__TryDequeue_1F3DB691",
    "Queue_1__TryPeek_1F3DB691",
    "Queue_1__Contains_2B595",
    "Queue_1__Clear",
    "Queue_1__TrimExcess",
    "Queue_1__ToArray",
    "Queue_1__CopyTo_Z3B4C077E",
    "Queue_1__size",
    "Queue_1__toIndex_Z524259A4",
    "Queue_1__ensure_Z524259A4",
    "Queue_1__toSeq",
]
