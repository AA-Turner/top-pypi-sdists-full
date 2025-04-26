from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional

from strong_typing.schema import json_schema_type


@json_schema_type
@dataclass
class ServerError(Exception):
    """
    An error returned by the server.

    :param body: Unspecified content returned by the server.
    """

    body: Any


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
