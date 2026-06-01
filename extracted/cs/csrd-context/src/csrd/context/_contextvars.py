import logging
from collections.abc import Callable
from contextvars import ContextVar, Token
from typing import Any

from ._constants import APP_ID_HEADER_NAME, HIT_ID_HEADER_NAME
from ._models import PathValue

logger = logging.getLogger(__name__)

# Request-scoped context variables and accessors.
#
# The ``configure_*`` functions below set module-level state and must be called
# once during application startup, before any requests are served.

_PATH_CONTEXT_KEY = "path_context"
_QUERY_CONTEXT_KEY = "query_context"
_API_VERSION_CONTEXT_KEY = "api_version_context"

_path_context: ContextVar[PathValue | None] = ContextVar(_PATH_CONTEXT_KEY, default=None)
_query_context: ContextVar[PathValue | None] = ContextVar(_QUERY_CONTEXT_KEY, default=None)
_api_version_context: ContextVar[str | None] = ContextVar(_API_VERSION_CONTEXT_KEY, default=None)

_headers_getter: Callable[[], Any] | None = None
_headers_setter: Callable[[Any], Any] | None = None
_headers_resetter: Callable[[Any], None] | None = None
_unconfigured_headers_warned = False


def reset_global_configuration() -> None:
    """Reset all module-level configuration to defaults.

    Intended for test teardown to prevent cross-test contamination.
    """
    global _headers_getter, _headers_setter, _headers_resetter
    global _unconfigured_headers_warned
    _headers_getter = None
    _headers_setter = None
    _headers_resetter = None
    _unconfigured_headers_warned = False


def configure_headers_context_provider(
    *,
    get_headers: Callable[[], Any],
    set_headers: Callable[[Any], Any],
    reset_headers: Callable[[Any], None],
) -> None:
    """Configure framework-provided header context accessors.

    Must be called during application startup, before serving requests.
    """

    global _headers_getter, _headers_setter, _headers_resetter
    if _headers_getter is not None:
        logger.warning("Overwriting previously configured headers_context_provider")
    _headers_getter = get_headers
    _headers_setter = set_headers
    _headers_resetter = reset_headers


def set_headers_context(headers: Any) -> Any:
    """Set current request headers in the configured framework context."""
    if _headers_setter is None:
        raise RuntimeError(
            "Headers context not configured. "
            "Call configure_headers_context_provider() "
            "before using the context system."
        )
    return _headers_setter(headers)


def reset_headers_context(token: Any) -> None:
    """Reset current request headers from the configured framework context."""
    if token is None:
        return
    if _headers_resetter is None:
        raise RuntimeError(
            "Headers context not configured. "
            "Call configure_headers_context_provider() "
            "before using the context system."
        )
    _headers_resetter(token)


def set_path_params(path_params: PathValue) -> Token[PathValue | None]:
    """Store path parameters for the current async context; returns a token for reset."""
    return _path_context.set(path_params)


def reset_path_params(token: Token[PathValue | None]) -> None:
    """Restore path parameters to their previous value."""
    _path_context.reset(token)


def set_query_params(query_params: PathValue) -> Token[PathValue | None]:
    """Store query parameters for the current async context; returns a token for reset."""
    return _query_context.set(query_params)


def reset_query_params(token: Token[PathValue | None]) -> None:
    """Restore query parameters to their previous value."""
    _query_context.reset(token)


def set_api_version_context(version: str | None) -> Token[str | None]:
    """Store the resolved API version for the current async context."""
    return _api_version_context.set(version)


def reset_api_version_context(token: Token[str | None]) -> None:
    """Restore the API version to its previous value."""
    _api_version_context.reset(token)


def get_path_params() -> PathValue:
    """Return request path parameters captured in the current context."""
    params = _path_context.get()
    if params is None:
        return PathValue()
    return params


def get_query_params() -> PathValue:
    """Return request query parameters captured in the current context."""
    params = _query_context.get()
    if params is None:
        return PathValue()
    return params


def get_api_version() -> str | None:
    """Return resolved API version for the current request context."""
    return _api_version_context.get()


def get_headers() -> Any:
    """Return current request headers captured during dispatch."""
    global _unconfigured_headers_warned
    if _headers_getter is None:
        if not _unconfigured_headers_warned:
            _unconfigured_headers_warned = True
            logger.warning(
                "Headers context provider not configured. "
                "get_headers(), get_app_id(), and get_hit_id() will return empty values. "
                "Call configure_headers_context_provider() during startup."
            )
        return {}
    headers = _headers_getter()
    if headers is None:
        return {}
    return headers


def get_app_id() -> str | None:
    """Return the current request app-id header value."""
    val = get_headers().get(APP_ID_HEADER_NAME, None)
    return str(val) if val is not None else None


def get_hit_id() -> str | None:
    """Return the current request hit-id header value."""
    val = get_headers().get(HIT_ID_HEADER_NAME, None)
    return str(val) if val is not None else None


__all__ = (
    "configure_headers_context_provider",
    "get_api_version",
    "get_app_id",
    "get_headers",
    "get_hit_id",
    "get_path_params",
    "get_query_params",
    "reset_api_version_context",
    "reset_global_configuration",
    "reset_headers_context",
    "reset_path_params",
    "reset_query_params",
    "set_api_version_context",
    "set_headers_context",
    "set_path_params",
    "set_query_params",
)
