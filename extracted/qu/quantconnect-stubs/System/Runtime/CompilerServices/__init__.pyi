from typing import overload
from enum import IntEnum
import abc
import typing
import warnings

import System
import System.Collections.Generic
import System.Diagnostics.Contracts
import System.Runtime.CompilerServices
import System.Runtime.Serialization
import System.Threading
import System.Threading.Tasks

System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_TaskAwaiter_TResult = typing.TypeVar("System_Runtime_CompilerServices_TaskAwaiter_TResult")
System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_ValueTaskAwaiter_TResult = typing.TypeVar("System_Runtime_CompilerServices_ValueTaskAwaiter_TResult")
System_Runtime_CompilerServices_StrongBox_T = typing.TypeVar("System_Runtime_CompilerServices_StrongBox_T")
System_Runtime_CompilerServices_InlineArray2_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray2_T")
System_Runtime_CompilerServices_InlineArray3_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray3_T")
System_Runtime_CompilerServices_InlineArray4_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray4_T")
System_Runtime_CompilerServices_InlineArray5_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray5_T")
System_Runtime_CompilerServices_InlineArray6_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray6_T")
System_Runtime_CompilerServices_InlineArray7_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray7_T")
System_Runtime_CompilerServices_InlineArray8_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray8_T")
System_Runtime_CompilerServices_InlineArray9_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray9_T")
System_Runtime_CompilerServices_InlineArray10_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray10_T")
System_Runtime_CompilerServices_InlineArray11_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray11_T")
System_Runtime_CompilerServices_InlineArray12_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray12_T")
System_Runtime_CompilerServices_InlineArray13_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray13_T")
System_Runtime_CompilerServices_InlineArray14_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray14_T")
System_Runtime_CompilerServices_InlineArray15_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray15_T")
System_Runtime_CompilerServices_InlineArray16_T = typing.TypeVar("System_Runtime_CompilerServices_InlineArray16_T")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult")
System_Runtime_CompilerServices_ConditionalWeakTable_TKey = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TKey")
System_Runtime_CompilerServices_ConditionalWeakTable_TValue = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TValue")
System_Runtime_CompilerServices__EventContainer_Callable = typing.TypeVar("System_Runtime_CompilerServices__EventContainer_Callable")
System_Runtime_CompilerServices__EventContainer_ReturnType = typing.TypeVar("System_Runtime_CompilerServices__EventContainer_ReturnType")
System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter")
System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter")
System_Runtime_CompilerServices_AsyncHelpers_Await_T = typing.TypeVar("System_Runtime_CompilerServices_AsyncHelpers_Await_T")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T")
System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T")
System_Runtime_CompilerServices_RuntimeHelpers_IsReferenceOrContainsReferences_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_IsReferenceOrContainsReferences_T")
System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T = typing.TypeVar("System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T")
System_Runtime_CompilerServices_Unsafe_AsPointer_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AsPointer_T")
System_Runtime_CompilerServices_Unsafe_SizeOf_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_SizeOf_T")
System_Runtime_CompilerServices_Unsafe_As_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_As_T")
System_Runtime_CompilerServices_Unsafe_As_TFrom = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_As_TFrom")
System_Runtime_CompilerServices_Unsafe_Add_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Add_T")
System_Runtime_CompilerServices_Unsafe_AddByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AddByteOffset_T")
System_Runtime_CompilerServices_Unsafe_AreSame_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AreSame_T")
System_Runtime_CompilerServices_Unsafe_BitCast_TFrom = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_BitCast_TFrom")
System_Runtime_CompilerServices_Unsafe_BitCast_TTo = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_BitCast_TTo")
System_Runtime_CompilerServices_Unsafe_Copy_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Copy_T")
System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T")
System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T")
System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T")
System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T")
System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T")
System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T")
System_Runtime_CompilerServices_Unsafe_Read_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Read_T")
System_Runtime_CompilerServices_Unsafe_Write_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Write_T")
System_Runtime_CompilerServices_Unsafe_AsRef_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AsRef_T")
System_Runtime_CompilerServices_Unsafe_ByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_ByteOffset_T")
System_Runtime_CompilerServices_Unsafe_NullRef_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_NullRef_T")
System_Runtime_CompilerServices_Unsafe_IsNullRef_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsNullRef_T")
System_Runtime_CompilerServices_Unsafe_SkipInit_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_SkipInit_T")
System_Runtime_CompilerServices_Unsafe_Subtract_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Subtract_T")
System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T")
System_Runtime_CompilerServices_Unsafe_Unbox_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Unbox_T")
System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg")


