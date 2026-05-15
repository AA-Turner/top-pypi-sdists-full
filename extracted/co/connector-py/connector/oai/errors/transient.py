"""
Transient exception classes.

Raise these for temporary failures that are safe to retry.  All classes in
this module inherit from ``TransientError``, which signals to the caller that
a retry (with appropriate back-off) is expected to succeed.

Fault: UPSTREAM / INFRASTRUCTURE  |  Category: TRANSIENT
"""

from typing import ClassVar

from connector_sdk_types.errors import ConnectorErrorCode, ConnectorErrorMetadata

from .base import ConnectorError


class TransientError(ConnectorError):
    """
    Base class for temporary failures.  Raise when the upstream service or
    network is temporarily unavailable and the request can be safely retried.

    Prefer a more specific subclass where possible:
    - Rate-limited → ``RateLimitError``
    - Upstream server error (5xx) → ``UpstreamError``
    - Network-level failure → ``NetworkError`` (or its subclasses)
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.SERVICE_ERROR
    DEFAULT_MESSAGE: ClassVar[str] = "A transient error occurred"
    DEFAULT_HINT: ClassVar[str | None] = "Please retry the request."

    def __init__(
        self,
        *,
        retry_after_seconds: int | None = None,
        message: str | None = None,
        error_code: ConnectorErrorCode | None = None,
        app_error_code: str | None = None,
        hint: str | None = None,
        retryable: bool | None = None,
        throttled: bool | None = None,
        refreshable: bool | None = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            app_error_code=app_error_code,
            hint=hint,
            retryable=retryable,
            throttled=throttled,
            refreshable=refreshable,
        )
        self.retry_after_seconds = retry_after_seconds

    def get_error_metadata(self) -> ConnectorErrorMetadata:
        metadata = super().get_error_metadata()
        return metadata.model_copy(update={"retry_after_seconds": self.retry_after_seconds})


class RateLimitError(TransientError):
    """
    Raise when the upstream API has throttled the request.

    The caller should respect the ``Retry-After`` header or apply exponential
    back-off before retrying.
    """

    DEFAULT_CODE = ConnectorErrorCode.RATE_LIMIT
    DEFAULT_MESSAGE = "Rate limit exceeded"


class BudgetExhaustedError(TransientError):
    """
    Raise when execution would exceed the caller's execution budget.

    Example:
    The connector detected it was about to sleep past the caller's deadline
    (from ``RateLimitRequestInfo.max_execution_time``). Rather than
    sleeping and letting the caller's timeout cancel the request with no
    response, the connector raises early so a structured retryable error
    can be returned. Accepts a ``retry_after`` parameter to specify the
    recommended retry-after duration (in seconds).
    """

    DEFAULT_CODE = ConnectorErrorCode.BUDGET_EXHAUSTED
    DEFAULT_MESSAGE = "Rate limit wait would exceed caller deadline"


class UpstreamError(TransientError):
    """
    Raise when the upstream API returns an unexpected server-side error (5xx)
    or a malformed / unreadable response that indicates a temporary outage.

    Use ``InvalidResponseError`` (in ``internal.py``) instead if the connector
    itself misread a structurally correct response.
    """

    DEFAULT_CODE = ConnectorErrorCode.BAD_GATEWAY
    DEFAULT_MESSAGE = "The upstream service returned an unexpected error"


class NetworkError(TransientError):
    """
    Raise when the upstream API cannot be reached at the network/transport
    layer — DNS failure, TCP connection timeout, or connection refused.

    Prefer a more specific subclass where possible:
    - Connection timed out → ``NetworkError`` (default) or ``ConnectionTimeoutError`` alias
    - Connection actively rejected → ``ConnectionRejectedError``
    - Connection closed mid-request → ``ConnectionClosedError``
    - Request timed out after connecting → ``RequestTimeoutError``
    """

    DEFAULT_CODE = ConnectorErrorCode.CONNECTION_TIMEOUT
    DEFAULT_MESSAGE = "Failed to connect to the upstream service"


class ConnectionRejectedError(NetworkError):
    """
    Raise when the upstream service actively refused the connection
    (e.g., TCP RST, firewall block).
    """

    DEFAULT_CODE = ConnectorErrorCode.CONNECTION_REJECTED
    DEFAULT_MESSAGE = "The upstream service refused the connection"


class ConnectionClosedError(NetworkError):
    """
    Raise when the upstream service closed the connection unexpectedly
    mid-request (e.g., keep-alive timeout, server-side abrupt close).
    """

    DEFAULT_CODE = ConnectorErrorCode.CONNECTION_CLOSED
    DEFAULT_MESSAGE = "The upstream service closed the connection unexpectedly"


class RequestTimeoutError(NetworkError):
    """
    Raise when a request was sent successfully but the upstream service did
    not respond within the allowed time window.
    """

    DEFAULT_CODE = ConnectorErrorCode.REQUEST_TIMEOUT
    DEFAULT_MESSAGE = "The upstream service did not respond in time"
