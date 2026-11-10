from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional

from strong_typing.schema import json_schema_type


class DAPClientError(RuntimeError):
    """
    Raised when the client itself cannot carry out a request, as opposed to the
    server rejecting one. Covers missing or invalid configuration, malformed
    arguments, and unparsable responses.
    """


class DownloadError(DAPClientError):
    """
    Raised when fetching a resource payload fails, either because the host
    rejected the request or because the downloaded data cannot be stored.
    """

    def __init__(self, response_str: str) -> None:
        super().__init__(f"download error: {response_str}")


@json_schema_type
@dataclass
class ServerError(Exception):
    """
    An error returned by the server that doesn't match any known error shape.

    :param status_code: The HTTP status code of the response.
    :param body: Unspecified content returned by the server.
    """

    status_code: int
    body: Any

    def __str__(self) -> str:
        return f"Server responded with HTTP status {self.status_code}: {self.body!r}"


@json_schema_type
@dataclass
class OperationError(Exception):
    """
    Encapsulates an error from an endpoint operation.

    :param type: A machine-processable identifier for the error. Typically corresponds to the fully-qualified exception
        class, as per the type system of the language that emitted the message (e.g. Java, Python or Scala exception type).
    :param uuid: Unique identifier of the error. This identifier helps locate the exact source of the error (e.g. find
        the log entry in the server log stream). Make sure to include this identifier when contacting support.
    :param message: A human-readable description for the error for informational purposes. The exact format of the
        message is unspecified, and implementations should not rely on the presence of any specific information.
    """

    type: str
    uuid: str
    message: str


class AuthenticationError(OperationError):
    """
    Raised when the client fails to provide valid authentication credentials.
    """


@dataclass
class OAuthTokenError(Exception):
    """
    Raised when the OAuth2 token endpoint rejects a token request (e.g. an
    invalid client ID or secret). Distinct from AuthenticationError: this
    reports the OAuth2 token issuer's own error shape (RFC 6749 SS5.2), not
    the DAP API's error shape.

    :param error: The OAuth2 error code (e.g. "invalid_client").
    :param error_description: Optional human-readable detail from the token issuer.
    """

    error: str
    error_description: Optional[str] = None

    def __str__(self) -> str:
        if self.error_description:
            return f"{self.error}: {self.error_description}"
        return self.error

    def describe(self) -> str:
        """
        Returns a user-friendly message for the error. For `invalid_client`, it
        replaces the issuer's report, which the token request logs as a warning.
        """
        if self.error == "invalid_client":
            return "Authentication failed. Check the client ID and secret, and the API base URL."
        return str(self)


@dataclass
class TableAccessNotGrantedError(Exception):
    """
    Raised when the token issuer's granted `authorization_details` does not
    contain the table access that was requested. Guards against silently
    trusting a token whose actual grant doesn't match what was asked for.

    :param requested: The requested table access, as `namespace/table`.
    """

    requested: str

    def __str__(self) -> str:
        return f"Requested access to '{self.requested}' was not granted by the token issuer."


class AuthorizationFailedError(OperationError):
    """
    Raised when the client fails to obtain the necessary authorization.
    """

    type: Literal["AuthorizationFailed"]


class AccountNotOnboardedError(OperationError):
    """
    Raised when the client is not onboarded.
    """

    type: Literal["AccountNotOnboarded"]


class AccountDisabledError(OperationError):
    """
    Raised when the client is onboarded but access is forbidden.
    """

    type: Literal["AccountDisabled"]


class AccountUnderMaintenanceError(OperationError):
    """
    Raised when account disabled because of maintenance
    """

    type: Literal["AccountUnderMaintenance"]


class RequestTypeForbiddenError(OperationError):
    """
    Raised when a request type (e.g. snapshot or incremental) is forbidden.
    """

    type: Literal["RequestTypeForbidden"]


@dataclass(frozen=True)
class Location:
    """
    Refers to a location in parsable text input (e.g. JSON, YAML or structured text).

    :param line: Line number (1-based).
    :param column: Column number w.r.t. the beginning of the line (1-based).
    :param character: Character number w.r.t. the beginning of the input (1-based).
    """

    line: int
    column: int
    character: int


@json_schema_type
@dataclass
class ValidationError(OperationError):
    """
    Raised when a JSON validation error occurs.

    :param location: Location of where invalid input was found.
    """

    location: Location


@json_schema_type
@dataclass
class NotFoundError(OperationError):
    """
    Raised when an entity does not exist or has expired.

    :param id: The identifier of the entity not found, e.g. the name of a table or the UUID of a job.
    :param kind: The entity that is not found such as a namespace, table, object or job.
    """

    id: str
    kind: str


@json_schema_type
@dataclass
class OutOfRangeError(OperationError):
    """
    Raised when data is queried outside of the allowed time range.

    :param since: The earliest permitted timestamp.
    :param until: The latest permitted timestamp.
    """

    since: datetime
    until: Optional[datetime]


@json_schema_type
@dataclass
class SnapshotRequiredError(OperationError):
    """
    Raised when data is queried outside of the allowed time range, and the table was reloaded recently.
    A new snapshot is required to keep data consistency.

    :param since: The earliest permitted timestamp.
    :param until: The latest permitted timestamp.
    """

    since: datetime
    until: Optional[datetime]


@json_schema_type
@dataclass
class ProcessingError(OperationError):
    """
    Raised when a job has terminated due to an unexpected error.
    """


@json_schema_type
@dataclass
class GatewayTimeoutError(Exception):
    """
    Raised when received timeout from gateway.

    :param message: Always the same message signaling that a timeout received.
    """

    message: str
