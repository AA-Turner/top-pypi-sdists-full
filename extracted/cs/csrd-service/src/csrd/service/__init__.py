"""Service layer boilerplate for the CSRD pattern.

The ``csrd.service`` package provides:

* :class:`BaseService` - lightweight base with context accessors.
* **Domain errors** - :class:`ServiceError` hierarchy
  (:class:`NotFoundError`, :class:`ConflictError`, :class:`ValidationError`,
  :class:`AuthorizationError`, :class:`DownstreamError`) that keep business
  logic free of ``HTTPException``.
* :func:`service_exception_handler` - FastAPI handler that maps
  ``ServiceError`` to structured JSON and returns a generic structured JSON
  500 response for all other unhandled exceptions.
"""

from ._base_service import BaseService
from ._errors import (
    AuthorizationError,
    ConflictError,
    DownstreamError,
    NotFoundError,
    ServiceError,
    ValidationError,
)
from ._exception_handler import service_exception_handler

__all__ = (
    "AuthorizationError",
    "BaseService",
    "ConflictError",
    "DownstreamError",
    "NotFoundError",
    "ServiceError",
    "ValidationError",
    "service_exception_handler",
)
