"""Request ID propagation middleware.

Adds X-Request-ID to every request/response for distributed tracing.
Works with FastAPI, Starlette, or any ASGI framework.
"""

import uuid
from contextvars import ContextVar

import structlog

# Context variable accessible anywhere in the request lifecycle
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

logger = structlog.get_logger()


def get_request_id() -> str:
    """Get current request ID from context."""
    return request_id_var.get()


# FastAPI / Starlette middleware
try:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    class RequestIDMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next) -> Response:
            rid = request.headers.get("x-request-id", str(uuid.uuid4()))
            request_id_var.set(rid)

            # Bind to structlog context
            structlog.contextvars.bind_contextvars(request_id=rid)

            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response

except ImportError:
    pass  # Starlette not installed — skip ASGI middleware
