from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable, Dict

if TYPE_CHECKING:
    from abstra_internals.services.jwt import UserClaims


def _get_page_sdk():
    # Lazy import: SDKContextStore transitively loads the execution/transport
    # stack (RabbitMQ, NATS, …). Users of abstra.pages should not pay that
    # cost at import time, and a failure in any of those deps must not turn
    # into "cannot import name 'register_function' from abstra.pages".
    from abstra_internals.controllers.sdk.sdk_context import SDKContextStore

    return SDKContextStore.get_by_thread().page_sdk


def register_function(func: Callable) -> Callable:
    """Register a Python function to be used by the Pages system.

    Regular functions become async JavaScript functions in the browser, callable via POST.
    A function named `__render__` is special: it is called on GET requests and must return an HTML string.

    Args:
        func (Callable): The function to register. Must have JSON-serializable parameters and return value.

    Returns:
        Callable: The original function (unchanged), allowing use as a decorator.

    Example:
        ```python
        from abstra.pages import register_function

        @register_function
        def get_data(query: str):
            return {"results": [...]}

        @register_function
        def __render__():
            return "<h1>My Page</h1><script>get_data('test').then(console.log)</script>"
        ```
    """
    return _get_page_sdk().register_function(func)


def get_user() -> UserClaims:
    """Get the authenticated user. Triggers a login prompt if the user is not authenticated.

    Can be called inside `__render__` or any registered function.

    Returns:
        UserClaims: User information with `email` (str) and `roles` (list[str]).

    Raises:
        GetUserFailed: If no valid authentication is found (results in HTTP 401).

    Example:
        ```python
        from abstra.pages import register_function, get_user

        @register_function
        def __render__():
            user = get_user()
            return f"<h1>Hello, {user.email}</h1>"
        ```
    """
    return _get_page_sdk().get_user()


def get_query_params() -> Dict[str, str]:
    """Get URL query parameters from the current request.

    Returns:
        Dict[str, str]: Query parameters as key-value pairs.

    Example:
        ```python
        from abstra.pages import register_function, get_query_params

        @register_function
        def __render__():
            params = get_query_params()
            name = params.get("name", "World")
            return f"<h1>Hello, {name}!</h1>"
        ```
    """
    return _get_page_sdk().get_query_params()


def register_static(file_path: str | os.PathLike) -> str:
    """Register a static file to be served by the Pages system. Copies the file to a public directory with a content-hashed name for cache busting and returns the URL path. Raises FileNotFoundError if the file does not exist.

    Args:
        file_path (str | os.PathLike): Path to the static file to register.
    """
    return _get_page_sdk().register_static(file_path)


__all__ = [
    "register_function",
    "register_static",
    "get_user",
    "get_query_params",
]
