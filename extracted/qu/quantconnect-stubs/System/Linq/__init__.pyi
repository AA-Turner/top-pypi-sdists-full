from typing import overload
from enum import IntEnum
import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.Immutable
import System.Linq

System_Linq_Lookup_TKey = typing.TypeVar("System_Linq_Lookup_TKey")
System_Linq_Lookup_TElement = typing.TypeVar("System_Linq_Lookup_TElement")
System_Linq_IOrderedEnumerable_TElement = typing.TypeVar("System_Linq_IOrderedEnumerable_TElement")
System_Linq_IGrouping_TKey = typing.TypeVar("System_Linq_IGrouping_TKey")
System_Linq_IGrouping_TElement = typing.TypeVar("System_Linq_IGrouping_TElement")
System_Linq_ILookup_TKey = typing.TypeVar("System_Linq_ILookup_TKey")
System_Linq_ILookup_TElement = typing.TypeVar("System_Linq_ILookup_TElement")
System_Linq_ImmutableArrayExtensions_Select_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Select_T")
System_Linq_ImmutableArrayExtensions_Select_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Select_TResult")
System_Linq_ImmutableArrayExtensions_SelectMany_TSource = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TSource")
System_Linq_ImmutableArrayExtensions_SelectMany_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TResult")
System_Linq_ImmutableArrayExtensions_SelectMany_TCollection = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TCollection")
System_Linq_ImmutableArrayExtensions_Where_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Where_T")
System_Linq_ImmutableArrayExtensions_Any_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Any_T")
System_Linq_ImmutableArrayExtensions_All_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_All_T")
System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived")
System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase")
System_Linq_ImmutableArrayExtensions_Aggregate_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_T")
System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate")
System_Linq_ImmutableArrayExtensions_Aggregate_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_TResult")
System_Linq_ImmutableArrayExtensions_ElementAt_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ElementAt_T")
System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T")
System_Linq_ImmutableArrayExtensions_First_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_First_T")
System_Linq_ImmutableArrayExtensions_FirstOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_FirstOrDefault_T")
System_Linq_ImmutableArrayExtensions_Last_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Last_T")
System_Linq_ImmutableArrayExtensions_LastOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_LastOrDefault_T")
System_Linq_ImmutableArrayExtensions_Single_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Single_T")
System_Linq_ImmutableArrayExtensions_SingleOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SingleOrDefault_T")
System_Linq_ImmutableArrayExtensions_ToDictionary_TKey = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_TKey")
System_Linq_ImmutableArrayExtensions_ToDictionary_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_T")
System_Linq_ImmutableArrayExtensions_ToDictionary_TElement = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_TElement")
System_Linq_ImmutableArrayExtensions_ToArray_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToArray_T")
System_Linq_Enumerable_Append_TSource = typing.TypeVar("System_Linq_Enumerable_Append_TSource")
System_Linq_Enumerable_Prepend_TSource = typing.TypeVar("System_Linq_Enumerable_Prepend_TSource")
System_Linq_Enumerable_Skip_TSource = typing.TypeVar("System_Linq_Enumerable_Skip_TSource")
System_Linq_Enumerable_SkipWhile_TSource = typing.TypeVar("System_Linq_Enumerable_SkipWhile_TSource")
System_Linq_Enumerable_SkipLast_TSource = typing.TypeVar("System_Linq_Enumerable_SkipLast_TSource")
System_Linq_Enumerable_Order_T = typing.TypeVar("System_Linq_Enumerable_Order_T")
System_Linq_Enumerable_OrderBy_TSource = typing.TypeVar("System_Linq_Enumerable_OrderBy_TSource")
System_Linq_Enumerable_OrderBy_TKey = typing.TypeVar("System_Linq_Enumerable_OrderBy_TKey")
System_Linq_Enumerable_OrderDescending_T = typing.TypeVar("System_Linq_Enumerable_OrderDescending_T")
System_Linq_Enumerable_OrderByDescending_TSource = typing.TypeVar("System_Linq_Enumerable_OrderByDescending_TSource")
System_Linq_Enumerable_OrderByDescending_TKey = typing.TypeVar("System_Linq_Enumerable_OrderByDescending_TKey")
System_Linq_Enumerable_ThenBy_TSource = typing.TypeVar("System_Linq_Enumerable_ThenBy_TSource")
System_Linq_Enumerable_ThenBy_TKey = typing.TypeVar("System_Linq_Enumerable_ThenBy_TKey")
System_Linq_Enumerable_ThenByDescending_TSource = typing.TypeVar("System_Linq_Enumerable_ThenByDescending_TSource")
System_Linq_Enumerable_ThenByDescending_TKey = typing.TypeVar("System_Linq_Enumerable_ThenByDescending_TKey")
System_Linq_Enumerable_Sum_TSource = typing.TypeVar("System_Linq_Enumerable_Sum_TSource")
System_Linq_Enumerable_Index_TSource = typing.TypeVar("System_Linq_Enumerable_Index_TSource")
System_Linq_Enumerable_Chunk_TSource = typing.TypeVar("System_Linq_Enumerable_Chunk_TSource")
System_Linq_Enumerable_Sequence_T = typing.TypeVar("System_Linq_Enumerable_Sequence_T")
System_Linq_Enumerable_AsEnumerable_TSource = typing.TypeVar("System_Linq_Enumerable_AsEnumerable_TSource")
System_Linq_Enumerable_Empty_TResult = typing.TypeVar("System_Linq_Enumerable_Empty_TResult")
System_Linq_Enumerable_First_TSource = typing.TypeVar("System_Linq_Enumerable_First_TSource")
System_Linq_Enumerable_FirstOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_FirstOrDefault_TSource")
System_Linq_Enumerable_Select_TSource = typing.TypeVar("System_Linq_Enumerable_Select_TSource")
System_Linq_Enumerable_Select_TResult = typing.TypeVar("System_Linq_Enumerable_Select_TResult")
System_Linq_Enumerable_Count_TSource = typing.TypeVar("System_Linq_Enumerable_Count_TSource")
System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource = typing.TypeVar("System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource")
System_Linq_Enumerable_LongCount_TSource = typing.TypeVar("System_Linq_Enumerable_LongCount_TSource")
System_Linq_Enumerable_Zip_TFirst = typing.TypeVar("System_Linq_Enumerable_Zip_TFirst")
System_Linq_Enumerable_Zip_TResult = typing.TypeVar("System_Linq_Enumerable_Zip_TResult")
System_Linq_Enumerable_Zip_TSecond = typing.TypeVar("System_Linq_Enumerable_Zip_TSecond")
System_Linq_Enumerable_Zip_TThird = typing.TypeVar("System_Linq_Enumerable_Zip_TThird")
System_Linq_Enumerable_Join_TOuter = typing.TypeVar("System_Linq_Enumerable_Join_TOuter")
System_Linq_Enumerable_Join_TResult = typing.TypeVar("System_Linq_Enumerable_Join_TResult")
System_Linq_Enumerable_Join_TInner = typing.TypeVar("System_Linq_Enumerable_Join_TInner")
System_Linq_Enumerable_Join_TKey = typing.TypeVar("System_Linq_Enumerable_Join_TKey")
System_Linq_Enumerable_InfiniteSequence_T = typing.TypeVar("System_Linq_Enumerable_InfiniteSequence_T")
System_Linq_Enumerable_GroupBy_TSource = typing.TypeVar("System_Linq_Enumerable_GroupBy_TSource")
System_Linq_Enumerable_GroupBy_TKey = typing.TypeVar("System_Linq_Enumerable_GroupBy_TKey")
System_Linq_Enumerable_GroupBy_TElement = typing.TypeVar("System_Linq_Enumerable_GroupBy_TElement")
System_Linq_Enumerable_GroupBy_TResult = typing.TypeVar("System_Linq_Enumerable_GroupBy_TResult")
System_Linq_Enumerable_Contains_TSource = typing.TypeVar("System_Linq_Enumerable_Contains_TSource")
System_Linq_Enumerable_Union_TSource = typing.TypeVar("System_Linq_Enumerable_Union_TSource")
System_Linq_Enumerable_UnionBy_TSource = typing.TypeVar("System_Linq_Enumerable_UnionBy_TSource")
System_Linq_Enumerable_UnionBy_TKey = typing.TypeVar("System_Linq_Enumerable_UnionBy_TKey")
System_Linq_Enumerable_Any_TSource = typing.TypeVar("System_Linq_Enumerable_Any_TSource")
System_Linq_Enumerable_All_TSource = typing.TypeVar("System_Linq_Enumerable_All_TSource")
System_Linq_Enumerable_SelectMany_TSource = typing.TypeVar("System_Linq_Enumerable_SelectMany_TSource")
System_Linq_Enumerable_SelectMany_TResult = typing.TypeVar("System_Linq_Enumerable_SelectMany_TResult")
System_Linq_Enumerable_SelectMany_TCollection = typing.TypeVar("System_Linq_Enumerable_SelectMany_TCollection")
System_Linq_Enumerable_Distinct_TSource = typing.TypeVar("System_Linq_Enumerable_Distinct_TSource")
System_Linq_Enumerable_DistinctBy_TSource = typing.TypeVar("System_Linq_Enumerable_DistinctBy_TSource")
System_Linq_Enumerable_DistinctBy_TKey = typing.TypeVar("System_Linq_Enumerable_DistinctBy_TKey")
System_Linq_Enumerable_ToArray_TSource = typing.TypeVar("System_Linq_Enumerable_ToArray_TSource")
System_Linq_Enumerable_ToList_TSource = typing.TypeVar("System_Linq_Enumerable_ToList_TSource")
System_Linq_Enumerable_ToDictionary_TKey = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TKey")
System_Linq_Enumerable_ToDictionary_TValue = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TValue")
System_Linq_Enumerable_ToDictionary_TSource = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TSource")
System_Linq_Enumerable_ToDictionary_TElement = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TElement")
System_Linq_Enumerable_ToHashSet_TSource = typing.TypeVar("System_Linq_Enumerable_ToHashSet_TSource")
System_Linq_Enumerable_LeftJoin_TOuter = typing.TypeVar("System_Linq_Enumerable_LeftJoin_TOuter")
System_Linq_Enumerable_LeftJoin_TResult = typing.TypeVar("System_Linq_Enumerable_LeftJoin_TResult")
System_Linq_Enumerable_LeftJoin_TInner = typing.TypeVar("System_Linq_Enumerable_LeftJoin_TInner")
System_Linq_Enumerable_LeftJoin_TKey = typing.TypeVar("System_Linq_Enumerable_LeftJoin_TKey")
System_Linq_Enumerable_SequenceEqual_TSource = typing.TypeVar("System_Linq_Enumerable_SequenceEqual_TSource")
System_Linq_Enumerable_Take_TSource = typing.TypeVar("System_Linq_Enumerable_Take_TSource")
System_Linq_Enumerable_TakeWhile_TSource = typing.TypeVar("System_Linq_Enumerable_TakeWhile_TSource")
System_Linq_Enumerable_TakeLast_TSource = typing.TypeVar("System_Linq_Enumerable_TakeLast_TSource")
System_Linq_Enumerable_ToLookup_TSource = typing.TypeVar("System_Linq_Enumerable_ToLookup_TSource")
System_Linq_Enumerable_ToLookup_TKey = typing.TypeVar("System_Linq_Enumerable_ToLookup_TKey")
System_Linq_Enumerable_ToLookup_TElement = typing.TypeVar("System_Linq_Enumerable_ToLookup_TElement")
System_Linq_Enumerable_Concat_TSource = typing.TypeVar("System_Linq_Enumerable_Concat_TSource")
System_Linq_Enumerable_CountBy_TSource = typing.TypeVar("System_Linq_Enumerable_CountBy_TSource")
System_Linq_Enumerable_CountBy_TKey = typing.TypeVar("System_Linq_Enumerable_CountBy_TKey")
System_Linq_Enumerable_AggregateBy_TSource = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TSource")
System_Linq_Enumerable_AggregateBy_TAccumulate = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TAccumulate")
System_Linq_Enumerable_AggregateBy_TKey = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TKey")
System_Linq_Enumerable_ElementAt_TSource = typing.TypeVar("System_Linq_Enumerable_ElementAt_TSource")
System_Linq_Enumerable_ElementAtOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_ElementAtOrDefault_TSource")
System_Linq_Enumerable_Cast_TResult = typing.TypeVar("System_Linq_Enumerable_Cast_TResult")
System_Linq_Enumerable_Max_TSource = typing.TypeVar("System_Linq_Enumerable_Max_TSource")
System_Linq_Enumerable_Max_TResult = typing.TypeVar("System_Linq_Enumerable_Max_TResult")
System_Linq_Enumerable_MaxBy_TSource = typing.TypeVar("System_Linq_Enumerable_MaxBy_TSource")
System_Linq_Enumerable_MaxBy_TKey = typing.TypeVar("System_Linq_Enumerable_MaxBy_TKey")
System_Linq_Enumerable_Where_TSource = typing.TypeVar("System_Linq_Enumerable_Where_TSource")
System_Linq_Enumerable_Reverse_TSource = typing.TypeVar("System_Linq_Enumerable_Reverse_TSource")
System_Linq_Enumerable_Last_TSource = typing.TypeVar("System_Linq_Enumerable_Last_TSource")
System_Linq_Enumerable_LastOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_LastOrDefault_TSource")
System_Linq_Enumerable_Intersect_TSource = typing.TypeVar("System_Linq_Enumerable_Intersect_TSource")
System_Linq_Enumerable_IntersectBy_TSource = typing.TypeVar("System_Linq_Enumerable_IntersectBy_TSource")
System_Linq_Enumerable_IntersectBy_TKey = typing.TypeVar("System_Linq_Enumerable_IntersectBy_TKey")
System_Linq_Enumerable_Repeat_TResult = typing.TypeVar("System_Linq_Enumerable_Repeat_TResult")
System_Linq_Enumerable_RightJoin_TOuter = typing.TypeVar("System_Linq_Enumerable_RightJoin_TOuter")
System_Linq_Enumerable_RightJoin_TResult = typing.TypeVar("System_Linq_Enumerable_RightJoin_TResult")
System_Linq_Enumerable_RightJoin_TInner = typing.TypeVar("System_Linq_Enumerable_RightJoin_TInner")
System_Linq_Enumerable_RightJoin_TKey = typing.TypeVar("System_Linq_Enumerable_RightJoin_TKey")
System_Linq_Enumerable_Shuffle_TSource = typing.TypeVar("System_Linq_Enumerable_Shuffle_TSource")
System_Linq_Enumerable_FullJoin_TOuter = typing.TypeVar("System_Linq_Enumerable_FullJoin_TOuter")
System_Linq_Enumerable_FullJoin_TResult = typing.TypeVar("System_Linq_Enumerable_FullJoin_TResult")
System_Linq_Enumerable_FullJoin_TInner = typing.TypeVar("System_Linq_Enumerable_FullJoin_TInner")
System_Linq_Enumerable_FullJoin_TKey = typing.TypeVar("System_Linq_Enumerable_FullJoin_TKey")
System_Linq_Enumerable_Aggregate_TSource = typing.TypeVar("System_Linq_Enumerable_Aggregate_TSource")
System_Linq_Enumerable_Aggregate_TAccumulate = typing.TypeVar("System_Linq_Enumerable_Aggregate_TAccumulate")
System_Linq_Enumerable_Aggregate_TResult = typing.TypeVar("System_Linq_Enumerable_Aggregate_TResult")
System_Linq_Enumerable_OfType_TResult = typing.TypeVar("System_Linq_Enumerable_OfType_TResult")
System_Linq_Enumerable_Except_TSource = typing.TypeVar("System_Linq_Enumerable_Except_TSource")
System_Linq_Enumerable_ExceptBy_TSource = typing.TypeVar("System_Linq_Enumerable_ExceptBy_TSource")
System_Linq_Enumerable_ExceptBy_TKey = typing.TypeVar("System_Linq_Enumerable_ExceptBy_TKey")
System_Linq_Enumerable_Average_TSource = typing.TypeVar("System_Linq_Enumerable_Average_TSource")
System_Linq_Enumerable_Min_TSource = typing.TypeVar("System_Linq_Enumerable_Min_TSource")
System_Linq_Enumerable_Min_TResult = typing.TypeVar("System_Linq_Enumerable_Min_TResult")
System_Linq_Enumerable_MinBy_TSource = typing.TypeVar("System_Linq_Enumerable_MinBy_TSource")
System_Linq_Enumerable_MinBy_TKey = typing.TypeVar("System_Linq_Enumerable_MinBy_TKey")
System_Linq_Enumerable_Single_TSource = typing.TypeVar("System_Linq_Enumerable_Single_TSource")
System_Linq_Enumerable_SingleOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_SingleOrDefault_TSource")
System_Linq_Enumerable_GroupJoin_TOuter = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TOuter")
System_Linq_Enumerable_GroupJoin_TInner = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TInner")
System_Linq_Enumerable_GroupJoin_TKey = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TKey")
System_Linq_Enumerable_GroupJoin_TResult = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TResult")
System_Linq_Enumerable_DefaultIfEmpty_TSource = typing.TypeVar("System_Linq_Enumerable_DefaultIfEmpty_TSource")
System_Linq_Lookup_ApplyResultSelector_TResult = typing.TypeVar("System_Linq_Lookup_ApplyResultSelector_TResult")
System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey = typing.TypeVar("System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey")


