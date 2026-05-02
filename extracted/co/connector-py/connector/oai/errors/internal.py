"""
Internal exception classes.

Raise these when the failure is caused by a bug or misconfiguration inside
the connector itself — not by the caller or the upstream API.  These errors
require a code fix; retrying will not help.

Fault: CONNECTOR  |  Category: INTERNAL
"""

from typing import ClassVar

from connector_sdk_types.errors import ConnectorErrorCode

from .base import ConnectorError


class InternalError(ConnectorError):
    """
    Raise when there is a bug or misconfiguration inside the connector itself
    that is unrelated to the upstream API or the caller's input.

    Prefer a more specific subclass where possible:
    - Upstream returned an unreadable/unexpected response → ``InvalidResponseError``
    - Operation is not implemented by this connector → ``UnsupportedOperationError``
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.INTERNAL_ERROR
    DEFAULT_MESSAGE: ClassVar[str] = "An internal connector error occurred"
    DEFAULT_HINT: ClassVar[str | None] = None


class InvalidResponseError(InternalError):
    """
    Raise when the upstream API returned a structurally unexpected or
    unreadable response that the connector cannot handle.

    This indicates the connector's response-parsing logic does not match the
    current upstream API contract — a connector-side fix is required.

    Use ``UpstreamError`` (in ``transient.py``) instead for temporary 5xx
    outages where the response format is not the issue.
    """

    DEFAULT_CODE = ConnectorErrorCode.INVALID_RESPONSE
    DEFAULT_MESSAGE = "The upstream API returned an unexpected or unreadable response."


class UnsupportedOperationError(InternalError):
    """
    Raise when the connector does not support the requested operation for
    this integration or plan tier.

    This is a permanent failure — the caller should not retry.
    """

    DEFAULT_CODE = ConnectorErrorCode.UNSUPPORTED_OPERATION
    DEFAULT_MESSAGE = "This operation is not supported by the connector"
