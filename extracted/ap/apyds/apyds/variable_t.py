"""Wrapper class for logical variables in the deductive system."""

__all__ = [
    "Variable",
]

from . import ds
from .common import Common
from .string_t import String


class Variable(Common[ds.Variable]):
    """Wrapper class for logical variables in the deductive system.

    Variables are used in logical terms and can be unified.

    Example:
        >>> var1 = Variable("`X")
        >>> print(var1.name)  # "X"
    """

    _base = ds.Variable

    @property
    def name(self) -> String:
        """Get the name of this variable.

        Returns:
            The variable name as a String.
        """
        return String(self.value.name())
