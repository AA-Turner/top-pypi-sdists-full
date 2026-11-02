"""Mapping SDK failures to CLI errors without secrets."""

from __future__ import annotations

from typing import NoReturn

from labqoat.cli.exit_codes import ExitCodes
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.errors.api_error import ApiError
from labqoat.errors.authentication_error import AuthenticationError
from labqoat.errors.transport_error import TransportError
from labqoat.errors.run_failed_error import RunFailedError
import click


class ErrorReporter:
    """Convert exceptions into Click errors on stderr."""

    @staticmethod
    def report(error: Exception) -> NoReturn:
        """Raise the Click error matching an SDK failure."""
        if isinstance(error, (click.ClickException, click.exceptions.Exit, click.Abort)):
            raise error
        if isinstance(error, AuthenticationError):
            raise CliFailure(
                f"{error.message} Run 'labqoat auth login' or set LABQOAT_USERNAME/LABQOAT_PASSWORD.",
                ExitCodes.AUTH_FAILURE,
                error.problem,
            )
        if isinstance(error, TransportError):
            code = ExitCodes.DEADLINE_EXCEEDED if error.timed_out else ExitCodes.TRANSPORT_FAILURE
            ErrorReporter.raise_click(error.message, code)
        if isinstance(error, ApiError):
            resource = error.run.id if isinstance(error, RunFailedError) else None
            raise CliFailure(ErrorReporter.describe_api_error(error), ExitCodes.DOMAIN_FAILURE, error.problem, resource)
        if isinstance(error, (OSError, TypeError, ValueError)):
            ErrorReporter.raise_click(str(error), ExitCodes.DOMAIN_FAILURE)
        raise CliFailure(str(error), ExitCodes.DOMAIN_FAILURE) from error

    @staticmethod
    def describe_api_error(error: ApiError) -> str:
        """Describe an API error with its status when known."""
        if error.status is not None:
            context = ErrorReporter.response_context(error)
            return f"API error {error.status}: {error.message}{ErrorReporter.field_errors(error)}{context}"
        return f"API error: {error.message}"

    @staticmethod
    def field_errors(error: ApiError) -> str:
        """Name the fields a validation problem rejected, so the request can be fixed without guessing."""
        entries = error.problem.get("errors") if error.problem is not None else None
        if not isinstance(entries, list) or error.problem is None:
            return ""
        detail = error.problem.get("detail")
        named = [
            f"{entry.get('field')}: {entry.get('detail') or entry.get('code')}"
            for entry in entries[:5]
            if isinstance(entry, dict) and entry.get("field") and entry.get("detail") != detail
        ]
        return f" [{'; '.join(named)}]" if named else ""

    @staticmethod
    def response_context(error: ApiError) -> str:
        """Append retry and request identifiers when the server provided them."""
        parts = []
        if error.request_id:
            parts.append(f"request_id={error.request_id}")
        if error.retry_after:
            parts.append(f"retry_after={error.retry_after}")
        return f" ({', '.join(parts)})" if parts else ""

    @staticmethod
    def raise_click(message: str, exit_code: int) -> NoReturn:
        """Raise a Click failure with the stable process exit code."""
        raise CliFailure(message, exit_code)

    @staticmethod
    def report_generic(message: str) -> NoReturn:
        """Report a generic failure without secrets."""
        ErrorReporter.raise_click(message, ExitCodes.DOMAIN_FAILURE)

    @staticmethod
    def report_usage(message: str) -> NoReturn:
        """Reject local schema/input errors before a request with the standard usage status."""
        raise CliFailure(message, ExitCodes.USAGE_ERROR)
