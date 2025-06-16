"""This module implements exceptions for this package."""

__all__ = ["Error", "BackupAlreadyExistError"]


class Error(Exception):
    """
    Base class for exceptions in this module.
    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class BackupAlreadyExistError(Error):
    """File or directory already exists on backup path when vacate existing file on target path."""
