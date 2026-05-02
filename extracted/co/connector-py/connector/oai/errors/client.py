"""
Client exception classes.

Raise these when the request from the initiating system (Lumos) is invalid.
These are permanent failures — retrying the same request will not help; the
caller must fix the input.

Fault: CALLER  |  Category: CLIENT
"""

from typing import ClassVar

from connector_sdk_types.errors import ConnectorErrorCode

from .base import ConnectorError


class ClientError(ConnectorError):
    """
    Base class for caller/input errors.  Raise when Lumos sent provably
    invalid input to the connector or upstream API.

    Prefer a more specific subclass where possible:
    - Resource not found → ``NotFoundError``
    - Invalid field value → ``InvalidValueError``
    - Unrecognised enum/string value → ``UnknownValueError``
    - Bad pagination token → ``InvalidPageTokenError``
    - Required integration parameter absent → ``MissingParameterError``
    - Conflicting resource state → ``ConflictError``
    """

    DEFAULT_CODE: ClassVar[ConnectorErrorCode] = ConnectorErrorCode.BAD_REQUEST
    DEFAULT_MESSAGE: ClassVar[str] = "The request contains invalid input"
    DEFAULT_HINT: ClassVar[str | None] = None


class NotFoundError(ClientError):
    """
    Raise when a specific resource, account, or entitlement does not exist
    in the upstream application.
    """

    DEFAULT_CODE = ConnectorErrorCode.NOT_FOUND
    DEFAULT_MESSAGE = "The requested resource was not found."


class InvalidValueError(ClientError):
    """
    Raise when a field value fails validation — wrong type, out-of-range,
    or violates a business logic rule.
    """

    DEFAULT_CODE = ConnectorErrorCode.INVALID_VALUE
    DEFAULT_MESSAGE = "One or more field values are invalid."


class UnknownValueError(ClientError):
    """
    Raise when an enum or value is not recognised by the upstream API
    (e.g., an unsupported role name or resource type identifier).
    """

    DEFAULT_CODE = ConnectorErrorCode.UNKNOWN_VALUE
    DEFAULT_MESSAGE = "An unrecognised value was provided."


class InvalidPageTokenError(ClientError):
    """
    Raise when the pagination token supplied by the caller is malformed,
    expired, or does not match the current query.
    """

    DEFAULT_CODE = ConnectorErrorCode.INVALID_PAGE_TOKEN
    DEFAULT_MESSAGE = "The pagination token is invalid or has expired."


class MissingParameterError(ClientError):
    """
    Raise when a required parameter is absent or empty, including tenant-level
    integration settings, required request fields, or any other mandatory input.
    """

    DEFAULT_CODE = ConnectorErrorCode.INTEGRATION_MISSING_PARAMETER
    DEFAULT_MESSAGE = (
        "A required integration parameter is missing. Please check the integration configuration."
    )


class ConflictError(ClientError):
    """
    Raise when the requested operation conflicts with the current state of
    a resource (e.g., attempting to create a resource that already exists).
    """

    DEFAULT_CODE = ConnectorErrorCode.CONFLICT
    DEFAULT_MESSAGE = "The operation conflicts with the current resource state."


class InvalidConfigurationError(InvalidValueError):
    """
    Raise when a connector settings value is present but structurally invalid —
    wrong URL format, invalid domain shape, missing required scheme, etc.

    Distinct from ``MissingParameterError`` (the value is absent) and from
    generic ``InvalidValueError`` (a request-time field is wrong).  Use this
    when validating ``settings_model`` values at startup or at the top of a
    capability before any upstream call is made.

    Example:

        raise InvalidConfigurationError(
            message="Account Base URL must start with https://"
        )
        raise InvalidConfigurationError(
            message=f"Workspace URL must not include a path: {url!r}"
        )
    """

    DEFAULT_CODE = ConnectorErrorCode.INVALID_VALUE
    DEFAULT_MESSAGE = "The integration configuration contains an invalid value."
    DEFAULT_HINT = "Review the integration settings and correct the indicated field."
