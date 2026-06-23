from typing import overload
from enum import IntEnum
import abc
import typing

import System
import System.Collections
import System.Collections.Frozen
import System.Collections.Generic
import System.Collections.Immutable

System_Collections_Frozen_FrozenDictionary_TKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_TKey")
System_Collections_Frozen_FrozenDictionary_TValue = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_TValue")
System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey")
System_Collections_Frozen_FrozenSet_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_T")
System_Collections_Frozen_FrozenSet_AlternateLookup_TAlternate = typing.TypeVar("System_Collections_Frozen_FrozenSet_AlternateLookup_TAlternate")
System_Collections_Frozen_FrozenDictionary_Create_TKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_Create_TKey")
System_Collections_Frozen_FrozenDictionary_Create_TValue = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_Create_TValue")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement")
System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey")
System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey")
System_Collections_Frozen_FrozenSet_Create_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_Create_T")
System_Collections_Frozen_FrozenSet_ToFrozenSet_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_ToFrozenSet_T")
System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate = typing.TypeVar("System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate")
System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate = typing.TypeVar("System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate")


class _Typed_FrozenDictionary_Create(typing.Generic[System_Collections_Frozen_FrozenDictionary_Create_TKey]):
    """"""

    @overload
    def __call__(self, *source: typing.Union[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue]]]) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue]:
        ...

    @overload
    def __call__(self, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_Create_TKey], *source: typing.Union[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue]]]) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_Create_TKey, System_Collections_Frozen_FrozenDictionary_Create_TValue]:
        ...


class _FrozenDictionary_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenDictionary_Create_TKey]) -> System.Collections.Frozen._Typed_FrozenDictionary_Create[System_Collections_Frozen_FrozenDictionary_Create_TKey]:
        ...


class _Typed_FrozenDictionary_ToFrozenDictionary(typing.Generic[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], key_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource]:
        ...

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], key_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey], element_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement]:
        ...


class _FrozenDictionary_ToFrozenDictionary:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey]) -> System.Collections.Frozen._Typed_FrozenDictionary_ToFrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey]:
        ...


class _Typed_FrozenDictionary_GetAlternateLookup(typing.Generic[System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Frozen.FrozenDictionary.AlternateLookup[System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey]:
        ...


class _FrozenDictionary_GetAlternateLookup:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey]) -> System.Collections.Frozen._Typed_FrozenDictionary_GetAlternateLookup[System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey]:
        ...


class _Typed_FrozenDictionary_TryGetAlternateLookup(typing.Generic[System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey]):
    """"""

    @overload
    def __call__(self, lookup: typing.Optional[System.Collections.Frozen.FrozenDictionary.AlternateLookup[System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey]]) -> typing.Tuple[bool, System.Collections.Frozen.FrozenDictionary.AlternateLookup[System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey]]:
        ...


class _FrozenDictionary_TryGetAlternateLookup:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey]) -> System.Collections.Frozen._Typed_FrozenDictionary_TryGetAlternateLookup[System_Collections_Frozen_FrozenDictionary_TryGetAlternateLookup_TAlternateKey]:
        ...


class FrozenDictionary(typing.Generic[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Object, System.Collections.Generic.IDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Collections.Generic.IReadOnlyDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]]):
        """This class has no documentation."""

        @property
        def current(self) -> System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]:
            ...

        def move_next(self) -> bool:
            ...

    class AlternateLookup(typing.Generic[System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey]):
        """This class has no documentation."""

        @property
        def dictionary(self) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]:
            ...

        def __getitem__(self, key: System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey) -> System_Collections_Frozen_FrozenDictionary_TValue:
            ...

        def contains_key(self, key: System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey) -> bool:
            ...

        def try_get_value(self, key: System_Collections_Frozen_FrozenDictionary_AlternateLookup_TAlternateKey, value: typing.Optional[System_Collections_Frozen_FrozenDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Frozen_FrozenDictionary_TValue]:
            ...

    EMPTY: System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]

    @property
    def comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_TKey]:
        ...

    @property
    def keys(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenDictionary_TKey]:
        ...

    @property
    def values(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenDictionary_TValue]:
        ...

    @property
    def count(self) -> int:
        ...

    create: System.Collections.Frozen._FrozenDictionary_Create

    to_frozen_dictionary: System.Collections.Frozen._FrozenDictionary_ToFrozenDictionary

    @property
    def get_alternate_lookup(self) -> System.Collections.Frozen._FrozenDictionary_GetAlternateLookup:
        ...

    @property
    def try_get_alternate_lookup(self) -> System.Collections.Frozen._FrozenDictionary_TryGetAlternateLookup:
        ...

    def __contains__(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> bool:
        ...

    def __getitem__(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> typing.Any:
        ...

    def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]]:
        ...

    def __len__(self) -> int:
        ...

    def contains_key(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> bool:
        ...

    @overload
    def copy_to(self, destination: typing.List[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]], destination_index: int) -> None:
        ...

    @overload
    def copy_to(self, destination: System.Span[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]]) -> None:
        ...

    def get_enumerator(self) -> System.Collections.Frozen.FrozenDictionary.Enumerator:
        ...

    def get_value_ref_or_null_ref(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> typing.Any:
        ...

    def try_get_value(self, key: System_Collections_Frozen_FrozenDictionary_TKey, value: typing.Optional[System_Collections_Frozen_FrozenDictionary_TValue]) -> typing.Tuple[bool, System_Collections_Frozen_FrozenDictionary_TValue]:
        ...


class _Typed_FrozenSet_Create(typing.Generic[System_Collections_Frozen_FrozenSet_Create_T]):
    """"""

    @overload
    def __call__(self, *source: typing.Union[System_Collections_Frozen_FrozenSet_Create_T, typing.Iterable[System_Collections_Frozen_FrozenSet_Create_T]]) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_Create_T]:
        ...

    @overload
    def __call__(self, equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_Create_T], *source: typing.Union[System_Collections_Frozen_FrozenSet_Create_T, typing.Iterable[System_Collections_Frozen_FrozenSet_Create_T]]) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_Create_T]:
        ...