class CustomConstantAttribute(System.Attribute, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def value(self) -> System.Object:
        ...


class DateTimeConstantAttribute(System.Runtime.CompilerServices.CustomConstantAttribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Object:
        ...

    def __init__(self, ticks: int) -> None:
        ...


class CallerFilePathAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class RequiresLocationAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IsConst(System.Object):
    """This class has no documentation."""


class IAsyncStateMachine(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def move_next(self) -> None:
        ...

    def set_state_machine(self, state_machine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        ...


class IUnion(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def value(self) -> System.Object:
        ...


class StringFreezingAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StateMachineAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def state_machine_type(self) -> typing.Type:
        ...

    def __init__(self, state_machine_type: typing.Type) -> None:
        ...


class AsyncIteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, state_machine_type: typing.Type) -> None:
        ...


class NullablePublicOnlyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def includes_internals(self) -> bool:
        ...

    @includes_internals.setter
    def includes_internals(self, value: bool) -> None:
        ...

    def __init__(self, value: bool) -> None:
        ...


class ConfiguredCancelableAsyncEnumerable(typing.Generic[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]):
    """This class has no documentation."""

    class Enumerator:
        """This class has no documentation."""

        @property
        def current(self) -> System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T:
            ...

        def dispose_async(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
            ...

        def move_next_async(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable[bool]:
            ...

    def configure_await(self, continue_on_captured_context: bool) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        ...

    def get_async_enumerator(self) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable.Enumerator:
        ...

    def with_cancellation(self, cancellation_token: System.Threading.CancellationToken) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        ...


class IsReadOnlyAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class UnsafeValueTypeAttribute(System.Attribute):
    """This class has no documentation."""


class _Typed_AsyncHelpers_UnsafeAwaitAwaiter(typing.Generic[System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter) -> None:
        ...


class _AsyncHelpers_UnsafeAwaitAwaiter:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncHelpers_UnsafeAwaitAwaiter[System_Runtime_CompilerServices_AsyncHelpers_UnsafeAwaitAwaiter_TAwaiter]:
        ...


class _Typed_AsyncHelpers_AwaitAwaiter(typing.Generic[System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter) -> None:
        ...


class _AsyncHelpers_AwaitAwaiter:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncHelpers_AwaitAwaiter[System_Runtime_CompilerServices_AsyncHelpers_AwaitAwaiter_TAwaiter]:
        ...


class _Typed_AsyncHelpers_Await(typing.Generic[System_Runtime_CompilerServices_AsyncHelpers_Await_T]):
    """"""

    @overload
    def __call__(self, task: System.Threading.Tasks.Task[System_Runtime_CompilerServices_AsyncHelpers_Await_T]) -> System_Runtime_CompilerServices_AsyncHelpers_Await_T:
        ...

    @overload
    def __call__(self, task: System.Threading.Tasks.ValueTask[System_Runtime_CompilerServices_AsyncHelpers_Await_T]) -> System_Runtime_CompilerServices_AsyncHelpers_Await_T:
        ...

    @overload
    def __call__(self, configured_awaitable: System.Runtime.CompilerServices.ConfiguredTaskAwaitable[System_Runtime_CompilerServices_AsyncHelpers_Await_T]) -> System_Runtime_CompilerServices_AsyncHelpers_Await_T:
        ...

    @overload
    def __call__(self, configured_awaitable: System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable[System_Runtime_CompilerServices_AsyncHelpers_Await_T]) -> System_Runtime_CompilerServices_AsyncHelpers_Await_T:
        ...


class _AsyncHelpers_Await:
    """"""

    @overload
    def __call__(self, task: System.Threading.Tasks.Task) -> None:
        ...

    @overload
    def __call__(self, task: System.Threading.Tasks.ValueTask) -> None:
        ...

    @overload
    def __call__(self, configured_awaitable: System.Runtime.CompilerServices.ConfiguredTaskAwaitable) -> None:
        ...

    @overload
    def __call__(self, configured_awaitable: System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncHelpers_Await_T]) -> System.Runtime.CompilerServices._Typed_AsyncHelpers_Await[System_Runtime_CompilerServices_AsyncHelpers_Await_T]:
        ...


class AsyncHelpers(System.Object):
    """This class has no documentation."""

    unsafe_await_awaiter: System.Runtime.CompilerServices._AsyncHelpers_UnsafeAwaitAwaiter

    await_awaiter: System.Runtime.CompilerServices._AsyncHelpers_AwaitAwaiter

    Await: System.Runtime.CompilerServices._AsyncHelpers_Await

    @staticmethod
    @overload
    def handle_async_entry_point(task: System.Threading.Tasks.Task) -> None:
        ...

    @staticmethod
    @overload
    def handle_async_entry_point(task: System.Threading.Tasks.Task[int]) -> int:
        ...


class _Typed_AsyncValueTaskMethodBuilder_Start(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine]):
    """"""

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        ...


class _AsyncValueTaskMethodBuilder_Start:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine]) -> System.Runtime.CompilerServices._Typed_AsyncValueTaskMethodBuilder_Start[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine]:
        ...


class _Typed_AsyncValueTaskMethodBuilder_AwaitOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...


class _AsyncValueTaskMethodBuilder_AwaitOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncValueTaskMethodBuilder_AwaitOnCompleted[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]:
        ...


class _Typed_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...


class _AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]:
        ...


class AsyncValueTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]):
    """This class has no documentation."""

    @property
    def task(self) -> System.Threading.Tasks.ValueTask:
        ...

    @property
    def start(self) -> System.Runtime.CompilerServices._AsyncValueTaskMethodBuilder_Start:
        ...

    @property
    def await_on_completed(self) -> System.Runtime.CompilerServices._AsyncValueTaskMethodBuilder_AwaitOnCompleted:
        ...

    @property
    def await_unsafe_on_completed(self) -> System.Runtime.CompilerServices._AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted:
        ...

    @staticmethod
    def create() -> System.Runtime.CompilerServices.AsyncValueTaskMethodBuilder:
        ...

    def set_exception(self, exception: System.Exception) -> None:
        ...

    @overload
    def set_result(self) -> None:
        ...

    @overload
    def set_result(self, result: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult) -> None:
        ...

    def set_state_machine(self, state_machine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        ...


class CallerLineNumberAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class _Typed_AsyncIteratorMethodBuilder_MoveNext(typing.Generic[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine]):
    """"""

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine) -> None:
        ...


class _AsyncIteratorMethodBuilder_MoveNext:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine]) -> System.Runtime.CompilerServices._Typed_AsyncIteratorMethodBuilder_MoveNext[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine]:
        ...


class _Typed_AsyncIteratorMethodBuilder_AwaitOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...


class _AsyncIteratorMethodBuilder_AwaitOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncIteratorMethodBuilder_AwaitOnCompleted[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter]:
        ...


class _Typed_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...


class _AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted[System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]:
        ...


class AsyncIteratorMethodBuilder:
    """This class has no documentation."""

    @property
    def move_next(self) -> System.Runtime.CompilerServices._AsyncIteratorMethodBuilder_MoveNext:
        ...

    @property
    def await_on_completed(self) -> System.Runtime.CompilerServices._AsyncIteratorMethodBuilder_AwaitOnCompleted:
        ...

    @property
    def await_unsafe_on_completed(self) -> System.Runtime.CompilerServices._AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted:
        ...

    def complete(self) -> None:
        ...

    @staticmethod
    def create() -> System.Runtime.CompilerServices.AsyncIteratorMethodBuilder:
        ...


class INotifyCompletion(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...


class ICriticalNotifyCompletion(System.Runtime.CompilerServices.INotifyCompletion, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def unsafe_on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...


class TaskAwaiter(typing.Generic[System_Runtime_CompilerServices_TaskAwaiter_TResult], System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.ITaskAwaiter):
    """This class has no documentation."""

    @property
    def is_completed(self) -> bool:
        ...

    def get_result(self) -> None:
        ...

    def on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...

    def unsafe_on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...


class ConfiguredTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult]):
    """This class has no documentation."""

    def get_awaiter(self) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable.ConfiguredTaskAwaiter:
        ...


class TupleElementNamesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def transform_names(self) -> typing.List[str]:
        ...

    def __init__(self, transform_names: typing.List[str]) -> None:
        ...


