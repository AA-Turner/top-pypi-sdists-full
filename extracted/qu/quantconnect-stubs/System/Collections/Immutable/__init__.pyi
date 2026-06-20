from typing import overload
from enum import IntEnum
import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.Immutable

System_Collections_Immutable_ImmutableList_Enumerator = typing.Any
System_Collections_Immutable_ImmutableSortedSet_Enumerator = typing.Any
System_Collections_Immutable_ImmutableHashSet_Enumerator = typing.Any
System_Collections_Immutable_ImmutableArray = typing.Any

System_Collections_Immutable_ImmutableList_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_T")
System_Collections_Immutable_ImmutableDictionary_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_TValue")
System_Collections_Immutable_ImmutableDictionary_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_TKey")
System_Collections_Immutable_ImmutableSortedSet_T = typing.TypeVar("System_Collections_Immutable_ImmutableSortedSet_T")
System_Collections_Immutable_ImmutableHashSet_T = typing.TypeVar("System_Collections_Immutable_ImmutableHashSet_T")
System_Collections_Immutable_ImmutableArray_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_T")
System_Collections_Immutable_ImmutableQueue_T = typing.TypeVar("System_Collections_Immutable_ImmutableQueue_T")
System_Collections_Immutable_IImmutableStack_T = typing.TypeVar("System_Collections_Immutable_IImmutableStack_T")
System_Collections_Immutable_ImmutableStack_T = typing.TypeVar("System_Collections_Immutable_ImmutableStack_T")
System_Collections_Immutable_IImmutableSet_T = typing.TypeVar("System_Collections_Immutable_IImmutableSet_T")
System_Collections_Immutable_ImmutableSortedDictionary_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_TValue")
System_Collections_Immutable_ImmutableSortedDictionary_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_TKey")
System_Collections_Immutable_IImmutableDictionary_TKey = typing.TypeVar("System_Collections_Immutable_IImmutableDictionary_TKey")
System_Collections_Immutable_IImmutableDictionary_TValue = typing.TypeVar("System_Collections_Immutable_IImmutableDictionary_TValue")
System_Collections_Immutable_IImmutableList_T = typing.TypeVar("System_Collections_Immutable_IImmutableList_T")
System_Collections_Immutable_IImmutableQueue_T = typing.TypeVar("System_Collections_Immutable_IImmutableQueue_T")
System_Collections_Immutable_ImmutableList_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_Create_T")
System_Collections_Immutable_ImmutableList_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_CreateRange_T")
System_Collections_Immutable_ImmutableList_CreateBuilder_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_CreateBuilder_T")
System_Collections_Immutable_ImmutableList_ToImmutableList_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableList_ToImmutableList_TSource")
System_Collections_Immutable_ImmutableList_Replace_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_Replace_T")
System_Collections_Immutable_ImmutableList_Remove_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_Remove_T")
System_Collections_Immutable_ImmutableList_RemoveRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_RemoveRange_T")
System_Collections_Immutable_ImmutableList_IndexOf_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_IndexOf_T")
System_Collections_Immutable_ImmutableList_LastIndexOf_T = typing.TypeVar("System_Collections_Immutable_ImmutableList_LastIndexOf_T")
System_Collections_Immutable_ImmutableList_ConvertAll_TOutput = typing.TypeVar("System_Collections_Immutable_ImmutableList_ConvertAll_TOutput")
System_Collections_Immutable_ImmutableDictionary_Create_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_Create_TKey")
System_Collections_Immutable_ImmutableDictionary_Create_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_Create_TValue")
System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey")
System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue")
System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey")
System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue")
System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey")
System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TValue")
System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource")
System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey")
System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue")
System_Collections_Immutable_ImmutableDictionary_Contains_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_Contains_TKey")
System_Collections_Immutable_ImmutableDictionary_Contains_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_Contains_TValue")
System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey")
System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue")
System_Collections_Immutable_ImmutableSortedSet_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableSortedSet_Create_T")
System_Collections_Immutable_ImmutableSortedSet_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableSortedSet_CreateRange_T")
System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T = typing.TypeVar("System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T")
System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource")
System_Collections_Immutable_ImmutableHashSet_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableHashSet_Create_T")
System_Collections_Immutable_ImmutableHashSet_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableHashSet_CreateRange_T")
System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T = typing.TypeVar("System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T")
System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource")
System_Collections_Immutable_ImmutableArray_CastUp_TDerived = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CastUp_TDerived")
System_Collections_Immutable_ImmutableArray_CastArray_TOther = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CastArray_TOther")
System_Collections_Immutable_ImmutableArray_As_TOther = typing.TypeVar("System_Collections_Immutable_ImmutableArray_As_TOther")
System_Collections_Immutable_ImmutableArray_AddRange_TDerived = typing.TypeVar("System_Collections_Immutable_ImmutableArray_AddRange_TDerived")
System_Collections_Immutable_ImmutableArray_OfType_TResult = typing.TypeVar("System_Collections_Immutable_ImmutableArray_OfType_TResult")
System_Collections_Immutable_ImmutableArray_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_Create_T")
System_Collections_Immutable_ImmutableArray_ToImmutableArray_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_ToImmutableArray_T")
System_Collections_Immutable_ImmutableArray_ToImmutableArray_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableArray_ToImmutableArray_TSource")
System_Collections_Immutable_ImmutableArray_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CreateRange_T")
System_Collections_Immutable_ImmutableArray_CreateRange_TArg = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CreateRange_TArg")
System_Collections_Immutable_ImmutableArray_CreateRange_TResult = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CreateRange_TResult")
System_Collections_Immutable_ImmutableArray_CreateRange_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CreateRange_TSource")
System_Collections_Immutable_ImmutableArray_CreateBuilder_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_CreateBuilder_T")
System_Collections_Immutable_ImmutableArray_BinarySearch_T = typing.TypeVar("System_Collections_Immutable_ImmutableArray_BinarySearch_T")
System_Collections_Immutable_ImmutableQueue_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableQueue_Create_T")
System_Collections_Immutable_ImmutableQueue_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableQueue_CreateRange_T")
System_Collections_Immutable_ImmutableQueue_Dequeue_T = typing.TypeVar("System_Collections_Immutable_ImmutableQueue_Dequeue_T")
System_Collections_Immutable_ImmutableStack_Create_T = typing.TypeVar("System_Collections_Immutable_ImmutableStack_Create_T")
System_Collections_Immutable_ImmutableStack_CreateRange_T = typing.TypeVar("System_Collections_Immutable_ImmutableStack_CreateRange_T")
System_Collections_Immutable_ImmutableStack_Pop_T = typing.TypeVar("System_Collections_Immutable_ImmutableStack_Pop_T")
System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey")
System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue")
System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey")
System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue")
System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey")
System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TValue")
System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource")
System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey")
System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue")
System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived = typing.TypeVar("System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived")
System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput = typing.TypeVar("System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput")
System_Collections_Immutable_ImmutableInterlocked_Update_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_Update_T")
System_Collections_Immutable_ImmutableInterlocked_Update_TArg = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_Update_TArg")
System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T")
System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T")
System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T")
System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey")
System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue")
System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TArg = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TArg")
System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey")
System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue")
System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey")
System_Collections_Immutable_ImmutableInterlocked_TryAdd_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryAdd_TValue")
System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey")
System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TValue")
System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey")
System_Collections_Immutable_ImmutableInterlocked_TryRemove_TValue = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryRemove_TValue")
System_Collections_Immutable_ImmutableInterlocked_TryPop_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryPop_T")
System_Collections_Immutable_ImmutableInterlocked_Push_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_Push_T")
System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T")
System_Collections_Immutable_ImmutableInterlocked_Enqueue_T = typing.TypeVar("System_Collections_Immutable_ImmutableInterlocked_Enqueue_T")


class _Typed_ImmutableList_Create(typing.Generic[System_Collections_Immutable_ImmutableList_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableList_Create_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableList_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableList_Create_T]]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableList_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableList_Create_T]]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_Create_T]:
        ...


class _ImmutableList_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_Create_T]) -> System.Collections.Immutable._Typed_ImmutableList_Create[System_Collections_Immutable_ImmutableList_Create_T]:
        ...


class _Typed_ImmutableList_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableList_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_CreateRange_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_CreateRange_T]:
        ...


class _ImmutableList_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableList_CreateRange[System_Collections_Immutable_ImmutableList_CreateRange_T]:
        ...


class _Typed_ImmutableList_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableList_CreateBuilder_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableList.Builder:
        ...


class _ImmutableList_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_CreateBuilder_T]) -> System.Collections.Immutable._Typed_ImmutableList_CreateBuilder[System_Collections_Immutable_ImmutableList_CreateBuilder_T]:
        ...


class _Typed_ImmutableList_ToImmutableList(typing.Generic[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableList.Builder) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]:
        ...


class _ImmutableList_ToImmutableList:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]) -> System.Collections.Immutable._Typed_ImmutableList_ToImmutableList[System_Collections_Immutable_ImmutableList_ToImmutableList_TSource]:
        ...


class _Typed_ImmutableList_Replace(typing.Generic[System_Collections_Immutable_ImmutableList_Replace_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_Replace_T], old_value: System_Collections_Immutable_ImmutableList_Replace_T, new_value: System_Collections_Immutable_ImmutableList_Replace_T) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_Replace_T]:
        ...


class _ImmutableList_Replace:
    """"""

    @overload
    def __call__(self, old_value: System_Collections_Immutable_ImmutableList_T, new_value: System_Collections_Immutable_ImmutableList_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def __call__(self, old_value: System_Collections_Immutable_ImmutableList_T, new_value: System_Collections_Immutable_ImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_Replace_T]) -> System.Collections.Immutable._Typed_ImmutableList_Replace[System_Collections_Immutable_ImmutableList_Replace_T]:
        ...


class _Typed_ImmutableList_Remove(typing.Generic[System_Collections_Immutable_ImmutableList_Remove_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_Remove_T], value: System_Collections_Immutable_ImmutableList_Remove_T) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_Remove_T]:
        ...


