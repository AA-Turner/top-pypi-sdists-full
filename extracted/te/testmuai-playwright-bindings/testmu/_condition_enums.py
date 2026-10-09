"""Condition operators. Identical in every mode, so shared:
``testmu.PossibleCondition`` / ``ConcatenationOperator`` are these enums, and
each mode's ``_helpers.condition`` re-exports them.
"""
from __future__ import annotations

import enum


class PossibleCondition(enum.Enum):
    """Comparison operators supported in conditions."""

    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUALS = ">="
    LESS_THAN_OR_EQUALS = "<="
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"

    # No _missing_ fallback: an unrecognized operator must raise ValueError
    # rather than silently defaulting to EQUALS and producing a wrong verdict.

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PossibleCondition):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class ConcatenationOperator(enum.Enum):
    """Logical connectors between conditions."""

    AND = "AND"
    OR = "OR"