class _Typed_ImmutableArrayExtensions_Select(typing.Generic[System_Linq_ImmutableArrayExtensions_Select_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Select_T], selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_Select_T], System_Linq_ImmutableArrayExtensions_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_Select_TResult]:
        ...


class _ImmutableArrayExtensions_Select:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Select_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Select[System_Linq_ImmutableArrayExtensions_Select_T]:
        ...


class _Typed_ImmutableArrayExtensions_SelectMany(typing.Generic[System_Linq_ImmutableArrayExtensions_SelectMany_TSource]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_SelectMany_TSource], typing.List[System_Linq_ImmutableArrayExtensions_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_SelectMany_TSource, System_Linq_ImmutableArrayExtensions_SelectMany_TCollection], System_Linq_ImmutableArrayExtensions_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_SelectMany_TResult]:
        ...


class _ImmutableArrayExtensions_SelectMany:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_SelectMany_TSource]) -> System.Linq._Typed_ImmutableArrayExtensions_SelectMany[System_Linq_ImmutableArrayExtensions_SelectMany_TSource]:
        ...


class _Typed_ImmutableArrayExtensions_Where(typing.Generic[System_Linq_ImmutableArrayExtensions_Where_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Where_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Where_T], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_Where_T]:
        ...


class _ImmutableArrayExtensions_Where:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Where_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Where[System_Linq_ImmutableArrayExtensions_Where_T]:
        ...


