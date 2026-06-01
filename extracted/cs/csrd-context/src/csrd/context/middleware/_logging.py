"""HTTP logging middleware for FastAPI applications.

Implemented as a raw ASGI middleware (no ``BaseHTTPMiddleware``) so that
``StreamingResponse`` and SSE endpoints are not buffered.
"""

import logging
import time
import uuid
from collections import defaultdict
from http import HTTPStatus
from typing import Any, TypedDict

from starlette.requests import Request
from starlette.routing import Match
from starlette.types import ASGIApp, Receive, Scope, Send

from csrd.models.claims import UserClaims

logger = logging.getLogger(__name__)

REQUEST_SCOPE_KEY = "__DS__"


class RequestScope(TypedDict, total=False):
    hit_id: str
    app_id: str
    user_info: UserClaims | None


class HTTPLoggingMiddleware:
    """Raw ASGI middleware to log HTTP request details including timing,
    user context, and response information.

    Unlike ``BaseHTTPMiddleware``, this does **not** buffer the response
    body, so ``StreamingResponse`` and SSE endpoints work correctly.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        scope[REQUEST_SCOPE_KEY] = RequestScope()

        elapsed = -time.perf_counter()

        query_params: dict[str, list[str]] = defaultdict(list)
        for key, value in request.query_params.multi_items():
            query_params[key].append(value)

        extras: dict[str, Any] = {
            "method": request.method,
            "uri": request.url.path,
            "uri_mapping": self._get_route_path(request),
            "query_params": query_params,
            "hit_id": request.headers.get("x-client-hit-id") or str(uuid.uuid4()),
            "app_id": request.headers.get("x-client-app-id", "unknown"),
        }

        logger.info("http.request.start", extra=extras)

        # Track response status via a wrapper around send
        status_holder: dict[str, int] = {"status": 0}

        async def send_wrapper(message: Any) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
            await send(message)

        exc_info = None
        level = logging.INFO
        try:
            await self.app(scope, receive, send_wrapper)
            status = status_holder["status"]
            level = self._get_log_level(status)
        except Exception as exc:
            status = getattr(exc, "status_code", 500)
            extras["error"] = exc.__cause__
            exc_info = exc
            level = logging.ERROR
            raise
        finally:
            ds_scope = scope.get(REQUEST_SCOPE_KEY) or {}
            extras.update(
                hit_id=ds_scope.get("hit_id", "unknown"),
                app_id=ds_scope.get("app_id", "unknown"),
            )
            if user_info := ds_scope.get("user_info"):
                extras.update(
                    user_id=user_info.sub,
                    user_email=user_info.user_name,
                )
            elapsed += time.perf_counter()
            extras["elapsed_millis"] = int(elapsed * 1000)
            extras["status"] = status
            logger.log(level, "http.request.complete", exc_info=exc_info, extra=extras)

    @staticmethod
    def _get_log_level(status: int) -> int:
        http_status = HTTPStatus(status)
        if http_status.is_informational or http_status.is_success or http_status.is_redirection:
            return logging.INFO
        if http_status.is_client_error:
            return logging.WARNING
        return logging.ERROR

    @staticmethod
    def _get_route_path(request: Request) -> str:
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                return str(route.path)
        return request.url.path


__all__ = ("REQUEST_SCOPE_KEY", "HTTPLoggingMiddleware", "RequestScope")
