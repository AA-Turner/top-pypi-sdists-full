# flake8: noqa: I003
from functools import wraps
from typing import Callable, TypeVar
from fabric.internal.decorators.function_parameter_keywords import UNUSED_FABRIC_CONTEXT_PARAMETER, REQ_PARAMETER
from fabric.internal.decorators.constants import BatchInternalKeys
import asyncio

T = TypeVar('T')

def remove_unused_binding_params(func: Callable[..., T]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if REQ_PARAMETER in kwargs:
            del kwargs[REQ_PARAMETER]
        if UNUSED_FABRIC_CONTEXT_PARAMETER in kwargs:
            del kwargs[UNUSED_FABRIC_CONTEXT_PARAMETER]
        # Remove batch internal parameters
        if BatchInternalKeys.IS_BATCH in kwargs:
            del kwargs[BatchInternalKeys.IS_BATCH]
        if BatchInternalKeys.BATCH_SIZE in kwargs:
            del kwargs[BatchInternalKeys.BATCH_SIZE]
        if BatchInternalKeys.BATCH_ITEMS in kwargs:
            del kwargs[BatchInternalKeys.BATCH_ITEMS]
        if BatchInternalKeys.BATCH_VALIDATION_ERROR in kwargs:
            del kwargs[BatchInternalKeys.BATCH_VALIDATION_ERROR]

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs) 
        else: 
            return func(*args, **kwargs) 
    return wrapper