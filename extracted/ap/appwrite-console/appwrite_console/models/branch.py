from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Branch(AppwriteModel):
    """
    Branch

    Attributes
    ----------
    name : str
        Branch Name.
    """

    name: str = Field(..., alias='name')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'name' not in data:
            data['name'] = ''
        return data
