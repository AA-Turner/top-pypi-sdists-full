"""Contains shared errors types that can be raised from API functions"""


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(f"Unexpected status code: {status_code}")


class DeprecatedEndpointError(Exception):
    """Raised when calling an endpoint that has been permanently removed.

    This error indicates that the endpoint has been removed and will not be implemented
    in the new API. The functionality may have been replaced by a different approach.
    """

    def __init__(self, endpoint_name: str, message: str = None):
        self.endpoint_name = endpoint_name
        self.message = (
            message or f"Endpoint '{endpoint_name}' has been permanently removed."
        )
        super().__init__(self.message)


class V1MigrationPendingError(Exception):
    """Raised when calling an endpoint that is not yet available in the FastAPI v1 API.

    This error indicates that the endpoint migration is pending and will be implemented
    in a future release. Check the error message for the expected v1 endpoint path.
    """

    def __init__(
        self, endpoint_name: str, v1_endpoint: str = None, message: str = None
    ):
        self.endpoint_name = endpoint_name
        self.v1_endpoint = v1_endpoint
        if message:
            self.message = message
        elif v1_endpoint:
            self.message = f"Endpoint '{endpoint_name}' migration pending. Will be available at '{v1_endpoint}'."
        else:
            self.message = f"Endpoint '{endpoint_name}' migration to v1 API is pending."
        super().__init__(self.message)


__all__ = ["UnexpectedStatus", "DeprecatedEndpointError", "V1MigrationPendingError"]
