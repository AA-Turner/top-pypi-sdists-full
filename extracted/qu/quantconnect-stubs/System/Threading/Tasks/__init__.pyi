from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import System
import System.Collections.Generic
import System.Runtime.CompilerServices
import System.Threading
import System.Threading.Tasks
import System.Threading.Tasks.Sources

System_Threading_Tasks_Task = typing.Any
System_Threading_Tasks_ValueTask = typing.Any

System_Threading_Tasks_TaskFactory_TResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_TResult")
System_Threading_Tasks_TaskCompletionSource_TResult = typing.TypeVar("System_Threading_Tasks_TaskCompletionSource_TResult")
System_Threading_Tasks_Task_TResult = typing.TypeVar("System_Threading_Tasks_Task_TResult")
System_Threading_Tasks_ValueTask_TResult = typing.TypeVar("System_Threading_Tasks_ValueTask_TResult")
System_Threading_Tasks__EventContainer_Callable = typing.TypeVar("System_Threading_Tasks__EventContainer_Callable")
System_Threading_Tasks__EventContainer_ReturnType = typing.TypeVar("System_Threading_Tasks__EventContainer_ReturnType")
System_Threading_Tasks_TaskFactory_StartNew_TResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_StartNew_TResult")
System_Threading_Tasks_TaskFactory_FromAsync_TArg1 = typing.TypeVar("System_Threading_Tasks_TaskFactory_FromAsync_TArg1")
System_Threading_Tasks_TaskFactory_FromAsync_TArg2 = typing.TypeVar("System_Threading_Tasks_TaskFactory_FromAsync_TArg2")
System_Threading_Tasks_TaskFactory_FromAsync_TArg3 = typing.TypeVar("System_Threading_Tasks_TaskFactory_FromAsync_TArg3")
System_Threading_Tasks_TaskFactory_FromAsync_TResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_FromAsync_TResult")
System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult")
System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult")
System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult")
System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult = typing.TypeVar("System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult")
System_Threading_Tasks_Task_ContinueWith_TResult = typing.TypeVar("System_Threading_Tasks_Task_ContinueWith_TResult")
System_Threading_Tasks_Task_ContinueWith_TNewResult = typing.TypeVar("System_Threading_Tasks_Task_ContinueWith_TNewResult")
System_Threading_Tasks_Task_FromResult_TResult = typing.TypeVar("System_Threading_Tasks_Task_FromResult_TResult")
System_Threading_Tasks_Task_FromException_TResult = typing.TypeVar("System_Threading_Tasks_Task_FromException_TResult")
System_Threading_Tasks_Task_FromCanceled_TResult = typing.TypeVar("System_Threading_Tasks_Task_FromCanceled_TResult")
System_Threading_Tasks_Task_Run_TResult = typing.TypeVar("System_Threading_Tasks_Task_Run_TResult")
System_Threading_Tasks_Task_WhenAll_TResult = typing.TypeVar("System_Threading_Tasks_Task_WhenAll_TResult")
System_Threading_Tasks_Task_WhenAny_TResult = typing.TypeVar("System_Threading_Tasks_Task_WhenAny_TResult")
System_Threading_Tasks_Task_WhenEach_TResult = typing.TypeVar("System_Threading_Tasks_Task_WhenEach_TResult")
System_Threading_Tasks_ValueTask_FromResult_TResult = typing.TypeVar("System_Threading_Tasks_ValueTask_FromResult_TResult")
System_Threading_Tasks_ValueTask_FromCanceled_TResult = typing.TypeVar("System_Threading_Tasks_ValueTask_FromCanceled_TResult")
System_Threading_Tasks_ValueTask_FromException_TResult = typing.TypeVar("System_Threading_Tasks_ValueTask_FromException_TResult")
System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T = typing.TypeVar("System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T")
System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T = typing.TypeVar("System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T")
System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T = typing.TypeVar("System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T")
System_Threading_Tasks_TaskExtensions_Unwrap_TResult = typing.TypeVar("System_Threading_Tasks_TaskExtensions_Unwrap_TResult")


class UnobservedTaskExceptionEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def observed(self) -> bool:
        ...

    @property
    def exception(self) -> System.AggregateException:
        ...

    def __init__(self, exception: System.AggregateException) -> None:
        ...

    def set_observed(self) -> None:
        ...


