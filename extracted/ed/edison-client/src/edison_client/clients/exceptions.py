"""Exception classes for edison-client data storage operations."""


class RestClientError(Exception):
    """Base exception for REST client errors."""


class DataStorageError(RestClientError):
    """Base exception for data storage operations."""


class DataStorageCreationError(DataStorageError):
    """Raised when there's an error creating a data storage entry."""


class DataStorageRetrievalError(DataStorageError):
    """Raised when there's an error retrieving a data storage entry."""


class DataStorageValidationError(DataStorageError, ValueError):
    """Invalid storage input; ValueError ancestry preserves Pydantic validation."""


class DataStorageNotFoundError(DataStorageRetrievalError):
    """The requested entry or revision could not be found."""


class DataStoragePermissionError(DataStorageError):
    """The caller does not have permission for the storage operation."""


class DataStorageConflictError(DataStorageError):
    """The update conflicts with the entry's current state."""
