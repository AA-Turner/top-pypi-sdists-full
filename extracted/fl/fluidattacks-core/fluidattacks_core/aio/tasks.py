import asyncio
from collections.abc import AsyncIterator, Awaitable, Coroutine, Iterable
from typing import Any, Literal, TypeVar, overload

T = TypeVar("T")


async def as_completed(
    coroutines: Iterable[Awaitable[T]],
    *,
    concurrency_limit: int | None = None,
) -> AsyncIterator[Awaitable[T]]:
    """Run coroutines concurrently, yielding results in order of completion.

    Args:
        coroutines: An iterable of coroutines.
        concurrency_limit: Maximum number of concurrent coroutines.

    Yields:
        Results from the coroutines in the order they complete.

    """
    if concurrency_limit:
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def _run(coroutine: Awaitable[T]) -> T:
            async with semaphore:
                return await coroutine
    else:

        async def _run(coroutine: Awaitable[T]) -> T:
            return await coroutine

    tasks = [_run(coroutine) for coroutine in coroutines]
    for task in asyncio.as_completed(tasks):
        yield task


@overload
async def gather(
    coroutines: Iterable[Awaitable[T]],
    *,
    concurrency_limit: int | None = None,
    return_exceptions: Literal[False] = False,
) -> list[T]: ...


@overload
async def gather(
    coroutines: Iterable[Awaitable[T]],
    *,
    concurrency_limit: int | None = None,
    return_exceptions: Literal[True],
) -> list[T | BaseException]: ...


async def gather(
    coroutines: Iterable[Awaitable[T]],
    *,
    concurrency_limit: int | None = None,
    return_exceptions: bool = False,
) -> list[T] | list[T | BaseException]:
    """Run coroutines concurrently.

    Args:
        coroutines: An iterable of coroutines.
        concurrency_limit: Maximum number of concurrent coroutines.
        return_exceptions: Whether to return exceptions instead of raising them.

    Returns:
        A list of results or exceptions.

    Raises:
        Exception: If return_exceptions is False and any coroutine raises an exception.

    """
    if concurrency_limit:
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def _run(coroutine: Awaitable[T]) -> T:
            async with semaphore:
                return await coroutine
    else:

        async def _run(coroutine: Awaitable[T]) -> T:
            return await coroutine

    tasks = [_run(coroutine) for coroutine in coroutines]
    return await asyncio.gather(*tasks, return_exceptions=return_exceptions)


BACKGROUND_TASKS = set[asyncio.Task[Any]]()


def to_background(coroutine: Coroutine[Any, Any, T]) -> None:
    """Run a coroutine in the background, fire-and-forget style."""
    task = asyncio.create_task(coroutine)
    BACKGROUND_TASKS.add(task)
    task.add_done_callback(BACKGROUND_TASKS.discard)