class ExtensionAttribute(System.Attribute):
    """This class has no documentation."""


class DisablePrivateReflectionAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class InterpolatedStringHandlerAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class YieldAwaitable:
    """This class has no documentation."""

    class YieldAwaiter(System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.IStateMachineBoxAwareAwaiter):
        """This class has no documentation."""

        @property
        def is_completed(self) -> bool:
            ...

        def get_result(self) -> None:
            ...

        def on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
            ...

        def unsafe_on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
            ...

    def get_awaiter(self) -> System.Runtime.CompilerServices.YieldAwaitable.YieldAwaiter:
        ...


class _Typed_AsyncVoidMethodBuilder_Start(typing.Generic[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine]):
    """"""

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine) -> None:
        ...


class _AsyncVoidMethodBuilder_Start:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine]) -> System.Runtime.CompilerServices._Typed_AsyncVoidMethodBuilder_Start[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine]:
        ...


class _Typed_AsyncVoidMethodBuilder_AwaitOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...


class _AsyncVoidMethodBuilder_AwaitOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncVoidMethodBuilder_AwaitOnCompleted[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter]:
        ...


class _Typed_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...


class _AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted[System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]:
        ...


class AsyncVoidMethodBuilder:
    """This class has no documentation."""

    @property
    def start(self) -> System.Runtime.CompilerServices._AsyncVoidMethodBuilder_Start:
        ...

    @property
    def await_on_completed(self) -> System.Runtime.CompilerServices._AsyncVoidMethodBuilder_AwaitOnCompleted:
        ...

    @property
    def await_unsafe_on_completed(self) -> System.Runtime.CompilerServices._AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted:
        ...

    @staticmethod
    def create() -> System.Runtime.CompilerServices.AsyncVoidMethodBuilder:
        ...

    def set_exception(self, exception: System.Exception) -> None:
        ...

    def set_result(self) -> None:
        ...

    def set_state_machine(self, state_machine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        ...


class InlineArrayAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def length(self) -> int:
        ...

    def __init__(self, length: int) -> None:
        ...


class _Typed_AsyncTaskMethodBuilder_Start(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine]):
    """"""

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        ...


class _AsyncTaskMethodBuilder_Start:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine]) -> System.Runtime.CompilerServices._Typed_AsyncTaskMethodBuilder_Start[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine]:
        ...


class _Typed_AsyncTaskMethodBuilder_AwaitOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...


class _AsyncTaskMethodBuilder_AwaitOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncTaskMethodBuilder_AwaitOnCompleted[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter]:
        ...


class _Typed_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...


class _AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]:
        ...


class AsyncTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]):
    """This class has no documentation."""

    @property
    def task(self) -> System.Threading.Tasks.Task[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]:
        ...

    @property
    def start(self) -> System.Runtime.CompilerServices._AsyncTaskMethodBuilder_Start:
        ...

    @property
    def await_on_completed(self) -> System.Runtime.CompilerServices._AsyncTaskMethodBuilder_AwaitOnCompleted:
        ...

    @property
    def await_unsafe_on_completed(self) -> System.Runtime.CompilerServices._AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted:
        ...

    @staticmethod
    def create() -> System.Runtime.CompilerServices.AsyncTaskMethodBuilder[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]:
        ...

    def set_exception(self, exception: System.Exception) -> None:
        ...

    @overload
    def set_result(self, result: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult) -> None:
        ...

    @overload
    def set_result(self) -> None:
        ...

    def set_state_machine(self, state_machine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        ...


class CompilerFeatureRequiredAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def feature_name(self) -> str:
        ...

    @property
    def is_optional(self) -> bool:
        ...

    REF_STRUCTS: str = ...

    REQUIRED_MEMBERS: str = ...

    def __init__(self, feature_name: str) -> None:
        ...


class MetadataUpdateDeletedAttribute(System.Attribute):
    """This class has no documentation."""


class ReferenceAssemblyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def description(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, description: str) -> None:
        ...


class ValueTaskAwaiter(typing.Generic[System_Runtime_CompilerServices_ValueTaskAwaiter_TResult], System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.IStateMachineBoxAwareAwaiter):
    """This class has no documentation."""

    @property
    def is_completed(self) -> bool:
        ...

    def get_result(self) -> None:
        ...

    def on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...

    def unsafe_on_completed(self, continuation: typing.Callable[[], typing.Any]) -> None:
        ...


class CompilationRelaxations(IntEnum):
    """This class has no documentation."""

    NO_STRING_INTERNING = ...


class CompilationRelaxationsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def compilation_relaxations(self) -> int:
        ...

    @overload
    def __init__(self, relaxations: int) -> None:
        ...

    @overload
    def __init__(self, relaxations: System.Runtime.CompilerServices.CompilationRelaxations) -> None:
        ...


class IStrongBox(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def value(self) -> System.Object:
        ...

    @value.setter
    def value(self, value: System.Object) -> None:
        ...


class StrongBox(typing.Generic[System_Runtime_CompilerServices_StrongBox_T], System.Object, System.Runtime.CompilerServices.IStrongBox):
    """This class has no documentation."""

    @property
    def value(self) -> System_Runtime_CompilerServices_StrongBox_T:
        ...

    @value.setter
    def value(self, value: System_Runtime_CompilerServices_StrongBox_T) -> None:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: System_Runtime_CompilerServices_StrongBox_T) -> None:
        ...


class SkipLocalsInitAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IndexerNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self, indexer_name: str) -> None:
        ...


class LoadHint(IntEnum):
    """This class has no documentation."""

    DEFAULT = ...

    ALWAYS = ...

    SOMETIMES = ...


class RuntimeFeature(System.Object):
    """This class has no documentation."""

    IS_DYNAMIC_CODE_SUPPORTED: bool

    IS_DYNAMIC_CODE_COMPILED: bool

    PORTABLE_PDB: str = ...

    DEFAULT_IMPLEMENTATIONS_OF_INTERFACES: str = ...

    UNMANAGED_SIGNATURE_CALLING_CONVENTION: str = ...

    COVARIANT_RETURNS_OF_CLASSES: str = ...

    BY_REF_FIELDS: str = ...

    BY_REF_LIKE_GENERICS: str = ...

    VIRTUAL_STATICS_IN_INTERFACES: str = ...

    NUMERIC_INT_PTR: str = ...

    IS_MULTITHREADING_SUPPORTED: bool

    @staticmethod
    def is_supported(feature: str) -> bool:
        ...


class ExtensionMarkerAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def name(self) -> str:
        ...

    def __init__(self, name: str) -> None:
        ...


class FixedBufferAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def element_type(self) -> typing.Type:
        ...

    @property
    def length(self) -> int:
        ...

    def __init__(self, element_type: typing.Type, length: int) -> None:
        ...


class ModuleInitializerAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class InlineArray2(typing.Generic[System_Runtime_CompilerServices_InlineArray2_T]):
    """This class has no documentation."""


class InlineArray3(typing.Generic[System_Runtime_CompilerServices_InlineArray3_T]):
    """This class has no documentation."""


class InlineArray4(typing.Generic[System_Runtime_CompilerServices_InlineArray4_T]):
    """This class has no documentation."""


class InlineArray5(typing.Generic[System_Runtime_CompilerServices_InlineArray5_T]):
    """This class has no documentation."""


class InlineArray6(typing.Generic[System_Runtime_CompilerServices_InlineArray6_T]):
    """This class has no documentation."""


class InlineArray7(typing.Generic[System_Runtime_CompilerServices_InlineArray7_T]):
    """This class has no documentation."""


class InlineArray8(typing.Generic[System_Runtime_CompilerServices_InlineArray8_T]):
    """This class has no documentation."""


class InlineArray9(typing.Generic[System_Runtime_CompilerServices_InlineArray9_T]):
    """This class has no documentation."""


class InlineArray10(typing.Generic[System_Runtime_CompilerServices_InlineArray10_T]):
    """This class has no documentation."""


class InlineArray11(typing.Generic[System_Runtime_CompilerServices_InlineArray11_T]):
    """This class has no documentation."""


class InlineArray12(typing.Generic[System_Runtime_CompilerServices_InlineArray12_T]):
    """This class has no documentation."""


class InlineArray13(typing.Generic[System_Runtime_CompilerServices_InlineArray13_T]):
    """This class has no documentation."""


class InlineArray14(typing.Generic[System_Runtime_CompilerServices_InlineArray14_T]):
    """This class has no documentation."""


class InlineArray15(typing.Generic[System_Runtime_CompilerServices_InlineArray15_T]):
    """This class has no documentation."""


class InlineArray16(typing.Generic[System_Runtime_CompilerServices_InlineArray16_T]):
    """This class has no documentation."""


class DependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def dependent_assembly(self) -> str:
        ...

    @property
    def load_hint(self) -> System.Runtime.CompilerServices.LoadHint:
        ...

    def __init__(self, dependent_assembly_argument: str, load_hint_argument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class SuppressIldasmAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class ScopedRefAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class UnionAttribute(System.Attribute):
    """This class has no documentation."""


class ITuple(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def length(self) -> int:
        ...

    def __getitem__(self, index: int) -> typing.Any:
        ...


class ContractHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def raise_contract_failed_event(failure_kind: System.Diagnostics.Contracts.ContractFailureKind, user_message: str, condition_text: str, inner_exception: System.Exception) -> str:
        ...

    @staticmethod
    def trigger_failure(kind: System.Diagnostics.Contracts.ContractFailureKind, display_message: str, user_message: str, condition_text: str, inner_exception: System.Exception) -> None:
        ...


class InternalsVisibleToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def assembly_name(self) -> str:
        ...

    @property
    def all_internals_visible(self) -> bool:
        ...

    @all_internals_visible.setter
    def all_internals_visible(self, value: bool) -> None:
        ...

    def __init__(self, assembly_name: str) -> None:
        ...


class DisableRuntimeMarshallingAttribute(System.Attribute):
    """This class has no documentation."""


class AsyncStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, state_machine_type: typing.Type) -> None:
        ...


class IsByRefLikeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CompilerGlobalScopeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallerMemberNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class InterpolatedStringHandlerArgumentAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def arguments(self) -> typing.List[str]:
        ...

    @overload
    def __init__(self, argument: str) -> None:
        ...

    @overload
    def __init__(self, *arguments: typing.Union[str, typing.Iterable[str]]) -> None:
        ...


class DiscardableAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class _Typed_PoolingAsyncValueTaskMethodBuilder_Start(typing.Generic[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine]):
    """"""

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        ...


class _PoolingAsyncValueTaskMethodBuilder_Start:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine]) -> System.Runtime.CompilerServices._Typed_PoolingAsyncValueTaskMethodBuilder_Start[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine]:
        ...


class _Typed_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted(typing.Generic[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        ...


class _PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter]:
        ...


class _Typed_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted(typing.Generic[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]):
    """"""

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...

    @overload
    def __call__(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, state_machine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        ...


class _PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]) -> System.Runtime.CompilerServices._Typed_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter]:
        ...


class PoolingAsyncValueTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult]):
    """This class has no documentation."""

    @property
    def task(self) -> System.Threading.Tasks.ValueTask:
        ...

    @property
    def start(self) -> System.Runtime.CompilerServices._PoolingAsyncValueTaskMethodBuilder_Start:
        ...

    @property
    def await_on_completed(self) -> System.Runtime.CompilerServices._PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted:
        ...

    @property
    def await_unsafe_on_completed(self) -> System.Runtime.CompilerServices._PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted:
        ...

    @staticmethod
    def create() -> System.Runtime.CompilerServices.PoolingAsyncValueTaskMethodBuilder:
        ...

    def set_exception(self, exception: System.Exception) -> None:
        ...

    @overload
    def set_result(self) -> None:
        ...

    @overload
    def set_result(self, result: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult) -> None:
        ...

    def set_state_machine(self, state_machine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        ...


class FixedAddressValueTypeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class ConfiguredValueTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult]):
    """This class has no documentation."""

    def get_awaiter(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter:
        ...


class ParamCollectionAttribute(System.Attribute):
    """This class has no documentation."""


class NullableAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def nullable_flags(self) -> typing.List[int]:
        ...

    @nullable_flags.setter
    def nullable_flags(self, value: typing.List[int]) -> None:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self, value: typing.List[int]) -> None:
        ...


class FormattableStringFactory(System.Object):
    """This class has no documentation."""

    @staticmethod
    def create(format: str, *arguments: typing.Union[System.Object, typing.Iterable[System.Object]]) -> System.FormattableString:
        ...


class PreserveBaseOverridesAttribute(System.Attribute):
    """This class has no documentation."""


class MemorySafetyRulesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def version(self) -> int:
        ...

    def __init__(self, version: int) -> None:
        ...


class CompilerGeneratedAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class SwitchExpressionException(System.InvalidOperationException):
    """This class has no documentation."""

    @property
    def unmatched_value(self) -> System.Object:
        ...

    @property
    def message(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, inner_exception: System.Exception) -> None:
        ...

    @overload
    def __init__(self, unmatched_value: typing.Any) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner_exception: System.Exception) -> None:
        ...

    def get_object_data(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class NullableContextAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def flag(self) -> int:
        ...

    @flag.setter
    def flag(self, value: int) -> None:
        ...

    def __init__(self, value: int) -> None:
        ...


class UnsafeAccessorKind(IntEnum):
    """This class has no documentation."""

    CONSTRUCTOR = 0

    METHOD = 1

    STATIC_METHOD = 2

    FIELD = 3

    STATIC_FIELD = 4


class UnsafeAccessorAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def kind(self) -> System.Runtime.CompilerServices.UnsafeAccessorKind:
        ...

    @property
    def name(self) -> str:
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    def __init__(self, kind: System.Runtime.CompilerServices.UnsafeAccessorKind) -> None:
        ...


class EnumeratorCancellationAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvCdecl(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvFastcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvStdcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvSwift(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvSuppressGCTransition(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvThiscall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvMemberFunction(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IsVolatile(System.Object):
    """This class has no documentation."""


class IsClosedTypeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def derived_types(self) -> typing.List[typing.Type]:
        ...

    @derived_types.setter
    def derived_types(self, value: typing.List[typing.Type]) -> None:
        ...

    def __init__(self) -> None:
        ...


class RefSafetyRulesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def version(self) -> int:
        ...

    def __init__(self, version: int) -> None:
        ...


class UnsafeAccessorTypeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def type_name(self) -> str:
        ...

    def __init__(self, type_name: str) -> None:
        ...


class MethodCodeType(IntEnum):
    """This class has no documentation."""

    IL = ...

    NATIVE = ...

    OPTIL = ...

    RUNTIME = ...


class ConfiguredAsyncDisposable:
    """This class has no documentation."""

    def dispose_async(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
        ...


class _Typed_RuntimeHelpers_GetSubArray(typing.Generic[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]):
    """"""

    @overload
    def __call__(self, array: typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T], range: System.Range) -> typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]:
        ...


class _RuntimeHelpers_GetSubArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]) -> System.Runtime.CompilerServices._Typed_RuntimeHelpers_GetSubArray[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]:
        ...


class _Typed_RuntimeHelpers_CreateSpan(typing.Generic[System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T]):
    """"""

    @overload
    def __call__(self, fld_handle: System.RuntimeFieldHandle) -> System.ReadOnlySpan[System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T]:
        ...


class _RuntimeHelpers_CreateSpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T]) -> System.Runtime.CompilerServices._Typed_RuntimeHelpers_CreateSpan[System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T]:
        ...


class _Typed_RuntimeHelpers_IsReferenceOrContainsReferences(typing.Generic[System_Runtime_CompilerServices_RuntimeHelpers_IsReferenceOrContainsReferences_T]):
    """"""

    @overload
    def __call__(self) -> bool:
        ...


class _RuntimeHelpers_IsReferenceOrContainsReferences:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_RuntimeHelpers_IsReferenceOrContainsReferences_T]) -> System.Runtime.CompilerServices._Typed_RuntimeHelpers_IsReferenceOrContainsReferences[System_Runtime_CompilerServices_RuntimeHelpers_IsReferenceOrContainsReferences_T]:
        ...


class RuntimeHelpers(System.Object):
    """This class has no documentation."""

    OFFSET_TO_STRING_DATA: int

    get_sub_array: System.Runtime.CompilerServices._RuntimeHelpers_GetSubArray

    create_span: System.Runtime.CompilerServices._RuntimeHelpers_CreateSpan

    is_reference_or_contains_references: System.Runtime.CompilerServices._RuntimeHelpers_IsReferenceOrContainsReferences

    @staticmethod
    @overload
    def allocate_type_associated_memory(type: typing.Type, size: int) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def allocate_type_associated_memory(type: typing.Type, size: int, alignment: int) -> System.IntPtr:
        ...

    @staticmethod
    def box(target: int, type: System.RuntimeTypeHandle) -> System.Object:
        ...

    def cleanup_code(self, user_data: typing.Any, exception_thrown: bool) -> None:
        ...

    @staticmethod
    def ensure_sufficient_execution_stack() -> None:
        ...

    @staticmethod
    def equals(o_1: typing.Any, o_2: typing.Any) -> bool:
        ...

    @staticmethod
    def execute_code_with_guaranteed_cleanup(code: typing.Callable[[System.Object], typing.Any], backout_code: typing.Callable[[System.Object, bool], typing.Any], user_data: typing.Any) -> None:
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def get_hash_code(o: typing.Any) -> int:
        ...

    @staticmethod
    def get_object_value(obj: typing.Any) -> System.Object:
        ...

    @staticmethod
    def get_uninitialized_object(type: typing.Type) -> System.Object:
        ...

    @staticmethod
    def initialize_array(array: System.Array, fld_handle: System.RuntimeFieldHandle) -> None:
        ...

    @staticmethod
    def prepare_constrained_regions() -> None:
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def prepare_constrained_regions_no_op() -> None:
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def prepare_contracted_delegate(d: System.Delegate) -> None:
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def prepare_delegate(d: System.Delegate) -> None:
        ...

    @staticmethod
    @overload
    def prepare_method(method: System.RuntimeMethodHandle) -> None:
        ...

    @staticmethod
    @overload
    def prepare_method(method: System.RuntimeMethodHandle, instantiation: typing.List[System.RuntimeTypeHandle]) -> None:
        ...

    @staticmethod
    def probe_for_sufficient_stack() -> None:
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def run_class_constructor(type: System.RuntimeTypeHandle) -> None:
        ...

    @staticmethod
    def run_module_constructor(module: System.ModuleHandle) -> None:
        ...

    @staticmethod
    def size_of(type: System.RuntimeTypeHandle) -> int:
        ...

    def try_code(self, user_data: typing.Any) -> None:
        ...

    @staticmethod
    def try_ensure_sufficient_execution_stack() -> bool:
        ...


