"""
Custom exceptions.
"""


class CustomBaseException(Exception):
    """
    Base exception for all sub-exceptions.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class AuthenticationError(CustomBaseException):
    """
    Custom exception for authentication errors when interacting with the APIs.
    """

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message)


class ApiError(CustomBaseException):
    """
    Custom exception for non-authentication related API errors.
    """

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message)
