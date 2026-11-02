# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ....._types import SequenceNotStr

__all__ = ["CompareSearchParams"]


class CompareSearchParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    compare_to: Required[SequenceNotStr[str]]
    """EvaluationVersion IDs to compare with the reference, in result order."""

    cursor: str
    """The previous response's next_cursor value. Omit for the first page."""

    filter: str
    """Selects rows using column comparisons joined with AND, OR, and NOT.

    Parentheses group expressions. NOT and - bind tighter than AND and OR, and
    mixing AND and OR at one level needs parentheses. Parentheses nest at most 32
    deep.

    For string comparisons with = or !=, use these patterns:

        *    matches zero or more characters

    - matches a literal asterisk \\ matches a literal backslash

    A filter can contain at most 100 predicates and 65,536 bytes of normalized JSON
    literals in total.

    Example for an evaluation with an accuracy score column:

        variant = "model-a" AND s.accuracy >= 0.8
    """

    limit: int
    """Maximum number of results to return in one page."""

    order_by: str
    """Column to sort by, optionally followed by desc for descending order.

    Without desc, sorting is ascending. Omit to use the operation's standard order.
    """