class RuntimeWrappedException(System.Exception):
    """This class has no documentation."""

    @property
    def wrapped_exception(self) -> System.Object:
        ...

    def __init__(self, thrown_object: typing.Any) -> None:
        ...

    def get_object_data(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class SpecialNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class AccessedThroughPropertyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def property_name(self) -> str:
        ...

    def __init__(self, property_name: str) -> None:
        ...


class DefaultDependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def load_hint(self) -> System.Runtime.CompilerServices.LoadHint:
        ...

    def __init__(self, load_hint_argument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class _Typed_DefaultInterpolatedStringHandler_AppendFormatted(typing.Generic[System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T]):
    """"""

    @overload
    def __call__(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T) -> None:
        ...

    @overload
    def __call__(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, format: str) -> None:
        ...

    @overload
    def __call__(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, alignment: int) -> None:
        ...

    @overload
    def __call__(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, alignment: int, format: str) -> None:
        ...


class _DefaultInterpolatedStringHandler_AppendFormatted:
    """"""

    @overload
    def __call__(self, value: System.ReadOnlySpan[str]) -> None:
        ...

    @overload
    def __call__(self, value: System.ReadOnlySpan[str], alignment: int = 0, format: str = None) -> None:
        ...

    @overload
    def __call__(self, value: str) -> None:
        ...

    @overload
    def __call__(self, value: str, alignment: int = 0, format: str = None) -> None:
        ...

    @overload
    def __call__(self, value: typing.Any, alignment: int = 0, format: str = None) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T]) -> System.Runtime.CompilerServices._Typed_DefaultInterpolatedStringHandler_AppendFormatted[System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T]:
        ...


class DefaultInterpolatedStringHandler:
    """This class has no documentation."""

    @property
    def text(self) -> System.ReadOnlySpan[str]:
        ...

    @property
    def append_formatted(self) -> System.Runtime.CompilerServices._DefaultInterpolatedStringHandler_AppendFormatted:
        ...

    @overload
    def __init__(self, literal_length: int, formatted_count: int) -> None:
        ...

    @overload
    def __init__(self, literal_length: int, formatted_count: int, provider: System.IFormatProvider) -> None:
        ...

    @overload
    def __init__(self, literal_length: int, formatted_count: int, provider: System.IFormatProvider, initial_buffer: System.Span[str]) -> None:
        ...

    def append_literal(self, value: str) -> None:
        ...

    def clear(self) -> None:
        ...

    def to_string(self) -> str:
        ...

    def to_string_and_clear(self) -> str:
        ...


class IsUnmanagedAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class AsyncMethodBuilderAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def builder_type(self) -> typing.Type:
        ...

    def __init__(self, builder_type: typing.Type) -> None:
        ...


class MethodImplOptions(IntEnum):
    """This class has no documentation."""

    UNMANAGED = ...

    NO_INLINING = ...

    FORWARD_REF = ...

    SYNCHRONIZED = ...

    NO_OPTIMIZATION = ...

    PRESERVE_SIG = ...

    AGGRESSIVE_INLINING = ...

    AGGRESSIVE_OPTIMIZATION = ...

    ASYNC = ...

    INTERNAL_CALL = ...


class CreateNewOnMetadataUpdateAttribute(System.Attribute):
    """This class has no documentation."""


class MetadataUpdateOriginalTypeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def original_type(self) -> typing.Type:
        ...

    def __init__(self, original_type: typing.Type) -> None:
        ...


class TypeForwardedFromAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def assembly_full_name(self) -> str:
        ...

    def __init__(self, assembly_full_name: str) -> None:
        ...


class IteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, state_machine_type: typing.Type) -> None:
        ...


class DecimalConstantAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> float:
        ...

    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None:
        ...


class TypeForwardedToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def destination(self) -> typing.Type:
        ...

    def __init__(self, destination: typing.Type) -> None:
        ...


class RuntimeCompatibilityAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def wrap_non_exception_throws(self) -> bool:
        ...

    @wrap_non_exception_throws.setter
    def wrap_non_exception_throws(self, value: bool) -> None:
        ...

    def __init__(self) -> None:
        ...


class _Typed_Unsafe_AsPointer(typing.Generic[System_Runtime_CompilerServices_Unsafe_AsPointer_T]):
    """"""

    @overload
    def __call__(self, value: System_Runtime_CompilerServices_Unsafe_AsPointer_T) -> typing.Any:
        ...


class _Unsafe_AsPointer:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_AsPointer_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_AsPointer[System_Runtime_CompilerServices_Unsafe_AsPointer_T]:
        ...


class _Typed_Unsafe_SizeOf(typing.Generic[System_Runtime_CompilerServices_Unsafe_SizeOf_T]):
    """"""

    @overload
    def __call__(self) -> int:
        ...


class _Unsafe_SizeOf:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_SizeOf_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_SizeOf[System_Runtime_CompilerServices_Unsafe_SizeOf_T]:
        ...


class _Typed_Unsafe_As(typing.Generic[System_Runtime_CompilerServices_Unsafe_As_T]):
    """"""

    @overload
    def __call__(self, o: typing.Any) -> System_Runtime_CompilerServices_Unsafe_As_T:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_As_TFrom) -> typing.Any:
        ...


class _Unsafe_As:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_As_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_As[System_Runtime_CompilerServices_Unsafe_As_T]:
        ...


class _Typed_Unsafe_Add(typing.Generic[System_Runtime_CompilerServices_Unsafe_Add_T]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Add_T, element_offset: int) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Add_T, element_offset: System.IntPtr) -> typing.Any:
        ...

    @overload
    def __call__(self, source: typing.Any, element_offset: int) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Add_T, element_offset: System.UIntPtr) -> typing.Any:
        ...


class _Unsafe_Add:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Add_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Add[System_Runtime_CompilerServices_Unsafe_Add_T]:
        ...


class _Typed_Unsafe_AddByteOffset(typing.Generic[System_Runtime_CompilerServices_Unsafe_AddByteOffset_T]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_AddByteOffset_T, byte_offset: System.UIntPtr) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_AddByteOffset_T, byte_offset: System.IntPtr) -> typing.Any:
        ...


class _Unsafe_AddByteOffset:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_AddByteOffset_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_AddByteOffset[System_Runtime_CompilerServices_Unsafe_AddByteOffset_T]:
        ...


