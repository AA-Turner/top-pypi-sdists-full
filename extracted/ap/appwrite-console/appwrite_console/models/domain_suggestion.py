from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class DomainSuggestion(AppwriteModel):
    """
    DomainSuggestion

    Attributes
    ----------
    domain : str
        Domain suggestion.
    premium : bool
        Is the domain premium?
    price : Optional[float]
        Domain price.
    available : bool
        Is the domain available?
    """

    domain: str = Field(..., alias='domain')
    premium: bool = Field(..., alias='premium')
    price: Optional[float] = Field(default=None, alias='price')
    available: bool = Field(..., alias='available')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'domain' not in data:
            data['domain'] = ''
        if 'premium' not in data:
            data['premium'] = False
        if 'available' not in data:
            data['available'] = False
        return data
