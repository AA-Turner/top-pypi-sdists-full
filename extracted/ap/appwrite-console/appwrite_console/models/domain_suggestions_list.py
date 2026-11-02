from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel
from .domain_suggestion import DomainSuggestion


class DomainSuggestionsList(AppwriteModel):
    """
    Domain suggestions list

    Attributes
    ----------
    total : float
        Total number of suggestions that matched your query.
    suggestions : List[DomainSuggestion]
        List of suggestions.
    """

    total: float = Field(..., alias='total')
    suggestions: List[DomainSuggestion] = Field(..., alias='suggestions')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'total' not in data:
            data['total'] = 0
        if 'suggestions' not in data:
            data['suggestions'] = []
        return data
