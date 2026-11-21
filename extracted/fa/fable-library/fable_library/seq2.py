from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from .array_ import Array
from .core import FSharpRef, int32
from .list import FSharpList
from .map_util import add_to_dict, add_to_set, try_get_value
from .mutable_map import Dictionary
from .mutable_set import HashSet
from .protocols import IEnumerable_1, IEqualityComparer_1
from .seq import delay, to_list
from .seq_native import filter, map, map_indexed
from .util import UNIT, Disposable, Unit, get_enumerator, to_enumerable


def distinct[T](xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]) -> IEnumerable_1[T]:
    def _arrow28(__unit: Unit = UNIT, xs: Any = xs, comparer: Any = comparer) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow28)


def distinct_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow29(
        __unit: Unit = UNIT, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(Array[Any]([]), comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(projection(x), hash_set)

        return filter(predicate, xs)

    return delay(_arrow29)


def except_[T](
    items_to_exclude: IEnumerable_1[T], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[T]:
    def _arrow30(
        __unit: Unit = UNIT, items_to_exclude: Any = items_to_exclude, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[T]:
        hash_set: Any = HashSet(items_to_exclude, comparer)

        def predicate(x: T = UNIT) -> bool:
            return add_to_set(x, hash_set)

        return filter(predicate, xs)

    return delay(_arrow30)


def count_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, int]]:
    def _arrow34(
        __unit: Unit = UNIT, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, int]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        keys: list[Any] = []
        counts: list[int] = []
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                key: Any = projection(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
                match_value: tuple[bool, int]
                out_arg: int = 0

                def _arrow31(__unit: Unit = UNIT) -> int:
                    return out_arg

                def _arrow32(v: int) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow31, _arrow32)), out_arg)
                if match_value[0]:
                    index: int = match_value[1]
                    counts[index] = tmp if (-2147483648 <= (tmp := counts[index] + 1) <= 2147483647) else int32(tmp)

                else:
                    dict_1[key] = len(keys)
                    (keys.append(key))
                    (counts.append(1))

        def _arrow33(index_1: int, key_1: KEY) -> tuple[KEY, int]:
            return (key_1, counts[index_1])

        return map_indexed(_arrow33, to_enumerable(keys))

    return delay(_arrow34)


def group_by[T, KEY](
    projection: Callable[[T], KEY], xs: IEnumerable_1[T], comparer: IEqualityComparer_1[Any]
) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
    def _arrow38(
        __unit: Unit = UNIT, projection: Any = projection, xs: Any = xs, comparer: Any = comparer
    ) -> IEnumerable_1[tuple[KEY, IEnumerable_1[T]]]:
        dict_1: Any = Dictionary(Array[Any]([]), comparer)
        groups: list[tuple[Any, list[Any]]] = []
        with Disposable(get_enumerator(xs)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                key: Any = projection(x)
                match_value: tuple[bool, list[Any]]
                out_arg: list[Any] = cast(list[Any], None)

                def _arrow35(__unit: Unit = UNIT) -> list[T]:
                    return out_arg

                def _arrow36(v: list[T]) -> None:
                    nonlocal out_arg
                    out_arg = v

                match_value = (try_get_value(dict_1, key, FSharpRef(_arrow35, _arrow36)), out_arg)
                if match_value[0]:
                    (match_value[1].append(x))

                else:
                    group: list[Any] = [x]
                    add_to_dict(dict_1, key, group)
                    (groups.append((key, group)))

        def _arrow37(tupled_arg: tuple[KEY, list[T]]) -> tuple[KEY, IEnumerable_1[T]]:
            return (tupled_arg[0], to_enumerable(tupled_arg[1]))

        return map(_arrow37, to_enumerable(groups))

    return delay(_arrow38)


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
) -> Array[tuple[KEY, int]]:
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
) -> FSharpList[tuple[KEY, int]]:
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
