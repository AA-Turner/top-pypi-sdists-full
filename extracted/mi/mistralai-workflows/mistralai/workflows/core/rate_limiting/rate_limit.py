import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncContextManager, AsyncGenerator, Callable, Dict, List, cast
from uuid import NAMESPACE_DNS, uuid5

from asynciolimiter import StrictLimiter
from pydantic import BaseModel, Field

# we import as package here to avoid circular import error
from mistralai.workflows.core import config as config_package
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

_RATE_LIMITED_ATTR_NAME = "__wf_rate_limited"

_local_rate_limiters: Dict[str, StrictLimiter] = {}
_lock = asyncio.Lock()


class RateLimit(BaseModel):
    time_window_in_sec: int = Field(..., ge=1, le=3600, description="The time window in seconds.")
    """The time window in seconds."""

    max_execution: int = Field(
        ..., ge=1, le=100000, description="The maximum number of executions allowed within the time window."
    )
    """The maximum number of executions allowed within the time window."""

    key: str | None = Field(default=None, description="The key to identify the rate limit.")
    """The key to identify the rate limit. If not provided, the activity/function name will be used."""


class _RateLimit(RateLimit):
    task_queue_suffix: str = Field(..., description="The name of the task queue.")

    @property
    def task_queue(self) -> str:
        base_queue = config_package.config.get_effective_task_queue()
        return f"{base_queue}-{self.task_queue_suffix}"


def set_rate_limit(activity: Callable, rate_limit: RateLimit) -> _RateLimit:
    key = rate_limit.key or activity.__name__
    key_uuid = uuid5(NAMESPACE_DNS, key).hex.replace("-", "")
    task_queue_suffix = f"rate-limited-{key_uuid}"
    _rate_limit = _RateLimit(
        **{
            **rate_limit.model_dump(),
            "task_queue_suffix": task_queue_suffix,
        }
    )

    setattr(activity, _RATE_LIMITED_ATTR_NAME, _rate_limit)
    return _rate_limit


def get_rate_limit(activity: Callable) -> _RateLimit | None:
    return getattr(activity, _RATE_LIMITED_ATTR_NAME, None)


async def local_wait_rate_limit(rate_limit_config: _RateLimit) -> None:
    async with _lock:
        rate_limiter_key = rate_limit_config.task_queue
        if rate_limiter_key not in _local_rate_limiters:
            _local_rate_limiters[rate_limiter_key] = StrictLimiter(
                rate_limit_config.max_execution / rate_limit_config.time_window_in_sec
            )

    rate_limiter = _local_rate_limiters[rate_limit_config.task_queue]
    assert rate_limiter is not None
    await rate_limiter.wait()


def rate_limit(rate_limit: RateLimit) -> Callable:
    def decorator[T: Callable](func_or_ctx: T) -> T:
        if hasattr(func_or_ctx, "__temporal_activity_definition"):
            raise WorkflowsException(
                code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
                message="Cannot use `@rate_limit` with `@activity`, please use the parameter `rate_limit` instead in `@activity`.",  # noqa: E501
            )

        rate_limit_config = set_rate_limit(func_or_ctx, rate_limit)

        @wraps(func_or_ctx)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            result = func_or_ctx(*args, **kwargs)
            if isinstance(result, AsyncContextManager):

                @asynccontextmanager
                async def async_context_manager_callable() -> AsyncGenerator[Any, None]:
                    await local_wait_rate_limit(rate_limit_config)
                    async with func_or_ctx(*args, **kwargs) as value:
                        yield value

                return async_context_manager_callable()

            elif isinstance(result, AsyncGenerator):

                async def async_generator_callable() -> Any:
                    await local_wait_rate_limit(rate_limit_config)
                    async for value in result:
                        yield value

                return async_generator_callable()

            elif asyncio.iscoroutine(result):

                async def async_callable() -> Any:
                    await local_wait_rate_limit(rate_limit_config)
                    return await result

                return async_callable()

            else:
                raise WorkflowsException(
                    code=ErrorCode.RATE_LIMIT_ERROR,
                    message=f"Rate limit is not supported for {func_or_ctx}, please use async function or async context manager.",  # noqa: E501
                )

        return cast(T, wrapper)

    return decorator