class _Typed_ImmutableArrayExtensions_Any(typing.Generic[System_Linq_ImmutableArrayExtensions_Any_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Any_T]) -> bool:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Any_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Any_T], bool]) -> bool:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> bool:
        ...


class _ImmutableArrayExtensions_Any:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Any_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Any[System_Linq_ImmutableArrayExtensions_Any_T]:
        ...


class _Typed_ImmutableArrayExtensions_All(typing.Generic[System_Linq_ImmutableArrayExtensions_All_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_All_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_All_T], bool]) -> bool:
        ...


class _ImmutableArrayExtensions_All:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_All_T]) -> System.Linq._Typed_ImmutableArrayExtensions_All[System_Linq_ImmutableArrayExtensions_All_T]:
        ...


class _Typed_ImmutableArrayExtensions_SequenceEqual(typing.Generic[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase] = None) -> bool:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase] = None) -> bool:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase, System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], bool]) -> bool:
        ...


class _ImmutableArrayExtensions_SequenceEqual:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived]) -> System.Linq._Typed_ImmutableArrayExtensions_SequenceEqual[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived]:
        ...


class _Typed_ImmutableArrayExtensions_Aggregate(typing.Generic[System_Linq_ImmutableArrayExtensions_Aggregate_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_T, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_T]) -> System_Linq_ImmutableArrayExtensions_Aggregate_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], seed: System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate]) -> System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], seed: System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate], result_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate], System_Linq_ImmutableArrayExtensions_Aggregate_TResult]) -> System_Linq_ImmutableArrayExtensions_Aggregate_TResult:
        ...


class _ImmutableArrayExtensions_Aggregate:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Aggregate_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Aggregate[System_Linq_ImmutableArrayExtensions_Aggregate_T]:
        ...


class _Typed_ImmutableArrayExtensions_ElementAt(typing.Generic[System_Linq_ImmutableArrayExtensions_ElementAt_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ElementAt_T], index: int) -> System_Linq_ImmutableArrayExtensions_ElementAt_T:
        ...


class _ImmutableArrayExtensions_ElementAt:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_ElementAt_T]) -> System.Linq._Typed_ImmutableArrayExtensions_ElementAt[System_Linq_ImmutableArrayExtensions_ElementAt_T]:
        ...


class _Typed_ImmutableArrayExtensions_ElementAtOrDefault(typing.Generic[System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T], index: int) -> System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T:
        ...


class _ImmutableArrayExtensions_ElementAtOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T]) -> System.Linq._Typed_ImmutableArrayExtensions_ElementAtOrDefault[System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T]:
        ...


class _Typed_ImmutableArrayExtensions_First(typing.Generic[System_Linq_ImmutableArrayExtensions_First_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_First_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_First_T], bool]) -> System_Linq_ImmutableArrayExtensions_First_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_First_T]) -> System_Linq_ImmutableArrayExtensions_First_T:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_First_T:
        ...


class _ImmutableArrayExtensions_First:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_First_T]) -> System.Linq._Typed_ImmutableArrayExtensions_First[System_Linq_ImmutableArrayExtensions_First_T]:
        ...


class _Typed_ImmutableArrayExtensions_FirstOrDefault(typing.Generic[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        ...


class _ImmutableArrayExtensions_FirstOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T]) -> System.Linq._Typed_ImmutableArrayExtensions_FirstOrDefault[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T]:
        ...


class _Typed_ImmutableArrayExtensions_Last(typing.Generic[System_Linq_ImmutableArrayExtensions_Last_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Last_T]) -> System_Linq_ImmutableArrayExtensions_Last_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Last_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Last_T], bool]) -> System_Linq_ImmutableArrayExtensions_Last_T:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_Last_T:
        ...


class _ImmutableArrayExtensions_Last:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Last_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Last[System_Linq_ImmutableArrayExtensions_Last_T]:
        ...


class _Typed_ImmutableArrayExtensions_LastOrDefault(typing.Generic[System_Linq_ImmutableArrayExtensions_LastOrDefault_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_LastOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_LastOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_LastOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        ...


class _ImmutableArrayExtensions_LastOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_LastOrDefault_T]) -> System.Linq._Typed_ImmutableArrayExtensions_LastOrDefault[System_Linq_ImmutableArrayExtensions_LastOrDefault_T]:
        ...


class _Typed_ImmutableArrayExtensions_Single(typing.Generic[System_Linq_ImmutableArrayExtensions_Single_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Single_T]) -> System_Linq_ImmutableArrayExtensions_Single_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Single_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Single_T], bool]) -> System_Linq_ImmutableArrayExtensions_Single_T:
        ...


class _ImmutableArrayExtensions_Single:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_Single_T]) -> System.Linq._Typed_ImmutableArrayExtensions_Single[System_Linq_ImmutableArrayExtensions_Single_T]:
        ...


class _Typed_ImmutableArrayExtensions_SingleOrDefault(typing.Generic[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_SingleOrDefault_T:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_SingleOrDefault_T:
        ...


class _ImmutableArrayExtensions_SingleOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T]) -> System.Linq._Typed_ImmutableArrayExtensions_SingleOrDefault[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T]:
        ...


class _Typed_ImmutableArrayExtensions_ToDictionary(typing.Generic[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_T]:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_T]:
        ...

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]:
        ...


class _ImmutableArrayExtensions_ToDictionary:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Linq._Typed_ImmutableArrayExtensions_ToDictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]:
        ...


class _Typed_ImmutableArrayExtensions_ToArray(typing.Generic[System_Linq_ImmutableArrayExtensions_ToArray_T]):
    """"""

    @overload
    def __call__(self, immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToArray_T]) -> typing.List[System_Linq_ImmutableArrayExtensions_ToArray_T]:
        ...


class _ImmutableArrayExtensions_ToArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_ImmutableArrayExtensions_ToArray_T]) -> System.Linq._Typed_ImmutableArrayExtensions_ToArray[System_Linq_ImmutableArrayExtensions_ToArray_T]:
        ...


class ImmutableArrayExtensions(System.Object):
    """This class has no documentation."""

    select: System.Linq._ImmutableArrayExtensions_Select

    select_many: System.Linq._ImmutableArrayExtensions_SelectMany

    where: System.Linq._ImmutableArrayExtensions_Where

    any: System.Linq._ImmutableArrayExtensions_Any

    all: System.Linq._ImmutableArrayExtensions_All

    sequence_equal: System.Linq._ImmutableArrayExtensions_SequenceEqual

    aggregate: System.Linq._ImmutableArrayExtensions_Aggregate

    element_at: System.Linq._ImmutableArrayExtensions_ElementAt

    element_at_or_default: System.Linq._ImmutableArrayExtensions_ElementAtOrDefault

    first: System.Linq._ImmutableArrayExtensions_First

    first_or_default: System.Linq._ImmutableArrayExtensions_FirstOrDefault

    last: System.Linq._ImmutableArrayExtensions_Last

    last_or_default: System.Linq._ImmutableArrayExtensions_LastOrDefault

    single: System.Linq._ImmutableArrayExtensions_Single

    single_or_default: System.Linq._ImmutableArrayExtensions_SingleOrDefault

    to_dictionary: System.Linq._ImmutableArrayExtensions_ToDictionary

    to_array: System.Linq._ImmutableArrayExtensions_ToArray


