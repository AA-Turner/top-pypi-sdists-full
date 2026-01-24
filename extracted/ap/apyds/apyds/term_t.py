"""Wrapper class for logical terms in the deductive system."""

from __future__ import annotations

__all__ = [
    "Term",
]

from . import ds
from .common import Common
from .variable_t import Variable
from .item_t import Item
from .list_t import List
from .buffer_size import buffer_size


class Term(Common[ds.Term]):
    """Wrapper class for logical terms in the deductive system.

    A term can be a variable, item, or list.

    Example:
        >>> term = Term("(f `x a)")
        >>> inner_term = term.term  # Get the underlying term type
    """

    _base = ds.Term

    @property
    def term(self) -> Variable | Item | List:
        """Extracts the underlying term and returns it as its concrete type.

        Returns:
            The term as a Variable, Item, or List.

        Raises:
            TypeError: If the term type is unexpected.
        """
        match self.value.get_type():
            case ds.Term.Type.Variable:
                return Variable(self.value.variable())
            case ds.Term.Type.Item:
                return Item(self.value.item())
            case ds.Term.Type.List:
                return List(self.value.list())
            case _:
                raise TypeError("Unexpected term type.")

    def __floordiv__(self, other: Term) -> Term | None:
        return self.ground(other)

    def ground(self, other: Term, scope: str | None = None) -> Term | None:
        """Ground this term using a dictionary to substitute variables with values.

        Args:
            other: A term representing a dictionary (list of pairs). Each pair contains
                   a variable and its substitution value.
                   Example: Term("((`a b))") means substitute variable `a with value b.
            scope: Optional scope string for variable scoping.

        Returns:
            The grounded term, or None if grounding fails.

        Example:
            >>> a = Term("`a")
            >>> b = Term("((`a b))")
            >>> str(a.ground(b))  # "b"
            >>>
            >>> # With scope
            >>> c = Term("`a")
            >>> d = Term("((x y `a `b) (y x `b `c))")
            >>> str(c.ground(d, "x"))  # "`c"
        """
        capacity = buffer_size()
        term = ds.Term.ground(self.value, other.value, scope, capacity)
        if term is None:
            return None
        return Term(term, capacity)

    def __matmul__(self, other: Term) -> Term | None:
        """Match two terms and return the unification result as a dictionary.

        Args:
            other: The term to match with this term.

        Returns:
            A term representing the unification dictionary (list of tuples), or None if matching fails.

        Example:
            >>> a = Term("`a")
            >>> b = Term("b")
            >>> result = a @ b
            >>> str(result) if result else None  # "((1 2 `a b))"
        """
        capacity = buffer_size()
        term = ds.Term.match(self.value, other.value, "1", "2", capacity)
        if term is None:
            return None
        return Term(term, capacity)

    def rename(self, prefix_and_suffix: Term) -> Term | None:
        """Rename all variables in this term by adding prefix and suffix.

        Args:
            prefix_and_suffix: A term representing a list with two inner lists.
                Each inner list contains 0 or 1 item representing the prefix and suffix.
                Example: Term("((pre_) (_suf))") adds "pre_" as prefix and "_suf" as suffix.

        Returns:
            The renamed term, or None if renaming fails.

        Example:
            >>> a = Term("`x")
            >>> b = Term("((pre_) (_suf))")
            >>> str(a.rename(b))  # "`pre_x_suf"
            >>>
            >>> # With empty prefix (only suffix)
            >>> c = Term("`x")
            >>> d = Term("(() (_suf))")
            >>> str(c.rename(d))  # "`x_suf"
        """
        capacity = buffer_size()
        term = ds.Term.rename(self.value, prefix_and_suffix.value, capacity)
        if term is None:
            return None
        return Term(term, capacity)
