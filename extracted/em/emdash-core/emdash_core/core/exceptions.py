"""Custom exceptions for EmDash."""


class EmDashException(Exception):
    """Base exception for all EmDash errors."""
    pass


class ConfigurationError(EmDashException):
    """Raised when configuration is invalid or missing."""
    pass


class DatabaseConnectionError(EmDashException):
    """Raised when database connection fails."""
    pass


class RepositoryError(EmDashException):
    """Raised when repository operations fail."""
    pass


class ParsingError(EmDashException):
    """Raised when code parsing fails."""
    pass


class GraphBuildError(EmDashException):
    """Raised when graph construction fails."""
    pass


class QueryError(EmDashException):
    """Raised when graph queries fail."""
    pass


class AnalyticsError(EmDashException):
    """Raised when analytics computation fails."""
    pass


class ContextLengthError(EmDashException):
    """Raised when context length exceeds model's limit."""

    def __init__(
        self,
        message: str,
        tokens_requested: int = 0,
        tokens_limit: int = 0,
    ):
        super().__init__(message)
        self.tokens_requested = tokens_requested
        self.tokens_limit = tokens_limit
