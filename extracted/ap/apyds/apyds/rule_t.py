"""Wrapper class for logical rules in the deductive system."""

from __future__ import annotations

__all__ = [
    "Rule",
]

from . import ds
from .common import Common
from .term_t import Term
from .buffer_size import buffer_size


class Rule(Common[ds.Rule]):
    """Wrapper class for logical rules in the deductive system.

    A rule consists of zero or more premises (above the line) and a conclusion (below the line).

    Example:
        >>> rule = Rule("(father `X `Y)\\n----------\\n(parent `X `Y)\\n")
        >>> print(rule.conclusion)  # "(parent `X `Y)"
        >>> print(len(rule))  # 1 (number of premises)
    """

    _base = ds.Rule

    def __len__(self) -> int:
        """Get the number of premises in the rule.

        Returns:
            The number of premises.
        """
        return len(self.value)

    def __getitem__(self, index: int) -> Term:
        """Get a premise term by index.

        Args:
            index: The zero-based index of the premise.

        Returns:
            The premise term at the specified index.
        """
        return Term(self.value[index])

    @property
    def conclusion(self) -> Term:
        """Get the conclusion of the rule.

        Returns:
            The conclusion term.
        """
        return Term(self.value.conclusion())

    def __floordiv__(self, other: Rule) -> Rule | None:
        return self.ground(other)

    def ground(self, other: Rule, scope: str | None = None) -> Rule | None:
        """Ground this rule using a dictionary to substitute variables with values.

        Args:
            other: A rule representing a dictionary (list of pairs). Each pair contains
                   a variable and its substitution value.
                   Example: Rule("((`a b))") means substitute variable `a with value b.
            scope: Optional scope string for variable scoping.

        Returns:
            The grounded rule, or None if grounding fails.

        Example:
            >>> a = Rule("`a")
            >>> b = Rule("((`a b))")
            >>> str(a.ground(b))
            '----\\nb\\n'
            >>>
            >>> # With scope
            >>> c = Rule("`a")
            >>> d = Rule("((x y `a `b) (y x `b `c))")
            >>> str(c.ground(d, "x"))
            '----\\n`c\\n'
        """
        capacity = buffer_size()
        rule = ds.Rule.ground(self.value, other.value, scope, capacity)
        if rule is None:
            return None
        return Rule(rule, capacity)

    def __matmul__(self, other: Rule) -> Rule | None:
        """Match this rule with another rule using unification.

        This is the operator form of the match method, using the @ operator.
        This unifies the first premise of this rule with the other rule.
        The other rule must be a fact (a rule without premises).

        Args:
            other: The rule to match against (must be a fact without premises).

        Returns:
            The matched rule, or None if matching fails.

        Example:
            >>> mp = Rule("(`p -> `q)\\n`p\\n`q\\n")
            >>> pq = Rule("((! (! `x)) -> `x)")
            >>> str(mp @ pq)
            '(! (! `x))\\n----------\\n`x\\n'
        """
        capacity = buffer_size()
        rule = ds.Rule.match(self.value, other.value, capacity)
        if rule is None:
            return None
        return Rule(rule, capacity)

    def rename(self, prefix_and_suffix: Rule) -> Rule | None:
        """Rename all variables in this rule by adding prefix and suffix.

        Args:
            prefix_and_suffix: A rule with only a conclusion that is a list with two inner lists.
                Each inner list contains 0 or 1 item representing the prefix and suffix.
                Example: Rule("((pre_) (_suf))") adds "pre_" as prefix and "_suf" as suffix.

        Returns:
            The renamed rule, or None if renaming fails.

        Example:
            >>> a = Rule("`x")
            >>> b = Rule("((pre_) (_suf))")
            >>> str(a.rename(b))
            '----\\n`pre_x_suf\\n'
            >>>
            >>> # With empty prefix (only suffix)
            >>> c = Rule("`x")
            >>> d = Rule("(() (_suf))")
            >>> str(c.rename(d))
            '----\\n`x_suf\\n'
        """
        capacity = buffer_size()
        rule = ds.Rule.rename(self.value, prefix_and_suffix.value, capacity)
        if rule is None:
            return None
        return Rule(rule, capacity)

    def __repr__(self) -> str:
        return f"Rule[\n{self}]"
