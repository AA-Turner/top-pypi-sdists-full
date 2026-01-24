from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array
from .map_util import get_item_from_dict, try_get_value
from .native import Helpers_arrayFrom
from .option import some
from .reflection import TypeInfo, class_type
from .resize_array import find_index
from .seq import concat, iterate, iterate_indexed, map
from .types import FSharpRef, int32
from .util import IEnumerable_1, IEnumerator, IEqualityComparer_1, dispose, get_enumerator, ignore, to_iterator
from .util import int32 as int32_1


def _expr13(gen0: TypeInfo) -> TypeInfo:
    return class_type("Fable.Collections.HashSet", [gen0], HashSet)


class HashSet[T]:
    def __init__(self, items: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> None:
        this: FSharpRef[HashSet[T]] = FSharpRef(None)
        self.comparer: IEqualityComparer_1[Any] = comparer
        this.contents = self
        self.hash_map: Any = dict(Array[Any]([]))
        self.init_00409: int32 = int32.ONE
        with get_enumerator(items) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                item: T = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                ignore(HashSet__Add_2B595(this.contents, item))

    @property
    def Symbol_toStringTag(self, __unit: None = None) -> str:
        return "HashSet"

    def to_json(self, __unit: None = None) -> Any:
        this: HashSet[T] = self
        return Helpers_arrayFrom(this)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        this: HashSet[T] = self
        return get_enumerator(this)

    def GetEnumerator[T](self, __unit: None = None) -> IEnumerator[T]:
        this: HashSet[T] = self
        return get_enumerator(concat(this.hash_map.values()))

    def __iter__[T](self) -> IEnumerator[T]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_Generic_ICollection_1_Add2B595[T](self, item: T | None = None) -> None:
        this: HashSet[T] = self
        ignore(HashSet__Add_2B595(this, item))

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: None = None) -> None:
        this: HashSet[T] = self
        HashSet__Clear(this)

    def System_Collections_Generic_ICollection_1_Contains2B595[T](self, item: T | None = None) -> bool:
        this: HashSet[T] = self
        return HashSet__Contains_2B595(this, item)

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E[T](self, array: Array[T], array_index: int32) -> None:
        this: HashSet[T] = self

        def action(i: int32, e: T) -> None:
            array[array_index + i] = e

        iterate_indexed(action, this)

    def __len__(self, __unit: None = None) -> int32:
        this: HashSet[T] = self
        return HashSet__get_Count(this)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: None = None) -> bool:
        return False

    def System_Collections_Generic_ICollection_1_Remove2B595[T](self, item: T | None = None) -> bool:
        this: HashSet[T] = self
        return HashSet__Remove_2B595(this, item)

    @property
    def size(self, __unit: None = None) -> int32:
        this: HashSet[T] = self
        return HashSet__get_Count(this)

    def add[T](self, k: T | None = None) -> Set_1[T]:
        this: HashSet[T] = self
        ignore(HashSet__Add_2B595(this, k))
        return this

    def clear(self, __unit: None = None) -> None:
        this: HashSet[T] = self
        HashSet__Clear(this)

    def __delitem__[T](self, k: T | None = None) -> bool:
        this: HashSet[T] = self
        return HashSet__Remove_2B595(this, k)

    def __contains__[T](self, k: T | None = None) -> bool:
        this: HashSet[T] = self
        return HashSet__Contains_2B595(this, k)

    def keys[T](self, __unit: None = None) -> IEnumerable_1[T]:
        this: HashSet[T] = self

        def mapping(x: T | None = None) -> T | None:
            return x

        return map(mapping, this)

    def values[T](self, __unit: None = None) -> IEnumerable_1[T]:
        this: HashSet[T] = self

        def mapping(x: T | None = None) -> T | None:
            return x

        return map(mapping, this)

    def entries[T](self, __unit: None = None) -> IEnumerable_1[tuple[T, T]]:
        this: HashSet[T] = self

        def mapping(v: T | None = None) -> tuple[T, T]:
            return (v, v)

        return map(mapping, this)

    def for_each(self, f: Callable[[T, T, Set_1[T]], None], this_arg: Any | None = None) -> None:
        this: HashSet[T] = self

        def action(x: T | None = None) -> None:
            f(x, x, this)

        iterate(action, this)