class _Typed_Enumerable_Append(typing.Generic[System_Linq_Enumerable_Append_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Append_TSource], element: System_Linq_Enumerable_Append_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Append_TSource]:
        ...


class _Enumerable_Append:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Append_TSource]) -> System.Linq._Typed_Enumerable_Append[System_Linq_Enumerable_Append_TSource]:
        ...


class _Typed_Enumerable_Prepend(typing.Generic[System_Linq_Enumerable_Prepend_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Prepend_TSource], element: System_Linq_Enumerable_Prepend_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Prepend_TSource]:
        ...


class _Enumerable_Prepend:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Prepend_TSource]) -> System.Linq._Typed_Enumerable_Prepend[System_Linq_Enumerable_Prepend_TSource]:
        ...


class _Typed_Enumerable_Skip(typing.Generic[System_Linq_Enumerable_Skip_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Skip_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Skip_TSource]:
        ...


class _Enumerable_Skip:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Skip_TSource]) -> System.Linq._Typed_Enumerable_Skip[System_Linq_Enumerable_Skip_TSource]:
        ...


class _Typed_Enumerable_SkipWhile(typing.Generic[System_Linq_Enumerable_SkipWhile_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SkipWhile_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SkipWhile_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource]:
        ...


class _Enumerable_SkipWhile:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_SkipWhile_TSource]) -> System.Linq._Typed_Enumerable_SkipWhile[System_Linq_Enumerable_SkipWhile_TSource]:
        ...


class _Typed_Enumerable_SkipLast(typing.Generic[System_Linq_Enumerable_SkipLast_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipLast_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipLast_TSource]:
        ...


class _Enumerable_SkipLast:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_SkipLast_TSource]) -> System.Linq._Typed_Enumerable_SkipLast[System_Linq_Enumerable_SkipLast_TSource]:
        ...


class _Typed_Enumerable_Order(typing.Generic[System_Linq_Enumerable_Order_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Order_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_Order_T]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Order_T], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Order_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_Order_T]:
        ...


class _Enumerable_Order:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Order_T]) -> System.Linq._Typed_Enumerable_Order[System_Linq_Enumerable_Order_T]:
        ...


class _Typed_Enumerable_OrderBy(typing.Generic[System_Linq_Enumerable_OrderBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderBy_TSource], System_Linq_Enumerable_OrderBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderBy_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderBy_TSource], System_Linq_Enumerable_OrderBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderBy_TSource]:
        ...


class _Enumerable_OrderBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_OrderBy_TSource]) -> System.Linq._Typed_Enumerable_OrderBy[System_Linq_Enumerable_OrderBy_TSource]:
        ...


class _Typed_Enumerable_OrderDescending(typing.Generic[System_Linq_Enumerable_OrderDescending_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderDescending_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderDescending_T]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderDescending_T], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderDescending_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderDescending_T]:
        ...


class _Enumerable_OrderDescending:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_OrderDescending_T]) -> System.Linq._Typed_Enumerable_OrderDescending[System_Linq_Enumerable_OrderDescending_T]:
        ...


class _Typed_Enumerable_OrderByDescending(typing.Generic[System_Linq_Enumerable_OrderByDescending_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderByDescending_TSource], System_Linq_Enumerable_OrderByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderByDescending_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderByDescending_TSource], System_Linq_Enumerable_OrderByDescending_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderByDescending_TSource]:
        ...


class _Enumerable_OrderByDescending:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_OrderByDescending_TSource]) -> System.Linq._Typed_Enumerable_OrderByDescending[System_Linq_Enumerable_OrderByDescending_TSource]:
        ...


class _Typed_Enumerable_ThenBy(typing.Generic[System_Linq_Enumerable_ThenBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenBy_TSource], System_Linq_Enumerable_ThenBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource]:
        ...

    @overload
    def __call__(self, source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenBy_TSource], System_Linq_Enumerable_ThenBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_ThenBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource]:
        ...


class _Enumerable_ThenBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ThenBy_TSource]) -> System.Linq._Typed_Enumerable_ThenBy[System_Linq_Enumerable_ThenBy_TSource]:
        ...


class _Typed_Enumerable_ThenByDescending(typing.Generic[System_Linq_Enumerable_ThenByDescending_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenByDescending_TSource], System_Linq_Enumerable_ThenByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource]:
        ...

    @overload
    def __call__(self, source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenByDescending_TSource], System_Linq_Enumerable_ThenByDescending_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_ThenByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource]:
        ...


class _Enumerable_ThenByDescending:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ThenByDescending_TSource]) -> System.Linq._Typed_Enumerable_ThenByDescending[System_Linq_Enumerable_ThenByDescending_TSource]:
        ...


class _Typed_Enumerable_Sum(typing.Generic[System_Linq_Enumerable_Sum_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...


class _Enumerable_Sum:
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Sum_TSource]) -> System.Linq._Typed_Enumerable_Sum[System_Linq_Enumerable_Sum_TSource]:
        ...


class _Typed_Enumerable_Index(typing.Generic[System_Linq_Enumerable_Index_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Index_TSource]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[int, System_Linq_Enumerable_Index_TSource]]:
        ...


class _Enumerable_Index:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Index_TSource]) -> System.Linq._Typed_Enumerable_Index[System_Linq_Enumerable_Index_TSource]:
        ...


class _Typed_Enumerable_Chunk(typing.Generic[System_Linq_Enumerable_Chunk_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Chunk_TSource], size: int) -> System.Collections.Generic.IEnumerable[typing.List[System_Linq_Enumerable_Chunk_TSource]]:
        ...


class _Enumerable_Chunk:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Chunk_TSource]) -> System.Linq._Typed_Enumerable_Chunk[System_Linq_Enumerable_Chunk_TSource]:
        ...


class _Typed_Enumerable_Sequence(typing.Generic[System_Linq_Enumerable_Sequence_T]):
    """"""

    @overload
    def __call__(self, start: System_Linq_Enumerable_Sequence_T, end_inclusive: System_Linq_Enumerable_Sequence_T, step: System_Linq_Enumerable_Sequence_T) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sequence_T]:
        ...


class _Enumerable_Sequence:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Sequence_T]) -> System.Linq._Typed_Enumerable_Sequence[System_Linq_Enumerable_Sequence_T]:
        ...


class _Typed_Enumerable_AsEnumerable(typing.Generic[System_Linq_Enumerable_AsEnumerable_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AsEnumerable_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AsEnumerable_TSource]:
        ...


class _Enumerable_AsEnumerable:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_AsEnumerable_TSource]) -> System.Linq._Typed_Enumerable_AsEnumerable[System_Linq_Enumerable_AsEnumerable_TSource]:
        ...


class _Typed_Enumerable_Empty(typing.Generic[System_Linq_Enumerable_Empty_TResult]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Empty_TResult]:
        ...


class _Enumerable_Empty:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Empty_TResult]) -> System.Linq._Typed_Enumerable_Empty[System_Linq_Enumerable_Empty_TResult]:
        ...


class _Typed_Enumerable_First(typing.Generic[System_Linq_Enumerable_First_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_First_TSource]) -> System_Linq_Enumerable_First_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_First_TSource], predicate: typing.Callable[[System_Linq_Enumerable_First_TSource], bool]) -> System_Linq_Enumerable_First_TSource:
        ...


class _Enumerable_First:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_First_TSource]) -> System.Linq._Typed_Enumerable_First[System_Linq_Enumerable_First_TSource]:
        ...


class _Typed_Enumerable_FirstOrDefault(typing.Generic[System_Linq_Enumerable_FirstOrDefault_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource]) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], default_value: System_Linq_Enumerable_FirstOrDefault_TSource) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_FirstOrDefault_TSource], bool]) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_FirstOrDefault_TSource], bool], default_value: System_Linq_Enumerable_FirstOrDefault_TSource) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...


class _Enumerable_FirstOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_FirstOrDefault_TSource]) -> System.Linq._Typed_Enumerable_FirstOrDefault[System_Linq_Enumerable_FirstOrDefault_TSource]:
        ...


class _Typed_Enumerable_Select(typing.Generic[System_Linq_Enumerable_Select_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TSource], selector: typing.Callable[[System_Linq_Enumerable_Select_TSource], System_Linq_Enumerable_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TSource], selector: typing.Callable[[System_Linq_Enumerable_Select_TSource, int], System_Linq_Enumerable_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TResult]:
        ...


class _Enumerable_Select:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Select_TSource]) -> System.Linq._Typed_Enumerable_Select[System_Linq_Enumerable_Select_TSource]:
        ...


class _Typed_Enumerable_Count(typing.Generic[System_Linq_Enumerable_Count_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Count_TSource]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Count_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Count_TSource], bool]) -> int:
        ...


