import asyncio
import inspect
from asyncio import Task
from typing import Any, Coroutine, Iterable, List, Set, Tuple, TypeVar, overload

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")

# a coroutine alias type with only a return type but no yield type or send type
Invokable = Coroutine[None, None, T]


def _make_task(aw: Invokable[T]) -> Task:
    "Wraps a coroutine into a task, and schedules its execution."

    if not inspect.iscoroutine(aw):
        raise TypeError("not a coroutine")

    return asyncio.create_task(aw)


async def wait_n(coroutines: Iterable[Invokable[None]], *, concurrency: int) -> None:
    """
    Waits for all coroutines to complete, scheduling at most a fixed number of tasks concurrently.

    :param coroutines: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    iterator = iter(coroutines)
    pending = set(
        _make_task(coroutine) for _, coroutine in zip(range(concurrency), iterator)
    )
    try:
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task.cancelled():
                    raise asyncio.CancelledError
                exc = task.exception()
                if exc:
                    raise exc

            # schedule some tasks up to degree of concurrency
            for _, coroutine in zip(range(len(done)), iterator):
                pending.add(_make_task(coroutine))
    finally:
        # cancel remaining unscheduled tasks
        for coroutine in iterator:
            pending.add(_make_task(coroutine))
        if pending:
            for task in pending:
                task.cancel()
            await asyncio.wait(pending)


def _task_result(task: Task) -> Any:
    "Unwraps the result or exception from a task."

    exc = task.exception()
    if exc:
        return exc
    else:
        return task.result()


async def _gather_n(
    coroutines: Iterable[Invokable[T]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Iterable[T]:
    """
    Invokes coroutine objects, with at most the specified degree of concurrency.

    :param coroutines: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :param return_exceptions: If true, exceptions are treated the same as successful results;
        if false, the first raised exception is immediately propagated.
    :returns: Results returned by coroutines, in the order corresponding to the input sequence.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    iterator = iter(coroutines)

    tasks: List[Task] = []
    pending: Set[Task] = set()
    for _, coroutine in zip(range(concurrency), iterator):
        task = _make_task(coroutine)
        tasks.append(task)
        pending.add(task)

    try:
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task.cancelled():
                    raise asyncio.CancelledError
                exc = task.exception()
                if exc and not return_exceptions:
                    raise exc

            # schedule some tasks up to degree of concurrency
            for _, coroutine in zip(range(len(done)), iterator):
                task = _make_task(coroutine)
                tasks.append(task)
                pending.add(task)
    finally:
        # cancel remaining unscheduled tasks
        for coroutine in iterator:
            task = _make_task(coroutine)
            tasks.append(task)
            pending.add(task)
        if pending:
            for task in pending:
                task.cancel()
            await asyncio.wait(pending)

    return (_task_result(task) for task in tasks)


@overload
async def gather_n(
    coroutines: List[Invokable[T]], *, concurrency: int, return_exceptions: bool = False
) -> List[T]:
    ...


@overload
async def gather_n(
    coroutines: Tuple[Invokable[T1], Invokable[T2]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2]:
    ...


@overload
async def gather_n(
    coroutines: Tuple[Invokable[T1], Invokable[T2], Invokable[T3]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2, T3]:
    ...


@overload
async def gather_n(
    coroutines: Tuple[Invokable[T1], Invokable[T2], Invokable[T3], Invokable[T4]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2, T3, T4]:
    ...


async def gather_n(
    coroutines: Iterable[Invokable[T]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Iterable[T]:
    """
    Runs awaitable objects, with at most the specified degree of concurrency.

    :param awaitables: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :param return_exceptions: If true, exceptions are treated the same as successful results;
        if false, the first raised exception is immediately propagated.
    :returns: Results returned by coroutines, in the order corresponding to the input sequence.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    results = await _gather_n(
        coroutines, concurrency=concurrency, return_exceptions=return_exceptions
    )

    if isinstance(coroutines, list):
        return list(results)
    elif isinstance(coroutines, tuple):
        return tuple(results)
    else:
        return results