class _ImmutableList_Remove:
    """"""

    @overload
    def __call__(self, value: System_Collections_Immutable_ImmutableList_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def __call__(self, value: System_Collections_Immutable_ImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_Remove_T]) -> System.Collections.Immutable._Typed_ImmutableList_Remove[System_Collections_Immutable_ImmutableList_Remove_T]:
        ...


class _Typed_ImmutableList_RemoveRange(typing.Generic[System_Collections_Immutable_ImmutableList_RemoveRange_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_RemoveRange_T], items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_RemoveRange_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_RemoveRange_T]:
        ...


class _ImmutableList_RemoveRange:
    """"""

    @overload
    def __call__(self, index: int, count: int) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_RemoveRange_T]) -> System.Collections.Immutable._Typed_ImmutableList_RemoveRange[System_Collections_Immutable_ImmutableList_RemoveRange_T]:
        ...


class _Typed_ImmutableList_IndexOf(typing.Generic[System_Collections_Immutable_ImmutableList_IndexOf_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_IndexOf_T], item: System_Collections_Immutable_ImmutableList_IndexOf_T) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_IndexOf_T], item: System_Collections_Immutable_ImmutableList_IndexOf_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_IndexOf_T]) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_IndexOf_T], item: System_Collections_Immutable_ImmutableList_IndexOf_T, start_index: int) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_IndexOf_T], item: System_Collections_Immutable_ImmutableList_IndexOf_T, start_index: int, count: int) -> int:
        ...


class _ImmutableList_IndexOf:
    """"""

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableList_T, index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
        ...

    @overload
    def __call__(self, value: System_Collections_Immutable_ImmutableList_T) -> int:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_IndexOf_T]) -> System.Collections.Immutable._Typed_ImmutableList_IndexOf[System_Collections_Immutable_ImmutableList_IndexOf_T]:
        ...


class _Typed_ImmutableList_LastIndexOf(typing.Generic[System_Collections_Immutable_ImmutableList_LastIndexOf_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_LastIndexOf_T], item: System_Collections_Immutable_ImmutableList_LastIndexOf_T) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_LastIndexOf_T], item: System_Collections_Immutable_ImmutableList_LastIndexOf_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_LastIndexOf_T]) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_LastIndexOf_T], item: System_Collections_Immutable_ImmutableList_LastIndexOf_T, start_index: int) -> int:
        ...

    @overload
    def __call__(self, list: System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_LastIndexOf_T], item: System_Collections_Immutable_ImmutableList_LastIndexOf_T, start_index: int, count: int) -> int:
        ...


class _ImmutableList_LastIndexOf:
    """"""

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableList_T, index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_LastIndexOf_T]) -> System.Collections.Immutable._Typed_ImmutableList_LastIndexOf[System_Collections_Immutable_ImmutableList_LastIndexOf_T]:
        ...


class _Typed_ImmutableList_ConvertAll(typing.Generic[System_Collections_Immutable_ImmutableList_ConvertAll_TOutput]):
    """"""

    @overload
    def __call__(self, converter: typing.Callable[[System_Collections_Immutable_ImmutableList_T], System_Collections_Immutable_ImmutableList_ConvertAll_TOutput]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_ConvertAll_TOutput]:
        ...


class _ImmutableList_ConvertAll:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_ConvertAll_TOutput]) -> System.Collections.Immutable._Typed_ImmutableList_ConvertAll[System_Collections_Immutable_ImmutableList_ConvertAll_TOutput]:
        ...


class ImmutableList(typing.Generic[System_Collections_Immutable_ImmutableList_T], System.Object, System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableList_T], System.Collections.Generic.IList[System_Collections_Immutable_ImmutableList_T], System.Collections.IList, System.Collections.Immutable.IStrongEnumerable[System_Collections_Immutable_ImmutableList_T, System_Collections_Immutable_ImmutableList_Enumerator], typing.Iterable[System_Collections_Immutable_ImmutableList_T]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Immutable_ImmutableList_T], System.Collections.Immutable.ISecurePooledObjectUser, System.Collections.Immutable.IStrongEnumerator[System_Collections_Immutable_ImmutableList_T]):
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableList_T:
            ...

        def dispose(self) -> None:
            ...

        def move_next(self) -> bool:
            ...

        def reset(self) -> None:
            ...

    class Builder(System.Object, System.Collections.Generic.IList[System_Collections_Immutable_ImmutableList_T], System.Collections.IList, System.Collections.Generic.IReadOnlyList[System_Collections_Immutable_ImmutableList_T], typing.Iterable[System_Collections_Immutable_ImmutableList_T]):
        """This class has no documentation."""

        @property
        def count(self) -> int:
            ...

        @property
        def convert_all(self) -> System.Collections.Immutable._ImmutableList.Builder_ConvertAll:
            ...

        def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableList_T:
            ...

        def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableList_T]:
            ...

        def __len__(self) -> int:
            ...

        def __setitem__(self, index: int, value: System_Collections_Immutable_ImmutableList_T) -> None:
            ...

        def add(self, item: System_Collections_Immutable_ImmutableList_T) -> None:
            ...

        def add_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def binary_search(self, item: System_Collections_Immutable_ImmutableList_T) -> int:
            ...

        @overload
        def binary_search(self, item: System_Collections_Immutable_ImmutableList_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
            ...

        @overload
        def binary_search(self, index: int, count: int, item: System_Collections_Immutable_ImmutableList_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System_Collections_Immutable_ImmutableList_T) -> bool:
            ...

        @overload
        def copy_to(self, array: typing.List[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def copy_to(self, array: typing.List[System_Collections_Immutable_ImmutableList_T], array_index: int) -> None:
            ...

        @overload
        def copy_to(self, index: int, array: typing.List[System_Collections_Immutable_ImmutableList_T], array_index: int, count: int) -> None:
            ...

        def exists(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> bool:
            ...

        def find(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System_Collections_Immutable_ImmutableList_T:
            ...

        def find_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
            ...

        @overload
        def find_index(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        @overload
        def find_index(self, start_index: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        @overload
        def find_index(self, start_index: int, count: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        def find_last(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System_Collections_Immutable_ImmutableList_T:
            ...

        @overload
        def find_last_index(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        @overload
        def find_last_index(self, start_index: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        @overload
        def find_last_index(self, start_index: int, count: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        def for_each(self, action: typing.Callable[[System_Collections_Immutable_ImmutableList_T], typing.Any]) -> None:
            ...

        def get_enumerator(self) -> System.Collections.Immutable.ImmutableList.Enumerator:
            ...

        def get_range(self, index: int, count: int) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableList_T) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableList_T, index: int) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableList_T, index: int, count: int) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableList_T, index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
            ...

        def insert(self, index: int, item: System_Collections_Immutable_ImmutableList_T) -> None:
            ...

        def insert_range(self, index: int, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        def item_ref(self, index: int) -> typing.Any:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableList_T) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableList_T, start_index: int) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableList_T, start_index: int, count: int) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableList_T, start_index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
            ...

        @overload
        def remove(self, item: System_Collections_Immutable_ImmutableList_T) -> bool:
            ...

        @overload
        def remove(self, item: System_Collections_Immutable_ImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> bool:
            ...

        def remove_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
            ...

        def remove_at(self, index: int) -> None:
            ...

        @overload
        def remove_range(self, index: int, count: int) -> None:
            ...

        @overload
        def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def replace(self, old_value: System_Collections_Immutable_ImmutableList_T, new_value: System_Collections_Immutable_ImmutableList_T) -> None:
            ...

        @overload
        def replace(self, old_value: System_Collections_Immutable_ImmutableList_T, new_value: System_Collections_Immutable_ImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def reverse(self) -> None:
            ...

        @overload
        def reverse(self, index: int, count: int) -> None:
            ...

        @overload
        def sort(self) -> None:
            ...

        @overload
        def sort(self, comparison: typing.Callable[[System_Collections_Immutable_ImmutableList_T, System_Collections_Immutable_ImmutableList_T], int]) -> None:
            ...

        @overload
        def sort(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        @overload
        def sort(self, index: int, count: int, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> None:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
            ...

        def true_for_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> bool:
            ...

    EMPTY: System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T] = ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def count(self) -> int:
        ...

    create: System.Collections.Immutable._ImmutableList_Create

    create_range: System.Collections.Immutable._ImmutableList_CreateRange

    create_builder: System.Collections.Immutable._ImmutableList_CreateBuilder

    to_immutable_list: System.Collections.Immutable._ImmutableList_ToImmutableList

    replace: System.Collections.Immutable._ImmutableList_Replace

    remove: System.Collections.Immutable._ImmutableList_Remove

    remove_range: System.Collections.Immutable._ImmutableList_RemoveRange

    index_of: System.Collections.Immutable._ImmutableList_IndexOf

    last_index_of: System.Collections.Immutable._ImmutableList_LastIndexOf

    @property
    def convert_all(self) -> System.Collections.Immutable._ImmutableList_ConvertAll:
        ...

    def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableList_T:
        ...

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableList_T]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, value: System_Collections_Immutable_ImmutableList_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def add_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def binary_search(self, item: System_Collections_Immutable_ImmutableList_T) -> int:
        ...

    @overload
    def binary_search(self, item: System_Collections_Immutable_ImmutableList_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
        ...

    @overload
    def binary_search(self, index: int, count: int, item: System_Collections_Immutable_ImmutableList_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> int:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def contains(self, value: System_Collections_Immutable_ImmutableList_T) -> bool:
        ...

    @overload
    def copy_to(self, array: typing.List[System_Collections_Immutable_ImmutableList_T]) -> None:
        ...

    @overload
    def copy_to(self, array: typing.List[System_Collections_Immutable_ImmutableList_T], array_index: int) -> None:
        ...

    @overload
    def copy_to(self, index: int, array: typing.List[System_Collections_Immutable_ImmutableList_T], array_index: int, count: int) -> None:
        ...

    def exists(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> bool:
        ...

    def find(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System_Collections_Immutable_ImmutableList_T:
        ...

    def find_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def find_index(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    @overload
    def find_index(self, start_index: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    @overload
    def find_index(self, start_index: int, count: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    def find_last(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System_Collections_Immutable_ImmutableList_T:
        ...

    @overload
    def find_last_index(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    @overload
    def find_last_index(self, start_index: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    @overload
    def find_last_index(self, start_index: int, count: int, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> int:
        ...

    def for_each(self, action: typing.Callable[[System_Collections_Immutable_ImmutableList_T], typing.Any]) -> None:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableList.Enumerator:
        ...

    def get_range(self, index: int, count: int) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def insert(self, index: int, item: System_Collections_Immutable_ImmutableList_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def insert_range(self, index: int, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def item_ref(self, index: int) -> typing.Any:
        ...

    def remove_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def remove_at(self, index: int) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def reverse(self) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def reverse(self, index: int, count: int) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def set_item(self, index: int, value: System_Collections_Immutable_ImmutableList_T) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def sort(self) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def sort(self, comparison: typing.Callable[[System_Collections_Immutable_ImmutableList_T, System_Collections_Immutable_ImmutableList_T], int]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def sort(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    @overload
    def sort(self, index: int, count: int, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableList_T]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_T]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableList.Builder:
        ...

    def true_for_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableList_T], bool]) -> bool:
        ...


class _Typed_ImmutableDictionary_Create(typing.Generic[System_Collections_Immutable_ImmutableDictionary_Create_TKey]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_Create_TKey, System_Collections_Immutable_ImmutableDictionary_Create_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_Create_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_Create_TKey, System_Collections_Immutable_ImmutableDictionary_Create_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_Create_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_Create_TValue]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_Create_TKey, System_Collections_Immutable_ImmutableDictionary_Create_TValue]:
        ...


class _ImmutableDictionary_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_Create_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_Create[System_Collections_Immutable_ImmutableDictionary_Create_TKey]:
        ...


class _Typed_ImmutableDictionary_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey], items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue], items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRange_TValue]:
        ...


class _ImmutableDictionary_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_CreateRange[System_Collections_Immutable_ImmutableDictionary_CreateRange_TKey]:
        ...


class _Typed_ImmutableDictionary_CreateRangeWithOverwrite(typing.Generic[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey]):
    """"""

    @overload
    def __call__(self, *items: typing.Union[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue]]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey], *items: typing.Union[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue]]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey, System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TValue]:
        ...


class _ImmutableDictionary_CreateRangeWithOverwrite:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_CreateRangeWithOverwrite[System_Collections_Immutable_ImmutableDictionary_CreateRangeWithOverwrite_TKey]:
        ...


class _Typed_ImmutableDictionary_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableDictionary.Builder:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey]) -> System.Collections.Immutable.ImmutableDictionary.Builder:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TValue]) -> System.Collections.Immutable.ImmutableDictionary.Builder:
        ...


class _ImmutableDictionary_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_CreateBuilder[System_Collections_Immutable_ImmutableDictionary_CreateBuilder_TKey]:
        ...


class _Typed_ImmutableDictionary_ToImmutableDictionary(typing.Generic[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue], key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableDictionary.Builder) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue], key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource], System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]], key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]], key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TValue]:
        ...


class _ImmutableDictionary_ToImmutableDictionary:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource]) -> System.Collections.Immutable._Typed_ImmutableDictionary_ToImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_ToImmutableDictionary_TSource]:
        ...


