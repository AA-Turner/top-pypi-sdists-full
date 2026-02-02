"""Errors specific to communicating with the database."""

from corvic import result


class InvalidORMIdentifierError(result.Error):
    """Raised when an identifier can't be translated to its orm equivalent."""


class RequestedObjectsForNobodyError(result.Error):
    """Raised when attempts are made to access database objects as the nobody org."""


class DeletedObjectError(result.Error):
    """DeletedObjectError result Error.

    Raised on invalid operations to objects which are soft deleted.
    """
