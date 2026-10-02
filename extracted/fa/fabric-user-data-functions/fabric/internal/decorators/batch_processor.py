"""Batch processing logic for UDF execution."""

import asyncio
import inspect
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from ...functions import udf_exception as udf_exceptions
from ..converters.basic_datatype_converter import BasicDatatypeConverter
from ..invoke_response import BatchItemResult
from ..utils.parameter_utils import create_missing_input_error
from .constants import BatchInternalKeys


@dataclass
class BatchExecutionResult:
    """Result of executing a batch item or batch operation."""
    item_result: BatchItemResult
    user_error: Optional[Exception] = None
    timeout_error: Optional[Exception] = None
    response_too_large_error: Optional[Exception] = None
    internal_error: Optional[Exception] = None


def _is_parameter_required(param: inspect.Parameter) -> bool:
    """Check if a parameter is required (has no default value)."""
    return param.default == inspect.Parameter.empty


# Internal keys that should be excluded from user function arguments
_INTERNAL_KEYS = {
    BatchInternalKeys.IS_BATCH,
    BatchInternalKeys.BATCH_SIZE,
    BatchInternalKeys.BATCH_ITEMS,
    BatchInternalKeys.BATCH_VALIDATION_ERROR
}


async def _execute_single_batch_item(
    func: Callable,
    batch_item: Any,
    udf_params: List,
    args: tuple,
    kwargs: dict,
    check_args_for_exceptions: Callable,
    ensure_response_is_json_serializable: Callable,
    log_and_convert_to_formatted_error: Callable
) -> BatchExecutionResult:
    """
    Helper function to execute the UDF for ONE batch item (called multiple times in parallel).

    This function is invoked once per item in the batch, with all invocations running
    concurrently via asyncio.gather() in process_batch_items().

    Returns:
        BatchExecutionResult containing the item result and any errors encountered
    """
    item_result = BatchItemResult()
    user_error = None
    timeout_error = None
    response_too_large_error = None
    has_internal_error = None

    try:
        # Parse batch_item arguments (e.g., {x: 1, y: 2}) into function arguments (e.g., my_func(x=1, y=2))
        item_kwargs = {k: v for k, v in kwargs.items() if k not in _INTERNAL_KEYS}

        # Extract parameters from dict-formatted batch_item
        if isinstance(batch_item, dict):
            for param in udf_params:
                if param.name in batch_item:
                    value = batch_item[param.name]
                    # Handle null values: only error if parameter is required
                    if value is None and _is_parameter_required(param):
                        item_kwargs[param.name] = create_missing_input_error(param)
                    else:
                        item_kwargs[param.name] = BasicDatatypeConverter.tryconvert(param.annotation.__name__, value)
                else:
                    # Parameter missing: only error if required (no default)
                    if _is_parameter_required(param):
                        item_kwargs[param.name] = create_missing_input_error(param)
                    # Otherwise, omit it so Python uses the default value
        # Extract parameters from array-formatted batch_item
        elif isinstance(batch_item, (list, tuple)) and len(udf_params) > 0:
            for pos, param in enumerate(udf_params):
                if pos < len(batch_item):
                    value = batch_item[pos]
                    # Handle null values: only error if parameter is required
                    if value is None and _is_parameter_required(param):
                        item_kwargs[param.name] = create_missing_input_error(param)
                    else:
                        item_kwargs[param.name] = BasicDatatypeConverter.tryconvert(param.annotation.__name__, value)
                else:
                    # Parameter missing: only error if required (no default)
                    if _is_parameter_required(param):
                        item_kwargs[param.name] = create_missing_input_error(param)
                    # Otherwise, omit it so Python uses the default value
        # Extract parameter from scalar-formatted batch_item
        elif len(udf_params) == 1:
            param = udf_params[0]
            # Handle null values: only error if parameter is required
            if batch_item is None and _is_parameter_required(param):
                item_kwargs[param.name] = create_missing_input_error(param)
            else:
                item_kwargs[param.name] = BasicDatatypeConverter.tryconvert(param.annotation.__name__, batch_item)

        # Find parameters that were set to error objects (happens above when required param is missing from item)
        input_exceptions = check_args_for_exceptions(args, item_kwargs)

        if input_exceptions:
            user_error = input_exceptions[0]
            item_result.errors.extend([log_and_convert_to_formatted_error(ex) for ex in input_exceptions])
            item_result.output = None
        else:
            # Unwrap to original function (parameters already extracted)
            base_func = func
            while hasattr(base_func, '__wrapped__'):
                base_func = base_func.__wrapped__

            # Filter to only the parameters the original user function declares
            user_param_names = {p.name for p in udf_params}

            # Only pass parameters the original user function actually declares
            call_kwargs = {k: v for k, v in item_kwargs.items() if k in user_param_names}

            if asyncio.iscoroutinefunction(base_func):
                resp = await base_func(**call_kwargs)
            else:
                resp = base_func(**call_kwargs)
            item_result.output = ensure_response_is_json_serializable(resp)

    except Exception as e:
        if issubclass(type(e), udf_exceptions.UserDataFunctionError):

            if type(e) is udf_exceptions.UserDataFunctionTimeoutError:
                timeout_error = e  # 408 Timeout - populate per-item errors
                item_result.errors.append(log_and_convert_to_formatted_error(e))
            elif type(e) is udf_exceptions.UserDataFunctionResponseTooLargeError:
                response_too_large_error = e  # 413 Response Too Large - do not populate per-item errors
            elif issubclass(type(e), udf_exceptions.UserThrownError):
                user_error = e  # 200 Mixed Success - populate per-item errors
                item_result.errors.append(log_and_convert_to_formatted_error(e))
            else:
                has_internal_error = e  # 500 Internal Error - capture exception for top-level error
        else:
            has_internal_error = e
        item_result.output = None

    return BatchExecutionResult(
        item_result=item_result,
        user_error=user_error,
        timeout_error=timeout_error,
        response_too_large_error=response_too_large_error,
        internal_error=has_internal_error
    )


