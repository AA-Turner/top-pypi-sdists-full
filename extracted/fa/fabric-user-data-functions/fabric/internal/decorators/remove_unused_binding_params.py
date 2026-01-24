# flake8: noqa: I003
from functools import wraps
from typing import Callable, TypeVar
from fabric.internal.decorators.function_parameter_keywords import UNUSED_FABRIC_CONTEXT_PARAMETER, REQ_PARAMETER
import asyncio

T = TypeVar('T')

def remove_unused_binding_params(func: Callable[..., T]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if REQ_PARAMETER in kwargs:
            del kwargs[REQ_PARAMETER]
        if UNUSED_FABRIC_CONTEXT_PARAMETER in kwargs:
            del kwargs[UNUSED_FABRIC_CONTEXT_PARAMETER]

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs) 
        else: 
            return func(*args, **kwargs) 
    return wrapper