class _Typed_ImmutableDictionary_Contains(typing.Generic[System_Collections_Immutable_ImmutableDictionary_Contains_TKey]):
    """"""

    @overload
    def __call__(self, map: System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_Contains_TKey, System_Collections_Immutable_ImmutableDictionary_Contains_TValue], key: System_Collections_Immutable_ImmutableDictionary_Contains_TKey, value: System_Collections_Immutable_ImmutableDictionary_Contains_TValue) -> bool:
        ...


class _ImmutableDictionary_Contains:
    """"""

    @overload
    def __call__(self, pair: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]) -> bool:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_Contains_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_Contains[System_Collections_Immutable_ImmutableDictionary_Contains_TKey]:
        ...


class _Typed_ImmutableDictionary_GetValueOrDefault(typing.Generic[System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey]):
    """"""

    @overload
    def __call__(self, dictionary: System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey, System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue], key: System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey) -> System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue:
        ...

    @overload
    def __call__(self, dictionary: System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey, System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue], key: System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey, default_value: System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue) -> System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TValue:
        ...


class _ImmutableDictionary_GetValueOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey]) -> System.Collections.Immutable._Typed_ImmutableDictionary_GetValueOrDefault[System_Collections_Immutable_ImmutableDictionary_GetValueOrDefault_TKey]:
        ...


class ImmutableDictionary(typing.Generic[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Object, System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Collections.Immutable.IImmutableDictionaryInternal[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Collections.Generic.IDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]):
        """This class has no documentation."""

        @property
        def current(self) -> System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
            ...

        def dispose(self) -> None:
            ...

        def move_next(self) -> bool:
            ...

        def reset(self) -> None:
            ...

    class Builder(System.Object, System.Collections.Generic.IDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Collections.Generic.IReadOnlyDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]):
        """This class has no documentation."""

        @property
        def key_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TKey]:
            ...

        @key_comparer.setter
        def key_comparer(self, value: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TKey]) -> None:
            ...

        @property
        def value_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TValue]:
            ...

        @value_comparer.setter
        def value_comparer(self, value: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TValue]) -> None:
            ...

        @property
        def count(self) -> int:
            ...

        @property
        def keys(self) -> typing.Iterable[System_Collections_Immutable_ImmutableDictionary_TKey]:
            ...

        @property
        def values(self) -> typing.Iterable[System_Collections_Immutable_ImmutableDictionary_TValue]:
            ...

        def __contains__(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> bool:
            ...

        def __getitem__(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> System_Collections_Immutable_ImmutableDictionary_TValue:
            ...

        def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]:
            ...

        def __len__(self) -> int:
            ...

        def __setitem__(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> None:
            ...

        @overload
        def add(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> None:
            ...

        @overload
        def add(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]) -> None:
            ...

        def add_range(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]) -> None:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]) -> bool:
            ...

        def contains_key(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> bool:
            ...

        def contains_value(self, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> bool:
            ...

        def get_enumerator(self) -> System.Collections.Immutable.ImmutableDictionary.Enumerator:
            ...

        @overload
        def get_value_or_default(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> System_Collections_Immutable_ImmutableDictionary_TValue:
            ...

        @overload
        def get_value_or_default(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, default_value: System_Collections_Immutable_ImmutableDictionary_TValue) -> System_Collections_Immutable_ImmutableDictionary_TValue:
            ...

        @overload
        def remove(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> bool:
            ...

        @overload
        def remove(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]) -> bool:
            ...

        def remove_range(self, keys: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_TKey]) -> None:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
            ...

        def try_get_key(self, equal_key: System_Collections_Immutable_ImmutableDictionary_TKey, actual_key: typing.Optional[System_Collections_Immutable_ImmutableDictionary_TKey]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableDictionary_TKey]:
            ...

        def try_get_value(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: typing.Optional[System_Collections_Immutable_ImmutableDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableDictionary_TValue]:
            ...

    EMPTY: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue] = ...

    @property
    def count(self) -> int:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def key_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TKey]:
        ...

    @property
    def value_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    @property
    def keys(self) -> typing.Iterable[System_Collections_Immutable_ImmutableDictionary_TKey]:
        ...

    @property
    def values(self) -> typing.Iterable[System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    create: System.Collections.Immutable._ImmutableDictionary_Create

    create_range: System.Collections.Immutable._ImmutableDictionary_CreateRange

    create_range_with_overwrite: System.Collections.Immutable._ImmutableDictionary_CreateRangeWithOverwrite

    create_builder: System.Collections.Immutable._ImmutableDictionary_CreateBuilder

    to_immutable_dictionary: System.Collections.Immutable._ImmutableDictionary_ToImmutableDictionary

    contains: System.Collections.Immutable._ImmutableDictionary_Contains

    get_value_or_default: System.Collections.Immutable._ImmutableDictionary_GetValueOrDefault

    def __contains__(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> bool:
        ...

    def __getitem__(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> System_Collections_Immutable_ImmutableDictionary_TValue:
        ...

    def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def add_range(self, pairs: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def contains_key(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> bool:
        ...

    def contains_value(self, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> bool:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableDictionary.Enumerator:
        ...

    def remove(self, key: System_Collections_Immutable_ImmutableDictionary_TKey) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def remove_range(self, keys: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def set_item(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: System_Collections_Immutable_ImmutableDictionary_TValue) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def set_items(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableDictionary.Builder:
        ...

    def try_get_key(self, equal_key: System_Collections_Immutable_ImmutableDictionary_TKey, actual_key: typing.Optional[System_Collections_Immutable_ImmutableDictionary_TKey]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableDictionary_TKey]:
        ...

    def try_get_value(self, key: System_Collections_Immutable_ImmutableDictionary_TKey, value: typing.Optional[System_Collections_Immutable_ImmutableDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    @overload
    def with_comparers(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TValue]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...

    @overload
    def with_comparers(self, key_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableDictionary_TKey]) -> System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableDictionary_TKey, System_Collections_Immutable_ImmutableDictionary_TValue]:
        ...


class _Typed_ImmutableSortedSet_Create(typing.Generic[System_Collections_Immutable_ImmutableSortedSet_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_Create_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableSortedSet_Create_T) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_Create_T], item: System_Collections_Immutable_ImmutableSortedSet_Create_T) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableSortedSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_Create_T]]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableSortedSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_Create_T]]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_Create_T], *items: typing.Union[System_Collections_Immutable_ImmutableSortedSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_Create_T]]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_Create_T], *items: typing.Union[System_Collections_Immutable_ImmutableSortedSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_Create_T]]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...


class _ImmutableSortedSet_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedSet_Create_T]) -> System.Collections.Immutable._Typed_ImmutableSortedSet_Create[System_Collections_Immutable_ImmutableSortedSet_Create_T]:
        ...


class _Typed_ImmutableSortedSet_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T], items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]:
        ...


class _ImmutableSortedSet_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableSortedSet_CreateRange[System_Collections_Immutable_ImmutableSortedSet_CreateRange_T]:
        ...


class _Typed_ImmutableSortedSet_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableSortedSet.Builder:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T]) -> System.Collections.Immutable.ImmutableSortedSet.Builder:
        ...