class TaskScheduler(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def maximum_concurrency_level(self) -> int:
        ...

    DEFAULT: System.Threading.Tasks.TaskScheduler

    CURRENT: System.Threading.Tasks.TaskScheduler

    @property
    def id(self) -> int:
        ...

    unobserved_task_exception: _EventContainer[typing.Callable[[System.Object, System.Threading.Tasks.UnobservedTaskExceptionEventArgs], typing.Any], typing.Any]

    def __init__(self) -> None:
        ...

    @staticmethod
    def from_current_synchronization_context() -> System.Threading.Tasks.TaskScheduler:
        ...

    def get_scheduled_tasks(self) -> System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task]:
        ...

    def try_execute_task(self, task: System.Threading.Tasks.Task) -> bool:
        ...

    def try_execute_task_inline(self, task: System.Threading.Tasks.Task, task_was_previously_queued: bool) -> bool:
        ...


class TaskCreationOptions(IntEnum):
    """This class has no documentation."""

    NONE = ...

    PREFER_FAIRNESS = ...

    LONG_RUNNING = ...

    ATTACHED_TO_PARENT = ...

    DENY_CHILD_ATTACH = ...

    HIDE_SCHEDULER = ...

    RUN_CONTINUATIONS_ASYNCHRONOUSLY = ...


class TaskContinuationOptions(IntEnum):
    """This class has no documentation."""

    NONE = 0

    PREFER_FAIRNESS = ...

    LONG_RUNNING = ...

    ATTACHED_TO_PARENT = ...

    DENY_CHILD_ATTACH = ...

    HIDE_SCHEDULER = ...

    LAZY_CANCELLATION = ...

    RUN_CONTINUATIONS_ASYNCHRONOUSLY = ...

    NOT_ON_RAN_TO_COMPLETION = ...

    NOT_ON_FAULTED = ...

    NOT_ON_CANCELED = ...

    ONLY_ON_RAN_TO_COMPLETION = ...

    ONLY_ON_FAULTED = ...

    ONLY_ON_CANCELED = ...

    EXECUTE_SYNCHRONOUSLY = ...


class _Typed_TaskFactory_StartNew(typing.Generic[System_Threading_Tasks_TaskFactory_StartNew_TResult]):
    """"""

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_StartNew_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_StartNew_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_StartNew_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_StartNew_TResult], cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_StartNew_TResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_StartNew_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_StartNew_TResult], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_StartNew_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...


class _TaskFactory_StartNew:
    """"""

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any], cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskFactory_StartNew_TResult]) -> System.Threading.Tasks._Typed_TaskFactory_StartNew[System_Threading_Tasks_TaskFactory_StartNew_TResult]:
        ...


class _Typed_TaskFactory_FromAsync(typing.Generic[System_Threading_Tasks_TaskFactory_FromAsync_TArg1]):
    """"""

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_FromAsync_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_FromAsync_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[System_Threading_Tasks_TaskFactory_FromAsync_TArg1, System_Threading_Tasks_TaskFactory_FromAsync_TArg2, System_Threading_Tasks_TaskFactory_FromAsync_TArg3, typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], arg_1: System_Threading_Tasks_TaskFactory_FromAsync_TArg1, arg_2: System_Threading_Tasks_TaskFactory_FromAsync_TArg2, arg_3: System_Threading_Tasks_TaskFactory_FromAsync_TArg3, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...


class _TaskFactory_FromAsync:
    """"""

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], typing.Any], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], typing.Any], creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], typing.Any], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, async_result: System.IAsyncResult, end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, begin_method: typing.Callable[[typing.Callable[[System.IAsyncResult], typing.Any], System.Object], System.IAsyncResult], end_method: typing.Callable[[System.IAsyncResult], System_Threading_Tasks_TaskFactory_TResult], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskFactory_FromAsync_TArg1]) -> System.Threading.Tasks._Typed_TaskFactory_FromAsync[System_Threading_Tasks_TaskFactory_FromAsync_TArg1]:
        ...


class _Typed_TaskFactory_ContinueWhenAll(typing.Generic[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]):
    """"""

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...


class _TaskFactory_ContinueWhenAll:
    """"""

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task]], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task]], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task]], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[typing.List[System.Threading.Tasks.Task]], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[typing.List[System.Threading.Tasks.Task]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]) -> System.Threading.Tasks._Typed_TaskFactory_ContinueWhenAll[System_Threading_Tasks_TaskFactory_ContinueWhenAll_TAntecedentResult]:
        ...


class _Typed_TaskFactory_ContinueWhenAny(typing.Generic[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]):
    """"""

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TAntecedentResult]], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...