class _Typed_Unsafe_AreSame(typing.Generic[System_Runtime_CompilerServices_Unsafe_AreSame_T]):
    """"""

    @overload
    def __call__(self, left: System_Runtime_CompilerServices_Unsafe_AreSame_T, right: System_Runtime_CompilerServices_Unsafe_AreSame_T) -> bool:
        ...


class _Unsafe_AreSame:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_AreSame_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_AreSame[System_Runtime_CompilerServices_Unsafe_AreSame_T]:
        ...


class _Typed_Unsafe_BitCast(typing.Generic[System_Runtime_CompilerServices_Unsafe_BitCast_TFrom]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_BitCast_TFrom) -> System_Runtime_CompilerServices_Unsafe_BitCast_TTo:
        ...


class _Unsafe_BitCast:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_BitCast_TFrom]) -> System.Runtime.CompilerServices._Typed_Unsafe_BitCast[System_Runtime_CompilerServices_Unsafe_BitCast_TFrom]:
        ...


class _Typed_Unsafe_Copy(typing.Generic[System_Runtime_CompilerServices_Unsafe_Copy_T]):
    """"""

    @overload
    def __call__(self, destination: typing.Any, source: System_Runtime_CompilerServices_Unsafe_Copy_T) -> None:
        ...

    @overload
    def __call__(self, destination: System_Runtime_CompilerServices_Unsafe_Copy_T, source: typing.Any) -> None:
        ...


class _Unsafe_Copy:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Copy_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Copy[System_Runtime_CompilerServices_Unsafe_Copy_T]:
        ...


class _Typed_Unsafe_IsAddressGreaterThan(typing.Generic[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T]):
    """"""

    @overload
    def __call__(self, left: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T) -> bool:
        ...


class _Unsafe_IsAddressGreaterThan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_IsAddressGreaterThan[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T]:
        ...


class _Typed_Unsafe_IsAddressGreaterThanOrEqualTo(typing.Generic[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T]):
    """"""

    @overload
    def __call__(self, left: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T) -> bool:
        ...


class _Unsafe_IsAddressGreaterThanOrEqualTo:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_IsAddressGreaterThanOrEqualTo[System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThanOrEqualTo_T]:
        ...


class _Typed_Unsafe_IsAddressLessThan(typing.Generic[System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T]):
    """"""

    @overload
    def __call__(self, left: System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T) -> bool:
        ...


class _Unsafe_IsAddressLessThan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_IsAddressLessThan[System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T]:
        ...


class _Typed_Unsafe_IsAddressLessThanOrEqualTo(typing.Generic[System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T]):
    """"""

    @overload
    def __call__(self, left: System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T) -> bool:
        ...


class _Unsafe_IsAddressLessThanOrEqualTo:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_IsAddressLessThanOrEqualTo[System_Runtime_CompilerServices_Unsafe_IsAddressLessThanOrEqualTo_T]:
        ...


class _Typed_Unsafe_ReadUnaligned(typing.Generic[System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T]):
    """"""

    @overload
    def __call__(self, source: typing.Any) -> System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        ...

    @overload
    def __call__(self, source: int) -> System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        ...


class _Unsafe_ReadUnaligned:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_ReadUnaligned[System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T]:
        ...


class _Typed_Unsafe_WriteUnaligned(typing.Generic[System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T]):
    """"""

    @overload
    def __call__(self, destination: typing.Any, value: System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        ...

    @overload
    def __call__(self, destination: int, value: System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        ...


class _Unsafe_WriteUnaligned:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_WriteUnaligned[System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T]:
        ...


class _Typed_Unsafe_Read(typing.Generic[System_Runtime_CompilerServices_Unsafe_Read_T]):
    """"""

    @overload
    def __call__(self, source: typing.Any) -> System_Runtime_CompilerServices_Unsafe_Read_T:
        ...


class _Unsafe_Read:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Read_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Read[System_Runtime_CompilerServices_Unsafe_Read_T]:
        ...


class _Typed_Unsafe_Write(typing.Generic[System_Runtime_CompilerServices_Unsafe_Write_T]):
    """"""

    @overload
    def __call__(self, destination: typing.Any, value: System_Runtime_CompilerServices_Unsafe_Write_T) -> None:
        ...


class _Unsafe_Write:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Write_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Write[System_Runtime_CompilerServices_Unsafe_Write_T]:
        ...


class _Typed_Unsafe_AsRef(typing.Generic[System_Runtime_CompilerServices_Unsafe_AsRef_T]):
    """"""

    @overload
    def __call__(self, source: typing.Any) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_AsRef_T) -> typing.Any:
        ...


class _Unsafe_AsRef:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_AsRef_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_AsRef[System_Runtime_CompilerServices_Unsafe_AsRef_T]:
        ...


class _Typed_Unsafe_ByteOffset(typing.Generic[System_Runtime_CompilerServices_Unsafe_ByteOffset_T]):
    """"""

    @overload
    def __call__(self, origin: System_Runtime_CompilerServices_Unsafe_ByteOffset_T, target: System_Runtime_CompilerServices_Unsafe_ByteOffset_T) -> System.IntPtr:
        ...


class _Unsafe_ByteOffset:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_ByteOffset_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_ByteOffset[System_Runtime_CompilerServices_Unsafe_ByteOffset_T]:
        ...


class _Typed_Unsafe_NullRef(typing.Generic[System_Runtime_CompilerServices_Unsafe_NullRef_T]):
    """"""

    @overload
    def __call__(self) -> typing.Any:
        ...


class _Unsafe_NullRef:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_NullRef_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_NullRef[System_Runtime_CompilerServices_Unsafe_NullRef_T]:
        ...


class _Typed_Unsafe_IsNullRef(typing.Generic[System_Runtime_CompilerServices_Unsafe_IsNullRef_T]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_IsNullRef_T) -> bool:
        ...


class _Unsafe_IsNullRef:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_IsNullRef_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_IsNullRef[System_Runtime_CompilerServices_Unsafe_IsNullRef_T]:
        ...


class _Typed_Unsafe_SkipInit(typing.Generic[System_Runtime_CompilerServices_Unsafe_SkipInit_T]):
    """"""

    @overload
    def __call__(self, value: typing.Optional[System_Runtime_CompilerServices_Unsafe_SkipInit_T]) -> typing.Tuple[None, System_Runtime_CompilerServices_Unsafe_SkipInit_T]:
        ...


class _Unsafe_SkipInit:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_SkipInit_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_SkipInit[System_Runtime_CompilerServices_Unsafe_SkipInit_T]:
        ...


class _Typed_Unsafe_Subtract(typing.Generic[System_Runtime_CompilerServices_Unsafe_Subtract_T]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Subtract_T, element_offset: int) -> typing.Any:
        ...

    @overload
    def __call__(self, source: typing.Any, element_offset: int) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Subtract_T, element_offset: System.IntPtr) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_Subtract_T, element_offset: System.UIntPtr) -> typing.Any:
        ...


