import asyncio
import functools
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

import grpc
import grpc.aio

from langgraph_api.feature_flags import IS_POSTGRES_BACKEND

P = ParamSpec("P")
T = TypeVar("T")


class RetryableException(Exception):
    pass


if IS_POSTGRES_BACKEND:
    from psycopg.errors import (  # type: ignore[import-not-found]
        ConnectionTimeout,
        InternalError,
        OperationalError,
        UndefinedTable,
    )
    from psycopg_pool.errors import (  # type: ignore[import-not-found]
        PoolTimeout,
        TooManyRequests,
    )

    RETRIABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
        OperationalError,
        InternalError,
        RetryableException,
    )
    OVERLOADED_EXCEPTIONS: tuple[type[BaseException], ...] = (
        PoolTimeout,
        ConnectionTimeout,
        TooManyRequests,
    )
else:

    class UndefinedTable(Exception):
        pass

    RETRIABLE_EXCEPTIONS = (RetryableException,)
    OVERLOADED_EXCEPTIONS = ()

_RETRYABLE_STATUS_CODES = frozenset(
    {
        # Server or load balancer may cancel requests under high load
        grpc.StatusCode.CANCELLED,
        # Service temporarily unavailable, e.g., server restarting or network issues
        grpc.StatusCode.UNAVAILABLE,
        # Request timed out, may succeed with more time or less server load
        grpc.StatusCode.DEADLINE_EXCEEDED,
        # Rate limiting or quota exceeded, may succeed after backoff
        grpc.StatusCode.RESOURCE_EXHAUSTED,
        # Transaction aborted due to conflicts, may succeed on retry
        grpc.StatusCode.ABORTED,
        # Server internal error, may be transient (e.g., temporary DB issues)
        grpc.StatusCode.INTERNAL,
    }
)


def retry_db(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    attempts = 3

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        for i in range(attempts):
            if i == attempts - 1:
                return await func(*args, **kwargs)
            try:
                return await func(*args, **kwargs)
            except grpc.aio.AioRpcError as e:
                if e.code() in _RETRYABLE_STATUS_CODES:
                    await asyncio.sleep(0.01)
                    continue
                raise
            except UndefinedTable:
                await asyncio.sleep(5)
            except RETRIABLE_EXCEPTIONS:
                await asyncio.sleep(0.01)

    return wrapper