class _ImmutableSortedSet_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T]) -> System.Collections.Immutable._Typed_ImmutableSortedSet_CreateBuilder[System_Collections_Immutable_ImmutableSortedSet_CreateBuilder_T]:
        ...


class _Typed_ImmutableSortedSet_ToImmutableSortedSet(typing.Generic[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource], comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableSortedSet.Builder) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]:
        ...


class _ImmutableSortedSet_ToImmutableSortedSet:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]) -> System.Collections.Immutable._Typed_ImmutableSortedSet_ToImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_ToImmutableSortedSet_TSource]:
        ...


class ImmutableSortedSet(typing.Generic[System_Collections_Immutable_ImmutableSortedSet_T], System.Object, System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.Generic.IReadOnlyList[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.Generic.IList[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.Generic.ISet[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.IList, System.Collections.Immutable.IStrongEnumerable[System_Collections_Immutable_ImmutableSortedSet_T, System_Collections_Immutable_ImmutableSortedSet_Enumerator], typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_T]):
    """This class has no documentation."""

    class Builder(System.Object, System.Collections.Generic.IReadOnlyCollection[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.Generic.ISet[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.ICollection, typing.Iterable[System_Collections_Immutable_ImmutableSortedSet_T]):
        """This class has no documentation."""

        @property
        def count(self) -> int:
            ...

        @property
        def max(self) -> System_Collections_Immutable_ImmutableSortedSet_T:
            ...

        @property
        def min(self) -> System_Collections_Immutable_ImmutableSortedSet_T:
            ...

        @property
        def key_comparer(self) -> System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_T]:
            ...

        @key_comparer.setter
        def key_comparer(self, value: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_T]) -> None:
            ...

        def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableSortedSet_T:
            ...

        def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableSortedSet_T]:
            ...

        def __len__(self) -> int:
            ...

        def add(self, item: System_Collections_Immutable_ImmutableSortedSet_T) -> bool:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System_Collections_Immutable_ImmutableSortedSet_T) -> bool:
            ...

        def except_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> None:
            ...

        def get_enumerator(self) -> System.Collections.Immutable.ImmutableSortedSet.Enumerator:
            ...

        def index_of(self, item: System_Collections_Immutable_ImmutableSortedSet_T) -> int:
            ...

        def intersect_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> None:
            ...

        def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def item_ref(self, index: int) -> typing.Any:
            ...

        def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def remove(self, item: System_Collections_Immutable_ImmutableSortedSet_T) -> bool:
            ...

        def reverse(self) -> System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]:
            ...

        def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
            ...

        def symmetric_except_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> None:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
            ...

        def try_get_value(self, equal_value: System_Collections_Immutable_ImmutableSortedSet_T, actual_value: typing.Optional[System_Collections_Immutable_ImmutableSortedSet_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedSet_T]:
            ...

        def union_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> None:
            ...

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Immutable_ImmutableSortedSet_T], System.Collections.Immutable.ISecurePooledObjectUser, System.Collections.Immutable.IStrongEnumerator[System_Collections_Immutable_ImmutableSortedSet_T]):
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableSortedSet_T:
            ...

        def dispose(self) -> None:
            ...

        def move_next(self) -> bool:
            ...

        def reset(self) -> None:
            ...

    EMPTY: System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T] = ...

    @property
    def max(self) -> System_Collections_Immutable_ImmutableSortedSet_T:
        ...

    @property
    def min(self) -> System_Collections_Immutable_ImmutableSortedSet_T:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def count(self) -> int:
        ...

    @property
    def key_comparer(self) -> System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    create: System.Collections.Immutable._ImmutableSortedSet_Create

    create_range: System.Collections.Immutable._ImmutableSortedSet_CreateRange

    create_builder: System.Collections.Immutable._ImmutableSortedSet_CreateBuilder

    to_immutable_sorted_set: System.Collections.Immutable._ImmutableSortedSet_ToImmutableSortedSet

    def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableSortedSet_T:
        ...

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, value: System_Collections_Immutable_ImmutableSortedSet_T) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def contains(self, value: System_Collections_Immutable_ImmutableSortedSet_T) -> bool:
        ...

    def Except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableSortedSet.Enumerator:
        ...

    def index_of(self, item: System_Collections_Immutable_ImmutableSortedSet_T) -> int:
        ...

    def intersect(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def item_ref(self, index: int) -> typing.Any:
        ...

    def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def remove(self, value: System_Collections_Immutable_ImmutableSortedSet_T) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def reverse(self) -> System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> bool:
        ...

    def symmetric_except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableSortedSet.Builder:
        ...

    def try_get_value(self, equal_value: System_Collections_Immutable_ImmutableSortedSet_T, actual_value: typing.Optional[System_Collections_Immutable_ImmutableSortedSet_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def union(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedSet_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...

    def with_comparer(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedSet_T]) -> System.Collections.Immutable.ImmutableSortedSet[System_Collections_Immutable_ImmutableSortedSet_T]:
        ...


class _Typed_ImmutableHashSet_Create(typing.Generic[System_Collections_Immutable_ImmutableHashSet_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_Create_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableHashSet_Create_T) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_Create_T], item: System_Collections_Immutable_ImmutableHashSet_Create_T) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableHashSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableHashSet_Create_T]]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableHashSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableHashSet_Create_T]]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_Create_T], *items: typing.Union[System_Collections_Immutable_ImmutableHashSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableHashSet_Create_T]]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_Create_T], *items: typing.Union[System_Collections_Immutable_ImmutableHashSet_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableHashSet_Create_T]]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...


class _ImmutableHashSet_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableHashSet_Create_T]) -> System.Collections.Immutable._Typed_ImmutableHashSet_Create[System_Collections_Immutable_ImmutableHashSet_Create_T]:
        ...


class _Typed_ImmutableHashSet_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_CreateRange_T], items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]:
        ...


class _ImmutableHashSet_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableHashSet_CreateRange[System_Collections_Immutable_ImmutableHashSet_CreateRange_T]:
        ...


class _Typed_ImmutableHashSet_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableHashSet.Builder:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T]) -> System.Collections.Immutable.ImmutableHashSet.Builder:
        ...


class _ImmutableHashSet_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T]) -> System.Collections.Immutable._Typed_ImmutableHashSet_CreateBuilder[System_Collections_Immutable_ImmutableHashSet_CreateBuilder_T]:
        ...


class _Typed_ImmutableHashSet_ToImmutableHashSet(typing.Generic[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableHashSet.Builder) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]:
        ...


class _ImmutableHashSet_ToImmutableHashSet:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]) -> System.Collections.Immutable._Typed_ImmutableHashSet_ToImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_ToImmutableHashSet_TSource]:
        ...


class ImmutableHashSet(typing.Generic[System_Collections_Immutable_ImmutableHashSet_T], System.Object, System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_ImmutableHashSet_T], System.Collections.Generic.ISet[System_Collections_Immutable_ImmutableHashSet_T], System.Collections.ICollection, System.Collections.Immutable.IStrongEnumerable[System_Collections_Immutable_ImmutableHashSet_T, System_Collections_Immutable_ImmutableHashSet_Enumerator], typing.Iterable[System_Collections_Immutable_ImmutableHashSet_T]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Immutable_ImmutableHashSet_T], System.Collections.Immutable.IStrongEnumerator[System_Collections_Immutable_ImmutableHashSet_T]):
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableHashSet_T:
            ...

        def dispose(self) -> None:
            ...

        def move_next(self) -> bool:
            ...

        def reset(self) -> None:
            ...

    class Builder(System.Object, System.Collections.Generic.IReadOnlyCollection[System_Collections_Immutable_ImmutableHashSet_T], System.Collections.Generic.ISet[System_Collections_Immutable_ImmutableHashSet_T], typing.Iterable[System_Collections_Immutable_ImmutableHashSet_T]):
        """This class has no documentation."""

        @property
        def count(self) -> int:
            ...

        @property
        def key_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_T]:
            ...

        @key_comparer.setter
        def key_comparer(self, value: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_T]) -> None:
            ...

        def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableHashSet_T]:
            ...

        def __len__(self) -> int:
            ...

        def add(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> bool:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> bool:
            ...

        def except_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> None:
            ...

        def get_enumerator(self) -> System.Collections.Immutable.ImmutableHashSet.Enumerator:
            ...

        def intersect_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> None:
            ...

        def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def remove(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> bool:
            ...

        def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
            ...

        def symmetric_except_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> None:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
            ...

        def try_get_value(self, equal_value: System_Collections_Immutable_ImmutableHashSet_T, actual_value: typing.Optional[System_Collections_Immutable_ImmutableHashSet_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableHashSet_T]:
            ...

        def union_with(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> None:
            ...

    EMPTY: System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T] = ...

    @property
    def count(self) -> int:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def key_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    create: System.Collections.Immutable._ImmutableHashSet_Create

    create_range: System.Collections.Immutable._ImmutableHashSet_CreateRange

    create_builder: System.Collections.Immutable._ImmutableHashSet_CreateBuilder

    to_immutable_hash_set: System.Collections.Immutable._ImmutableHashSet_ToImmutableHashSet

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def contains(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> bool:
        ...

    def Except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableHashSet.Enumerator:
        ...

    def intersect(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def remove(self, item: System_Collections_Immutable_ImmutableHashSet_T) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> bool:
        ...

    def symmetric_except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableHashSet.Builder:
        ...

    def try_get_value(self, equal_value: System_Collections_Immutable_ImmutableHashSet_T, actual_value: typing.Optional[System_Collections_Immutable_ImmutableHashSet_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def union(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableHashSet_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...

    def with_comparer(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableHashSet_T]) -> System.Collections.Immutable.ImmutableHashSet[System_Collections_Immutable_ImmutableHashSet_T]:
        ...


class _Typed_ImmutableArray_CastUp(typing.Generic[System_Collections_Immutable_ImmutableArray_CastUp_TDerived]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CastUp_TDerived]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...


class _ImmutableArray_CastUp:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_CastUp_TDerived]) -> System.Collections.Immutable._Typed_ImmutableArray_CastUp[System_Collections_Immutable_ImmutableArray_CastUp_TDerived]:
        ...


class _Typed_ImmutableArray_CastArray(typing.Generic[System_Collections_Immutable_ImmutableArray_CastArray_TOther]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CastArray_TOther]:
        ...


class _ImmutableArray_CastArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_CastArray_TOther]) -> System.Collections.Immutable._Typed_ImmutableArray_CastArray[System_Collections_Immutable_ImmutableArray_CastArray_TOther]:
        ...


class _Typed_ImmutableArray_As(typing.Generic[System_Collections_Immutable_ImmutableArray_As_TOther]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_As_TOther]:
        ...


class _ImmutableArray_As:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_As_TOther]) -> System.Collections.Immutable._Typed_ImmutableArray_As[System_Collections_Immutable_ImmutableArray_As_TOther]:
        ...


class _Typed_ImmutableArray_AddRange(typing.Generic[System_Collections_Immutable_ImmutableArray_AddRange_TDerived]):
    """"""

    @overload
    def __call__(self, items: typing.List[System_Collections_Immutable_ImmutableArray_AddRange_TDerived]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_AddRange_TDerived]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...


class _ImmutableArray_AddRange:
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: typing.List[System_Collections_Immutable_ImmutableArray_T], length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T], length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableArray_T, typing.Iterable[System_Collections_Immutable_ImmutableArray_T]]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_AddRange_TDerived]) -> System.Collections.Immutable._Typed_ImmutableArray_AddRange[System_Collections_Immutable_ImmutableArray_AddRange_TDerived]:
        ...


