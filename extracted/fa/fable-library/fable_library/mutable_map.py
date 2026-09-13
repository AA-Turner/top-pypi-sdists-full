from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import Any, cast

from fable_library.util import to_iterator

from .array_ import Array
from .bases import EnumerableBase
from .core import FSharpRef, int32
from .map_util import get_item_from_dict, make_dict, try_get_value
from .option import erase
from .protocols import ICollection, IEnumerable_1, IEnumerator, IEqualityComparer_1
from .reflection import TypeInfo, class_type
from .resize_array import find_index
from .seq import concat, delay, iterate_indexed
from .seq_native import map
from .string_ import format
from .system import ArgumentException__ctor_Z721C83C5
from .types import ExceptionBase
from .types import FSharpRef as FSharpRef_1
from .util import UNIT, Disposable, Unit, dispose, equals, get_enumerator, ignore, nullable, to_enumerable


def _expr16(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Fable.Collections.Dictionary", Array([gen0, gen1]), Dictionary)


class Dictionary[KEY, VALUE](MutableMapping[Any, Any], Mapping[Any, Any], EnumerableBase[Any]):
    def __init__(self, pairs: IEnumerable_1[Any], comparer: IEqualityComparer_1[Any]) -> None:
        this: FSharpRef[Dictionary[Any, Any]] = FSharpRef_1(cast(Dictionary[Any, Any], None))
        self.comparer: IEqualityComparer_1[Any] = comparer
        this.contents = self
        self.hash_map: Any = make_dict(Array[Any]([]))
        self.init_004010: int = 1
        with Disposable(get_enumerator(pairs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                pair: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                Dictionary__Add_5BDDA1(this.contents, pair[0], pair[1])

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        this: Dictionary[Any, Any] = self
        return get_enumerator(this)

    def GetEnumerator(self, __unit: Unit = UNIT) -> IEnumerator[Any]:
        this: Dictionary[Any, Any] = self
        return get_enumerator(concat(to_enumerable(this.hash_map.values())))

    def System_Collections_Generic_ICollection_1_Add2B595(self, item: Any = UNIT) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__Add_5BDDA1(this, item[0], item[1])

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: Unit = UNIT) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__Clear(this)

    def System_Collections_Generic_ICollection_1_Contains2B595(self, item: Any = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        match_value: Any | None = erase(Dictionary__TryFind_2B595(this, item[0]))
        (pattern_matching_result,) = nullable[int]()
        if match_value is not None:
            if equals(match_value[1], item[1]):
                pattern_matching_result = 0

            else:
                pattern_matching_result = 1

        else:
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return True

        else:
            return False

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, array: Array[Any], array_index: int) -> None:
        this: Dictionary[Any, Any] = self

        def action(i: int, e: Any) -> None:
            array[tmp if (-2147483648 <= (tmp := array_index + i) <= 2147483647) else int32(tmp)] = e

        iterate_indexed(action, this)

    def System_Collections_Generic_ICollection_1_get_Count(self, __unit: Unit = UNIT) -> int:
        this: Dictionary[Any, Any] = self
        return Dictionary__get_Count(this)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: Unit = UNIT) -> bool:
        return False

    def System_Collections_Generic_ICollection_1_Remove2B595(self, item: Any = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        match_value: Any | None = erase(Dictionary__TryFind_2B595(this, item[0]))
        (pattern_matching_result,) = nullable[int]()
        if match_value is not None:
            if equals(match_value[1], item[1]):
                pattern_matching_result = 0

            else:
                pattern_matching_result = 1

        else:
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return Dictionary__Remove_2B595(this, item[0])

        else:
            return False

    def System_Collections_Generic_IDictionary_2_Add5BDDA1(self, key: KEY, value: VALUE) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__Add_5BDDA1(this, key, value)

    def System_Collections_Generic_IDictionary_2_ContainsKey2B595(self, key: KEY = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        return Dictionary__ContainsKey_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_get_Item2B595(self, key: KEY = UNIT) -> VALUE:
        this: Dictionary[Any, Any] = self
        return Dictionary__get_Item_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_set_Item5BDDA1(self, key: KEY, v: VALUE) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__set_Item_5BDDA1(this, key, v)

    def System_Collections_Generic_IDictionary_2_get_Keys(self, __unit: Unit = UNIT) -> ICollection[KEY]:
        this: Dictionary[Any, Any] = self

        def _arrow9(__unit: Unit = UNIT) -> IEnumerable_1[KEY]:
            def _arrow8(pair: Any) -> KEY:
                return pair[0]

            return map(_arrow8, this)

        return Array[Any](delay(_arrow9))

    def System_Collections_Generic_IDictionary_2_Remove2B595(self, key: KEY = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        return Dictionary__Remove_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_TryGetValue6DC89625(self, key: KEY, value: FSharpRef[VALUE]) -> bool:
        this: Dictionary[Any, Any] = self
        match_value: Any | None = erase(Dictionary__TryFind_2B595(this, key))
        if match_value is not None:
            pair: Any = match_value
            value.contents = pair[1]
            return True

        else:
            return False

    def System_Collections_Generic_IDictionary_2_get_Values(self, __unit: Unit = UNIT) -> ICollection[VALUE]:
        this: Dictionary[Any, Any] = self

        def _arrow11(__unit: Unit = UNIT) -> IEnumerable_1[VALUE]:
            def _arrow10(pair: Any) -> VALUE:
                return pair[1]

            return map(_arrow10, this)

        return Array[Any](delay(_arrow11))

    def get_item(self, key: KEY = UNIT) -> VALUE:
        this: Dictionary[Any, Any] = self
        return Dictionary__get_Item_2B595(this, key)

    def set_item(self, key: KEY, value: VALUE) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__set_Item_5BDDA1(this, key, value)

    def ContainsKey(self, key: KEY = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        return Dictionary__ContainsKey_2B595(this, key)

    @property
    def Count(self, __unit: Unit = UNIT) -> int:
        this: Dictionary[Any, Any] = self
        return Dictionary__get_Count(this)

    def Remove(self, key: KEY = UNIT) -> bool:
        this: Dictionary[Any, Any] = self
        return Dictionary__Remove_2B595(this, key)

    def Clear(self, __unit: Unit = UNIT) -> None:
        this: Dictionary[Any, Any] = self
        Dictionary__Clear(this)

    def __getitem__(self, key):
        return self.get_item(key)

    def __contains__(self, key):
        return self.ContainsKey(key)

    def __len__(self):
        return self.Count

    def __iter__(self):
        for kv in to_iterator(self.GetEnumerator()):
            yield kv[0]

    def __setitem__(self, key, value):
        self.set_item(key, value)

    def __delitem__(self, key):
        self.Remove(key)


Dictionary_reflection = _expr16


def Dictionary__ctor_6623D9B3[KEY, VALUE](
    pairs: IEnumerable_1[Any], comparer: IEqualityComparer_1[Any]
) -> Dictionary[KEY, VALUE]:
    return Dictionary(pairs, comparer)


def Dictionary__TryFindIndex_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> tuple[bool, int, int]:
    h: int = this.comparer.GetHashCode(k)
    match_value: tuple[bool, list[Any]]
    out_arg: list[Any] = cast(list[Any], None)

    def _arrow17(__unit: Unit = UNIT) -> list[Any]:
        return out_arg

    def _arrow18(v: list[Any]) -> None:
        nonlocal out_arg
        out_arg = v

    match_value = (try_get_value(this.hash_map, h, FSharpRef(_arrow17, _arrow18)), out_arg)
    if match_value[0]:

        def _arrow19(pair: Any, this: Any = this, k: Any = k) -> bool:
            return this.comparer.Equals(k, pair[0])

        return (True, h, find_index(_arrow19, match_value[1]))

    else:
        return (False, h, -1)


def Dictionary__TryFind_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> Any | None:
    match_value: tuple[bool, int, int] = Dictionary__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > -1:
            return get_item_from_dict(this.hash_map, match_value[1])[match_value[2]]

        case _:
            return None


def Dictionary__get_Comparer[KEY, VALUE](this: Dictionary[KEY, VALUE]) -> IEqualityComparer_1[Any]:
    return this.comparer


def Dictionary__Clear[KEY, VALUE](this: Dictionary[KEY, VALUE]) -> None:
    this.hash_map.clear()


def Dictionary__get_Count[KEY, VALUE](this: Dictionary[KEY, VALUE]) -> int:
    count: int = 0
    enumerator: Any = get_enumerator(to_enumerable(this.hash_map.values()))
    try:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            pairs: list[Any] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            count = tmp if (-2147483648 <= (tmp := count + len(pairs)) <= 2147483647) else int32(tmp)

    finally:
        dispose(enumerator)

    return count


def Dictionary__get_Item_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> VALUE:
    match_value: Any | None = erase(Dictionary__TryFind_2B595(this, k))
    if match_value is not None:
        return match_value[1]

    else:
        raise ExceptionBase("The item was not found in collection")


def Dictionary__set_Item_5BDDA1[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY, v: VALUE) -> None:
    match_value: tuple[bool, int, int] = Dictionary__TryFindIndex_2B595(this, k)
    if match_value[0]:
        if match_value[2] > -1:
            get_item_from_dict(this.hash_map, match_value[1])[match_value[2]] = (k, v)

        else:
            (get_item_from_dict(this.hash_map, match_value[1]).append((k, v)))
            ignore(None)

    else:
        this.hash_map[match_value[1]] = [(k, v)]


def Dictionary__Add_5BDDA1[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY, v: VALUE) -> None:
    match_value: tuple[bool, int, int] = Dictionary__TryFindIndex_2B595(this, k)
    if match_value[0]:
        if match_value[2] > -1:
            raise ArgumentException__ctor_Z721C83C5(
                format("An item with the same key has already been added. Key: {0}", k)
            )

        else:
            (get_item_from_dict(this.hash_map, match_value[1]).append((k, v)))
            ignore(None)

    else:
        this.hash_map[match_value[1]] = [(k, v)]


def Dictionary__ContainsKey_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> bool:
    match_value: tuple[bool, int, int] = Dictionary__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > -1:
            return True

        case _:
            return False


def Dictionary__Remove_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> bool:
    match_value: tuple[bool, int, int] = Dictionary__TryFindIndex_2B595(this, k)
    match match_value:
        case [True, _, i_0] if i_0 > -1:
            get_item_from_dict(this.hash_map, match_value[1]).pop(match_value[2])
            return True

        case _:
            return False


__all__ = [
    "Dictionary__Add_5BDDA1",
    "Dictionary__Clear",
    "Dictionary__ContainsKey_2B595",
    "Dictionary__Remove_2B595",
    "Dictionary__TryFindIndex_2B595",
    "Dictionary__TryFind_2B595",
    "Dictionary__get_Comparer",
    "Dictionary__get_Count",
    "Dictionary__get_Item_2B595",
    "Dictionary__set_Item_5BDDA1",
    "Dictionary_reflection",
]
