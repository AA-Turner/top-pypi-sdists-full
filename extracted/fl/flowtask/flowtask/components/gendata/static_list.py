"""Static list rule handler for GenData.

Generates a pandas Series from an inline list of values defined in YAML.
"""
from typing import Any, List, Union

import pandas as pd
from pydantic import BaseModel, Field


class StaticListRule(BaseModel):
    """Rule for generating a Series from a static list of values.

    Attributes:
        type: Rule type identifier, must be 'static_list'.
        column_name: Name of the output Series/column.
        values: List of values to include in the Series.
    """

    type: str = Field("static_list", description="Rule type identifier")
    column_name: str = Field(..., description="Name of the output column")
    values: List[Any] = Field(..., description="List of values")


def generate_static_list(rule: Union[StaticListRule, dict]) -> pd.Series:
    """Generate a Series from a static list of values.

    Args:
        rule: A StaticListRule instance or a dict with the same fields.

    Returns:
        A pd.Series named after rule.column_name containing the values.
    """
    if isinstance(rule, dict):
        rule = StaticListRule(**rule)

    return pd.Series(rule.values, name=rule.column_name)
