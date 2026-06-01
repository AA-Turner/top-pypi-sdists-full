"""Domain error hierarchy for the service layer.

Services raise these instead of ``HTTPException`` — keeping business logic
transport-agnostic.  The versioning framework's exception handler (or a
standalone handler registered via ``service_exception_handler``) maps them
to structured ``APIErrorResponse`` JSON automatically.

Each error carries:

* ``message`` — human-readable summary (becomes the ``meta.error`` field)
* ``detail`` — optional extended description (becomes ``errors[0].detail``)
* ``code`` — optional machine-readable error code (e.g. ``"DUPLICATE_EMAIL"``)
* ``status_code`` — HTTP status the handler will use (class-level default,
  overridable per-instance)
"""


class ServiceError(Exception):
    """Base class for all domain/service-layer errors.

    Subclasses set ``status_code`` as a class attribute.  Individual
    raises can override via the constructor keyword.
    """

    status_code: int = 500

    def __init__(
        self,
        message: str = "Internal service error",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail
        self.code = code
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(ServiceError):
    """The requested resource does not exist."""

    status_code: int = 404

    def __init__(
        self,
        message: str = "Resource not found",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message, detail=detail, code=code, status_code=status_code)


class ConflictError(ServiceError):
    """A write was rejected due to a conflict (duplicate, version mismatch, …)."""

    status_code: int = 409

    def __init__(
        self,
        message: str = "Conflict",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message, detail=detail, code=code, status_code=status_code)


class ValidationError(ServiceError):
    """Business-rule validation failed (distinct from request-schema validation)."""

    status_code: int = 422

    def __init__(
        self,
        message: str = "Validation failed",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message, detail=detail, code=code, status_code=status_code)


class AuthorizationError(ServiceError):
    """The authenticated user is not allowed to perform this action."""

    status_code: int = 403

    def __init__(
        self,
        message: str = "Forbidden",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message, detail=detail, code=code, status_code=status_code)


class DownstreamError(ServiceError):
    """A call to a downstream service (via a delegate) failed."""

    status_code: int = 502

    def __init__(
        self,
        message: str = "Downstream service error",
        *,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, detail=detail, code=code, status_code=status_code)
        if cause is not None:
            self.__cause__ = cause


__all__ = (
    "AuthorizationError",
    "ConflictError",
    "DownstreamError",
    "NotFoundError",
    "ServiceError",
    "ValidationError",
)
