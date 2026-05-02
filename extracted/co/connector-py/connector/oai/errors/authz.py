"""
Authorization exception classes.

Raise these when credentials are valid but lack the required permission scope
for the requested operation (HTTP 403 semantics).

Fault: UPSTREAM  |  Category: AUTHORIZATION
"""

from typing import ClassVar

from connector_sdk_types.errors import ConnectorErrorCode

from .base import ConnectorError


class AuthorizationError(ConnectorError):
    """
    Raise when the credentials are valid but the account lacks the required
    permission scope to perform the operation.

    Re-connection with broader permissions is typically required — a simple
    token refresh is unlikely to help.
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.PERMISSION_DENIED
    DEFAULT_MESSAGE: ClassVar[str] = "Permission denied"
    DEFAULT_HINT: ClassVar[
        str | None
    ] = "Visit the end system and verify that the account has the required scope."