class _Enumerable_Count:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Count_TSource]) -> System.Linq._Typed_Enumerable_Count[System_Linq_Enumerable_Count_TSource]:
        ...


class _Typed_Enumerable_TryGetNonEnumeratedCount(typing.Generic[System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource], count: typing.Optional[int]) -> typing.Tuple[bool, int]:
        ...


class _Enumerable_TryGetNonEnumeratedCount:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource]) -> System.Linq._Typed_Enumerable_TryGetNonEnumeratedCount[System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource]:
        ...


class _Typed_Enumerable_LongCount(typing.Generic[System_Linq_Enumerable_LongCount_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LongCount_TSource]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LongCount_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LongCount_TSource], bool]) -> int:
        ...


class _Enumerable_LongCount:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_LongCount_TSource]) -> System.Linq._Typed_Enumerable_LongCount[System_Linq_Enumerable_LongCount_TSource]:
        ...


class _Typed_Enumerable_Zip(typing.Generic[System_Linq_Enumerable_Zip_TFirst]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond], result_selector: typing.Callable[[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond], System_Linq_Enumerable_Zip_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TResult]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond]]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond], third: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TThird]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond, System_Linq_Enumerable_Zip_TThird]]:
        ...


class _Enumerable_Zip:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Zip_TFirst]) -> System.Linq._Typed_Enumerable_Zip[System_Linq_Enumerable_Zip_TFirst]:
        ...


class _Typed_Enumerable_Join(typing.Generic[System_Linq_Enumerable_Join_TOuter]):
    """"""

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter], System_Linq_Enumerable_Join_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter, System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter], System_Linq_Enumerable_Join_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter, System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Join_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter], System_Linq_Enumerable_Join_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Join_TKey] = None) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_Join_TOuter, System_Linq_Enumerable_Join_TInner]]:
        ...


class _Enumerable_Join:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Join_TOuter]) -> System.Linq._Typed_Enumerable_Join[System_Linq_Enumerable_Join_TOuter]:
        ...


class _Typed_Enumerable_InfiniteSequence(typing.Generic[System_Linq_Enumerable_InfiniteSequence_T]):
    """"""

    @overload
    def __call__(self, start: System_Linq_Enumerable_InfiniteSequence_T, step: System_Linq_Enumerable_InfiniteSequence_T) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_InfiniteSequence_T]:
        ...


class _Enumerable_InfiniteSequence:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_InfiniteSequence_T]) -> System.Linq._Typed_Enumerable_InfiniteSequence[System_Linq_Enumerable_InfiniteSequence_T]:
        ...


class _Typed_Enumerable_GroupBy(typing.Generic[System_Linq_Enumerable_GroupBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TSource]]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TSource]]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TElement]]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TElement]]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, typing.List[System_Linq_Enumerable_GroupBy_TSource]], System_Linq_Enumerable_GroupBy_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, typing.List[System_Linq_Enumerable_GroupBy_TSource]], System_Linq_Enumerable_GroupBy_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, typing.List[System_Linq_Enumerable_GroupBy_TElement]], System_Linq_Enumerable_GroupBy_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, typing.List[System_Linq_Enumerable_GroupBy_TElement]], System_Linq_Enumerable_GroupBy_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...


class _Enumerable_GroupBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_GroupBy_TSource]) -> System.Linq._Typed_Enumerable_GroupBy[System_Linq_Enumerable_GroupBy_TSource]:
        ...


class _Typed_Enumerable_Contains(typing.Generic[System_Linq_Enumerable_Contains_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Contains_TSource], value: System_Linq_Enumerable_Contains_TSource) -> bool:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Contains_TSource], value: System_Linq_Enumerable_Contains_TSource, comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Contains_TSource]) -> bool:
        ...


class _Enumerable_Contains:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Contains_TSource]) -> System.Linq._Typed_Enumerable_Contains[System_Linq_Enumerable_Contains_TSource]:
        ...


class _Typed_Enumerable_Union(typing.Generic[System_Linq_Enumerable_Union_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Union_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]:
        ...


class _Enumerable_Union:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Union_TSource]) -> System.Linq._Typed_Enumerable_Union[System_Linq_Enumerable_Union_TSource]:
        ...


class _Typed_Enumerable_UnionBy(typing.Generic[System_Linq_Enumerable_UnionBy_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_UnionBy_TSource], System_Linq_Enumerable_UnionBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_UnionBy_TSource], System_Linq_Enumerable_UnionBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_UnionBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource]:
        ...


class _Enumerable_UnionBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_UnionBy_TSource]) -> System.Linq._Typed_Enumerable_UnionBy[System_Linq_Enumerable_UnionBy_TSource]:
        ...


class _Typed_Enumerable_Any(typing.Generic[System_Linq_Enumerable_Any_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Any_TSource]) -> bool:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Any_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Any_TSource], bool]) -> bool:
        ...


class _Enumerable_Any:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Any_TSource]) -> System.Linq._Typed_Enumerable_Any[System_Linq_Enumerable_Any_TSource]:
        ...


class _Typed_Enumerable_All(typing.Generic[System_Linq_Enumerable_All_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_All_TSource], predicate: typing.Callable[[System_Linq_Enumerable_All_TSource], bool]) -> bool:
        ...


class _Enumerable_All:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_All_TSource]) -> System.Linq._Typed_Enumerable_All[System_Linq_Enumerable_All_TSource]:
        ...


class _Typed_Enumerable_SelectMany(typing.Generic[System_Linq_Enumerable_SelectMany_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource], typing.List[System_Linq_Enumerable_SelectMany_TResult]]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, int], typing.List[System_Linq_Enumerable_SelectMany_TResult]]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, int], typing.List[System_Linq_Enumerable_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, System_Linq_Enumerable_SelectMany_TCollection], System_Linq_Enumerable_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource], typing.List[System_Linq_Enumerable_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, System_Linq_Enumerable_SelectMany_TCollection], System_Linq_Enumerable_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...


class _Enumerable_SelectMany:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_SelectMany_TSource]) -> System.Linq._Typed_Enumerable_SelectMany[System_Linq_Enumerable_SelectMany_TSource]:
        ...


class _Typed_Enumerable_Distinct(typing.Generic[System_Linq_Enumerable_Distinct_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Distinct_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]:
        ...


class _Enumerable_Distinct:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Distinct_TSource]) -> System.Linq._Typed_Enumerable_Distinct[System_Linq_Enumerable_Distinct_TSource]:
        ...


class _Typed_Enumerable_DistinctBy(typing.Generic[System_Linq_Enumerable_DistinctBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_DistinctBy_TSource], System_Linq_Enumerable_DistinctBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_DistinctBy_TSource], System_Linq_Enumerable_DistinctBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_DistinctBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource]:
        ...


class _Enumerable_DistinctBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_DistinctBy_TSource]) -> System.Linq._Typed_Enumerable_DistinctBy[System_Linq_Enumerable_DistinctBy_TSource]:
        ...


class _Typed_Enumerable_ToArray(typing.Generic[System_Linq_Enumerable_ToArray_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToArray_TSource]) -> typing.List[System_Linq_Enumerable_ToArray_TSource]:
        ...


class _Enumerable_ToArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ToArray_TSource]) -> System.Linq._Typed_Enumerable_ToArray[System_Linq_Enumerable_ToArray_TSource]:
        ...


class _Typed_Enumerable_ToList(typing.Generic[System_Linq_Enumerable_ToList_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToList_TSource]) -> System.Collections.Generic.List[System_Linq_Enumerable_ToList_TSource]:
        ...


class _Enumerable_ToList:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ToList_TSource]) -> System.Linq._Typed_Enumerable_ToList[System_Linq_Enumerable_ToList_TSource]:
        ...


class _Typed_Enumerable_ToDictionary(typing.Generic[System_Linq_Enumerable_ToDictionary_TKey]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TElement]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TElement]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TElement]:
        ...


class _Enumerable_ToDictionary:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Linq._Typed_Enumerable_ToDictionary[System_Linq_Enumerable_ToDictionary_TKey]:
        ...


class _Typed_Enumerable_ToHashSet(typing.Generic[System_Linq_Enumerable_ToHashSet_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToHashSet_TSource]) -> System.Collections.Generic.HashSet[System_Linq_Enumerable_ToHashSet_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToHashSet_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToHashSet_TSource]) -> System.Collections.Generic.HashSet[System_Linq_Enumerable_ToHashSet_TSource]:
        ...


class _Enumerable_ToHashSet:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ToHashSet_TSource]) -> System.Linq._Typed_Enumerable_ToHashSet[System_Linq_Enumerable_ToHashSet_TSource]:
        ...


