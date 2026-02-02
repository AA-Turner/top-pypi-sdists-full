"""
Error handling for Kodexa Go bindings - minimal wrapper.
"""

from ._native import lib, ffi


# Error codes from Go
ERR_NONE = 0
ERR_INVALID_INPUT = 1
ERR_NOT_FOUND = 2
ERR_DATABASE = 3
ERR_VALIDATION = 4
ERR_UNAUTHORIZED = 5
ERR_INTERNAL = 100


class DocumentError(Exception):
    """Base exception for document operations."""
    pass


# Alias for backwards compatibility and clarity
KodexaError = DocumentError


class DocumentNotFoundError(DocumentError):
    """Document or file not found."""
    pass


class InvalidDocumentError(DocumentError):
    """Invalid document format or data."""
    pass


class ExtractionError(DocumentError):
    """Raised when extraction engine fails."""
    pass


class MemoryError(DocumentError):
    """Raised when memory management fails."""
    pass


def check_error():
    """Check for errors from the last C call and raise if needed."""
    error_code = lib.KodexaGetLastError()
    if error_code == ERR_NONE:
        return
    
    # Get error message
    msg_ptr = lib.KodexaGetLastErrorMessage()
    if msg_ptr != ffi.NULL:
        try:
            error_msg = ffi.string(msg_ptr).decode('utf-8')
        finally:
            lib.FreeString(msg_ptr)
    else:
        error_msg = f"Unknown error (code {error_code})"
    
    # Clear the error state
    lib.ClearError()
    
    # Raise appropriate exception
    if error_code == ERR_NOT_FOUND:
        raise DocumentNotFoundError(error_msg)
    elif error_code == ERR_INVALID_INPUT or error_code == ERR_VALIDATION:
        raise InvalidDocumentError(error_msg)
    else:
        raise DocumentError(error_msg)


def clear_error():
    """Clear any pending error state."""
    lib.ClearError()