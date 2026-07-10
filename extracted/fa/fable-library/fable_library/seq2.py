from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from .array_ import Array
from .core import FSharpRef, int32
from .list import FSharpList
from .map_util import add_to_dict, add_to_set, get_item_from_dict, try_get_value
from .mutable_map import Dictionary
from .mutable_set import HashSet
from .protocols import IEnumerable_1, IEqualityComparer_1
from .seq import delay, to_list
from .seq_native import filter, map
from .util import UNIT, Disposable, Unit, get_enumerator, to_enumerable


def distinct[T](xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> IEnumerable_1[T]:
    def _arrow39(xs: Any = xs, comparer: Any = comparer) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow39)


def distinct_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow40(projection: Any = projection, xs: Any = xs, comparer: Any = comparer) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(projection(x), hash_set)

        return filter(predicate, xs)

    return delay(_arrow40)


def except_[T](
    items_to_exclude: IEnumerable_1[T], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow41(items_to_exclude: Any = items_to_exclude, xs: Any = xs, comparer: Any = comparer) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(items_to_exclude, comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow41)


def count_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, int32]]:
    def _arrow45(
        projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, int32]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        keys: list[Any] = []
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                key: Any = projection(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
                match_value: tuple[bool, int32]
                out_arg: int32 = int32.ZERO

                def _arrow42(__unit: Unit = UNIT) -> int32:
                    return out_arg

                def _arrow43(v: int32) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow42, _arrow43)), out_arg)
                if match_value[0]:
                    dict_1[key] = match_value[1] + int32.ONE

                else:
                    dict_1[key] = int32.ONE
                    (keys.append(key))

        def _arrow44(key_1: KEY = UNIT) -> tuple[KEY, int32]:
            return (key_1, get_item_from_dict(dict_1, key_1))

        return map(_arrow44, to_enumerable(keys))

    return delay(_arrow45)


def group_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
    def _arrow50(
        projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        keys: list[Any] = []
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                key: Any = projection(x)
                match_value: tuple[bool, list[Any]]
                out_arg: list[Any] = cast(list[Any], None)

                def _arrow47(__unit: Unit = UNIT) -> list[T]:
                    return out_arg

                def _arrow48(v: list[T]) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow47, _arrow48)), out_arg)
                if match_value[0]:
                    (match_value[1].append(x))

                else:
                    add_to_dict(dict_1, key, [x])
                    (keys.append(key))

        def _arrow49(key_1: KEY = UNIT) -> tuple[KEY, IEnumerable_1[T]]:
            return (key_1, to_enumerable(get_item_from_dict(dict_1, key_1)))

        return map(_arrow49, to_enumerable(keys))

    return delay(_arrow50)


def Array_distinct[T](xs: Array[T], comparer: IEqualityComparer_1[Any]) -> Array[T]:
    return Array[Any](distinct(xs, comparer))


def Array_distinctBy[T, KEY](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[T]:
    return Array[Any](distinct_by(projection, xs, comparer))


def Array_except[T](items_to_exclude: IEnumerable_1[T], xs: Array[T], comparer: IEqualityComparer_1[Any]) -> Array[T]:
    return Array[Any](except_(items_to_exclude, xs, comparer))


def Array_countBy[T, KEY](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[tuple[KEY, int32]]:
    return Array[Any](count_by(projection, xs, comparer))


def Array_groupBy[T, KEY](
    projection: Callable[[T], KEY], xs: Array[T], comparer: IEqualityComparer_1[Any]
) -> Array[tuple[KEY, Array[T]]]:
    def mapping(tupled_arg: tuple[KEY, IEnumerable_1[T]]) -> tuple[KEY, Array[T]]:
        return (tupled_arg[0], Array[Any](tupled_arg[1]))

    return Array[Any](map(mapping, group_by(projection, xs, comparer)))


def List_distinct[T](xs: FSharpList[T], comparer: IEqualityComparer_1[Any]) -> FSharpList[T]:
    return to_list(distinct(xs, comparer))


def List_distinctBy[T, KEY](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[T]:
    return to_list(distinct_by(projection, xs, comparer))


def List_except[T](
    items_to_exclude: IEnumerable_1[T], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[T]:
    return to_list(except_(items_to_exclude, xs, comparer))


def List_countBy[T, KEY](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[tuple[KEY, int32]]:
    return to_list(count_by(projection, xs, comparer))


def List_groupBy[T, KEY](
    projection: Callable[[T], KEY], xs: FSharpList[T], comparer: IEqualityComparer_1[Any]
) -> FSharpList[tuple[KEY, FSharpList[T]]]:
    def mapping(tupled_arg: tuple[KEY, IEnumerable_1[T]]) -> tuple[KEY, FSharpList[T]]:
        return (tupled_arg[0], to_list(tupled_arg[1]))

    return to_list(map(mapping, group_by(projection, xs, comparer)))


__all__ = [
    "Array_countBy",
    "Array_distinct",
    "Array_distinctBy",
    "Array_except",
    "Array_groupBy",
    "List_countBy",
    "List_distinct",
    "List_distinctBy",
    "List_except",
    "List_groupBy",
    "count_by",
    "distinct",
    "distinct_by",
    "except_",
    "group_by",
]