class _Typed_ImmutableArray_OfType(typing.Generic[System_Collections_Immutable_ImmutableArray_OfType_TResult]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_OfType_TResult]:
        ...


class _ImmutableArray_OfType:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_OfType_TResult]) -> System.Collections.Immutable._Typed_ImmutableArray_OfType[System_Collections_Immutable_ImmutableArray_OfType_TResult]:
        ...


class _Typed_ImmutableArray_Create(typing.Generic[System_Collections_Immutable_ImmutableArray_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableArray_Create_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, item_1: System_Collections_Immutable_ImmutableArray_Create_T, item_2: System_Collections_Immutable_ImmutableArray_Create_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, item_1: System_Collections_Immutable_ImmutableArray_Create_T, item_2: System_Collections_Immutable_ImmutableArray_Create_T, item_3: System_Collections_Immutable_ImmutableArray_Create_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, item_1: System_Collections_Immutable_ImmutableArray_Create_T, item_2: System_Collections_Immutable_ImmutableArray_Create_T, item_3: System_Collections_Immutable_ImmutableArray_Create_T, item_4: System_Collections_Immutable_ImmutableArray_Create_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableArray_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableArray_Create_T]]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, items: System.Span[System_Collections_Immutable_ImmutableArray_Create_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableArray_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableArray_Create_T]]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, items: typing.List[System_Collections_Immutable_ImmutableArray_Create_T], start: int, length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T], start: int, length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...


class _ImmutableArray_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_Create_T]) -> System.Collections.Immutable._Typed_ImmutableArray_Create[System_Collections_Immutable_ImmutableArray_Create_T]:
        ...


class _Typed_ImmutableArray_ToImmutableArray(typing.Generic[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]):
    """"""

    @overload
    def __call__(self, items: System.ReadOnlySpan[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: System.Span[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_ToImmutableArray_TSource]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_ToImmutableArray_TSource]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_ToImmutableArray_TSource]:
        ...


class _ImmutableArray_ToImmutableArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]) -> System.Collections.Immutable._Typed_ImmutableArray_ToImmutableArray[System_Collections_Immutable_ImmutableArray_ToImmutableArray_T]:
        ...


class _Typed_ImmutableArray_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableArray_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_CreateRange_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_T]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], selector: typing.Callable[[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], System_Collections_Immutable_ImmutableArray_CreateRange_TResult]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TResult]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], start: int, length: int, selector: typing.Callable[[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], System_Collections_Immutable_ImmutableArray_CreateRange_TResult]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TResult]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], selector: typing.Callable[[System_Collections_Immutable_ImmutableArray_CreateRange_TSource, System_Collections_Immutable_ImmutableArray_CreateRange_TArg], System_Collections_Immutable_ImmutableArray_CreateRange_TResult], arg: System_Collections_Immutable_ImmutableArray_CreateRange_TArg) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TResult]:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TSource], start: int, length: int, selector: typing.Callable[[System_Collections_Immutable_ImmutableArray_CreateRange_TSource, System_Collections_Immutable_ImmutableArray_CreateRange_TArg], System_Collections_Immutable_ImmutableArray_CreateRange_TResult], arg: System_Collections_Immutable_ImmutableArray_CreateRange_TArg) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_CreateRange_TResult]:
        ...


class _ImmutableArray_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableArray_CreateRange[System_Collections_Immutable_ImmutableArray_CreateRange_T]:
        ...


class _Typed_ImmutableArray_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableArray_CreateBuilder_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableArray.Builder:
        ...

    @overload
    def __call__(self, initial_capacity: int) -> System.Collections.Immutable.ImmutableArray.Builder:
        ...


class _ImmutableArray_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_CreateBuilder_T]) -> System.Collections.Immutable._Typed_ImmutableArray_CreateBuilder[System_Collections_Immutable_ImmutableArray_CreateBuilder_T]:
        ...


class _Typed_ImmutableArray_BinarySearch(typing.Generic[System_Collections_Immutable_ImmutableArray_BinarySearch_T]):
    """"""

    @overload
    def __call__(self, array: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_BinarySearch_T], value: System_Collections_Immutable_ImmutableArray_BinarySearch_T) -> int:
        ...

    @overload
    def __call__(self, array: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_BinarySearch_T], value: System_Collections_Immutable_ImmutableArray_BinarySearch_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_BinarySearch_T]) -> int:
        ...

    @overload
    def __call__(self, array: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_BinarySearch_T], index: int, length: int, value: System_Collections_Immutable_ImmutableArray_BinarySearch_T) -> int:
        ...

    @overload
    def __call__(self, array: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_BinarySearch_T], index: int, length: int, value: System_Collections_Immutable_ImmutableArray_BinarySearch_T, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_BinarySearch_T]) -> int:
        ...


class _ImmutableArray_BinarySearch:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_BinarySearch_T]) -> System.Collections.Immutable._Typed_ImmutableArray_BinarySearch[System_Collections_Immutable_ImmutableArray_BinarySearch_T]:
        ...