class _Typed_Enumerable_LeftJoin(typing.Generic[System_Linq_Enumerable_LeftJoin_TOuter]):
    """"""

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TOuter], System_Linq_Enumerable_LeftJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TInner], System_Linq_Enumerable_LeftJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TOuter, System_Linq_Enumerable_LeftJoin_TInner], System_Linq_Enumerable_LeftJoin_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TOuter], System_Linq_Enumerable_LeftJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TInner], System_Linq_Enumerable_LeftJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TOuter, System_Linq_Enumerable_LeftJoin_TInner], System_Linq_Enumerable_LeftJoin_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_LeftJoin_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LeftJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TOuter], System_Linq_Enumerable_LeftJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_LeftJoin_TInner], System_Linq_Enumerable_LeftJoin_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_LeftJoin_TKey] = None) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_LeftJoin_TOuter, System_Linq_Enumerable_LeftJoin_TInner]]:
        ...


class _Enumerable_LeftJoin:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_LeftJoin_TOuter]) -> System.Linq._Typed_Enumerable_LeftJoin[System_Linq_Enumerable_LeftJoin_TOuter]:
        ...


class _Typed_Enumerable_SequenceEqual(typing.Generic[System_Linq_Enumerable_SequenceEqual_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource]) -> bool:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_SequenceEqual_TSource]) -> bool:
        ...


class _Enumerable_SequenceEqual:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_SequenceEqual_TSource]) -> System.Linq._Typed_Enumerable_SequenceEqual[System_Linq_Enumerable_SequenceEqual_TSource]:
        ...


class _Typed_Enumerable_Take(typing.Generic[System_Linq_Enumerable_Take_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource], range: System.Range) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource]:
        ...


class _Enumerable_Take:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Take_TSource]) -> System.Linq._Typed_Enumerable_Take[System_Linq_Enumerable_Take_TSource]:
        ...


class _Typed_Enumerable_TakeWhile(typing.Generic[System_Linq_Enumerable_TakeWhile_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_TakeWhile_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_TakeWhile_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource]:
        ...


class _Enumerable_TakeWhile:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_TakeWhile_TSource]) -> System.Linq._Typed_Enumerable_TakeWhile[System_Linq_Enumerable_TakeWhile_TSource]:
        ...


class _Typed_Enumerable_TakeLast(typing.Generic[System_Linq_Enumerable_TakeLast_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeLast_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeLast_TSource]:
        ...


class _Enumerable_TakeLast:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_TakeLast_TSource]) -> System.Linq._Typed_Enumerable_TakeLast[System_Linq_Enumerable_TakeLast_TSource]:
        ...


class _Typed_Enumerable_ToLookup(typing.Generic[System_Linq_Enumerable_ToLookup_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TElement]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TElement]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TElement]:
        ...


class _Enumerable_ToLookup:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ToLookup_TSource]) -> System.Linq._Typed_Enumerable_ToLookup[System_Linq_Enumerable_ToLookup_TSource]:
        ...


class _Typed_Enumerable_Concat(typing.Generic[System_Linq_Enumerable_Concat_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource]:
        ...


class _Enumerable_Concat:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Concat_TSource]) -> System.Linq._Typed_Enumerable_Concat[System_Linq_Enumerable_Concat_TSource]:
        ...


class _Typed_Enumerable_CountBy(typing.Generic[System_Linq_Enumerable_CountBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_CountBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_CountBy_TSource], System_Linq_Enumerable_CountBy_TKey], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_CountBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_CountBy_TKey, int]]:
        ...


class _Enumerable_CountBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_CountBy_TSource]) -> System.Linq._Typed_Enumerable_CountBy[System_Linq_Enumerable_CountBy_TSource]:
        ...


class _Typed_Enumerable_AggregateBy(typing.Generic[System_Linq_Enumerable_AggregateBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AggregateBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TKey], seed: System_Linq_Enumerable_AggregateBy_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_AggregateBy_TAccumulate, System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TAccumulate], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_AggregateBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_AggregateBy_TKey, System_Linq_Enumerable_AggregateBy_TAccumulate]]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AggregateBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TKey], seed_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TKey], System_Linq_Enumerable_AggregateBy_TAccumulate], func: typing.Callable[[System_Linq_Enumerable_AggregateBy_TAccumulate, System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TAccumulate], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_AggregateBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_AggregateBy_TKey, System_Linq_Enumerable_AggregateBy_TAccumulate]]:
        ...


class _Enumerable_AggregateBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_AggregateBy_TSource]) -> System.Linq._Typed_Enumerable_AggregateBy[System_Linq_Enumerable_AggregateBy_TSource]:
        ...


class _Typed_Enumerable_ElementAt(typing.Generic[System_Linq_Enumerable_ElementAt_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAt_TSource], index: int) -> System_Linq_Enumerable_ElementAt_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAt_TSource], index: System.Index) -> System_Linq_Enumerable_ElementAt_TSource:
        ...


class _Enumerable_ElementAt:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ElementAt_TSource]) -> System.Linq._Typed_Enumerable_ElementAt[System_Linq_Enumerable_ElementAt_TSource]:
        ...


class _Typed_Enumerable_ElementAtOrDefault(typing.Generic[System_Linq_Enumerable_ElementAtOrDefault_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAtOrDefault_TSource], index: int) -> System_Linq_Enumerable_ElementAtOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAtOrDefault_TSource], index: System.Index) -> System_Linq_Enumerable_ElementAtOrDefault_TSource:
        ...


class _Enumerable_ElementAtOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ElementAtOrDefault_TSource]) -> System.Linq._Typed_Enumerable_ElementAtOrDefault[System_Linq_Enumerable_ElementAtOrDefault_TSource]:
        ...


class _Typed_Enumerable_Cast(typing.Generic[System_Linq_Enumerable_Cast_TResult]):
    """"""

    @overload
    def __call__(self, source: System.Collections.IEnumerable) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Cast_TResult]:
        ...


class _Enumerable_Cast:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Cast_TResult]) -> System.Linq._Typed_Enumerable_Cast[System_Linq_Enumerable_Cast_TResult]:
        ...


class _Typed_Enumerable_Max(typing.Generic[System_Linq_Enumerable_Max_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource]) -> System_Linq_Enumerable_Max_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Max_TSource]) -> System_Linq_Enumerable_Max_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], System_Linq_Enumerable_Max_TResult]) -> System_Linq_Enumerable_Max_TResult:
        ...


class _Enumerable_Max:
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Max_TSource]) -> System.Linq._Typed_Enumerable_Max[System_Linq_Enumerable_Max_TSource]:
        ...


class _Typed_Enumerable_MaxBy(typing.Generic[System_Linq_Enumerable_MaxBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MaxBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MaxBy_TSource], System_Linq_Enumerable_MaxBy_TKey]) -> System_Linq_Enumerable_MaxBy_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MaxBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MaxBy_TSource], System_Linq_Enumerable_MaxBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_MaxBy_TKey]) -> System_Linq_Enumerable_MaxBy_TSource:
        ...


class _Enumerable_MaxBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_MaxBy_TSource]) -> System.Linq._Typed_Enumerable_MaxBy[System_Linq_Enumerable_MaxBy_TSource]:
        ...


class _Typed_Enumerable_Where(typing.Generic[System_Linq_Enumerable_Where_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Where_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Where_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource]:
        ...


class _Enumerable_Where:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Where_TSource]) -> System.Linq._Typed_Enumerable_Where[System_Linq_Enumerable_Where_TSource]:
        ...


class _Typed_Enumerable_Reverse(typing.Generic[System_Linq_Enumerable_Reverse_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]:
        ...

    @overload
    def __call__(self, source: typing.List[System_Linq_Enumerable_Reverse_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]:
        ...


class _Enumerable_Reverse:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Reverse_TSource]) -> System.Linq._Typed_Enumerable_Reverse[System_Linq_Enumerable_Reverse_TSource]:
        ...


class _Typed_Enumerable_Last(typing.Generic[System_Linq_Enumerable_Last_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Last_TSource]) -> System_Linq_Enumerable_Last_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Last_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Last_TSource], bool]) -> System_Linq_Enumerable_Last_TSource:
        ...


class _Enumerable_Last:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Last_TSource]) -> System.Linq._Typed_Enumerable_Last[System_Linq_Enumerable_Last_TSource]:
        ...


class _Typed_Enumerable_LastOrDefault(typing.Generic[System_Linq_Enumerable_LastOrDefault_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource]) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], default_value: System_Linq_Enumerable_LastOrDefault_TSource) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LastOrDefault_TSource], bool]) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LastOrDefault_TSource], bool], default_value: System_Linq_Enumerable_LastOrDefault_TSource) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...