HashSet_reflection = _expr13


def HashSet__ctor_Z6150332D(items: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> HashSet[T]:
    return HashSet(items, comparer)


def HashSet__TryFindIndex_2B595[T](this: HashSet[T], k: T) -> tuple[bool, int32, int32]:
    h: int32 = this.comparer.GetHashCode(k)
    match_value: tuple[bool, list[T]]
    out_arg: list[T] = None

    def _arrow16(__unit: None = None, this: Any = this, k: Any = k) -> list[T]:
        return out_arg

    def _arrow17(v: list[T], this: Any = this, k: Any = k) -> None:
        nonlocal out_arg
        out_arg = v

    match_value = (try_get_value(this.hash_map, h, FSharpRef(_arrow16, _arrow17)), out_arg)
    if match_value[int32_1(0)]:

        def _arrow19(v_1: T | None = None, this: Any = this, k: Any = k) -> bool:
            return this.comparer.Equals(k, v_1)

        return (True, h, find_index(_arrow19, match_value[int32_1(1)]))

    else:
        return (False, h, int32.NEG_ONE)


def HashSet__TryFind_2B595[T](this: HashSet[T], k: T) -> T | None:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32_1(0)]:
        if match_value[int32_1(2)] > int32.NEG_ONE:
            pattern_matching_result = int32_1(0)

        else:
            pattern_matching_result = int32_1(1)

    else:
        pattern_matching_result = int32_1(1)

    if pattern_matching_result == int32.ZERO:
        return some(get_item_from_dict(this.hash_map, match_value[int32_1(1)])[match_value[int32_1(2)]])

    elif pattern_matching_result == int32.ONE:
        return None


def HashSet__get_Comparer[T](this: HashSet[T]) -> IEqualityComparer_1[Any]:
    return this.comparer


def HashSet__Clear(this: HashSet[Any]) -> None:
    this.hash_map.clear()


def HashSet__get_Count(this: HashSet[Any]) -> int32:
    count: int32 = int32.ZERO
    enumerator: Any = get_enumerator(this.hash_map.values())
    try:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            items: list[T] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            count = count + len(items)

    finally:
        dispose(enumerator)

    return count


def HashSet__Add_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    if match_value[int32_1(0)]:
        if match_value[int32_1(2)] > int32.NEG_ONE:
            return False

        else:
            value: None = get_item_from_dict(this.hash_map, match_value[int32_1(1)]).append(k)
            ignore(None)
            return True

    else:
        this.hash_map[match_value[int32_1(1)]] = [k]
        return True


def HashSet__Contains_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32_1(0)]:
        if match_value[int32_1(2)] > int32.NEG_ONE:
            pattern_matching_result = int32_1(0)

        else:
            pattern_matching_result = int32_1(1)

    else:
        pattern_matching_result = int32_1(1)

    if pattern_matching_result == int32.ZERO:
        return True

    elif pattern_matching_result == int32.ONE:
        return False


def HashSet__Remove_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32_1(0)]:
        if match_value[int32_1(2)] > int32.NEG_ONE:
            pattern_matching_result = int32_1(0)

        else:
            pattern_matching_result = int32_1(1)

    else:
        pattern_matching_result = int32_1(1)

    if pattern_matching_result == int32.ZERO:
        get_item_from_dict(this.hash_map, match_value[int32_1(1)]).pop(match_value[int32_1(2)])
        return True

    elif pattern_matching_result == int32.ONE:
        return False


__all__ = [
    "HashSet_reflection",
    "HashSet__TryFindIndex_2B595",
    "HashSet__TryFind_2B595",
    "HashSet__get_Comparer",
    "HashSet__Clear",
    "HashSet__get_Count",
    "HashSet__Add_2B595",
    "HashSet__Contains_2B595",
    "HashSet__Remove_2B595",
]
