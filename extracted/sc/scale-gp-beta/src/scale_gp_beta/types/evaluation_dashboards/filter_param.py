# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FilterParam", "Condition"]


class Condition(TypedDict, total=False):
    """Single filter condition comparing a column to a value.

    Example:
        {"column": "score", "operator": ">", "value": 0.5}
        {"column": "category", "operator": "=", "value": "test"}
    """

    column: Required[str]
    """Column name to filter on"""

    operator: Required[
        Literal["=", "!=", ">", "<", ">=", "<=", "IN", "NOT IN", "LIKE", "NOT LIKE", "IS NULL", "IS NOT NULL"]
    ]
    """Comparison operator"""

    source: str
    """Column source: 'data' or 'task_result_cache'"""

    value: Union[str, float, bool, Iterable[object]]
    """Value to compare against. Not required for IS NULL / IS NOT NULL operators."""


class FilterParam(TypedDict, total=False):
    """Filter clause with conditions connected by logical operators.

    Conditions are evaluated left-to-right without precedence (no nesting/parentheses).
    Example: condition1 AND condition2 OR condition3 evaluates as ((condition1 AND condition2) OR condition3)

    Example:
        {
            "conditions": [
                {"column": "score", "operator": ">", "value": 0.5},
                {"column": "category", "operator": "=", "value": "test"}
            ],
            "logicalOperators": ["AND"]
        }
    """

    conditions: Required[Iterable[Condition]]

    logical_operators: Annotated[List[Literal["AND", "OR"]], PropertyInfo(alias="logicalOperators")]
    """Logical operators connecting conditions. Length must be len(conditions) - 1"""
