# flake8: noqa: I003
from functools import wraps
import logging
from azure.functions import HttpRequest
import inspect
import asyncio
from typing import Callable, TypeVar

from fabric.functions.udf_exception import UserDataFunctionInvalidInputError
from fabric.internal.utils.parameter_utils import apply_fabric_item_providers, parse_scalar_parameters
from .function_parameter_keywords import REQ_PARAMETER
from .constants import HeaderConstants, BatchInternalKeys, BatchErrorMessages
from fabric.internal.providers import ProviderMetadata, ProviderFactory

T = TypeVar('T')

def add_batched_parameters(func: Callable[..., T], 
                           udfParams: list[inspect.Parameter], 
                           fabricItemParams: list[inspect.Parameter]):
    """Add parameters to a batched function"""
    # Create provider instances once at decorator level
    provider_factory = ProviderFactory()
    provider_metadata = ProviderMetadata()
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # get request from kwargs
        req: HttpRequest = None
        if REQ_PARAMETER in kwargs:
            req = kwargs[REQ_PARAMETER]
        
        # Get batch size from metadata
        max_batch_size = getattr(func, '__udf_metadata__', {}).get('max_batch_size', None)
        
        # Get request body
        content_type = req.headers.get('Content-Type')
        if content_type == None or 'application/json' in content_type:
            body = req.get_json()
            
           # Support both batch (list) and scalar (dict) invocations for test/invoke
            if isinstance(body, list):
                # Process as batch
                kwargs[BatchInternalKeys.IS_BATCH] = True
                kwargs[BatchInternalKeys.BATCH_SIZE] = max_batch_size
                kwargs[BatchInternalKeys.BATCH_ITEMS] = body
            elif isinstance(body, dict):
                # Process as scalar (test/invoke compatibility)
                kwargs[BatchInternalKeys.IS_BATCH] = False
                parse_scalar_parameters(body, udfParams, kwargs)
            else:
                # Invalid body type
                kwargs[BatchInternalKeys.IS_BATCH] = True
                kwargs[BatchInternalKeys.BATCH_VALIDATION_ERROR] = UserDataFunctionInvalidInputError(
                    message=BatchErrorMessages.BATCH_ARRAY_EXPECTED,
                    properties={'receivedType': type(body).__name__, 'expectedType': 'array'}
                )
        
        # Apply fabric item providers using shared utility
        apply_fabric_item_providers(
            fabricItemParams, kwargs, func.__name__, req,
            provider_factory, provider_metadata
        )

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs) 
        else: 
            return func(*args, **kwargs) 
    return wrapper
