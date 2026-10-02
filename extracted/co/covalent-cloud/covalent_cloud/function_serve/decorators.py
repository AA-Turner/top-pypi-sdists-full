# Copyright 2024 Agnostiq Inc.

import inspect
import warnings
from functools import wraps
from typing import Callable, Optional

from covalent_cloud.cloud_executor.cloud_executor import CloudExecutor
from covalent_cloud.function_serve.common import SupportedMethods
from covalent_cloud.function_serve.service_class import FunctionService
from covalent_cloud.shared.classes.exceptions import InsufficientMemoryError
from covalent_cloud.shared.classes.settings import settings
from covalent_cloud.volume.volume import Volume

__all__ = [
    "service",
]


def service(
    _func: Optional[Callable] = None,
    *,
    executor: CloudExecutor,
    name: str = "",
    description: str = "",
    auth: Optional[bool] = None,
    tags: Optional[list] = None,
    compute_share: float = 1.0,
    volume: Optional[Volume] = None,
) -> FunctionService:
    """Decorator used to create a function service by wrapping its initializer.

    Args:
        _func: Service initializer function to be wrapped. This function should return a
            dict-like object containing initialized values to be used by the service's endpoints.
        executor: A CloudExecutor instance that specifies compute resources assigned to this service.
        name: Optional name for the function service. Defaults to the decorated function's name.
        description: Optional description for the function service.
            Defaults to the decorated function's docstring.
        auth: Whether or not to require an authentication token for requests.
            Auth is required by default.
        tags: An optional list of tags to associate with the function service. Defaults to None.
        compute_share: Fraction of resources to allocate to each replica of the function service.
            Defaults to 1, meaning a single replica that uses all assigned resources.
        volume: Choice of cloud storage volume to attach. Defaults to None.

    Raises:
        InsufficientMemoryError: If the assigned executor has less than the minimum required memory.

    Returns:
        A function service object with an `endpoint` decorator method for creating HTTP routes.
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    if executor.memory < settings.function_serve.min_executor_memory_gb * 1024:
        raise InsufficientMemoryError(int(executor.memory / 1024))

    tags = tags or []

    def service_decorator(func=None):
        @wraps(func)
        def internal_wrapper(executor, name, description, auth, tags, compute_share, volume):
            return FunctionService(
                func,
                executor,
                name,
                description,
                auth,
                tags,
                compute_share,
                volume,
                _main_func=func,
            )

        return internal_wrapper(executor, name, description, auth, tags, compute_share, volume)

    if _func is None:
        return service_decorator

    return service_decorator(_func)


def op_internal_wrapper_generator(
    route,
    executor,
    name,
    streaming,
    description,
    auth,
    tags,
    compute_share,
    op,
):
    fs_instance = service(
        executor=executor,
        name=name,
        description=description,
        auth=auth,
        tags=tags,
        compute_share=compute_share,
    )(None)

    # Get the correct method from the FunctionService class, e.g. _get, _post, _put, etc.
    op_func = getattr(fs_instance, "_" + op.value.lower())

    def internal_wrapper(func):

        # Set the function service instance attributes since there is no init_func function
        fs_instance.func_name = func.__name__
        fs_instance.name = fs_instance.name or func.__name__
        fs_instance.func_source = inspect.getsource(func)
        fs_instance.func_description = description or func.__doc__ or ""
        fs_instance._main_func = func

        # Register the route and the method function and return the FunctionService instance
        return op_func(route, name, description, streaming)(func)

    return internal_wrapper


def get_decorator(
    route,
    executor=None,
    name=None,
    streaming=False,
    description=None,
    auth=None,
    tags=None,
    compute_share=None,
):
    return op_internal_wrapper_generator(
        route,
        executor,
        name,
        streaming,
        description,
        auth,
        tags,
        compute_share,
        SupportedMethods.GET,
    )


def post_decorator(
    route,
    executor=None,
    name=None,
    streaming=False,
    description=None,
    auth=None,
    tags=None,
    compute_share=None,
):

    return op_internal_wrapper_generator(
        route,
        executor,
        name,
        streaming,
        description,
        auth,
        tags,
        compute_share,
        SupportedMethods.POST,
    )


def put_decorator(
    route,
    executor=None,
    name=None,
    streaming=False,
    description=None,
    auth=None,
    tags=None,
    compute_share=None,
):

    return op_internal_wrapper_generator(
        route,
        executor,
        name,
        streaming,
        description,
        auth,
        tags,
        compute_share,
        SupportedMethods.PUT,
    )


def delete_decorator(
    route,
    executor=None,
    name=None,
    streaming=False,
    description=None,
    auth=None,
    tags=None,
    compute_share=None,
):

    return op_internal_wrapper_generator(
        route,
        executor,
        name,
        streaming,
        description,
        auth,
        tags,
        compute_share,
        SupportedMethods.DELETE,
    )


def patch_decorator(
    route,
    executor=None,
    name=None,
    streaming=False,
    description=None,
    auth=None,
    tags=None,
    compute_share=None,
):

    return op_internal_wrapper_generator(
        route,
        executor,
        name,
        streaming,
        description,
        auth,
        tags,
        compute_share,
        SupportedMethods.PATCH,
    )


# Assigning the decorators to the service function

# We still do this instead of directly using `op_internal_wrapper_generator`
# so that the correct supported arguments are shown when something like autocompletion is used
service._get = get_decorator
service._post = post_decorator
service._put = put_decorator
service._delete = delete_decorator

# This is the one that will be used by the user
service.endpoint = post_decorator
