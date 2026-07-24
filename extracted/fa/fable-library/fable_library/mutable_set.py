from __future__ import annotations

from collections.abc import MutableSet, Set
from typing import Any, cast

from fable_library.util import to_iterator

from .array_ import Array
from .bases import EnumerableBase
from .core import FSharpRef as FSharpRef_1
from .core import int32
from .map_util import get_item_from_dict, make_dict, try_get_value
from .option import Option, some
from .protocols import IEnumerable_1, IEnumerator, IEqualityComparer_1
from .reflection import TypeInfo, class_type
from .resize_array import find_index
from .seq import concat, iterate_indexed
from .types import FSharpRef
from .util import UNIT, Disposable, Unit, dispose, get_enumerator, ignore, to_enumerable


def _expr12(gen0: TypeInfo) -> TypeInfo:
    return class_type("Fable.Collections.HashSet", Array([gen0]), HashSet)


class HashSet[T](MutableSet[Any], Set[Any], EnumerableBase[Any]):
    def __init__(self, items: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> None:
        this: FSharpRef_1[HashSet[Any]] = FSharpRef(cast(HashSet[Any], None))
        self.comparer: IEqualityComparer_1[Any] = comparer
        this.contents = self
        self.hash_map: Any = make_dict(Array[Any]([]))
        self.init_004011: int32 = int32.ONE
        with Disposable(get_enumerator(items)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                item: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                ignore(HashSet__Add_2B595(this.contents, item))

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        this: HashSet[Any] = self
        return get_enumerator(this)

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[T]:
        this: HashSet[Any] = self
        return get_enumerator(concat(to_enumerable(this.hash_map.values())))

    def System_Collections_Generic_ICollection_1_Add2B595(self, item: T = UNIT) -> None:
        this: HashSet[Any] = self
        ignore(HashSet__Add_2B595(this, item))

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: Unit = UNIT) -> None:
        this: HashSet[Any] = self
        HashSet__Clear(this)

    def System_Collections_Generic_ICollection_1_Contains2B595(self, item: T = UNIT) -> bool:
        this: HashSet[Any] = self
        return HashSet__Contains_2B595(this, item)

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, array: Array[T], array_index: int32) -> None:
        this: HashSet[Any] = self

        def action(i: int32, e: T) -> None:
            array[array_index + i] = e

        iterate_indexed(action, this)

    def System_Collections_Generic_ICollection_1_get_Count(self, __unit: Unit = UNIT) -> int32:
        this: HashSet[Any] = self
        return HashSet__get_Count(this)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: Unit = UNIT) -> bool:
        return False

    def System_Collections_Generic_ICollection_1_Remove2B595(self, item: T = UNIT) -> bool:
        this: HashSet[Any] = self
        return HashSet__Remove_2B595(this, item)

    def Contains(self, item: T = UNIT) -> bool:
        this: HashSet[Any] = self
        return HashSet__Contains_2B595(this, item)

    @property
    def Count(self, __unit: Unit = UNIT) -> int32:
        this: HashSet[Any] = self
        return HashSet__get_Count(this)

    def Add(self, item: T = UNIT) -> None:
        this: HashSet[Any] = self
        ignore(HashSet__Add_2B595(this, item))

    def Remove(self, item: T = UNIT) -> bool:
        this: HashSet[Any] = self
        return HashSet__Remove_2B595(this, item)

    def Clear(self, __unit: Unit = UNIT) -> None:
        this: HashSet[Any] = self
        HashSet__Clear(this)

    def __contains__(self, item):
        return self.Contains(item)

    def __len__(self):
        return self.Count

    def __iter__(self):
        return to_iterator(self.GetEnumerator())

    def add(self, value):
        self.Add(value)

    def discard(self, value):
        self.Remove(value)


HashSet_reflection = _expr12


def HashSet__ctor_Z6150332D[T](items: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> HashSet[T]:
    return HashSet(items, comparer)


def HashSet__TryFindIndex_2B595[T](this: HashSet[T], k: T) -> tuple[bool, int32, int32]:
    h: int32 = this.comparer.GetHashCode(k)
    match_value: tuple[bool, list[Any]]
    out_arg: list[Any] = cast(list[Any], None)

    def _arrow14(__unit: Unit = UNIT) -> list[T]:
        return out_arg

    def _arrow15(v: list[T]) -> None:
        nonlocal out_arg
        out_arg = v

    match_value = (try_get_value(this.hash_map, h, FSharpRef_1(_arrow14, _arrow15)), out_arg)
    if match_value[0]:

        def _arrow18(v_1: T = UNIT, this: Any = this, k: Any = k) -> bool:
            return this.comparer.Equals(k, v_1)

        return (True, h, find_index(_arrow18, match_value[1]))

    else:
        return (False, h, int32.NEG_ONE)


def HashSet__TryFind_2B595[T](this: HashSet[T], k: T) -> Option[T]:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > int32.NEG_ONE:
            return some(get_item_from_dict(this.hash_map, match_value[1])[match_value[2]])

        case _:
            return None


def HashSet__get_Comparer[T](this: HashSet[T]) -> IEqualityComparer_1[Any]:
    return this.comparer


def HashSet__Clear[T](this: HashSet[T]) -> None:
    this.hash_map.clear()


def HashSet__get_Count[T](this: HashSet[T]) -> int32:
    count: int32 = int32.ZERO
    enumerator: Any = get_enumerator(to_enumerable(this.hash_map.values()))
    try:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            items: list[Any] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            count = count + int32(len(items))

    finally:
        dispose(enumerator)

    return count


def HashSet__Add_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    if match_value[0]:
        if match_value[2] > int32.NEG_ONE:
            return False

        else:
            value: None = get_item_from_dict(this.hash_map, match_value[1]).append(k)
            ignore(None)
            return True

    else:
        this.hash_map[match_value[1]] = [k]
        return True


def HashSet__Contains_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > int32.NEG_ONE:
            return True

        case _:
            return False


def HashSet__Remove_2B595[T](this: HashSet[T], k: T) -> bool:
    match_value: tuple[bool, int32, int32] = HashSet__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > int32.NEG_ONE:
            get_item_from_dict(this.hash_map, match_value[1]).pop(match_value[2])
            return True

        case _:
            return False


__all__ = [
    "HashSet__Add_2B595",
    "HashSet__Clear",
    "HashSet__Contains_2B595",
    "HashSet__Remove_2B595",
    "HashSet__TryFindIndex_2B595",
    "HashSet__TryFind_2B595",
    "HashSet__get_Comparer",
    "HashSet__get_Count",
    "HashSet_reflection",
]
