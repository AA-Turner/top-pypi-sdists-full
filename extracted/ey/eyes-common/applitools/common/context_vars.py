"""Context variable management for marshmallow schema serialization.

This module provides thread-safe context variable management to replace
the deprecated 'context' parameter in marshmallow 3+.
"""

from __future__ import absolute_import, division, print_function

import contextvars
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Generator, Optional

    from .object_registry import ObjectRegistry


# Global context variable for object registry
_object_registry_context = contextvars.ContextVar(
    "object_registry", default=None
)  # type: contextvars.ContextVar[Optional[ObjectRegistry]]


def get_object_registry():
    # type: () -> ObjectRegistry
    """Get the current object registry from context.

    Returns:
        ObjectRegistry: The current object registry instance.

    Raises:
        RuntimeError: If no object registry is set in the current context.
    """
    registry = _object_registry_context.get()
    if registry is None:
        raise RuntimeError(
            "No object registry found in context. "
            "Ensure you're calling this within a set_object_registry() context manager."
        )
    return registry


@contextmanager
def set_object_registry(registry):
    # type: (ObjectRegistry) -> Generator[ObjectRegistry, None, None]
    """Context manager to set the object registry for the current context.

    Args:
        registry: The ObjectRegistry instance to set in the context.

    Yields:
        ObjectRegistry: The registry instance that was set.

    Example:
        with set_object_registry(my_registry) as registry:
            # Now schema fields can access the registry via get_object_registry()
            result = some_schema.dump(data)
    """
    token = _object_registry_context.set(registry)
    try:
        yield registry
    finally:
        _object_registry_context.reset(token)


def has_object_registry():
    # type: () -> bool
    """Check if an object registry is currently set in the context.

    Returns:
        bool: True if an object registry is available, False otherwise.
    """
    return _object_registry_context.get() is not None
