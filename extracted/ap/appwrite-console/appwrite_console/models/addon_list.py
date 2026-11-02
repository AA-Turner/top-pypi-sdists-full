from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .addon import Addon


class AddonList(AppwriteModel):
    """
    Addons list

    Attributes
    ----------
    total : float
        Total number of addons that matched your query.
    addons : List[Addon]
        List of addons.
    """

    total: float = Field(..., alias='total')
    addons: List[Addon] = Field(..., alias='addons')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'addons' not in data:
            data['addons'] = []
        return data
