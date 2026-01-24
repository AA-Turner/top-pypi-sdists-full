from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array
from .map_util import get_item_from_dict, try_get_value
from .native import Helpers_arrayFrom
from .reflection import TypeInfo, class_type
from .resize_array import find_index
from .seq import concat, delay, iterate, iterate_indexed, map
from .string_ import format
from .system import ArgumentException__ctor_Z721C83C5
from .types import FSharpRef
from .types import int32 as int32_1
from .util import (
    ICollection,
    IEnumerable_1,
    IEnumerator,
    IEqualityComparer_1,
    dispose,
    equals,
    get_enumerator,
    ignore,
    int32,
    to_iterator,
)


def _expr12(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Fable.Collections.Dictionary", [gen0, gen1], Dictionary)


class Dictionary[KEY, VALUE]:
    def __init__(self, pairs: IEnumerable_1[Any], comparer: IEqualityComparer_1[Any]) -> None:
        this: FSharpRef[Dictionary[KEY, VALUE]] = FSharpRef(None)
        self.comparer: IEqualityComparer_1[Any] = comparer
        this.contents = self
        self.hash_map: Any = dict(Array[Any]([]))
        self.init_00409: int32_1 = int32_1.ONE
        with get_enumerator(pairs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                pair: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                Dictionary__Add_5BDDA1(this.contents, pair[int32(0)], pair[int32(1)])

    @property
    def Symbol_toStringTag(self, __unit: None = None) -> str:
        return "Dictionary"

    def to_json(self, __unit: None = None) -> Any:
        this: Dictionary[KEY, VALUE] = self
        return Helpers_arrayFrom(this)

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None = None) -> IEnumerator[Any]:
        this: Dictionary[KEY, VALUE] = self
        return get_enumerator(this)

    def GetEnumerator[KEY, VALUE](self, __unit: None = None) -> IEnumerator[Any]:
        this: Dictionary[KEY, VALUE] = self
        return get_enumerator(concat(this.hash_map.values()))

    def __iter__[KEY, VALUE](self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_Generic_ICollection_1_Add2B595(self, item: Any) -> None:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__Add_5BDDA1(this, item[int32(0)], item[int32(1)])

    def System_Collections_Generic_ICollection_1_Clear(self, __unit: None = None) -> None:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__Clear(this)

    def System_Collections_Generic_ICollection_1_Contains2B595(self, item: Any) -> bool:
        this: Dictionary[KEY, VALUE] = self
        match_value: Any | None = Dictionary__TryFind_2B595(this, item[int32(0)])
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if equals(match_value[int32(1)], item[int32(1)]):
                pattern_matching_result = int32(0)

            else:
                pattern_matching_result = int32(1)

        else:
            pattern_matching_result = int32(1)

        if pattern_matching_result == int32_1.ZERO:
            return True

        elif pattern_matching_result == int32_1.ONE:
            return False

    def System_Collections_Generic_ICollection_1_CopyToZ3B4C077E(self, array: Array[Any], array_index: int32_1) -> None:
        this: Dictionary[KEY, VALUE] = self

        def action(i: int32_1, e: Any) -> None:
            array[array_index + i] = e

        iterate_indexed(action, this)

    def __len__(self, __unit: None = None) -> int32_1:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__get_Count(this)

    def System_Collections_Generic_ICollection_1_get_IsReadOnly(self, __unit: None = None) -> bool:
        return False

    def System_Collections_Generic_ICollection_1_Remove2B595(self, item: Any) -> bool:
        this: Dictionary[KEY, VALUE] = self
        match_value: Any | None = Dictionary__TryFind_2B595(this, item[int32(0)])
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if equals(match_value[int32(1)], item[int32(1)]):
                pattern_matching_result = int32(0)

            else:
                pattern_matching_result = int32(1)

        else:
            pattern_matching_result = int32(1)

        if pattern_matching_result == int32_1.ZERO:
            return Dictionary__Remove_2B595(this, item[int32(0)])

        elif pattern_matching_result == int32_1.ONE:
            return False

    def System_Collections_Generic_IDictionary_2_Add5BDDA1(self, key: KEY, value: VALUE) -> None:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__Add_5BDDA1(this, key, value)

    def System_Collections_Generic_IDictionary_2_ContainsKey2B595(self, key: KEY | None = None) -> bool:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__ContainsKey_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_get_Item2B595[VALUE](self, key: KEY | None = None) -> VALUE:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__get_Item_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_set_Item5BDDA1(self, key: KEY, v: VALUE) -> None:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__set_Item_5BDDA1(this, key, v)

    def System_Collections_Generic_IDictionary_2_get_Keys[KEY](self, __unit: None = None) -> ICollection[KEY]:
        this: Dictionary[KEY, VALUE] = self

        def _arrow9(__unit: None = None) -> IEnumerable_1[KEY]:
            def _arrow8(pair: Any) -> KEY:
                return pair[int32(0)]

            return map(_arrow8, this)

        return Array[Any](delay(_arrow9))

    def System_Collections_Generic_IDictionary_2_Remove2B595(self, key: KEY | None = None) -> bool:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__Remove_2B595(this, key)

    def System_Collections_Generic_IDictionary_2_TryGetValue6DC89625(self, key: KEY, value: FSharpRef[VALUE]) -> bool:
        this: Dictionary[KEY, VALUE] = self
        match_value: Any | None = Dictionary__TryFind_2B595(this, key)
        if match_value is not None:
            pair: Any = match_value
            value.contents = pair[int32(1)]
            return True

        else:
            return False

    def System_Collections_Generic_IDictionary_2_get_Values[VALUE](self, __unit: None = None) -> ICollection[VALUE]:
        this: Dictionary[KEY, VALUE] = self

        def _arrow11(__unit: None = None) -> IEnumerable_1[VALUE]:
            def _arrow10(pair: Any) -> VALUE:
                return pair[int32(1)]

            return map(_arrow10, this)

        return Array[Any](delay(_arrow11))

    @property
    def size(self, __unit: None = None) -> int32_1:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__get_Count(this)

    def clear(self, __unit: None = None) -> None:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__Clear(this)

    def __delitem__(self, k: KEY | None = None) -> bool:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__Remove_2B595(this, k)

    def entries[KEY, VALUE](self, __unit: None = None) -> IEnumerable_1[tuple[KEY, VALUE]]:
        this: Dictionary[KEY, VALUE] = self

        def mapping(p: Any) -> tuple[KEY, VALUE]:
            return (p[int32(0)], p[int32(1)])

        return map(mapping, this)

    def __getitem__[VALUE](self, k: KEY | None = None) -> VALUE:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__get_Item_2B595(this, k)

    def __contains__(self, k: KEY | None = None) -> bool:
        this: Dictionary[KEY, VALUE] = self
        return Dictionary__ContainsKey_2B595(this, k)

    def keys[KEY](self, __unit: None = None) -> IEnumerable_1[KEY]:
        this: Dictionary[KEY, VALUE] = self

        def mapping(p: Any) -> KEY:
            return p[int32(0)]

        return map(mapping, this)

    def __setitem__[KEY, VALUE](self, k: KEY, v: VALUE) -> Map_2[KEY, VALUE]:
        this: Dictionary[KEY, VALUE] = self
        Dictionary__set_Item_5BDDA1(this, k, v)
        return this

    def values[VALUE](self, __unit: None = None) -> IEnumerable_1[VALUE]:
        this: Dictionary[KEY, VALUE] = self

        def mapping(p: Any) -> VALUE:
            return p[int32(1)]

        return map(mapping, this)

    def for_each(self, f: Callable[[VALUE, KEY, Map_2[KEY, VALUE]], None], this_arg: Any | None = None) -> None:
        this: Dictionary[KEY, VALUE] = self

        def action(p: Any) -> None:
            f(p[int32(1)], p[int32(0)], this)

        iterate(action, this)


Dictionary_reflection = _expr12


def Dictionary__ctor_6623D9B3(pairs: IEnumerable_1[Any], comparer: IEqualityComparer_1[Any]) -> Dictionary[KEY, VALUE]:
    return Dictionary(pairs, comparer)


def Dictionary__TryFindIndex_2B595(this: Dictionary[KEY, Any], k: KEY) -> tuple[bool, int32_1, int32_1]:
    h: int32_1 = this.comparer.GetHashCode(k)
    match_value: tuple[bool, list[Any]]
    out_arg: list[Any] = None

    def _arrow14(__unit: None = None, this: Any = this, k: Any = k) -> list[Any]:
        return out_arg

    def _arrow15(v: list[Any], this: Any = this, k: Any = k) -> None:
        nonlocal out_arg
        out_arg = v

    match_value = (try_get_value(this.hash_map, h, FSharpRef(_arrow14, _arrow15)), out_arg)
    if match_value[int32(0)]:

        def _arrow18(pair: Any, this: Any = this, k: Any = k) -> bool:
            return this.comparer.Equals(k, pair[int32(0)])

        return (True, h, find_index(_arrow18, match_value[int32(1)]))

    else:
        return (False, h, int32_1.NEG_ONE)


def Dictionary__TryFind_2B595[KEY, VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> Any | None:
    match_value: tuple[bool, int32_1, int32_1] = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32(0)]:
        if match_value[int32(2)] > int32_1.NEG_ONE:
            pattern_matching_result = int32(0)

        else:
            pattern_matching_result = int32(1)

    else:
        pattern_matching_result = int32(1)

    if pattern_matching_result == int32_1.ZERO:
        return get_item_from_dict(this.hash_map, match_value[int32(1)])[match_value[int32(2)]]

    elif pattern_matching_result == int32_1.ONE:
        return None


def Dictionary__get_Comparer[KEY](this: Dictionary[KEY, Any]) -> IEqualityComparer_1[Any]:
    return this.comparer


def Dictionary__Clear(this: Dictionary[Any, Any]) -> None:
    this.hash_map.clear()


def Dictionary__get_Count(this: Dictionary[Any, Any]) -> int32_1:
    count: int32_1 = int32_1.ZERO
    enumerator: Any = get_enumerator(this.hash_map.values())
    try:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            pairs: list[Any] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            count = count + len(pairs)

    finally:
        dispose(enumerator)

    return count


def Dictionary__get_Item_2B595[VALUE](this: Dictionary[KEY, VALUE], k: KEY) -> VALUE:
    match_value: Any | None = Dictionary__TryFind_2B595(this, k)
    if match_value is not None:
        return match_value[int32(1)]

    else:
        raise Exception("The item was not found in collection")


def Dictionary__set_Item_5BDDA1(this: Dictionary[KEY, VALUE], k: KEY, v: VALUE) -> None:
    match_value: tuple[bool, int32_1, int32_1] = Dictionary__TryFindIndex_2B595(this, k)
    if match_value[int32(0)]:
        if match_value[int32(2)] > int32_1.NEG_ONE:
            get_item_from_dict(this.hash_map, match_value[int32(1)])[match_value[int32(2)]] = (k, v)

        else:
            value: None = get_item_from_dict(this.hash_map, match_value[int32(1)]).append((k, v))
            ignore(None)

    else:
        this.hash_map[match_value[int32(1)]] = [(k, v)]


def Dictionary__Add_5BDDA1(this: Dictionary[KEY, VALUE], k: KEY, v: VALUE) -> None:
    match_value: tuple[bool, int32_1, int32_1] = Dictionary__TryFindIndex_2B595(this, k)
    if match_value[int32(0)]:
        if match_value[int32(2)] > int32_1.NEG_ONE:
            raise ArgumentException__ctor_Z721C83C5(
                format("An item with the same key has already been added. Key: {0}", k)
            )

        else:
            value: None = get_item_from_dict(this.hash_map, match_value[int32(1)]).append((k, v))
            ignore(None)

    else:
        this.hash_map[match_value[int32(1)]] = [(k, v)]


def Dictionary__ContainsKey_2B595(this: Dictionary[KEY, Any], k: KEY) -> bool:
    match_value: tuple[bool, int32_1, int32_1] = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32(0)]:
        if match_value[int32(2)] > int32_1.NEG_ONE:
            pattern_matching_result = int32(0)

        else:
            pattern_matching_result = int32(1)

    else:
        pattern_matching_result = int32(1)

    if pattern_matching_result == int32_1.ZERO:
        return True

    elif pattern_matching_result == int32_1.ONE:
        return False


def Dictionary__Remove_2B595(this: Dictionary[KEY, Any], k: KEY) -> bool:
    match_value: tuple[bool, int32_1, int32_1] = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[int32(0)]:
        if match_value[int32(2)] > int32_1.NEG_ONE:
            pattern_matching_result = int32(0)

        else:
            pattern_matching_result = int32(1)

    else:
        pattern_matching_result = int32(1)

    if pattern_matching_result == int32_1.ZERO:
        get_item_from_dict(this.hash_map, match_value[int32(1)]).pop(match_value[int32(2)])
        return True

    elif pattern_matching_result == int32_1.ONE:
        return False


__all__ = [
    "Dictionary_reflection",
    "Dictionary__TryFindIndex_2B595",
    "Dictionary__TryFind_2B595",
    "Dictionary__get_Comparer",
    "Dictionary__Clear",
    "Dictionary__get_Count",
    "Dictionary__get_Item_2B595",
    "Dictionary__set_Item_5BDDA1",
    "Dictionary__Add_5BDDA1",
    "Dictionary__ContainsKey_2B595",
    "Dictionary__Remove_2B595",
]