class ImmutableArray(typing.Generic[System_Collections_Immutable_ImmutableArray_T], System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T], System.IEquatable[System_Collections_Immutable_ImmutableArray], System.Collections.Immutable.IImmutableArray, System.Collections.Generic.IList[System_Collections_Immutable_ImmutableArray_T], System.Collections.IList, System.Collections.IStructuralComparable, System.Collections.IStructuralEquatable, System.Collections.Immutable.IImmutableList[System_Collections_Immutable_ImmutableArray_T], typing.Iterable[System_Collections_Immutable_ImmutableArray_T]):
    """This class has no documentation."""

    class Builder(System.Object, System.Collections.Generic.IList[System_Collections_Immutable_ImmutableArray_T], System.Collections.Generic.IReadOnlyList[System_Collections_Immutable_ImmutableArray_T], typing.Iterable[System_Collections_Immutable_ImmutableArray_T]):
        """This class has no documentation."""

        @property
        def capacity(self) -> int:
            ...

        @capacity.setter
        def capacity(self, value: int) -> None:
            ...

        @property
        def count(self) -> int:
            ...

        @count.setter
        def count(self, value: int) -> None:
            ...

        @property
        def add_range(self) -> System.Collections.Immutable._ImmutableArray.Builder_AddRange:
            ...

        def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableArray_T:
            ...

        def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableArray_T]:
            ...

        def __len__(self) -> int:
            ...

        def __setitem__(self, index: int, value: System_Collections_Immutable_ImmutableArray_T) -> None:
            ...

        def add(self, item: System_Collections_Immutable_ImmutableArray_T) -> None:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System_Collections_Immutable_ImmutableArray_T) -> bool:
            ...

        @overload
        def copy_to(self, array: typing.List[System_Collections_Immutable_ImmutableArray_T], index: int) -> None:
            ...

        @overload
        def copy_to(self, destination: typing.List[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        @overload
        def copy_to(self, source_index: int, destination: typing.List[System_Collections_Immutable_ImmutableArray_T], destination_index: int, length: int) -> None:
            ...

        @overload
        def copy_to(self, destination: System.Span[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        def drain_to_immutable(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
            ...

        def get_enumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Immutable_ImmutableArray_T]:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableArray_T) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
            ...

        @overload
        def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
            ...

        def insert(self, index: int, item: System_Collections_Immutable_ImmutableArray_T) -> None:
            ...

        @overload
        def insert_range(self, index: int, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        @overload
        def insert_range(self, index: int, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        def item_ref(self, index: int) -> typing.Any:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int) -> int:
            ...

        @overload
        def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
            ...

        def move_to_immutable(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
            ...

        @overload
        def remove(self, element: System_Collections_Immutable_ImmutableArray_T) -> bool:
            ...

        @overload
        def remove(self, element: System_Collections_Immutable_ImmutableArray_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> bool:
            ...

        def remove_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableArray_T], bool]) -> None:
            ...

        def remove_at(self, index: int) -> None:
            ...

        @overload
        def remove_range(self, index: int, length: int) -> None:
            ...

        @overload
        def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        @overload
        def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        @overload
        def replace(self, old_value: System_Collections_Immutable_ImmutableArray_T, new_value: System_Collections_Immutable_ImmutableArray_T) -> None:
            ...

        @overload
        def replace(self, old_value: System_Collections_Immutable_ImmutableArray_T, new_value: System_Collections_Immutable_ImmutableArray_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        def reverse(self) -> None:
            ...

        @overload
        def sort(self) -> None:
            ...

        @overload
        def sort(self, comparison: typing.Callable[[System_Collections_Immutable_ImmutableArray_T, System_Collections_Immutable_ImmutableArray_T], int]) -> None:
            ...

        @overload
        def sort(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        @overload
        def sort(self, index: int, count: int, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_T]) -> None:
            ...

        def to_array(self) -> typing.List[System_Collections_Immutable_ImmutableArray_T]:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
            ...

    class Enumerator:
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableArray_T:
            ...

        def move_next(self) -> bool:
            ...

    EMPTY: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T] = ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def length(self) -> int:
        ...

    @property
    def is_default(self) -> bool:
        ...

    @property
    def is_default_or_empty(self) -> bool:
        ...

    cast_up: System.Collections.Immutable._ImmutableArray_CastUp

    @property
    def cast_array(self) -> System.Collections.Immutable._ImmutableArray_CastArray:
        ...

    @property
    def As(self) -> System.Collections.Immutable._ImmutableArray_As:
        ...

    @property
    def add_range(self) -> System.Collections.Immutable._ImmutableArray_AddRange:
        ...

    @property
    def of_type(self) -> System.Collections.Immutable._ImmutableArray_OfType:
        ...

    create: System.Collections.Immutable._ImmutableArray_Create

    to_immutable_array: System.Collections.Immutable._ImmutableArray_ToImmutableArray

    create_range: System.Collections.Immutable._ImmutableArray_CreateRange

    create_builder: System.Collections.Immutable._ImmutableArray_CreateBuilder

    binary_search: System.Collections.Immutable._ImmutableArray_BinarySearch

    @overload
    def __eq__(self, right: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> bool:
        ...

    @overload
    def __eq__(self, right: typing.Optional[System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]]) -> bool:
        ...

    def __getitem__(self, index: int) -> System_Collections_Immutable_ImmutableArray_T:
        ...

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def __ne__(self, right: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> bool:
        ...

    @overload
    def __ne__(self, right: typing.Optional[System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]]) -> bool:
        ...

    def add(self, item: System_Collections_Immutable_ImmutableArray_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def as_memory(self) -> System.ReadOnlyMemory[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def as_span(self, range: System.Range) -> System.ReadOnlySpan[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def as_span(self) -> System.ReadOnlySpan[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def as_span(self, start: int, length: int) -> System.ReadOnlySpan[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def contains(self, item: System_Collections_Immutable_ImmutableArray_T) -> bool:
        ...

    @overload
    def contains(self, item: System_Collections_Immutable_ImmutableArray_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> bool:
        ...

    @overload
    def copy_to(self, destination: typing.List[System_Collections_Immutable_ImmutableArray_T]) -> None:
        ...

    @overload
    def copy_to(self, destination: typing.List[System_Collections_Immutable_ImmutableArray_T], destination_index: int) -> None:
        ...

    @overload
    def copy_to(self, source_index: int, destination: typing.List[System_Collections_Immutable_ImmutableArray_T], destination_index: int, length: int) -> None:
        ...

    @overload
    def copy_to(self, destination: System.Span[System_Collections_Immutable_ImmutableArray_T]) -> None:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> bool:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableArray.Enumerator:
        ...

    def get_hash_code(self) -> int:
        ...

    @overload
    def index_of(self, item: System_Collections_Immutable_ImmutableArray_T) -> int:
        ...

    @overload
    def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
        ...

    @overload
    def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int) -> int:
        ...

    @overload
    def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int) -> int:
        ...

    @overload
    def index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
        ...

    def insert(self, index: int, item: System_Collections_Immutable_ImmutableArray_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def insert_range(self, index: int, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def insert_range(self, index: int, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def insert_range(self, index: int, items: typing.List[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def insert_range(self, index: int, *items: typing.Union[System_Collections_Immutable_ImmutableArray_T, typing.Iterable[System_Collections_Immutable_ImmutableArray_T]]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def item_ref(self, index: int) -> typing.Any:
        ...

    @overload
    def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T) -> int:
        ...

    @overload
    def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int) -> int:
        ...

    @overload
    def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int) -> int:
        ...

    @overload
    def last_index_of(self, item: System_Collections_Immutable_ImmutableArray_T, start_index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> int:
        ...

    @overload
    def remove(self, item: System_Collections_Immutable_ImmutableArray_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove(self, item: System_Collections_Immutable_ImmutableArray_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def remove_all(self, match: typing.Callable[[System_Collections_Immutable_ImmutableArray_T], bool]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def remove_at(self, index: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, index: int, length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: System.ReadOnlySpan[System_Collections_Immutable_ImmutableArray_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T] = None) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def remove_range(self, items: typing.List[System_Collections_Immutable_ImmutableArray_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T] = None) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def replace(self, old_value: System_Collections_Immutable_ImmutableArray_T, new_value: System_Collections_Immutable_ImmutableArray_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def replace(self, old_value: System_Collections_Immutable_ImmutableArray_T, new_value: System_Collections_Immutable_ImmutableArray_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def set_item(self, index: int, item: System_Collections_Immutable_ImmutableArray_T) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def slice(self, start: int, length: int) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def sort(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def sort(self, comparison: typing.Callable[[System_Collections_Immutable_ImmutableArray_T, System_Collections_Immutable_ImmutableArray_T], int]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def sort(self, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    @overload
    def sort(self, index: int, count: int, comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableArray.Builder:
        ...


class _Typed_ImmutableQueue_Create(typing.Generic[System_Collections_Immutable_ImmutableQueue_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableQueue_Create_T) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableQueue_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableQueue_Create_T]]) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableQueue_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableQueue_Create_T]]) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_Create_T]:
        ...


class _ImmutableQueue_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableQueue_Create_T]) -> System.Collections.Immutable._Typed_ImmutableQueue_Create[System_Collections_Immutable_ImmutableQueue_Create_T]:
        ...


class _Typed_ImmutableQueue_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableQueue_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableQueue_CreateRange_T]) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_CreateRange_T]:
        ...


class _ImmutableQueue_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableQueue_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableQueue_CreateRange[System_Collections_Immutable_ImmutableQueue_CreateRange_T]:
        ...


class _Typed_ImmutableQueue_Dequeue(typing.Generic[System_Collections_Immutable_ImmutableQueue_Dequeue_T]):
    """"""

    @overload
    def __call__(self, queue: System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_ImmutableQueue_Dequeue_T], value: typing.Optional[System_Collections_Immutable_ImmutableQueue_Dequeue_T]) -> typing.Tuple[System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_ImmutableQueue_Dequeue_T], System_Collections_Immutable_ImmutableQueue_Dequeue_T]:
        ...


class _ImmutableQueue_Dequeue:
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_T]:
        ...

    @overload
    def __call__(self, value: typing.Optional[System_Collections_Immutable_ImmutableQueue_T]) -> typing.Tuple[System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_T], System_Collections_Immutable_ImmutableQueue_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableQueue_Dequeue_T]) -> System.Collections.Immutable._Typed_ImmutableQueue_Dequeue[System_Collections_Immutable_ImmutableQueue_Dequeue_T]:
        ...


class ImmutableQueue(typing.Generic[System_Collections_Immutable_ImmutableQueue_T], System.Object, System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_ImmutableQueue_T], typing.Iterable[System_Collections_Immutable_ImmutableQueue_T]):
    """This class has no documentation."""

    class Enumerator:
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableQueue_T:
            ...

        def move_next(self) -> bool:
            ...

    @property
    def is_empty(self) -> bool:
        ...

    EMPTY: System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_T]

    create: System.Collections.Immutable._ImmutableQueue_Create

    create_range: System.Collections.Immutable._ImmutableQueue_CreateRange

    dequeue: System.Collections.Immutable._ImmutableQueue_Dequeue

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableQueue_T]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_T]:
        ...

    def enqueue(self, value: System_Collections_Immutable_ImmutableQueue_T) -> System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableQueue_T]:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableQueue.Enumerator:
        ...

    def peek(self) -> System_Collections_Immutable_ImmutableQueue_T:
        ...

    def peek_ref(self) -> typing.Any:
        ...


class IImmutableStack(typing.Generic[System_Collections_Immutable_IImmutableStack_T], System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableStack_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def is_empty(self) -> bool:
        ...

    def clear(self) -> System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_IImmutableStack_T]:
        ...

    def peek(self) -> System_Collections_Immutable_IImmutableStack_T:
        ...

    def pop(self) -> System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_IImmutableStack_T]:
        ...

    def push(self, value: System_Collections_Immutable_IImmutableStack_T) -> System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_IImmutableStack_T]:
        ...


class _Typed_ImmutableStack_Create(typing.Generic[System_Collections_Immutable_ImmutableStack_Create_T]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_Create_T]:
        ...

    @overload
    def __call__(self, item: System_Collections_Immutable_ImmutableStack_Create_T) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableStack_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableStack_Create_T]]) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_Create_T]:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableStack_Create_T, typing.Iterable[System_Collections_Immutable_ImmutableStack_Create_T]]) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_Create_T]:
        ...


class _ImmutableStack_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableStack_Create_T]) -> System.Collections.Immutable._Typed_ImmutableStack_Create[System_Collections_Immutable_ImmutableStack_Create_T]:
        ...


class _Typed_ImmutableStack_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableStack_CreateRange_T]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableStack_CreateRange_T]) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_CreateRange_T]:
        ...


class _ImmutableStack_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableStack_CreateRange_T]) -> System.Collections.Immutable._Typed_ImmutableStack_CreateRange[System_Collections_Immutable_ImmutableStack_CreateRange_T]:
        ...


class _Typed_ImmutableStack_Pop(typing.Generic[System_Collections_Immutable_ImmutableStack_Pop_T]):
    """"""

    @overload
    def __call__(self, stack: System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_ImmutableStack_Pop_T], value: typing.Optional[System_Collections_Immutable_ImmutableStack_Pop_T]) -> typing.Tuple[System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_ImmutableStack_Pop_T], System_Collections_Immutable_ImmutableStack_Pop_T]:
        ...


class _ImmutableStack_Pop:
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_T]:
        ...

    @overload
    def __call__(self, value: typing.Optional[System_Collections_Immutable_ImmutableStack_T]) -> typing.Tuple[System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_T], System_Collections_Immutable_ImmutableStack_T]:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableStack_Pop_T]) -> System.Collections.Immutable._Typed_ImmutableStack_Pop[System_Collections_Immutable_ImmutableStack_Pop_T]:
        ...


