"""
    Wrapper function to automatically create sync versions of async functions
"""

import asyncio
from functools import wraps


def sync_wrapper(async_func):
    @wraps(async_func)
    def wrapper(*args, **kwargs):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # No running event loop, safe to proceed with asyncio.run
            return asyncio.run(async_func(*args, **kwargs))

        # If called inside an existing event loop, raise an error
        raise RuntimeError(
            f"Called {async_func.__name__} synchronously from an async context. Use the async function directly."
        )

    return wrapper
