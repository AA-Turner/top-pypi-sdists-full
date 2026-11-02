from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class TemplateVariable(AppwriteModel):
    """
    Template Variable

    Attributes
    ----------
    name : str
        Variable Name.
    description : str
        Variable Description.
    value : str
        Variable Value.
    secret : bool
        Variable secret flag. Secret variables can only be updated or deleted, but never read.
    placeholder : str
        Variable Placeholder.
    required : bool
        Is the variable required?
    type : str
        Variable Type.
    """

    name: str = Field(..., alias='name')
    description: str = Field(..., alias='description')
    value: str = Field(..., alias='value')
    secret: bool = Field(..., alias='secret')
    placeholder: str = Field(..., alias='placeholder')
    required: bool = Field(..., alias='required')
    type: str = Field(..., alias='type')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'name' not in data:
            data['name'] = ''
        if 'description' not in data:
            data['description'] = ''
        if 'value' not in data:
            data['value'] = ''
        if 'secret' not in data:
            data['secret'] = False
        if 'placeholder' not in data:
            data['placeholder'] = ''
        if 'required' not in data:
            data['required'] = False
        if 'type' not in data:
            data['type'] = ''
        return data
