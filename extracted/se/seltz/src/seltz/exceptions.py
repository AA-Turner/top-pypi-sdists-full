"""Custom exceptions for the Seltz SDK."""

from typing import Optional

import grpc


class SeltzError(Exception):
    """Base exception for all Seltz SDK errors."""

    pass


class SeltzConfigurationError(SeltzError):
    """Raised when there's a configuration issue."""

    pass


class SeltzAuthenticationError(SeltzError):
    """Raised when authentication fails."""

    pass


class SeltzConnectionError(SeltzError):
    """Raised when connection to the API fails."""

    pass


class SeltzAPIError(SeltzError):
    """Raised when the API returns an error."""

    def __init__(
        self,
        message: str,
        grpc_code: Optional[grpc.StatusCode] = None,
        grpc_details: Optional[str] = None,
    ):
        super().__init__(message)
        self.grpc_code = grpc_code
        self.grpc_details = grpc_details


class SeltzTimeoutError(SeltzError):
    """Raised when a request times out."""

    pass


class SeltzRateLimitError(SeltzError):
    """Raised when rate limit is exceeded."""

    pass


def map_rpc_error(error: grpc.RpcError) -> SeltzError:
    """Translate a gRPC error into the matching Seltz exception."""
    code = error.code()
    details = error.details()

    if code == grpc.StatusCode.UNAUTHENTICATED:
        return SeltzAuthenticationError(f"Authentication failed: {details}")

    if code == grpc.StatusCode.UNAVAILABLE:
        return SeltzConnectionError(f"Connection failed: {details}")

    if code == grpc.StatusCode.DEADLINE_EXCEEDED:
        return SeltzTimeoutError(f"Request timed out: {details}")

    if code == grpc.StatusCode.RESOURCE_EXHAUSTED:
        return SeltzRateLimitError(f"Rate limit exceeded: {details}")

    return SeltzAPIError(f"API error: {details}", code, details)
