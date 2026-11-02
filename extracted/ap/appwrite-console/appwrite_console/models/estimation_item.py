from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class EstimationItem(AppwriteModel):
    """
    Item

    Attributes
    ----------
    label : str
        Label
    value : float
        Gross payable amount
    """

    label: str = Field(..., alias='label')
    value: float = Field(..., alias='value')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'label' not in data:
            data['label'] = ''
        if 'value' not in data:
            data['value'] = 0
        return data
