"""Chain engine for the deductive system."""

__all__ = [
    "Chain",
]

import typing
from . import ds
from .rule_t import Rule


class Chain:
    """Chain engine for the deductive system.

    Similar to Search, but matches all premises of a rule in a single cycle.

    Example:
        >>> chain = Chain()
        >>> chain.add("p q r")
        >>> chain.add("p")
        >>> chain.add("q")
        >>> def callback(rule):
        ...     print(rule)
        ...     return False  # Return False to continue, True to stop
        >>> chain.execute(callback)  # Will find r in a single cycle
    """

    def __init__(self, limit_size: int = 1000, buffer_size: int = 10000):
        """Creates a new chain engine instance.

        Args:
            limit_size: Size of the buffer for storing the final objects (rules/facts)
                       in the knowledge base (default: 1000).
            buffer_size: Size of the buffer for internal operations like conversions
                        and transformations (default: 10000).
        """
        self._chain: ds.Chain = ds.Chain(limit_size, buffer_size)

    def set_limit_size(self, limit_size: int) -> None:
        """Set the size of the buffer for storing final objects.

        Args:
            limit_size: The new limit size for storing rules/facts.
        """
        self._chain.set_limit_size(limit_size)

    def set_buffer_size(self, buffer_size: int) -> None:
        """Set the buffer size for internal operations.

        Args:
            buffer_size: The new buffer size.
        """
        self._chain.set_buffer_size(buffer_size)

    def reset(self) -> None:
        """Reset the chain engine, clearing all rules and facts."""
        self._chain.reset()

    def add(self, text: str) -> bool:
        """Add a rule or fact to the knowledge base.

        Args:
            text: The rule or fact as a string.

        Returns:
            True if successfully added, False otherwise.
        """
        return self._chain.add(text)

    def execute(self, callback: typing.Callable[[Rule], bool]) -> int:
        """Execute the chain engine with a callback for each inferred rule.

        Args:
            callback: Function called for each candidate rule. Return False to continue,
                     True to stop.

        Returns:
            The number of rules processed.
        """
        return self._chain.execute(lambda candidate: callback(Rule(candidate.clone())))

    def __iter__(self) -> typing.Iterator[Rule]:
        """Iterate over inferred rules.

        Returns:
            An iterator over Rule objects.

        Example:
            >>> for rule in chain:
            ...     print(rule)
        """
        iterator = self._chain.iter()
        while True:
            candidate = iterator.next()
            if candidate is None:
                break
            yield Rule(candidate.clone())
