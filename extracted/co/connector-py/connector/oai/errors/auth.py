"""
Authentication exception classes.

Raise these when existing credentials no longer grant access — i.e., the
upstream API rejected the request due to an auth-related failure.

Fault: UPSTREAM  |  Category: AUTHENTICATION
"""

from typing import ClassVar

from connector_sdk_types.errors import ConnectorErrorCode

from .base import ConnectorError


class AuthenticationError(ConnectorError):
    """
    Raise when the upstream API rejects the request because credentials are
    missing, invalid, or not recognised (HTTP 401 semantics).

    For more specific auth failures, prefer a subclass:
    - Token/session expired → ``AuthenticationExpiredError``
    - Credentials actively revoked → ``CredentialsRevokedError``
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.UNAUTHORIZED
    DEFAULT_MESSAGE: ClassVar[str] = "Authentication failed"
    DEFAULT_HINT: ClassVar[str | None] = "Please contact support if the problem persists."


class AuthenticationExpiredError(AuthenticationError):
    """
    Raise when a token or session has expired and must be refreshed before
    retrying.  The caller should attempt a token refresh or re-authentication.
    """

    DEFAULT_CODE = ConnectorErrorCode.AUTHENTICATION_EXPIRED
    DEFAULT_MESSAGE = "Authentication has expired"
    DEFAULT_HINT = None


class CredentialsRevokedError(AuthenticationError):
    """
    Raise when credentials have been actively revoked and cannot be refreshed.
    Re-connection with new credentials is required.
    """

    DEFAULT_CODE = ConnectorErrorCode.CREDS_REVOKED
    DEFAULT_MESSAGE = "Credentials have been revoked"
    DEFAULT_HINT = "Visit the end system and verify that the credentials have not been revoked."
