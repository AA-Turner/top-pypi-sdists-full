"""
Error classification for the Lumos Connector SDK.
"""

from __future__ import annotations

from connector_sdk_types.errors.codes import ConnectorErrorCode
from connector_sdk_types.generated.models.connector_error_category import ConnectorErrorCategory
from connector_sdk_types.generated.models.connector_error_fault import ConnectorErrorFault

__all__ = [
    "ConnectorErrorFault",
    "ConnectorErrorCategory",
    "CODE_FAULT_MAP",
    "CODE_CATEGORY_MAP",
]

CODE_FAULT_MAP: dict[ConnectorErrorCode, ConnectorErrorFault] = {
    ConnectorErrorCode.BAD_REQUEST: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.INVALID_VALUE: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.UNKNOWN_VALUE: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.NOT_FOUND: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.CONFLICT: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.INVALID_PAGE_TOKEN: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.INTEGRATION_MISSING_PARAMETER: ConnectorErrorFault.CALLER,
    ConnectorErrorCode.UNSUPPORTED_OPERATION: ConnectorErrorFault.CONNECTOR,
    ConnectorErrorCode.UNAUTHORIZED: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.AUTHENTICATION_EXPIRED: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.CREDS_REVOKED: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.PERMISSION_DENIED: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.RATE_LIMIT: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.BAD_GATEWAY: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.SERVICE_ERROR: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.REQUEST_TIMEOUT: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.BUDGET_EXHAUSTED: ConnectorErrorFault.UPSTREAM,
    ConnectorErrorCode.CONNECTION_TIMEOUT: ConnectorErrorFault.INFRASTRUCTURE,
    ConnectorErrorCode.CONNECTION_REJECTED: ConnectorErrorFault.INFRASTRUCTURE,
    ConnectorErrorCode.CONNECTION_CLOSED: ConnectorErrorFault.INFRASTRUCTURE,
    ConnectorErrorCode.INTERNAL_ERROR: ConnectorErrorFault.CONNECTOR,
    ConnectorErrorCode.INVALID_RESPONSE: ConnectorErrorFault.CONNECTOR,
}

CODE_CATEGORY_MAP: dict[ConnectorErrorCode, ConnectorErrorCategory] = {
    ConnectorErrorCode.BAD_REQUEST: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.INVALID_VALUE: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.UNKNOWN_VALUE: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.NOT_FOUND: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.CONFLICT: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.INVALID_PAGE_TOKEN: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.INTEGRATION_MISSING_PARAMETER: ConnectorErrorCategory.CLIENT,
    ConnectorErrorCode.UNSUPPORTED_OPERATION: ConnectorErrorCategory.INTERNAL,
    ConnectorErrorCode.UNAUTHORIZED: ConnectorErrorCategory.AUTHENTICATION,
    ConnectorErrorCode.AUTHENTICATION_EXPIRED: ConnectorErrorCategory.AUTHENTICATION,
    ConnectorErrorCode.CREDS_REVOKED: ConnectorErrorCategory.AUTHENTICATION,
    ConnectorErrorCode.PERMISSION_DENIED: ConnectorErrorCategory.AUTHORIZATION,
    ConnectorErrorCode.RATE_LIMIT: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.BUDGET_EXHAUSTED: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.BAD_GATEWAY: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.SERVICE_ERROR: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.CONNECTION_TIMEOUT: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.REQUEST_TIMEOUT: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.CONNECTION_REJECTED: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.CONNECTION_CLOSED: ConnectorErrorCategory.TRANSIENT,
    ConnectorErrorCode.INTERNAL_ERROR: ConnectorErrorCategory.INTERNAL,
    ConnectorErrorCode.INVALID_RESPONSE: ConnectorErrorCategory.INTERNAL,
}
