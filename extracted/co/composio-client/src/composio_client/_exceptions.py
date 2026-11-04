"""Stainless-compatible error hierarchy.

Mirrors the published Stainless ``composio-client`` Python package (the drop-in
target) so downstream ``except`` / ``isinstance`` checks keep working: the class
names and the inheritance chain are part of the contract
(``BadRequestError`` -> ``APIStatusError`` -> ``APIError`` -> ``ComposioError`` ->
``Exception``). The status -> class routing mirrors the TS golden reference
(``src/compat/error.ts``).
"""

from __future__ import annotations

from typing import Any

import httpx

__all__ = [
    "ComposioError",
    "APIError",
    "APIStatusError",
    "APIConnectionError",
    "APITimeoutError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]


class ComposioError(Exception):
    """Base class for every error raised by this library."""


class APIError(ComposioError):
    """Base class for errors originating from an API interaction."""

    message: str
    request: httpx.Request | None
    #: The parsed JSON body of the response that caused the error, when available.
    body: object | None

    def __init__(
        self,
        message: str,
        request: httpx.Request | None = None,
        *,
        body: object | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.request = request
        self.body = body


class APIResponseValidationError(APIError):
    """Raised when a successful response fails to validate against its model."""

    response: httpx.Response
    status_code: int

    def __init__(
        self,
        response: httpx.Response,
        body: object | None = None,
        *,
        message: str | None = None,
    ) -> None:
        super().__init__(
            message or "Data returned by API invalid for expected schema.",
            response.request,
            body=body,
        )
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """Raised when the API returns a non-success HTTP status code."""

    response: httpx.Response
    status_code: int
    #: The request id the API assigned: the ``x-request-id`` response header
    #: first, the envelope's ``request_id`` otherwise, ``None`` when neither is
    #: present. Not part of the Stainless surface — a sanctioned superset,
    #: mirroring ``APIError.requestId`` in the TS kernel.
    request_id: str | None

    def __init__(self, message: str, *, response: httpx.Response, body: object | None) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        details = self.details
        header_id = response.headers.get("x-request-id")
        self.request_id = header_id or (details.get("request_id") if details is not None else None)

    @property
    def details(self) -> dict[str, Any] | None:
        """The body narrowed to the Composio error envelope's inner object.

        Every Apollo error response carries ``{"error": {"message", "code",
        "slug", "status", "request_id"?, "suggested_fix"?, "errors"?}}``;
        anything else (a proxy's HTML 502, foreign JSON) is ``None``. ``body``
        stays the raw parsed body. Same superset status as ``request_id``.
        """
        return _error_details(self.body)


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx.Request) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx.Request) -> None:
        super().__init__(message="Request timed out.", request=request)


class BadRequestError(APIStatusError):
    pass


class AuthenticationError(APIStatusError):
    pass


class PermissionDeniedError(APIStatusError):
    pass


class NotFoundError(APIStatusError):
    pass


class ConflictError(APIStatusError):
    pass


class UnprocessableEntityError(APIStatusError):
    pass


class RateLimitError(APIStatusError):
    pass


class InternalServerError(APIStatusError):
    pass


_STATUS_TO_ERROR: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def _error_details(body: object | None) -> dict[str, Any] | None:
    """Narrow a parsed error body to the envelope's inner object.

    Checks exactly the fields the shared ``Error`` schema requires plus the
    optional ones' types (mirrors ``errorDetails`` in the TS kernel).
    """
    if not isinstance(body, dict):
        return None
    inner = body.get("error")
    if not isinstance(inner, dict):
        return None
    if not isinstance(inner.get("message"), str) or not isinstance(inner.get("slug"), str):
        return None
    if not _is_int(inner.get("code")) or not _is_int(inner.get("status")):
        return None
    for key in ("request_id", "suggested_fix"):
        if key in inner and not isinstance(inner[key], str):
            return None
    errors = inner.get("errors")
    if errors is not None and not (
        isinstance(errors, list) and all(isinstance(item, str) for item in errors)
    ):
        return None
    return {key: value for key, value in inner.items() if key in _ENVELOPE_KEYS}


_ENVELOPE_KEYS = frozenset({"message", "code", "slug", "status", "request_id", "suggested_fix", "errors"})


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _error_message(status_code: int, body: object | None) -> str:
    """Build the exception message, preferring ``body["error"]["message"]``.

    The v3.1 API wraps errors as ``{"error": {"message": ...}}``; fall back to
    the whole body, then to a status-only message (mirrors ``makeMessage`` in
    the TS kernel).
    """
    detail: object | None = None
    if isinstance(body, dict):
        err = body.get("error", body)
        if isinstance(err, dict):
            detail = err.get("message")
        if detail is None:
            detail = err if err else None
    if detail:
        text = detail if isinstance(detail, str) else repr(detail)
        return f"{status_code} {text}"
    return f"{status_code} status code (no body)"


def status_error(response: httpx.Response, body: object | None) -> APIStatusError:
    """Map an HTTP error response to the matching Stainless error class."""
    message = _error_message(response.status_code, body)
    cls = _STATUS_TO_ERROR.get(response.status_code)
    if cls is None:
        cls = InternalServerError if response.status_code >= 500 else APIStatusError
    return cls(message, response=response, body=body)
