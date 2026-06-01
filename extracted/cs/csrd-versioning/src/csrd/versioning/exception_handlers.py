import datetime
import re
import uuid
from datetime import UTC

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from csrd.context import get_api_version
from csrd.context.middleware._logging import REQUEST_SCOPE_KEY
from csrd.models.errors import APIErrorResponse, APIVersion, ErrorMeta
from csrd.versioning._constants import API_VERSION_HEADER_NAME


def _display_api_version(version: str | None) -> str | None:
    if version is None:
        return None
    if str(version).lower() == "unv":
        return "Unversioned"
    return version


_VERSION_SEGMENT_RE = re.compile(
    r"(unv|unversioned|latest|v\d+(?:[._-]\d+)*)(?:/|$)",
    flags=re.IGNORECASE,
)


def _get_served_api_version(request: Request) -> str | None:
    # 1. Scope key set by VersionDispatchMiddleware
    scope = getattr(request, "scope", None)
    if isinstance(scope, dict):
        scoped_version = scope.get("api_version")
        if isinstance(scoped_version, str):
            return _display_api_version(scoped_version)

    # 2. Contextvar set by set_api_version_context()
    ctx_version = get_api_version()
    if ctx_version is not None:
        return _display_api_version(ctx_version)

    # 3. Path params resolved by FastAPI routing
    path_params = getattr(request, "path_params", None)
    if isinstance(path_params, dict):
        version = path_params.get("version")
        if isinstance(version, str):
            return _display_api_version(version)

    # 4. Best-effort path parsing (prefix-agnostic)
    path = getattr(getattr(request, "url", None), "path", "")
    if isinstance(path, str):
        for segment in path.strip("/").split("/"):
            if _VERSION_SEGMENT_RE.fullmatch(segment):
                return _display_api_version(segment)

    return None


def _api_version_from_request(request: Request) -> APIVersion:
    requested = None
    headers = getattr(request, "headers", None)
    if headers is not None:
        requested_value = headers.get(API_VERSION_HEADER_NAME)
        requested = requested_value if isinstance(requested_value, str) else None

    served = _get_served_api_version(request)
    return APIVersion(served=served, requested=requested)


def _get_request_id(request: Request):
    try:
        return request.scope[REQUEST_SCOPE_KEY]["hit_id"]
    except KeyError:
        return str(uuid.uuid4())


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIErrorResponse(
            meta=ErrorMeta(
                status=exc.status_code,
                error=exc.detail or "Unknown Error",
                method=request.method,
                path=request.url.path,
                request_id=_get_request_id(request),
                timestamp=datetime.datetime.now(UTC),
                api_version=_api_version_from_request(request),
            ),
            errors=[],
        ).as_dict(by_alias=True, mode="json"),
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=APIErrorResponse(
            meta=ErrorMeta(
                status=status.HTTP_400_BAD_REQUEST,
                error="Validation Error",
                method=request.method,
                path=request.url.path,
                request_id=_get_request_id(request),
                timestamp=datetime.datetime.now(UTC),
                api_version=_api_version_from_request(request),
            ),
            errors=[],
        ).as_dict(by_alias=True, mode="json"),
    )


EXCEPTION_HANDLERS = {
    # the HTTPException is being intercepted for 404s likely in the instana middleware
    # force a 404 to be handled by the http_exception_handler
    404: http_exception_handler,
    HTTPException: http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
}

__all__ = (
    "EXCEPTION_HANDLERS",
    "http_exception_handler",
    "request_validation_exception_handler",
)
