"""Wrapper class for items in the deductive system."""

__all__ = [
    "Item",
]

from . import ds
from .common import Common
from .string_t import String


class Item(Common[ds.Item]):
    """Wrapper class for items in the deductive system.

    Items represent constants or functors in logical terms.

    Example:
        >>> item = Item("atom")
        >>> print(item.name)  # "atom"
    """

    _base = ds.Item

    @property
    def name(self) -> String:
        """Get the name of this item.

        Returns:
            The item name as a String.
        """
        return String(self.value.name())
