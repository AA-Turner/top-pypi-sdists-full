from __future__ import annotations

import inspect
import math
import os
from typing import TYPE_CHECKING, Callable, Dict, Optional, Union, overload

if TYPE_CHECKING:
    from abstra_internals.services.jwt import UserClaims

# Mirrored from controllers.sdk.sdk_pages.RENDER_FUNCTION_NAME. Duplicated as a
# literal here to keep this module free of controller imports — otherwise we
# pull in the transport stack (NATS, RabbitMQ, …) that the lazy
# `_get_page_sdk` indirection exists to avoid.
_RENDER_FUNCTION_NAME = "__render__"


def _get_page_sdk():
    # Lazy import: SDKContextStore transitively loads the execution/transport
    # stack (RabbitMQ, NATS, …). Users of abstra.pages should not pay that
    # cost at import time, and a failure in any of those deps must not turn
    # into "cannot import name 'register_function' from abstra.pages".
    from abstra_internals.controllers.sdk.sdk_context import SDKContextStore

    return SDKContextStore.get_by_thread().page_sdk


def _validate_cache_value(cache: object) -> float:
    # bool is a subclass of int — reject it explicitly so `cache=True` doesn't
    # silently become "cache for 1 second".
    if isinstance(cache, bool) or not isinstance(cache, (int, float)):
        raise TypeError(
            f"cache must be a number of seconds, got {type(cache).__name__}"
        )
    cache_float = float(cache)
    if not math.isfinite(cache_float) or cache_float <= 0:
        raise ValueError(
            f"cache must be a positive, finite number of seconds, got {cache!r}"
        )
    return cache_float


@overload
def register_function(func: Callable) -> Callable: ...


@overload
def register_function(
    *, cache: Optional[Union[int, float]] = None
) -> Callable[[Callable], Callable]: ...


def register_function(
    func: Optional[Callable] = None,
    *,
    cache: Optional[Union[int, float]] = None,
) -> Union[Callable, Callable[[Callable], Callable]]:
    """Register a Python function to be used by the Pages system.

    Regular functions become async JavaScript functions in the browser, callable via POST.
    A function named `__render__` is special: it is called on GET requests and must return an HTML string.

    Args:
        func (Callable): The function to register. Must have JSON-serializable parameters and return value.
        cache (int | float, optional): If set, the generated JS function caches its
            result in memory for this many seconds, keyed by the call's positional
            arguments. Subsequent calls within the TTL skip the worker round-trip
            entirely. Concurrent in-flight calls share a single request. The cache
            is per page load (not persisted), bypassed when any argument is a
            ``Blob``/``FileList``, and exposes a ``fn.clearCache()`` JS helper for
            manual invalidation (e.g. after auth changes). Not supported on
            generator functions or ``__render__``.

    Returns:
        Callable: The original function (unchanged), allowing use as a decorator.

    Example:
        ```python
        from abstra.pages import register_function

        @register_function
        def get_data(query: str):
            return {"results": [...]}

        @register_function(cache=60)
        def get_settings():
            return {"theme": "dark"}

        @register_function
        def __render__():
            return "<h1>My Page</h1><script>get_data('test').then(console.log)</script>"
        ```
    """
    if cache is not None:
        cache_seconds: Optional[float] = _validate_cache_value(cache)
    else:
        cache_seconds = None

    def _wrap(f: Callable) -> Callable:
        if cache_seconds is not None:
            if inspect.isgeneratorfunction(f):
                raise ValueError(
                    f"register_function(cache=...) is not supported on generator "
                    f"functions ({f.__name__!r}); generators stream chunks and "
                    f"caching them would change semantics for `for await...of`."
                )
            if f.__name__ == _RENDER_FUNCTION_NAME:
                raise ValueError(
                    "register_function(cache=...) cannot be used on __render__ "
                    "(it is not exposed to the browser)."
                )
            try:
                f._abstra_cache_ttl = cache_seconds  # type: ignore[attr-defined]
            except (AttributeError, TypeError):
                # Builtin/C functions or slot-only callables can't accept attributes.
                # User-defined functions always can; this is a defensive guard.
                raise TypeError(
                    f"register_function(cache=...) requires a callable that "
                    f"accepts attributes; got {type(f).__name__}"
                )
        return _get_page_sdk().register_function(f)

    if func is None:
        return _wrap
    return _wrap(func)


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
