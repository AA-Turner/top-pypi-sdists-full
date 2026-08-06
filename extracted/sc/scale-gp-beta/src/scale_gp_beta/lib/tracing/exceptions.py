from scale_gp_beta._exceptions import SGPClientError

from .types import ErrorCategory


class CategorizedError(Exception):
    """Base class for failures with known operational ownership.

    Use ``ApplicationError`` for failures owned by caller code, including
    business logic, user input, tools, and application configuration. Use
    ``PlatformError`` only at a known SGP-owned boundary, such as managed
    runtime, tracing, persistence, or platform networking. Ordinary exceptions
    intentionally remain ``unknown``.
    """

    error_category: ErrorCategory = "unknown"


class ApplicationError(CategorizedError):
    """Failure owned by the calling application."""

    error_category: ErrorCategory = "application"


class PlatformError(CategorizedError):
    """Failure owned by SGP or a platform-managed dependency."""

    error_category: ErrorCategory = "platform"


class ParamsCreationError(SGPClientError):
    pass