class _TaskFactory_ContinueWhenAny:
    """"""

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    @overload
    def __call__(self, tasks: typing.List[System.Threading.Tasks.Task], continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_TaskFactory_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskFactory_TResult]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]) -> System.Threading.Tasks._Typed_TaskFactory_ContinueWhenAny[System_Threading_Tasks_TaskFactory_ContinueWhenAny_TResult]:
        ...


class TaskFactory(typing.Generic[System_Threading_Tasks_TaskFactory_TResult], System.Object):
    """This class has no documentation."""

    @property
    def cancellation_token(self) -> System.Threading.CancellationToken:
        ...

    @property
    def scheduler(self) -> System.Threading.Tasks.TaskScheduler:
        ...

    @property
    def creation_options(self) -> System.Threading.Tasks.TaskCreationOptions:
        ...

    @property
    def continuation_options(self) -> System.Threading.Tasks.TaskContinuationOptions:
        ...

    @property
    def start_new(self) -> System.Threading.Tasks._TaskFactory_StartNew:
        ...

    @property
    def from_async(self) -> System.Threading.Tasks._TaskFactory_FromAsync:
        ...

    @property
    def continue_when_all(self) -> System.Threading.Tasks._TaskFactory_ContinueWhenAll:
        ...

    @property
    def continue_when_any(self) -> System.Threading.Tasks._TaskFactory_ContinueWhenAny:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, scheduler: System.Threading.Tasks.TaskScheduler) -> None:
        ...

    @overload
    def __init__(self, creation_options: System.Threading.Tasks.TaskCreationOptions, continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> None:
        ...

    @overload
    def __init__(self, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> None:
        ...


class TaskCompletionSource(typing.Generic[System_Threading_Tasks_TaskCompletionSource_TResult], System.Object):
    """This class has no documentation."""

    @property
    def task(self) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, state: typing.Any) -> None:
        ...

    @overload
    def __init__(self, state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def set_canceled(self) -> None:
        ...

    @overload
    def set_canceled(self, cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def set_exception(self, exception: System.Exception) -> None:
        ...

    @overload
    def set_exception(self, exceptions: System.Collections.Generic.IEnumerable[System.Exception]) -> None:
        ...

    @overload
    def set_from_task(self, completed_task: System.Threading.Tasks.Task) -> None:
        ...

    @overload
    def set_from_task(self, completed_task: System.Threading.Tasks.Task[System_Threading_Tasks_TaskCompletionSource_TResult]) -> None:
        ...

    @overload
    def set_result(self) -> None:
        ...

    @overload
    def set_result(self, result: System_Threading_Tasks_TaskCompletionSource_TResult) -> None:
        ...

    @overload
    def try_set_canceled(self) -> bool:
        ...

    @overload
    def try_set_canceled(self, cancellation_token: System.Threading.CancellationToken) -> bool:
        ...

    @overload
    def try_set_exception(self, exception: System.Exception) -> bool:
        ...

    @overload
    def try_set_exception(self, exceptions: System.Collections.Generic.IEnumerable[System.Exception]) -> bool:
        ...

    @overload
    def try_set_from_task(self, completed_task: System.Threading.Tasks.Task) -> bool:
        ...

    @overload
    def try_set_from_task(self, completed_task: System.Threading.Tasks.Task[System_Threading_Tasks_TaskCompletionSource_TResult]) -> bool:
        ...

    @overload
    def try_set_result(self) -> bool:
        ...

    @overload
    def try_set_result(self, result: System_Threading_Tasks_TaskCompletionSource_TResult) -> bool:
        ...


class TaskStatus(IntEnum):
    """This class has no documentation."""

    CREATED = 0

    WAITING_FOR_ACTIVATION = 1

    WAITING_TO_RUN = 2

    RUNNING = 3

    WAITING_FOR_CHILDREN_TO_COMPLETE = 4

    RAN_TO_COMPLETION = 5

    CANCELED = 6

    FAULTED = 7


class _Typed_Task_ContinueWith(typing.Generic[System_Threading_Tasks_Task_ContinueWith_TResult]):
    """"""

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_Task_ContinueWith_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_Task_ContinueWith_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_Task_ContinueWith_TResult], scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_Task_ContinueWith_TResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task], System_Threading_Tasks_Task_ContinueWith_TResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task, System.Object], System_Threading_Tasks_Task_ContinueWith_TResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task, System.Object], System_Threading_Tasks_Task_ContinueWith_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task, System.Object], System_Threading_Tasks_Task_ContinueWith_TResult], state: typing.Any, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task, System.Object], System_Threading_Tasks_Task_ContinueWith_TResult], state: typing.Any, continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task, System.Object], System_Threading_Tasks_Task_ContinueWith_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], System_Threading_Tasks_Task_ContinueWith_TNewResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], System_Threading_Tasks_Task_ContinueWith_TNewResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], System_Threading_Tasks_Task_ContinueWith_TNewResult], scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], System_Threading_Tasks_Task_ContinueWith_TNewResult], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], System_Threading_Tasks_Task_ContinueWith_TNewResult], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], System_Threading_Tasks_Task_ContinueWith_TNewResult], state: typing.Any) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], System_Threading_Tasks_Task_ContinueWith_TNewResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], System_Threading_Tasks_Task_ContinueWith_TNewResult], state: typing.Any, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], System_Threading_Tasks_Task_ContinueWith_TNewResult], state: typing.Any, continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...

    @overload
    def __call__(self, continuation_function: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], System_Threading_Tasks_Task_ContinueWith_TNewResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_ContinueWith_TNewResult]:
        ...


