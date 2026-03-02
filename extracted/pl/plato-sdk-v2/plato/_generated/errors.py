"""API error types for Plato API."""

from __future__ import annotations

from typing import Any


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        status_code: int,
        message: str | None = None,
        body: dict[str, Any] | None = None,
    ):
        self.status_code = status_code
        self.message = message or f"API request failed with status {status_code}"
        self.body = body
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={self.message!r})"


class BadRequestError(APIError):
    """400 Bad Request - Invalid request parameters."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(400, message or "Bad request", body)


class UnauthorizedError(APIError):
    """401 Unauthorized - Invalid or missing authentication."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(401, message or "Unauthorized", body)


class ForbiddenError(APIError):
    """403 Forbidden - Insufficient permissions."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(403, message or "Forbidden", body)


class NotFoundError(APIError):
    """404 Not Found - Resource not found."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(404, message or "Not found", body)


class ConflictError(APIError):
    """409 Conflict - Resource conflict."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(409, message or "Conflict", body)


class UnprocessableEntityError(APIError):
    """422 Unprocessable Entity - Validation error."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(422, message or "Unprocessable entity", body)


class RateLimitError(APIError):
    """429 Too Many Requests - Rate limit exceeded."""

    def __init__(
        self,
        message: str | None = None,
        body: dict[str, Any] | None = None,
        retry_after: float | None = None,
    ):
        super().__init__(429, message or "Rate limit exceeded", body)
        self.retry_after = retry_after


class InternalServerError(APIError):
    """500 Internal Server Error - Server error."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(500, message or "Internal server error", body)


class ServiceUnavailableError(APIError):
    """503 Service Unavailable - Service temporarily unavailable."""

    def __init__(self, message: str | None = None, body: dict[str, Any] | None = None):
        super().__init__(503, message or "Service unavailable", body)


def raise_for_status(response) -> None:
    """Raise appropriate error based on response status code.

    Args:
        response: httpx.Response object

    Raises:
        APIError: Appropriate subclass based on status code
    """
    if response.is_success:
        return

    status = response.status_code

    try:
        body = response.json()
        message = body.get("message") or body.get("error") or body.get("detail")
    except Exception:
        body = None
        message = response.text or None

    error_map = {
        400: BadRequestError,
        401: UnauthorizedError,
        403: ForbiddenError,
        404: NotFoundError,
        409: ConflictError,
        422: UnprocessableEntityError,
        429: RateLimitError,
        500: InternalServerError,
        503: ServiceUnavailableError,
    }

    error_class = error_map.get(status, APIError)

    if status == 429:
        retry_after = response.headers.get("retry-after")
        raise RateLimitError(
            message=message,
            body=body,
            retry_after=float(retry_after) if retry_after else None,
        )

    if error_class == APIError:
        raise APIError(status, message, body)

    raise error_class(message, body)
