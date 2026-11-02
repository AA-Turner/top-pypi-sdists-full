from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .usage_resources import UsageResources


class AggregationBreakdown(AppwriteModel):
    """
    Breakdown

    Attributes
    ----------
    id : str
        Aggregation ID.
    name : str
        Project name
    region : str
        Project region
    amount : float
        Aggregated amount
    resources : List[UsageResources]
        Typed model field.
    """

    id: str = Field(..., alias='$id')
    name: str = Field(..., alias='name')
    region: str = Field(..., alias='region')
    amount: float = Field(..., alias='amount')
    resources: List[UsageResources] = Field(..., alias='resources')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'name' not in data:
            data['name'] = ''
        if 'region' not in data:
            data['region'] = 'fra'
        if 'amount' not in data:
            data['amount'] = 0
        if 'resources' not in data:
            data['resources'] = []
        return data