class _Task_ContinueWith:
    """"""

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task, System.Object], typing.Any], state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task, System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task, System.Object], typing.Any], state: typing.Any, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task, System.Object], typing.Any], state: typing.Any, continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task, System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], typing.Any], scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], typing.Any], continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult]], typing.Any], cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], typing.Any], state: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], typing.Any], state: typing.Any, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], typing.Any], state: typing.Any, continuation_options: System.Threading.Tasks.TaskContinuationOptions) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, continuation_action: typing.Callable[[System.Threading.Tasks.Task[System_Threading_Tasks_Task_TResult], System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken, continuation_options: System.Threading.Tasks.TaskContinuationOptions, scheduler: System.Threading.Tasks.TaskScheduler) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_ContinueWith_TResult]) -> System.Threading.Tasks._Typed_Task_ContinueWith[System_Threading_Tasks_Task_ContinueWith_TResult]:
        ...


class _Typed_Task_FromResult(typing.Generic[System_Threading_Tasks_Task_FromResult_TResult]):
    """"""

    @overload
    def __call__(self, result: System_Threading_Tasks_Task_FromResult_TResult) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_FromResult_TResult]:
        ...


class _Task_FromResult:
    """"""

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_FromResult_TResult]) -> System.Threading.Tasks._Typed_Task_FromResult[System_Threading_Tasks_Task_FromResult_TResult]:
        ...


class _Typed_Task_FromException(typing.Generic[System_Threading_Tasks_Task_FromException_TResult]):
    """"""

    @overload
    def __call__(self, exception: System.Exception) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_FromException_TResult]:
        ...


class _Task_FromException:
    """"""

    @overload
    def __call__(self, exception: System.Exception) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_FromException_TResult]) -> System.Threading.Tasks._Typed_Task_FromException[System_Threading_Tasks_Task_FromException_TResult]:
        ...


class _Typed_Task_FromCanceled(typing.Generic[System_Threading_Tasks_Task_FromCanceled_TResult]):
    """"""

    @overload
    def __call__(self, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_FromCanceled_TResult]:
        ...


class _Task_FromCanceled:
    """"""

    @overload
    def __call__(self, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_FromCanceled_TResult]) -> System.Threading.Tasks._Typed_Task_FromCanceled[System_Threading_Tasks_Task_FromCanceled_TResult]:
        ...


class _Typed_Task_Run(typing.Generic[System_Threading_Tasks_Task_Run_TResult]):
    """"""

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_Task_Run_TResult]) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System_Threading_Tasks_Task_Run_TResult], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]]) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[System_Threading_Tasks_Task_Run_TResult]:
        ...


class _Task_Run:
    """"""

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, action: typing.Callable[[], typing.Any], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System.Threading.Tasks.Task]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, function: typing.Callable[[], System.Threading.Tasks.Task], cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_Run_TResult]) -> System.Threading.Tasks._Typed_Task_Run[System_Threading_Tasks_Task_Run_TResult]:
        ...


class _Typed_Task_WhenAll(typing.Generic[System_Threading_Tasks_Task_WhenAll_TResult]):
    """"""

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAll_TResult]]) -> System.Threading.Tasks.Task[typing.List[System_Threading_Tasks_Task_WhenAll_TResult]]:
        ...

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAll_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAll_TResult]]]) -> System.Threading.Tasks.Task[typing.List[System_Threading_Tasks_Task_WhenAll_TResult]]:
        ...

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAll_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAll_TResult]]]) -> System.Threading.Tasks.Task[typing.List[System_Threading_Tasks_Task_WhenAll_TResult]]:
        ...


