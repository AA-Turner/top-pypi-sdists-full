"""
Backward compatibility re-export for exceptions.

The canonical exceptions live in istari_digital_client.legacy.exceptions.
This module re-exports them for backward compatibility.
"""

from istari_digital_client.legacy.exceptions import (
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
    "ApiAttributeError",
    "ApiException",
    "ApiKeyError",
    "ApiTypeError",
    "ApiValueError",
    "BadRequestException",
    "ConflictException",
    "ForbiddenException",
    "NotFoundException",
    "OpenApiException",
    "ServiceException",
    "UnauthorizedException",
    "UnprocessableEntityException",
]