class _Enumerable_LastOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_LastOrDefault_TSource]) -> System.Linq._Typed_Enumerable_LastOrDefault[System_Linq_Enumerable_LastOrDefault_TSource]:
        ...


class _Typed_Enumerable_Intersect(typing.Generic[System_Linq_Enumerable_Intersect_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Intersect_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]:
        ...


class _Enumerable_Intersect:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Intersect_TSource]) -> System.Linq._Typed_Enumerable_Intersect[System_Linq_Enumerable_Intersect_TSource]:
        ...


class _Typed_Enumerable_IntersectBy(typing.Generic[System_Linq_Enumerable_IntersectBy_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_IntersectBy_TSource], System_Linq_Enumerable_IntersectBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_IntersectBy_TSource], System_Linq_Enumerable_IntersectBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_IntersectBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource]:
        ...


class _Enumerable_IntersectBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_IntersectBy_TSource]) -> System.Linq._Typed_Enumerable_IntersectBy[System_Linq_Enumerable_IntersectBy_TSource]:
        ...


class _Typed_Enumerable_Repeat(typing.Generic[System_Linq_Enumerable_Repeat_TResult]):
    """"""

    @overload
    def __call__(self, element: System_Linq_Enumerable_Repeat_TResult, count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Repeat_TResult]:
        ...


class _Enumerable_Repeat:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Repeat_TResult]) -> System.Linq._Typed_Enumerable_Repeat[System_Linq_Enumerable_Repeat_TResult]:
        ...


class _Typed_Enumerable_RightJoin(typing.Generic[System_Linq_Enumerable_RightJoin_TOuter]):
    """"""

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TOuter], System_Linq_Enumerable_RightJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TInner], System_Linq_Enumerable_RightJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TOuter, System_Linq_Enumerable_RightJoin_TInner], System_Linq_Enumerable_RightJoin_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TOuter], System_Linq_Enumerable_RightJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TInner], System_Linq_Enumerable_RightJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TOuter, System_Linq_Enumerable_RightJoin_TInner], System_Linq_Enumerable_RightJoin_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_RightJoin_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_RightJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TOuter], System_Linq_Enumerable_RightJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_RightJoin_TInner], System_Linq_Enumerable_RightJoin_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_RightJoin_TKey] = None) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_RightJoin_TOuter, System_Linq_Enumerable_RightJoin_TInner]]:
        ...


class _Enumerable_RightJoin:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_RightJoin_TOuter]) -> System.Linq._Typed_Enumerable_RightJoin[System_Linq_Enumerable_RightJoin_TOuter]:
        ...


class _Typed_Enumerable_Shuffle(typing.Generic[System_Linq_Enumerable_Shuffle_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Shuffle_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Shuffle_TSource]:
        ...


class _Enumerable_Shuffle:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Shuffle_TSource]) -> System.Linq._Typed_Enumerable_Shuffle[System_Linq_Enumerable_Shuffle_TSource]:
        ...


class _Typed_Enumerable_FullJoin(typing.Generic[System_Linq_Enumerable_FullJoin_TOuter]):
    """"""

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FullJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FullJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_FullJoin_TOuter], System_Linq_Enumerable_FullJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_FullJoin_TInner], System_Linq_Enumerable_FullJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_FullJoin_TOuter, System_Linq_Enumerable_FullJoin_TInner], System_Linq_Enumerable_FullJoin_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_FullJoin_TKey] = None) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FullJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FullJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FullJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_FullJoin_TOuter], System_Linq_Enumerable_FullJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_FullJoin_TInner], System_Linq_Enumerable_FullJoin_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_FullJoin_TKey] = None) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_FullJoin_TOuter, System_Linq_Enumerable_FullJoin_TInner]]:
        ...


class _Enumerable_FullJoin:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_FullJoin_TOuter]) -> System.Linq._Typed_Enumerable_FullJoin[System_Linq_Enumerable_FullJoin_TOuter]:
        ...


class _Typed_Enumerable_Aggregate(typing.Generic[System_Linq_Enumerable_Aggregate_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], func: typing.Callable[[System_Linq_Enumerable_Aggregate_TSource, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TSource]) -> System_Linq_Enumerable_Aggregate_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], seed: System_Linq_Enumerable_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TAccumulate]) -> System_Linq_Enumerable_Aggregate_TAccumulate:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], seed: System_Linq_Enumerable_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TAccumulate], result_selector: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate], System_Linq_Enumerable_Aggregate_TResult]) -> System_Linq_Enumerable_Aggregate_TResult:
        ...


class _Enumerable_Aggregate:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Aggregate_TSource]) -> System.Linq._Typed_Enumerable_Aggregate[System_Linq_Enumerable_Aggregate_TSource]:
        ...


class _Typed_Enumerable_OfType(typing.Generic[System_Linq_Enumerable_OfType_TResult]):
    """"""

    @overload
    def __call__(self, source: System.Collections.IEnumerable) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OfType_TResult]:
        ...


class _Enumerable_OfType:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_OfType_TResult]) -> System.Linq._Typed_Enumerable_OfType[System_Linq_Enumerable_OfType_TResult]:
        ...


class _Typed_Enumerable_Except(typing.Generic[System_Linq_Enumerable_Except_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Except_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]:
        ...


class _Enumerable_Except:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Except_TSource]) -> System.Linq._Typed_Enumerable_Except[System_Linq_Enumerable_Except_TSource]:
        ...


class _Typed_Enumerable_ExceptBy(typing.Generic[System_Linq_Enumerable_ExceptBy_TSource]):
    """"""

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_ExceptBy_TSource], System_Linq_Enumerable_ExceptBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource]:
        ...

    @overload
    def __call__(self, first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_ExceptBy_TSource], System_Linq_Enumerable_ExceptBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ExceptBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource]:
        ...


class _Enumerable_ExceptBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_ExceptBy_TSource]) -> System.Linq._Typed_Enumerable_ExceptBy[System_Linq_Enumerable_ExceptBy_TSource]:
        ...


class _Typed_Enumerable_Average(typing.Generic[System_Linq_Enumerable_Average_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], int]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], int]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...


class _Enumerable_Average:
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[int]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Average_TSource]) -> System.Linq._Typed_Enumerable_Average[System_Linq_Enumerable_Average_TSource]:
        ...


class _Typed_Enumerable_Min(typing.Generic[System_Linq_Enumerable_Min_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource]) -> System_Linq_Enumerable_Min_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Min_TSource]) -> System_Linq_Enumerable_Min_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], System_Linq_Enumerable_Min_TResult]) -> System_Linq_Enumerable_Min_TResult:
        ...


class _Enumerable_Min:
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Min_TSource]) -> System.Linq._Typed_Enumerable_Min[System_Linq_Enumerable_Min_TSource]:
        ...


class _Typed_Enumerable_MinBy(typing.Generic[System_Linq_Enumerable_MinBy_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MinBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MinBy_TSource], System_Linq_Enumerable_MinBy_TKey]) -> System_Linq_Enumerable_MinBy_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MinBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MinBy_TSource], System_Linq_Enumerable_MinBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_MinBy_TKey]) -> System_Linq_Enumerable_MinBy_TSource:
        ...


class _Enumerable_MinBy:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_MinBy_TSource]) -> System.Linq._Typed_Enumerable_MinBy[System_Linq_Enumerable_MinBy_TSource]:
        ...


class _Typed_Enumerable_Single(typing.Generic[System_Linq_Enumerable_Single_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Single_TSource]) -> System_Linq_Enumerable_Single_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Single_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Single_TSource], bool]) -> System_Linq_Enumerable_Single_TSource:
        ...


class _Enumerable_Single:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_Single_TSource]) -> System.Linq._Typed_Enumerable_Single[System_Linq_Enumerable_Single_TSource]:
        ...


class _Typed_Enumerable_SingleOrDefault(typing.Generic[System_Linq_Enumerable_SingleOrDefault_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource]) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], default_value: System_Linq_Enumerable_SingleOrDefault_TSource) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SingleOrDefault_TSource], bool]) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SingleOrDefault_TSource], bool], default_value: System_Linq_Enumerable_SingleOrDefault_TSource) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...


class _Enumerable_SingleOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_SingleOrDefault_TSource]) -> System.Linq._Typed_Enumerable_SingleOrDefault[System_Linq_Enumerable_SingleOrDefault_TSource]:
        ...