class ImmutableStack(typing.Generic[System_Collections_Immutable_ImmutableStack_T], System.Object, System.Collections.Immutable.IImmutableStack[System_Collections_Immutable_ImmutableStack_T], typing.Iterable[System_Collections_Immutable_ImmutableStack_T]):
    """This class has no documentation."""

    class Enumerator:
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Immutable_ImmutableStack_T:
            ...

        def move_next(self) -> bool:
            ...

    EMPTY: System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_T]

    @property
    def is_empty(self) -> bool:
        ...

    create: System.Collections.Immutable._ImmutableStack_Create

    create_range: System.Collections.Immutable._ImmutableStack_CreateRange

    pop: System.Collections.Immutable._ImmutableStack_Pop

    def __iter__(self) -> typing.Iterator[System_Collections_Immutable_ImmutableStack_T]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_T]:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableStack.Enumerator:
        ...

    def peek(self) -> System_Collections_Immutable_ImmutableStack_T:
        ...

    def peek_ref(self) -> typing.Any:
        ...

    def push(self, value: System_Collections_Immutable_ImmutableStack_T) -> System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableStack_T]:
        ...


class IImmutableSet(typing.Generic[System_Collections_Immutable_IImmutableSet_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Immutable_IImmutableSet_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def add(self, value: System_Collections_Immutable_IImmutableSet_T) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def clear(self) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def contains(self, value: System_Collections_Immutable_IImmutableSet_T) -> bool:
        ...

    def Except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def intersect(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def remove(self, value: System_Collections_Immutable_IImmutableSet_T) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> bool:
        ...

    def symmetric_except(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...

    def try_get_value(self, equal_value: System_Collections_Immutable_IImmutableSet_T, actual_value: typing.Optional[System_Collections_Immutable_IImmutableSet_T]) -> typing.Tuple[bool, System_Collections_Immutable_IImmutableSet_T]:
        ...

    def union(self, other: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableSet_T]) -> System.Collections.Immutable.IImmutableSet[System_Collections_Immutable_IImmutableSet_T]:
        ...


class _Typed_ImmutableSortedDictionary_Create(typing.Generic[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey, System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey, System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey, System_Collections_Immutable_ImmutableSortedDictionary_Create_TValue]:
        ...


class _ImmutableSortedDictionary_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey]) -> System.Collections.Immutable._Typed_ImmutableSortedDictionary_Create[System_Collections_Immutable_ImmutableSortedDictionary_Create_TKey]:
        ...


class _Typed_ImmutableSortedDictionary_CreateRange(typing.Generic[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey]):
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey], items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue], items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey, System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TValue]:
        ...


class _ImmutableSortedDictionary_CreateRange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey]) -> System.Collections.Immutable._Typed_ImmutableSortedDictionary_CreateRange[System_Collections_Immutable_ImmutableSortedDictionary_CreateRange_TKey]:
        ...


class _Typed_ImmutableSortedDictionary_CreateBuilder(typing.Generic[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Immutable.ImmutableSortedDictionary.Builder:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary.Builder:
        ...

    @overload
    def __call__(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary.Builder:
        ...


class _ImmutableSortedDictionary_CreateBuilder:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey]) -> System.Collections.Immutable._Typed_ImmutableSortedDictionary_CreateBuilder[System_Collections_Immutable_ImmutableSortedDictionary_CreateBuilder_TKey]:
        ...


class _Typed_ImmutableSortedDictionary_ToImmutableSortedDictionary(typing.Generic[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue], key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableSortedDictionary.Builder) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue], key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], key_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey], element_selector: typing.Callable[[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource], System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]], key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]], key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TValue]:
        ...


class _ImmutableSortedDictionary_ToImmutableSortedDictionary:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource]) -> System.Collections.Immutable._Typed_ImmutableSortedDictionary_ToImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_ToImmutableSortedDictionary_TSource]:
        ...


class ImmutableSortedDictionary(typing.Generic[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue], System.Object, System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue], System.Collections.Generic.IDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]):
    """This class has no documentation."""

    class Builder(System.Object, System.Collections.Generic.IDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue], System.Collections.Generic.IReadOnlyDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]):
        """This class has no documentation."""

        @property
        def keys(self) -> typing.Iterable[System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
            ...

        @property
        def values(self) -> typing.Iterable[System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
            ...

        @property
        def count(self) -> int:
            ...

        @property
        def key_comparer(self) -> System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
            ...

        @key_comparer.setter
        def key_comparer(self, value: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> None:
            ...

        @property
        def value_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
            ...

        @value_comparer.setter
        def value_comparer(self, value: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> None:
            ...

        def __contains__(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> bool:
            ...

        def __getitem__(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> System_Collections_Immutable_ImmutableSortedDictionary_TValue:
            ...

        def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]:
            ...

        def __len__(self) -> int:
            ...

        def __setitem__(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> None:
            ...

        @overload
        def add(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> None:
            ...

        @overload
        def add(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> None:
            ...

        def add_range(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]) -> None:
            ...

        def clear(self) -> None:
            ...

        def contains(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> bool:
            ...

        def contains_key(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> bool:
            ...

        def contains_value(self, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> bool:
            ...

        def get_enumerator(self) -> System.Collections.Immutable.ImmutableSortedDictionary.Enumerator:
            ...

        @overload
        def get_value_or_default(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> System_Collections_Immutable_ImmutableSortedDictionary_TValue:
            ...

        @overload
        def get_value_or_default(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, default_value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> System_Collections_Immutable_ImmutableSortedDictionary_TValue:
            ...

        @overload
        def remove(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> bool:
            ...

        @overload
        def remove(self, item: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> bool:
            ...

        def remove_range(self, keys: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> None:
            ...

        def to_immutable(self) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
            ...

        def try_get_key(self, equal_key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, actual_key: typing.Optional[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
            ...

        def try_get_value(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: typing.Optional[System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
            ...

        def value_ref(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> typing.Any:
            ...

    class Enumerator(System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]], System.Collections.Immutable.ISecurePooledObjectUser):
        """This class has no documentation."""

        @property
        def current(self) -> System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
            ...

        def dispose(self) -> None:
            ...

        def move_next(self) -> bool:
            ...

        def reset(self) -> None:
            ...

    EMPTY: System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue] = ...

    @property
    def value_comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    @property
    def count(self) -> int:
        ...

    @property
    def keys(self) -> typing.Iterable[System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
        ...

    @property
    def values(self) -> typing.Iterable[System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    @property
    def key_comparer(self) -> System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
        ...

    create: System.Collections.Immutable._ImmutableSortedDictionary_Create

    create_range: System.Collections.Immutable._ImmutableSortedDictionary_CreateRange

    create_builder: System.Collections.Immutable._ImmutableSortedDictionary_CreateBuilder

    to_immutable_sorted_dictionary: System.Collections.Immutable._ImmutableSortedDictionary_ToImmutableSortedDictionary

    def __contains__(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> bool:
        ...

    def __getitem__(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> System_Collections_Immutable_ImmutableSortedDictionary_TValue:
        ...

    def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def add_range(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def clear(self) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def contains(self, pair: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> bool:
        ...

    def contains_key(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> bool:
        ...

    def contains_value(self, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> bool:
        ...

    def get_enumerator(self) -> System.Collections.Immutable.ImmutableSortedDictionary.Enumerator:
        ...

    def remove(self, value: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def remove_range(self, keys: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def set_item(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: System_Collections_Immutable_ImmutableSortedDictionary_TValue) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def set_items(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def to_builder(self) -> System.Collections.Immutable.ImmutableSortedDictionary.Builder:
        ...

    def try_get_key(self, equal_key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, actual_key: typing.Optional[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedDictionary_TKey]:
        ...

    def try_get_value(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey, value: typing.Optional[System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    def value_ref(self, key: System_Collections_Immutable_ImmutableSortedDictionary_TKey) -> typing.Any:
        ...

    @overload
    def with_comparers(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_TKey], value_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_ImmutableSortedDictionary_TValue]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...

    @overload
    def with_comparers(self, key_comparer: System.Collections.Generic.IComparer[System_Collections_Immutable_ImmutableSortedDictionary_TKey]) -> System.Collections.Immutable.ImmutableSortedDictionary[System_Collections_Immutable_ImmutableSortedDictionary_TKey, System_Collections_Immutable_ImmutableSortedDictionary_TValue]:
        ...


class IImmutableDictionary(typing.Generic[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue], System.Collections.Generic.IReadOnlyDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def add(self, key: System_Collections_Immutable_IImmutableDictionary_TKey, value: System_Collections_Immutable_IImmutableDictionary_TValue) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def add_range(self, pairs: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]]) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def clear(self) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def contains(self, pair: System.Collections.Generic.KeyValuePair[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]) -> bool:
        ...

    def remove(self, key: System_Collections_Immutable_IImmutableDictionary_TKey) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def remove_range(self, keys: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableDictionary_TKey]) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def set_item(self, key: System_Collections_Immutable_IImmutableDictionary_TKey, value: System_Collections_Immutable_IImmutableDictionary_TValue) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def set_items(self, items: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]]) -> System.Collections.Immutable.IImmutableDictionary[System_Collections_Immutable_IImmutableDictionary_TKey, System_Collections_Immutable_IImmutableDictionary_TValue]:
        ...

    def try_get_key(self, equal_key: System_Collections_Immutable_IImmutableDictionary_TKey, actual_key: typing.Optional[System_Collections_Immutable_IImmutableDictionary_TKey]) -> typing.Tuple[bool, System_Collections_Immutable_IImmutableDictionary_TKey]:
        ...


class IImmutableList(typing.Generic[System_Collections_Immutable_IImmutableList_T], System.Collections.Generic.IReadOnlyList[System_Collections_Immutable_IImmutableList_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def add(self, value: System_Collections_Immutable_IImmutableList_T) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def add_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableList_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def clear(self) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def index_of(self, item: System_Collections_Immutable_IImmutableList_T, index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_IImmutableList_T]) -> int:
        ...

    def insert(self, index: int, element: System_Collections_Immutable_IImmutableList_T) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def insert_range(self, index: int, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableList_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def last_index_of(self, item: System_Collections_Immutable_IImmutableList_T, index: int, count: int, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_IImmutableList_T]) -> int:
        ...

    def remove(self, value: System_Collections_Immutable_IImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_IImmutableList_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def remove_all(self, match: typing.Callable[[System_Collections_Immutable_IImmutableList_T], bool]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def remove_at(self, index: int) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    @overload
    def remove_range(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableList_T], equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_IImmutableList_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    @overload
    def remove_range(self, index: int, count: int) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def replace(self, old_value: System_Collections_Immutable_IImmutableList_T, new_value: System_Collections_Immutable_IImmutableList_T, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Immutable_IImmutableList_T]) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...

    def set_item(self, index: int, value: System_Collections_Immutable_IImmutableList_T) -> System.Collections.Immutable.IImmutableList[System_Collections_Immutable_IImmutableList_T]:
        ...


class _Typed_ImmutableInterlocked_Update(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_Update_T]):
    """"""

    @overload
    def __call__(self, location: System_Collections_Immutable_ImmutableInterlocked_Update_T, transformer: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_Update_T], System_Collections_Immutable_ImmutableInterlocked_Update_T]) -> bool:
        ...

    @overload
    def __call__(self, location: System_Collections_Immutable_ImmutableInterlocked_Update_T, transformer: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_Update_T, System_Collections_Immutable_ImmutableInterlocked_Update_TArg], System_Collections_Immutable_ImmutableInterlocked_Update_T], transformer_argument: System_Collections_Immutable_ImmutableInterlocked_Update_TArg) -> bool:
        ...

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T], transformer: typing.Callable[[System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T]], System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T]]) -> bool:
        ...

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T], transformer: typing.Callable[[System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T], System_Collections_Immutable_ImmutableInterlocked_Update_TArg], System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_Update_T]], transformer_argument: System_Collections_Immutable_ImmutableInterlocked_Update_TArg) -> bool:
        ...


class _ImmutableInterlocked_Update:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_Update_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_Update[System_Collections_Immutable_ImmutableInterlocked_Update_T]:
        ...


class _Typed_ImmutableInterlocked_InterlockedExchange(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T], value: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T]:
        ...


class _ImmutableInterlocked_InterlockedExchange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_InterlockedExchange[System_Collections_Immutable_ImmutableInterlocked_InterlockedExchange_T]:
        ...


class _Typed_ImmutableInterlocked_InterlockedCompareExchange(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T], value: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T], comparand: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T]) -> System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T]:
        ...


class _ImmutableInterlocked_InterlockedCompareExchange:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_InterlockedCompareExchange[System_Collections_Immutable_ImmutableInterlocked_InterlockedCompareExchange_T]:
        ...


class _Typed_ImmutableInterlocked_InterlockedInitialize(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T], value: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T]) -> bool:
        ...


class _ImmutableInterlocked_InterlockedInitialize:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_InterlockedInitialize[System_Collections_Immutable_ImmutableInterlocked_InterlockedInitialize_T]:
        ...


class _Typed_ImmutableInterlocked_GetOrAdd(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue], key: System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, value_factory: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TArg], System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue], factory_argument: System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TArg) -> System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue:
        ...

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue], key: System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, value_factory: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey], System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue]) -> System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue:
        ...

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue], key: System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey, value: System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue) -> System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TValue:
        ...


