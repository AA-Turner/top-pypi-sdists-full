# flake8: noqa: I003
from functools import wraps
import queue
import threading
import time
import traceback
from typing import Callable, Optional, TypeVar

from fabric.functions.udf_exception import UserDataFunctionTimeoutError
from fabric.internal.logging import UdfLogger
from fabric.internal.decorators.function_parameter_keywords import CONTEXT_PARAMETER

from .constants import Timeout

import asyncio
import inspect
import functools
import contextvars

T = TypeVar('T')

logger = UdfLogger(__name__)

def add_timeout(func: Callable[..., T], function_timeout: int = Timeout.FUNC_TIMEOUT_IN_SECONDS):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        context = None
        # Extract Azure Function Context to setup invocation id for logging
        if CONTEXT_PARAMETER in kwargs:
            context = kwargs[CONTEXT_PARAMETER]
            del kwargs[CONTEXT_PARAMETER]

        try:
            # This will raise a TimeoutError if the function takes longer than the timeout
            loop = asyncio.get_running_loop()
            func_task = None

            if inspect.iscoroutinefunction(func):
                # For async functions, create a task in the current event loop
                # Set up context in the current thread before creating the task
                if context is not None:
                    context.thread_local_storage.invocation_id = context.invocation_id
                
                func_task = asyncio.create_task(func(*args, **kwargs))
            else:
                # For sync functions, run in thread pool with proper context setup
                def sync_function_runner():
                    if context is not None:
                        context.thread_local_storage.invocation_id = context.invocation_id
                    return func(*args, **kwargs)
                ctx = contextvars.copy_context()
                func_task = loop.run_in_executor(None, ctx.run, sync_function_runner)

            return await asyncio.wait_for(func_task, timeout=function_timeout)

        except asyncio.TimeoutError:
            return UserDataFunctionTimeoutError(function_timeout)
        
    return wrapper