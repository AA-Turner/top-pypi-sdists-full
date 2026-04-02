"""Wrapper class for lists in the deductive system."""

from __future__ import annotations

__all__ = [
    "List",
]

import typing
from . import ds
from .common import Common

if typing.TYPE_CHECKING:
    from .term_t import Term


class List(Common[ds.List]):
    """Wrapper class for lists in the deductive system.

    Lists contain ordered sequences of terms.

    Example:
        >>> lst = List("(a b c)")
        >>> print(len(lst))  # 3
        >>> print(lst[0])  # "a"
    """

    _base = ds.List

    def __len__(self) -> int:
        """Get the number of elements in the list.

        Returns:
            The list length.
        """
        return len(self.value)

    def __getitem__(self, index: int) -> Term:
        """Get an element from the list by index.

        Args:
            index: The zero-based index of the element.

        Returns:
            The term at the specified index.
        """
        from .term_t import Term

        return Term(self.value[index])
