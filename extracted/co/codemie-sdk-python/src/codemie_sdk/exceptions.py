"""Custom exceptions for the CodeMie SDK."""


class CodeMieError(Exception):
    """Base exception for all CodeMie SDK errors."""

    pass


class ApiError(CodeMieError):
    """Exception raised for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: dict | None = None,
    ):
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
            response: Raw API response if available
        """
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class NotFoundError(ApiError):
    """Exception raised when a resource is not found."""

    def __init__(self, resource_type: str, resource_id: str):
        """Initialize not found error.

        Args:
            resource_type: Type of resource that was not found (e.g., "Integration")
            resource_id: ID or identifier of the resource
        """
        super().__init__(
            message=f"{resource_type} with {resource_id} not found", status_code=404
        )
