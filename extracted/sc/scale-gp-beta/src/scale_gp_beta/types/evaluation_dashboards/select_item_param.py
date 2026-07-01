# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = ["SelectItemParam", "Expression", "ExpressionColumn", "ExpressionAggregation"]


class ExpressionColumn(TypedDict, total=False):
    """Reference to a column from evaluation_items.data

    Example:
        {"type": "COLUMN", "column": "category"}
    """

    column: Required[str]
    """Column name from evaluation_items.data"""

    source: str
    """Column source: 'data' or 'task_result_cache'"""

    type: Literal["COLUMN"]


class ExpressionAggregation(TypedDict, total=False):
    """Aggregation function to apply

    Examples:
        {"type": "AGGREGATION", "function": "AVG", "column": "score"}
        {"type": "AGGREGATION", "function": "COUNT", "column": "*"}
        {"type": "AGGREGATION", "function": "PERCENTILE", "column": "score", "params": {"percentile": 95}}
    """

    column: Required[str]
    """Column to aggregate, or '_' for COUNT(_)"""

    function: Required[
        Literal["COUNT", "SUM", "AVG", "MIN", "MAX", "STDDEV", "VARIANCE", "PERCENTILE", "COUNT_DISTINCT", "PERCENTAGE"]
    ]
    """Supported aggregation functions"""

    evaluation_ids: SequenceNotStr[str]
    """
    Optional subset of evaluation IDs for per-aggregation filtering in evaluation
    group dashboards.
    """

    params: Dict[str, object]
    """
    Function parameters (e.g., {'percentile': 95} for PERCENTILE,
    {'percentage_filters': Filter} for PERCENTAGE)
    """

    source: str
    """Column source: 'data' or 'task_result_cache'"""

    type: Literal["AGGREGATION"]


Expression: TypeAlias = Union[ExpressionColumn, ExpressionAggregation]


class SelectItemParam(TypedDict, total=False):
    """Column in SELECT clause"""

    expression: Required[Expression]
    """Reference to a column from evaluation_items.data

    Example: {"type": "COLUMN", "column": "category"}
    """

    alias: str
    """Optional alias for the selected item"""
