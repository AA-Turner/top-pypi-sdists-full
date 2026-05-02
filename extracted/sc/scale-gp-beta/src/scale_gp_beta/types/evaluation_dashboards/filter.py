# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Filter", "Condition"]


class Condition(BaseModel):
    """Single filter condition comparing a column to a value.

    Example:
        {"column": "score", "operator": ">", "value": 0.5}
        {"column": "category", "operator": "=", "value": "test"}
    """

    column: str
    """Column name to filter on"""

    operator: Literal["=", "!=", ">", "<", ">=", "<=", "IN", "NOT IN", "LIKE", "NOT LIKE", "IS NULL", "IS NOT NULL"]
    """Comparison operator"""

    source: Optional[str] = None
    """Column source: 'data' or 'task_result_cache'"""

    value: Union[str, float, bool, List[object], None] = None
    """Value to compare against. Not required for IS NULL / IS NOT NULL operators."""


class Filter(BaseModel):
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

    conditions: List[Condition]

    logical_operators: Optional[List[Literal["AND", "OR"]]] = FieldInfo(alias="logicalOperators", default=None)
    """Logical operators connecting conditions. Length must be len(conditions) - 1"""
