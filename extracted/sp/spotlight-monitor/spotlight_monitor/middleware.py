"""
Spotlight Middleware

Auto-instruments FastAPI applications with:
- Request/response tracking
- Exception capture with full context
- Breadcrumb trail
"""

import time
import json
from typing import Callable, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response as StarletteResponse

from .exceptions import (
    Breadcrumb,
    RequestContext,
    capture_exception,
    ExceptionInfo,
)


class SpotlightMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for automatic request tracking and exception capture.
    """

    def __init__(self, app, spotlight):
        super().__init__(app)
        self.spotlight = spotlight

        self.skip_endpoints = {
            "/health", "/healthz", "/ready",
            "/docs", "/redoc", "/openapi.json",
            "/metrics",
        }

    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        if request.url.path in self.skip_endpoints:
            return await call_next(request)

        # Clear context for new request
        Breadcrumb.clear()
        RequestContext.clear()

        # Set request context
        headers = dict(request.headers)
        body = None

        # Get client IP
        ip_address = request.client.host if request.client else None
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            ip_address = forwarded.split(",")[0].strip()

        RequestContext.set(
            method=request.method,
            url=str(request.url),
            headers=headers,
            body=body,
            ip_address=ip_address,
            query_params=dict(request.query_params),
        )

        # Add breadcrumb for request start
        Breadcrumb.add(
            message=f"{request.method} {request.url.path}",
            category="http",
            level="info",
        )

        start_time = time.perf_counter()
        error_type = None
        error_message = None
        exception_info: Optional[ExceptionInfo] = None
        status_code = 500
        response_body = None
        request_data = {
            "query_params": dict(request.query_params),
            "method": request.method,
            "path": request.url.path,
        }

        try:
            response = await call_next(request)
            status_code = response.status_code

            # Buffer response body for validators
            body_parts = []
            async for chunk in response.body_iterator:
                body_parts.append(chunk)

            body_bytes = b"".join(body_parts)

            # Try to parse as JSON
            try:
                response_body = json.loads(body_bytes) if body_bytes else {}
            except (json.JSONDecodeError, UnicodeDecodeError):
                response_body = {}

            # Add breadcrumb for response
            Breadcrumb.add(
                message=f"Response {status_code}",
                category="http",
                level="info" if status_code < 400 else "error",
            )

            # Create new response with buffered body
            new_response = StarletteResponse(
                content=body_bytes,
                status_code=status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

            return new_response

        except Exception as exc:
            # Capture full exception info
            exception_info = capture_exception(
                exc,
                environment=getattr(self.spotlight, 'environment', 'production'),
                release=getattr(self.spotlight, 'release', None),
                tags=getattr(self.spotlight, 'tags', {}),
            )

            error_type = type(exc).__name__
            error_message = str(exc)

            # Re-raise to let FastAPI handle the response
            raise

        finally:
            # Calculate latency
            latency_ms = int((time.perf_counter() - start_time) * 1000)

            # Track request
            self.spotlight.track_request(
                endpoint=request.url.path,
                method=request.method,
                status_code=status_code,
                latency_ms=latency_ms,
                error_type=error_type,
                error_message=error_message,
                request_data=request_data,
                response_data=response_body,
                metadata={
                    "query_params": dict(request.query_params),
                },
            )

            # Track exception if captured
            if exception_info:
                self.spotlight.track_exception(exception_info)