from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .credit import Credit


class CreditList(AppwriteModel):
    """
    CreditList

    Attributes
    ----------
    credits : List[Credit]
        Credits
    total : float
        Total number of credits
    available : float
        Total available credit balance in USD
    """

    credits: List[Credit] = Field(..., alias='credits')
    total: float = Field(..., alias='total')
    available: float = Field(..., alias='available')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'credits' not in data:
            data['credits'] = []
        if 'total' not in data:
            data['total'] = 0
        if 'available' not in data:
            data['available'] = 0
        return data
