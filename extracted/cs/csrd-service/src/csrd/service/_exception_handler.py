"""FastAPI exception handler that maps exceptions to ``APIErrorResponse``.

Register with ``configure_versioned_api``::

    from csrd.service import service_exception_handler
    from csrd.versioning import VersionedApiConfig

    configure_versioned_api(
        app,
        version_mapping=VERSIONS,
        config=VersionedApiConfig(
            ex_handlers=[(Exception, service_exception_handler)],
        ),
    )

Or register directly on a plain FastAPI app::

    app.add_exception_handler(Exception, service_exception_handler)
"""

import contextlib
import datetime
import logging
import uuid
from datetime import UTC

from fastapi import Request
from fastapi.responses import JSONResponse

from csrd.models.errors import APIErrorResponse, APIVersion, Error, ErrorMeta

from ._errors import ServiceError


def _get_request_id(request: Request) -> str:
    """Best-effort extraction of request ID from scope, falling back to a UUID."""
    try:
        return str(request.scope["_request_context"]["hit_id"])
    except (KeyError, TypeError):
        return str(uuid.uuid4())


def _get_api_version(request: Request) -> APIVersion:
    served = None
    with contextlib.suppress(AttributeError, TypeError):
        served = request.scope.get("api_version")  # type: ignore[union-attr]
    return APIVersion(served=served)


async def service_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Convert exceptions into a structured ``APIErrorResponse``.

    ``ServiceError`` values preserve their status/message/detail/code.
    All other exceptions are logged with traceback and returned as a generic 500.
    """
    errors: list[Error] = []

    if isinstance(exc, ServiceError):
        status_code = exc.status_code
        error_message = exc.message
        if exc.detail or exc.code:
            errors.append(Error(title=exc.message, detail=exc.detail, code=exc.code))
    else:
        status_code = 500
        error_message = "Internal Server Error"

        # Prefer ContextLogger when available; fall back to stdlib logging.
        try:
            from csrd.logging import ContextLogger  # type: ignore[import-not-found]

            ContextLogger(logging.getLogger("csrd.service")).exception(
                "Unhandled exception",
                meta={"method": request.method, "path": request.url.path},
            )
        except ImportError:
            logging.getLogger("csrd.service").exception(
                "Unhandled exception method=%s path=%s",
                request.method,
                request.url.path,
            )

    body = APIErrorResponse(
        meta=ErrorMeta(
            status=status_code,
            error=error_message,
            method=request.method,
            path=request.url.path,
            request_id=_get_request_id(request),
            timestamp=datetime.datetime.now(UTC),
            api_version=_get_api_version(request),
        ),
        errors=errors,
    )

    return JSONResponse(
        status_code=status_code,
        content=body.as_dict(by_alias=True, mode="json"),
    )


__all__ = ("service_exception_handler",)
