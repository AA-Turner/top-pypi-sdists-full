"""
Custom exceptions for the V1MemoryClient.
"""


class MemoryException(Exception):
    """Base exception class for all memory errors."""

    pass


class NamespaceNotFoundException(MemoryException):
    """Raised when a namespace is not found."""

    pass


class NamespaceAlreadyExistsException(MemoryException):
    """Raised when a namespace already exists."""


class RunNotFoundException(MemoryException):
    """Raised when a run does not exist."""


class RunAlreadyExistsException(MemoryException):
    """Raised when a run already exists."""


class APIRequestException(MemoryException):
    """Raised when an API request fails."""

    pass
