import asyncio
from typing import Coroutine, Any, Callable, Dict, Optional, TypeVar, cast
import functools

T = TypeVar("T")


def async_lru_cache():
    """
    Decorator that creates a simple cache for async functions with a single entry.
    Unlike functools.lru_cache, this properly caches the result of an awaited coroutine,
    not the coroutine object itself.
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, T]]):
        # Lock doesn't need to be nonlocal because it's only used within the wrapper function
        # and is properly captured in the closure
        lock = asyncio.Lock()

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            if hasattr(wrapper, "cache"):
                return cast(T, wrapper.cache)  # type: ignore

            async with lock:
                if hasattr(wrapper, "cache"):
                    return cast(T, wrapper.cache)  # type: ignore

                # Call the original function and await its result
                value = await func(*args, **kwargs)

                # Store result in cache
                wrapper.cache = value  # type: ignore
                return value

        return wrapper

    return decorator


def run_coroutine_in_appropriate_loop(coro: Coroutine[Any, Any, T]) -> T:
    """
    Runs a coroutine in the appropriate event loop context and returns its result.

    This handles three cases:
    1. Inside a running event loop - creates a future and waits for it
    2. Event loop exists but not running - runs until complete
    3. No event loop available - creates a new one with asyncio.run

    Returns:
        The result of the coroutine
    """
    # Try to run the coroutine in the current event loop if possible
    loop = asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    else:
        # If we're not in an async context, we can run until complete
        return loop.run_until_complete(coro)