class _Task_WhenAll:
    """"""

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task]) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task, typing.Iterable[System.Threading.Tasks.Task]]) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_WhenAll_TResult]) -> System.Threading.Tasks._Typed_Task_WhenAll[System_Threading_Tasks_Task_WhenAll_TResult]:
        ...


class _Typed_Task_WhenAny(typing.Generic[System_Threading_Tasks_Task_WhenAny_TResult]):
    """"""

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]:
        ...

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]:
        ...

    @overload
    def __call__(self, task_1: System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult], task_2: System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]:
        ...

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenAny_TResult]]:
        ...


class _Task_WhenAny:
    """"""

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task, typing.Iterable[System.Threading.Tasks.Task]]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task]:
        ...

    @overload
    def __call__(self, task_1: System.Threading.Tasks.Task, task_2: System.Threading.Tasks.Task) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task]:
        ...

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task]) -> System.Threading.Tasks.Task[System.Threading.Tasks.Task]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_WhenAny_TResult]) -> System.Threading.Tasks._Typed_Task_WhenAny[System_Threading_Tasks_Task_WhenAny_TResult]:
        ...


class _Typed_Task_WhenEach(typing.Generic[System_Threading_Tasks_Task_WhenEach_TResult]):
    """"""

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]]) -> System.Collections.Generic.IAsyncEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]:
        ...

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult], typing.Iterable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]]) -> System.Collections.Generic.IAsyncEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]:
        ...

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]) -> System.Collections.Generic.IAsyncEnumerable[System.Threading.Tasks.Task[System_Threading_Tasks_Task_WhenEach_TResult]]:
        ...


class _Task_WhenEach:
    """"""

    @overload
    def __call__(self, *tasks: typing.Union[System.Threading.Tasks.Task, typing.Iterable[System.Threading.Tasks.Task]]) -> System.Collections.Generic.IAsyncEnumerable[System.Threading.Tasks.Task]:
        ...

    @overload
    def __call__(self, tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task]) -> System.Collections.Generic.IAsyncEnumerable[System.Threading.Tasks.Task]:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_Task_WhenEach_TResult]) -> System.Threading.Tasks._Typed_Task_WhenEach[System_Threading_Tasks_Task_WhenEach_TResult]:
        ...


class ConfigureAwaitOptions(IntEnum):
    """This class has no documentation."""

    NONE = ...

    CONTINUE_ON_CAPTURED_CONTEXT = ...

    SUPPRESS_THROWING = ...

    FORCE_YIELDING = ...


