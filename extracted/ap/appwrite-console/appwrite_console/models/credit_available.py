from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class CreditAvailable(AppwriteModel):
    """
    CreditAvailable

    Attributes
    ----------
    available : float
        Total available credits for the organization.
    """

    available: float = Field(..., alias='available')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'available' not in data:
            data['available'] = 0
        return data
