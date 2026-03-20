from typing import Callable, Dict

from abstra_internals.controllers.sdk.sdk_context import SDKContextStore
from abstra_internals.services.jwt import UserClaims


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
    return SDKContextStore.get_by_thread().page_sdk.register_function(func)


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
    return SDKContextStore.get_by_thread().page_sdk.get_user()


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
    return SDKContextStore.get_by_thread().page_sdk.get_query_params()


__all__ = [
    "register_function",
    "get_user",
    "get_query_params",
]
