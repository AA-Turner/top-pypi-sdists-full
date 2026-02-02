"""Errors specific to working with corvic models."""

from corvic.result import Error


class InvalidOnAnonymousError(Error):
    """InvalidOnAnonymousError result Error.

    Raised when an operation cannot be done on an unregistered object.
    """
