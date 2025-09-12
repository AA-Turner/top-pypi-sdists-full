import asyncio
import logging
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Coroutine, Iterable
from contextlib import suppress
from typing import Any, Literal, TypeVar, cast, overload

T = TypeVar("T")

# Sentinel object to signal generator completion
_GENERATOR_DONE_SENTINEL = object()

# Logger for the aio module
_LOGGER = logging.getLogger(__name__)


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


async def _consume_generator(
    gen: AsyncGenerator[T, None],
    queue: asyncio.Queue[T | object],
    active_generators: list[int],
) -> None:
    """Consume a single generator and put its items in the queue.

    Args:
        gen: The async generator to consume.
        queue: The queue to put items into.
        active_generators: A list containing the count of active generators.

    """
    active_generators[0] += 1
    try:
        async for item in gen:
            await queue.put(item)
    except Exception:
        _LOGGER.exception(
            "Error consuming generator %s, unhandled exception",
            gen,
        )
    finally:
        active_generators[0] -= 1
        await queue.put(_GENERATOR_DONE_SENTINEL)


async def merge_async_generators(
    generators: Iterable[AsyncGenerator[T, None]],
    limit: int,
) -> AsyncGenerator[T, None]:
    """Merge multiple async generators into a single async generator with concurrency control.

    This function runs multiple async generators concurrently, yielding items as they become
    available. It maintains a maximum number of active generators specified by the limit.

    Args:
        generators: An iterable of async generators to merge.
        limit: Maximum number of generators to run concurrently.

    Yields:
        Items from the generators as they become available.

    Raises:
        ValueError: If limit is less than 1.

    Example:
        >>> async def gen1():
        ...     yield 1
        ...     yield 2
        >>> async def gen2():
        ...     yield 3
        ...     yield 4
        >>> async for item in merge_async_generators([gen1(), gen2()], limit=2):
        ...     print(item)  # May print 1, 3, 2, 4 in any order

    """
    if limit < 1:
        raise ValueError("limit must be at least 1")

    queue: asyncio.Queue[T | object] = asyncio.Queue()
    active_generators = [0]  # Use list to allow modification in nested function
    tasks: list[asyncio.Task[None]] = []

    gen_iter = iter(generators)

    # Start initial tasks up to the limit
    for _ in range(limit):
        try:
            gen = next(gen_iter)
            tasks.append(asyncio.create_task(_consume_generator(gen, queue, active_generators)))
        except StopIteration:
            break

    # Keep track of how many generators we expect to finish
    expected_done_signals = len(tasks)
    done_signals_received = 0

    try:
        while done_signals_received < expected_done_signals:
            item = await queue.get()
            if item is _GENERATOR_DONE_SENTINEL:
                done_signals_received += 1
                # Try to start a new task if there are more generators
                with suppress(StopIteration):
                    next_gen = next(gen_iter)
                    tasks.append(
                        asyncio.create_task(_consume_generator(next_gen, queue, active_generators)),
                    )
                    expected_done_signals += 1
            else:
                yield cast("T", item)
    finally:
        # Ensure all tasks are complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
