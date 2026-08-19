"""Typed CLI errors that carry an error code and an exit code.

Click reads ``exit_code`` from ``ClickException``, so the class alone decides
the exit code.
"""
from contextvars import ContextVar
from enum import Enum
import json
import os
import sys
from typing import Dict, IO, NoReturn, Optional, Type, TypedDict

import click
import urllib3
import yaml


class ErrorCode(str, Enum):
    """A documented error a command may raise."""

    RESOURCE_NOT_FOUND = "resource_not_found"
    NAME_CONFLICT = "name_conflict"
    AUTH_UNAUTHORIZED = "auth_unauthorized"
    AUTH_FORBIDDEN = "auth_forbidden"
    AUTH_TOKEN_EXPIRED = "auth_token_expired"
    OPERATION_TIMEOUT = "operation_timeout"
    WORKLOAD_FAILED = "workload_failed"
    INSUFFICIENT_CAPACITY = "insufficient_capacity"
    CONNECTION_ERROR = "connection_error"
    RATE_LIMITED = "rate_limited"
    MISSING_CONFIG = "missing_config"
    INVALID_CONFIG = "invalid_config"


class ExitCode:
    """Process exit codes the CLI returns.

    ``USER_ERROR`` is the default for any error without a more exact code.
    """

    USER_ERROR = 1
    INFRA_ERROR = 2
    TIMEOUT = 3
    AUTH_ERROR = 4
    WORKLOAD_FAILED = 10


# A ContextVar, not a Click parameter: Click discards the context before it
# shows an error. ``AnyscaleCommand.invoke`` sets this.
_OUTPUT_FORMAT: ContextVar[str] = ContextVar("anyscale_error_output_format")

# These formats get an error envelope instead of a text line.
_STRUCTURED_FORMATS = frozenset({"json", "yaml"})

DEBUG_ENV_VAR = "ANYSCALE_DEBUG"

_DEBUG_HINT = f"Re-run with {DEBUG_ENV_VAR}=1 for the full traceback."

# Set this to "1" to get the exit codes of a CLI from before the typed errors.
# It is an escape hatch for automation that reads the old codes.
LEGACY_EXIT_CODES_ENV_VAR = "ANYSCALE_LEGACY_EXIT_CODES"


def set_error_output_format(output_format: Optional[str]) -> None:
    """Record the output format so an error can match it."""
    _OUTPUT_FORMAT.set((output_format or "text").lower())


def get_error_output_format() -> str:
    """Return the recorded output format. The default is ``text``."""
    return _OUTPUT_FORMAT.get("text")


def debug_enabled() -> bool:
    """Return True if the user asked for debug output."""
    return os.environ.get(DEBUG_ENV_VAR) == "1"


def legacy_exit_codes_enabled() -> bool:
    """Return True if the user asked for the exit codes of the older CLI."""
    return os.environ.get(LEGACY_EXIT_CODES_ENV_VAR) == "1"


class _ErrorDetails(TypedDict):
    code: Optional[str]
    message: str
    resolution: Optional[str]
    exit_code: int


class _ErrorEnvelope(TypedDict):
    """The machine-readable form of an error."""

    error: _ErrorDetails


class AnyscaleError(click.ClickException):
    """Base class for every error the CLI shows to a user."""

    error_code: Optional[ErrorCode] = None
    exit_code: int = ExitCode.USER_ERROR
    resolution: str = ""

    def __init__(self, message: str, legacy_exit_code: Optional[int] = None) -> None:
        """Build the error.

        ``legacy_exit_code`` is the code the CLI returned at this site before
        the typed errors. A site that printed an error and then returned 0
        passes 0. Every other site returned 1, which is the default below.
        """
        super().__init__(message)
        if legacy_exit_codes_enabled():
            # An instance attribute hides the class attribute that Click reads.
            self.exit_code = 1 if legacy_exit_code is None else legacy_exit_code

    def to_dict(self) -> _ErrorEnvelope:
        """Return the machine-readable form of this error."""
        return {
            "error": {
                "code": self.error_code.value if self.error_code else None,
                "message": self.format_message(),
                "resolution": self.resolution or None,
                "exit_code": self.exit_code,
            }
        }

    def show(self, file: Optional[IO] = None) -> None:
        """Print the error in the command's output format.

        The envelope goes to stderr. A failed command must leave stdout empty,
        because a caller parses stdout as one document.
        """
        output_format = get_error_output_format()
        set_error_output_format(None)
        if output_format not in _STRUCTURED_FORMATS:
            super().show(file)
            return

        payload = self.to_dict()
        if output_format == "yaml":
            rendered = yaml.dump(payload, sort_keys=False).rstrip("\n")
        else:
            rendered = json.dumps(payload, indent=4, allow_nan=False)
        click.echo(rendered, err=True)


class UserError(AnyscaleError):
    """Bad input, invalid config, or a missing resource."""

    exit_code = ExitCode.USER_ERROR


class ResourceNotFoundError(UserError):
    error_code = ErrorCode.RESOURCE_NOT_FOUND
    resolution = (
        "Verify the resource ID or name. Use the list command to find "
        "available resources."
    )


class NameConflictError(UserError):
    error_code = ErrorCode.NAME_CONFLICT
    resolution = "Use a different name or terminate/delete the existing resource."


class MissingConfigError(UserError):
    error_code = ErrorCode.MISSING_CONFIG
    resolution = "Use -f/--config to specify a YAML config file."


class InvalidConfigError(UserError):
    """A config file or an option value is not valid."""

    error_code = ErrorCode.INVALID_CONFIG
    resolution = "Check YAML syntax and field types against the expected schema."


