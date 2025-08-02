# arpakit


import asyncio
from datetime import timedelta
from typing import Any

from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


async def async_retry_func(
        *,
        async_func: Any,
        async_func_args: tuple[Any, ...] | None = None,
        async_func_kwargs: dict[str, Any] | None = None,
        max_tries: int = 5,
        endlessly: bool = False,
        timeout_after_exception: timedelta | None = None,
        raise_if_exception: bool = True
):
    tries = 0
    async_func_args = async_func_args or ()
    async_func_kwargs = async_func_kwargs or {}

    while True:
        try:
            return await async_func(*async_func_args, **async_func_kwargs)
        except Exception as exception:
            tries += 1
            if not endlessly and tries >= max_tries:
                if raise_if_exception:
                    raise exception
                return None
            if timeout_after_exception:
                await async_safe_sleep(timeout_after_exception.total_seconds())


def sync_retry_func(
        *,
        sync_func: Any,
        sync_func_args: tuple[Any, ...] | None = None,
        sync_func_kwargs: dict[str, Any] | None = None,
        max_tries: int = 5,
        endlessly: bool = False,
        timeout_after_exception: timedelta | None = None,
        raise_if_exception: bool = True
):
    tries = 0
    sync_func_args = sync_func_args or ()
    sync_func_kwargs = sync_func_kwargs or {}

    while True:
        try:
            return sync_func(*sync_func_args, **sync_func_kwargs)
        except Exception as exception:
            tries += 1
            if not endlessly and tries >= max_tries:
                if raise_if_exception:
                    raise exception
                return None
            if timeout_after_exception:
                sync_safe_sleep(timeout_after_exception.total_seconds())


async def __async_example():
    async def g():
        print(1)
        raise Exception

    await async_retry_func(
        async_func=g,
        endlessly=True,
        max_tries=5,
        timeout_after_exception=timedelta(seconds=1)
    )


if __name__ == '__main__':
    asyncio.run(__async_example())
