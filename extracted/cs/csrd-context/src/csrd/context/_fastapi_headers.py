"""FastAPI-specific context variable for request headers."""

from contextvars import ContextVar

from starlette.datastructures import Headers

HEADERS_KEY = "request_headers"

_EMPTY_HEADERS = Headers()

headers_context: ContextVar[Headers] = ContextVar(HEADERS_KEY, default=_EMPTY_HEADERS)


def get_headers() -> Headers:
    """Return request headers stored in the current context."""
    return headers_context.get()


__all__ = ("HEADERS_KEY", "get_headers", "headers_context")