class InfraError(AnyscaleError):
    """The cloud, the network, or the API is unavailable."""

    exit_code = ExitCode.INFRA_ERROR


class InsufficientCapacityError(InfraError):
    error_code = ErrorCode.INSUFFICIENT_CAPACITY
    resolution = "Try different instance types or a different cloud/region."


class ApiConnectionError(InfraError):
    """The CLI cannot reach the Anyscale API."""

    error_code = ErrorCode.CONNECTION_ERROR
    resolution = "Check your network and ANYSCALE_HOST."


class RateLimitedError(InfraError):
    error_code = ErrorCode.RATE_LIMITED
    resolution = "Wait and retry."


class OperationTimeoutError(AnyscaleError):
    """A wait deadline passed before the operation finished."""

    error_code = ErrorCode.OPERATION_TIMEOUT
    exit_code = ExitCode.TIMEOUT
    resolution = "Retry with a longer --timeout or check resource status."


class AuthError(AnyscaleError):
    """The token is not valid, or the account lacks permission."""

    exit_code = ExitCode.AUTH_ERROR


class AuthUnauthorizedError(AuthError):
    error_code = ErrorCode.AUTH_UNAUTHORIZED
    resolution = "Check your ANYSCALE_CLI_TOKEN or run 'anyscale login --token'."


class AuthForbiddenError(AuthError):
    error_code = ErrorCode.AUTH_FORBIDDEN
    resolution = (
        "Your account lacks permission for this operation. Check service "
        "account scopes."
    )


class AuthTokenExpiredError(AuthError):
    error_code = ErrorCode.AUTH_TOKEN_EXPIRED
    resolution = "Re-authenticate with 'anyscale login --token'."


class WorkloadFailedError(AnyscaleError):
    """A job or a service reached a FAILED state."""

    error_code = ErrorCode.WORKLOAD_FAILED
    exit_code = ExitCode.WORKLOAD_FAILED
    resolution = "Check logs with the logs command."


_STATUS_TO_CLASS: Dict[int, Type[AnyscaleError]] = {
    # Status 0 means the request never reached the server.
    0: ApiConnectionError,
    400: InvalidConfigError,
    401: AuthUnauthorizedError,
    403: AuthForbiddenError,
    404: ResourceNotFoundError,
    409: NameConflictError,
    422: InvalidConfigError,
    429: RateLimitedError,
}


def error_class_for_http_status(status: Optional[int]) -> Type[AnyscaleError]:
    """Return the error class for an HTTP status."""
    if status is None:
        return ApiConnectionError
    cls = _STATUS_TO_CLASS.get(status)
    if cls is not None:
        return cls
    # This also covers the client's own 599 read-timeout code.
    if status >= 500:
        return ApiConnectionError
    return AnyscaleError


def from_http_status(status: Optional[int], message: str) -> AnyscaleError:
    """Build the error that matches an HTTP status."""
    return error_class_for_http_status(status)(message)


def from_unexpected_exception(exc: BaseException) -> AnyscaleError:
    """Convert an exception that no command handled into an AnyscaleError."""
    if isinstance(exc, AnyscaleError):
        return exc

    # Import here to keep this module a leaf. Import from ``rest``, not from
    # ``exceptions``: anyscale/__init__.py puts ``client/`` on sys.path, so the
    # qualified ``exceptions`` path gives a class that rest.py never raises.
    from anyscale.client.openapi_client.rest import (  # noqa: PLC0415
        ApiException as InternalApiException,
    )
    from anyscale.sdk.anyscale_client.rest import (  # noqa: PLC0415
        ApiException as ExternalApiException,
    )

    if isinstance(exc, (InternalApiException, ExternalApiException)):
        return from_http_status(
            exc.status, f"API Exception ({exc.status})\nReason: {exc.reason}"
        )

    # TimeoutError must come before OSError, because it is a subclass.
    if isinstance(exc, TimeoutError):
        return OperationTimeoutError(str(exc) or "The operation timed out.")

    if isinstance(
        exc,
        (
            ValueError,
            TypeError,
            RuntimeError,
            FileNotFoundError,
            FileExistsError,
            IsADirectoryError,
            NotADirectoryError,
            PermissionError,
        ),
    ):
        return UserError(str(exc) or exc.__class__.__name__)

    if isinstance(exc, (OSError, urllib3.exceptions.HTTPError)):
        return ApiConnectionError(str(exc) or exc.__class__.__name__)

    detail = str(exc) or exc.__class__.__name__
    return AnyscaleError(f"An unexpected error occurred: {detail}\n{_DEBUG_HINT}")


def from_command_exception(
    exc: BaseException, prefix: str, legacy_exit_code: Optional[int] = None,
) -> AnyscaleError:
    """Return the typed error for an exception that a command caught.

    A command that calls the SDK receives the generated client's ApiException,
    not an AnyscaleError, because the SDK builds its clients with
    ``raise_structured_exception=True``. Map it here so that the HTTP status
    still decides the exit code.
    """
    if isinstance(exc, AnyscaleError):
        return type(exc)(f"{prefix}: {exc.format_message()}", legacy_exit_code)
    if debug_enabled():
        raise exc
    error = from_unexpected_exception(exc)
    return type(error)(f"{prefix}: {error.format_message()}", legacy_exit_code)


def handle_uncaught_exception(exc: BaseException) -> NoReturn:
    """Show an uncaught exception as a CLI error, then exit.

    ``ANYSCALE_DEBUG=1`` re-raises instead, so a developer keeps the traceback.
    """
    if debug_enabled():
        raise exc

    error = from_unexpected_exception(exc)
    error.show()
    sys.exit(error.exit_code)