class Task(typing.Generic[System_Threading_Tasks_Task_TResult], System_Threading_Tasks_Task):
    """This class has no documentation."""

    @property
    def id(self) -> int:
        ...

    CURRENT_ID: typing.Optional[int]

    @property
    def exception(self) -> System.AggregateException:
        ...

    @property
    def status(self) -> System.Threading.Tasks.TaskStatus:
        ...

    @property
    def is_canceled(self) -> bool:
        ...

    @property
    def is_completed(self) -> bool:
        ...

    @property
    def is_completed_successfully(self) -> bool:
        ...

    @property
    def creation_options(self) -> System.Threading.Tasks.TaskCreationOptions:
        ...

    @property
    def async_state(self) -> System.Object:
        ...

    FACTORY: System.Threading.Tasks.TaskFactory

    COMPLETED_TASK: System.Threading.Tasks.Task

    @property
    def is_faulted(self) -> bool:
        ...

    @property
    def result(self) -> System_Threading_Tasks_Task_TResult:
        ...

    @property
    def continue_with(self) -> System.Threading.Tasks._Task_ContinueWith:
        ...

    from_result: System.Threading.Tasks._Task_FromResult

    from_exception: System.Threading.Tasks._Task_FromException

    from_canceled: System.Threading.Tasks._Task_FromCanceled

    run: System.Threading.Tasks._Task_Run

    when_all: System.Threading.Tasks._Task_WhenAll

    when_any: System.Threading.Tasks._Task_WhenAny

    when_each: System.Threading.Tasks._Task_WhenEach

    @overload
    def __init__(self, action: typing.Callable[[], typing.Any]) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[], typing.Any], cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[], typing.Any], creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[], typing.Any], cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, action: typing.Callable[[System.Object], typing.Any], state: typing.Any, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[], System_Threading_Tasks_Task_TResult]) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[], System_Threading_Tasks_Task_TResult], cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[], System_Threading_Tasks_Task_TResult], creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[], System_Threading_Tasks_Task_TResult], cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_Task_TResult], state: typing.Any) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_Task_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_Task_TResult], state: typing.Any, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def __init__(self, function: typing.Callable[[System.Object], System_Threading_Tasks_Task_TResult], state: typing.Any, cancellation_token: System.Threading.CancellationToken, creation_options: System.Threading.Tasks.TaskCreationOptions) -> None:
        ...

    @overload
    def configure_await(self, continue_on_captured_context: bool) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable:
        ...

    @overload
    def configure_await(self, options: System.Threading.Tasks.ConfigureAwaitOptions) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable:
        ...

    @staticmethod
    @overload
    def delay(delay: datetime.timedelta) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def delay(delay: datetime.timedelta, time_provider: System.TimeProvider) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def delay(delay: datetime.timedelta, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def delay(delay: datetime.timedelta, time_provider: System.TimeProvider, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def delay(milliseconds_delay: int) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def delay(milliseconds_delay: int, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def dispose(self) -> None:
        ...

    @overload
    def dispose(self, disposing: bool) -> None:
        ...

    def get_awaiter(self) -> System.Runtime.CompilerServices.TaskAwaiter:
        ...

    @overload
    def run_synchronously(self) -> None:
        ...

    @overload
    def run_synchronously(self, scheduler: System.Threading.Tasks.TaskScheduler) -> None:
        ...

    @overload
    def start(self) -> None:
        ...

    @overload
    def start(self, scheduler: System.Threading.Tasks.TaskScheduler) -> None:
        ...

    @overload
    def wait(self) -> None:
        ...

    @overload
    def wait(self, timeout: datetime.timedelta) -> bool:
        ...

    @overload
    def wait(self, timeout: datetime.timedelta, cancellation_token: System.Threading.CancellationToken) -> bool:
        ...

    @overload
    def wait(self, cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def wait(self, milliseconds_timeout: int) -> bool:
        ...

    @overload
    def wait(self, milliseconds_timeout: int, cancellation_token: System.Threading.CancellationToken) -> bool:
        ...

    @staticmethod
    @overload
    def wait_all(*tasks: typing.Union[System.Threading.Tasks.Task, typing.Iterable[System.Threading.Tasks.Task]]) -> None:
        ...

    @staticmethod
    @overload
    def wait_all(tasks: typing.List[System.Threading.Tasks.Task], timeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    @overload
    def wait_all(tasks: typing.List[System.Threading.Tasks.Task], milliseconds_timeout: int) -> bool:
        ...

    @staticmethod
    @overload
    def wait_all(tasks: typing.List[System.Threading.Tasks.Task], cancellation_token: System.Threading.CancellationToken) -> None:
        ...

    @staticmethod
    @overload
    def wait_all(tasks: typing.List[System.Threading.Tasks.Task], milliseconds_timeout: int, cancellation_token: System.Threading.CancellationToken) -> bool:
        ...

    @staticmethod
    @overload
    def wait_all(tasks: System.Collections.Generic.IEnumerable[System.Threading.Tasks.Task], cancellation_token: System.Threading.CancellationToken = ...) -> None:
        ...

    @staticmethod
    @overload
    def wait_any(*tasks: typing.Union[System.Threading.Tasks.Task, typing.Iterable[System.Threading.Tasks.Task]]) -> int:
        ...

    @staticmethod
    @overload
    def wait_any(tasks: typing.List[System.Threading.Tasks.Task], timeout: datetime.timedelta) -> int:
        ...

    @staticmethod
    @overload
    def wait_any(tasks: typing.List[System.Threading.Tasks.Task], cancellation_token: System.Threading.CancellationToken) -> int:
        ...

    @staticmethod
    @overload
    def wait_any(tasks: typing.List[System.Threading.Tasks.Task], milliseconds_timeout: int) -> int:
        ...

    @staticmethod
    @overload
    def wait_any(tasks: typing.List[System.Threading.Tasks.Task], milliseconds_timeout: int, cancellation_token: System.Threading.CancellationToken) -> int:
        ...

    @overload
    def wait_async(self, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def wait_async(self, timeout: datetime.timedelta) -> System.Threading.Tasks.Task:
        ...

    @overload
    def wait_async(self, timeout: datetime.timedelta, time_provider: System.TimeProvider) -> System.Threading.Tasks.Task:
        ...

    @overload
    def wait_async(self, timeout: datetime.timedelta, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @overload
    def wait_async(self, timeout: datetime.timedelta, time_provider: System.TimeProvider, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    def Yield() -> System.Runtime.CompilerServices.YieldAwaitable:
        ...


class _Typed_ValueTask_FromResult(typing.Generic[System_Threading_Tasks_ValueTask_FromResult_TResult]):
    """"""

    @overload
    def __call__(self, result: System_Threading_Tasks_ValueTask_FromResult_TResult) -> System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_FromResult_TResult]:
        ...


class _ValueTask_FromResult:
    """"""

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_ValueTask_FromResult_TResult]) -> System.Threading.Tasks._Typed_ValueTask_FromResult[System_Threading_Tasks_ValueTask_FromResult_TResult]:
        ...


class _Typed_ValueTask_FromCanceled(typing.Generic[System_Threading_Tasks_ValueTask_FromCanceled_TResult]):
    """"""

    @overload
    def __call__(self, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_FromCanceled_TResult]:
        ...


class _ValueTask_FromCanceled:
    """"""

    @overload
    def __call__(self, cancellation_token: System.Threading.CancellationToken) -> System.Threading.Tasks.ValueTask:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_ValueTask_FromCanceled_TResult]) -> System.Threading.Tasks._Typed_ValueTask_FromCanceled[System_Threading_Tasks_ValueTask_FromCanceled_TResult]:
        ...


class _Typed_ValueTask_FromException(typing.Generic[System_Threading_Tasks_ValueTask_FromException_TResult]):
    """"""

    @overload
    def __call__(self, exception: System.Exception) -> System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_FromException_TResult]:
        ...


class _ValueTask_FromException:
    """"""

    @overload
    def __call__(self, exception: System.Exception) -> System.Threading.Tasks.ValueTask:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_ValueTask_FromException_TResult]) -> System.Threading.Tasks._Typed_ValueTask_FromException[System_Threading_Tasks_ValueTask_FromException_TResult]:
        ...


