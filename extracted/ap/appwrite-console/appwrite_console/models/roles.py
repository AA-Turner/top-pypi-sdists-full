from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Roles(AppwriteModel):
    """
    Roles

    Attributes
    ----------
    scopes : List[Any]
        Array of scopes accessible to current user.
    roles : List[Any]
        Array of roles assigned to current user.
    """

    scopes: List[Any] = Field(..., alias='scopes')
    roles: List[Any] = Field(..., alias='roles')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'scopes' not in data:
            data['scopes'] = []
        if 'roles' not in data:
            data['roles'] = []
        return data
