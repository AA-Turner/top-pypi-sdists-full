from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class ConsoleKeyScope(AppwriteModel):
    """
    Console Key Scope

    Attributes
    ----------
    id : str
        Scope ID.
    description : str
        Scope description.
    category : str
        Scope category.
    deprecated : bool
        Scope is deprecated.
    """

    id: str = Field(..., alias='$id')
    description: str = Field(..., alias='description')
    category: str = Field(..., alias='category')
    deprecated: bool = Field(..., alias='deprecated')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '$id' not in data and 'id' not in data:
            data['$id'] = ''
        if 'description' not in data:
            data['description'] = ''
        if 'category' not in data:
            data['category'] = ''
        if 'deprecated' not in data:
            data['deprecated'] = False
        return data
