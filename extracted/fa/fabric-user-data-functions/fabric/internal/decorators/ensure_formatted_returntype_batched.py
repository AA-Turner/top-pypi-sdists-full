# flake8: noqa: I003

from functools import wraps
from azure.functions import HttpResponse
import json
from typing import Callable, TypeVar
import fabric.functions.udf_exception as udf_exceptions
from fabric.internal.invoke_response import StatusCode, UserDataFunctionInvokeResponse
from fabric.internal.middleware._invocationIdMiddleware import INVOCATION_ID_PARAMETER
from fabric.internal.utils.parameter_utils import check_args_for_exceptions
from .function_parameter_keywords import REQ_PARAMETER
from fabric.internal.logging import UdfLogger
from .constants import BatchConstants, BatchErrorMessages, BatchInternalKeys
from .batch_processor import process_batch_items
from .ensure_formatted_returntype import _execute_scalar_invocation
import sys
import asyncio

logger = UdfLogger(__name__)

T = TypeVar('T')

def ensure_formatted_returntype_batched(func: Callable[..., T]):
    """Ensure formatted return type for batched functions."""
    
    def _ensure_response_is_not_too_large(resp, response_size_limit_in_mb=100):
        if (sys.getsizeof(resp) > response_size_limit_in_mb * 1024 * 1024):
            raise udf_exceptions.UserDataFunctionResponseTooLargeError(response_size_limit_in_mb)

    def _ensure_response_is_json_serializable(resp):
        ret = ""
        try:
            import inspect
            obj_type = inspect.getmodule(resp)
            is_pandas = obj_type is not None and 'pandas.core' in obj_type.__package__
            
            if is_pandas:
                # If it's a dataframe/series we need to convert it to a dictionary
                if resp.__class__.__name__ == 'DataFrame':
                    resp = resp.to_dict(orient='records')
                else:
                    resp = resp.to_dict()
                _ensure_response_is_not_too_large(resp)  
            else:
                output = json.dumps(resp)
                _ensure_response_is_not_too_large(output)     
            ret = resp

        except (TypeError, OverflowError):
            ret = getattr(resp, '__dict__', str(resp))
            _ensure_response_is_not_too_large(ret)
            
        return ret

    def _log_and_convert_to_formatted_error(e: Exception):
        from fabric.internal.invoke_response import FormattedError
        ret = FormattedError(getattr(e, "error_code", type(e).__name__), getattr(e, 'message', str(e)), getattr(e, 'properties', {}))
        logger.error(f"Error during function invoke: {ret.to_json()}")
        return ret
    
    def _create_http_response(invoke_response: UserDataFunctionInvokeResponse) -> HttpResponse:
        """Create standardized HTTP response for batch functions."""
        return HttpResponse(
            body=invoke_response.to_json(), 
            status_code=200, 
            headers={'x-fabric-udf-status': str(invoke_response.status)}, 
            mimetype="application/json", 
            charset="utf-8"
        )
        
    @wraps(func)
    async def wrapper(*args, **kwargs):
        invocationId = kwargs[INVOCATION_ID_PARAMETER]
        del kwargs[INVOCATION_ID_PARAMETER]

        req = kwargs[REQ_PARAMETER]
        
        # Get batch information
        is_batch = kwargs.pop(BatchInternalKeys.IS_BATCH, False)
        max_batch_size = kwargs.pop(BatchInternalKeys.BATCH_SIZE, None)
        batch_items = kwargs.pop(BatchInternalKeys.BATCH_ITEMS, None)
        batch_validation_error = kwargs.pop(BatchInternalKeys.BATCH_VALIDATION_ERROR, None)

        invoke_response = UserDataFunctionInvokeResponse()
        invoke_response.functionName = func.__name__
        invoke_response.invocationId = invocationId

        # Handle batch validation errors
        if batch_validation_error:
            invoke_response.status = StatusCode.BAD_REQUEST
            invoke_response.add_error(_log_and_convert_to_formatted_error(batch_validation_error))
            return _create_http_response(invoke_response)

        # Process batch items
        if is_batch and batch_items is not None:
            # Validate batch size is within allowed range
            if len(batch_items) < BatchConstants.MIN_BATCH_SIZE:
                invoke_response.status = StatusCode.BAD_REQUEST
                invoke_response.add_error(_log_and_convert_to_formatted_error(
                    udf_exceptions.UserDataFunctionInvalidInputError(
                        message=BatchErrorMessages.BATCH_TOO_SMALL.format(min_required=BatchConstants.MIN_BATCH_SIZE),
                        properties={'batch_size': len(batch_items), 'min_required': BatchConstants.MIN_BATCH_SIZE}
                    )
                ))
            elif max_batch_size and len(batch_items) > max_batch_size:
                invoke_response.status = StatusCode.BAD_REQUEST
                invoke_response.add_error(_log_and_convert_to_formatted_error(
                    udf_exceptions.UserDataFunctionInvalidInputError(
                        message=BatchErrorMessages.BATCH_TOO_LARGE.format(batch_size=len(batch_items), max_allowed=max_batch_size),
                        properties={'batch_size': len(batch_items), 'max_allowed': max_batch_size}
                    )
                ))
            else:
                # Execute the UDF once per batch item
                result = await process_batch_items(
                    func, batch_items, args, kwargs, 
                    check_args_for_exceptions, _ensure_response_is_json_serializable, _log_and_convert_to_formatted_error
                )
                
                # Determine overall batch status and populate top-level errors for system failures
                invoke_response.batchOutput = result.batch_results
                if result.response_too_large_error:
                    invoke_response.add_error(_log_and_convert_to_formatted_error(result.response_too_large_error))
                    invoke_response.status = StatusCode.RESPONSE_TOO_LARGE
                elif result.timeout_error:
                    invoke_response.status = StatusCode.TIMEOUT
                elif result.internal_error:
                    error = udf_exceptions.UserDataFunctionInternalError(
                        properties={'error_type': type(result.internal_error).__name__, 'error_message': getattr(result.internal_error, 'message', str(result.internal_error))}
                    )
                    invoke_response.add_error(_log_and_convert_to_formatted_error(error))
                    invoke_response.status = StatusCode.FAILED
                else:
                    invoke_response.status = StatusCode.SUCCEEDED
            
            return _create_http_response(invoke_response)

        # Handle scalar mode for batched functions (e.g., test mode or /invoke endpoint)
        if not is_batch:
            await _execute_scalar_invocation(
                func, args, kwargs, invoke_response,
                _ensure_response_is_json_serializable, None,
                _log_and_convert_to_formatted_error, None, req
            )
            return _create_http_response(invoke_response)

        # Should not reach here for batched functions, but handle gracefully
        invoke_response.status = StatusCode.FAILED
        error = udf_exceptions.UserDataFunctionInternalError(
            properties={'error_type': 'InvalidBatchRequest', 'error_message': 'Batched function called without valid batch data'}
        )
        invoke_response.add_error(_log_and_convert_to_formatted_error(error))
        return _create_http_response(invoke_response)

    return wrapper
