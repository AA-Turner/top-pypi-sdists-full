from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .usage_data_point import UsageDataPoint


class UsageMetric(AppwriteModel):
    """
    usageMetric

    Attributes
    ----------
    metric : str
        Metric key this series describes.
    points : List[UsageDataPoint]
        Data points in the requested order.
    """

    metric: str = Field(..., alias='metric')
    points: List[UsageDataPoint] = Field(..., alias='points')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'metric' not in data:
            data['metric'] = ''
        if 'points' not in data:
            data['points'] = []
        return data
