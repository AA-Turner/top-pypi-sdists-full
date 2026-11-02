"""Error hierarchy for the getanyapi SDK (SPEC 3.6).

Every failed call raises a subclass of :class:`AnyAPIError`. The HTTP status to
class mapping is frozen:

    400 -> BadRequestError
    401 -> AuthenticationError
    402 -> InsufficientBalanceError
    404 -> NotFoundError
    429 -> RateLimitedError
    502 -> UpstreamError
    (any other non-2xx) -> AnyAPIError

Transport failures raise :class:`ConnectionError` (status 0); timeouts raise
:class:`TimeoutError` (status 0). Both names intentionally shadow the Python
builtins of the same name and are exported from the package root.
"""

from __future__ import annotations

__all__ = [
    "AnyAPIError",
    "BadRequestError",
    "AuthenticationError",
    "InsufficientBalanceError",
    "NotFoundError",
    "ResultNotFoundError",
    "RateLimitedError",
    "UpstreamError",
    "ConnectionError",
    "TimeoutError",
    "RequestPendingError",
    "error_for_status",
]


class AnyAPIError(Exception):
    """Base class for every error raised by the SDK.

    Attributes:
        status: HTTP status code, or 0 for transport-level failures.
        request_id: The gateway's X-Anyapi-Request-Id response header when present
            (falling back to a proxy-set x-request-id), else None.
        code: Stable gateway error code when the JSON body includes one, else None.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int,
        request_id: str | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.request_id = request_id
        self.code = code


class BadRequestError(AnyAPIError):
    """HTTP 400: the input failed validation."""


class AuthenticationError(AnyAPIError):
    """HTTP 401: the API key is missing or invalid."""


class InsufficientBalanceError(AnyAPIError):
    """HTTP 402: the wallet balance or per-key cap was exceeded."""


class NotFoundError(AnyAPIError):
    """HTTP 404: the slug or resource does not exist."""


class ResultNotFoundError(NotFoundError):
    """Raised by :func:`getanyapi.unwrap` when a found-data result had ``found: false``.

    A subclass of :class:`NotFoundError` so ``except NotFoundError`` still catches
    it; catch ``ResultNotFoundError`` specifically to handle only empty results
    (not HTTP 404s). See SPEC 2.3 erratum.
    """


class RateLimitedError(AnyAPIError):
    """HTTP 429: too many requests. Retried automatically."""


class UpstreamError(AnyAPIError):
    """HTTP 502: an upstream backend failed."""


class ConnectionError(AnyAPIError):
    """A network or transport failure (status 0).

    This name intentionally shadows the Python builtin ``ConnectionError``.
    """


class TimeoutError(AnyAPIError):
    """A request that exceeded its timeout (status 0).

    This name intentionally shadows the Python builtin ``TimeoutError``.
    Timeouts are never retried.
    """


class RequestPendingError(TimeoutError):
    """The SDK deadline elapsed while durable work remained resumable."""

    def __init__(self, request_id: str) -> None:
        super().__init__(
            "request is still running; resume with requests.get or "
            f"requests.wait: {request_id}",
            status=0,
            request_id=request_id,
        )
        self.durable_request_id = request_id


_STATUS_MAP: dict[int, type[AnyAPIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    402: InsufficientBalanceError,
    404: NotFoundError,
    429: RateLimitedError,
    502: UpstreamError,
}


def error_for_status(
    status: int,
    message: str,
    *,
    request_id: str | None = None,
    code: str | None = None,
) -> AnyAPIError:
    """Build the mapped error for a non-2xx HTTP status (SPEC 3.6)."""
    cls = _STATUS_MAP.get(status, AnyAPIError)
    return cls(message, status=status, request_id=request_id, code=code)
