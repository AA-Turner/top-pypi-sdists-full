"""
connector.oai.errors — exception classes and handlers for Lumos connectors.

Backwards-compatible re-export surface.  Everything that was previously
importable from ``connector.oai.errors`` (the old single-file module) remains
importable from here.

New typed exception classes are also exported so connector authors can import
them directly:

    from connector.oai.errors import RateLimitError, NotFoundError
"""

from connector_sdk_types.generated import Error, ErrorCode, ErrorResponse

from .auth import AuthenticationError, AuthenticationExpiredError, CredentialsRevokedError
from .authz import AuthorizationError
from .base import (
    ConnectorError,
    DefaultHandler,
    ErrorMap,
    ExceptionHandler,
    GQLTransportHandler,
    HTTPHandler,
    handle_exception,
)
from .client import (
    ClientError,
    ConflictError,
    InvalidConfigurationError,
    InvalidPageTokenError,
    InvalidValueError,
    MissingParameterError,
    NotFoundError,
    UnknownValueError,
)
from .internal import InternalError, InvalidResponseError, UnsupportedOperationError
from .transient import (
    BudgetExhaustedError,
    ConnectionClosedError,
    ConnectionRejectedError,
    NetworkError,
    RateLimitError,
    RequestTimeoutError,
    TransientError,
    UpstreamError,
)

__all__ = [
    # SDK types
    "Error",
    "ErrorCode",
    "ErrorResponse",
    # Base infrastructure
    "ConnectorError",
    "ExceptionHandler",
    "DefaultHandler",
    "GQLTransportHandler",
    "HTTPHandler",
    "ErrorMap",
    "handle_exception",
    # Authentication (UPSTREAM / AUTHENTICATION)
    "AuthenticationError",
    "AuthenticationExpiredError",
    "CredentialsRevokedError",
    # Authorization (UPSTREAM / AUTHORIZATION)
    "AuthorizationError",
    # Transient (UPSTREAM+INFRASTRUCTURE / TRANSIENT)
    "TransientError",
    "RateLimitError",
    "BudgetExhaustedError",
    "UpstreamError",
    "NetworkError",
    "ConnectionRejectedError",
    "ConnectionClosedError",
    "RequestTimeoutError",
    # Client (CALLER / CLIENT)
    "ClientError",
    "NotFoundError",
    "InvalidValueError",
    "UnknownValueError",
    "InvalidPageTokenError",
    "MissingParameterError",
    "InvalidConfigurationError",
    "ConflictError",
    # Internal (CONNECTOR / INTERNAL)
    "InternalError",
    "InvalidResponseError",
    "UnsupportedOperationError",
]
