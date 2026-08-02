class BaseError(Exception):
    """Base class for exceptions in this module."""

    pass


class ConnectionError(BaseError):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = f"Connection Error: {message}"
        super().__init__(self.message)