class ValueTask(typing.Generic[System_Threading_Tasks_ValueTask_TResult], System.IEquatable[System_Threading_Tasks_ValueTask]):
    """This class has no documentation."""

    COMPLETED_TASK: System.Threading.Tasks.ValueTask

    @property
    def is_completed(self) -> bool:
        ...

    @property
    def is_completed_successfully(self) -> bool:
        ...

    @property
    def is_faulted(self) -> bool:
        ...

    @property
    def is_canceled(self) -> bool:
        ...

    @property
    def result(self) -> System_Threading_Tasks_ValueTask_TResult:
        ...

    from_result: System.Threading.Tasks._ValueTask_FromResult

    from_canceled: System.Threading.Tasks._ValueTask_FromCanceled

    from_exception: System.Threading.Tasks._ValueTask_FromException

    @overload
    def __eq__(self, right: System.Threading.Tasks.ValueTask) -> bool:
        ...

    @overload
    def __eq__(self, right: System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_TResult]) -> bool:
        ...

    @overload
    def __init__(self, task: System.Threading.Tasks.Task) -> None:
        ...

    @overload
    def __init__(self, source: System.Threading.Tasks.Sources.IValueTaskSource, token: int) -> None:
        ...

    @overload
    def __init__(self, result: System_Threading_Tasks_ValueTask_TResult) -> None:
        ...

    @overload
    def __init__(self, task: System.Threading.Tasks.Task[System_Threading_Tasks_ValueTask_TResult]) -> None:
        ...

    @overload
    def __init__(self, source: System.Threading.Tasks.Sources.IValueTaskSource[System_Threading_Tasks_ValueTask_TResult], token: int) -> None:
        ...

    @overload
    def __ne__(self, right: System.Threading.Tasks.ValueTask) -> bool:
        ...

    @overload
    def __ne__(self, right: System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_TResult]) -> bool:
        ...

    def as_task(self) -> System.Threading.Tasks.Task:
        ...

    def configure_await(self, continue_on_captured_context: bool) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Threading.Tasks.ValueTask) -> bool:
        ...

    @overload
    def equals(self, other: System.Threading.Tasks.ValueTask[System_Threading_Tasks_ValueTask_TResult]) -> bool:
        ...

    def get_awaiter(self) -> System.Runtime.CompilerServices.ValueTaskAwaiter:
        ...

    def get_hash_code(self) -> int:
        ...

    def preserve(self) -> System.Threading.Tasks.ValueTask:
        ...

    def to_string(self) -> str:
        ...


class TaskCanceledException(System.OperationCanceledException):
    """This class has no documentation."""

    @property
    def task(self) -> System.Threading.Tasks.Task:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner_exception: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, inner_exception: System.Exception, token: System.Threading.CancellationToken) -> None:
        ...

    @overload
    def __init__(self, task: System.Threading.Tasks.Task) -> None:
        ...


