"""Search engine for the deductive system."""

__all__ = [
    "Search",
]

import typing
from . import ds
from .rule_t import Rule


class Search:
    """Search engine for the deductive system.

    Manages a knowledge base of rules and performs logical inference.

    Example:
        >>> search = Search()
        >>> search.add("(parent john mary)")
        >>> search.add("(father `X `Y)\\n----------\\n(parent `X `Y)\\n")
        >>> def callback(rule):
        ...     print(rule)
        ...     return False  # Return False to continue, True to stop
        >>> search.execute(callback)
    """

    def __init__(self, limit_size: int = 1000, buffer_size: int = 10000):
        """Creates a new search engine instance.

        Args:
            limit_size: Size of the buffer for storing the final objects (rules/facts)
                       in the knowledge base (default: 1000).
            buffer_size: Size of the buffer for internal operations like conversions
                        and transformations (default: 10000).
        """
        self._search: ds.Search = ds.Search(limit_size, buffer_size)

    def set_limit_size(self, limit_size: int) -> None:
        """Set the size of the buffer for storing final objects.

        Args:
            limit_size: The new limit size for storing rules/facts.
        """
        self._search.set_limit_size(limit_size)

    def set_buffer_size(self, buffer_size: int) -> None:
        """Set the buffer size for internal operations.

        Args:
            buffer_size: The new buffer size.
        """
        self._search.set_buffer_size(buffer_size)

    def reset(self) -> None:
        """Reset the search engine, clearing all rules and facts."""
        self._search.reset()

    def add(self, text: str) -> bool:
        """Add a rule or fact to the knowledge base.

        Args:
            text: The rule or fact as a string.

        Returns:
            True if successfully added, False otherwise.
        """
        return self._search.add(text)

    def execute(self, callback: typing.Callable[[Rule], bool]) -> int:
        """Execute the search engine with a callback for each inferred rule.

        Args:
            callback: Function called for each candidate rule. Return False to continue,
                     True to stop.

        Returns:
            The number of rules processed.
        """
        return self._search.execute(lambda candidate: callback(Rule(candidate.clone())))
