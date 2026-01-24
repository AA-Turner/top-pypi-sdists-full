"""Wrapper class for deductive system strings."""

__all__ = [
    "String",
]

from . import ds
from .common import Common


class String(Common[ds.String]):
    """Wrapper class for deductive system strings.

    Supports initialization from strings, buffers, or other instances.

    Example:
        >>> str1 = String("hello")
        >>> str2 = String(str1.data())  # From binary
        >>> print(str1)  # "hello"
    """

    _base = ds.String
