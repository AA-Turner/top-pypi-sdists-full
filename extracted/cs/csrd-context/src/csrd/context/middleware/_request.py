"""Request context middleware for setting up headers context.

Implemented as a raw ASGI middleware (no ``BaseHTTPMiddleware``) so that
``StreamingResponse`` and SSE endpoints are not buffered.
"""

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from .._contextvars import (
    configure_headers_context_provider,
    reset_headers_context,
    set_headers_context,
)
from .._fastapi_headers import headers_context


def _setup_fastapi_headers_provider() -> None:
    """Wire the FastAPI headers ContextVar as the headers provider."""
    configure_headers_context_provider(
        get_headers=headers_context.get,
        set_headers=headers_context.set,
        reset_headers=headers_context.reset,
    )


class RequestContextMiddleware:
    """Raw ASGI middleware that captures request headers into context variables.

    Unlike ``BaseHTTPMiddleware``, this does **not** buffer the response body,
    so ``StreamingResponse`` and SSE endpoints work correctly.
    """

    def __init__(self, app: ASGIApp, **kwargs: object) -> None:
        self.app = app
        _setup_fastapi_headers_provider()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        token = set_headers_context(request.headers)
        try:
            await self.app(scope, receive, send)
        finally:
            reset_headers_context(token)


__all__ = ("RequestContextMiddleware",)
