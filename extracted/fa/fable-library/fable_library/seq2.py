from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .array_ import Array
from .list import FSharpList
from .map_util import add_to_dict, add_to_set, get_item_from_dict, try_get_value
from .mutable_map import Dictionary
from .mutable_set import HashSet
from .seq import delay, filter, map, to_list
from .types import FSharpRef, int32
from .util import IEnumerable_1, IEqualityComparer_1, get_enumerator
from .util import int32 as int32_1


def distinct[T](xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> IEnumerable_1[T]:
    def _arrow46(__unit: None = None, xs: Any = xs, comparer: Any = comparer) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T | None = None) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow46)


def distinct_by[KEY, T](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow47(
        __unit: None = None, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T | None = None) -> bool:
            return add_to_set(projection(x), hash_set)

        return filter(predicate, xs)

    return delay(_arrow47)


def except_[T](
    items_to_exclude: IEnumerable_1[T], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow49(
        __unit: None = None, items_to_exclude: Any = items_to_exclude, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(items_to_exclude, comparer)

        def predicate(x: T | None = None) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow49)


def count_by[KEY, T](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, int32]]:
    def _arrow54(
        __unit: None = None, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, int32]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        keys: list[KEY] = []
        with get_enumerator(xs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                key: KEY = projection(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
                match_value: tuple[bool, int32]
                out_arg: int32 = int32.ZERO

                def _arrow51(__unit: None = None) -> int32:
                    return out_arg

                def _arrow52(v: int32) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow51, _arrow52)), out_arg)
                if match_value[int32_1(0)]:
                    dict_1[key] = match_value[int32_1(1)] + int32.ONE

                else:
                    dict_1[key] = int32.ONE
                    (keys.append(key))

        def _arrow53(key_1: KEY | None = None) -> tuple[KEY, int32]:
            return (key_1, get_item_from_dict(dict_1, key_1))

        return map(_arrow53, keys)

    return delay(_arrow54)


def group_by[KEY, T](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
    def _arrow58(
        __unit: None = None, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        keys: list[KEY] = []
        with get_enumerator(xs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x: T = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                key: KEY = projection(x)
                match_value: tuple[bool, list[T]]
                out_arg: list[T] = None

                def _arrow55(__unit: None = None) -> list[T]:
                    return out_arg

                def _arrow56(v: list[T]) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow55, _arrow56)), out_arg)
                if match_value[int32_1(0)]:
                    (match_value[int32_1(1)].append(x))

                else:
                    add_to_dict(dict_1, key, [x])
                    (keys.append(key))

        def _arrow57(key_1: KEY | None = None) -> tuple[KEY, IEnumerable_1[T]]:
            return (key_1, get_item_from_dict(dict_1, key_1))

        return map(_arrow57, keys)

    return delay(_arrow58)


def Array_distinct[T](xs: Array[T], comparer: IEqualityComparer_1[Any]) -> Array[T]:
    return Array[Any](distinct(xs, comparer))


def Array_distinctBy[KEY, T](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[T]:
    return Array[Any](distinct_by(projection, xs, comparer))


def Array_except[T](items_to_exclude: IEnumerable_1[T], xs: Array[T], comparer: IEqualityComparer_1[Any]) -> Array[T]:
    return Array[Any](except_(items_to_exclude, xs, comparer))


def Array_countBy[KEY, T](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[tuple[KEY, int32]]:
    return Array[Any](count_by(projection, xs, comparer))


def Array_groupBy[KEY, T](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[tuple[KEY, Array[T]]]:
    def mapping(
        tupled_arg: tuple[KEY, IEnumerable_1[T]], projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> tuple[KEY, Array[T]]:
        return (tupled_arg[int32_1(0)], Array[Any](tupled_arg[int32_1(1)]))

    return Array[Any](map(mapping, group_by(projection, xs, comparer)))


def List_distinct[T](xs: FSharpList[T], comparer: IEqualityComparer_1[Any]) -> FSharpList[T]:
    return to_list(distinct(xs, comparer))


def List_distinctBy[KEY, T](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[T]:
    return to_list(distinct_by(projection, xs, comparer))


def List_except[T](
    items_to_exclude: IEnumerable_1[T], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[T]:
    return to_list(except_(items_to_exclude, xs, comparer))


def List_countBy[KEY, T](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[tuple[KEY, int32]]:
    return to_list(count_by(projection, xs, comparer))


def List_groupBy[KEY, T](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[tuple[KEY, FSharpList[T]]]:
    def mapping(
        tupled_arg: tuple[KEY, IEnumerable_1[T]], projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> tuple[KEY, FSharpList[T]]:
        return (tupled_arg[int32_1(0)], to_list(tupled_arg[int32_1(1)]))

    return to_list(map(mapping, group_by(projection, xs, comparer)))


__all__ = [
    "distinct",
    "distinct_by",
    "except_",
    "count_by",
    "group_by",
    "Array_distinct",
    "Array_distinctBy",
    "Array_except",
    "Array_countBy",
    "Array_groupBy",
    "List_distinct",
    "List_distinctBy",
    "List_except",
    "List_countBy",
    "List_groupBy",
]