class _ImmutableInterlocked_GetOrAdd:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_GetOrAdd[System_Collections_Immutable_ImmutableInterlocked_GetOrAdd_TKey]:
        ...


class _Typed_ImmutableInterlocked_AddOrUpdate(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue], key: System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, add_value_factory: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey], System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue], update_value_factory: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue], System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue]) -> System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue:
        ...

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue], key: System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, add_value: System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue, update_value_factory: typing.Callable[[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey, System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue], System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue]) -> System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TValue:
        ...


class _ImmutableInterlocked_AddOrUpdate:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_AddOrUpdate[System_Collections_Immutable_ImmutableInterlocked_AddOrUpdate_TKey]:
        ...


class _Typed_ImmutableInterlocked_TryAdd(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey, System_Collections_Immutable_ImmutableInterlocked_TryAdd_TValue], key: System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey, value: System_Collections_Immutable_ImmutableInterlocked_TryAdd_TValue) -> bool:
        ...


class _ImmutableInterlocked_TryAdd:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_TryAdd[System_Collections_Immutable_ImmutableInterlocked_TryAdd_TKey]:
        ...


class _Typed_ImmutableInterlocked_TryUpdate(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey, System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TValue], key: System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey, new_value: System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TValue, comparison_value: System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TValue) -> bool:
        ...


class _ImmutableInterlocked_TryUpdate:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_TryUpdate[System_Collections_Immutable_ImmutableInterlocked_TryUpdate_TKey]:
        ...


class _Typed_ImmutableInterlocked_TryRemove(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableDictionary[System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey, System_Collections_Immutable_ImmutableInterlocked_TryRemove_TValue], key: System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey, value: typing.Optional[System_Collections_Immutable_ImmutableInterlocked_TryRemove_TValue]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableInterlocked_TryRemove_TValue]:
        ...


class _ImmutableInterlocked_TryRemove:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_TryRemove[System_Collections_Immutable_ImmutableInterlocked_TryRemove_TKey]:
        ...


class _Typed_ImmutableInterlocked_TryPop(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_TryPop_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableInterlocked_TryPop_T], value: typing.Optional[System_Collections_Immutable_ImmutableInterlocked_TryPop_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableInterlocked_TryPop_T]:
        ...


class _ImmutableInterlocked_TryPop:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_TryPop_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_TryPop[System_Collections_Immutable_ImmutableInterlocked_TryPop_T]:
        ...


class _Typed_ImmutableInterlocked_Push(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_Push_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableStack[System_Collections_Immutable_ImmutableInterlocked_Push_T], value: System_Collections_Immutable_ImmutableInterlocked_Push_T) -> None:
        ...


class _ImmutableInterlocked_Push:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_Push_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_Push[System_Collections_Immutable_ImmutableInterlocked_Push_T]:
        ...


class _Typed_ImmutableInterlocked_TryDequeue(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T], value: typing.Optional[System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T]) -> typing.Tuple[bool, System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T]:
        ...


class _ImmutableInterlocked_TryDequeue:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_TryDequeue[System_Collections_Immutable_ImmutableInterlocked_TryDequeue_T]:
        ...


class _Typed_ImmutableInterlocked_Enqueue(typing.Generic[System_Collections_Immutable_ImmutableInterlocked_Enqueue_T]):
    """"""

    @overload
    def __call__(self, location: System.Collections.Immutable.ImmutableQueue[System_Collections_Immutable_ImmutableInterlocked_Enqueue_T], value: System_Collections_Immutable_ImmutableInterlocked_Enqueue_T) -> None:
        ...


class _ImmutableInterlocked_Enqueue:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableInterlocked_Enqueue_T]) -> System.Collections.Immutable._Typed_ImmutableInterlocked_Enqueue[System_Collections_Immutable_ImmutableInterlocked_Enqueue_T]:
        ...


class ImmutableInterlocked(System.Object):
    """This class has no documentation."""

    update: System.Collections.Immutable._ImmutableInterlocked_Update

    interlocked_exchange: System.Collections.Immutable._ImmutableInterlocked_InterlockedExchange

    interlocked_compare_exchange: System.Collections.Immutable._ImmutableInterlocked_InterlockedCompareExchange

    interlocked_initialize: System.Collections.Immutable._ImmutableInterlocked_InterlockedInitialize

    get_or_add: System.Collections.Immutable._ImmutableInterlocked_GetOrAdd

    add_or_update: System.Collections.Immutable._ImmutableInterlocked_AddOrUpdate

    try_add: System.Collections.Immutable._ImmutableInterlocked_TryAdd

    try_update: System.Collections.Immutable._ImmutableInterlocked_TryUpdate

    try_remove: System.Collections.Immutable._ImmutableInterlocked_TryRemove

    try_pop: System.Collections.Immutable._ImmutableInterlocked_TryPop

    push: System.Collections.Immutable._ImmutableInterlocked_Push

    try_dequeue: System.Collections.Immutable._ImmutableInterlocked_TryDequeue

    enqueue: System.Collections.Immutable._ImmutableInterlocked_Enqueue


class IImmutableQueue(typing.Generic[System_Collections_Immutable_IImmutableQueue_T], System.Collections.Generic.IEnumerable[System_Collections_Immutable_IImmutableQueue_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def is_empty(self) -> bool:
        ...

    def clear(self) -> System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_IImmutableQueue_T]:
        ...

    def dequeue(self) -> System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_IImmutableQueue_T]:
        ...

    def enqueue(self, value: System_Collections_Immutable_IImmutableQueue_T) -> System.Collections.Immutable.IImmutableQueue[System_Collections_Immutable_IImmutableQueue_T]:
        ...

    def peek(self) -> System_Collections_Immutable_IImmutableQueue_T:
        ...


class Builder_AddRange:
    """"""

    @overload
    def __call__(self, items: System.Collections.Generic.IEnumerable[System_Collections_Immutable_ImmutableArray_T]) -> None:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableArray_T, typing.Iterable[System_Collections_Immutable_ImmutableArray_T]]) -> None:
        ...

    @overload
    def __call__(self, items: typing.List[System_Collections_Immutable_ImmutableArray_T], length: int) -> None:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T]) -> None:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_T], length: int) -> None:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray.Builder) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]) -> System.Collections.Immutable._Typed_ImmutableArray.Builder_AddRange[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]:
        ...


class Builder_AddRange(typing.Generic[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]):
    """"""

    @overload
    def __call__(self, items: typing.List[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]) -> None:
        ...

    @overload
    def __call__(self, *items: typing.Union[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived, typing.Iterable[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]]) -> None:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray[System_Collections_Immutable_ImmutableArray_AddRange_Builder_TDerived]) -> None:
        ...

    @overload
    def __call__(self, items: System.Collections.Immutable.ImmutableArray.Builder) -> None:
        ...


class Builder_ConvertAll:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput]) -> System.Collections.Immutable._Typed_ImmutableList.Builder_ConvertAll[System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput]:
        ...


class Builder_ConvertAll(typing.Generic[System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput]):
    """"""

    @overload
    def __call__(self, converter: typing.Callable[[System_Collections_Immutable_ImmutableList_T], System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput]) -> System.Collections.Immutable.ImmutableList[System_Collections_Immutable_ImmutableList_ConvertAll_Builder_TOutput]:
        ...


