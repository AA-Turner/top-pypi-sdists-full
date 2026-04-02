"""
Enrichment layer for ConnectorErrorCode.

ConnectorErrorCode itself is generated from TypeSpec — see connector_sdk_types/generated/models/sdk_error_code.py.
This module re-exports it and adds the behavioural signal frozensets that live outside the generated layer.

Design rules:
- Codes encode *what happened*, never *what to do*. Behavioral signals (retryable, reauth,
  etc.) are expressed via the frozensets below so that callers never need to hardcode lists.
- Backwards-compatible: the old ErrorCode enum values are preserved but deprecated.
"""

from connector_sdk_types.generated.models.connector_error_code import ConnectorErrorCode
from connector_sdk_types.generated.models.error_code import ErrorCode

__all__ = [
    "ConnectorErrorCode",
    "THROTTLE_AND_RETRY_CODES",
    "RETRYABLE_CODES",
    "REFRESHABLE_CODES",
    "DEPRECATED_CODE_REDIRECTS",
]

# Behavioural frozensets
# Source of truth for retry/refresh logic. Moved from the Lumos App repository to the SDK
# so that the SDK owns the domain knowledge of what is retryable — not the caller.

REFRESHABLE_CODES: frozenset[ConnectorErrorCode] = frozenset(
    {
        ConnectorErrorCode.UNAUTHORIZED,
        ConnectorErrorCode.AUTHENTICATION_EXPIRED,
        ConnectorErrorCode.CREDS_REVOKED,
    }
)
"""Errors that indicate a credential problem — a refresh or re-auth may restore access."""

THROTTLE_AND_RETRY_CODES: frozenset[ConnectorErrorCode] = frozenset(
    {
        ConnectorErrorCode.RATE_LIMIT,
    }
)
"""Errors that require throttled retry (respect Retry-After / back-off)."""

RETRYABLE_CODES: frozenset[ConnectorErrorCode | ErrorCode] = frozenset(
    {
        ConnectorErrorCode.INTERNAL_ERROR,
        ConnectorErrorCode.BAD_GATEWAY,
        ConnectorErrorCode.SERVICE_ERROR,
        ConnectorErrorCode.REQUEST_TIMEOUT,
        ConnectorErrorCode.CONNECTION_TIMEOUT,
        ConnectorErrorCode.CONNECTION_REJECTED,
        ConnectorErrorCode.CONNECTION_CLOSED,
    }
)
"""Errors that are safe to retry immediately (no throttle needed)."""

# Mapping from deprecated ErrorCode string values to their ConnectorErrorCode replacements.
# Used by the SDK's DefaultHandler to normalise connector errors at the boundary,
# and by linters/migration tooling to flag stale usages.
DEPRECATED_CODE_REDIRECTS: dict[str, ConnectorErrorCode] = {
    **{
        code.value: ConnectorErrorCode(code.value)
        if code.value in ConnectorErrorCode.__members__.values()
        else ConnectorErrorCode.INTERNAL_ERROR
        for code in ErrorCode
    },
    "unexpected_error": ConnectorErrorCode.INTERNAL_ERROR,  # same behavior (retried)
    "not_implemented": ConnectorErrorCode.UNSUPPORTED_OPERATION,  # reduction
    "client_call_error": ConnectorErrorCode.INVALID_RESPONSE,  # same behavior (not retried)
    "api_error": ConnectorErrorCode.INVALID_RESPONSE,  # same behavior (not retried)
    "unauthenticated": ConnectorErrorCode.UNAUTHORIZED,  # reduction
}
