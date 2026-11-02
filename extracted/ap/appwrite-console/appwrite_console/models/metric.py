from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Metric(AppwriteModel):
    """
    Metric

    Attributes
    ----------
    value : float
        The value of this metric at the timestamp.
    date : str
        The date at which this metric was aggregated in ISO 8601 format.
    """

    value: float = Field(..., alias='value')
    date: str = Field(..., alias='date')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'value' not in data:
            data['value'] = -1
        if 'date' not in data:
            data['date'] = ''
        return data
