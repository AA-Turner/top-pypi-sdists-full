# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["SelectItem", "Expression", "ExpressionColumn", "ExpressionAggregation"]


class ExpressionColumn(BaseModel):
    """Reference to a column from evaluation_items.data

    Example:
        {"type": "COLUMN", "column": "category"}
    """

    column: str
    """Column name from evaluation_items.data"""

    source: Optional[str] = None
    """Column source: 'data' or 'task_result_cache'"""

    type: Optional[Literal["COLUMN"]] = None


class ExpressionAggregation(BaseModel):
    """Aggregation function to apply

    Examples:
        {"type": "AGGREGATION", "function": "AVG", "column": "score"}
        {"type": "AGGREGATION", "function": "COUNT", "column": "*"}
        {"type": "AGGREGATION", "function": "PERCENTILE", "column": "score", "params": {"percentile": 95}}
    """

    column: str
    """Column to aggregate, or '_' for COUNT(_)"""

    function: Literal[
        "COUNT", "SUM", "AVG", "MIN", "MAX", "STDDEV", "VARIANCE", "PERCENTILE", "COUNT_DISTINCT", "PERCENTAGE"
    ]
    """Supported aggregation functions"""

    evaluation_ids: Optional[List[str]] = None
    """
    Optional subset of evaluation IDs for per-aggregation filtering in evaluation
    group dashboards.
    """

    params: Optional[Dict[str, object]] = None
    """
    Function parameters (e.g., {'percentile': 95} for PERCENTILE,
    {'percentage_filters': Filter} for PERCENTAGE)
    """

    source: Optional[str] = None
    """Column source: 'data' or 'task_result_cache'"""

    type: Optional[Literal["AGGREGATION"]] = None


Expression: TypeAlias = Union[ExpressionColumn, ExpressionAggregation]


class SelectItem(BaseModel):
    """Column in SELECT clause"""

    expression: Expression
    """Reference to a column from evaluation_items.data

    Example: {"type": "COLUMN", "column": "category"}
    """

    alias: Optional[str] = None
    """Optional alias for the selected item"""
