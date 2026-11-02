from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .usage_metric import UsageMetric


class UsageGaugeList(AppwriteModel):
    """
    usageGaugeList

    Attributes
    ----------
    interval : str
        Requested interval, or an empty string for a flat aggregate.
    metrics : List[UsageMetric]
        One series per requested gauge metric.
    """

    interval: str = Field(..., alias='interval')
    metrics: List[UsageMetric] = Field(..., alias='metrics')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'interval' not in data:
            data['interval'] = ''
        if 'metrics' not in data:
            data['metrics'] = []
        return data