class _Unsafe_Subtract:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Subtract_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Subtract[System_Runtime_CompilerServices_Unsafe_Subtract_T]:
        ...


class _Typed_Unsafe_SubtractByteOffset(typing.Generic[System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T]):
    """"""

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T, byte_offset: System.IntPtr) -> typing.Any:
        ...

    @overload
    def __call__(self, source: System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T, byte_offset: System.UIntPtr) -> typing.Any:
        ...


class _Unsafe_SubtractByteOffset:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_SubtractByteOffset[System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T]:
        ...


class _Typed_Unsafe_Unbox(typing.Generic[System_Runtime_CompilerServices_Unsafe_Unbox_T]):
    """"""

    @overload
    def __call__(self, box: typing.Any) -> typing.Any:
        ...


class _Unsafe_Unbox:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_Unsafe_Unbox_T]) -> System.Runtime.CompilerServices._Typed_Unsafe_Unbox[System_Runtime_CompilerServices_Unsafe_Unbox_T]:
        ...


class Unsafe(System.Object):
    """This class has no documentation."""

    as_pointer: System.Runtime.CompilerServices._Unsafe_AsPointer

    size_of: System.Runtime.CompilerServices._Unsafe_SizeOf

    As: System.Runtime.CompilerServices._Unsafe_As

    add: System.Runtime.CompilerServices._Unsafe_Add

    add_byte_offset: System.Runtime.CompilerServices._Unsafe_AddByteOffset

    are_same: System.Runtime.CompilerServices._Unsafe_AreSame

    bit_cast: System.Runtime.CompilerServices._Unsafe_BitCast

    copy: System.Runtime.CompilerServices._Unsafe_Copy

    is_address_greater_than: System.Runtime.CompilerServices._Unsafe_IsAddressGreaterThan

    is_address_greater_than_or_equal_to: System.Runtime.CompilerServices._Unsafe_IsAddressGreaterThanOrEqualTo

    is_address_less_than: System.Runtime.CompilerServices._Unsafe_IsAddressLessThan

    is_address_less_than_or_equal_to: System.Runtime.CompilerServices._Unsafe_IsAddressLessThanOrEqualTo

    read_unaligned: System.Runtime.CompilerServices._Unsafe_ReadUnaligned

    write_unaligned: System.Runtime.CompilerServices._Unsafe_WriteUnaligned

    read: System.Runtime.CompilerServices._Unsafe_Read

    write: System.Runtime.CompilerServices._Unsafe_Write

    as_ref: System.Runtime.CompilerServices._Unsafe_AsRef

    byte_offset: System.Runtime.CompilerServices._Unsafe_ByteOffset

    null_ref: System.Runtime.CompilerServices._Unsafe_NullRef

    is_null_ref: System.Runtime.CompilerServices._Unsafe_IsNullRef

    skip_init: System.Runtime.CompilerServices._Unsafe_SkipInit

    subtract: System.Runtime.CompilerServices._Unsafe_Subtract

    subtract_byte_offset: System.Runtime.CompilerServices._Unsafe_SubtractByteOffset

    unbox: System.Runtime.CompilerServices._Unsafe_Unbox

    @staticmethod
    @overload
    def copy_block(destination: typing.Any, source: typing.Any, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def copy_block(destination: int, source: int, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def copy_block_unaligned(destination: typing.Any, source: typing.Any, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def copy_block_unaligned(destination: int, source: int, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def init_block(start_address: typing.Any, value: int, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def init_block(start_address: int, value: int, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def init_block_unaligned(start_address: typing.Any, value: int, byte_count: int) -> None:
        ...

    @staticmethod
    @overload
    def init_block_unaligned(start_address: int, value: int, byte_count: int) -> None:
        ...


class MethodImplAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def method_code_type(self) -> System.Runtime.CompilerServices.MethodCodeType:
        ...

    @method_code_type.setter
    def method_code_type(self, value: System.Runtime.CompilerServices.MethodCodeType) -> None:
        ...

    @property
    def value(self) -> System.Runtime.CompilerServices.MethodImplOptions:
        ...

    @overload
    def __init__(self, method_impl_options: System.Runtime.CompilerServices.MethodImplOptions) -> None:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self) -> None:
        ...


class _Typed_ConditionalWeakTable_GetOrAdd(typing.Generic[System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg]):
    """"""

    @overload
    def __call__(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value_factory: typing.Callable[[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg], System_Runtime_CompilerServices_ConditionalWeakTable_TValue], factory_argument: System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...


class _ConditionalWeakTable_GetOrAdd:
    """"""

    @overload
    def __call__(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    @overload
    def __call__(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value_factory: typing.Callable[[System_Runtime_CompilerServices_ConditionalWeakTable_TKey], System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg]) -> System.Runtime.CompilerServices._Typed_ConditionalWeakTable_GetOrAdd[System_Runtime_CompilerServices_ConditionalWeakTable_GetOrAdd_TArg]:
        ...


class ConditionalWeakTable(typing.Generic[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue], System.Object, System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]]):
    """This class has no documentation."""

    @property
    def get_or_add(self) -> System.Runtime.CompilerServices._ConditionalWeakTable_GetOrAdd:
        ...

    def __init__(self) -> None:
        ...

    def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]]:
        ...

    def add(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        ...

    def add_or_update(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        ...

    def clear(self) -> None:
        ...

    def create_value_callback(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    def get_or_create_value(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    def get_value(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, create_value_callback: typing.Callable[[System_Runtime_CompilerServices_ConditionalWeakTable_TKey], System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    @overload
    def remove(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> bool:
        ...

    @overload
    def remove(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: typing.Optional[System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> typing.Tuple[bool, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]:
        ...

    def try_add(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> bool:
        ...

    def try_get_value(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: typing.Optional[System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> typing.Tuple[bool, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]:
        ...


class _EventContainer(typing.Generic[System_Runtime_CompilerServices__EventContainer_Callable, System_Runtime_CompilerServices__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Runtime_CompilerServices__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Runtime_CompilerServices__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Runtime_CompilerServices__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