class _Typed_TaskAsyncEnumerableExtensions_ToBlockingEnumerable(typing.Generic[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IAsyncEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T], cancellation_token: System.Threading.CancellationToken = ...) -> System.Collections.Generic.IEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T]:
        ...


class _TaskAsyncEnumerableExtensions_ToBlockingEnumerable:
    """"""

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T]) -> System.Threading.Tasks._Typed_TaskAsyncEnumerableExtensions_ToBlockingEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ToBlockingEnumerable_T]:
        ...


class _Typed_TaskAsyncEnumerableExtensions_ConfigureAwait(typing.Generic[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IAsyncEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T], continue_on_captured_context: bool) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T]:
        ...


class _TaskAsyncEnumerableExtensions_ConfigureAwait:
    """"""

    @overload
    def __call__(self, source: System.IAsyncDisposable, continue_on_captured_context: bool) -> System.Runtime.CompilerServices.ConfiguredAsyncDisposable:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T]) -> System.Threading.Tasks._Typed_TaskAsyncEnumerableExtensions_ConfigureAwait[System_Threading_Tasks_TaskAsyncEnumerableExtensions_ConfigureAwait_T]:
        ...


class _Typed_TaskAsyncEnumerableExtensions_WithCancellation(typing.Generic[System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T]):
    """"""

    @overload
    def __call__(self, source: System.Collections.Generic.IAsyncEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T], cancellation_token: System.Threading.CancellationToken) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T]:
        ...


class _TaskAsyncEnumerableExtensions_WithCancellation:
    """"""

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T]) -> System.Threading.Tasks._Typed_TaskAsyncEnumerableExtensions_WithCancellation[System_Threading_Tasks_TaskAsyncEnumerableExtensions_WithCancellation_T]:
        ...


class TaskAsyncEnumerableExtensions(System.Object):
    """This class has no documentation."""

    to_blocking_enumerable: System.Threading.Tasks._TaskAsyncEnumerableExtensions_ToBlockingEnumerable

    configure_await: System.Threading.Tasks._TaskAsyncEnumerableExtensions_ConfigureAwait

    with_cancellation: System.Threading.Tasks._TaskAsyncEnumerableExtensions_WithCancellation


class _Typed_TaskExtensions_Unwrap(typing.Generic[System_Threading_Tasks_TaskExtensions_Unwrap_TResult]):
    """"""

    @overload
    def __call__(self, task: System.Threading.Tasks.Task[System.Threading.Tasks.Task[System_Threading_Tasks_TaskExtensions_Unwrap_TResult]]) -> System.Threading.Tasks.Task[System_Threading_Tasks_TaskExtensions_Unwrap_TResult]:
        ...


class _TaskExtensions_Unwrap:
    """"""

    @overload
    def __call__(self, task: System.Threading.Tasks.Task[System.Threading.Tasks.Task]) -> System.Threading.Tasks.Task:
        ...

    def __getitem__(self, type: typing.Type[System_Threading_Tasks_TaskExtensions_Unwrap_TResult]) -> System.Threading.Tasks._Typed_TaskExtensions_Unwrap[System_Threading_Tasks_TaskExtensions_Unwrap_TResult]:
        ...


class TaskExtensions(System.Object):
    """This class has no documentation."""

    unwrap: System.Threading.Tasks._TaskExtensions_Unwrap


class TaskSchedulerException(System.Exception):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, inner_exception: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, inner_exception: System.Exception) -> None:
        ...


class ConcurrentExclusiveSchedulerPair(System.Object):
    """This class has no documentation."""

    @property
    def completion(self) -> System.Threading.Tasks.Task:
        ...

    @property
    def concurrent_scheduler(self) -> System.Threading.Tasks.TaskScheduler:
        ...

    @property
    def exclusive_scheduler(self) -> System.Threading.Tasks.TaskScheduler:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, task_scheduler: System.Threading.Tasks.TaskScheduler) -> None:
        ...

    @overload
    def __init__(self, task_scheduler: System.Threading.Tasks.TaskScheduler, max_concurrency_level: int) -> None:
        ...

    @overload
    def __init__(self, task_scheduler: System.Threading.Tasks.TaskScheduler, max_concurrency_level: int, max_items_per_task: int) -> None:
        ...

    def complete(self) -> None:
        ...


class _EventContainer(typing.Generic[System_Threading_Tasks__EventContainer_Callable, System_Threading_Tasks__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Threading_Tasks__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Threading_Tasks__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Threading_Tasks__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


