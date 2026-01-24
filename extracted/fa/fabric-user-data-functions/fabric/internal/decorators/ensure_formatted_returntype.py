# flake8: noqa: I003

from functools import wraps
from azure.functions import HttpResponse
import json
import inspect
import sys
from typing import Any, Callable, TypeVar
import fabric.functions.udf_exception as udf_exceptions
from fabric.internal.arrow import arrow_dataframe_response, arrow_series_response
from fabric.internal.invoke_response import FormattedError, StatusCode, UserDataFunctionInvokeResponse
from fabric.internal.middleware._invocationIdMiddleware import INVOCATION_ID_PARAMETER
from .function_parameter_keywords import REQ_PARAMETER

from fabric.internal.logging import UdfLogger

from .constants import SizeLimit

import asyncio

logger = UdfLogger(__name__)

T = TypeVar('T')

def ensure_formatted_returntype(func: Callable[..., T], response_size_limit_in_mb: int = SizeLimit.RESPONSE_SIZE_LIMIT_IN_MB):
    def _check_args_for_exceptions(args: tuple, kwargs: dict):
        exceptions = []
        for arg in args:
            if issubclass(type(arg), udf_exceptions.UserDataFunctionError):
                exceptions.append(arg)
        for key, value in kwargs.items():
            if issubclass(type(value), udf_exceptions.UserDataFunctionError):
                value.properties['parameter_name'] = key
                exceptions.append(value)
        
        return exceptions
    
    def _ensure_response_is_not_too_large(resp: Any):
        if (sys.getsizeof(resp) > response_size_limit_in_mb * 1024 * 1024): # X MB = 1024 (bytes) * 1024 (kilobytes) * X
            raise udf_exceptions.UserDataFunctionResponseTooLargeError(response_size_limit_in_mb)

    def _is_pandas_type(obj) -> bool:
        # Check if the object is a pandas dataframe or series
        obj_type = inspect.getmodule(obj)
        if obj_type is not None:
            return 'pandas.core' in obj_type.__package__
        return False

    def _ensure_response_is_json_serializable(resp: Any):
        ret = ""
        try:
            if _is_pandas_type(resp):
                # If it's a dataframe/series we need to convert it to a dictionary
                if resp.__class__.__name__ == 'DataFrame':
                    resp = resp.to_dict(orient='records')
                else:
                    resp = resp.to_dict() # Adding Orient=type will break pandas.Series as this is not a valid argument for to_dict
                _ensure_response_is_not_too_large(resp)  
            else:
                output = json.dumps(resp) # we are checking it is json serializable here, not that we actually need the value of it
                # call sys.getsizeof on the string representation, since we know sys.getsizeof will work on the string representation
                _ensure_response_is_not_too_large(output)     
            ret = resp

        except (TypeError, OverflowError):
            ret = getattr(resp, '__dict__', str(resp))
            _ensure_response_is_not_too_large(ret)
            
        return ret
    
    def _ensure_response_is_binary_serializeable(resp: Any):
        ret = ""
        try:
            arrow_type = None
            if resp.__class__.__name__ == 'DataFrame':
                arrow_type = arrow_dataframe_response(resp)
            else:
                arrow_type = arrow_series_response(resp)

            arrow_bytes = arrow_type.to_bytes()
            # call sys.getsizeof on the string representation, since we know sys.getsizeof will work on the string representation
            _ensure_response_is_not_too_large(arrow_bytes)     
            ret = arrow_bytes

        except (TypeError, OverflowError):
            ret = getattr(resp, '__dict__', str(resp))
            _ensure_response_is_not_too_large(ret)
            
        return ret

    def _log_and_convert_to_formatted_error(e: Exception):
            ret = FormattedError(getattr(e, "error_code", type(e).__name__), getattr(e, 'message', str(e)), getattr(e, 'properties', {}))

            logger.error(f"Error during function invoke: {ret.to_json()}")
            return ret
        
    @wraps(func)
    async def wrapper(*args, **kwargs):
        invocationId = kwargs[INVOCATION_ID_PARAMETER]
        del kwargs[INVOCATION_ID_PARAMETER]

        # Use request to know how to format the return type
        req = kwargs[REQ_PARAMETER]

        invoke_response = UserDataFunctionInvokeResponse()
        invoke_response.functionName = func.__name__
        invoke_response.invocationId = invocationId

        try:
            input_exceptions = _check_args_for_exceptions(args, kwargs)
            if len(input_exceptions) > 0:
                invoke_response.status = StatusCode.BAD_REQUEST
                for exception in input_exceptions:
                    invoke_response.add_error(_log_and_convert_to_formatted_error(exception))
            else:
                # The line that actually invokes the user's function
                if asyncio.iscoroutinefunction(func):
                    resp = await func(*args, **kwargs) 
                else: 
                    resp = func(*args, **kwargs) 

                # Find return value in annotations. If is a dataframe or series and request is formdata
                if 'multipart/form-data' in req.headers.get('Content-Type') and _is_pandas_type(resp):
                    # If it's a data frame and it's successful we need to convert it to bytes and return right away
                    serializable_resp = _ensure_response_is_binary_serializeable(resp)
                    invoke_response.content_type = "application/octet-stream"
                    headers = {
                        'x-fabric-udf-status': str(StatusCode.SUCCEEDED)
                    }
                    formatted_response = {"status_code": 200, "headers": headers, "mimetype": "application/octet-stream", "charset": "utf-8"}
                    return HttpResponse(body=serializable_resp, status_code=formatted_response['status_code'], headers=formatted_response['headers'], mimetype=formatted_response['mimetype'], charset=formatted_response['charset'])

                # If it's not a dataframe we need to run existing checks
                serializable_resp = _ensure_response_is_json_serializable(resp)

                invoke_response.output = serializable_resp
                invoke_response.status = StatusCode.SUCCEEDED
        except Exception as e:
            if issubclass(type(e), udf_exceptions.UserDataFunctionError):
                invoke_response.add_error(_log_and_convert_to_formatted_error(e))

                if type(e) is udf_exceptions.UserDataFunctionTimeoutError:
                    invoke_response.status = StatusCode.TIMEOUT
                elif type(e) is udf_exceptions.UserDataFunctionResponseTooLargeError:
                    invoke_response.status = StatusCode.RESPONSE_TOO_LARGE
                elif issubclass(type(e), udf_exceptions.UserThrownError): # custom exceptions that the user can throw, or they can use as a base class
                    invoke_response.status = StatusCode.BAD_REQUEST
                else: # custom exceptions that we  throw
                    invoke_response.status = StatusCode.FAILED
            else:
                invoke_response.status = StatusCode.FAILED
                # Put the details into an InternalErrorException to hide other details from the exception
                error = udf_exceptions.UserDataFunctionInternalError(properties={'error_type': type(e).__name__, 'error_message': getattr(e, 'message', str(e))})
                invoke_response.add_error(_log_and_convert_to_formatted_error(error))

        # we need to make a new HttpResponse because there is no way to modify the body of an existing one
        headers = {
            'x-fabric-udf-status': str(invoke_response.status)
        }
        formatted_response = {"status_code": 200, "headers": headers, "mimetype": "application/json", "charset": "utf-8"}
        return HttpResponse(body=invoke_response.to_json(), status_code=formatted_response['status_code'], headers=formatted_response['headers'], mimetype=formatted_response['mimetype'], charset=formatted_response['charset'])

    return wrapper
