# flake8: noqa: I003

import asyncio
from functools import wraps
import inspect
import sys
import logging
import traceback
from typing import Callable, TypeVar
T = TypeVar('T')

def log_error(func: Callable[..., T]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            stacktrace = traceback.format_exc()
            logging.error(stacktrace)
            raise
        
    return wrapper