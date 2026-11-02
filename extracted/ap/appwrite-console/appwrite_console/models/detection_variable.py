from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class DetectionVariable(AppwriteModel):
    """
    DetectionVariable

    Attributes
    ----------
    name : str
        Name of environment variable
    value : str
        Value of environment variable
    """

    name: str = Field(..., alias='name')
    value: str = Field(..., alias='value')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'name' not in data:
            data['name'] = ''
        if 'value' not in data:
            data['value'] = ''
        return data