@dataclass
class BatchProcessingResult:
    """Result of processing all batch items."""
    batch_results: List[dict]
    user_error: Optional[Exception] = None
    timeout_error: Optional[Exception] = None
    response_too_large_error: Optional[Exception] = None
    internal_error: Optional[Exception] = None


async def process_batch_items(
    func: Callable,
    batch_items: List[Any],
    args: tuple,
    kwargs: dict,
    check_args_for_exceptions: Callable,
    ensure_response_is_json_serializable: Callable,
    log_and_convert_to_formatted_error: Callable
) -> BatchProcessingResult:
    """
    Execute the UDF concurrently for each item in the batch using asyncio.

    Args:
        func: The UDF to execute
        batch_items: List of items to process
        args: Positional arguments for the UDF
        kwargs: Keyword arguments for the UDF
        check_args_for_exceptions: Helper to check for exception objects in arguments
        ensure_response_is_json_serializable: Helper to serialize response
        log_and_convert_to_formatted_error: Helper to format and log errors

    Returns:
        BatchProcessingResult containing batch results and any errors encountered
    """
    udf_params = getattr(func, '__udf_metadata__', {}).get('udf_params', [])

    # Execute all batch items concurrently using asyncio.gather
    # Each batch_item runs in parallel via _execute_single_batch_item
    results = await asyncio.gather(
        *[
            _execute_single_batch_item(
                func, batch_item, udf_params, args, kwargs,
                check_args_for_exceptions, ensure_response_is_json_serializable,
                log_and_convert_to_formatted_error
            )
            for batch_item in batch_items
        ],
        return_exceptions=False  # Exceptions are handled within _execute_single_batch_item
    )

    # Aggregate results and error flags
    batch_results = []
    user_error = None
    timeout_error = None
    response_too_large_error = None
    has_internal_error = None

    for result in results:
        batch_results.append(result.item_result.to_dict())
        # Capture first occurrence of each error type
        user_error = user_error or result.user_error
        timeout_error = timeout_error or result.timeout_error
        response_too_large_error = response_too_large_error or result.response_too_large_error
        has_internal_error = has_internal_error or result.internal_error

    return BatchProcessingResult(
        batch_results=batch_results,
        user_error=user_error,
        timeout_error=timeout_error,
        response_too_large_error=response_too_large_error,
        internal_error=has_internal_error
    )
