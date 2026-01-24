"""
Errors and exceptions for the authentication module
"""


class AuthError(Exception):
    """Base exception for authentication errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ConfigurationError(AuthError):
    """Exception for configuration-related errors"""
    def __init__(self, message: str):
        super().__init__(message)


class TokenError(Exception):
    """Exception for token-related errors"""
    def __init__(self, message: str, cause=None):
        self.message = message
        self.cause = cause
        super().__init__(message)


class AuthenticationError(AuthError):
    """Exception for authentication failures"""
    def __init__(self, message: str):
        super().__init__(message)


class NetworkError(AuthError):
    """Exception for network-related errors"""
    def __init__(self, message: str):
        super().__init__(message) 