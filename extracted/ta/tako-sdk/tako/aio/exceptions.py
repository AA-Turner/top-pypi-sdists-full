"""Async client exceptions.

Hand-written (see ``.openapi-generator-ignore``): instead of a second, parallel
copy of the exception classes, the async client re-exports the single canonical
hierarchy from ``tako.exceptions``. Sync and async therefore raise *identical*
classes, so one ``except tako.exceptions.ApiException`` (or ``tako.ApiException``)
covers both lanes and ``isinstance`` works across them.

``tako.exceptions`` depends only on the standard library, so this re-export
introduces no import cycle.
"""

from tako.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    BadRequestException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    OpenApiException,
    ServiceException,
    UnauthorizedException,
    UnprocessableEntityException,
)

__all__ = [
    "OpenApiException",
    "ApiTypeError",
    "ApiValueError",
    "ApiAttributeError",
    "ApiKeyError",
    "ApiException",
    "BadRequestException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException",
    "ServiceException",
    "ConflictException",
    "UnprocessableEntityException",
]
