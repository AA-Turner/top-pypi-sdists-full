"""Buffer size management for the deductive system."""

__all__ = [
    "buffer_size",
    "scoped_buffer_size",
]

from contextlib import contextmanager

_buffer_size = 1024


def buffer_size(size: int = 0) -> int:
    """Gets the current buffer size, or sets a new buffer size and returns the previous value.

    The buffer size is used for internal operations like conversions and transformations.

    Args:
        size: The new buffer size to set. If 0 (default), the current size is returned without modification.

    Returns:
        The previous buffer size value.

    Example:
        >>> current_size = buffer_size()  # Get current size
        >>> old_size = buffer_size(2048)  # Set new size, returns old size
    """
    global _buffer_size
    old_buffer_size = _buffer_size
    if size > 0:
        _buffer_size = size
    return old_buffer_size


@contextmanager
def scoped_buffer_size(size: int = 0):
    """Context manager for temporarily changing the buffer size.

    Sets the buffer size for the duration of the context and restores the
    previous value when exiting.

    Args:
        size: The temporary buffer size to set.

    Example:
        >>> with scoped_buffer_size(4096):
        ...     # Operations here use buffer size of 4096
        ...     pass
        >>> # Buffer size is restored to previous value
    """
    old_buffer_size = buffer_size(size)
    try:
        yield
    finally:
        buffer_size(old_buffer_size)
