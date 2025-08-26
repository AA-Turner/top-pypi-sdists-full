import functools
import inspect
from inspect import BoundArguments, Signature
from typing import Any, Callable, Optional

import grpc
from frogml_storage.logging import logger
from qwak.exceptions import QwakException


def grpc_try_catch_wrapper(
    exception_message: str,
    reraise_non_grpc_error_original_exception: Optional[bool] = False,
) -> Callable:
    """A decorator for handling exceptions in client methods.

    This decorator wraps a function, catching any `grpc.RpcError` or other
    `Exception`. it re-raises them as a `QwakException`. The error message can be a
    static string or a template formatted with the decorated function's
    runtime arguments.

    Parameters
    ----------
    exception_message : str
        The error message template. This can be a static string or a format
        string using placeholders that match the decorated function's
        parameter names (e.g., "Failed on item {item_id}").
    reraise_non_grpc_error_original_exception : bool, optional
        If `True`, any exception that is *not* a `grpc.RpcError` will be
        re-raised in its original form. If `False` (the default), all
        exceptions are wrapped in `QwakException`.

    Returns
    -------
    Callable
        A decorator that wraps the function with the error handling logic.

    Raises
    ------
    QwakException
        Raised when the decorated function encounters any exception, unless
        `reraise_non_grpc_error_original_exception` is `True` and the error
        is not a `grpc.RpcError`. The new exception's message is formatted
        and includes details from the original error.
    Exception
        The original non-gRPC exception is re-raised if
        `reraise_non_grpc_error_original_exception` is set to `True`.

    Usage
    -----
    The decorator can be used with static strings and formatted strings

    **1. Formatted Error Messages**

    Use placeholders matching the function's parameter names to create
    context-specific error messages.

        @grpc_try_catch_wrapper("Failed to delete version {version_number} for FeatureSet {featureset_name}")
        def delete_featureset_version(self, featureset_name: str, version_number: int):
            # ... gRPC call ...

    If this function fails with a gRPC error, a `QwakException` is raised with a message like:
    `"Failed to delete version 2 for FeatureSet customer_churn - <original gRPC error code> - <original gRPC error details>."`

    **2. Static Error Messages**

    When no dynamic context is needed, a simple string is sufficient.

        @grpc_try_catch_wrapper("Failed to retrieve featuresets mapping")
        def get_featuresets_mapping(self):
            # ... gRPC call ...

    If this fails, the `QwakException` message will be:
    `"Failed to retrieve featuresets mapping - <original gRPC error code> - <original gRPC error details>."`
    """

    def decorator(function: Callable):
        @functools.wraps(function)
        def _inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except grpc.RpcError as e:
                error_message: str = __get_error_msg(
                    exception_message=exception_message, e=e
                )

                formatted_message = __get_formatted_error_message(
                    exception_message=error_message,
                    function=function,
                    args=args,
                    kwargs=kwargs,
                )

                raise QwakException(formatted_message) from e

            except Exception as e:
                if reraise_non_grpc_error_original_exception:
                    raise e

                formatted_message = __get_formatted_error_message(
                    exception_message=exception_message,
                    function=function,
                    args=args,
                    kwargs=kwargs,
                )
                raise QwakException(f"{formatted_message}. Error is: {e}.") from e

        return _inner_wrapper

    return decorator


def __get_error_msg(exception_message: str, e: grpc.RpcError) -> str:
    err_msg: str = (
        f"{exception_message} - {e.code() if hasattr(e, 'code') else 'UNKNOWN'}"
    )
    if hasattr(e, "details") and e.details() is not None:
        err_msg: str = f"{err_msg} - {e.details()}"
    elif hasattr(e, "debug_error_string"):
        err_msg: str = f"{err_msg} - {e.debug_error_string()}"
    logger.debug(f"{err_msg}: {e}")
    return err_msg


def __get_formatted_error_message(
    exception_message: str, function: Callable, args: tuple[Any], kwargs: dict[str, Any]
) -> str:
    """Formats an error message string with the runtime arguments of a function.

    It inspects the function's signature and binds the passed args and kwargs
    to their parameter names, then uses them to format the message string.

    Args:
        exception_message (str): The error message template with placeholders.
        function (Callable): The decorated function.
        args (tuple[Any]): The positional arguments passed to the function.
        kwargs (dict[str, Any]): The keyword arguments passed to the function.

    Returns:
        str: The error message with placeholders filled in.
    """
    try:
        sig: Signature = inspect.signature(function)
        bound_args: BoundArguments = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        return exception_message.format(**bound_args.arguments)
    except (ValueError, KeyError, TypeError):
        # Fallback if formatting fails (e.g., missing key in template)
        return exception_message