class _Typed_Enumerable_GroupJoin(typing.Generic[System_Linq_Enumerable_GroupJoin_TOuter]):
    """"""

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter], System_Linq_Enumerable_GroupJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TInner], System_Linq_Enumerable_GroupJoin_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupJoin_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupJoin_TOuter, System_Linq_Enumerable_GroupJoin_TInner]]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter], System_Linq_Enumerable_GroupJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TInner], System_Linq_Enumerable_GroupJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter, typing.List[System_Linq_Enumerable_GroupJoin_TInner]], System_Linq_Enumerable_GroupJoin_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TResult]:
        ...

    @overload
    def __call__(self, outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter], System_Linq_Enumerable_GroupJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TInner], System_Linq_Enumerable_GroupJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter, typing.List[System_Linq_Enumerable_GroupJoin_TInner]], System_Linq_Enumerable_GroupJoin_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupJoin_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TResult]:
        ...


class _Enumerable_GroupJoin:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_GroupJoin_TOuter]) -> System.Linq._Typed_Enumerable_GroupJoin[System_Linq_Enumerable_GroupJoin_TOuter]:
        ...


class _Typed_Enumerable_DefaultIfEmpty(typing.Generic[System_Linq_Enumerable_DefaultIfEmpty_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource], default_value: System_Linq_Enumerable_DefaultIfEmpty_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]:
        ...


class _Enumerable_DefaultIfEmpty:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Enumerable_DefaultIfEmpty_TSource]) -> System.Linq._Typed_Enumerable_DefaultIfEmpty[System_Linq_Enumerable_DefaultIfEmpty_TSource]:
        ...


class Enumerable(System.Object):
    """This class has no documentation."""

    append: System.Linq._Enumerable_Append

    prepend: System.Linq._Enumerable_Prepend

    skip: System.Linq._Enumerable_Skip

    skip_while: System.Linq._Enumerable_SkipWhile

    skip_last: System.Linq._Enumerable_SkipLast

    order: System.Linq._Enumerable_Order

    order_by: System.Linq._Enumerable_OrderBy

    order_descending: System.Linq._Enumerable_OrderDescending

    order_by_descending: System.Linq._Enumerable_OrderByDescending

    then_by: System.Linq._Enumerable_ThenBy

    then_by_descending: System.Linq._Enumerable_ThenByDescending

    sum: System.Linq._Enumerable_Sum

    index: System.Linq._Enumerable_Index

    chunk: System.Linq._Enumerable_Chunk

    sequence: System.Linq._Enumerable_Sequence

    as_enumerable: System.Linq._Enumerable_AsEnumerable

    empty: System.Linq._Enumerable_Empty

    first: System.Linq._Enumerable_First

    first_or_default: System.Linq._Enumerable_FirstOrDefault

    select: System.Linq._Enumerable_Select

    count: System.Linq._Enumerable_Count

    try_get_non_enumerated_count: System.Linq._Enumerable_TryGetNonEnumeratedCount

    long_count: System.Linq._Enumerable_LongCount

    zip: System.Linq._Enumerable_Zip

    join: System.Linq._Enumerable_Join

    infinite_sequence: System.Linq._Enumerable_InfiniteSequence

    group_by: System.Linq._Enumerable_GroupBy

    contains: System.Linq._Enumerable_Contains

    union: System.Linq._Enumerable_Union

    union_by: System.Linq._Enumerable_UnionBy

    any: System.Linq._Enumerable_Any

    all: System.Linq._Enumerable_All

    select_many: System.Linq._Enumerable_SelectMany

    distinct: System.Linq._Enumerable_Distinct

    distinct_by: System.Linq._Enumerable_DistinctBy

    to_array: System.Linq._Enumerable_ToArray

    to_list: System.Linq._Enumerable_ToList

    to_dictionary: System.Linq._Enumerable_ToDictionary

    to_hash_set: System.Linq._Enumerable_ToHashSet

    left_join: System.Linq._Enumerable_LeftJoin

    sequence_equal: System.Linq._Enumerable_SequenceEqual

    take: System.Linq._Enumerable_Take

    take_while: System.Linq._Enumerable_TakeWhile

    take_last: System.Linq._Enumerable_TakeLast

    to_lookup: System.Linq._Enumerable_ToLookup

    concat: System.Linq._Enumerable_Concat

    count_by: System.Linq._Enumerable_CountBy

    aggregate_by: System.Linq._Enumerable_AggregateBy

    element_at: System.Linq._Enumerable_ElementAt

    element_at_or_default: System.Linq._Enumerable_ElementAtOrDefault

    cast: System.Linq._Enumerable_Cast

    max: System.Linq._Enumerable_Max

    max_by: System.Linq._Enumerable_MaxBy

    where: System.Linq._Enumerable_Where

    reverse: System.Linq._Enumerable_Reverse

    last: System.Linq._Enumerable_Last

    last_or_default: System.Linq._Enumerable_LastOrDefault

    intersect: System.Linq._Enumerable_Intersect

    intersect_by: System.Linq._Enumerable_IntersectBy

    repeat: System.Linq._Enumerable_Repeat

    right_join: System.Linq._Enumerable_RightJoin

    shuffle: System.Linq._Enumerable_Shuffle

    full_join: System.Linq._Enumerable_FullJoin

    aggregate: System.Linq._Enumerable_Aggregate

    of_type: System.Linq._Enumerable_OfType

    Except: System.Linq._Enumerable_Except

    except_by: System.Linq._Enumerable_ExceptBy

    average: System.Linq._Enumerable_Average

    min: System.Linq._Enumerable_Min

    min_by: System.Linq._Enumerable_MinBy

    single: System.Linq._Enumerable_Single

    single_or_default: System.Linq._Enumerable_SingleOrDefault

    group_join: System.Linq._Enumerable_GroupJoin

    default_if_empty: System.Linq._Enumerable_DefaultIfEmpty

    @staticmethod
    def range(start: int, count: int) -> System.Collections.Generic.IEnumerable[int]:
        ...


class _Typed_Lookup_ApplyResultSelector(typing.Generic[System_Linq_Lookup_ApplyResultSelector_TResult]):
    """"""

    @overload
    def __call__(self, result_selector: typing.Callable[[System_Linq_Lookup_TKey, typing.List[System_Linq_Lookup_TElement]], System_Linq_Lookup_ApplyResultSelector_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Lookup_ApplyResultSelector_TResult]:
        ...


class _Lookup_ApplyResultSelector:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_Lookup_ApplyResultSelector_TResult]) -> System.Linq._Typed_Lookup_ApplyResultSelector[System_Linq_Lookup_ApplyResultSelector_TResult]:
        ...


class Lookup(typing.Generic[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement], System.Object, System.Linq.ILookup[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement], typing.Iterable[System.Linq.IGrouping[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement]]):
    """This class has no documentation."""

    @property
    def count(self) -> int:
        ...

    @property
    def apply_result_selector(self) -> System.Linq._Lookup_ApplyResultSelector:
        ...

    def __getitem__(self, key: System_Linq_Lookup_TKey) -> System.Collections.Generic.IEnumerable[System_Linq_Lookup_TElement]:
        ...

    def __iter__(self) -> typing.Iterator[System.Linq.IGrouping[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement]]:
        ...

    def __len__(self) -> int:
        ...

    def contains(self, key: System_Linq_Lookup_TKey) -> bool:
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[System.Linq.IGrouping[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement]]:
        ...


class _Typed_IOrderedEnumerable_CreateOrderedEnumerable(typing.Generic[System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey]):
    """"""

    @overload
    def __call__(self, key_selector: typing.Callable[[System_Linq_IOrderedEnumerable_TElement], System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey], descending: bool) -> System.Linq.IOrderedEnumerable[System_Linq_IOrderedEnumerable_TElement]:
        ...


class _IOrderedEnumerable_CreateOrderedEnumerable:
    """"""

    def __getitem__(self, type: typing.Type[System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey]) -> System.Linq._Typed_IOrderedEnumerable_CreateOrderedEnumerable[System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey]:
        ...


class IOrderedEnumerable(typing.Generic[System_Linq_IOrderedEnumerable_TElement], System.Collections.Generic.IEnumerable[System_Linq_IOrderedEnumerable_TElement], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def create_ordered_enumerable(self) -> System.Linq._IOrderedEnumerable_CreateOrderedEnumerable:
        ...


class IGrouping(typing.Generic[System_Linq_IGrouping_TKey, System_Linq_IGrouping_TElement], System.Collections.Generic.IEnumerable[System_Linq_IGrouping_TElement], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def key(self) -> System_Linq_IGrouping_TKey:
        ...


class ILookup(typing.Generic[System_Linq_ILookup_TKey, System_Linq_ILookup_TElement], System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_ILookup_TKey, System_Linq_ILookup_TElement]], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def count(self) -> int:
        ...

    def __getitem__(self, key: System_Linq_ILookup_TKey) -> System.Collections.Generic.IEnumerable[System_Linq_ILookup_TElement]:
        ...

    def __len__(self) -> int:
        ...

    def contains(self, key: System_Linq_ILookup_TKey) -> bool:
        ...