class _FrozenSet_Create:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenSet_Create_T]) -> System.Collections.Frozen._Typed_FrozenSet_Create[System_Collections_Frozen_FrozenSet_Create_T]:
        ...


class _Typed_FrozenSet_ToFrozenSet(typing.Generic[System_Collections_Frozen_FrozenSet_ToFrozenSet_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_ToFrozenSet_T], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_ToFrozenSet_T] = None) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_ToFrozenSet_T]:
        ...


class _FrozenSet_ToFrozenSet:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenSet_ToFrozenSet_T]) -> System.Collections.Frozen._Typed_FrozenSet_ToFrozenSet[System_Collections_Frozen_FrozenSet_ToFrozenSet_T]:
        ...


class _Typed_FrozenSet_GetAlternateLookup(typing.Generic[System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Frozen.FrozenSet.AlternateLookup[System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate]:
        ...


class _FrozenSet_GetAlternateLookup:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate]) -> System.Collections.Frozen._Typed_FrozenSet_GetAlternateLookup[System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate]:
        ...


class _Typed_FrozenSet_TryGetAlternateLookup(typing.Generic[System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate]):
    """"""

    @overload
    def __call__(self, lookup: typing.Optional[System.Collections.Frozen.FrozenSet.AlternateLookup[System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate]]) -> typing.Tuple[bool, System.Collections.Frozen.FrozenSet.AlternateLookup[System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate]]:
        ...


class _FrozenSet_TryGetAlternateLookup:
    """"""

    def __getitem__(self, type: typing.Type[System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate]) -> System.Collections.Frozen._Typed_FrozenSet_TryGetAlternateLookup[System_Collections_Frozen_FrozenSet_TryGetAlternateLookup_TAlternate]:
        ...


class FrozenSet(typing.Generic[System_Collections_Frozen_FrozenSet_T], System.Object, System.Collections.Generic.ISet[System_Collections_Frozen_FrozenSet_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Frozen_FrozenSet_T], System.Collections.ICollection, typing.Iterable[System_Collections_Frozen_FrozenSet_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Frozen_FrozenSet_T]):
        """This class has no documentation."""

        @property
        def current(self) -> System_Collections_Frozen_FrozenSet_T:
            ...

        def move_next(self) -> bool:
            ...

    class AlternateLookup(typing.Generic[System_Collections_Frozen_FrozenSet_AlternateLookup_TAlternate]):
        """This class has no documentation."""

        @property
        def set(self) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_T]:
            ...

        def contains(self, item: System_Collections_Frozen_FrozenSet_AlternateLookup_TAlternate) -> bool:
            ...

        def try_get_value(self, equal_value: System_Collections_Frozen_FrozenSet_AlternateLookup_TAlternate, actual_value: typing.Optional[System_Collections_Frozen_FrozenSet_T]) -> typing.Tuple[bool, System_Collections_Frozen_FrozenSet_T]:
            ...

    EMPTY: System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_T]

    @property
    def comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_T]:
        ...

    @property
    def items(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenSet_T]:
        ...

    @property
    def count(self) -> int:
        ...

    create: System.Collections.Frozen._FrozenSet_Create

    to_frozen_set: System.Collections.Frozen._FrozenSet_ToFrozenSet

    @property
    def get_alternate_lookup(self) -> System.Collections.Frozen._FrozenSet_GetAlternateLookup:
        ...

    @property
    def try_get_alternate_lookup(self) -> System.Collections.Frozen._FrozenSet_TryGetAlternateLookup:
        ...

    def __iter__(self) -> typing.Iterator[System_Collections_Frozen_FrozenSet_T]:
        ...

    def __len__(self) -> int:
        ...

    def contains(self, item: System_Collections_Frozen_FrozenSet_T) -> bool:
        ...

    @overload
    def copy_to(self, destination: typing.List[System_Collections_Frozen_FrozenSet_T], destination_index: int) -> None:
        ...

    @overload
    def copy_to(self, destination: System.Span[System_Collections_Frozen_FrozenSet_T]) -> None:
        ...

    def get_enumerator(self) -> System.Collections.Frozen.FrozenSet.Enumerator:
        ...

    def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def try_get_value(self, equal_value: System_Collections_Frozen_FrozenSet_T, actual_value: typing.Optional[System_Collections_Frozen_FrozenSet_T]) -> typing.Tuple[bool, System_Collections_Frozen_FrozenSet_T]:
        ...


